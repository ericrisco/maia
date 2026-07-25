"""Golden + unit tests for juridical ingestion and chunk-by-article (PLAN M1.06)."""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from maia.schemas import License, Rang, Registre, Source
from maia.scraping.http import PoliteFetcher, RobotsPolicy
from maia.scraping.juridic import (
    LawSpec,
    citation_line,
    fetch_law,
    license_for,
    parse_law,
    split_law,
)

FIXTURES = Path(__file__).parent / "fixtures"
CONSTITUCIO = (FIXTURES / "constitucio_sample.txt").read_text(encoding="utf-8")
CODI_PENAL = (FIXTURES / "llei_qualificada_sample.txt").read_text(encoding="utf-8")

STAMP = datetime(2026, 8, 1, tzinfo=UTC)

CONSTITUCIO_SPEC = LawSpec(
    citation="Constitució del Principat d'Andorra",
    rang=Rang.CONSTITUCIO,
    consolidacio_data=date(1993, 5, 4),
    url="https://www.portaljuridicandorra.ad/constitucio",
)
CODI_PENAL_SPEC = LawSpec(
    citation="Llei 9/2005, del 21 de febrer, qualificada del Codi penal",
    rang=Rang.QUALIFICADA,
    consolidacio_data=date(2024, 4, 1),
    url="https://www.portaljuridicandorra.ad/codi-penal",
    llei="Llei 9/2005",
)


# ─────────────────────────────────────────────────────────────
# split_law — the chunk-by-article parser
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_constitucio_splits_into_articles_and_disposicions() -> None:
    split = split_law(CONSTITUCIO)
    assert [chunk.label for chunk in split.articles] == [
        "Article 1",
        "Article 2",
        "Article 5",
        "Article 9",
        "Disposició transitòria primera",
        "Disposició transitòria segona",
        "Disposició final",
    ]


@pytest.mark.unit
def test_preamble_is_returned_not_discarded() -> None:
    split = split_law(CONSTITUCIO)
    assert "Preàmbul" in split.preamble
    assert "El poble andorrà" in split.preamble
    # …and it is not smuggled into the first article.
    assert "El poble andorrà" not in split.articles[0].body


@pytest.mark.unit
def test_structural_hierarchy_is_carried_on_each_article() -> None:
    by_label = {chunk.label: chunk for chunk in split_law(CONSTITUCIO).articles}
    assert by_label["Article 1"].structure == ("Títol I",)
    assert by_label["Article 5"].structure == ("Títol II", "Capítol III")
    # A Títol resets the deeper levels it encloses.
    assert by_label["Article 2"].structure == ("Títol I",)


@pytest.mark.unit
def test_disposicions_carry_no_structure() -> None:
    # They close the norm, outside the articulated body. Inheriting the last article's
    # "Títol II, Capítol III" would fabricate a citation no lawyer would recognize.
    for fixture in (CONSTITUCIO, CODI_PENAL):
        disposicions = [c for c in split_law(fixture).articles if c.label.startswith("Disposici")]
        assert disposicions
        assert all(chunk.structure == () for chunk in disposicions)


@pytest.mark.unit
def test_disposicio_citation_line_has_no_structural_path() -> None:
    docs = parse_law(CONSTITUCIO, CONSTITUCIO_SPEC, fetched_at=STAMP)
    final = next(d for d in docs if d.legal is not None and d.legal.article == "Disposició final")
    assert final.text.splitlines()[0] == ("Constitució del Principat d'Andorra — Disposició final")


@pytest.mark.unit
def test_article_body_stops_at_the_next_heading() -> None:
    by_label = {chunk.label: chunk for chunk in split_law(CONSTITUCIO).articles}
    article_2 = by_label["Article 2"]
    assert "El català és la llengua oficial de l'Estat." in article_2.body
    assert "Títol II" not in article_2.body
    assert "Declaració Universal" not in article_2.body


