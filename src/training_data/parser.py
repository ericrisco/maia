"""Lectura sense pèrdues de frontmatter i estructura Markdown."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlsplit

import yaml

BlockKind = Literal[
    "heading",
    "paragraph",
    "list_item",
    "table_row",
    "blockquote",
    "code_block",
    "other",
]
LinkKind = Literal["markdown", "wikilink"]

METADATA_FIELDS = (
    "type",
    "title",
    "description",
    "tema",
    "veu",
    "epoca",
    "apte_llengua",
    "font",
    "timestamp",
    "tags",
)

FRONTMATTER_START = re.compile(r"\A(?:\ufeff)?---[ \t]*\r?\n")
FRONTMATTER_END = re.compile(r"(?m)^---[ \t]*(?:\r?\n|\Z)")
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")
FENCE_START = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
LIST_ITEM = re.compile(r"^( *)([-+*]|\d+[.)])[ \t]+(.*)$")
INDENTED_CODE = re.compile(r"^ {4,}\S")
TABLE_ROW = re.compile(r"^ {0,3}\|.*\|[ \t]*$")
BLOCKQUOTE = re.compile(r"^ {0,3}>.*$")
THEMATIC_BREAK = re.compile(r"^ {0,3}(?:-{3,}|\*{3,}|_{3,})[ \t]*$")
MARKDOWN_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\((<[^>]+>|[^)\s]+)(?:[ \t]+[^)]*)?\)")
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")


class MarkdownParseError(ValueError):
    """Un document Markdown amb delimitadors o YAML frontmatter invàlids."""


@dataclass(frozen=True, slots=True)
class MarkdownBlock:
    """Un bloc reconegut, amb el text Markdown original i la seva estructura."""

    kind: BlockKind
    text: str
    level: int | None = None
    indent: int = 0
    marker: str = ""
    cells: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class MarkdownLink:
    """Un enllaç Markdown o wikilink trobat al cos del document."""

    label: str
    target: str
    kind: LinkKind
    internal: bool


@dataclass(frozen=True, slots=True)
class DocumentRecord:
    """Metadades, cos complet i estructura d'una fitxa Markdown."""

    path: str
    metadata: dict[str, object]
    selected_metadata: dict[str, object | None]
    body: str
    structure: tuple[MarkdownBlock, ...]
    links: tuple[MarkdownLink, ...]


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


def _is_internal(target: str) -> bool:
    parsed = urlsplit(target)
    return not parsed.scheme and not parsed.netloc


def _links(blocks: tuple[MarkdownBlock, ...]) -> tuple[MarkdownLink, ...]:
    links: list[MarkdownLink] = []
    for block in blocks:
        if block.kind == "code_block":
            continue
        found: list[tuple[int, MarkdownLink]] = []
        for match in MARKDOWN_LINK.finditer(block.text):
            target = match.group(2)
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            found.append(
                (
                    match.start(),
                    MarkdownLink(
                        label=match.group(1),
                        target=target,
                        kind="markdown",
                        internal=_is_internal(target),
                    ),
                )
            )
        for match in WIKILINK.finditer(block.text):
            raw = match.group(1)
            target, separator, alias = raw.partition("|")
            label = alias if separator else target
            target = target.strip()
            found.append(
                (
                    match.start(),
                    MarkdownLink(
                        label=label.strip(),
                        target=target,
                        kind="wikilink",
                        internal=_is_internal(target),
                    ),
                )
            )
        links.extend(link for _, link in sorted(found, key=lambda item: item[0]))
    return tuple(links)


def _is_block_start(line: str) -> bool:
    return bool(
        HEADING.match(line)
        or FENCE_START.match(line)
        or LIST_ITEM.match(line)
        or TABLE_ROW.match(line)
        or BLOCKQUOTE.match(line)
        or THEMATIC_BREAK.match(line)
        or INDENTED_CODE.match(line)
    )


