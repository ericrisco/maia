#!/usr/bin/env python3
"""Index Markdown knowledge units in docs/temes for coverage review."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
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
LIST_ITEM = re.compile(r"^(\s{0,3})(?:[-+*]|\d+[.)])\s+(.+?)\s*$")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
TABLE_DELIMITER = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")


def split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def internal_links(text: str) -> list[str]:
    result: list[str] = []
    for match in LINK.finditer(text):
        target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
        if target and not re.match(r"^(?:[a-z]+:|//|#)", target, re.IGNORECASE):
            result.append(target)
    return result


def parse_units(relative: str, body: str) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    section_stack: list[tuple[int, str]] = []
    duplicate_counts: Counter[tuple[str, str]] = Counter()
    lines = body.splitlines()
    index = 0

    def add_unit(kind: str, line_number: int, text: str, **extra: Any) -> None:
        normalized = re.sub(r"\s+", " ", text).strip()
        if not normalized:
            return
        digest = hashlib.sha256(f"{kind}\0{normalized}".encode("utf-8")).hexdigest()[:12]
        key = (kind, digest)
        duplicate_counts[key] += 1
        occurrence = duplicate_counts[key]
        units.append({
            "unit_id": f"{relative}#u-{kind}-{digest}-{occurrence}",
            "document": relative,
            "kind": kind,
            "line": line_number,
            "section": [title for _, title in section_stack],
            "text": normalized,
            "internal_links": internal_links(text),
            **extra,
        })

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
            add_unit("heading", index + 1, title, level=level)
            index += 1
            continue

        if stripped.startswith(("```", "~~~")):
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
            table_lines: list[tuple[int, str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append((index + 1, lines[index].strip()))
                index += 1
            content_rows = [(number, text) for number, text in table_lines if not TABLE_DELIMITER.match(text)]
            if content_rows:
                header_line, header_text = content_rows[0]
                headers = split_cells(header_text)
                add_unit("table_header", header_line, header_text, columns=headers)
                for row_number, row_text in content_rows[1:]:
                    add_unit("table_row", row_number, row_text, columns=headers, cells=split_cells(row_text))
            continue

        list_match = LIST_ITEM.match(line)
        if list_match:
            start_line = index + 1
            base_indent = len(list_match.group(1))
            item_lines = [list_match.group(2).strip()]
            index += 1
            while index < len(lines):
                next_line = lines[index]
                if not next_line.strip() or HEADING.match(next_line) or LIST_ITEM.match(next_line) or next_line.lstrip().startswith(("|", ">", "```", "~~~")):
                    break
                indent = len(next_line) - len(next_line.lstrip())
                if indent > base_indent:
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
            add_unit("blockquote", start_line, " ".join(quote_lines))
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

    return units


def parse_document(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    return parse_document_text(path.relative_to(ROOT).as_posix(), raw)


def parse_document_text(relative: str, raw: str) -> dict[str, Any]:
    match = FRONTMATTER.match(raw)
    error = ""
    metadata: dict[str, Any] = {}
    body = raw
    if not match:
        error = "missing or malformed YAML frontmatter"
    else:
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

    units: list[dict[str, Any]] = []
    for field in ("title", "description"):
        value = metadata.get(field)
        if value:
            normalized = re.sub(r"\s+", " ", str(value)).strip()
            digest = hashlib.sha256(f"metadata_{field}\0{normalized}".encode("utf-8")).hexdigest()[:12]
            units.append({
                "unit_id": f"{relative}#u-metadata_{field}-{digest}-1",
                "document": relative,
                "kind": f"metadata_{field}",
                "line": 1,
                "section": [],
                "text": normalized,
                "internal_links": internal_links(normalized),
            })

    units.extend(parse_units(relative, body))
    counts = Counter(unit["kind"] for unit in units)
    return {
        "path": relative,
        "type": str(metadata.get("type") or "unparsed"),
        "title": str(metadata.get("title") or ""),
        "topic": str(metadata.get("tema") or ""),
        "source": str(metadata.get("font") or ""),
        "frontmatter_error": error,
        "headings": [unit["text"] for unit in units if unit["kind"] == "heading"],
        "unit_counts": dict(sorted(counts.items())),
        "unit_count": len(units),
        "units": units,
    }


def write_outputs(documents: list[dict[str, Any]]) -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    inventory_path = WORK / "document-units.jsonl"
    unit_ids: set[str] = set()
    all_counts: Counter[str] = Counter()
    by_topic: dict[str, Counter[str]] = defaultdict(Counter)
    by_source: Counter[str] = Counter()
    errors: list[dict[str, Any]] = []
    unit_total = 0
    with inventory_path.open("w", encoding="utf-8") as output:
        for document in documents:
            if document["frontmatter_error"]:
                errors.append(document)
            topic = document["topic"] or "(sense tema)"
            by_topic[topic][document["type"]] += 1
            by_source[document["source"] or "(sense font)"] += 1
            for unit in document["units"]:
                if unit["unit_id"] in unit_ids:
                    continue
                unit_ids.add(unit["unit_id"])
                unit_total += 1
                all_counts[unit["kind"]] += 1
                output.write(json.dumps(unit, ensure_ascii=False) + "\n")

    article_count = sum(doc["type"] == "article" for doc in documents)
    lines = [
        "# Inventari de Maia Knowledge", "",
        "Inventari regenerable de les unitats estructurals de `docs/temes/`. Cada unitat conserva el document, la secció, la línia i el text original per poder marcar cobertura. L'existència d'una unitat a l'inventari no vol dir que ja tingui una conversa.", "",
        f"- Documents Markdown: **{len(documents)}**.",
        f"- Articles: **{article_count}**.",
        f"- Unitats estructurals: **{unit_total}**.",
        f"- Errors de frontmatter: **{len(errors)}**.",
        f"- ID duplicats: **{sum(len(doc['units']) for doc in documents) - len(unit_ids)}**.",
        f"- Inventari regenerable: `knowledge/work/document-units.jsonl`.", "",
        "## Unitats per tipus", "", "| Tipus | Unitats |", "|---|---:|",
    ]
    lines.extend(f"| `{kind}` | {count} |" for kind, count in sorted(all_counts.items()))
    lines += ["", "## Documents per tema", "", "| Tema | Articles | Altres |", "|---|---:|---:|"]
    for topic, counts in sorted(by_topic.items()):
        lines.append(f"| `{topic}` | {counts['article']} | {sum(counts.values()) - counts['article']} |")
    lines += ["", "## Fonts declarades", "", "| Font | Documents |", "|---|---:|"]
    lines.extend(f"| `{source}` | {count} |" for source, count in sorted(by_source.items()))
    if errors:
        lines += ["", "## Errors de frontmatter", ""]
        lines.extend(f"- `{doc['path']}`: {doc['frontmatter_error']}" for doc in errors)
    (REPORTS / "inventory-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate corpus frontmatter and unit IDs without writing outputs")
    args = parser.parse_args()
    paths = sorted(DOCS.rglob("*.md"))
    documents = [parse_document(path) for path in paths]
    errors = [doc for doc in documents if doc["frontmatter_error"]]
    ids = [unit["unit_id"] for doc in documents for unit in doc["units"]]
    duplicates = len(ids) - len(set(ids))
    if duplicates or not documents or (args.check and errors):
        raise SystemExit(f"inventory check failed: documents={len(documents)}, frontmatter_errors={len(errors)}, duplicate_ids={duplicates}")
    if not args.check:
        write_outputs(documents)
    print(f"Documents: {len(documents)}; articles: {sum(d['type'] == 'article' for d in documents)}; units: {len(ids)}; frontmatter errors: {len(errors)}; duplicate IDs: {duplicates}")


if __name__ == "__main__":
    main()
