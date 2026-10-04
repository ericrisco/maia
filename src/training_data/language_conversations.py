"""Converteix només torns humans explícitament etiquetats a Maia Language."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from training_data.language import LanguageLedger, SpeechPiece

TurnRole = Literal["user", "assistant"]
NormalizationStatus = Literal["verbatim"]
TURN_LABEL = re.compile(
    r"^\s*(?:\*\*)?(?P<label>entrevistador|entrevistadora|interviewer|user|"
    r"parlant|persona entrevistada|interviewee|assistant)(?:\*\*)?:\s*(?P<text>.*)$",
    re.IGNORECASE,
)
USER_LABELS = {"entrevistador", "entrevistadora", "interviewer", "user"}


@dataclass(frozen=True, slots=True)
class _Turn:
    role: TurnRole
    text: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class SpeechConversationCandidate:
    """Torn user/assistant provinent de dos spans literals del mateix enregistrament."""

    family_id: str
    source_path: str
    piece_id: str
    conversation_id: str
    user: str
    assistant: str
    user_start: int
    user_end: int
    assistant_start: int
    assistant_end: int
    normalization_status: NormalizationStatus

    def to_public_record(self) -> dict[str, list[dict[str, str]]]:
        """Retorna només els dos missatges públics, sense metadades internes."""

        return {
            "messages": [
                {"role": "user", "content": self.user},
                {"role": "assistant", "content": self.assistant},
            ]
        }


@dataclass(frozen=True, slots=True)
class LanguageConversationReport:
    """Comptadors dels torns explícits trobats a peces lingüístiques elegibles."""

    eligible_pieces: int
    pieces_with_explicit_dialogue: int
    candidates: int
    verbatim_assistant_turns: int


def _turns(piece: SpeechPiece) -> tuple[_Turn, ...]:
    turns: list[_Turn] = []
    offset = 0
    for line in piece.text.splitlines(keepends=True):
        visible = line.rstrip("\r\n")
        match = TURN_LABEL.match(visible)
        if match is not None:
            label = match.group("label").casefold()
            raw_text = match.group("text")
            leading = len(raw_text) - len(raw_text.lstrip())
            text = raw_text.strip()
            if text:
                start = offset + match.start("text") + leading
                turns.append(
                    _Turn(
                        "user" if label in USER_LABELS else "assistant",
                        text,
                        start,
                        start + len(text),
                    )
                )
        offset += len(line)
    return tuple(turns)


def _pair_turns(piece: SpeechPiece) -> tuple[SpeechConversationCandidate, ...]:
    candidates: list[SpeechConversationCandidate] = []
    pending_user: _Turn | None = None
    for turn in _turns(piece):
        if turn.role == "user":
            pending_user = turn
        elif pending_user is not None:
            index = len(candidates) + 1
            candidates.append(
                SpeechConversationCandidate(
                    family_id=f"{piece.path}#turn-{index:05d}",
                    source_path=piece.path,
                    piece_id=piece.piece_id,
                    conversation_id=piece.piece_id,
                    user=pending_user.text,
                    assistant=turn.text,
                    user_start=pending_user.start,
                    user_end=pending_user.end,
                    assistant_start=turn.start,
                    assistant_end=turn.end,
                    normalization_status="verbatim",
                )
            )
            pending_user = None
    return tuple(candidates)


def build_human_conversations(
    ledger: LanguageLedger,
) -> tuple[SpeechConversationCandidate, ...]:
    """Extreu parelles explícites user→assistant sense inventar cap missatge."""

    return tuple(
        candidate
        for piece in ledger.pieces
        if piece.eligibility == "eligible"
        for candidate in _pair_turns(piece)
    )


def validate_human_conversations(
    ledger: LanguageLedger, candidates: tuple[SpeechConversationCandidate, ...]
) -> None:
    """Comprova que cada torn coincideixi literalment amb la seva peça font."""

    pieces = {piece.path: piece for piece in ledger.pieces}
    seen: set[str] = set()
    for candidate in candidates:
        if candidate.family_id in seen:
            raise ValueError(f"duplicate Language candidate: {candidate.family_id}")
        seen.add(candidate.family_id)
        piece = pieces.get(candidate.source_path)
        if piece is None or piece.eligibility != "eligible":
            raise ValueError(f"Language source is not eligible: {candidate.source_path}")
        if candidate.user != piece.text[candidate.user_start : candidate.user_end]:
            raise ValueError(f"user turn does not match source span: {candidate.family_id}")
        if candidate.assistant != piece.text[candidate.assistant_start : candidate.assistant_end]:
            raise ValueError(f"assistant turn does not match source span: {candidate.family_id}")


def write_human_conversations(ledger: LanguageLedger, *, work: Path) -> LanguageConversationReport:
    """Desa candidats interns i missatges literals provisionals per al filtre T014."""

    candidates = build_human_conversations(ledger)
    validate_human_conversations(ledger, candidates)
    work.mkdir(parents=True, exist_ok=True)
    _atomic_jsonl(work / "conversation-candidates.jsonl", (asdict(item) for item in candidates))
    _atomic_jsonl(
        work / "candidate-messages.jsonl", (item.to_public_record() for item in candidates)
    )
    report = LanguageConversationReport(
        eligible_pieces=ledger.report.eligible_pieces,
        pieces_with_explicit_dialogue=len({item.piece_id for item in candidates}),
        candidates=len(candidates),
        verbatim_assistant_turns=len(candidates),
    )
    _atomic_write(
        work / "conversation-report.json",
        json.dumps(asdict(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    return report


def _atomic_jsonl(path: Path, records: Iterable[object]) -> None:
    content = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records
    )
    _atomic_write(path, content)


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="")
    temporary.replace(path)
