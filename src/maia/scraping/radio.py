"""Radio / oral subcorpus — PLAN M1.13.

RTVA broadcasts transcribed with ``whisper-large-v3-ca`` are the only source of *unedited*
spoken Andorran Catalan. The Diari de Sessions (M1.04) is edited before it is printed; radio
is not, so it is closer to how Andorrans actually talk — and it carries transcription error
the Diari does not. That is why it gets its own register, ``andorra_parlat_oral``, rather than
being folded into ``andorra_parlat``: downstream weights them differently.

**This subcorpus is grounding-only and the licence is not negotiable.** RTVA audio is not
ours to redistribute, so every document is stamped ``no-redistribute`` with no parameter to
override it — the text feeds the RAG index and grounds the synthetic dataset, and only
paraphrased knowledge ever reaches a public artifact. Making that a constant rather than an
argument is deliberate: there is no caller who should be able to ask for anything else.

What this module owns is everything between a transcript and §3.1 documents:

* **Segment merging.** Whisper emits a segment every few seconds. One segment is too short to
  be a useful chunk and a whole programme is too long, so consecutive segments are merged up
  to a character budget, preferring to break where a sentence ends and never merging across a
  long silence (which usually means the topic changed).
* **Hallucination filtering.** ``whisper-large-v3`` is well known to invent repeated text over
  silence, music and applause — "Subtítols per Amara.org" and the same clause ten times over.
  Left in, that fabricated text would be indistinguishable from real speech in the corpus.
  :func:`looks_hallucinated` catches the two signatures: near-zero vocabulary, and known
  boilerplate captions.
* **Oral cleaning**, reusing :func:`maia.scraping.diari.clean_oral` — the same conservative
  rule applies, strip bracketed annotations and tidy spacing, never touch the words, so
  genuine dialectal lexicon survives.

Both the audio and the transcription are **blocked-by-resource**: getting RTVA recordings is a
permissions question, and ``whisper-large-v3-ca`` needs a GPU. :class:`Transcriber` is the
seam, so everything above is exercised offline against fixture transcripts.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from maia.schemas import CorpusDocument, License, Registre, Source, normalize_text
from maia.scraping.diari import clean_oral

#: RTVA text is never publishable. Not a parameter — see the module docstring.
RADIO_LICENSE = License.NO_REDISTRIBUTE

#: Merge consecutive segments up to roughly this many characters.
DEFAULT_MAX_CHARS = 1200

#: A gap longer than this (seconds) ends a chunk: the programme has moved on.
DEFAULT_MAX_GAP = 3.0

#: Below this unique-word ratio, text is a phrase on repeat rather than speech.
MIN_UNIQUE_WORD_RATIO = 0.34

#: Captions whisper emits over music and silence. Verbatim artifacts of its training data.
_HALLUCINATION_MARKERS = (
    "subtítols per amara.org",
    "subtitols per amara.org",
    "subtítulos por amara.org",
    "subtitles by amara.org",
    "subtitled by",
    "transcripció de",
    "gràcies per veure el vídeo",
    "gracies per veure el video",
    "gracias por ver el video",
    "thanks for watching",
    "www.rtva.ad",
)

_WORD = re.compile(r"\w+", re.UNICODE)
_SENTENCE_END = re.compile(r"[.!?…]['\"»]?\s*$")


@dataclass(frozen=True)
class Segment:
    """One transcription segment: a span of audio and what was said in it."""

    start: float
    end: float
    text: str


class Transcriber(Protocol):
    """Turns an audio file into transcription segments.

    ``whisper-large-v3-ca`` satisfies this. It is a protocol rather than a concrete class so
    the pipeline needs neither a GPU nor the model to be tested.
    """

    def transcribe(self, audio: Path) -> Sequence[Segment]:
        """Transcribe ``audio`` into time-stamped segments."""


@dataclass(frozen=True)
class ProgrammeSpec:
    """Identity and provenance of one broadcast.

    §3.1 has no broadcast-date field, so ``url`` is the identity anchor (as for the Diari).
    ``programme`` is carried into ``topic`` so the corpus can be filtered by show without
    parsing URLs.
    """

    programme: str
    url: str
    topic: tuple[str, ...] = ()


def unique_word_ratio(text: str) -> float:
    """Share of distinct words in ``text`` — the cheap tell for repeated output."""
    words = _WORD.findall(text.lower())
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def looks_hallucinated(text: str, *, min_unique_word_ratio: float = MIN_UNIQUE_WORD_RATIO) -> bool:
    """Whether ``text`` looks like whisper output over silence rather than speech.

    Two independent signatures. **Known captions** are matched verbatim — whisper reproduces
    subtitle-credit boilerplate from its training data when there is nothing to transcribe.
    **Vocabulary collapse** catches the other mode, the same clause repeated: real speech of
    any length keeps introducing new words, so a very low unique-word ratio means the model
    was looping. Short text is exempt from the ratio test, where a low ratio is just how
    ordinary phrases work.
    """
    lowered = text.lower()
    if any(marker in lowered for marker in _HALLUCINATION_MARKERS):
        return True
    words = _WORD.findall(lowered)
    return len(words) >= 12 and unique_word_ratio(text) < min_unique_word_ratio


def merge_segments(
    segments: Iterable[Segment],
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    max_gap: float = DEFAULT_MAX_GAP,
) -> list[Segment]:
    """Merge consecutive segments into chunks of roughly ``max_chars``.

    A chunk is closed when adding the next segment would exceed the budget *and* the text so
    far ends on a sentence boundary — so a chunk overshoots slightly rather than cutting
    mid-sentence, which would leave both halves harder to retrieve. A silence longer than
    ``max_gap`` closes a chunk regardless: the programme has moved on.

    Timestamps are preserved as the span of the merged run, so a chunk can still be located
    in the recording.
    """
    merged: list[Segment] = []
    current: Segment | None = None

    for segment in segments:
        text = segment.text.strip()
        if not text:
            continue
        if current is None:
            current = Segment(segment.start, segment.end, text)
            continue

        gap = segment.start - current.end
        would_be = f"{current.text} {text}"
        over_budget = len(would_be) > max_chars and _SENTENCE_END.search(current.text)
        if gap > max_gap or over_budget:
            merged.append(current)
            current = Segment(segment.start, segment.end, text)
        else:
            current = Segment(current.start, segment.end, would_be)

    if current is not None:
        merged.append(current)
    return merged


def parse_programme(
    segments: Iterable[Segment],
    spec: ProgrammeSpec,
    *,
    fetched_at: datetime | None = None,
    max_chars: int = DEFAULT_MAX_CHARS,
    max_gap: float = DEFAULT_MAX_GAP,
    min_chars: int = 200,
) -> list[CorpusDocument]:
    """Turn a transcript into §3.1 documents, dropping hallucinated and trivial chunks."""
    stamp = fetched_at or datetime.now(UTC)
    topics = [spec.programme, *spec.topic]
    documents: list[CorpusDocument] = []

    for chunk in merge_segments(segments, max_chars=max_chars, max_gap=max_gap):
        text = clean_oral(chunk.text)
        if len(normalize_text(text)) < min_chars or looks_hallucinated(text):
            continue
        documents.append(
            CorpusDocument(
                text=text,
                source=Source.RTVA,
                url=spec.url,  # type: ignore[arg-type]
                fetched_at=stamp,
                lang="ca",
                topic=topics,
                license=RADIO_LICENSE,
                registre=Registre.ANDORRA_PARLAT_ORAL,
            )
        )
    return documents


def transcribe_programme(
    transcriber: Transcriber,
    audio: Path,
    spec: ProgrammeSpec,
    *,
    fetched_at: datetime | None = None,
    max_chars: int = DEFAULT_MAX_CHARS,
    max_gap: float = DEFAULT_MAX_GAP,
    min_chars: int = 200,
) -> list[CorpusDocument]:
    """Transcribe a recording and chunk it into §3.1 documents.

    Both halves of the live path are blocked-by-resource — obtaining the RTVA recording is a
    permissions question, and ``whisper-large-v3-ca`` needs a GPU — so ``transcriber`` is
    injected and this function holds no model-specific logic.
    """
    return parse_programme(
        transcriber.transcribe(audio),
        spec,
        fetched_at=fetched_at,
        max_chars=max_chars,
        max_gap=max_gap,
        min_chars=min_chars,
    )


def read_transcript(path: str | Path) -> list[Segment]:
    """Read a transcript in the ``start<TAB>end<TAB>text`` form used by the fixtures.

    Blank lines and ``#`` comments are ignored. This is the hand-off format for a transcript
    produced elsewhere (a GPU box, or a manual pass), so the chunking can be run and reviewed
    without re-transcribing.

    Raises:
        ValueError: on a malformed line — a silently skipped line would lose speech.
    """
    segments: list[Segment] = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3:
            raise ValueError(f"line {number}: expected 'start<TAB>end<TAB>text', got {line!r}")
        try:
            start, end = float(parts[0]), float(parts[1])
        except ValueError as exc:
            raise ValueError(f"line {number}: timestamps must be numbers, got {line!r}") from exc
        segments.append(Segment(start, end, parts[2].strip()))
    return segments