@pytest.mark.unit
def test_rubric_is_lifted_off_the_heading_line() -> None:
    by_label = {chunk.label: chunk for chunk in split_law(CONSTITUCIO).articles}
    article_9 = by_label["Article 9"]
    assert article_9.rubric == "Dret a la llibertat"
    assert not article_9.body.startswith("Dret a la llibertat")
    assert article_9.body.startswith("1. Totes les persones")
    # An article with no rubric keeps its whole text as body.
    assert by_label["Article 5"].rubric is None
    assert by_label["Article 5"].body.startswith("La Declaració Universal")


@pytest.mark.unit
def test_wrapped_body_on_the_heading_line_is_not_mistaken_for_a_rubric() -> None:
    # "Article 4. Les penes s'imposen amb la finalitat de la reinserció social de la persona
    #  condemnada, …" — the body starts on the heading line and wraps.
    by_label = {chunk.label: chunk for chunk in split_law(CODI_PENAL).articles}
    article_4 = by_label["Article 4"]
    assert article_4.rubric is None
    assert article_4.body.startswith("Les penes s'imposen")
    assert "reinserció social de la persona condemnada" in article_4.body


@pytest.mark.unit
def test_hard_wrapped_sentences_are_rejoined() -> None:
    by_label = {chunk.label: chunk for chunk in split_law(CONSTITUCIO).articles}
    assert "La seva denominació oficial és Principat d'Andorra." in by_label["Article 1"].body
    # …including when the continuation line happens to start with a proper noun.
    assert "al Butlletí Oficial del Principat d'Andorra." in by_label["Disposició final"].body


@pytest.mark.unit
def test_enumerated_items_keep_their_line_breaks() -> None:
    text = (
        "Article 1\n"
        "Són infraccions greus:\n"
        "a) La primera conducta\n"
        "b) La segona conducta\n"
        "c) La tercera conducta\n"
    )
    body = split_law(text).articles[0].body
    assert body.splitlines() == [
        "Són infraccions greus:",
        "a) La primera conducta",
        "b) La segona conducta",
        "c) La tercera conducta",
    ]


@pytest.mark.unit
def test_numbered_paragraphs_stay_separate() -> None:
    by_label = {chunk.label: chunk for chunk in split_law(CONSTITUCIO).articles}
    lines = by_label["Article 2"].body.splitlines()
    assert lines == [
        "1. El català és la llengua oficial de l'Estat.",
        "2. Andorra la Vella és la capital de l'Estat.",
    ]


@pytest.mark.unit
def test_bis_and_ter_articles_are_recognized() -> None:
    split = split_law(CODI_PENAL)
    by_label = {chunk.label: chunk for chunk in split.articles}
    assert "Article 2 bis" in by_label
    assert "Article 3 ter" in by_label
    assert by_label["Article 2 bis"].designator == "2 bis"
    assert by_label["Article 2 bis"].rubric == "Aplicació temporal"


@pytest.mark.unit
def test_llibre_titol_and_seccio_all_track_as_structure() -> None:
    by_label = {chunk.label: chunk for chunk in split_law(CODI_PENAL).articles}
    assert by_label["Article 1"].structure == ("Llibre I", "Títol I")
    assert by_label["Article 4"].structure == ("Llibre I", "Títol I", "Secció segona")


@pytest.mark.unit
def test_both_disposicio_spellings_are_handled() -> None:
    labels = [chunk.label for chunk in split_law(CODI_PENAL).articles]
    # Singular with an ordinal, singular with "única", and the plural-group + ordinal form.
    assert "Disposició addicional primera" in labels
    assert "Disposició derogatòria única" in labels
    assert "Disposició final primera" in labels
    assert "Disposició final segona" in labels
    # The plural group heading itself is not emitted as a chunk.
    assert "Disposicions finals" not in labels


@pytest.mark.unit
def test_ordinal_sub_items_get_the_group_body_not_a_rubric() -> None:
    by_label = {chunk.label: chunk for chunk in split_law(CODI_PENAL).articles}
    segona = by_label["Disposició final segona"]
    assert segona.rubric is None
    assert segona.body.startswith("Aquesta Llei entra en vigor")


