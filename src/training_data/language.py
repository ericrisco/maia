"""Selecció traçable de peces de parla humana elegibles per a Maia Language."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from training_data.inventory import Inventory, InventoryEntry

Eligibility = Literal["eligible", "excluded", "unresolved"]
ProvenanceStatus = Literal[
    "recorded",
    "missing_source_id",
    "missing_source_card",
    "source_card_error",
    "ambiguous_source_card",
]
UNCERTAIN_SPAN = re.compile(r"\[\s?\?\s?[^\]\r\n]+\]")
TIMESTAMPED_TRANSCRIPT_LINE = re.compile(
    r"^\[\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}\]\s*(?P<text>.*)$"
)


@dataclass(frozen=True, slots=True)
class SpeechProvenance:
    """Targeta de font vinculada a una peça i el seu estat de redistribució."""

    source_id: str | None
    source_path: str | None
    status: ProvenanceStatus
    redistribution: str | None


@dataclass(frozen=True, slots=True)
class UncertaintySpan:
    """Span explícit de transcripció dubtosa, indexat sobre el text font."""

    start: int
    end: int
    text: str


@dataclass(frozen=True, slots=True)
class SpeechPiece:
    """Document original de parla, sense transformar i amb elegibilitat explicada."""

    path: str
    piece_id: str
    title: str
    document_type: str
    voice: object
    epoch: object
    language_eligible: object
    text: str
    provenance: tuple[SpeechProvenance, ...]
    uncertainty_spans: tuple[UncertaintySpan, ...]
    eligibility: Eligibility
    reason: str
    conversation_id: str | None = None
    speaker_id: str | None = None


@dataclass(frozen=True, slots=True)
class LanguageSelectionReport:
    """Comptadors de totes les entrades i decisions de selecció."""

    processed_entries: int
    speech_documents: int
    markdown_errors: int
    eligible_pieces: int
    excluded_pieces: int
    unresolved_pieces: int
    uncertainty_spans: int
    source_redistribution: dict[str, int]


@dataclass(frozen=True, slots=True)
class LanguageLedger:
    """Selecció de documents parla; el text font queda sense reescriure."""

    pieces: tuple[SpeechPiece, ...]
    report: LanguageSelectionReport


@dataclass(frozen=True, slots=True)
class AuthenticSpeechSegment:
    """Span fontal literal; aquest model no conté camps de text generat."""

    segment_id: str
    source_path: str
    piece_id: str
    source_start: int
    source_end: int
    text: str


@dataclass(frozen=True, slots=True)
class LanguageAuthenticityReport:
    """Volum de spans copiats literalment de peces de parla elegibles."""

    eligible_pieces: int
    authentic_segments: int
    source_characters: int
    uncertain_transcript_lines_excluded: int
    rewritten_segments: int
    generated_segments: int


def _source_ids(value: object) -> tuple[str, ...]:
    if isinstance(value, str) and value.strip():
        return (value.strip(),)
    if isinstance(value, list):
        return tuple(item.strip() for item in value if isinstance(item, str) and item.strip())
    return ()


def _source_cards(
    entries: tuple[InventoryEntry, ...],
) -> tuple[dict[str, list[InventoryEntry]], dict[str, InventoryEntry]]:
    by_id: dict[str, list[InventoryEntry]] = {}
    by_stem: dict[str, InventoryEntry] = {}
    for entry in entries:
        if not entry.path.startswith("fonts/") or not entry.path.lower().endswith(".md"):
            continue
        metadata = entry.document.metadata if entry.document is not None else {}
        is_card = metadata.get("type") == "font" or bool(metadata.get("id"))
        if entry.disposition == "markdown_error" or is_card:
            by_stem[Path(entry.path).stem] = entry
        if entry.document is not None and metadata.get("id"):
            source_id = str(metadata["id"]).strip()
            by_id.setdefault(source_id, []).append(entry)
    return by_id, by_stem


def _provenance(
    entry: InventoryEntry,
    by_id: dict[str, list[InventoryEntry]],
    by_stem: dict[str, InventoryEntry],
) -> tuple[SpeechProvenance, ...]:
    document = entry.document
    if document is None:
        return ()
    source_ids = _source_ids(document.metadata.get("font"))
    if not source_ids:
        return (SpeechProvenance(None, None, "missing_source_id", None),)
    references: list[SpeechProvenance] = []
    for source_id in source_ids:
        matches = by_id.get(source_id, [])
        if len(matches) > 1:
            references.append(SpeechProvenance(source_id, None, "ambiguous_source_card", None))
            continue
        if matches:
            card = matches[0]
            if card.document is not None:
                raw_redistribution = card.document.metadata.get("redistribucio")
                if raw_redistribution is None or raw_redistribution == "":
                    redistribution = "pendent"
                elif isinstance(raw_redistribution, bool):
                    # PyYAML resolves unquoted YAML 1.1 `yes` / `no` as booleans.
                    redistribution = "si" if raw_redistribution else "no"
                else:
                    redistribution = str(raw_redistribution).strip().casefold()
                references.append(
                    SpeechProvenance(source_id, card.path, "recorded", redistribution)
                )
                continue
        stem_entry = by_stem.get(source_id)
        if stem_entry is not None and stem_entry.disposition == "markdown_error":
            references.append(
                SpeechProvenance(source_id, stem_entry.path, "source_card_error", None)
            )
        else:
            references.append(SpeechProvenance(source_id, None, "missing_source_card", None))
    return tuple(references)


def _spans(text: str) -> tuple[UncertaintySpan, ...]:
    return tuple(
        UncertaintySpan(match.start(), match.end(), match.group())
        for match in UNCERTAIN_SPAN.finditer(text)
    )


def _select_entry(
    entry: InventoryEntry,
    by_id: dict[str, list[InventoryEntry]],
    by_stem: dict[str, InventoryEntry],
) -> SpeechPiece:
    document = entry.document
    path = entry.path
    stem = Path(path).with_suffix("").as_posix()
    if entry.disposition == "markdown_error":
        return SpeechPiece(
            path,
            stem,
            "",
            "unknown",
            None,
            None,
            None,
            "",
            (),
            (),
            "unresolved",
            "markdown_error",
        )
    if document is None:
        return SpeechPiece(
            path,
            stem,
            "",
            "unknown",
            None,
            None,
            None,
            "",
            (),
            (),
            "excluded",
            "non_markdown_or_auxiliary",
        )
    metadata = document.metadata
    document_type = str(metadata.get("type") or "unknown")
    provenance = _provenance(entry, by_id, by_stem)
    spans = _spans(document.body)
    if document_type != "parla":
        eligibility: Eligibility = "excluded"
        reason = "not_speech_piece"
    elif metadata.get("veu") != "originaria":
        eligibility = "excluded"
        reason = "voice_not_original"
    elif metadata.get("epoca") != "contemporania":
        eligibility = "excluded"
        reason = "epoch_not_contemporary"
    elif metadata.get("apte_llengua") is not True:
        eligibility = "excluded"
        reason = "not_marked_language_eligible"
    elif not provenance or any(reference.status != "recorded" for reference in provenance):
        eligibility = "unresolved"
        reason = "missing_or_invalid_provenance"
    else:
        eligibility = "eligible"
        reason = "all_eligibility_fields_and_source_recorded"
    return SpeechPiece(
        path=path,
        piece_id=stem,
        title=str(metadata.get("title") or ""),
        document_type=document_type,
        voice=metadata.get("veu"),
        epoch=metadata.get("epoca"),
        language_eligible=metadata.get("apte_llengua"),
        text=document.body,
        provenance=provenance,
        uncertainty_spans=spans,
        eligibility=eligibility,
        reason=reason,
    )


def extract_language(inventory: Inventory) -> LanguageLedger:
    """Classifica tot el que hi ha sota parla/ i conserva el text original."""

    entries = tuple(entry for entry in inventory.entries if entry.path.startswith("parla/"))
    by_id, by_stem = _source_cards(inventory.entries)
    pieces = tuple(_select_entry(entry, by_id, by_stem) for entry in entries)
    source_redistribution: dict[str, int] = {}
    for piece in pieces:
        for reference in piece.provenance:
            if reference.status == "recorded" and reference.redistribution is not None:
                source_redistribution[reference.redistribution] = (
                    source_redistribution.get(reference.redistribution, 0) + 1
                )
    report = LanguageSelectionReport(
        processed_entries=len(entries),
        speech_documents=sum(piece.document_type == "parla" for piece in pieces),
        markdown_errors=sum(piece.reason == "markdown_error" for piece in pieces),
        eligible_pieces=sum(piece.eligibility == "eligible" for piece in pieces),
        excluded_pieces=sum(piece.eligibility == "excluded" for piece in pieces),
        unresolved_pieces=sum(piece.eligibility == "unresolved" for piece in pieces),
        uncertainty_spans=sum(len(piece.uncertainty_spans) for piece in pieces),
        source_redistribution=source_redistribution,
    )
    return LanguageLedger(pieces, report)


def write_language_selection(
    ledger: LanguageLedger, *, work: Path, reports: Path
) -> LanguageSelectionReport:
    """Desa la selecció i el report; no exporta encara dades conversacionals."""

    work.mkdir(parents=True, exist_ok=True)
    selection_path = work / "selection.jsonl"
    selection_content = "".join(
        json.dumps(asdict(piece), ensure_ascii=False, sort_keys=True) + "\n"
        for piece in ledger.pieces
    )
    _atomic_write(selection_path, selection_content)
    reports.mkdir(parents=True, exist_ok=True)
    report_path = reports / "eligibility.json"
    _atomic_write(
        report_path,
        json.dumps(asdict(ledger.report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    return ledger.report


def build_authentic_speech_segments(
    ledger: LanguageLedger,
) -> tuple[AuthenticSpeechSegment, ...]:
    """Extreu només línies de transcripció literal sense marques d'incertesa."""

    segments: list[AuthenticSpeechSegment] = []
    for piece in ledger.pieces:
        if piece.eligibility != "eligible":
            continue
        offset = 0
        piece_segment = 0
        for line in piece.text.splitlines(keepends=True):
            visible = line.rstrip("\r\n")
            match = TIMESTAMPED_TRANSCRIPT_LINE.match(visible)
            if match is not None:
                raw_text = match.group("text")
                text = raw_text.strip()
                if text and not UNCERTAIN_SPAN.search(text):
                    leading = len(raw_text) - len(raw_text.lstrip())
                    start = offset + match.start("text") + leading
                    piece_segment += 1
                    segments.append(
                        AuthenticSpeechSegment(
                            segment_id=f"{piece.path}#speech-{piece_segment:05d}",
                            source_path=piece.path,
                            piece_id=piece.piece_id,
                            source_start=start,
                            source_end=start + len(text),
                            text=text,
                        )
                    )
            offset += len(line)
    return tuple(segments)


