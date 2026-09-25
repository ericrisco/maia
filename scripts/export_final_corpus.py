#!/usr/bin/env python3
"""Exporta només decisions aprovades amb staging i recuperació de transacció.

python scripts/export_final_corpus.py --write
python scripts/export_final_corpus.py --check
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

import build_final_manifest as manifest
from curacio_corpus import InventoryError


class ExportError(ValueError):
    """No es pot reproduir o substituir l'exportació amb seguretat."""


STATIC_FILES = ("README.md", "coneixement/README.md", "llengua/README.md")


def expected_files(project_root: Path) -> dict[str, bytes]:
    expected: dict[str, bytes] = {}
    for unit_id, decision in manifest.approved_decisions(project_root):
        _, _, content = manifest.validate_decision_source(project_root, unit_id, decision)
        relative = decision["export_path"]
        category = "coneixement" if decision["destination"] == "knowledge" else "llengua"
        parts = Path(relative).parts
        if (
            not parts
            or parts[0] != category
            or Path(relative).is_absolute()
            or ".." in parts
            or not relative.endswith(".md")
        ):
            raise ExportError(f"{unit_id}: export_path invàlid: {relative}")
        if relative in expected:
            raise ExportError(f"export_path duplicat: {relative}")
        expected[relative] = content
    return expected


def actual_content_files(root: Path) -> dict[str, bytes]:
    actual: dict[str, bytes] = {}
    for category in ("coneixement", "llengua"):
        directory = root / category
        if not directory.is_dir():
            raise ExportError(f"falta el directori {category}/")
        for path in sorted(directory.rglob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            actual[path.relative_to(root).as_posix()] = path.read_bytes()
    return actual


def compare(root: Path, project_root: Path) -> None:
    expected = expected_files(project_root)
    actual = actual_content_files(root)
    if expected != actual:
        changed = sorted(
            path for path in set(actual) & set(expected) if actual[path] != expected[path]
        )
        raise ExportError(
            f"contingut exportat divergeix: extra={sorted(set(actual) - set(expected))}, "
            f"missing={sorted(set(expected) - set(actual))}, "
            f"changed={changed}"
        )
    try:
        expected_manifest = manifest.render(root, project_root)
    except (manifest.ManifestError, InventoryError, OSError, UnicodeError) as exc:
        raise ExportError(str(exc)) from exc
    manifest_path = root / "manifest.jsonl"
    if not manifest_path.is_file() or manifest_path.read_bytes() != expected_manifest:
        raise ExportError("manifest absent o diferent de les decisions i els fitxers exportats")


def preserve_static_files(root: Path, staging: Path) -> None:
    for relative in STATIC_FILES:
        source = root / relative
        if source.is_file():
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    (staging / "coneixement").mkdir(parents=True, exist_ok=True)
    (staging / "llengua").mkdir(parents=True, exist_ok=True)


def validate_existing_tree(root: Path) -> None:
    project_root = root.parent
    actual_files = {
        path.relative_to(root).as_posix(): path for path in root.rglob("*") if path.is_file()
    }
    expected_paths = set(expected_files(project_root))
    allowed = set(STATIC_FILES) | {"manifest.jsonl"} | expected_paths
    extras = set(actual_files) - allowed
    if extras:
        raise ExportError(
            "exportació actual conté fitxers fora del flux; es conserva intacta: "
            + ", ".join(sorted(extras)[:5])
        )
    content_paths = set(actual_content_files(root))
    if content_paths:
        manifest_path = root / "manifest.jsonl"
        try:
            rows = [
                json.loads(line) for line in manifest_path.read_text(encoding="utf-8").splitlines()
            ]
            old_records = rows[1:]
            recorded = {
                item.get("exported_path", item.get("path")): item.get(
                    "exported_sha256", item.get("content_sha256")
                )
                for item in old_records
                if isinstance(item, dict)
            }
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ExportError(
                "no es pot validar l'exportació anterior; es conserva intacta"
            ) from exc
        if set(recorded) != content_paths:
            raise ExportError(
                "l'exportació anterior no coincideix amb el manifest; es conserva intacta"
            )
        for relative, path in actual_files.items():
            if relative in content_paths and manifest.sha256_file(path) != recorded[relative]:
                raise ExportError(
                    f"fitxer exportat modificat fora del flux, es conserva intacte: {relative}"
                )


def transaction_path(project_root: Path) -> Path:
    return project_root / "docs" / "raw" / "curacio" / "export-transaction.json"


def recover(project_root: Path) -> None:
    journal = transaction_path(project_root)
    if not journal.exists():
        return
    state = json.loads(journal.read_text(encoding="utf-8"))
    root = project_root / "final-corpus"
    backup_name = state.get("backup")
    if not isinstance(backup_name, str) or not backup_name.startswith(".final-corpus-backup-"):
        raise ExportError("registre de transacció invàlid; còpia anterior no s'ha tocat")
    backup = project_root / backup_name
    if not root.exists() and backup.exists():
        backup.replace(root)
    elif root.exists() and backup.exists():
        shutil.rmtree(backup)
    elif not root.exists() and not backup.exists():
        raise ExportError("registre de transacció sense corpus ni còpia recuperable")
    journal.unlink(missing_ok=True)


def write(project_root: Path) -> None:
    root = project_root / "final-corpus"
    recover(project_root)
    if root.exists():
        validate_existing_tree(root)
    stage = Path(tempfile.mkdtemp(prefix=".final-corpus-stage-", dir=project_root))
    backup: Path | None = None
    try:
        preserve_static_files(root, stage)
        for relative, content in expected_files(project_root).items():
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        (stage / "manifest.jsonl").write_bytes(manifest.render(stage, project_root))
        compare(stage, project_root)

        if root.exists():
            backup = Path(tempfile.mkdtemp(prefix=".final-corpus-backup-", dir=project_root))
            backup.rmdir()
            journal = transaction_path(project_root)
            journal_tmp = journal.with_suffix(".tmp")
            journal_tmp.write_text(
                json.dumps({"backup": backup.name}, sort_keys=True) + "\n", encoding="utf-8"
            )
            journal_tmp.replace(journal)
            root.replace(backup)
        try:
            stage.replace(root)
        except OSError:
            if backup is not None and backup.exists() and not root.exists():
                backup.replace(root)
                transaction_path(project_root).unlink(missing_ok=True)
            raise
        if backup is not None:
            shutil.rmtree(backup)
            transaction_path(project_root).unlink(missing_ok=True)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    compare(root, project_root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--write", action="store_true", help="construeix staging i substitueix l'exportació"
    )
    group.add_argument(
        "--check", action="store_true", help="comprova exportació, manifest i decisions"
    )
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parent.parent
    try:
        recover(project_root)
        if args.write:
            write(project_root)
        else:
            compare(project_root / "final-corpus", project_root)
    except (
        ExportError,
        manifest.ManifestError,
        InventoryError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    count = len(expected_files(project_root))
    print(f"ok · exportació reproduïble de {count} unitats", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