@pytest.mark.unit
def test_plural_group_without_sub_items_degrades_to_a_unit() -> None:
    text = (
        "Llei de prova\n\n"
        "Article 1\nUna norma qualsevol.\n\n"
        "Disposicions finals\n"
        "Aquesta Llei entra en vigor l'endemà de la seva publicació.\n"
    )
    labels = [chunk.label for chunk in split_law(text).articles]
    assert labels == ["Article 1", "Disposicions finals"]
    body = split_law(text).articles[1].body
    assert body.startswith("Aquesta Llei entra en vigor")


@pytest.mark.unit
def test_stray_ordinal_line_outside_a_group_is_not_a_heading() -> None:
    text = "Article 1\nLa primera part diu això.\nSegona\nI això continua l'article.\n"
    split = split_law(text)
    assert [chunk.label for chunk in split.articles] == ["Article 1"]
    assert "Segona" in split.articles[0].body


@pytest.mark.unit
def test_lowercase_cross_reference_is_not_a_new_article() -> None:
    text = (
        "Article 1\n"
        "El que estableix l'article 5 d'aquesta Llei s'aplica igualment.\n"
        "article 7 no encapçala res.\n"
    )
    assert [chunk.label for chunk in split_law(text).articles] == ["Article 1"]


@pytest.mark.unit
def test_body_on_the_heading_line_ending_in_a_full_stop_is_body() -> None:
    split = split_law("Article 1. Aquesta és tota la norma.\n")
    assert split.articles[0].rubric is None
    assert split.articles[0].body == "Aquesta és tota la norma."


@pytest.mark.unit
def test_heading_on_the_very_last_line_without_a_newline() -> None:
    split = split_law("Article 1. Rúbrica sense cos")
    assert [chunk.label for chunk in split.articles] == ["Article 1"]
    assert split.articles[0].rubric == "Rúbrica sense cos"
    assert split.articles[0].body == ""
    # An empty article is not a document.
    assert parse_law("Article 1. Rúbrica sense cos", CODI_PENAL_SPEC, fetched_at=STAMP) == []


@pytest.mark.unit
def test_group_without_sub_items_degrades_even_when_more_headings_follow() -> None:
    text = (
        "Article 1\nUna norma qualsevol.\n\n"
        "Disposicions transitòries\n"
        "Les normes anteriors es mantenen mentre no es dictin les noves.\n\n"
        "Disposicions finals\n\n"
        "Primera. Aquesta Llei entra en vigor l'endemà.\n"
    )
    chunks = split_law(text).articles
    assert [chunk.label for chunk in chunks] == [
        "Article 1",
        "Disposicions transitòries",
        "Disposició final primera",
    ]
    assert chunks[1].body == "Les normes anteriors es mantenen mentre no es dictin les noves."


@pytest.mark.unit
def test_text_without_any_article_yields_only_a_preamble() -> None:
    split = split_law("Un document que no és una norma articulada.")
    assert split.articles == ()
    assert split.preamble == "Un document que no és una norma articulada."


@pytest.mark.unit
def test_empty_text_is_handled() -> None:
    split = split_law("")
    assert split.articles == ()
    assert split.preamble == ""


# ─────────────────────────────────────────────────────────────
# license_for — the official-sources-only compliance gate
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.portaljuridicandorra.ad/eli/llei/2005/9", License.PUBLIC_OFFICIAL),
        ("https://www.consellgeneral.ad/ca/arxiu/lleis/2005", License.PUBLIC_OFFICIAL),
        ("https://portaljuridicandorra.ad/x", License.PUBLIC_OFFICIAL),
        ("https://www.bopa.ad/documents/2005/GD20050309", License.NO_REDISTRIBUTE),
    ],
)
def test_license_is_derived_per_official_route(url: str, expected: License) -> None:
    assert license_for(url) is expected


@pytest.mark.unit
def test_bopa_text_is_never_publishable() -> None:
    # BOPA disposals may be cited within a publication but not republished as a collection.
    assert not license_for("https://www.bopa.ad/x").is_public()


