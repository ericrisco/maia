#!/usr/bin/env python3
"""Inventory human-language sources without copying transcript contents."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
PARLA = ROOT / "docs" / "parla"
FONTS = ROOT / "docs" / "fonts"
WORK = ROOT / "training-data" / "language" / "work"
REPORTS = ROOT / "training-data" / "language" / "reports"
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", re.DOTALL)
UNCERTAIN = re.compile(r"\[\?[^\]]+\]")


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER.match(raw)
    if not match:
        return {}, "missing or malformed YAML frontmatter"
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return {}, f"invalid YAML frontmatter: {exc}"
    if not isinstance(metadata, dict):
        return {}, "frontmatter is not a YAML mapping"
    if not metadata.get("type") or not metadata.get("title"):
        return metadata, "frontmatter requires type and title"
    return metadata, ""


def load_fonts() -> dict[str, dict[str, Any]]:
    fonts: dict[str, dict[str, Any]] = {}
    for path in sorted(FONTS.glob("*.md")):
        metadata, error = parse_frontmatter(path)
        if error or metadata.get("type") != "font" or not metadata.get("id"):
            continue
        fonts[str(metadata["id"])] = metadata
    return fonts


def inspect_piece(path: Path, fonts: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    metadata, error = parse_frontmatter(path)
    relative = path.relative_to(ROOT).as_posix()
    if error:
        return {"path": relative, "frontmatter_error": error}, error
    if metadata.get("type") != "parla":
        return {"path": relative, "type": metadata.get("type"), "title": metadata.get("title")}, ""

    source_id = str(metadata.get("font") or "")
    source = fonts.get(source_id, {})
    source_rights = str(source.get("redistribucio") or "missing").strip().lower()
    source_notes = str(source.get("notes") or "").lower()
    tags = {str(tag).lower() for tag in (metadata.get("tags") or [])}
    apte = metadata.get("apte_llengua") is True
    uncertain_count = len(UNCERTAIN.findall(raw))
    transcript_unverified = (
        "transcripcio-no-verificada" in tags
        or "transcripcio-incerta" in tags
        or "no verificada contra l'àudio" in raw.lower()
    )
    consent_section = re.search(r"(?ims)^#{1,4}\s+Consentiment\s*\n(.*?)(?=^#{1,4}\s+|\Z)", raw)
    consent_text = consent_section.group(1).lower() if consent_section else ""
    consent_status = "documented_yes" if re.search(r"consentiment\s*(?:sí|consta)|\bconsentiment sí\b", consent_text) or (consent_section and re.search(r"\bconsta\b", consent_text)) else "not_documented"
    per_piece_terms = any(marker in source_notes for marker in ("per peça", "per vídeo", "verificada a #"))
    capsule_match = re.search(r"(?:càpsula|capsula)\s*#?\s*(\d+)", raw, re.IGNORECASE)
    capsule_number = capsule_match.group(1) if capsule_match else ""
    piece_license_verified = bool(
        capsule_number
        and re.search(
            rf"(?:verificada(?: a)?|declara CC BY per a)[^\n.]*#\s*0?{re.escape(capsule_number)}\b",
            source_notes,
            re.IGNORECASE,
        )
    )
    effective_rights = "si (per peça)" if piece_license_verified else source_rights

    if not apte:
        candidate_status = "not_a_language_sample"
    elif source_rights in {"no", "no; es conserva per a lectura i citació"} or source_rights.startswith("no"):
        candidate_status = "redistribution_not_allowed"
    elif source_rights in {"pendent", "missing"} and per_piece_terms and not piece_license_verified:
        candidate_status = "piece_level_rights_check"
    elif source_rights in {"pendent", "missing"} and not piece_license_verified:
        candidate_status = "rights_unresolved"
    elif (source_rights.startswith("si") or piece_license_verified) and transcript_unverified:
        candidate_status = "transcription_review_required"
    elif (source_rights.startswith("si") or piece_license_verified) and consent_status != "documented_yes":
        candidate_status = "consent_review_required"
    else:
        candidate_status = "manual_review_required"

    return {
        "path": relative,
        "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "title": str(metadata.get("title") or ""),
        "voice": str(metadata.get("veu") or ""),
        "topic": str(metadata.get("tema") or ""),
        "source_id": source_id,
        "source_path": f"docs/fonts/{source_id}.md" if source_id in fonts else "",
        "source_redistribution": source_rights,
        "effective_piece_redistribution": effective_rights,
        "source_license_requires_piece_check": per_piece_terms,
        "piece_license_verified_in_source_record": piece_license_verified,
        "apte_llengua": apte,
        "consent_evidence": consent_status,
        "transcription_review": "unverified" if transcript_unverified else "no_unverified_flag_found",
        "uncertain_token_markers": uncertain_count,
        "candidate_status": candidate_status,
        "tags": sorted(tags),
    }, ""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on malformed metadata or missing source records")
    args = parser.parse_args()
    fonts = load_fonts()
    paths = sorted(PARLA.rglob("*.md"))
    parsed = [inspect_piece(path, fonts) for path in paths]
    records = [record for record, _ in parsed if record.get("type") == "parla" or "candidate_status" in record]
    errors = [(path.relative_to(ROOT).as_posix(), error) for path, (_, error) in zip(paths, parsed) if error]
    missing_sources = [record["path"] for record in records if record.get("candidate_status") and not record.get("source_path")]
    if args.check and (errors or missing_sources or not paths):
        raise SystemExit(f"language inventory check failed: files={len(paths)}, errors={len(errors)}, missing_sources={len(missing_sources)}")

    WORK.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    counts = Counter(record.get("candidate_status", "not_a_language_sample") for record in records)
    inventory = {
        "source_root": "docs/parla/",
        "file_count": len(paths),
        "piece_count": len(records),
        "candidate_status_counts": dict(sorted(counts.items())),
        "parse_error_count": len(errors),
        "missing_source_count": len(missing_sources),
        "pieces": records,
    }
    (WORK / "source-inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    source_counts: dict[str, Counter[str]] = {}
    for record in records:
        source_counts.setdefault(record.get("source_id", ""), Counter())[record.get("candidate_status", "unknown")] += 1
    lines = [
        "# Auditoria inicial de Maia Language", "",
        "Inventari de fitxes de `docs/parla/`. No copia les transcripcions al fitxer d'inventari ni aprova cap fragment automàticament.", "",
        f"- Fitxers Markdown: **{len(paths)}**.",
        f"- Peces amb `type: parla`: **{len(records)}**.",
        f"- Errors de metadades: **{len(errors)}**.",
        f"- Fonts sense fitxa: **{len(missing_sources)}**.", "",
        "## Estat de candidatura", "", "| Estat | Peces |", "|---|---:|",
    ]
    lines.extend(f"| `{status}` | {count} |" for status, count in sorted(counts.items()))
    lines += ["", "## Peces per font", "", "| Font | Estat de candidatura | Peces |", "|---|---|---:|"]
    for source_id, statuses in sorted(source_counts.items()):
        for status, count in sorted(statuses.items()):
            lines.append(f"| `{source_id}` | `{status}` | {count} |")
    lines += [
        "", "## Criteri", "",
        "Una font `pendent` no s'aprova per defecte. Les llicències de plataformes i canals s'han de comprovar per peça. `apte_llengua` és una etiqueta editorial, no prova de consentiment ni de llicència.",
        "Les marques de transcripció incerta i els avisos de transcripció no verificada requereixen revisió abans d'exportar fragments. Les peces sense permís de redistribució o amb termes pendents no entren al dataset.",
        "Els splits s'han de fer per peça o parlant, mai per fragment aleatori de la mateixa veu.", "",
    ]
    if errors:
        lines += ["## Errors", ""] + [f"- `{path}`: {error}" for path, error in errors]
    (REPORTS / "eligibility-status.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Files: {len(paths)}; pieces: {len(records)}; errors: {len(errors)}; missing sources: {len(missing_sources)}; candidates: {dict(counts)}")


if __name__ == "__main__":
    main()
