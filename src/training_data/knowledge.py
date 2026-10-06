"""Knowledge evidence extraction with provenance and structural traceability."""

from __future__ import annotations

import json
import posixpath
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Literal
from urllib.parse import unquote, urlsplit

from curacio.metadata import volatility_for
from training_data.inventory import Inventory, InventoryEntry
from training_data.parser import DocumentRecord, MarkdownBlock, MarkdownLink

ProvenanceStatus = Literal[
    "recorded",
    "missing_source_id",
    "missing_source_card",
    "source_card_error",
    "ambiguous_source_card",
]
IssueState = Literal["unresolved", "excluded"]


@dataclass(frozen=True, slots=True)
class SourceCard:
    """La fitxa de procedència original, sense normalitzar els seus valors."""

    source_id: str
    path: str
    title: str
    holder: str
    url: str
    licence: str
    redistribution: str
    metadata: dict[str, object]


@dataclass(frozen=True, slots=True)
class SourceReference:
    """Estat de procedència d'una unitat en relació amb una fitxa de font."""

    source_id: str | None
    source_path: str | None
    status: ProvenanceStatus
    redistribution: str | None


@dataclass(frozen=True, slots=True)
class KnowledgeDocument:
    """Disposició, font i unitats detectades d'una fitxa temàtica."""

    path: str
    title: str
    document_type: str
    disposition: str
    provenance: tuple[SourceReference, ...]
    evidence_ids: tuple[str, ...]
    error: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceUnit:
    """Una unitat estructural completa que es pot auditar i representar."""

    id: str
    document_path: str
    location: str
    block_index: int | None
    block_kind: str
    heading_path: tuple[str, ...]
    content: str
    provenance: tuple[SourceReference, ...]
    volatility_score: float
    volatility_status: Literal["unreviewed"]
    representation_status: Literal["unrepresented"]


@dataclass(frozen=True, slots=True)
class KnowledgeRelation:
    """Un enllaç sortint d'una fitxa temàtica, resolt o marcat com a trencat."""

    source_path: str
    target: str
    target_path: str | None
    link_kind: str
    internal: bool
    resolved: bool


@dataclass(frozen=True, slots=True)
class KnowledgeIssue:
    """Error, manca de procedència o referència interna pendent de resoldre."""

    code: str
    path: str
    message: str
    state: IssueState


@dataclass(frozen=True, slots=True)
class KnowledgeReport:
    """Comptadors per reconciliar l'extracció amb el corpus temàtic."""

    processed_documents: int
    markdown_errors: int
    excluded_files: int
    sections_processed: int
    tables_processed: int
    table_rows_processed: int
    units_detected: int
    links_detected: int
    internal_links_detected: int
    unresolved_internal_links: int
    documents_missing_source_id: int
    documents_missing_source_card: int
    documents_with_source_card_error: int
    documents_with_ambiguous_source_card: int
    units_flagged_for_volatility_review: int


@dataclass(frozen=True, slots=True)
class KnowledgeLedger:
    """Ledger intern; cap camp auxiliar s'exporta als JSONL finals."""

    documents: tuple[KnowledgeDocument, ...]
    units: tuple[EvidenceUnit, ...]
    source_cards: tuple[SourceCard, ...]
    relations: tuple[KnowledgeRelation, ...]
    unresolved: tuple[KnowledgeIssue, ...]
    exclusions: tuple[KnowledgeIssue, ...]
    report: KnowledgeReport


JSONRecord = KnowledgeDocument | EvidenceUnit | SourceCard | KnowledgeRelation | KnowledgeIssue


def _source_ids(value: object) -> tuple[str, ...]:
    if isinstance(value, str) and value.strip():
        return (value.strip(),)
    if isinstance(value, list):
        return tuple(item.strip() for item in value if isinstance(item, str) and item.strip())
    return ()