@pytest.mark.unit
@pytest.mark.parametrize(
    "url",
    [
        "https://www.leslleis.com/lleis/codi-penal",  # private compilation — banned outright
        "https://example.com/codi-penal",
        "https://portaljuridicandorra.ad.evil.test/x",  # look-alike host
    ],
)
def test_unofficial_sources_are_refused(url: str) -> None:
    with pytest.raises(ValueError, match="not an official Andorran legal source"):
        license_for(url)


# ─────────────────────────────────────────────────────────────
# parse_law — §3.1 documents with legal metadata
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_parse_law_emits_one_document_per_article_with_legal_metadata() -> None:
    docs = parse_law(CODI_PENAL, CODI_PENAL_SPEC, fetched_at=STAMP)
    assert len(docs) == len(split_law(CODI_PENAL).articles)
    doc = next(d for d in docs if d.legal is not None and d.legal.article == "2 bis")
    assert doc.source is Source.JURIDIC
    assert doc.registre is Registre.ESTANDARD
    assert doc.license is License.PUBLIC_OFFICIAL
    assert doc.lang == "ca"
    assert doc.fetched_at == STAMP
    assert str(doc.url) == CODI_PENAL_SPEC.url
    assert doc.legal is not None
    assert doc.legal.rang is Rang.QUALIFICADA
    assert doc.legal.llei == "Llei 9/2005"
    assert doc.legal.consolidacio_data == date(2024, 4, 1)


@pytest.mark.unit
def test_constitution_has_no_llei_number() -> None:
    docs = parse_law(CONSTITUCIO, CONSTITUCIO_SPEC, fetched_at=STAMP)
    assert docs
    for doc in docs:
        assert doc.legal is not None
        assert doc.legal.rang is Rang.CONSTITUCIO
        assert doc.legal.llei is None


@pytest.mark.unit
def test_every_chunk_opens_with_its_own_citation() -> None:
    docs = parse_law(CONSTITUCIO, CONSTITUCIO_SPEC, fetched_at=STAMP)
    article_5 = next(d for d in docs if d.legal is not None and d.legal.article == "5")
    assert article_5.text.splitlines()[0] == (
        "Constitució del Principat d'Andorra — Títol II, Capítol III — Article 5"
    )
    assert "La Declaració Universal dels Drets Humans" in article_5.text


@pytest.mark.unit
def test_citation_line_includes_the_rubric_when_there_is_one() -> None:
    split = split_law(CODI_PENAL)
    chunk = next(c for c in split.articles if c.label == "Article 1")
    assert citation_line(CODI_PENAL_SPEC, chunk) == (
        "Llei 9/2005, del 21 de febrer, qualificada del Codi penal — Llibre I, Títol I — "
        "Article 1. Principi de legalitat"
    )


@pytest.mark.unit
def test_identical_boilerplate_in_two_laws_gets_distinct_ids() -> None:
    """The regression the citation line exists to prevent.

    The closing provision is verbatim identical across dozens of Andorran laws. Since the
    §3.1 id is the sha256 of the text, without a per-law citation line the consolidation
    pass would collapse them into one document citing only one law.
    """
    boilerplate = (
        "Article 1\nUna disposició qualsevol.\n\n"
        "Disposició final\n"
        "Aquesta Llei entra en vigor l'endemà de la seva publicació al Butlletí Oficial "
        "del Principat d'Andorra.\n"
    )
    other = LawSpec(
        citation="Llei 11/2012, del 21 de juny, de l'impost general indirecte",
        rang=Rang.ORDINARIA,
        consolidacio_data=date(2023, 1, 1),
        url="https://www.portaljuridicandorra.ad/igi",
        llei="Llei 11/2012",
    )
    ids_a = {d.id for d in parse_law(boilerplate, CODI_PENAL_SPEC, fetched_at=STAMP)}
    ids_b = {d.id for d in parse_law(boilerplate, other, fetched_at=STAMP)}
    assert len(ids_a) == 2
    assert ids_a.isdisjoint(ids_b)


@pytest.mark.unit
def test_short_articles_are_kept() -> None:
    # Constitution art. 2 is two one-line paragraphs; a length filter would delete an
    # article the corpus must be able to cite.
    docs = parse_law(CONSTITUCIO, CONSTITUCIO_SPEC, fetched_at=STAMP)
    articles = {doc.legal.article for doc in docs if doc.legal is not None}
    assert {"1", "2", "5", "9"} <= articles


