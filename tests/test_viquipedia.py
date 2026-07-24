"""Tests for the Viquipèdia dump parser (PLAN M1.02), driven by a fixture dump."""

from __future__ import annotations

import io
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import unquote

import pytest

from maia.schemas import CorpusDocument, License, Registre, Source
from maia.scraping.viquipedia import (
    extract_categories,
    is_relevant,
    iter_pages,
    parse_dump,
    wikitext_to_text,
)

FIXTURE = Path(__file__).parent / "fixtures" / "viquipedia_sample.xml"
STAMP = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)


def _slug(doc: CorpusDocument) -> str:
    """The article title (underscored) recovered from the document URL."""
    return unquote(str(doc.url).rsplit("/", 1)[-1])


@pytest.mark.unit
def test_iter_pages_reads_all_pages_with_metadata() -> None:
    pages = {p.title: p for p in iter_pages(FIXTURE)}
    assert set(pages) == {
        "Andorra",
        "Escaldes-Engordany",
        "Principat d'Andorra",
        "França",
        "Categoria:Andorra",
        "Casa de la Vall (esbós)",
    }
    assert pages["Categoria:Andorra"].ns == 14
    assert pages["Principat d'Andorra"].is_redirect
    assert not pages["Andorra"].is_redirect


@pytest.mark.unit
def test_extract_categories() -> None:
    page = {p.title: p for p in iter_pages(FIXTURE)}["Andorra"]
    assert extract_categories(page.wikitext) == ["Andorra", "Microestats d'Europa"]


@pytest.mark.unit
def test_extract_categories_deduplicates() -> None:
    assert extract_categories("[[Categoria:Andorra]] text [[Categoria:Andorra]]") == ["Andorra"]


@pytest.mark.unit
def test_wikitext_to_text_strips_markup() -> None:
    page = {p.title: p for p in iter_pages(FIXTURE)}["Andorra"]
    text = wikitext_to_text(page.wikitext)
    assert "[[" not in text and "'''" not in text
    assert "Categoria:" not in text
    assert "microestat" in text
    assert "Andorra" in text


@pytest.mark.unit
def test_is_relevant_keyword_fallback_excludes_france() -> None:
    pages = {p.title: p for p in iter_pages(FIXTURE)}
    andorra = pages["Andorra"]
    france = pages["França"]
    assert is_relevant(andorra, extract_categories(andorra.wikitext))
    assert not is_relevant(france, extract_categories(france.wikitext))


@pytest.mark.unit
def test_is_relevant_allowlist_mode() -> None:
    pages = {p.title: p for p in iter_pages(FIXTURE)}
    france = pages["França"]
    # With an allowlist, only category membership counts.
    assert is_relevant(france, ["Països d'Europa"], category_allowlist=["Països d'Europa"])
    assert not is_relevant(france, ["Països d'Europa"], category_allowlist=["Andorra"])


@pytest.mark.unit
def test_parse_dump_default_yields_relevant_long_articles() -> None:
    docs = list(parse_dump(FIXTURE, fetched_at=STAMP))
    titles = {_slug(d) for d in docs}
    # Andorra + Escaldes; redirect, ns14, irrelevant França, and the short stub excluded.
    assert titles == {"Andorra", "Escaldes-Engordany"}
    for doc in docs:
        assert doc.source is Source.VIQUIPEDIA
        assert doc.license is License.CC_BY_SA_3_0
        assert doc.registre is Registre.ESTANDARD
        assert doc.lang == "ca"
        assert doc.fetched_at == STAMP
        assert doc.id  # computed


@pytest.mark.unit
def test_parse_dump_topics_come_from_categories() -> None:
    docs = {_slug(d): d for d in parse_dump(FIXTURE, fetched_at=STAMP)}
    assert docs["Andorra"].topic == ["Andorra", "Microestats d'Europa"]


@pytest.mark.unit
def test_parse_dump_allowlist_and_min_chars() -> None:
    docs = list(
        parse_dump(
            FIXTURE,
            category_allowlist=["Andorra"],
            min_chars=10,
            fetched_at=STAMP,
        )
    )
    titles = {_slug(d) for d in docs}
    # Only pages carrying [[Categoria:Andorra]]: the Andorra article and the (now
    # long-enough) stub. Escaldes is under a different category → excluded.
    assert titles == {"Andorra", "Casa_de_la_Vall_(esbós)"}


@pytest.mark.unit
def test_parse_dump_min_chars_excludes_stub_by_default() -> None:
    docs = list(parse_dump(FIXTURE, category_allowlist=["Andorra"], fetched_at=STAMP))
    titles = {_slug(d) for d in docs}
    assert titles == {"Andorra"}  # stub < 200 chars excluded


@pytest.mark.unit
def test_iter_pages_handles_nonnumeric_ns() -> None:
    xml = (
        b"<mediawiki><page><title>X</title><ns>bad</ns>"
        b"<revision><text>hola</text></revision></page>"
        b"<page><title>Y</title></page></mediawiki>"  # no <ns>, no <text>
    )
    pages = list(iter_pages(io.BytesIO(xml)))
    assert len(pages) == 2
    assert pages[0].ns == 0  # non-numeric ns falls back to 0
    assert pages[1].ns == 0 and pages[1].wikitext == ""  # missing elements → defaults
