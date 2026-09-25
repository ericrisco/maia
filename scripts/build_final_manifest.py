#!/usr/bin/env python3
"""Construeix i valida el manifest des del ledger de curació i l'exportació.

python scripts/build_final_manifest.py --write
python scripts/build_final_manifest.py --check
python scripts/build_final_manifest.py --self-test
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml
from curacio_corpus import InventoryError, parse_decisions


class ManifestError(ValueError):
    """Una unitat no compleix el contracte del corpus final."""


ALLOWED_TRANSFORMS = {"strip_frontmatter", "unwrap_markdown_links"}
VERSION = "maia-curation-v1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def split_frontmatter(text: str, path: Path) -> tuple[dict[str, Any], str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ManifestError(f"{path}: falta frontmatter YAML")
    end = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if end is None:
        raise ManifestError(f"{path}: frontmatter sense tancament")
    try:
        metadata = yaml.safe_load("".join(lines[1:end]))
    except yaml.YAMLError as exc:
        raise ManifestError(f"{path}: frontmatter YAML invàlid: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ManifestError(f"{path}: frontmatter no és un objecte")
    return metadata, "".join(lines[end + 1 :])


def render_content(source_text: str, transformations: list[str], path: Path) -> bytes:
    unknown = set(transformations) - ALLOWED_TRANSFORMS
    if unknown:
        raise ManifestError(f"{path}: transformacions desconegudes: {sorted(unknown)}")
    _, body = split_frontmatter(source_text, path)
    if "strip_frontmatter" not in transformations:
        raise ManifestError(f"{path}: falta declarar strip_frontmatter")
    if "unwrap_markdown_links" in transformations:
        body = re.sub(r"\[([^\]]+)\]\((?:[^()]|\([^)]*\))*\)", r"\1", body)
    body = body.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n"
    if re.search(r"^##? Related\s*$", body, re.MULTILINE | re.IGNORECASE):
        raise ManifestError(f"{path}: secció Related encara és contingut de navegació")
    if re.search(r"\[[^\]]+\]\([^)]+\)", body):
        raise ManifestError(f"{path}: queda un enllaç Markdown sense resoldre")
    if "## Buits registrats" not in body and "type: article" in source_text:
        raise ManifestError(f"{path}: article sense Buits registrats")
    return body.encode("utf-8")


def safe_project_path(project_root: Path, raw: str, label: str) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise ManifestError(f"falta {label}")
    candidate = project_root / raw
    if candidate.is_symlink():
        raise ManifestError(f"{label} no pot ser un enllaç simbòlic: {raw}")
    resolved = candidate.resolve()
    if not resolved.is_relative_to(project_root.resolve()):
        raise ManifestError(f"{label} surt del repositori: {raw}")
    return resolved


def yaml_frontmatter(path: Path) -> dict[str, Any]:
    try:
        metadata, _ = split_frontmatter(path.read_text(encoding="utf-8"), path)
    except (OSError, UnicodeError) as exc:
        raise ManifestError(f"no es pot llegir {path}: {exc}") from exc
    return metadata


def source_card(project_root: Path, slug: str) -> tuple[Path, dict[str, Any]]:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ManifestError(f"identificador de font invàlid: {slug}")
    path = project_root / "docs" / "fonts" / f"{slug}.md"
    if not path.is_file():
        raise ManifestError(f"falta la fitxa de font {path}")
    metadata = yaml_frontmatter(path)
    if metadata.get("type") != "font" or metadata.get("id") != slug:
        raise ManifestError(f"{path}: fitxa no correspon a {slug}")
    if str(metadata.get("redistribucio", "")).strip().lower() not in {"si", "sí", "yes", "true"}:
        raise ManifestError(f"{path}: redistribució no aprovada")
    return path, metadata


def validate_decision_source(
    project_root: Path, unit_id: str, decision: dict[str, Any]
) -> tuple[Path, dict[str, Any], bytes]:
    prefix = "maia-docs/"
    if not unit_id.startswith(prefix):
        raise ManifestError(f"ID d'unitat desconegut: {unit_id}")
    source_path = safe_project_path(project_root, "docs/" + unit_id[len(prefix) :], "original")
    if not source_path.is_file() or source_path.is_symlink():
        raise ManifestError(f"original absent o enllaç simbòlic: {source_path}")
    digest = sha256_file(source_path)
    if digest != decision.get("input_sha256"):
        raise ManifestError(f"{unit_id}: hash original canvia des de la decisió")
    metadata = yaml_frontmatter(source_path)
    destination = decision.get("destination")
    expected_language = (
        metadata.get("veu") == "originaria" and metadata.get("epoca") == "contemporania"
    )
    if metadata.get("apte_llengua") is not expected_language:
        raise ManifestError(f"{unit_id}: apte_llengua no concorda amb veu i època")
    if destination == "knowledge":
        if metadata.get("type") not in {"article", "parla"}:
            raise ManifestError(f"{unit_id}: tipus no elegible per a coneixement")
    elif destination == "language":
        if not (
            metadata.get("type") == "parla"
            and metadata.get("veu") == "originaria"
            and metadata.get("epoca") == "contemporania"
            and metadata.get("apte_llengua") is True
        ):
            raise ManifestError(f"{unit_id}: llengua requereix parla originària contemporània")
    else:
        raise ManifestError(f"{unit_id}: destí no exportable: {destination}")
    transformations = decision.get("transformations", [])
    rendered = render_content(source_path.read_text(encoding="utf-8"), transformations, source_path)
    if destination == "language" and "strip_frontmatter" not in transformations:
        raise ManifestError(f"{unit_id}: transcripció sense transformació declarada")
    return source_path, metadata, rendered


def approved_decisions(project_root: Path) -> list[tuple[str, dict[str, Any]]]:
    path = project_root / "docs" / "raw" / "curacio" / "decisions.jsonl"
    decisions = parse_decisions(path)
    approved = [(unit_id, row) for unit_id, row in decisions.items() if row["status"] == "approved"]
    return sorted(approved)


def _required_decision_fields(unit_id: str, row: dict[str, Any]) -> None:
    required = (
        "batch_id",
        "source_ids",
        "source_locators",
        "source_fragment",
        "language",
        "text_type",
        "review_methods",
        "reviewer",
        "reviewed_at",
        "terms_evidence",
        "transformations",
        "export_path",
    )
    missing = [key for key in required if not row.get(key)]
    if missing:
        raise ManifestError(f"{unit_id}: falten camps de manifest: {', '.join(missing)}")
    if not isinstance(row.get("human_reviewed"), bool):
        raise ManifestError(f"{unit_id}: human_reviewed ha de ser booleà")
    if row.get("duplicate_group") is None:
        raise ManifestError(f"{unit_id}: cal registrar la família de duplicats o declarar-ne cap")
    if row.get("reference_date") is None:
        raise ManifestError(f"{unit_id}: falta reference_date (usa cadena buida si no consta)")


def record(
    project_root: Path,
    root: Path,
    unit_id: str,
    decision: dict[str, Any],
) -> dict[str, Any]:
    _required_decision_fields(unit_id, decision)
    source_path, source_meta, expected_content = validate_decision_source(
        project_root, unit_id, decision
    )
    relative = decision["export_path"]
    category = "coneixement" if decision["destination"] == "knowledge" else "llengua"
    if (
        not relative.startswith(category + "/")
        or Path(relative).is_absolute()
        or ".." in Path(relative).parts
    ):
        raise ManifestError(f"{unit_id}: export_path fora de {category}/")
    exported = root / relative
    if exported.is_symlink() or not exported.is_file():
        raise ManifestError(f"export absent: {exported}")
    exported_bytes = exported.read_bytes()
    if exported_bytes != expected_content:
        raise ManifestError(f"{exported}: no es pot regenerar exactament des de l'original")
    if source_meta.get(
        "type"
    ) == "article" and "## Buits registrats" not in expected_content.decode("utf-8"):
        raise ManifestError(f"{exported}: falta Buits registrats")

    fonts = []
    source_slug = source_meta.get("font")
    if isinstance(source_slug, str) and source_slug not in decision["source_ids"]:
        raise ManifestError(f"{unit_id}: source_ids no inclou la font declarada al document")
    for slug in decision["source_ids"]:
        card_path, card = source_card(project_root, slug)
        fonts.append(
            {
                "id": slug,
                "title": card.get("title"),
                "titular": card.get("titular"),
                "url": card.get("url"),
                "licence": card.get("llicencia"),
                "redistribution": card.get("redistribucio"),
                "record": card_path.relative_to(project_root).as_posix(),
                "record_sha256": sha256_file(card_path),
            }
        )

    evidence_records = []
    for reference in decision["evidence"]:
        raw_path, _, locator = reference.partition("#")
        evidence = safe_project_path(project_root, raw_path, "evidence")
        if not evidence.is_file():
            raise ManifestError(f"{unit_id}: evidència absent: {raw_path}")
        evidence_records.append(
            {
                "path": evidence.relative_to(project_root).as_posix(),
                "locator": locator,
                "sha256": sha256_file(evidence),
            }
        )
    terms_records = []
    for reference in decision["terms_evidence"]:
        raw_path, _, locator = reference.partition("#")
        terms = safe_project_path(project_root, raw_path, "terms_evidence")
        if not terms.is_file():
            raise ManifestError(f"{unit_id}: evidència de termes absent: {raw_path}")
        terms_records.append(
            {
                "path": terms.relative_to(project_root).as_posix(),
                "locator": locator,
                "sha256": sha256_file(terms),
            }
        )

    if not evidence_records or not terms_records or not fonts:
        raise ManifestError(f"{unit_id}: evidència, termes i font són obligatoris")
    domain = source_meta.get("tema")
    return {
        "id": unit_id,
        "status": "approved",
        "exported_path": relative,
        "exported_sha256": sha256_bytes(exported_bytes),
        "original_path": source_path.relative_to(project_root).as_posix(),
        "original_sha256": sha256_file(source_path),
        "source_fragment": decision["source_fragment"],
        "sources": fonts,
        "evidence": evidence_records,
        "domain": domain,
        "language": decision["language"],
        "text_type": decision["text_type"],
        "reference_date": decision["reference_date"],
        "terms": terms_records,
        "review": {
            "methods": decision["review_methods"],
            "reviewer": decision["reviewer"],
            "reviewed_at": decision["reviewed_at"],
            "human_reviewed": decision["human_reviewed"],
        },
        "transformations": decision["transformations"],
        "duplicate_group": decision["duplicate_group"],
        "batch_id": decision["batch_id"],
        "corpus_version": VERSION,
    }


def render(root: Path, project_root: Path | None = None) -> bytes:
    project = (project_root or root.parent).resolve()
    approved = approved_decisions(project)
    rows = [record(project, root, unit_id, decision) for unit_id, decision in approved]
    ids = [row["id"] for row in rows]
    paths = [row["exported_path"] for row in rows]
    if len(ids) != len(set(ids)) or len(paths) != len(set(paths)):
        raise ManifestError("IDs o rutes exportades duplicats")
    expected = set(paths)
    actual = {
        path.relative_to(root).as_posix()
        for category in ("coneixement", "llengua")
        for path in (root / category).rglob("*.md")
        if path.name.lower() != "readme.md"
    }
    if actual != expected:
        raise ManifestError(
            f"fitxers i decisions aprovades divergeixen: extra={sorted(actual - expected)}, "
            f"missing={sorted(expected - actual)}"
        )
    snapshot = sha256_bytes(
        json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    )
    header = {
        "schema": "maia-final-corpus/v2",
        "corpus_version": VERSION,
        "snapshot_sha256": snapshot,
        "description": "Selecció reproduïble des d'originals, decisions, fonts i evidència.",
    }
    lines = [json.dumps(header, ensure_ascii=False, sort_keys=True)]
    lines.extend(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    return ("\n".join(lines) + "\n").encode("utf-8")


def self_test() -> None:
    sample = (
        "---\ntype: article\n---\n# Títol\n"
        "[Font, p. 4](docs/raw/font.pdf)\n\n## Buits registrats\nCap.\n"
    )
    rendered = render_content(
        sample, ["strip_frontmatter", "unwrap_markdown_links"], Path("sample.md")
    )
    assert b"# T\xc3\xadtol" in rendered and b"[Font, p. 4](" not in rendered
    for transforms, text in [
        (["strip_frontmatter"], sample.replace("[Font, p. 4](docs/raw/font.pdf)", "[Font](x)")),
        (["strip_frontmatter", "unknown"], sample),
    ]:
        try:
            render_content(text, transforms, Path("invalid.md"))
        except ManifestError:
            continue
        raise AssertionError("self-test: contingut d'exportació defectuós acceptat")
    try:
        render_content(
            sample.replace("## Buits registrats", "## Related"),
            ["strip_frontmatter", "unwrap_markdown_links"],
            Path("invalid.md"),
        )
    except ManifestError:
        pass
    else:
        raise AssertionError("self-test: secció de navegació o sense buits acceptada")
    print("ok · transformació vàlida i tres casos d'exportació invàlids rebutjats")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="genera manifest.jsonl")
    group.add_argument("--check", action="store_true", help="comprova el manifest i l'exportació")
    group.add_argument(
        "--self-test", action="store_true", help="prova transformacions vàlides i invàlides"
    )
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0

    root = Path(__file__).resolve().parent.parent / "final-corpus"
    output = root / "manifest.jsonl"
    try:
        data = render(root)
    except (ManifestError, InventoryError, OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.check:
        if not output.is_file() or output.read_bytes() != data:
            print(
                "error: manifest absent o desactualitzat; regenera'l amb --write", file=sys.stderr
            )
            return 1
    else:
        handle, temporary = tempfile.mkstemp(prefix="manifest-", suffix=".tmp", dir=root)
        try:
            with os.fdopen(handle, "wb") as file:
                file.write(data)
            Path(temporary).replace(output)
        finally:
            Path(temporary).unlink(missing_ok=True)
    print(f"ok · manifest de {max(data.count(bytes([10])) - 1, 0)} unitats", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
