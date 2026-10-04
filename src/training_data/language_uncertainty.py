"""Filtra converses de parla que contenen spans transcrits com a incerts."""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

from training_data.language import LanguageLedger, SpeechPiece, UncertaintySpan
from training_data.language_conversations import SpeechConversationCandidate


@dataclass(frozen=True, slots=True)
class ExcludedLanguageCandidate:
    """Candidat descartat amb el span que n'impedeix l'ús."""

    family_id: str
    source_path: str
    reason: str
    uncertainty_spans: tuple[UncertaintySpan, ...]


@dataclass(frozen=True, slots=True)
class LanguageUncertaintyReport:
    """Reconciliació de peces i converses incloses o descartades per incertesa."""

    eligible_pieces: int
    pieces_with_candidates: int
    pieces_with_accepted_candidates: int
    pieces_fully_excluded: int
    input_candidates: int
    accepted_candidates: int
    excluded_candidates: int
    uncertainty_spans_in_sources: int
    uncertainty_spans_discarded: int
    uncertainty_spans_outside_candidates: int


@dataclass(frozen=True, slots=True)
class LanguageUncertaintyResult:
    """Candidates acceptats i decisions d'exclusió per incertesa."""

    accepted: tuple[SpeechConversationCandidate, ...]
    excluded: tuple[ExcludedLanguageCandidate, ...]
    report: LanguageUncertaintyReport


def _overlaps(span: UncertaintySpan, start: int, end: int) -> bool:
    return span.start < end and start < span.end


def _candidate_uncertainties(
    piece: SpeechPiece, candidate: SpeechConversationCandidate
) -> tuple[UncertaintySpan, ...]:
    return tuple(
        span
        for span in piece.uncertainty_spans
        if _overlaps(span, candidate.user_start, candidate.user_end)
        or _overlaps(span, candidate.assistant_start, candidate.assistant_end)
    )


def filter_uncertain_conversations(
    ledger: LanguageLedger,
    candidates: tuple[SpeechConversationCandidate, ...],
) -> LanguageUncertaintyResult:
    """Descarta el torn complet si la pregunta o la resposta toca un span dubtós."""

    pieces = {piece.path: piece for piece in ledger.pieces}
    accepted: list[SpeechConversationCandidate] = []
    excluded: list[ExcludedLanguageCandidate] = []
    discarded_spans: set[tuple[str, int, int]] = set()
    candidates_by_piece: dict[str, int] = {}
    accepted_by_piece: set[str] = set()
    for candidate in candidates:
        piece = pieces.get(candidate.source_path)
        if piece is None or piece.eligibility != "eligible":
            raise ValueError(f"conversation source is not eligible: {candidate.source_path}")
        candidates_by_piece[candidate.source_path] = (
            candidates_by_piece.get(candidate.source_path, 0) + 1
        )
        uncertain = _candidate_uncertainties(piece, candidate)
        if uncertain:
            excluded.append(
                ExcludedLanguageCandidate(
                    candidate.family_id,
                    candidate.source_path,
                    "uncertain_span_in_turn",
                    uncertain,
                )
            )
            discarded_spans.update((piece.path, span.start, span.end) for span in uncertain)
        else:
            accepted.append(candidate)
            accepted_by_piece.add(candidate.source_path)

    source_spans = sum(
        len(piece.uncertainty_spans) for piece in ledger.pieces if piece.eligibility == "eligible"
    )
    report = LanguageUncertaintyReport(
        eligible_pieces=ledger.report.eligible_pieces,
        pieces_with_candidates=len(candidates_by_piece),
        pieces_with_accepted_candidates=len(accepted_by_piece),
        pieces_fully_excluded=sum(path not in accepted_by_piece for path in candidates_by_piece),
        input_candidates=len(candidates),
        accepted_candidates=len(accepted),
        excluded_candidates=len(excluded),
        uncertainty_spans_in_sources=source_spans,
        uncertainty_spans_discarded=len(discarded_spans),
        uncertainty_spans_outside_candidates=source_spans - len(discarded_spans),
    )
    return LanguageUncertaintyResult(tuple(accepted), tuple(excluded), report)


def validate_uncertainty_filter(ledger: LanguageLedger, result: LanguageUncertaintyResult) -> None:
    """Falla si queda cap span incert dins d'una conversa acceptada."""

    pieces = {piece.path: piece for piece in ledger.pieces}
    for candidate in result.accepted:
        piece = pieces[candidate.source_path]
        if _candidate_uncertainties(piece, candidate):
            raise ValueError(f"uncertain span reaches accepted conversation: {candidate.family_id}")


def write_language_uncertainty_result(
    ledger: LanguageLedger,
    result: LanguageUncertaintyResult,
    *,
    work: Path,
    reports: Path,
) -> LanguageUncertaintyReport:
    """Valida i desa només missatges acceptats, decisions i comptadors locals."""

    validate_uncertainty_filter(ledger, result)
    work.mkdir(parents=True, exist_ok=True)
    _atomic_jsonl(
        work / "accepted-conversation-candidates.jsonl",
        (asdict(candidate) for candidate in result.accepted),
    )
    _atomic_jsonl(
        work / "accepted-messages.jsonl",
        (candidate.to_public_record() for candidate in result.accepted),
    )
    _atomic_jsonl(
        work / "uncertainty-decisions.jsonl",
        (asdict(decision) for decision in result.excluded),
    )
    reports.mkdir(parents=True, exist_ok=True)
    _atomic_write(
        reports / "uncertainty.json",
        json.dumps(asdict(result.report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    return result.report


def _atomic_jsonl(path: Path, records: Iterable[object]) -> None:
    _atomic_write(
        path,
        "".join(
            json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records
        ),
    )


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="")
    temporary.replace(path)