def _structure(body: str) -> tuple[MarkdownBlock, ...]:
    lines = body.splitlines(keepends=True)
    blocks: list[MarkdownBlock] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        visible = line.rstrip("\r\n")
        if not visible.strip():
            index += 1
            continue

        fence = FENCE_START.match(visible)
        if fence:
            marker = fence.group(1)
            fence_char = marker[0]
            end = re.compile(rf"^ {{0,3}}{re.escape(fence_char)}{{{len(marker)},}}[ \t]*$")
            raw = [line]
            index += 1
            while index < len(lines):
                raw.append(lines[index])
                candidate = lines[index].rstrip("\r\n")
                index += 1
                if end.match(candidate):
                    break
            blocks.append(MarkdownBlock(kind="code_block", text="".join(raw)))
            continue

        heading = HEADING.match(visible)
        if heading:
            blocks.append(
                MarkdownBlock(
                    kind="heading",
                    text="".join([line]),
                    level=len(heading.group(1)),
                )
            )
            index += 1
            continue

        item = LIST_ITEM.match(visible)
        if item:
            blocks.append(
                MarkdownBlock(
                    kind="list_item",
                    text=line,
                    indent=len(item.group(1)),
                    marker=item.group(2),
                )
            )
            index += 1
            continue

        if INDENTED_CODE.match(visible):
            raw = [line]
            index += 1
            while index < len(lines):
                candidate = lines[index].rstrip("\r\n")
                if INDENTED_CODE.match(candidate):
                    raw.append(lines[index])
                    index += 1
                    continue
                if not candidate.strip() and index + 1 < len(lines):
                    following = lines[index + 1].rstrip("\r\n")
                    if INDENTED_CODE.match(following):
                        raw.append(lines[index])
                        index += 1
                        continue
                break
            blocks.append(MarkdownBlock(kind="code_block", text="".join(raw)))
            continue

        if TABLE_ROW.match(visible):
            blocks.append(MarkdownBlock(kind="table_row", text=line, cells=_table_cells(visible)))
            index += 1
            continue

        if BLOCKQUOTE.match(visible):
            raw = [line]
            index += 1
            while index < len(lines):
                candidate = lines[index].rstrip("\r\n")
                if not BLOCKQUOTE.match(candidate):
                    break
                raw.append(lines[index])
                index += 1
            blocks.append(MarkdownBlock(kind="blockquote", text="".join(raw)))
            continue

        if THEMATIC_BREAK.match(visible):
            blocks.append(MarkdownBlock(kind="other", text=line))
            index += 1
            continue

        raw = [line]
        index += 1
        while index < len(lines):
            candidate = lines[index].rstrip("\r\n")
            if not candidate.strip() or _is_block_start(candidate):
                break
            raw.append(lines[index])
            index += 1
        blocks.append(MarkdownBlock(kind="paragraph", text="".join(raw)))

    return tuple(blocks)


def parse_markdown(path: str, source: str) -> DocumentRecord:
    """Parse YAML frontmatter and preserve the complete Markdown body."""

    metadata: dict[str, object] = {}
    body = source
    start = FRONTMATTER_START.match(source)
    if start:
        end = FRONTMATTER_END.search(source, start.end())
        if end is None:
            raise MarkdownParseError(f"{path}: falta el delimitador final del frontmatter")
        try:
            raw_metadata = yaml.safe_load(source[start.end() : end.start()])
        except yaml.YAMLError as error:
            raise MarkdownParseError(f"{path}: YAML frontmatter invàlid: {error}") from error
        if raw_metadata is None:
            metadata = {}
        elif isinstance(raw_metadata, dict) and all(isinstance(key, str) for key in raw_metadata):
            metadata = raw_metadata
        else:
            raise MarkdownParseError(f"{path}: el frontmatter ha de ser un mapa YAML")
        body = source[end.end() :]

    selected = {key: metadata.get(key) for key in METADATA_FIELDS}
    structure = _structure(body)
    return DocumentRecord(
        path=path,
        metadata=metadata,
        selected_metadata=selected,
        body=body,
        structure=structure,
        links=_links(structure),
    )
