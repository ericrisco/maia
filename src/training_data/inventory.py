"""Inventari complet dels fitxers del corpus, sense les exclusions del lector vell."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from training_data.parser import DocumentRecord, MarkdownParseError, parse_markdown

Disposition = Literal[
    "markdown_read",
    "markdown_error",
    "generated_auxiliary",
    "non_markdown",
]
FileKind = Literal["markdown", "non_markdown"]

GENERATED_AUXILIARY_SUFFIXES = {".base", ".canvas"}
GENERATED_DIRECTORIES = {".obsidian", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


@dataclass(frozen=True, slots=True)
class InventoryEntry:
    """Una entrada per cada fitxer trobat sota l'arrel."""

    path: str
    kind: FileKind
    disposition: Disposition
    size_bytes: int
    document: DocumentRecord | None = None
    error: str | None = None


@dataclass(frozen=True, slots=True)
class Inventory:
    """Inventari ordenat i auditable d'un arbre de fitxers."""

    root: str
    entries: tuple[InventoryEntry, ...]


def _is_generated_auxiliary(path: Path, document: DocumentRecord | None) -> bool:
    if GENERATED_DIRECTORIES.intersection(path.parts):
        return True
    if path.suffix.lower() in GENERATED_AUXILIARY_SUFFIXES:
        return True
    if document is not None:
        opening = document.body.lstrip()[:512].casefold()
        if "<!-- generat" in opening or "<!-- generated" in opening:
            return True
    return False


def _read_markdown(path: Path, relative: str) -> InventoryEntry:
    try:
        with path.open("r", encoding="utf-8", newline="") as source_file:
            source = source_file.read()
    except (OSError, UnicodeError) as error:
        return InventoryEntry(
            path=relative,
            kind="markdown",
            disposition="markdown_error",
            size_bytes=path.stat().st_size,
            error=f"{error.__class__.__name__}: {error}",
        )
    try:
        document = parse_markdown(relative, source)
    except MarkdownParseError as error:
        return InventoryEntry(
            path=relative,
            kind="markdown",
            disposition="markdown_error",
            size_bytes=path.stat().st_size,
            error=str(error),
        )
    disposition: Disposition = (
        "generated_auxiliary" if _is_generated_auxiliary(path, document) else "markdown_read"
    )
    return InventoryEntry(
        path=relative,
        kind="markdown",
        disposition=disposition,
        size_bytes=path.stat().st_size,
        document=document,
    )


def scan_tree(root: Path) -> Inventory:
    """Classify every file below ``root`` once and parse every Markdown file."""

    if not root.exists():
        raise FileNotFoundError(root)
    if not root.is_dir():
        raise NotADirectoryError(root)

    candidates = sorted(
        (path for path in root.rglob("*") if not path.is_dir()), key=lambda p: p.as_posix()
    )
    entries: list[InventoryEntry] = []
    for path in candidates:
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            entries.append(
                InventoryEntry(
                    path=relative,
                    kind="non_markdown",
                    disposition="non_markdown",
                    size_bytes=0,
                    error="symlink not followed",
                )
            )
        elif path.suffix.lower() == ".md":
            entries.append(_read_markdown(path, relative))
        elif _is_generated_auxiliary(path, None):
            entries.append(
                InventoryEntry(
                    path=relative,
                    kind="non_markdown",
                    disposition="generated_auxiliary",
                    size_bytes=path.stat().st_size,
                )
            )
        else:
            entries.append(
                InventoryEntry(
                    path=relative,
                    kind="non_markdown",
                    disposition="non_markdown",
                    size_bytes=path.stat().st_size,
                )
            )
    return Inventory(root=str(root), entries=tuple(entries))
