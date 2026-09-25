#!/usr/bin/env python3
"""Genera un inventari traçable dels fitxers sota ``docs/``.

Les unitats no revisades queden pendents per defecte. Les decisions humanes
van a ``docs/raw/curacio/decisions.jsonl`` i no es perden en regenerar
``inventory.jsonl``.

    python scripts/curacio_corpus.py --write
    python scripts/curacio_corpus.py --check
    python scripts/curacio_corpus.py --self-test
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

STATUSES = {"unreviewed", "in_review", "approved", "pending", "excluded"}
DESTINATIONS = {"knowledge", "language", "none"}
ROOT_META = {
    "CONTRACT.md",
    "el-cervell-andorra-index-del-corpus.md",
    "index.md",
    "registre-de-canvis.md",
}


class InventoryError(ValueError):
    """Una decisió o una unitat d'inventari no és vàlida."""


def validate_decision(
    decision: Any,
    line_number: int,
    seen: set[str],
    source: str,
) -> dict[str, Any]:
    if not isinstance(decision, dict):
        raise InventoryError(f"{source}:{line_number}: cada decisió ha de ser un objecte")
    unit_id = decision.get("unit_id")
    status = decision.get("status")
    rationale = decision.get("rationale")
    if not isinstance(unit_id, str) or not unit_id.strip():
        raise InventoryError(f"{source}:{line_number}: falta unit_id")
    if unit_id in seen:
        raise InventoryError(f"{source}:{line_number}: unit_id duplicat: {unit_id}")
    if status not in STATUSES:
        raise InventoryError(
            f"{source}:{line_number}: status ha de ser unreviewed, in_review, approved, "
            "pending o excluded"
        )
    if not isinstance(rationale, str) or not rationale.strip():
        raise InventoryError(f"{source}:{line_number}: falta rationale no buida")
    evidence = decision.get("evidence", [])
    if not isinstance(evidence, list) or any(
        not isinstance(item, str) or not item.strip() for item in evidence
    ):
        raise InventoryError(f"{source}:{line_number}: evidence ha de ser una llista de textos")
    destination = decision.get("destination", "none")
    if destination not in DESTINATIONS:
        raise InventoryError(
            f"{source}:{line_number}: destination ha de ser knowledge, language o none"
        )
    input_sha256 = decision.get("input_sha256")
    if input_sha256 is not None and (
        not isinstance(input_sha256, str)
        or len(input_sha256) != 64
        or any(char not in "0123456789abcdef" for char in input_sha256)
    ):
        raise InventoryError(f"{source}:{line_number}: input_sha256 ha de ser SHA-256 hexadecimal")
    if status == "approved" and (destination == "none" or input_sha256 is None):
        raise InventoryError(
            f"{source}:{line_number}: una aprovació necessita destí i hash de la versió revisada"
        )
    optional_strings = (
        "batch_id",
        "source_fragment",
        "language",
        "text_type",
        "reviewer",
        "reviewed_at",
    )
    for key in optional_strings:
        value = decision.get(key)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise InventoryError(f"{source}:{line_number}: {key} ha de ser text no buit")
    optional_lists = (
        "review_methods",
        "source_ids",
        "source_locators",
        "terms_evidence",
        "transformations",
    )
    for key in optional_lists:
        value = decision.get(key, [])
        if not isinstance(value, list) or any(
            not isinstance(item, str) or not item.strip() for item in value
        ):
            raise InventoryError(
                f"{source}:{line_number}: {key} ha de ser una llista de textos no buits"
            )
    human_reviewed = decision.get("human_reviewed", False)
    if not isinstance(human_reviewed, bool):
        raise InventoryError(f"{source}:{line_number}: human_reviewed ha de ser booleà")
    reference_date = decision.get("reference_date")
    if reference_date is not None and not isinstance(reference_date, str):
        raise InventoryError(f"{source}:{line_number}: reference_date ha de ser text o nul")
    duplicate_group = decision.get("duplicate_group")
    if duplicate_group is not None and (
        not isinstance(duplicate_group, str) or not duplicate_group.strip()
    ):
        raise InventoryError(
            f"{source}:{line_number}: duplicate_group ha de ser text no buit o nul"
        )
    export_path = decision.get("export_path")
    if export_path is not None and (not isinstance(export_path, str) or not export_path.strip()):
        raise InventoryError(f"{source}:{line_number}: export_path ha de ser text no buit o nul")
    if export_path is not None:
        export_parts = Path(export_path).parts
        expected_folder = "coneixement" if destination == "knowledge" else "llengua"
        if (
            Path(export_path).is_absolute()
            or ".." in export_parts
            or not export_parts
            or export_parts[0] != expected_folder
        ):
            raise InventoryError(
                f"{source}:{line_number}: export_path ha de quedar sota {expected_folder}/"
            )
    if status == "approved" and export_path is None:
        raise InventoryError(f"{source}:{line_number}: una aprovació necessita export_path")
    seen.add(unit_id)
    parsed = {
        "status": status,
        "rationale": rationale.strip(),
        "evidence": evidence,
        "destination": destination,
        "input_sha256": input_sha256,
    }
    for key in (
        *optional_strings,
        *optional_lists,
        "human_reviewed",
        "reference_date",
        "duplicate_group",
        "export_path",
    ):
        if key in decision:
            parsed[key] = decision[key]
    return parsed