@pytest.mark.unit
def test_min_chars_can_still_be_raised_explicitly() -> None:
    docs = parse_law(CONSTITUCIO, CONSTITUCIO_SPEC, fetched_at=STAMP, min_chars=200)
    articles = {doc.legal.article for doc in docs if doc.legal is not None}
    assert "2" not in articles  # short article dropped only because the caller asked


@pytest.mark.unit
def test_duplicate_designators_fail_loudly() -> None:
    text = "Article 1\nPrimera versió.\n\nArticle 1\nSegona versió.\n"
    with pytest.raises(ValueError, match="duplicate legal designators"):
        parse_law(text, CODI_PENAL_SPEC, fetched_at=STAMP)


@pytest.mark.unit
def test_topic_is_propagated() -> None:
    docs = parse_law(CONSTITUCIO, CONSTITUCIO_SPEC, fetched_at=STAMP, topic=["dret", "estat"])
    assert all(doc.topic == ["dret", "estat"] for doc in docs)


@pytest.mark.unit
def test_parse_law_refuses_an_unofficial_url_before_producing_anything() -> None:
    spec = LawSpec(
        citation="Còpia privada del Codi penal",
        rang=Rang.QUALIFICADA,
        consolidacio_data=date(2024, 4, 1),
        url="https://www.leslleis.com/codi-penal",
    )
    with pytest.raises(ValueError, match="not an official Andorran legal source"):
        parse_law(CODI_PENAL, spec, fetched_at=STAMP)


@pytest.mark.unit
def test_a_licence_override_may_tighten() -> None:
    # A publishable route can be narrowed — e.g. a norm whose own terms turn out to restrict it.
    spec = LawSpec(
        citation="Llei 9/2005",
        rang=Rang.QUALIFICADA,
        consolidacio_data=date(2024, 4, 1),
        url="https://www.portaljuridicandorra.ad/codi-penal",
        license=License.NO_REDISTRIBUTE,
    )
    docs = parse_law(CODI_PENAL, spec, fetched_at=STAMP)
    assert docs
    assert all(doc.license is License.NO_REDISTRIBUTE for doc in docs)


@pytest.mark.unit
def test_a_licence_override_may_never_widen_a_restricted_route() -> None:
    """The hole an adversarial review found: the override skipped the host gate entirely.

    It made BOPA re-taggable as publishable — which then passes M1.09's public-upload wall —
    and made ``leslleis.com`` ingestible with one keyword argument, defeating the one control
    D-0009 says is "enforced in code rather than by convention".
    """
    widened = LawSpec(
        citation="Constitució del Principat d'Andorra",
        rang=Rang.CONSTITUCIO,
        consolidacio_data=date(1993, 5, 4),
        url="https://www.bopa.ad/constitucio",
        license=License.PUBLIC_OFFICIAL,
    )
    with pytest.raises(ValueError, match="may only tighten, never widen"):
        widened.resolved_license()
    with pytest.raises(ValueError, match="may only tighten, never widen"):
        parse_law(CONSTITUCIO, widened, fetched_at=STAMP)


@pytest.mark.unit
def test_an_override_cannot_smuggle_in_an_unofficial_host() -> None:
    private = LawSpec(
        citation="Còpia privada del Codi penal",
        rang=Rang.QUALIFICADA,
        consolidacio_data=date(2024, 4, 1),
        url="https://www.leslleis.com/codi-penal",
        license=License.PUBLIC_OFFICIAL,
    )
    # The host is checked even when a licence is supplied.
    with pytest.raises(ValueError, match="not an official Andorran legal source"):
        private.resolved_license()
    with pytest.raises(ValueError, match="not an official Andorran legal source"):
        parse_law(CODI_PENAL, private, fetched_at=STAMP)


# ─────────────────────────────────────────────────────────────
# fetch_law — the live seam (network is blocked-by-resource)
# ─────────────────────────────────────────────────────────────