def _source_card(entry: InventoryEntry) -> SourceCard | None:
    document = entry.document
    if document is None:
        return None
    metadata = document.metadata
    if metadata.get("type") != "font" and not metadata.get("id"):
        return None
    source_id = str(metadata.get("id") or Path(entry.path).stem).strip()
    redistribution_value = metadata.get("redistribucio")
    if redistribution_value is None or redistribution_value == "":
        redistribution = "pendent"
    elif isinstance(redistribution_value, bool):
        # PyYAML's YAML 1.1 resolver reads bare `yes` / `no` as booleans.
        redistribution = "si" if redistribution_value else "no"
    else:
        redistribution = str(redistribution_value).strip().casefold()
    return SourceCard(
        source_id=source_id,
        path=entry.path,
        title=str(metadata.get("title") or ""),
        holder=str(metadata.get("titular") or ""),
        url=str(metadata.get("url") or ""),
        licence=str(metadata.get("llicencia") or ""),
        redistribution=redistribution,
        metadata=metadata,
    )


def _source_index(
    entries: tuple[InventoryEntry, ...],
) -> tuple[dict[str, list[InventoryEntry]], dict[str, InventoryEntry]]:
    by_id: dict[str, list[InventoryEntry]] = {}
    by_stem: dict[str, InventoryEntry] = {}
    for entry in entries:
        if not entry.path.startswith("fonts/") or not entry.path.lower().endswith(".md"):
            continue
        metadata = entry.document.metadata if entry.document is not None else {}
        is_source_card = metadata.get("type") == "font" or bool(metadata.get("id"))
        if entry.disposition == "markdown_error" or is_source_card:
            by_stem[Path(entry.path).stem] = entry
        if entry.document is not None and entry.document.metadata.get("id"):
            source_id = str(entry.document.metadata["id"]).strip()
            by_id.setdefault(source_id, []).append(entry)
    return by_id, by_stem


def _source_references(
    entry: InventoryEntry,
    by_id: dict[str, list[InventoryEntry]],
    by_stem: dict[str, InventoryEntry],
) -> tuple[SourceReference, ...]:
    if entry.document is None:
        return ()
    source_ids = _source_ids(entry.document.metadata.get("font"))
    if not source_ids:
        return (
            SourceReference(
                source_id=None,
                source_path=None,
                status="missing_source_id",
                redistribution=None,
            ),
        )

    references: list[SourceReference] = []
    for source_id in source_ids:
        matches = by_id.get(source_id, [])
        if len(matches) > 1:
            references.append(SourceReference(source_id, None, "ambiguous_source_card", None))
            continue
        if matches:
            card_entry = matches[0]
            card = _source_card(card_entry)
            if card is not None:
                references.append(
                    SourceReference(
                        source_id,
                        card_entry.path,
                        "recorded",
                        card.redistribution,
                    )
                )
                continue
        stem_entry = by_stem.get(source_id)
        if stem_entry is not None and stem_entry.disposition == "markdown_error":
            references.append(
                SourceReference(source_id, stem_entry.path, "source_card_error", None)
            )
        else:
            references.append(SourceReference(source_id, None, "missing_source_card", None))
    return tuple(references)


def _heading_text(block: MarkdownBlock) -> str:
    line = block.text.strip()
    if block.level is None:
        return line
    prefix = "#" * block.level
    value = line.removeprefix(prefix).strip()
    return value.rstrip("# ").strip()


def _resolve_target(
    source_path: str, link: MarkdownLink, known_paths: set[str]
) -> tuple[str | None, bool]:
    if not link.internal:
        return None, False
    raw_path = unquote(urlsplit(link.target).path)
    if raw_path.startswith("/"):
        candidate = posixpath.normpath(raw_path.lstrip("/"))
    elif raw_path:
        candidate = posixpath.normpath(posixpath.join(posixpath.dirname(source_path), raw_path))
    else:
        candidate = source_path
    if candidate == ".." or candidate.startswith("../"):
        return None, False
    alternatives = [candidate]
    if not Path(candidate).suffix:
        alternatives.extend((f"{candidate}.md", posixpath.join(candidate, "index.md")))
    for alternative in alternatives:
        if alternative in known_paths:
            return alternative, True
    return candidate or None, False


def _table_counts(document: DocumentRecord) -> tuple[int, int]:
    tables = 0
    rows = 0
    in_table = False
    for block in document.structure:
        if block.kind == "table_row":
            rows += 1
            if not in_table:
                tables += 1
            in_table = True
        else:
            in_table = False
    return tables, rows


