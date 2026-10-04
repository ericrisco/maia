"""Normalització segura de format Markdown per al text públic del dataset."""

from __future__ import annotations

import html
import re

TABLE_SEPARATOR = re.compile(r"^:?-{3,}:?$")
MARKDOWN_LINK = re.compile(r"!?\[([^\]]*)\]\((?:[^()]|\([^()]*\))*\)")
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
HTML_TAG = re.compile(r"</?[A-Za-z][^>]*>")


def _table_cells(line: str) -> tuple[str, ...]:
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for character in value:
        if character == "|" and not escaped:
            cells.append("".join(current).strip())
            current.clear()
        else:
            current.append(character)
        escaped = character == "\\" and not escaped
    cells.append("".join(current).strip())
    return tuple(cells)


def _plain_inline(value: str) -> str:
    value = MARKDOWN_LINK.sub(lambda match: match.group(1), value)
    value = WIKILINK.sub(lambda match: (match.group(2) or match.group(1)).strip(), value)
    value = re.sub(r"~~.*?~~", " ", value, flags=re.DOTALL)
    value = value.replace("~~", "")
    value = value.replace("**", "").replace("__", "").replace("`", "")
    value = HTML_TAG.sub("", value)
    value = value.replace("*", "").replace("_", "")
    return html.unescape(value)


def markdown_to_plain_text(value: str, *, block_kind: str = "paragraph") -> str:
    """Elimina sintaxi Markdown i text ratllat substituït, sense redactar contingut."""

    if value.count("~~") % 2:
        return ""
    if block_kind == "table_row" or value.strip().startswith("|"):
        cells = _table_cells(value)
        if cells and all(TABLE_SEPARATOR.fullmatch(cell) for cell in cells):
            return ""
        plain = " — ".join(plain for cell in cells if (plain := _plain_inline(cell).strip()))
        plain = re.sub(r"(?<!\w)-\s+(?=\w)", " ", plain)
        return re.sub(r"^(?:\d{1,2}[.)]|[-+*])\s+", "", plain)

    lines: list[str] = []
    for raw_line in value.splitlines():
        line = raw_line.strip()
        line = re.sub(r"^#{1,6}\s+", "", line)
        while re.match(r"^(?:[-+*]|\d{1,2}[.)])\s+", line):
            line = re.sub(r"^(?:[-+*]|\d{1,2}[.)])\s+", "", line, count=1)
        line = re.sub(r"^>\s?", "", line)
        if line.strip():
            lines.append(line.strip())
    plain = re.sub(r"\s+", " ", _plain_inline(" ".join(lines))).strip()
    # Some parsers classify a numbered Markdown item as a paragraph and leave
    # its list marker attached to the first sentence.
    plain = re.sub(r"(?<!\w)-\s+(?=\w)", " ", plain)
    return re.sub(r"^\d{1,2}[.)]\s+", "", plain)
