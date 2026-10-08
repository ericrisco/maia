#!/usr/bin/env python3
"""Parse Maia Knowledge Markdown into ordered semantic blocks and report coverage."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "docs/temes"
DEFAULT_REPORT = ROOT / "training-data/knowledge/reports/parser-coverage.md"
FENCE = chr(96) * 3
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LIST_RE = re.compile(r"^\s*(?:[-+*]|\d+[.)])\s+(.+)$")
MARKERS = {
    "partial": ("parcial", "parcialment", "queda obert"),
    "unknown": ("buit registrat", "no consta", "no se sap", "desconegut"),
    "divergence": ("divergència", "no coincideix", "es contradiu"),
    "resolved": ("resolt", "tancat el", "resposta trobada"),
    "uncertain": ("incert", "no verificat", "no s'identifica", "no es pot determinar"),
}


def split_frontmatter(document: str) -> tuple[str, str]:
    lines = document.splitlines()
    if not lines or lines[0].strip() != "---":
        return "", document
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            return "\n".join(lines[1:end]), "\n".join(lines[end + 1 :])
    return "", document


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def parse_frontmatter(raw: str) -> dict[str, Any]:
    """Read scalar, flow-list and block-scalar YAML used in Maia frontmatter."""
    lines = raw.splitlines()
    result: dict[str, Any] = {}
    index = 0
    while index < len(lines):
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", lines[index])
        if not match:
            index += 1
            continue
        key, value = match.groups()
        index += 1
        if value in (">", ">-", ">+", "|", "|-", "|+"):
            chunks = []
            while index < len(lines) and (not lines[index].strip() or lines[index][:1].isspace()):
                chunks.append(lines[index].strip())
                index += 1
            separator = "\n" if value.startswith("|") else " "
            result[key] = separator.join(part for part in chunks if part)
        elif value.startswith("[") and value.endswith("]"):
            try:
                items = next(csv.reader([value[1:-1]], skipinitialspace=True))
                result[key] = [_unquote(item) for item in items if item.strip()]
            except csv.Error:
                result[key] = value
        elif value.lower() in ("true", "false"):
            result[key] = value.lower() == "true"
        elif value in ("null", "~"):
            result[key] = None
        else:
            result[key] = _unquote(value)
    return result


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _links(text: str) -> list[dict[str, str]]:
    return [{"label": label, "target": target} for label, target in LINK_RE.findall(text)]


def _markers(text: str) -> list[str]:
    lowered = text.casefold()
    return [name for name, words in MARKERS.items() if any(word in lowered for word in words)]


def parse_markdown(body: str) -> tuple[list[dict[str, Any]], dict[str, int]]:
    lines = body.splitlines()
    blocks: list[dict[str, Any]] = []
    headings: list[dict[str, Any]] = []
    index = 0

    def add(kind: str, start: int, end: int, text: str, **extra: Any) -> None:
        blocks.append({
            "kind": kind,
            "line_start": start + 1,
            "line_end": end + 1,
            "heading_context": [item["text"] for item in headings],
            "text": text,
            "links": _links(text),
            "markers": _markers(text),
            **extra,
        })

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        heading = HEADING_RE.match(line)
        if heading:
            level, title = len(heading.group(1)), heading.group(2).strip()
            headings[:] = [item for item in headings if item["level"] < level]
            headings.append({"level": level, "text": title})
            add("heading", index, index, title, level=level)
            index += 1
            continue
        if line.lstrip().startswith(FENCE):
            start = index
            index += 1
            while index < len(lines) and not lines[index].lstrip().startswith(FENCE):
                index += 1
            if index < len(lines):
                index += 1
            add("code", start, index - 1, "\n".join(lines[start:index]))
            continue
        if "|" in line and index + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[index + 1]):
            start = index
            table_lines = [line]
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                table_lines.append(lines[index])
                index += 1
            add("table", start, index - 1, "\n".join(table_lines),
                header=_cells(table_lines[0]),
                rows=[_cells(row) for row in table_lines[1:]])
            continue
        if line.lstrip().startswith(">"):
            start = index
            quoted = []
            while index < len(lines) and lines[index].lstrip().startswith(">"):
                quoted.append(re.sub(r"^\s*>\s?", "", lines[index]))
                index += 1
            add("quote", start, index - 1, "\n".join(quoted))
            continue
        item = LIST_RE.match(line)
        if item:
            start = index
            parts = [item.group(1)]
            index += 1
            while index < len(lines) and lines[index].strip() and (lines[index][:1].isspace() or LIST_RE.match(lines[index])):
                parts.append(lines[index].strip())
                index += 1
            add("list_item", start, index - 1, "\n".join(parts))
            continue
        start = index
        parts = [line]
        index += 1
        while index < len(lines) and lines[index].strip():
            next_line = lines[index]
            if HEADING_RE.match(next_line) or next_line.lstrip().startswith((">", FENCE)) or LIST_RE.match(next_line):
                break
            if "|" in next_line and index + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[index + 1]):
                break
            parts.append(next_line)
            index += 1
        add("paragraph", start, index - 1, "\n".join(parts))

    metrics = {
        "blocks": len(blocks),
        "headings": sum(block["kind"] == "heading" for block in blocks),
        "tables": sum(block["kind"] == "table" for block in blocks),
        "table_rows": sum(len(block.get("rows", [])) for block in blocks),
        "links": sum(len(block["links"]) for block in blocks),
    }
    return blocks, metrics


def parse_document(path: Path, base: Path = ROOT) -> dict[str, Any]:
    document = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(document)
    blocks, metrics = parse_markdown(body)
    return {"path": path.relative_to(base).as_posix(),
            "metadata": parse_frontmatter(frontmatter), "blocks": blocks, "metrics": metrics}


def build_report(source: Path) -> str:
    paths = sorted(source.rglob("*.md"), key=lambda item: item.as_posix().casefold())
    totals = {"documents": 0, "errors": 0, "sections": 0, "tables": 0, "table_rows": 0, "links": 0, "blocks": 0}
    errors = []
    for path in paths:
        try:
            parsed = parse_document(path)
            totals["documents"] += 1
            totals["sections"] += parsed["metrics"]["headings"]
            totals["tables"] += parsed["metrics"]["tables"]
            totals["table_rows"] += parsed["metrics"]["table_rows"]
            totals["links"] += parsed["metrics"]["links"]
            totals["blocks"] += parsed["metrics"]["blocks"]
        except (OSError, UnicodeError, ValueError) as exc:
            totals["errors"] += 1
            errors.append(f"- {path.relative_to(ROOT).as_posix()}: {type(exc).__name__}: {exc}")
    table = "\n".join(f"| {label} | {totals[key]} |" for key, label in [
        ("documents", "Documents processats"), ("errors", "Errors"),
        ("sections", "Títols i seccions"), ("tables", "Taules"),
        ("table_rows", "Files de taules"), ("links", "Enllaços Markdown"),
        ("blocks", "Blocs semàntics")])
    error_text = "\n".join(errors) if errors else "Cap error de lectura o parseig."
    return f"""# Cobertura del parser de Knowledge

Generat recorrent docs/temes/ amb scripts/parse_corpus.py. El parser conserva els blocs Markdown en ordre i les metadades del frontmatter; no crea preguntes ni divideix per longitud.

| Mesura | Resultat |
|---|---:|
{table}

## Errors

{error_text}

Els marcadors partial, unknown, divergence, resolved i uncertain són pistes lèxiques. El text es conserva íntegre i aquests marcadors no substitueixen la revisió editorial.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    report = build_report(args.source)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