def parse_decisions(path: Path) -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return decisions
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            decision = json.loads(line)
        except json.JSONDecodeError as exc:
            raise InventoryError(f"{path}:{line_number}: JSON invàlid: {exc.msg}") from exc
        if not isinstance(decision, dict):
            raise InventoryError(f"{path}:{line_number}: cada decisió ha de ser un objecte")
        unit_id = decision.get("unit_id")
        parsed = validate_decision(decision, line_number, set(decisions), str(path))
        decisions[unit_id] = parsed
    return decisions


def parse_baseline(path: Path) -> dict[str, dict[str, Any]]:
    """Llegeix la fotografia immutable que fixa l'abast inicial."""
    baseline: dict[str, dict[str, Any]] = {}
    if not path.is_file():
        raise InventoryError(f"falta la fotografia inicial immutable: {path}")
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise InventoryError(f"{path}:{line_number}: JSON invàlid: {exc.msg}") from exc
        if line_number == 1:
            if not isinstance(row, dict) or row.get("schema") != "maia-corpus-inventory/v2":
                raise InventoryError(f"{path}: esquema de fotografia inicial desconegut")
            continue
        if not isinstance(row, dict):
            raise InventoryError(f"{path}:{line_number}: cada unitat ha de ser un objecte")
        unit_id = row.get("unit_id")
        digest = row.get("sha256")
        valid_digest = (isinstance(digest, str) and len(digest) == 64) or (
            digest is None and row.get("kind") == "symlink"
        )
        if not isinstance(unit_id, str) or not valid_digest or unit_id in baseline:
            raise InventoryError(f"{path}:{line_number}: identificador absent o duplicat")
        baseline[unit_id] = row
    return baseline


def frontmatter(path: Path) -> dict[str, Any]:
    if path.suffix.lower() != ".md":
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) < 3 or lines[0] != "---":
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        detail = str(exc).splitlines()[0]
        mark = getattr(exc, "problem_mark", None)
        if mark is not None:
            detail += f" at frontmatter line {mark.line + 1}, column {mark.column + 1}"
        return {"_parse_error": detail}
    return data if isinstance(data, dict) else {}


def classify(path: Path, relative: str, metadata: dict[str, Any]) -> tuple[str, str, str]:
    parts = Path(relative).parts
    if parts and parts[0] == "temes" and metadata.get("type") == "article":
        destination = "knowledge"
    elif parts and parts[0] == "parla" and metadata.get("type") == "parla":
        destination = "language"
    else:
        destination = "none"
    if relative.startswith("raw/curacio/") or relative in ROOT_META:
        return "excluded", "fitxer de control, índex o documentació del projecte", "none"
    if "_parse_error" in metadata:
        return "pending", "frontmatter invàlid; revisar abans de seleccionar la unitat", destination
    if relative.startswith(".obsidian/"):
        return "excluded", "configuració d'Obsidian, fora del corpus de contingut", "none"
    if path.name == ".DS_Store" or path.suffix.lower() in {".pyc", ".pyo"}:
        return "excluded", "fitxer auxiliar del sistema o bytecode", "none"
    if metadata.get("type") == "index" or "index" in path.stem.lower():
        return "excluded", "índex de navegació, no unitat de coneixement", "none"
    if path.suffix.lower() in {".py", ".sh", ".log"}:
        return "excluded", "codi o registre tècnic, no contingut d'entrenament", "none"
    if destination == "none":
        return "excluded", "no és un article ni una unitat de parla seleccionable", "none"
    return "unreviewed", "unitat candidata encara no revisada per contingut i drets", destination


