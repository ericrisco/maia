#!/usr/bin/env python3
"""Build a document-level coverage ledger from Maia's Knowledge corpus."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "docs" / "temes"
REVIEW = ROOT / "training-data" / "knowledge" / "review"
REPORTS = ROOT / "training-data" / "knowledge" / "reports"

FRONTMATTER_KEYS = ("type", "title", "tema", "font")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
INTERNAL_LINK = re.compile(r"\[[^\]]+\]\((?:\.{1,2}/|/)[^)]+\)|\[\[[^\]]+\]\]")


def read_frontmatter(lines: list[str]) -> tuple[dict[str, str], int, str | None]:
    if not lines or lines[0].strip() != "---":
        return {}, 0, "missing YAML frontmatter"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, 0, "unterminated YAML frontmatter"

    data: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*?)\s*$", line)
        if match and match.group(1) in FRONTMATTER_KEYS:
            data[match.group(1)] = match.group(2).strip().strip("\"'")
    missing = [key for key in ("type", "title") if not data.get(key)]
    error = f"missing frontmatter fields: {', '.join(missing)}" if missing else None
    return data, end + 1, error


def inspect_markdown(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    metadata, body_start, frontmatter_error = read_frontmatter(lines)

    sections: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    paragraph_open = False
    quote_open = False
    table_open = False
    code_open = False

    def close_paragraph() -> None:
        nonlocal paragraph_open
        if paragraph_open:
            counts["paragraph"] += 1
            paragraph_open = False

    for line in lines[body_start:]:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            close_paragraph()
            if not code_open:
                counts["code_block"] += 1
            code_open = not code_open
            quote_open = False
            table_open = False
            continue
        if code_open:
            continue
        if not stripped:
            close_paragraph()
            quote_open = False
            table_open = False
            continue

        heading = HEADING.match(stripped)
        if heading:
            close_paragraph()
            sections.append({"level": len(heading.group(1)), "title": heading.group(2)})
            counts["heading"] += 1
            quote_open = False
            table_open = False
            continue

        if stripped.startswith(">"):
            close_paragraph()
            if not quote_open:
                counts["blockquote"] += 1
            quote_open = True
            table_open = False
            continue
        quote_open = False

        if stripped.startswith("|") and stripped.endswith("|"):
            close_paragraph()
            if re.fullmatch(r"[\s|:=-]+", stripped):
                continue
            if not table_open:
                counts["table"] += 1
                counts["table_header"] += 1
                table_open = True
            else:
                counts["table_row"] += 1
            continue
        table_open = False

        if LIST_ITEM.match(line):
            close_paragraph()
            counts["list_item"] += 1
            continue

        paragraph_open = True

    close_paragraph()
    counts["internal_link"] = len(INTERNAL_LINK.findall(text))

    parts = path.relative_to(SOURCE).parts
    return {
        "document": path.relative_to(ROOT).as_posix(),
        "type": metadata.get("type", ""),
        "title": metadata.get("title", path.stem),
        "topic": metadata.get("tema", "/".join(parts[:-1])),
        "topic_root": parts[0] if parts else "",
        "source": metadata.get("font", ""),
        "sections": sections,
        "structure_counts": dict(sorted(counts.items())),
        "frontmatter_error": frontmatter_error,
    }


def reviewed_records_by_document() -> dict[str, list[dict[str, object]]]:
    mapping: dict[str, list[dict[str, object]]] = {}
    path = REVIEW / "provenance.jsonl"
    if not path.exists():
        return mapping
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record.get("status") != "reviewed" or record.get("training_eligible") is not True:
            continue
        for source in record.get("sources", []):
            if isinstance(source, dict) and source.get("article"):
                mapping.setdefault(source["article"], []).append(record)
    return mapping


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    records_by_document = reviewed_records_by_document()
    documents = [inspect_markdown(path) for path in sorted(SOURCE.rglob("*.md"))]

    for document in documents:
        records = records_by_document.get(str(document["document"]), [])
        document["coverage_status"] = "partial" if records else "pending"
        document["reviewed_conversations"] = sorted({str(r["sample_id"]) for r in records})
        document["linked_claim_count"] = sum(len(r.get("claims", [])) for r in records)
        document["coverage_note"] = (
            "Some reviewed claims cite this document; section and unit coverage remains incomplete."
            if records
            else "No training-eligible reviewed conversation cites this document yet."
        )

    ledger = REPORTS / "coverage.jsonl"
    ledger.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in documents), encoding="utf-8")

    topic_counts: Counter[str] = Counter(str(row["topic_root"]) for row in documents)
    status_counts: Counter[str] = Counter(str(row["coverage_status"]) for row in documents)
    structure_totals: Counter[str] = Counter()
    for row in documents:
        structure_totals.update(row["structure_counts"])

    summary = [
        "# Maia Knowledge: cobertura del corpus",
        "",
        "Regenerar amb `python3 training-data/knowledge/scripts/build_coverage_report.py`.",
        "",
        f"Documents inventariats: **{len(documents)}**.",
        f"Cobertura parcial: **{status_counts['partial']}**. Pendents: **{status_counts['pending']}**. Complets: **{status_counts['complete']}**.",
        "",
        "La cobertura parcial només indica que hi ha converses revisades que citen el document. No vol dir que totes les seccions, files de taules o unitats estiguin cobertes. Els mostrejos editorials no compten com a cobertura.",
        "",
        "## Documents per branca",
        "",
        "| Branca | Documents |",
        "|---|---:|",
    ]
    summary.extend(f"| {topic} | {count} |" for topic, count in sorted(topic_counts.items()))
    summary.extend(
        [
            "",
            "## Unitats estructurals detectades",
            "",
            "| Tipus | Nombre |",
            "|---|---:|",
        ]
    )
    summary.extend(f"| {kind} | {count} |" for kind, count in sorted(structure_totals.items()))
    (REPORTS / "coverage-summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"Wrote {ledger} ({len(documents)} documents)")
    print(f"Wrote {REPORTS / 'coverage-summary.md'}")


if __name__ == "__main__":
    main()
