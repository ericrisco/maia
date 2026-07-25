"""Tests for the PO quality sampling gate (PLAN M1.11)."""

from __future__ import annotations

import hashlib
from collections import Counter
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from maia.corpus.sampling import (
    DEFAULT_MIN_CLEAN_RATE,
    DEFAULT_SAMPLE_SIZE,
    FIELDNAMES,
    IncompleteReviewError,
    SampledDocument,
    Verdict,
    allocate,
    draw_sample,
    from_csv,
    main,
    render,
    score,
    to_csv,
    to_markdown,
)
from maia.schemas import CorpusDocument, Legal, License, Rang, Registre, Source

STAMP = datetime(2026, 8, 1, tzinfo=UTC)


def doc(
    text: str,
    *,
    source: Source = Source.GOVERN,
    license: License = License.PUBLIC_OFFICIAL,
    registre: Registre = Registre.ESTANDARD,
    speaker: str | None = None,
    legal: Legal | None = None,
) -> CorpusDocument:
    return CorpusDocument(
        text=text,
        source=source,
        # A stable slug, not hash(): builtin hash is salted per process, which would make
        # the fixtures differ run to run.
        url=f"https://www.example.ad/{hashlib.blake2b(text.encode(), digest_size=6).hexdigest()}",  # type: ignore[arg-type]
        fetched_at=STAMP,
        lang="ca",
        license=license,
        registre=registre,
        speaker=speaker,
        legal=legal,
    )


def corpus(**per_source: int) -> list[CorpusDocument]:
    """A corpus with the requested number of documents per source."""
    documents: list[CorpusDocument] = []
    for name, count in per_source.items():
        source = Source(name)
        for index in range(count):
            documents.append(
                doc(f"Document {index} de la font {name}, amb text prou llarg.", source=source)
            )
    return documents


# ─────────────────────────────────────────────────────────────
# Stratified allocation
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_allocation_is_proportional_and_sums_to_size() -> None:
    counts = Counter({"viquipedia": 900, "govern": 80, "juridic": 20})
    allocation = allocate(counts, 50)
    assert sum(allocation.values()) == 50
    assert allocation["viquipedia"] > allocation["govern"] > allocation["juridic"]


@pytest.mark.unit
def test_every_source_gets_at_least_one_slot() -> None:
    """The reason for stratifying at all.

    A uniform draw of 50 over this corpus would return ~0 legal documents, and a 96 % clean
    rate on Viquipèdia says nothing about whether the legal subcorpus is usable.
    """
    counts = Counter({"viquipedia": 100_000, "govern": 500, "juridic": 30, "comuns": 5})
    allocation = allocate(counts, 50)
    assert sum(allocation.values()) == 50
    assert all(count >= 1 for count in allocation.values())
    assert set(allocation) == set(counts)


@pytest.mark.unit
def test_allocation_never_exceeds_a_source_stock() -> None:
    counts = Counter({"viquipedia": 40, "govern": 3, "juridic": 2})
    allocation = allocate(counts, 50)
    assert all(allocation[source] <= counts[source] for source in allocation)


@pytest.mark.unit
def test_a_corpus_smaller_than_the_sample_is_taken_whole() -> None:
    counts = Counter({"govern": 3, "juridic": 2})
    assert allocate(counts, 50) == dict(counts)


@pytest.mark.unit
def test_more_sources_than_slots_gives_the_slots_to_the_largest() -> None:
    counts = Counter({"a": 100, "b": 90, "c": 80, "d": 70})
    allocation = allocate(counts, 2)
    assert allocation == {"a": 1, "b": 1}


@pytest.mark.unit
@pytest.mark.parametrize("size", [0, -1])
def test_a_non_positive_size_allocates_nothing(size: int) -> None:
    assert allocate(Counter({"govern": 10}), size) == {}


@pytest.mark.unit
def test_no_sources_allocates_nothing() -> None:
    assert allocate(Counter(), 50) == {}


# ─────────────────────────────────────────────────────────────
# Drawing
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_draw_returns_the_requested_size() -> None:
    sample = draw_sample(corpus(viquipedia=200, govern=50, juridic=20), size=50, seed=7)
    assert len(sample) == 50
    assert all(item.verdict is Verdict.PENDING for item in sample)


@pytest.mark.unit
def test_the_draw_is_reproducible_from_the_seed() -> None:
    # A gate whose sample cannot be redrawn is not evidence.
    pool = corpus(viquipedia=200, govern=50, juridic=20)
    first = draw_sample(pool, size=50, seed=7)
    second = draw_sample(pool, size=50, seed=7)
    assert [item.document.id for item in first] == [item.document.id for item in second]