def domain_for(path: Path, relative: str) -> str:
    parts = Path(relative).parts
    if len(parts) > 1 and parts[0] == "temes":
        return parts[1]
    if len(parts) > 1 and parts[0] == "parla":
        return parts[1]
    if parts and parts[0] in {"fonts", "raw"}:
        return parts[0]
    return "project-meta"


def source_group(relative: str) -> str | None:
    parts = Path(relative).parts
    if not parts or parts[0] != "raw":
        return None
    return "/".join(parts[:-1]) or "raw"


def unit(path: Path, docs: Path, decisions: dict[str, dict[str, Any]]) -> dict[str, Any]:
    relative = path.relative_to(docs).as_posix()
    unit_id = f"maia-docs/{relative}"
    metadata = frontmatter(path)
    status, rationale, destination = classify(path, relative, metadata)
    evidence: list[str] = []
    if unit_id in decisions:
        decision = decisions[unit_id]
        status = decision["status"]
        rationale = decision["rationale"]
        evidence = decision["evidence"]
        destination = decision["destination"]
        reviewed_sha256 = decision["input_sha256"]
        review = {
            key: value
            for key, value in decision.items()
            if key not in {"status", "rationale", "evidence", "destination", "input_sha256"}
        }
    else:
        reviewed_sha256 = None
        review = {}
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as file:
        while chunk := file.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    source = metadata.get("font", metadata.get("source"))
    return {
        "unit_id": unit_id,
        "path": f"docs/{relative}",
        "kind": metadata.get("type", path.suffix.lower().lstrip(".") or "file"),
        "domain": domain_for(path, relative),
        "source_group": source_group(relative),
        "source_slug": source if isinstance(source, str) else None,
        "metadata_issue": metadata.get("_parse_error"),
        "size_bytes": size,
        "sha256": digest.hexdigest(),
        "status": status,
        "rationale": rationale,
        "evidence": evidence,
        "destination": destination,
        "reviewed_sha256": reviewed_sha256,
        "review": review,
    }


