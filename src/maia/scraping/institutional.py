"""Institutional website scrapers — PLAN M1.03.

Turns a list of URLs from an Andorran institutional site (govern.ad, cultura.ad, the
comuns, visitandorra.com…) into §3.1 corpus documents: fetch politely, extract the main
text, tag with the source's fixed metadata, drop too-short pages.

One :class:`SiteSpec` per source fixes its schema metadata; the fetch and extraction seams
are injected, so the whole pipeline is tested offline against fixture HTML.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime

from maia.schemas import CorpusDocument, License, Registre, Source, normalize_text
from maia.scraping.extract import extract_main_text
from maia.scraping.http import PoliteFetcher

Extractor = Callable[[str, str | None], str | None]


@dataclass(frozen=True)
class SiteSpec:
    """Fixed §3.1 metadata for one institutional source."""

    source: Source
    license: License
    registre: Registre = Registre.ESTANDARD
    min_chars: int = 200


#: Prewired specs for the P0/P1 institutional sources (all public institutional).
SITE_SPECS: dict[str, SiteSpec] = {
    "govern": SiteSpec(Source.GOVERN, License.PUBLIC_OFFICIAL),
    "cultura": SiteSpec(Source.CULTURA, License.PUBLIC_OFFICIAL),
    "comuns": SiteSpec(Source.COMUNS, License.PUBLIC_OFFICIAL),
    "visitandorra": SiteSpec(Source.VISITANDORRA, License.PUBLIC_OFFICIAL),
}


def scrape_site(
    fetcher: PoliteFetcher,
    urls: Iterable[str],
    spec: SiteSpec,
    *,
    fetched_at: datetime | None = None,
    extractor: Extractor = extract_main_text,
    topic: Iterable[str] | None = None,
) -> Iterator[CorpusDocument]:
    """Yield §3.1 documents for the fetchable, non-trivial pages among ``urls``.

    Pages disallowed by robots.txt, unreachable, empty, or shorter than
    ``spec.min_chars`` after extraction are skipped.
    """
    stamp = fetched_at or datetime.now(UTC)
    topics = list(topic) if topic is not None else []
    for url in urls:
        html = fetcher.fetch(url)
        if html is None:
            continue
        text = extractor(html, url)
        if text is None or len(normalize_text(text)) < spec.min_chars:
            continue
        yield CorpusDocument(
            text=text,
            source=spec.source,
            url=url,  # type: ignore[arg-type]
            fetched_at=stamp,
            lang="ca",
            topic=topics,
            license=spec.license,
            registre=spec.registre,
        )