@pytest.mark.unit
def test_a_different_seed_draws_a_different_sample() -> None:
    pool = corpus(viquipedia=200, govern=50, juridic=20)
    first = {item.document.id for item in draw_sample(pool, size=50, seed=7)}
    second = {item.document.id for item in draw_sample(pool, size=50, seed=8)}
    assert first != second


@pytest.mark.unit
def test_the_draw_does_not_depend_on_input_order() -> None:
    pool = corpus(viquipedia=200, govern=50, juridic=20)
    forwards = draw_sample(pool, size=30, seed=7)
    backwards = draw_sample(list(reversed(pool)), size=30, seed=7)
    assert [i.document.id for i in forwards] == [i.document.id for i in backwards]


@pytest.mark.unit
def test_a_stratified_draw_reaches_every_source() -> None:
    sample = draw_sample(corpus(viquipedia=5000, govern=200, juridic=30), size=50, seed=7)
    assert set(Counter(i.document.source.value for i in sample)) == {
        "viquipedia",
        "govern",
        "juridic",
    }


@pytest.mark.unit
def test_a_uniform_draw_can_miss_a_small_source() -> None:
    # The behaviour --uniform warns about, asserted so the difference is not theoretical.
    pool = corpus(viquipedia=5000, juridic=5)
    uniform = draw_sample(pool, size=50, seed=7, stratify=False)
    assert "juridic" not in {item.document.source.value for item in uniform}
    stratified = draw_sample(pool, size=50, seed=7)
    assert "juridic" in {item.document.source.value for item in stratified}


@pytest.mark.unit
def test_a_small_corpus_is_returned_whole() -> None:
    pool = corpus(govern=3, juridic=2)
    sample = draw_sample(pool, size=50, seed=7)
    assert len(sample) == 5
    assert {i.document.id for i in sample} == {d.id for d in pool}


@pytest.mark.unit
def test_an_empty_corpus_draws_nothing() -> None:
    assert draw_sample([], size=50, seed=7) == []


@pytest.mark.unit
def test_the_sample_is_grouped_by_source_for_the_reviewer() -> None:
    sample = draw_sample(corpus(viquipedia=100, govern=100, juridic=100), size=30, seed=7)
    sources = [item.document.source.value for item in sample]
    assert sources == sorted(sources)


@pytest.mark.unit
def test_documents_are_never_drawn_twice() -> None:
    sample = draw_sample(corpus(viquipedia=200, govern=50), size=50, seed=7)
    ids = [item.document.id for item in sample]
    assert len(ids) == len(set(ids))


# ─────────────────────────────────────────────────────────────
# The review sheet
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_csv_round_trips_the_sample() -> None:
    sample = draw_sample(corpus(govern=4, juridic=3), size=50, seed=7)
    restored = from_csv(to_csv(sample, seed=7))
    assert [i.document.id for i in restored] == [i.document.id for i in sample]
    assert [i.document.text for i in restored] == [i.document.text for i in sample]
    assert all(i.verdict is Verdict.PENDING for i in restored)


@pytest.mark.unit
def test_csv_round_trips_text_containing_newlines_and_commas() -> None:
    # Legal chunks always contain newlines; a naive split(",") sheet would corrupt them, and
    # the §3.1 id check on the way back is what would catch it.
    tricky = doc(
        'Constitució — Article 5\n\nLa Declaració, "Universal", és vigent;\ni prou.',
        source=Source.JURIDIC,
        legal=Legal(rang=Rang.CONSTITUCIO, article="5", consolidacio_data=date(1993, 5, 4)),
    )
    restored = from_csv(to_csv([SampledDocument(tricky)], seed=1))
    assert restored[0].document.text == tricky.text
    assert restored[0].document.id == tricky.id


@pytest.mark.unit
def test_the_sheet_records_the_seed() -> None:
    assert "seed=99" in to_csv(draw_sample(corpus(govern=2), size=50, seed=99), seed=99)


@pytest.mark.unit
def test_the_sheet_has_the_expected_columns() -> None:
    header = to_csv(draw_sample(corpus(govern=2), size=50, seed=1), seed=1).splitlines()[1]
    assert header.split(",") == list(FIELDNAMES)


@pytest.mark.unit
def test_verdicts_and_notes_are_read_back() -> None:
    sample = draw_sample(corpus(govern=3), size=50, seed=1)
    filled = [
        SampledDocument(sample[0].document, Verdict.CLEAN),
        SampledDocument(sample[1].document, Verdict.DIRTY, "menú de navegació"),
        SampledDocument(sample[2].document, Verdict.CLEAN, "correcte"),
    ]
    restored = from_csv(to_csv(filled, seed=1))
    assert [i.verdict for i in restored] == [Verdict.CLEAN, Verdict.DIRTY, Verdict.CLEAN]
    assert restored[1].note == "menú de navegació"


