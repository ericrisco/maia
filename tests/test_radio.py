"""Tests for the radio / oral subcorpus (PLAN M1.13)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from maia.schemas import License, Registre, Source
from maia.scraping.radio import (
    DEFAULT_MAX_GAP,
    RADIO_LICENSE,
    ProgrammeSpec,
    Segment,
    looks_hallucinated,
    merge_segments,
    parse_programme,
    read_transcript,
    transcribe_programme,
    unique_word_ratio,
)

FIXTURE = Path(__file__).parent / "fixtures" / "rtva_programme_sample.tsv"
STAMP = datetime(2026, 8, 1, tzinfo=UTC)
SPEC = ProgrammeSpec(
    programme="El matí de RTVA",
    url="https://www.rtva.ad/programes/el-mati/2026-07-20",
    topic=("cultura",),
)


def segments(*items: tuple[float, float, str]) -> list[Segment]:
    return [Segment(start, end, text) for start, end, text in items]


# ─────────────────────────────────────────────────────────────
# Transcript reading
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_read_transcript_parses_the_fixture() -> None:
    parsed = read_transcript(FIXTURE)
    assert len(parsed) == 14
    assert parsed[0].start == 0.0
    assert parsed[0].end == 4.2
    assert parsed[0].text.startswith("Bon dia a tothom")


@pytest.mark.unit
def test_read_transcript_ignores_comments_and_blanks(tmp_path: Path) -> None:
    path = tmp_path / "t.tsv"
    path.write_text("# comentari\n\n0.0\t1.0\tHola\n   \n", encoding="utf-8")
    assert read_transcript(path) == [Segment(0.0, 1.0, "Hola")]


@pytest.mark.unit
def test_a_malformed_transcript_line_raises_rather_than_being_skipped(tmp_path: Path) -> None:
    # Silently skipping would lose speech, which is the one thing this corpus is for.
    path = tmp_path / "t.tsv"
    path.write_text("0.0\tno hi ha tercer camp\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected 'start<TAB>end<TAB>text'"):
        read_transcript(path)


@pytest.mark.unit
def test_non_numeric_timestamps_raise(tmp_path: Path) -> None:
    path = tmp_path / "t.tsv"
    path.write_text("inici\tfi\tHola\n", encoding="utf-8")
    with pytest.raises(ValueError, match="timestamps must be numbers"):
        read_transcript(path)


# ─────────────────────────────────────────────────────────────
# Segment merging
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_consecutive_segments_merge_into_one_chunk() -> None:
    merged = merge_segments(
        segments((0.0, 2.0, "Bon dia."), (2.0, 4.0, "Com esteu?")), max_chars=1000
    )
    assert len(merged) == 1
    assert merged[0].text == "Bon dia. Com esteu?"
    # Timestamps span the merged run, so a chunk stays locatable in the recording.
    assert (merged[0].start, merged[0].end) == (0.0, 4.0)


@pytest.mark.unit
def test_a_long_silence_closes_a_chunk() -> None:
    merged = merge_segments(
        segments((0.0, 2.0, "Primera part."), (30.0, 32.0, "Segona part.")), max_chars=1000
    )
    assert [chunk.text for chunk in merged] == ["Primera part.", "Segona part."]


@pytest.mark.unit
def test_a_short_gap_does_not_close_a_chunk() -> None:
    merged = merge_segments(
        segments((0.0, 2.0, "Primera part."), (2.0 + DEFAULT_MAX_GAP - 0.1, 6.0, "Segona part.")),
        max_chars=1000,
    )
    assert len(merged) == 1


@pytest.mark.unit
def test_the_budget_only_breaks_at_a_sentence_boundary() -> None:
    """Overshooting beats cutting mid-sentence.

    A chunk split in the middle of a clause leaves both halves harder to retrieve, so the
    budget is a target rather than a hard limit.
    """
    merged = merge_segments(
        segments(
            (0.0, 2.0, "Una frase sense acabar i que continua"),
            (2.0, 4.0, "encara una mica més enllà del pressupost."),
            (4.0, 6.0, "Ja podem tallar aquí."),
        ),
        max_chars=20,
    )
    assert merged[0].text.endswith("del pressupost.")
    assert len(merged) == 2


@pytest.mark.unit
def test_blank_segments_are_dropped() -> None:
    merged = merge_segments(
        segments((0.0, 1.0, "   "), (1.0, 2.0, "Text real."), (2.0, 3.0, "")), max_chars=1000
    )
    assert [chunk.text for chunk in merged] == ["Text real."]


@pytest.mark.unit
def test_merging_nothing_yields_nothing() -> None:
    assert merge_segments([]) == []
    assert merge_segments(segments((0.0, 1.0, "  "))) == []


# ─────────────────────────────────────────────────────────────
# Hallucination filtering
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_unique_word_ratio() -> None:
    assert unique_word_ratio("una dues tres") == 1.0
    assert unique_word_ratio("una una una una") == 0.25
    assert unique_word_ratio("") == 0.0


@pytest.mark.unit
@pytest.mark.parametrize(
    "caption",
    [
        "Subtítols per Amara.org",
        "subtítulos por amara.org",
        "Subtitles by Amara.org",
        "Gràcies per veure el vídeo",
        "www.rtva.ad",
    ],
)
def test_known_whisper_captions_are_caught(caption: str) -> None:
    # whisper reproduces subtitle-credit boilerplate from its training data over silence.
    assert looks_hallucinated(caption)


@pytest.mark.unit
def test_a_looping_phrase_is_caught() -> None:
    assert looks_hallucinated("gràcies " * 14)


@pytest.mark.unit
def test_real_speech_is_not_flagged() -> None:
    speech = (
        "Doncs miri, jo hi vaig des dels vuit anys, i cada any és igual d'emocionant, tot i "
        "que ara costa més pujar la muntanya amb les falles enceses."
    )
    assert not looks_hallucinated(speech)


@pytest.mark.unit
def test_short_text_is_exempt_from_the_vocabulary_test() -> None:
    # "sí, sí, sí" is how people talk; only sustained repetition is a hallucination.
    assert not looks_hallucinated("Sí, sí, sí.")
    assert not looks_hallucinated("Bon dia, bon dia.")


@pytest.mark.unit
def test_the_vocabulary_threshold_is_adjustable() -> None:
    text = "una dues una dues una dues una dues una dues una dues"
    assert looks_hallucinated(text)
    assert not looks_hallucinated(text, min_unique_word_ratio=0.1)


# ─────────────────────────────────────────────────────────────
# §3.1 documents
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_fixture_programme_becomes_documents() -> None:
    documents = parse_programme(read_transcript(FIXTURE), SPEC, fetched_at=STAMP)
    assert documents
    for doc in documents:
        assert doc.source is Source.RTVA
        assert doc.registre is Registre.ANDORRA_PARLAT_ORAL
        assert doc.license is License.NO_REDISTRIBUTE
        assert doc.lang == "ca"
        assert doc.fetched_at == STAMP
        assert str(doc.url) == SPEC.url
        assert doc.topic == ["El matí de RTVA", "cultura"]


@pytest.mark.unit
def test_hallucinations_never_reach_the_corpus() -> None:
    text = " ".join(doc.text for doc in parse_programme(read_transcript(FIXTURE), SPEC))
    assert "Amara.org" not in text
    assert "gràcies gràcies gràcies" not in text.lower()
    # …while the real speech around them survives.
    assert "falles" in text
    assert "fallaire" in text or "fallaires" in text


@pytest.mark.unit
def test_the_licence_cannot_be_anything_but_no_redistribute() -> None:
    """RTVA text is not ours to redistribute, so there is no parameter to get wrong."""
    assert RADIO_LICENSE is License.NO_REDISTRIBUTE
    documents = parse_programme(read_transcript(FIXTURE), SPEC, fetched_at=STAMP)
    assert all(not doc.license.is_public() for doc in documents)


@pytest.mark.unit
def test_short_chunks_are_dropped() -> None:
    documents = parse_programme(
        segments((0.0, 2.0, "Massa curt.")), SPEC, fetched_at=STAMP, min_chars=200
    )
    assert documents == []


@pytest.mark.unit
def test_min_chars_can_be_lowered() -> None:
    documents = parse_programme(
        segments((0.0, 2.0, "Un fragment curt però vàlid.")),
        SPEC,
        fetched_at=STAMP,
        min_chars=10,
    )
    assert len(documents) == 1
    assert documents[0].text == "Un fragment curt però vàlid."


@pytest.mark.unit
def test_bracketed_annotations_are_cleaned() -> None:
    documents = parse_programme(
        segments((0.0, 5.0, "Bon dia [música] a tothom i benvinguts (rialles) al programa.")),
        SPEC,
        fetched_at=STAMP,
        min_chars=10,
    )
    assert documents[0].text == "Bon dia a tothom i benvinguts al programa."


@pytest.mark.unit
def test_dialectal_words_survive_cleaning() -> None:
    # The same rule as the Diari: clean artifacts, never touch the words.
    spoken = "Hi ha molta canalla al poble i la gent hi va d'allò més contenta, ves."
    documents = parse_programme(segments((0.0, 5.0, spoken)), SPEC, fetched_at=STAMP, min_chars=10)
    assert documents[0].text == spoken


@pytest.mark.unit
def test_an_empty_transcript_yields_no_documents() -> None:
    assert parse_programme([], SPEC, fetched_at=STAMP) == []


@pytest.mark.unit
def test_topic_defaults_to_just_the_programme_name() -> None:
    spec = ProgrammeSpec(programme="Notícies", url="https://www.rtva.ad/noticies/1")
    documents = parse_programme(
        segments((0.0, 5.0, "Una notícia prou llarga per passar el filtre de longitud mínima.")),
        spec,
        fetched_at=STAMP,
        min_chars=10,
    )
    assert documents[0].topic == ["Notícies"]


# ─────────────────────────────────────────────────────────────
# The transcriber seam (audio + GPU are blocked-by-resource)
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_transcribe_programme_drives_the_injected_transcriber(tmp_path: Path) -> None:
    calls: list[Path] = []

    class FakeWhisper:
        def transcribe(self, audio: Path) -> list[Segment]:
            calls.append(audio)
            return read_transcript(FIXTURE)

    audio = tmp_path / "programa.mp3"
    audio.write_bytes(b"not really audio")
    documents = transcribe_programme(FakeWhisper(), audio, SPEC, fetched_at=STAMP)
    assert calls == [audio]
    assert documents
    assert all(doc.source is Source.RTVA for doc in documents)


@pytest.mark.unit
def test_a_transcriber_returning_nothing_yields_no_documents(tmp_path: Path) -> None:
    class SilentWhisper:
        def transcribe(self, audio: Path) -> list[Segment]:
            return []

    assert transcribe_programme(SilentWhisper(), tmp_path / "a.mp3", SPEC) == []
