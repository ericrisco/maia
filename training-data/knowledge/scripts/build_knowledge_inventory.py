#!/usr/bin/env python3
"""Inventory every Markdown document and structural content unit in docs/temes."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs" / "temes"
DATA = ROOT / "training-data" / "knowledge"
WORK = DATA / "work"
REPORTS = DATA / "reports"
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", re.DOTALL)
HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
LIST_ITEM = re.compile(r"^\s{0,3}(?:[-+*]|\d+[.)])\s+(.+?)\s*$")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
TABLE_DELIMITER = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")


def json_default(value: Any) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    raise TypeError(f"unsupported frontmatter value: {type(value).__name__}")


def split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def internal_links(text: str) -> list[str]:
    links: list[str] = []
    for match in LINK.finditer(text):
        target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
        if target and not re.match(r"^(?:[a-z]+:|//|#)", target, re.IGNORECASE):
            links.append(target)
    return links


def parse_document(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    relative = path.relative_to(ROOT).as_posix()
    match = FRONTMATTER.match(raw)
    metadata: dict[str, Any] = {}
    error = ""
    body = raw
    if match:
        body = raw[match.end():]
        try:
            loaded = yaml.safe_load(match.group(1))
            if not isinstance(loaded, dict):
                error = "frontmatter is not a YAML mapping"
            else:
                metadata = loaded
                if not metadata.get("type") or not metadata.get("title"):
                    error = "frontmatter requires type and title"
        except yaml.YAMLError as exc:
            error = f"invalid YAML frontmatter: {exc}"
    else:
        error = "missing or malformed YAML frontmatter"

    headings: list[dict[str, Any]] = []
    units: list[dict[str, Any]] = []
    section_stack: list[tuple[int, str]] = []
    lines = body.splitlines()
    index = 0

    def add_unit(kind: str, line_number: int, text: str, **extra: Any) -> None:
        text = text.strip()
        if not text:
            return
        unit_number = len(units) + 1
        unit: dict[str, Any] = {
            "unit_id": f"{relative}#unit-{unit_number:04d}",
            "kind": kind,
            "line": line_number,
            "section": [title for _, title in section_stack],
            "text": text,
            "internal_links": internal_links(text),
        }
        unit.update(extra)
        units.append(unit)

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue

        heading_match = HEADING.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            section_stack = [(depth, name) for depth, name in section_stack if depth < level]
            section_stack.append((level, title))
            headings.append({"level": level, "title": title, "line": index + 1})
            index += 1
            continue

        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = stripped[:3]
            start_line = index + 1
            code_lines = [line]
            index += 1
            while index < len(lines):
                code_lines.append(lines[index])
                if lines[index].strip().startswith(fence):
                    index += 1
                    break
                index += 1
            add_unit("code_block", start_line, "\n".join(code_lines))
            continue

        if stripped.startswith("|"):
            table_start = index + 1
            table_lines: list[tuple[int, str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append((index + 1, lines[index].strip()))
                index += 1
            non_delimiters = [(number, text) for number, text in table_lines if not TABLE_DELIMITER.match(text)]
            if non_delimiters:
                header_line, header_text = non_delimiters[0]
                headers = split_cells(header_text)
                add_unit("table_header", header_line, header_text, columns=headers)
                for row_number, row_text in non_delimiters[1:]:
                    add_unit("table_row", row_number, row_text, columns=headers, cells=split_cells(row_text))
            continue

        list_match = LIST_ITEM.match(line)
        if list_match:
            start_line = index + 1
            item_lines = [list_match.group(1).strip()]
            index += 1
            while index < len(lines):
                next_line = lines[index]
                if not next_line.strip():
                    break
                if HEADING.match(next_line) or LIST_ITEM.match(next_line) or next_line.lstrip().startswith("|"):
                    break
                if len(next_line) - len(next_line.lstrip()) >= 2:
                    item_lines.append(next_line.strip())
                    index += 1
                else:
                    break
            add_unit("list_item", start_line, " ".join(item_lines))
            continue

        if stripped.startswith(">"):
            start_line = index + 1
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[index]))
                index += 1
            add_unit("blockquote", start_line, "\n".join(quote_lines))
            continue

        start_line = index + 1
        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            next_line = lines[index]
            if not next_line.strip() or HEADING.match(next_line) or LIST_ITEM.match(next_line):
                break
            if next_line.lstrip().startswith(("|", ">", "```", "~~~")):
                break
            paragraph_lines.append(next_line.strip())
            index += 1
        add_unit("paragraph", start_line, " ".join(paragraph_lines))

    counts = Counter(unit["kind"] for unit in units)
    return {
        "path": relative,
        "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "metadata": metadata,
        "type": str(metadata.get("type") or "unparsed"),
        "title": str(metadata.get("title") or ""),
        "topic": str(metadata.get("tema") or ""),
        "source": str(metadata.get("font") or ""),
        "frontmatter_error": error,
        "headings": headings,
        "unit_counts": dict(sorted(counts.items())),
        "unit_count": len(units),
        "internal_links": sorted({link for unit in units for link in unit["internal_links"]}),
        "units": units,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if documents or stable unit IDs are invalid")
    args = parser.parse_args()
    paths = sorted(DOCS.rglob("*.md"))
    documents = [parse_document(path) for path in paths]
    errors = [doc for doc in documents if doc["frontmatter_error"]]
    ids = [unit["unit_id"] for doc in documents for unit in doc["units"]]
    duplicate_ids = len(ids) - len(set(ids))
    if args.check and (errors or not documents or duplicate_ids):
        raise SystemExit(f"inventory check failed: documents={len(documents)}, frontmatter_errors={len(errors)}, duplicate_unit_ids={duplicate_ids}")

    WORK.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    inventory = {
        "source_root": "docs/temes/",
        "document_count": len(documents),
        "article_count": sum(doc["type"] == "article" for doc in documents),
        "unit_count": len(ids),
        "parse_error_count": len(errors),
        "duplicate_unit_id_count": duplicate_ids,
        "documents": documents,
    }
    (WORK / "document-inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2, default=json_default) + "\n", encoding="utf-8")

    by_topic: dict[str, Counter[str]] = defaultdict(Counter)
    unit_total = Counter()
    for doc in documents:
        topic = doc["topic"] or "(sense tema)"
        by_topic[topic][doc["type"]] += 1
        unit_total.update(doc["unit_counts"])
    lines = [
        "# Inventari de Maia Knowledge", "",
        "Inventari estructural de tots els Markdown de `docs/temes/`. Els blocs s'han preservat com a unitats auditables; això encara no vol dir que estiguin coberts per converses.", "",
        f"- Documents Markdown: **{len(documents)}**.",
        f"- Articles: **{inventory['article_count']}**.",
        f"- Unitats estructurals: **{len(ids)}**.",
        f"- Errors de frontmatter: **{len(errors)}**.",
        f"- ID de unitat duplicats: **{duplicate_ids}**.", "",
        "## Tipus d'unitat", "", "| Tipus | Unitats |", "|---|---:|",
    ]
    lines.extend(f"| `{kind}` | {count} |" for kind, count in sorted(unit_total.items()))
    lines += ["", "## Documents per tema", "", "| Tema | Articles | Altres documents |", "|---|---:|---:|"]
    for topic, counts in sorted(by_topic.items()):
        lines.append(f"| `{topic}` | {counts['article']} | {sum(counts.values()) - counts['article']} |")
    if errors:
        lines += ["", "## Errors de frontmatter", ""]
        lines.extend(f"- `{doc['path']}`: {doc['frontmatter_error']}" for doc in errors)
    (REPORTS / "inventory-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Documents: {len(documents)}; articles: {inventory['article_count']}; units: {len(ids)}; frontmatter errors: {len(errors)}; duplicate IDs: {duplicate_ids}")


if __name__ == "__main__":
    main()