@pytest.mark.unit
@pytest.mark.parametrize("written", ["CLEAN", " clean ", "Dirty"])
def test_verdicts_are_read_case_and_space_insensitively(written: str) -> None:
    sheet = to_csv(draw_sample(corpus(govern=1), size=1, seed=1), seed=1)
    sheet = sheet.replace(",pending,", f",{written},")
    assert from_csv(sheet)[0].verdict in {Verdict.CLEAN, Verdict.DIRTY}


@pytest.mark.unit
def test_an_unrecognised_verdict_is_an_error_not_a_zero() -> None:
    # A typo must not silently become a clean document.
    sheet = to_csv(draw_sample(corpus(govern=1), size=1, seed=1), seed=1)
    with pytest.raises(ValueError, match="unrecognised verdict"):
        from_csv(sheet.replace(",pending,", ",clena,"))


@pytest.mark.unit
def test_a_sheet_missing_a_column_is_rejected() -> None:
    with pytest.raises(ValueError, match="missing column"):
        from_csv("id,source\nabc,govern\n")


@pytest.mark.unit
def test_an_empty_sheet_reads_as_no_documents() -> None:
    assert from_csv("") == []


@pytest.mark.unit
def test_markdown_companion_shows_text_and_metadata() -> None:
    legal_doc = doc(
        "Constitució del Principat d'Andorra — Article 5\n\nLa Declaració és vigent.",
        source=Source.JURIDIC,
        legal=Legal(rang=Rang.CONSTITUCIO, article="5", consolidacio_data=date(1993, 5, 4)),
    )
    speech = doc(
        "Bon dia a tothom, senyores i senyors consellers generals.",
        source=Source.CONSELL_DIARI_SESSIONS,
        registre=Registre.ANDORRA_PARLAT,
        speaker="Maria Font",
    )
    markdown = to_markdown([SampledDocument(legal_doc), SampledDocument(speech)], seed=42)
    assert "seed `42`" in markdown
    assert "La Declaració és vigent." in markdown
    assert "speaker: Maria Font" in markdown
    assert "article 5" in markdown
    assert "consolidated 1993-05-04" in markdown
    assert f"≥{DEFAULT_MIN_CLEAN_RATE:.0%} clean" in markdown


# ─────────────────────────────────────────────────────────────
# Scoring
# ─────────────────────────────────────────────────────────────


def _reviewed(clean: int, dirty: int, *, source: Source = Source.GOVERN) -> list[SampledDocument]:
    items = [
        SampledDocument(doc(f"Document net número {i}.", source=source), Verdict.CLEAN)
        for i in range(clean)
    ]
    items += [
        SampledDocument(doc(f"Document brut número {i}.", source=source), Verdict.DIRTY)
        for i in range(dirty)
    ]
    return items


@pytest.mark.unit
def test_the_gate_passes_at_exactly_the_threshold() -> None:
    result = score(_reviewed(48, 2))  # 96 %
    assert result.clean_rate == pytest.approx(0.96)
    assert result.passed
    assert "PASS" in render(result)


@pytest.mark.unit
def test_the_gate_fails_just_below_the_threshold() -> None:
    result = score(_reviewed(47, 3))  # 94 %
    assert result.clean_rate == pytest.approx(0.94)
    assert not result.passed
    assert "FAIL" in render(result)


@pytest.mark.unit
def test_exactly_95_percent_passes() -> None:
    assert score(_reviewed(19, 1)).passed  # 95 %


@pytest.mark.unit
def test_the_threshold_is_adjustable() -> None:
    sample = _reviewed(45, 5)  # 90 %
    assert not score(sample).passed
    assert score(sample, min_clean_rate=0.9).passed


@pytest.mark.unit
def test_a_pending_verdict_blocks_scoring() -> None:
    """The one way this gate could quietly fail.

    A half-finished sheet must not be scoreable: treating pending as clean would pass, and
    treating it as dirty would fail — both are answers the review has not given.
    """
    sample = [*_reviewed(48, 1), SampledDocument(doc("Encara sense revisar."))]
    with pytest.raises(IncompleteReviewError, match="still pending"):
        score(sample)


@pytest.mark.unit
def test_scoring_an_empty_sample_is_an_error() -> None:
    with pytest.raises(ValueError, match="sample is empty"):
        score([])


@pytest.mark.unit
def test_per_source_breakdown_locates_the_problem() -> None:
    # An overall pass can still hide one unusable subcorpus.
    sample = _reviewed(30, 0) + _reviewed(0, 4, source=Source.VIQUIPEDIA)
    result = score(sample, min_clean_rate=0.8)
    assert result.passed
    assert result.by_source["govern"] == (30, 0)
    assert result.by_source["viquipedia"] == (0, 4)
    rendered = render(result)
    assert "viquipedia: 0/4 clean (0%)" in rendered