def validate_authentic_speech_segments(
    ledger: LanguageLedger, segments: tuple[AuthenticSpeechSegment, ...]
) -> None:
    """Falla si un span no coincide literalment amb una peça elegible."""

    pieces_by_path = {piece.path: piece for piece in ledger.pieces}
    seen: set[str] = set()
    for segment in segments:
        if segment.segment_id in seen:
            raise ValueError(f"duplicate authentic segment: {segment.segment_id}")
        seen.add(segment.segment_id)
        piece = pieces_by_path.get(segment.source_path)
        if piece is None or piece.eligibility != "eligible":
            raise ValueError(f"segment source is not eligible: {segment.source_path}")
        if not 0 <= segment.source_start <= segment.source_end <= len(piece.text):
            raise ValueError(f"segment offsets are outside the source: {segment.segment_id}")
        if segment.text != piece.text[segment.source_start : segment.source_end]:
            raise ValueError(f"segment does not match source span: {segment.segment_id}")


def write_authentic_speech_segments(
    ledger: LanguageLedger, *, work: Path, reports: Path
) -> LanguageAuthenticityReport:
    """Valida i desa spans de parla literal i el report de no-inflació."""

    segments = build_authentic_speech_segments(ledger)
    validate_authentic_speech_segments(ledger, segments)
    work.mkdir(parents=True, exist_ok=True)
    _atomic_write(
        work / "authentic-segments.jsonl",
        "".join(
            json.dumps(asdict(segment), ensure_ascii=False, sort_keys=True) + "\n"
            for segment in segments
        ),
    )
    report = LanguageAuthenticityReport(
        eligible_pieces=ledger.report.eligible_pieces,
        authentic_segments=len(segments),
        source_characters=sum(len(segment.text) for segment in segments),
        uncertain_transcript_lines_excluded=sum(
            bool(TIMESTAMPED_TRANSCRIPT_LINE.match(line.rstrip("\r\n")))
            and bool(UNCERTAIN_SPAN.search(line))
            for piece in ledger.pieces
            if piece.eligibility == "eligible"
            for line in piece.text.splitlines(keepends=True)
        ),
        rewritten_segments=0,
        generated_segments=0,
    )
    reports.mkdir(parents=True, exist_ok=True)
    _atomic_write(
        reports / "no-inflation.json",
        json.dumps(asdict(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    return report


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="")
    temporary.replace(path)
