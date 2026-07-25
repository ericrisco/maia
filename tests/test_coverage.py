"""Tests for the F1 corpus coverage report (PLAN M1.10)."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from maia.corpus.coverage import (
    CHARS_PER_TOKEN,
    TARGET_MAX_TOKENS,
    TARGET_MIN_TOKENS,
    CoverageReport,
    Volume,
    build_report,
    count_words,
    estimate_tokens,
    main,
    to_json,
    to_markdown,
    tokenizer_counter,
)
from maia.schemas import CorpusDocument, Legal, License, Rang, Registre, Source

STAMP = datetime(2026, 8, 1, tzinfo=UTC)

PROSE = (
    "Les falles són una tradició molt antiga que se celebra a diverses parròquies del "
    "Principat cada any quan arriba el solstici d'estiu."
)


def doc(
    text: str = PROSE,
    *,
    source: Source = Source.GOVERN,
    url: str = "https://www.govern.ad/pagina",
    license: License = License.PUBLIC_OFFICIAL,
    registre: Registre = Registre.ESTANDARD,
    speaker: str | None = None,
    legal: Legal | None = None,
) -> CorpusDocument:
    return CorpusDocument(
        text=text,
        source=source,
        url=url,  # type: ignore[arg-type]
        fetched_at=STAMP,
        lang="ca",
        license=license,
        registre=registre,
        speaker=speaker,
        legal=legal,
    )


def speech(text: str, speaker: str) -> CorpusDocument:
    return doc(
        text,
        source=Source.CONSELL_DIARI_SESSIONS,
        url=f"https://www.consellgeneral.ad/diari/{speaker.replace(' ', '-')}",
        registre=Registre.ANDORRA_PARLAT,
        speaker=speaker,
    )


def article(number: str, *, llei: str | None, rang: Rang, day: date) -> CorpusDocument:
    return doc(
        f"Article {number}\n\n{PROSE} Aquest és l'article {number}.",
        source=Source.JURIDIC,
        url=f"https://www.portaljuridicandorra.ad/{llei or 'constitucio'}/{number}",
        legal=Legal(rang=rang, article=number, consolidacio_data=day, llei=llei),
    )


# ─────────────────────────────────────────────────────────────
# Counting
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_token_estimate_follows_the_documented_ratio() -> None:
    text = "x" * 370
    assert estimate_tokens(text) == round(370 / CHARS_PER_TOKEN)
    assert estimate_tokens("") == 0


@pytest.mark.unit
def test_word_count_is_whitespace_delimited() -> None:
    assert count_words("una  dues\ttres\nquatre") == 4
    assert count_words("   ") == 0


@pytest.mark.unit
def test_a_real_tokenizer_can_be_injected() -> None:
    # The seam that makes the report exact once the Gemma tokenizer is available.
    report = build_report(
        [doc(), doc(f"{PROSE} Un altre.", url="https://www.govern.ad/b")],
        count_tokens=lambda _t: 100,
    )
    assert report.total.estimated_tokens == 200


@pytest.mark.unit
def test_tokenizer_counter_wraps_a_tokenizer_object() -> None:
    """The counter takes a tokenizer rather than building one.

    That is what keeps ``transformers`` and the gated Gemma download out of this module: the
    blocked-by-resource part is the caller's, and the wiring is testable with a stand-in.
    """

    class WordTokenizer:
        def encode(self, text: str, add_special_tokens: bool = True) -> list[int]:
            assert add_special_tokens is False  # the report counts content, not markers
            return list(range(len(text.split())))

    counter = tokenizer_counter(WordTokenizer())
    assert counter("una dues tres") == 3
    report = build_report([doc()], count_tokens=counter)
    assert report.total.estimated_tokens == count_words(PROSE)


@pytest.mark.unit
def test_volume_accumulates_all_four_measures() -> None:
    report = build_report([doc()])
    volume = report.total
    assert volume.documents == 1
    assert volume.characters == len(PROSE)
    assert volume.words == count_words(PROSE)
    assert volume.estimated_tokens == estimate_tokens(PROSE)


# ─────────────────────────────────────────────────────────────
# Breakdowns
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_by_source_breakdown_and_shares() -> None:
    report = build_report(
        [
            doc(),
            doc(url="https://www.govern.ad/b"),
            doc(source=Source.CULTURA, url="https://www.cultura.ad/a"),
        ]
    )
    assert report.by_source["govern"].documents == 2
    assert report.by_source["cultura"].documents == 1
    assert report.share("govern") == pytest.approx(2 / 3)
    assert report.share("cultura") == pytest.approx(1 / 3)
    assert sum(report.share(name) for name in report.by_source) == pytest.approx(1.0)


@pytest.mark.unit
def test_publishable_and_grounding_only_are_split_by_licence() -> None:
    report = build_report(
        [
            doc(f"{PROSE} Del Govern."),
            doc(
                f"{PROSE} De la Viquipèdia.",
                url="https://ca.wikipedia.org/a",
                source=Source.VIQUIPEDIA,
                license=License.CC_BY_SA_3_0,
            ),
            doc(
                PROSE,
                url="https://www.bopa.ad/a",
                source=Source.BOPA,
                license=License.NO_REDISTRIBUTE,
            ),
        ]
    )
    assert report.publishable.documents == 2
    assert report.grounding_only.documents == 1
    assert report.grounding_only.estimated_tokens == estimate_tokens(PROSE)


@pytest.mark.unit
def test_a_corpus_with_no_restricted_content_reports_zero_grounding_only() -> None:
    report = build_report([doc()])
    assert report.grounding_only == Volume()
    assert report.publishable.documents == 1


@pytest.mark.unit
def test_registre_breakdown_and_speaker_counts() -> None:
    report = build_report(
        [
            doc(),
            speech(f"{PROSE} Primera intervenció.", "Maria Font"),
            speech(f"{PROSE} Segona intervenció.", "Maria Font"),
            speech(f"{PROSE} Tercera intervenció.", "Joan Martí"),
        ]
    )
    assert report.by_registre["estandard"].documents == 1
    assert report.by_registre["andorra_parlat"].documents == 3
    assert report.speakers == {"Maria Font": 2, "Joan Martí": 1}


@pytest.mark.unit
def test_legal_coverage_counts_articles_per_law() -> None:
    report = build_report(
        [
            article("1", llei=None, rang=Rang.CONSTITUCIO, day=date(1993, 5, 4)),
            article("2", llei=None, rang=Rang.CONSTITUCIO, day=date(1993, 5, 4)),
            article("1", llei="Llei 9/2005", rang=Rang.QUALIFICADA, day=date(2024, 4, 1)),
        ]
    )
    by_citation = {law.citation: law for law in report.laws}
    # The Constitution has no `llei` number, so it is keyed by its rank.
    assert by_citation["constitucio"].articles == 2
    assert by_citation["constitucio"].rang == "constitucio"
    assert by_citation["Llei 9/2005"].articles == 1
    assert by_citation["Llei 9/2005"].consolidacio_data == "2024-04-01"


@pytest.mark.unit
def test_repeated_article_numbers_within_a_law_count_once() -> None:
    # Articles are counted as a set: the same article ingested twice is not coverage.
    report = build_report(
        [
            article("5", llei="Llei 9/2005", rang=Rang.QUALIFICADA, day=date(2024, 4, 1)),
            article("5", llei="Llei 9/2005", rang=Rang.QUALIFICADA, day=date(2024, 4, 1)),
        ]
    )
    assert report.laws[0].articles == 1


@pytest.mark.unit
def test_length_summary() -> None:
    report = build_report(
        [doc("a" * n, url=f"https://www.govern.ad/{n}") for n in (100, 200, 300, 400, 5000)]
    )
    summary = report.length_summary
    assert summary["min"] == 100
    assert summary["median"] == 300
    assert summary["max"] == 5000
    assert 400 <= summary["p90"] <= 5000


@pytest.mark.unit
def test_length_summary_of_an_empty_corpus_is_zeroed() -> None:
    assert build_report([]).length_summary == {"min": 0, "median": 0, "p90": 0, "max": 0}


@pytest.mark.unit
def test_share_of_an_empty_corpus_does_not_divide_by_zero() -> None:
    assert build_report([]).share("govern") == 0.0


# ─────────────────────────────────────────────────────────────
# Target and integrity
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        (TARGET_MIN_TOKENS - 1, "below"),
        (TARGET_MIN_TOKENS, "within"),
        (TARGET_MAX_TOKENS, "within"),
        (TARGET_MAX_TOKENS + 1, "above"),
    ],
)
def test_target_status_boundaries(tokens: int, expected: str) -> None:
    report = build_report([doc()], count_tokens=lambda _t: tokens)
    assert report.target_status == expected


@pytest.mark.unit
def test_a_small_corpus_is_below_target() -> None:
    assert build_report([doc()]).target_status == "below"


@pytest.mark.unit
def test_duplicate_ids_are_reported() -> None:
    # Consolidation should have removed these; the report checks the artifact anyway.
    report = build_report([doc(), doc(url="https://www.govern.ad/altra-url")])
    assert len(report.duplicate_ids) == 1
    assert not report.integrity_ok


@pytest.mark.unit
def test_a_mismatched_id_is_reported() -> None:
    good = doc()
    tampered = good.model_copy(update={"text": f"{PROSE} Text canviat sense refer l'id."})
    report = build_report([tampered])
    assert report.mismatched_ids == [good.id]
    assert not report.integrity_ok


@pytest.mark.unit
def test_a_clean_corpus_passes_integrity() -> None:
    report = build_report(
        [doc(), doc(f"{PROSE} Un altre document.", url="https://www.govern.ad/b")]
    )
    assert report.integrity_ok
    assert report.duplicate_ids == []
    assert report.mismatched_ids == []


# ─────────────────────────────────────────────────────────────
# Rendering
# ─────────────────────────────────────────────────────────────


def _full_corpus() -> list[CorpusDocument]:
    # Distinct text per document: in a consolidated corpus identical text would already have
    # collapsed into one document, and reusing it here would trip the integrity check.
    return [
        doc(f"{PROSE} Pàgina del Govern."),
        doc(f"{PROSE} Pàgina de Cultura.", source=Source.CULTURA, url="https://www.cultura.ad/a"),
        doc(
            f"{PROSE} Edicte publicat al BOPA.",
            source=Source.BOPA,
            url="https://www.bopa.ad/a",
            license=License.NO_REDISTRIBUTE,
        ),
        speech(f"{PROSE} Una intervenció.", "Maria Font"),
        article("1", llei="Llei 9/2005", rang=Rang.QUALIFICADA, day=date(2024, 4, 1)),
    ]


@pytest.mark.unit
def test_markdown_covers_every_f1_question() -> None:
    markdown = to_markdown(build_report(_full_corpus()))
    for heading in (
        "# Corpus coverage report",
        "## By source",
        "## By licence",
        "## By register",
        "## Spoken subcorpus",
        "## Juridical subcorpus",
        "## Document length",
        "## Integrity",
    ):
        assert heading in markdown
    assert "estimates" in markdown  # the token caveat is never dropped
    assert "`govern`" in markdown
    assert "Maria Font" in markdown
    assert "Llei 9/2005" in markdown
    assert "Grounding-only:" in markdown


@pytest.mark.unit
def test_markdown_marks_restricted_licences_as_not_publishable() -> None:
    markdown = to_markdown(build_report(_full_corpus()))
    restricted_row = next(
        line for line in markdown.splitlines() if line.startswith("| `no-redistribute`")
    )
    assert restricted_row.endswith("**no** |")


@pytest.mark.unit
def test_markdown_handles_a_corpus_with_no_legal_documents() -> None:
    markdown = to_markdown(build_report([doc()]))
    assert "_No legal documents in this corpus._" in markdown


@pytest.mark.unit
def test_markdown_flags_a_failing_integrity_check() -> None:
    markdown = to_markdown(build_report([doc(), doc(url="https://www.govern.ad/dup")]))
    assert "duplicate id" in markdown


@pytest.mark.unit
def test_markdown_reports_target_status() -> None:
    assert "below target" in to_markdown(build_report([doc()]))
    healthy = build_report([doc()], count_tokens=lambda _t: TARGET_MIN_TOKENS)
    assert "within target" in to_markdown(healthy)
    big = build_report([doc()], count_tokens=lambda _t: TARGET_MAX_TOKENS + 1)
    assert "above target" in to_markdown(big)


@pytest.mark.unit
def test_json_is_machine_readable_and_complete() -> None:
    payload = json.loads(to_json(build_report(_full_corpus())))
    assert payload["total"]["documents"] == 5
    assert payload["target"]["status"] == "below"
    assert payload["target"]["min_tokens"] == TARGET_MIN_TOKENS
    assert set(payload["by_source"]) == {
        "govern",
        "cultura",
        "bopa",
        "consell_diari_sessions",
        "juridic",
    }
    assert payload["by_source"]["govern"]["share"] == pytest.approx(
        build_report(_full_corpus()).share("govern"), abs=0.0001
    )
    assert payload["grounding_only"]["documents"] == 1
    assert payload["speakers"] == {"Maria Font": 1}
    assert payload["laws"][0]["citation"] == "Llei 9/2005"
    assert payload["integrity"]["ok"] is True


@pytest.mark.unit
def test_empty_report_renders_without_raising() -> None:
    report = CoverageReport()
    assert "# Corpus coverage report" in to_markdown(report)
    assert json.loads(to_json(report))["total"]["documents"] == 0


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


def _corpus_file(path: Path, documents: list[CorpusDocument]) -> Path:
    path.write_text("".join(f"{d.model_dump_json()}\n" for d in documents), encoding="utf-8")
    return path


@pytest.mark.unit
def test_cli_prints_markdown_by_default(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    corpus = _corpus_file(tmp_path / "corpus.jsonl", _full_corpus())
    assert main([str(corpus)]) == 0
    out = capsys.readouterr().out
    assert "# Corpus coverage report" in out
    assert "## By licence" in out


@pytest.mark.unit
def test_cli_writes_both_artifacts(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    corpus = _corpus_file(tmp_path / "corpus.jsonl", _full_corpus())
    markdown = tmp_path / "report" / "coverage.md"
    payload = tmp_path / "report" / "coverage.json"
    assert main([str(corpus), "--markdown", str(markdown), "--json", str(payload)]) == 0
    assert "# Corpus coverage report" in markdown.read_text(encoding="utf-8")
    assert json.loads(payload.read_text(encoding="utf-8"))["total"]["documents"] == 5
    assert "5 documents" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_fails_on_a_failing_integrity_check(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = _corpus_file(tmp_path / "corpus.jsonl", [doc(), doc(url="https://www.govern.ad/dup")])
    assert main([str(corpus)]) == 1
    assert "integrity check failed" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_require_target_gates_on_volume(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = _corpus_file(tmp_path / "corpus.jsonl", [doc()])
    assert main([str(corpus)]) == 0  # reporting alone never fails on volume
    assert main([str(corpus), "--require-target"]) == 1
    assert "below the" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_rejects_invalid_input(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "corpus.jsonl"
    path.write_text(f"{doc().model_dump_json()}\n{{bad}}\n", encoding="utf-8")
    assert main([str(path)]) == 1
    assert "failed §3.1 validation" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_missing_input(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "absent.jsonl")]) == 1
    assert "no such file" in capsys.readouterr().err
