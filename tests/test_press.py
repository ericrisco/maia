"""Tests for the press subcorpus (PLAN M1.14)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from maia.schemas import License, Registre, Source
from maia.scraping.http import PoliteFetcher, RobotsPolicy
from maia.scraping.press import (
    DEFAULT_MIN_CHARS,
    PRESS_LICENSE,
    PRESS_OUTLETS,
    is_teaser,
    outlet_for,
    press_spec,
    scrape_press,
)

STAMP = datetime(2026, 8, 1, tzinfo=UTC)

ARTICLE_BODY = (
    "El Comú d'Encamp ha aprovat el pressupost per a l'exercici vinent amb el suport de la "
    "majoria i l'abstenció de la minoria. La partida més gran es destina a la reforma del "
    "aparcament comunal i a la millora dels accessos al centre del poble, una demanda que els "
    "veïns havien plantejat repetidament durant els darrers anys. La cònsol major ha explicat "
    "que les obres començaran després de l'estiu i que s'allargaran aproximadament un any, "
    "amb una afectació limitada al trànsit del carrer principal. Els consellers de la minoria "
    "han criticat que el calendari no s'hagi consensuat prèviament i han demanat una comissió "
    "de seguiment que informi trimestralment de l'execució de les obres i del cost final. "
    "El pressupost inclou també una aportació al servei de transport públic i una partida per "
    "a activitats culturals i esportives durant tot l'any que ve."
)

URL = "https://www.diariandorra.ad/noticies/encamp-pressupost"


def article_html(body: str) -> str:
    paragraphs = "".join(f"<p>{chunk}</p>" for chunk in body.split(". ") if chunk)
    return f"<html><body><article><h1>Titular</h1>{paragraphs}</article></body></html>"


def fetcher_for(html: str, robots: RobotsPolicy | None = None) -> PoliteFetcher:
    return PoliteFetcher(lambda _url: html, robots, min_interval=0.0)


# ─────────────────────────────────────────────────────────────
# The outlet registry
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.diariandorra.ad/noticies/1", "Diari d'Andorra"),
        ("https://diariandorra.ad/noticies/1", "Diari d'Andorra"),
        ("https://www.bondia.ad/nacional/2", "Bondia"),
        ("https://www.elperiodic.ad/noticia/3", "El Periòdic d'Andorra"),
        ("https://www.altaveu.com/noticia/4", "Altaveu"),
    ],
)
def test_the_outlet_is_recovered_from_the_url(url: str, expected: str) -> None:
    assert outlet_for(url).name == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "url",
    [
        "https://www.example.com/noticies/1",
        "https://www.govern.ad/noticies/1",
        "https://diariandorra.ad.evil.test/noticies/1",  # look-alike host
    ],
)
def test_an_unregistered_host_is_refused(url: str) -> None:
    # A typo in a host must not produce documents tagged `premsa` from somewhere that is not.
    with pytest.raises(ValueError, match="not a registered Andorran press outlet"):
        outlet_for(url)


@pytest.mark.unit
def test_the_registry_covers_the_outlets_the_plan_names() -> None:
    names = {outlet.name for outlet in PRESS_OUTLETS}
    assert {"Diari d'Andorra", "Bondia", "El Periòdic d'Andorra"} <= names


# ─────────────────────────────────────────────────────────────
# Paywall and teaser detection
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_full_article_is_not_a_teaser() -> None:
    assert not is_teaser(ARTICLE_BODY)


@pytest.mark.unit
@pytest.mark.parametrize(
    "pitch",
    [
        "Per continuar llegint, fes-te subscriptor.",
        "Aquest contingut és exclusiu per a subscriptors.",
        "Subscriu-te per accedir a tots els continguts.",
        "Para seguir leyendo, hazte suscriptor.",
        "Inicia sessió per llegir l'article complet.",
    ],
)
def test_a_subscription_pitch_is_conclusive(pitch: str) -> None:
    # No article body asks the reader to subscribe — length alone would miss a long wall.
    assert is_teaser(f"{ARTICLE_BODY} {pitch}")


@pytest.mark.unit
@pytest.mark.parametrize("suffix", ["…", "...", "[…]"])
def test_a_truncated_body_is_a_teaser(suffix: str) -> None:
    assert is_teaser(f"{ARTICLE_BODY}{suffix}")


@pytest.mark.unit
def test_a_short_stub_is_a_teaser() -> None:
    # The backstop for a wall that says nothing recognisable.
    stub = "El Comú d'Encamp ha aprovat el pressupost per a l'exercici vinent."
    assert len(stub) < DEFAULT_MIN_CHARS
    assert is_teaser(stub)


@pytest.mark.unit
def test_the_length_backstop_is_adjustable() -> None:
    stub = "El Comú d'Encamp ha aprovat el pressupost per a l'exercici vinent."
    assert is_teaser(stub)
    assert not is_teaser(stub, min_chars=10)


@pytest.mark.unit
def test_teaser_detection_ignores_surrounding_whitespace() -> None:
    assert is_teaser(f"  {ARTICLE_BODY}…  \n")


# ─────────────────────────────────────────────────────────────
# The §3.1 metadata
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_press_documents_are_never_publishable() -> None:
    """Press text is copyright, so the licence is a constant with no override."""
    assert PRESS_LICENSE is License.NO_REDISTRIBUTE
    assert not press_spec().license.is_public()


@pytest.mark.unit
def test_the_spec_tags_source_and_register() -> None:
    spec = press_spec()
    assert spec.source is Source.PREMSA
    assert spec.registre is Registre.ESTANDARD
    assert spec.min_chars == DEFAULT_MIN_CHARS


# ─────────────────────────────────────────────────────────────
# Scraping
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_article_becomes_a_document() -> None:
    documents = list(scrape_press(fetcher_for(article_html(ARTICLE_BODY)), [URL], fetched_at=STAMP))
    assert len(documents) == 1
    doc = documents[0]
    assert doc.source is Source.PREMSA
    assert doc.license is License.NO_REDISTRIBUTE
    assert doc.registre is Registre.ESTANDARD
    assert doc.lang == "ca"
    assert doc.fetched_at == STAMP
    assert str(doc.url) == URL
    assert doc.topic == ["Diari d'Andorra"]
    assert "pressupost" in doc.text


@pytest.mark.unit
def test_extra_topics_come_after_the_outlet() -> None:
    documents = list(
        scrape_press(
            fetcher_for(article_html(ARTICLE_BODY)),
            [URL],
            fetched_at=STAMP,
            topic=["comuns", "pressupostos"],
        )
    )
    assert documents[0].topic == ["Diari d'Andorra", "comuns", "pressupostos"]


@pytest.mark.unit
def test_a_paywalled_article_is_dropped() -> None:
    """The failure mode that makes a press scrape look successful while collecting nothing.

    Every other filter in the pipeline sees ordinary Catalan prose here: the boilerplate score
    is low, the language is Catalan, and the page returned HTTP 200.
    """
    walled = article_html(f"{ARTICLE_BODY} Per continuar llegint, fes-te subscriptor.")
    assert list(scrape_press(fetcher_for(walled), [URL], fetched_at=STAMP)) == []


@pytest.mark.unit
def test_a_truncated_preview_is_dropped() -> None:
    preview = article_html(ARTICLE_BODY[:400] + "…")
    assert list(scrape_press(fetcher_for(preview), [URL], fetched_at=STAMP)) == []


@pytest.mark.unit
def test_a_short_page_is_dropped() -> None:
    assert list(scrape_press(fetcher_for(article_html("Massa curt.")), [URL])) == []


@pytest.mark.unit
def test_robots_txt_is_respected() -> None:
    # For press this matters more than anywhere else: an outlet that disallows crawling is
    # simply not collected, and the honest route is to ask rather than work around it.
    robots = RobotsPolicy.from_text("User-agent: *\nDisallow: /\n")
    fetcher = fetcher_for(article_html(ARTICLE_BODY), robots)
    assert list(scrape_press(fetcher, [URL], fetched_at=STAMP)) == []
    assert fetcher.disallowed == [URL]


@pytest.mark.unit
def test_an_unreachable_page_is_skipped() -> None:
    fetcher = PoliteFetcher(lambda _url: None, min_interval=0.0)
    assert list(scrape_press(fetcher, [URL], fetched_at=STAMP)) == []


@pytest.mark.unit
def test_an_unregistered_host_is_refused_before_any_request() -> None:
    calls: list[str] = []

    def fetch_fn(url: str) -> str | None:
        calls.append(url)
        return article_html(ARTICLE_BODY)

    fetcher = PoliteFetcher(fetch_fn, min_interval=0.0)
    with pytest.raises(ValueError, match="not a registered Andorran press outlet"):
        list(scrape_press(fetcher, ["https://www.example.com/x"], fetched_at=STAMP))
    assert calls == []


@pytest.mark.unit
def test_several_outlets_in_one_run_are_each_tagged() -> None:
    urls = [
        "https://www.diariandorra.ad/noticies/1",
        "https://www.bondia.ad/nacional/2",
    ]
    documents = list(scrape_press(fetcher_for(article_html(ARTICLE_BODY)), urls, fetched_at=STAMP))
    # Same body from two outlets: both are collected here, and consolidation (M1.08) is what
    # collapses the duplicate — keeping that concern in one place.
    assert [doc.topic[0] for doc in documents] == ["Diari d'Andorra", "Bondia"]


@pytest.mark.unit
def test_min_chars_is_applied_to_both_filters() -> None:
    body = "El Comú ha aprovat el pressupost per a l'exercici vinent amb el suport de tots."
    assert list(scrape_press(fetcher_for(article_html(body)), [URL])) == []
    documents = list(scrape_press(fetcher_for(article_html(body)), [URL], min_chars=50))
    assert len(documents) == 1


@pytest.mark.unit
def test_no_urls_yields_nothing() -> None:
    assert list(scrape_press(fetcher_for(article_html(ARTICLE_BODY)), [])) == []