def _html(body: str) -> str:
    return f"<html><body><article>{body}</article></body></html>"


@pytest.mark.unit
def test_fetch_law_chunks_a_fetched_page() -> None:
    paragraphs = "".join(f"<p>{line}</p>" for line in CONSTITUCIO.splitlines() if line.strip())
    fetcher = PoliteFetcher(lambda _url: _html(paragraphs), min_interval=0.0)
    docs = fetch_law(fetcher, CONSTITUCIO_SPEC, fetched_at=STAMP)
    articles = {doc.legal.article for doc in docs if doc.legal is not None}
    assert {"1", "2", "5", "9"} <= articles
    assert all(doc.source is Source.JURIDIC for doc in docs)


@pytest.mark.unit
def test_fetch_law_returns_nothing_when_the_page_is_unreachable() -> None:
    fetcher = PoliteFetcher(lambda _url: None, min_interval=0.0)
    assert fetch_law(fetcher, CONSTITUCIO_SPEC, fetched_at=STAMP) == []


@pytest.mark.unit
def test_fetch_law_returns_nothing_when_extraction_finds_no_content() -> None:
    fetcher = PoliteFetcher(lambda _url: "<html><body></body></html>", min_interval=0.0)
    assert fetch_law(fetcher, CONSTITUCIO_SPEC, fetched_at=STAMP) == []


@pytest.mark.unit
def test_fetch_law_respects_robots_txt() -> None:
    robots = RobotsPolicy.from_text("User-agent: *\nDisallow: /\n")
    fetcher = PoliteFetcher(lambda _url: _html("<p>Article 1</p>"), robots, min_interval=0.0)
    assert fetch_law(fetcher, CONSTITUCIO_SPEC, fetched_at=STAMP) == []
    assert fetcher.disallowed == [CONSTITUCIO_SPEC.url]


@pytest.mark.unit
def test_fetch_law_never_requests_an_unofficial_host() -> None:
    calls: list[str] = []

    def fetch_fn(url: str) -> str | None:
        calls.append(url)
        return _html("<p>Article 1</p>")

    spec = LawSpec(
        citation="Còpia privada",
        rang=Rang.ORDINARIA,
        consolidacio_data=date(2024, 1, 1),
        url="https://www.leslleis.com/x",
    )
    with pytest.raises(ValueError, match="not an official Andorran legal source"):
        fetch_law(PoliteFetcher(fetch_fn, min_interval=0.0), spec)
    assert calls == []


@pytest.mark.unit
def test_a_wrapped_cross_reference_does_not_become_an_article() -> None:
    """The regression an adversarial review found.

    Headings were matched on the *raw* text. A hard wrap that happens to break before a
    cross-reference reads exactly like a heading: it fabricated an ``Article 7`` citing the
    wrong law, and truncated the real article's body at the wrap.
    """
    wrapped = (
        "Article 5. Sancions\n"
        "Les sancions previstes s'imposen d'acord amb el que estableix l'\n"
        "Article 7 de la Llei de bases de l'ordenament tributari, i són acumulables.\n"
        "\n"
        "Article 6\n"
        "Una altra disposició prou llarga per ser un cos real.\n"
    )
    chunks = split_law(wrapped).articles
    assert [chunk.label for chunk in chunks] == ["Article 5", "Article 6"]
    # The rubric survives — unwrapping must not let a heading swallow its own body.
    assert chunks[0].rubric == "Sancions"
    # …and the cross-reference stays inside article 5, where it belongs.
    assert "Article 7 de la Llei de bases" in chunks[0].body
    assert chunks[0].body.endswith("són acumulables.")


@pytest.mark.unit
def test_a_padded_article_number_is_the_same_article() -> None:
    # "Article 01" and "Article 1" must collide, or the duplicate guard misses them and two
    # documents cite the same article.
    with pytest.raises(ValueError, match="duplicate legal designators"):
        parse_law(
            "Article 01\nPrimera versió.\n\nArticle 1\nSegona versió.\n",
            CODI_PENAL_SPEC,
            fetched_at=STAMP,
        )
