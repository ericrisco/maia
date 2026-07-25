"""Tests for the corpus consolidation pipeline (PLAN M1.08)."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from maia.corpus.consolidate import (
    ConsolidationReport,
    consolidate,
    dump_report,
    main,
    min_chars_for,
    passes_language_filter,
    read_documents,
    render,
    renormalize,
    survivor_rank,
    write_partitioned,
)
from maia.schemas import CorpusDocument, Legal, License, Rang, Registre, Source

STAMP = datetime(2026, 8, 1, tzinfo=UTC)

FALLES = (
    "Les falles són una tradició molt antiga que se celebra a diverses parròquies del "
    "Principat. Cada any, quan arriba el solstici d'estiu, els fallaires baixen de la "
    "muntanya amb les falles enceses i il·luminen el poble sencer durant tota la nit. "
    "La celebració està inscrita a la llista del patrimoni cultural immaterial."
)
CONSELL = (
    "El Consell General és l'òrgan que representa el poble andorrà, exerceix la potestat "
    "legislativa, aprova els pressupostos de l'Estat i impulsa i controla l'acció política "
    "del Govern. Es compon d'un mínim de vint-i-vuit i un màxim de quaranta-dos consellers "
    "generals, la meitat elegits en circumscripció parroquial."
)
SPANISH = (
    "Andorra es un Estado independiente, de Derecho, Democrático y Social. Su denominación "
    "oficial es Principado de Andorra. La Constitución proclama como principios inspiradores "
    "de la acción del Estado andorrano el respeto y la promoción de la libertad, con la "
    "igualdad y la justicia. Esto es lo que establece este artículo, pero también hay que "
    "tener en cuenta las otras normas."
)


def doc(
    text: str,
    *,
    source: Source = Source.GOVERN,
    url: str = "https://www.govern.ad/pagina",
    license: License = License.PUBLIC_OFFICIAL,
    legal: Legal | None = None,
) -> CorpusDocument:
    return CorpusDocument(
        text=text,
        source=source,
        url=url,  # type: ignore[arg-type]
        fetched_at=STAMP,
        lang="ca",
        license=license,
        registre=Registre.ESTANDARD,
        legal=legal,
    )


# ─────────────────────────────────────────────────────────────
# Renormalization and the id
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_renormalize_recomputes_the_id() -> None:
    # A zero-width space is invisible and is not whitespace, so it changes the content hash.
    dirty = doc(f"Les\u200bfalles són una tradició. {FALLES}")
    cleaned = renormalize(dirty)
    assert cleaned is not None
    assert "\u200b" not in cleaned.text
    assert cleaned.id != dirty.id
    # The rebuilt document satisfies the §3.1 invariant: id == sha256 of normalized text.
    assert CorpusDocument.model_validate(json.loads(cleaned.model_dump_json())).id == cleaned.id


@pytest.mark.unit
def test_renormalize_preserves_every_other_field() -> None:
    legal = Legal(rang=Rang.CONSTITUCIO, article="5", consolidacio_data=date(1993, 5, 4))
    original = doc(
        f"  {FALLES}  ",
        source=Source.JURIDIC,
        url="https://www.portaljuridicandorra.ad/x",
        license=License.NO_REDISTRIBUTE,
        legal=legal,
    )
    cleaned = renormalize(original)
    assert cleaned is not None
    assert cleaned.source is Source.JURIDIC
    assert cleaned.license is License.NO_REDISTRIBUTE
    assert cleaned.legal == legal
    assert cleaned.fetched_at == STAMP
    assert str(cleaned.url) == str(original.url)


@pytest.mark.unit
def test_renormalize_returns_none_when_nothing_survives() -> None:
    assert renormalize(doc("\u200b\u200b\ufeff")) is None


@pytest.mark.unit
def test_two_documents_differing_only_in_invisibles_become_the_same_id() -> None:
    # This is why normalization runs before dedup: without it these are not duplicates.
    plain, spaced = renormalize(doc(FALLES)), renormalize(doc(FALLES.replace(" ", "\u00a0", 3)))
    assert plain is not None and spaced is not None
    assert plain.id == spaced.id


# ─────────────────────────────────────────────────────────────
# Per-source length floor
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_juridic_is_exempt_from_the_length_floor() -> None:
    assert min_chars_for(Source.JURIDIC) == 1
    assert min_chars_for(Source.GOVERN) == 200


@pytest.mark.unit
def test_a_short_legal_article_survives_consolidation() -> None:
    # The regression M1.06's D-0009 decision demands: a one-line article is not boilerplate,
    # and a blanket 200-character floor here would delete it.
    article = doc(
        "Constitució del Principat d'Andorra — Article 5\n\n"
        "La Declaració Universal dels Drets Humans és vigent a Andorra.",
        source=Source.JURIDIC,
        url="https://www.portaljuridicandorra.ad/constitucio",
        legal=Legal(rang=Rang.CONSTITUCIO, article="5", consolidacio_data=date(1993, 5, 4)),
    )
    result = consolidate([article])
    assert result.report.kept == 1
    assert result.report.dropped == []


@pytest.mark.unit
def test_a_short_non_legal_page_is_still_dropped() -> None:
    result = consolidate([doc("Massa curt per ser útil.")])
    assert result.report.kept == 0
    assert result.report.by_stage["boilerplate"] == 1


# ─────────────────────────────────────────────────────────────
# Language filter
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_spanish_is_dropped_and_catalan_kept() -> None:
    result = consolidate([doc(FALLES), doc(SPANISH, url="https://www.govern.ad/es")])
    assert result.report.kept == 1
    assert result.report.by_stage["language"] == 1
    assert result.documents[0].text.startswith("Les falles")


@pytest.mark.unit
def test_no_language_signal_is_kept_not_dropped() -> None:
    keep, rendered = passes_language_filter("Canillo Encamp Ordino Massana Escaldes")
    assert keep
    assert rendered.startswith("und")


@pytest.mark.unit
def test_the_language_verdict_is_recorded_for_the_report() -> None:
    result = consolidate([doc(SPANISH)])
    assert result.report.dropped[0].stage == "language"
    assert result.report.dropped[0].reason.startswith("es")
    assert result.report.dropped[0].url == "https://www.govern.ad/pagina"


# ─────────────────────────────────────────────────────────────
# Dedup
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_exact_duplicates_collapse() -> None:
    result = consolidate([doc(FALLES), doc(FALLES, url="https://www.govern.ad/altra")])
    assert result.report.kept == 1
    assert result.report.by_stage["exact-duplicate"] == 1


@pytest.mark.unit
def test_near_duplicates_collapse_and_the_longer_survives() -> None:
    printed = "Imprimir aquesta pàgina\n\n" + FALLES + "\n\nCompartir a les xarxes socials."
    result = consolidate([doc(FALLES), doc(printed, url="https://www.govern.ad/print")])
    assert result.report.kept == 1
    assert result.report.by_stage["near-duplicate"] == 1
    assert result.documents[0].text.startswith("Imprimir")  # the longer rendering


@pytest.mark.unit
def test_distinct_documents_both_survive() -> None:
    result = consolidate([doc(FALLES), doc(CONSELL, url="https://www.consellgeneral.ad/x")])
    assert result.report.kept == 2
    assert result.report.by_stage["near-duplicate"] == 0


@pytest.mark.unit
def test_a_publishable_duplicate_beats_a_no_redistribute_one_even_if_shorter() -> None:
    """The compliance rule: licence outranks length when collapsing duplicates.

    Keeping the restricted copy would carry it into the public dataset at M1.09/M6.01, so a
    shorter publishable rendering of the same content is the correct survivor.
    """
    restricted = doc(
        FALLES + "\n\nFont oficial.",
        source=Source.BOPA,
        url="https://www.bopa.ad/x",
        license=License.NO_REDISTRIBUTE,
    )
    publishable = doc(FALLES, source=Source.GOVERN, license=License.PUBLIC_OFFICIAL)
    for order in ([restricted, publishable], [publishable, restricted]):
        result = consolidate(order)
        assert result.report.kept == 1
        assert result.report.by_stage["near-duplicate"] == 1
        assert result.documents[0].license is License.PUBLIC_OFFICIAL
        assert result.report.no_redistribute == 0


@pytest.mark.unit
def test_an_exact_duplicate_also_respects_licence_over_arrival_order() -> None:
    """The same hole as above, in the exact-duplicate path.

    Identical text under two URLs can carry different licences. Keeping whichever arrived
    first would let a ``no-redistribute`` copy outlive a publishable one purely because of
    input ordering.
    """
    restricted = doc(
        FALLES, source=Source.BOPA, url="https://www.bopa.ad/x", license=License.NO_REDISTRIBUTE
    )
    publishable = doc(FALLES, source=Source.GOVERN, license=License.PUBLIC_OFFICIAL)
    for order in ([restricted, publishable], [publishable, restricted]):
        result = consolidate(order)
        assert result.report.kept == 1
        assert result.report.by_stage["exact-duplicate"] == 1
        assert result.documents[0].license is License.PUBLIC_OFFICIAL
        assert result.report.no_redistribute == 0
        # The dropped record names the restricted copy, not whichever came second.
        assert result.report.dropped[0].source == "bopa"


@pytest.mark.unit
def test_survivor_rank_puts_licence_before_length() -> None:
    short_public = doc("x" * 10)
    long_restricted = doc("y" * 1000, license=License.NO_REDISTRIBUTE)
    assert survivor_rank(short_public) > survivor_rank(long_restricted)


@pytest.mark.unit
def test_survivor_rank_is_deterministic_for_equal_licence_and_length() -> None:
    left, right = doc(FALLES), doc(CONSELL)
    assert (survivor_rank(left) > survivor_rank(right)) == (left.id > right.id)


# ─────────────────────────────────────────────────────────────
# Accounting
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_every_document_is_accounted_for() -> None:
    result = consolidate(
        [
            doc(FALLES),
            doc(FALLES, url="https://www.govern.ad/dup"),
            doc(SPANISH, url="https://www.govern.ad/es"),
            doc("curt"),
            doc(CONSELL, url="https://www.consellgeneral.ad/x"),
        ],
        report=ConsolidationReport(read=5),
    )
    assert result.report.balanced
    assert result.report.kept == 2
    assert len(result.report.dropped) == 3


@pytest.mark.unit
def test_report_counts_by_source_and_license() -> None:
    result = consolidate(
        [doc(FALLES), doc(CONSELL, source=Source.COMUNS, url="https://www.encamp.ad/x")]
    )
    assert result.report.by_source == {"govern": 1, "comuns": 1}
    assert result.report.by_license == {"public-official": 2}


@pytest.mark.unit
def test_surviving_no_redistribute_documents_are_flagged() -> None:
    result = consolidate(
        [
            doc(
                FALLES,
                source=Source.BOPA,
                url="https://www.bopa.ad/x",
                license=License.NO_REDISTRIBUTE,
            )
        ]
    )
    assert result.report.no_redistribute == 1
    assert "no-redistribute" in render(result.report)


@pytest.mark.unit
def test_render_and_dump_report_summarize_the_run() -> None:
    result = consolidate(
        [doc(FALLES), doc(SPANISH, url="https://www.govern.ad/es")],
        report=ConsolidationReport(read=2),
    )
    text = render(result.report)
    assert "kept: 1" in text
    assert "language=1" in text
    payload = json.loads(dump_report(result.report))
    assert payload["kept"] == 1
    assert payload["dropped_by_stage"] == {"language": 1}
    assert payload["balanced"] is True


# ─────────────────────────────────────────────────────────────
# Reading and writing
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_read_documents_reports_invalid_lines_without_guessing(tmp_path: Path) -> None:
    path = tmp_path / "corpus.jsonl"
    good = doc(FALLES).model_dump_json()
    path.write_text(
        f"{good}\n\n" + "{not json}\n" + '{"text": "manca la resta"}\n' + "[1, 2]\n",
        encoding="utf-8",
    )
    report = ConsolidationReport()
    documents = read_documents([path], report)
    assert len(documents) == 1
    assert report.read == 4
    assert len(report.invalid) == 3
    assert all("corpus.jsonl" in error.reason for error in report.invalid)


@pytest.mark.unit
def test_write_partitioned_creates_one_file_per_source(tmp_path: Path) -> None:
    documents = [
        doc(FALLES),
        doc(CONSELL, source=Source.COMUNS, url="https://www.encamp.ad/x"),
    ]
    written = write_partitioned(documents, tmp_path / "out")
    assert set(written) == {"govern", "comuns"}
    for source, path in written.items():
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        assert json.loads(lines[0])["source"] == source


@pytest.mark.unit
def test_written_output_round_trips_through_the_schema(tmp_path: Path) -> None:
    written = write_partitioned([doc(FALLES)], tmp_path / "out")
    raw = written["govern"].read_text(encoding="utf-8").strip()
    assert CorpusDocument.model_validate(json.loads(raw)).text == FALLES


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


def _write_corpus(path: Path, documents: list[CorpusDocument]) -> Path:
    path.write_text("".join(f"{d.model_dump_json()}\n" for d in documents), encoding="utf-8")
    return path


@pytest.mark.unit
def test_cli_consolidates_and_partitions(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    govern = _write_corpus(
        tmp_path / "govern.jsonl", [doc(FALLES), doc(FALLES, url="https://www.govern.ad/dup")]
    )
    comuns = _write_corpus(
        tmp_path / "comuns.jsonl",
        [doc(CONSELL, source=Source.COMUNS, url="https://www.encamp.ad/x")],
    )
    out = tmp_path / "out"
    assert main([str(govern), str(comuns), "--out", str(out)]) == 0
    captured = capsys.readouterr().out
    assert "read: 3" in captured
    assert "kept: 2" in captured
    assert (out / "govern.jsonl").is_file()
    assert (out / "comuns.jsonl").is_file()


@pytest.mark.unit
def test_cli_reports_a_missing_input(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "absent.jsonl"), "--out", str(tmp_path / "out")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_fails_when_nothing_survives(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = _write_corpus(tmp_path / "es.jsonl", [doc(SPANISH)])
    assert main([str(path), "--out", str(tmp_path / "out")]) == 1
    assert "produced no documents" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_strict_fails_on_invalid_input(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "mixed.jsonl"
    path.write_text(f"{doc(FALLES).model_dump_json()}\n{{bad}}\n", encoding="utf-8")
    out = tmp_path / "out"
    assert main([str(path), "--out", str(out)]) == 0  # tolerant by default
    assert main([str(path), "--out", str(out), "--strict"]) == 1
    assert "invalid input lines" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_threshold_is_configurable(tmp_path: Path) -> None:
    printed = "Imprimir aquesta pàgina\n\n" + FALLES + "\n\nCompartir a les xarxes socials."
    path = _write_corpus(
        tmp_path / "govern.jsonl", [doc(FALLES), doc(printed, url="https://www.govern.ad/print")]
    )
    out = tmp_path / "out"
    assert main([str(path), "--out", str(out), "--near-dup-threshold", "0.99"]) == 0
    assert len((out / "govern.jsonl").read_text(encoding="utf-8").splitlines()) == 2


@pytest.mark.unit
def test_a_document_that_is_only_invisible_characters_is_dropped() -> None:
    # Valid per §3.1 (text is one character long) but empty once normalized.
    result = consolidate([doc("​")])
    assert result.report.kept == 0
    assert result.report.by_stage["normalize"] == 1
    assert result.report.dropped[0].reason == "empty after normalization"


@pytest.mark.unit
def test_render_truncates_a_long_list_of_invalid_lines(tmp_path: Path) -> None:
    path = tmp_path / "broken.jsonl"
    path.write_text("{bad}\n" * 25, encoding="utf-8")
    report = ConsolidationReport()
    read_documents([path], report)
    assert len(report.invalid) == 25
    text = render(report)
    assert "… and 5 more invalid lines" in text


@pytest.mark.unit
def test_the_diari_floor_matches_its_producer(capsys: pytest.CaptureFixture[str]) -> None:
    """The bug D-0010 was written to prevent, missed for the Diari.

    `diari.parse_session` filters at 120 characters deliberately; consolidation's default 200
    floor was deleting every intervention between the two, filing them as `boilerplate`.
    """
    assert min_chars_for(Source.CONSELL_DIARI_SESSIONS) == 120
    text = (
        "Doncs miri, jo hi vaig cada any des dels vuit anys i sempre és igual d'emocionant, "
        "ves. La canalla ho espera tot l'any i els grans també."
    )
    assert 120 <= len(text) < 200
    intervention = doc(
        text,
        source=Source.CONSELL_DIARI_SESSIONS,
        url="https://www.consellgeneral.ad/diari/1",
    )
    result = consolidate([intervention], report=ConsolidationReport(read=1))
    assert result.report.kept == 1


@pytest.mark.unit
def test_drops_are_reported_per_source() -> None:
    # An aggregate `boilerplate=N` hides a filter deleting one whole subcorpus.
    result = consolidate(
        [
            doc(SPANISH, url="https://www.govern.ad/es"),
            doc("curt", source=Source.CULTURA, url="https://www.cultura.ad/x"),
        ],
        report=ConsolidationReport(read=2),
    )
    assert result.report.dropped_by_source == {"govern": 1, "cultura": 1}
    assert "dropped by source: cultura=1, govern=1" in render(result.report)


@pytest.mark.unit
def test_the_cli_fails_when_accounting_does_not_balance(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """`balanced` was computed and asserted only in a test — a real run could lose documents."""
    path = _write_corpus(tmp_path / "corpus.jsonl", [doc(FALLES)])
    real = consolidate

    def losing(documents, **kwargs):  # type: ignore[no-untyped-def]
        result = real(documents, **kwargs)
        result.report.read += 5  # simulate five documents that vanished
        return result

    monkeypatch.setattr("maia.corpus.consolidate.consolidate", losing)
    assert main([str(path), "--out", str(tmp_path / "out")]) == 1
    assert "accounting does not balance" in capsys.readouterr().err