def build_inventory(
    docs: Path,
    decisions: dict[str, dict[str, Any]],
    baseline: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    paths: list[Path] = []
    symlinks: list[Path] = []
    for current, dirs, files in os.walk(docs, followlinks=False):
        current_path = Path(current)
        if current_path.relative_to(docs).as_posix() == "raw/curacio":
            dirs[:] = []
            continue
        kept_dirs = []
        for name in sorted(dirs):
            child = current_path / name
            if child.is_symlink():
                symlinks.append(child)
            else:
                kept_dirs.append(name)
        dirs[:] = kept_dirs
        paths.extend(current_path / name for name in sorted(files))

    rows = [
        unit(path, docs, decisions) for path in paths if path.is_file() and not path.is_symlink()
    ]
    for path in symlinks:
        relative = path.relative_to(docs).as_posix()
        rows.append(
            {
                "unit_id": f"maia-docs/{relative}",
                "path": f"docs/{relative}",
                "kind": "symlink",
                "domain": domain_for(path, relative),
                "source_group": source_group(relative),
                "source_slug": None,
                "metadata_issue": None,
                "size_bytes": None,
                "sha256": None,
                "status": "excluded",
                "rationale": "enllaç simbòlic; no se segueix ni s'inclou el destí",
                "evidence": [],
                "destination": "none",
            }
        )
    rows.sort(key=lambda item: item["path"])
    known = {row["unit_id"] for row in rows}
    stale = sorted(set(decisions) - known)
    if stale:
        raise InventoryError("decisions amb unit_id inexistent: " + ", ".join(stale[:5]))

    for row in rows:
        original = baseline.get(row["unit_id"])
        row["scope"] = "initial" if original else "post-freeze"
        row["baseline_sha256"] = original.get("sha256") if original else None
        if original is None:
            row["drift"] = "new"
            if row["destination"] != "none":
                row["status"] = "pending"
                row["rationale"] = (
                    "incorporat després de fixar l'abast inicial; pendent de revisió separada"
                )
        elif original.get("sha256") != row.get("sha256"):
            row["drift"] = "modified"
            if row["reviewed_sha256"] != row["sha256"]:
                row["status"] = "pending"
                row["rationale"] = (
                    "el hash ha canviat des de la fotografia inicial; revisió pendent"
                )
        else:
            row["drift"] = "unchanged"
    for unit_id, original in baseline.items():
        if unit_id in known:
            continue
        missing = dict(original)
        missing.update(
            {
                "scope": "initial",
                "baseline_sha256": original.get("sha256"),
                "drift": "missing",
                "status": "pending",
                "rationale": "unitat de la fotografia inicial absent del corpus actual",
                "evidence": [],
            }
        )
        rows.append(missing)
    rows.sort(key=lambda item: item["path"])
    return rows


def render(rows: list[dict[str, Any]]) -> bytes:
    header = {
        "schema": "maia-corpus-inventory/v2",
        "description": (
            "Una línia JSON per fitxer o enllaç simbòlic sota docs/; "
            "la fotografia inicial fixa l'abast i els canvis queden pendents."
        ),
    }
    lines = [json.dumps(header, ensure_ascii=False, sort_keys=True)]
    lines.extend(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    return ("\n".join(lines) + "\n").encode("utf-8")


def self_test() -> None:
    valid = {
        "unit_id": "maia-docs/temes/a.md",
        "status": "approved",
        "destination": "knowledge",
        "input_sha256": "a" * 64,
        "export_path": "coneixement/a.md",
        "rationale": "llicència i evidència",
        "evidence": ["font#article-1"],
    }
    assert validate_decision(valid, 1, set(), "self-test")["status"] == "approved"
    assert (
        classify(Path("article.md"), "temes/historia/article.md", {"type": "article"})[0]
        == "unreviewed"
    )
    assert classify(Path("index.md"), "temes/historia/index.md", {"type": "index"})[0] == "excluded"
    invalid_cases = [
        {"unit_id": "x", "status": "unknown", "rationale": "motiu"},
        {"unit_id": "x", "status": "approved", "rationale": " "},
        {
            "unit_id": "x",
            "status": "approved",
            "rationale": "sense hash",
            "destination": "knowledge",
        },
        {"unit_id": "x", "status": "pending", "rationale": "motiu", "evidence": "url"},
        {"unit_id": "x", "status": "approved", "rationale": "motiu", "destination": "maybe"},
        {
            "unit_id": "x",
            "status": "approved",
            "rationale": "motiu",
            "destination": "knowledge",
            "input_sha256": "a" * 64,
            "export_path": "coneixement/../../fora.md",
        },
    ]
    for case in invalid_cases:
        try:
            validate_decision(case, 1, set(), "self-test")
        except InventoryError:
            continue
        raise AssertionError(f"self-test: decisió invàlida acceptada: {case}")
    try:
        validate_decision(valid, 1, {valid["unit_id"]}, "self-test")
    except InventoryError:
        pass
    else:
        raise AssertionError("self-test: decisió duplicada acceptada")
    print("ok · decisió vàlida acceptada; sis decisions invàlides rebutjades")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true", help="genera inventory.jsonl")
    group.add_argument(
        "--check", action="store_true", help="comprova que inventory.jsonl coincideix"
    )
    group.add_argument(
        "--self-test",
        action="store_true",
        help="comprova els casos vàlids i invàlids del contracte",
    )
    parser.add_argument(
        "--docs", type=Path, default=Path("docs"), help="carpeta de documents d'entrada"
    )
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0

    docs = args.docs.resolve()
    if not docs.is_dir():
        print(f"no hi ha cap directori {docs}", file=sys.stderr)
        return 2
    curation = docs / "raw" / "curacio"
    curation.mkdir(parents=True, exist_ok=True)
    decisions_path = curation / "decisions.jsonl"
    decisions_path.touch(exist_ok=True)
    baseline_path = curation / "initial-inventory.jsonl"
    output = curation / "inventory.jsonl"
    try:
        decisions = parse_decisions(decisions_path)
        baseline = parse_baseline(baseline_path)
        rows = build_inventory(docs, decisions, baseline)
    except (InventoryError, OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    data = render(rows)
    if args.check:
        if not output.exists() or output.read_bytes() != data:
            print(
                "error: inventory absent o desactualitzat; torna'l a generar amb --write",
                file=sys.stderr,
            )
            return 1
    elif args.write:
        handle, temporary = tempfile.mkstemp(prefix="inventory-", suffix=".tmp", dir=curation)
        try:
            with os.fdopen(handle, "wb") as file:
                file.write(data)
            Path(temporary).replace(output)
        finally:
            Path(temporary).unlink(missing_ok=True)
    else:
        sys.stdout.buffer.write(data)

    counts = Counter(row["status"] for row in rows)
    summary = " ".join(f"{status}={counts[status]}" for status in sorted(STATUSES))
    print(f"ok · {len(rows)} unitats · {summary}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
