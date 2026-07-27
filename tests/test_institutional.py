"""Tests for extraction + institutional scraping (PLAN M1.03), offline via fixtures."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from maia.schemas import License, Registre, Source
from maia.scraping.extract import extract_main_text
from maia.scraping.http import PoliteFetcher, RobotsPolicy
from maia.scraping.institutional import SITE_SPECS, scrape_site

STAMP = datetime(2026, 8, 1, tzinfo=UTC)

ARTICLE_HTML = """
<html><head><title>Institucions d'Andorra</title></head>
<body>
  <nav>Menú principal · Inici · Contacte</nav>
  <article>
    <h1>El Consell General</h1>
    <p>El Consell General és el parlament del Principat d'Andorra. Representa el poble
    andorrà i exerceix la potestat legislativa, aprova els pressupostos de l'Estat i
    controla l'acció política del Govern segons estableix la Constitució de 1993.</p>
    <p>Els consellers generals són elegits per sufragi universal per un mandat de quatre
    anys, en part per circumscripció parroquial i en part per circumscripció nacional.</p>
  </article>
  <footer>© Govern d'Andorra · Avís legal · Política de cookies</footer>
</body></html>
"""

BOILERPLATE_HTML = "<html><body><nav>Inici</nav><footer>© 2026</footer></body></html>"


class _MapFetcher:
    """A PoliteFetcher-shaped fake backed by a {url: html} map."""

    def __init__(self, pages: dict[str, str]) -> None:
        self._pages = pages

    def fetch(self, url: str) -> str | None:
        return self._pages.get(url)


@pytest.mark.unit
def test_extract_main_text_drops_boilerplate() -> None:
    text = extract_main_text(ARTICLE_HTML, "https://govern.ad/consell")
    assert text is not None
    assert "Consell General" in text
    assert "cookies" not in text  # footer dropped
    assert "Menú principal" not in text  # nav dropped


@pytest.mark.unit
def test_extract_empty_and_boilerplate_return_none_or_short() -> None:
    assert extract_main_text("", None) is None
    assert extract_main_text("   ", None) is None
    # A nav/footer-only page yields no meaningful body.
    result = extract_main_text(BOILERPLATE_HTML, None)
    assert result is None or len(result) < 50


@pytest.mark.unit
def test_extract_returns_none_when_body_is_whitespace(monkeypatch: pytest.MonkeyPatch) -> None:
    import trafilatura

    monkeypatch.setattr(trafilatura, "extract", lambda *a, **k: "   \n  ")
    assert extract_main_text("<html><body><p>x</p></body></html>", None) is None


@pytest.mark.unit
def test_extract_returns_none_when_trafilatura_finds_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import trafilatura

    monkeypatch.setattr(trafilatura, "extract", lambda *a, **k: None)
    assert extract_main_text("<html><body><p>x</p></body></html>", None) is None


@pytest.mark.unit
def test_scrape_site_builds_documents() -> None:
    fetcher = _MapFetcher({"https://govern.ad/consell": ARTICLE_HTML})
    docs = list(
        scrape_site(
            fetcher,  # type: ignore[arg-type]
            ["https://govern.ad/consell"],
            SITE_SPECS["govern"],
            fetched_at=STAMP,
            topic=["institucions"],
        )
    )
    assert len(docs) == 1
    doc = docs[0]
    assert doc.source is Source.GOVERN
    assert doc.license is License.PUBLIC_OFFICIAL
    assert doc.registre is Registre.ESTANDARD
    assert doc.topic == ["institucions"]
    assert doc.fetched_at == STAMP
    assert "Consell General" in doc.text


@pytest.mark.unit
def test_scrape_site_skips_unfetchable_and_short() -> None:
    fetcher = _MapFetcher(
        {
            "https://govern.ad/ok": ARTICLE_HTML,
            "https://govern.ad/boiler": BOILERPLATE_HTML,
            # "https://govern.ad/missing" absent → fetch returns None
        }
    )
    docs = list(
        scrape_site(
            fetcher,  # type: ignore[arg-type]
            [
                "https://govern.ad/ok",
                "https://govern.ad/boiler",
                "https://govern.ad/missing",
            ],
            SITE_SPECS["govern"],
            fetched_at=STAMP,
        )
    )
    assert [str(d.url) for d in docs] == ["https://govern.ad/ok"]


@pytest.mark.unit
def test_scrape_site_integrates_with_polite_fetcher_and_robots() -> None:
    net_pages = {"https://govern.ad/ok": ARTICLE_HTML, "https://govern.ad/private/x": ARTICLE_HTML}
    robots = RobotsPolicy.from_text("User-agent: *\nDisallow: /private/")
    fetcher = PoliteFetcher(lambda url: net_pages.get(url), robots, sleep=lambda _s: None)
    docs = list(
        scrape_site(
            fetcher,
            ["https://govern.ad/ok", "https://govern.ad/private/x"],
            SITE_SPECS["govern"],
            fetched_at=STAMP,
        )
    )
    assert [str(d.url) for d in docs] == ["https://govern.ad/ok"]
    assert fetcher.disallowed == ["https://govern.ad/private/x"]


@pytest.mark.unit
def test_every_p0_institutional_source_has_a_spec() -> None:
    """The parliament's own site was named P0 in the plan and had no spec until D-0043 — a source
    can only be scraped if it is in this catalogue, so an omission here is silent: the pipeline
    runs green over the sources it does know about and nobody notices the missing one."""
    assert {s.source for s in SITE_SPECS.values()} >= {
        Source.CONSELL_GENERAL,
        Source.GOVERN,
        Source.CULTURA,
        Source.COMUNS,
    }


@pytest.mark.unit
def test_consell_general_is_not_the_diari_de_sessions() -> None:
    """Institutional prose from the chamber's website, not transcribed speech: the Diari carries a
    D7 constraint (never clone an individual's voice) that must not silently extend to — or be
    lost from — either body of text."""
    spec = SITE_SPECS["consellgeneral"]
    assert spec.source is Source.CONSELL_GENERAL
    assert spec.source.value != Source.CONSELL_DIARI_SESSIONS.value
    assert spec.license is License.PUBLIC_OFFICIAL

    fetcher = _MapFetcher({"https://consellgeneral.ad/ca/el-consell": ARTICLE_HTML})
    docs = list(
        scrape_site(
            fetcher,  # type: ignore[arg-type]
            ["https://consellgeneral.ad/ca/el-consell"],
            spec,
            fetched_at=STAMP,
            topic=["institucions"],
        )
    )
    assert [d.source for d in docs] == [Source.CONSELL_GENERAL]
    assert docs[0].registre is Registre.ESTANDARD