def _unit(
    *,
    document_path: str,
    block_index: int | None,
    block_kind: str,
    heading_path: tuple[str, ...],
    content: str,
    provenance: tuple[SourceReference, ...],
) -> EvidenceUnit:
    if block_index is None:
        if not block_kind.startswith("metadata_"):
            raise ValueError("metadata evidence units require a metadata block kind")
        suffix = block_kind.replace("_", "-", 1)
    else:
        suffix = f"block-{block_index:05d}"
    return EvidenceUnit(
        id=f"{document_path}#{suffix}",
        document_path=document_path,
        location=" > ".join(heading_path),
        block_index=block_index,
        block_kind=block_kind,
        heading_path=heading_path,
        content=content,
        provenance=provenance,
        volatility_score=volatility_for(content),
        volatility_status="unreviewed",
        representation_status="unrepresented",
    )


def extract_knowledge(inventory: Inventory) -> KnowledgeLedger:
    """Extract every thematic document and structural Markdown block."""

    thematic_entries = tuple(
        entry for entry in inventory.entries if entry.path.startswith("temes/")
    )
    by_id, by_stem = _source_index(inventory.entries)
    source_cards = tuple(
        card
        for entry in inventory.entries
        if entry.path.startswith("fonts/")
        and entry.document is not None
        and entry.document.metadata.get("type") == "font"
        and entry.disposition != "markdown_error"
        if (card := _source_card(entry)) is not None
    )
    known_paths = {entry.path for entry in inventory.entries}
    documents: list[KnowledgeDocument] = []
    units: list[EvidenceUnit] = []
    relations: list[KnowledgeRelation] = []
    unresolved: list[KnowledgeIssue] = []
    exclusions: list[KnowledgeIssue] = []
    sections = 0
    tables = 0
    table_rows = 0
    links_detected = 0
    internal_links = 0
    unresolved_links = 0
    missing_source_ids = 0
    missing_source_cards = 0
    source_card_errors = 0
    ambiguous_source_cards = 0
    volatility_candidates = 0

    for entry in thematic_entries:
        if entry.disposition == "non_markdown" or entry.disposition == "generated_auxiliary":
            exclusions.append(
                KnowledgeIssue(
                    "non_markdown_or_auxiliary",
                    entry.path,
                    f"Fitxer temàtic amb disposició {entry.disposition}.",
                    "excluded",
                )
            )
            continue
        if entry.disposition == "markdown_error" or entry.document is None:
            unresolved.append(
                KnowledgeIssue(
                    "markdown_error",
                    entry.path,
                    entry.error or "No s'ha pogut interpretar el document Markdown.",
                    "unresolved",
                )
            )
            documents.append(
                KnowledgeDocument(
                    path=entry.path,
                    title="",
                    document_type="unknown",
                    disposition=entry.disposition,
                    provenance=(),
                    evidence_ids=(),
                    error=entry.error,
                )
            )
            continue

        document = entry.document
        document_type = str(document.metadata.get("type") or "unknown")
        title = str(document.metadata.get("title") or "")
        provenance = _source_references(entry, by_id, by_stem)
        for reference in provenance:
            if reference.status == "missing_source_id":
                missing_source_ids += 1
                unresolved.append(
                    KnowledgeIssue(
                        "missing_source_id",
                        entry.path,
                        "La fitxa no declara cap font de procedència.",
                        "unresolved",
                    )
                )
            elif reference.status == "missing_source_card":
                missing_source_cards += 1
                unresolved.append(
                    KnowledgeIssue(
                        "missing_source_card",
                        entry.path,
                        f"No existeix la fitxa de procedència {reference.source_id!r}.",
                        "unresolved",
                    )
                )
            elif reference.status == "source_card_error":
                source_card_errors += 1
                unresolved.append(
                    KnowledgeIssue(
                        "source_card_error",
                        entry.path,
                        f"La fitxa de procedència {reference.source_id!r} té errors Markdown/YAML.",
                        "unresolved",
                    )
                )
            elif reference.status == "ambiguous_source_card":
                ambiguous_source_cards += 1
                unresolved.append(
                    KnowledgeIssue(
                        "ambiguous_source_card",
                        entry.path,
                        f"Hi ha més d'una fitxa per a {reference.source_id!r}.",
                        "unresolved",
                    )
                )

        heading_stack: list[tuple[int, str]] = []
        document_units: list[EvidenceUnit] = []
        for metadata_key in ("title", "description"):
            value = document.metadata.get(metadata_key)
            if isinstance(value, str) and value.strip():
                unit = _unit(
                    document_path=entry.path,
                    block_index=None,
                    block_kind=f"metadata_{metadata_key}",
                    heading_path=(),
                    content=value,
                    provenance=provenance,
                )
                units.append(unit)
                document_units.append(unit)

        for block_index, block in enumerate(document.structure):
            if block.kind == "heading" and block.level is not None:
                while heading_stack and heading_stack[-1][0] >= block.level:
                    heading_stack.pop()
                heading_stack.append((block.level, _heading_text(block)))
                if block.level >= 2:
                    sections += 1
            unit = _unit(
                document_path=entry.path,
                block_index=block_index,
                block_kind=block.kind,
                heading_path=tuple(heading for _, heading in heading_stack),
                content=block.text,
                provenance=provenance,
            )
            units.append(unit)
            document_units.append(unit)
            if unit.volatility_score > 0:
                volatility_candidates += 1

        doc_tables, doc_table_rows = _table_counts(document)
        tables += doc_tables
        table_rows += doc_table_rows
        for link in document.links:
            links_detected += 1
            target_path, resolved = _resolve_target(entry.path, link, known_paths)
            if link.internal:
                internal_links += 1
                if not resolved:
                    unresolved_links += 1
                    unresolved.append(
                        KnowledgeIssue(
                            "unresolved_internal_link",
                            entry.path,
                            f"No s'ha resolt l'enllaç intern {link.target!r}.",
                            "unresolved",
                        )
                    )
            relations.append(
                KnowledgeRelation(
                    source_path=entry.path,
                    target=link.target,
                    target_path=target_path,
                    link_kind=link.kind,
                    internal=link.internal,
                    resolved=resolved,
                )
            )
        documents.append(
            KnowledgeDocument(
                path=entry.path,
                title=title,
                document_type=document_type,
                disposition=entry.disposition,
                provenance=provenance,
                evidence_ids=tuple(unit.id for unit in document_units),
            )
        )

    report = KnowledgeReport(
        processed_documents=sum(entry.path.lower().endswith(".md") for entry in thematic_entries),
        markdown_errors=sum(entry.disposition == "markdown_error" for entry in thematic_entries),
        excluded_files=len(exclusions),
        sections_processed=sections,
        tables_processed=tables,
        table_rows_processed=table_rows,
        units_detected=len(units),
        links_detected=links_detected,
        internal_links_detected=internal_links,
        unresolved_internal_links=unresolved_links,
        documents_missing_source_id=missing_source_ids,
        documents_missing_source_card=missing_source_cards,
        documents_with_source_card_error=source_card_errors,
        documents_with_ambiguous_source_card=ambiguous_source_cards,
        units_flagged_for_volatility_review=volatility_candidates,
    )
    unit_ids = [unit.id for unit in units]
    if len(unit_ids) != len(set(unit_ids)):
        raise ValueError("knowledge evidence IDs must be unique within the ledger")
    return KnowledgeLedger(
        documents=tuple(documents),
        units=tuple(units),
        source_cards=source_cards,
        relations=tuple(relations),
        unresolved=tuple(unresolved),
        exclusions=tuple(exclusions),
        report=report,
    )


def _json_default(value: object) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Path):
        return value.as_posix()
    return str(value)


def _write_jsonl(path: Path, values: tuple[JSONRecord, ...]) -> None:
    content = "".join(
        json.dumps(asdict(value), ensure_ascii=False, sort_keys=True, default=_json_default) + "\n"
        for value in values
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="")
    temporary.replace(path)


def write_knowledge_extraction(
    ledger: KnowledgeLedger, *, work: Path, reports: Path
) -> KnowledgeReport:
    """Write deterministic, local-only intermediate ledgers and first report."""

    _write_jsonl(work / "documents.jsonl", ledger.documents)
    _write_jsonl(work / "evidence.jsonl", ledger.units)
    _write_jsonl(work / "source-cards.jsonl", ledger.source_cards)
    _write_jsonl(work / "relations.jsonl", ledger.relations)
    _write_jsonl(work / "unresolved.jsonl", ledger.unresolved)
    _write_jsonl(work / "exclusions.jsonl", ledger.exclusions)
    reports.mkdir(parents=True, exist_ok=True)
    report_path = reports / "inventory.json"
    temporary = report_path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(asdict(ledger.report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(report_path)
    return ledger.report