@pytest.mark.unit
def test_notes_on_dirty_documents_are_surfaced() -> None:
    flagged = doc("Aquest document és un menú de navegació sencer.")
    sample = [*_reviewed(19, 0), SampledDocument(flagged, Verdict.DIRTY, "només navegació")]
    result = score(sample)
    assert result.notes == [(flagged.id, "només navegació")]
    assert "només navegació" in render(result)


@pytest.mark.unit
def test_notes_on_clean_documents_are_not_surfaced_as_problems() -> None:
    sample = [SampledDocument(doc("Un document correcte."), Verdict.CLEAN, "impecable")]
    assert score(sample).notes == []


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


def _corpus_file(path: Path, documents: list[CorpusDocument]) -> Path:
    path.write_text("".join(f"{d.model_dump_json()}\n" for d in documents), encoding="utf-8")
    return path


@pytest.mark.unit
def test_cli_draw_writes_both_artifacts(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = _corpus_file(tmp_path / "corpus.jsonl", corpus(govern=40, juridic=20))
    sheet = tmp_path / "review" / "sample.csv"
    reading = tmp_path / "review" / "sample.md"
    assert (
        main(
            [
                "draw",
                str(source),
                "--csv",
                str(sheet),
                "--markdown",
                str(reading),
                "--seed",
                "42",
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert f"drew {DEFAULT_SAMPLE_SIZE} documents (seed 42)" in out
    assert "govern=" in out and "juridic=" in out
    assert len(from_csv(sheet.read_text(encoding="utf-8"))) == DEFAULT_SAMPLE_SIZE
    assert "Corpus review sample" in reading.read_text(encoding="utf-8")


@pytest.mark.unit
def test_cli_draw_and_score_round_trip(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = _corpus_file(tmp_path / "corpus.jsonl", corpus(govern=30))
    sheet = tmp_path / "sample.csv"
    assert main(["draw", str(source), "--csv", str(sheet), "--size", "20", "--seed", "1"]) == 0

    # Stand in for the PO: mark one document dirty (95 % clean → passes).
    filled = from_csv(sheet.read_text(encoding="utf-8"))
    reviewed = [
        SampledDocument(item.document, Verdict.DIRTY if index == 0 else Verdict.CLEAN)
        for index, item in enumerate(filled)
    ]
    sheet.write_text(to_csv(reviewed, seed=1), encoding="utf-8")

    assert main(["score", str(sheet)]) == 0
    assert "PASS" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_score_exits_nonzero_when_the_gate_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sheet = tmp_path / "sample.csv"
    sheet.write_text(to_csv(_reviewed(15, 5), seed=1), encoding="utf-8")
    assert main(["score", str(sheet)]) == 1
    assert "FAIL" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_score_refuses_a_pending_sheet(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sheet = tmp_path / "sample.csv"
    sheet.write_text(
        to_csv(draw_sample(corpus(govern=5), size=5, seed=1), seed=1), encoding="utf-8"
    )
    assert main(["score", str(sheet)]) == 1
    assert "still pending" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_score_reports_a_bad_verdict(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sheet = tmp_path / "sample.csv"
    sheet.write_text(
        to_csv(_reviewed(1, 0), seed=1).replace(",clean,", ",maybe,"), encoding="utf-8"
    )
    assert main(["score", str(sheet)]) == 1
    assert "unrecognised verdict" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_draw_uniform_flag_is_honoured(tmp_path: Path) -> None:
    source = _corpus_file(tmp_path / "corpus.jsonl", corpus(viquipedia=500, juridic=5))
    sheet = tmp_path / "sample.csv"
    assert main(["draw", str(source), "--csv", str(sheet), "--seed", "7", "--uniform"]) == 0
    sources = {i.document.source.value for i in from_csv(sheet.read_text(encoding="utf-8"))}
    assert sources == {"viquipedia"}


@pytest.mark.unit
def test_cli_reports_a_missing_corpus(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        main(
            [
                "draw",
                str(tmp_path / "absent.jsonl"),
                "--csv",
                str(tmp_path / "s.csv"),
                "--seed",
                "1",
            ]
        )
        == 1
    )
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_missing_sheet(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["score", str(tmp_path / "absent.csv")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_rejects_an_invalid_corpus(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "corpus.jsonl"
    path.write_text("{bad}\n", encoding="utf-8")
    assert main(["draw", str(path), "--csv", str(tmp_path / "s.csv"), "--seed", "1"]) == 1
    assert "failed §3.1 validation" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_rejects_an_empty_corpus(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "corpus.jsonl"
    path.write_text("\n", encoding="utf-8")
    assert main(["draw", str(path), "--csv", str(tmp_path / "s.csv"), "--seed", "1"]) == 1
    assert "corpus is empty" in capsys.readouterr().err
