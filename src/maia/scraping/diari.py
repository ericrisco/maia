"""Diari de Sessions parser — PLAN M1.04.

Turns a Consell General session transcript (manually downloaded — sindicatura.ad blocks
automated access, so the *download* is a blocked-by-resource manual/email step) into §3.1
corpus documents: one per whitelisted speaker's intervention, oral artifacts cleaned,
tagged ``registre=andorra_parlat`` and ``source=consell_diari_sessions``.

The whitelist of parliamentarians is a PO input (M1.05); this module only provides the
mechanism (:func:`read_whitelist`) and the deterministic split/clean/filter logic. Risk
control (D7): register/lexicon only — mix speakers, never clone a person's voice, and no
attributed political opinions reach the public dataset.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from maia.schemas import CorpusDocument, License, Registre, Source, normalize_text

# Speaker header at line start, e.g. "El Sr. Nom Cognom:", "La Sra. X:",
# "El M. I. Sr. President:" (Molt Il·lustre honorific tolerated).
_HEADER = re.compile(
    r"^[ \t]*(?:El|La)\s+(?:M\.\s*I\.\s*)?(?:Sr|Sra)\.?\s+(?P<name>[^:\n]+?):",
    re.MULTILINE,
)

# Stage directions / editorial notes: "(rialles)", "[inaudible]", "(Se suspèn la sessió)".
_STAGE = re.compile(r"[(\[][^)\]]*[)\]]")


@dataclass(frozen=True)
class SpeakerTurn:
    """One intervention: the speaker's name (as printed) and the raw turn text."""

    speaker: str
    text: str


def _norm_name(name: str) -> str:
    return re.sub(r"\s+", " ", name).strip().lower()


def split_interventions(transcript: str) -> list[SpeakerTurn]:
    """Split a transcript into interventions by speaker header."""
    matches = list(_HEADER.finditer(transcript))
    turns: list[SpeakerTurn] = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(transcript)
        turns.append(
            SpeakerTurn(speaker=match.group("name").strip(), text=transcript[start:end].strip())
        )
    return turns


def clean_oral(text: str) -> str:
    """Remove stage directions/editorial notes and normalize spacing.

    Deliberately conservative: it strips bracketed annotations and collapses whitespace but
    leaves the words themselves untouched, so genuine dialectal lexicon survives.
    """
    text = _STAGE.sub("", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def read_whitelist(path: str | Path) -> set[str]:
    """Read a speaker whitelist file (one name per line; ``#`` comments and blanks ignored).

    The names themselves are a PO input (M1.05) — this only parses the file.
    """
    names: set[str] = set()
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            names.add(stripped)
    return names


def parse_session(
    transcript: str,
    *,
    whitelist: Iterable[str],
    session_url: str,
    fetched_at: datetime | None = None,
    topic: Iterable[str] | None = None,
    min_chars: int = 120,
) -> list[CorpusDocument]:
    """Parse a session transcript into §3.1 documents for whitelisted speakers only.

    ``session_url`` carries the session's provenance (the §3.1 schema has no session/date
    field, so the source URL is the identity anchor). Interventions shorter than
    ``min_chars`` after cleaning are dropped.
    """
    stamp = fetched_at or datetime.now(UTC)
    allow = {_norm_name(n) for n in whitelist}
    topics = list(topic) if topic is not None else []
    docs: list[CorpusDocument] = []
    for turn in split_interventions(transcript):
        if _norm_name(turn.speaker) not in allow:
            continue
        text = clean_oral(turn.text)
        if len(normalize_text(text)) < min_chars:
            continue
        docs.append(
            CorpusDocument(
                text=text,
                source=Source.CONSELL_DIARI_SESSIONS,
                url=session_url,  # type: ignore[arg-type]
                fetched_at=stamp,
                lang="ca",
                topic=topics,
                license=License.PUBLIC_OFFICIAL,
                registre=Registre.ANDORRA_PARLAT,
                speaker=turn.speaker,
            )
        )
    return docs
