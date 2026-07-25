"""Press subcorpus — PLAN M1.14.

Andorran newspapers (Diari d'Andorra, Bondia, El Periòdic d'Andorra, Altaveu) are where the
country's *current* institutional and everyday lexicon actually lives — the names of ongoing
debates, the words used for local politics and services, phrasing no institutional page uses.

**Grounding-only, and the licence is not negotiable.** Press text is copyright; it is read to
ground the synthetic dataset and to populate the RAG index, and only paraphrased knowledge
ever reaches a public artifact. :data:`PRESS_LICENSE` is a module constant with no override,
for the same reason as RTVA (M1.13): there is no caller who should be able to ask otherwise.

The fetch, extract and tag pipeline is already M1.03's (:func:`~maia.scraping.institutional.
scrape_site`), so this module adds only what press specifically needs:

* **An outlet registry** keyed by host, so a document's outlet is recoverable from its URL —
  §3.1 has one ``premsa`` source value, and adding one per newspaper would bloat the contract
  for something the URL already tells us. The outlet goes into ``topic``.
* **Paywall and teaser detection.** A metered article returns HTTP 200 with two paragraphs and
  a subscription pitch. That is the failure mode that makes a press scrape look successful
  while collecting nothing: the boilerplate filter sees ordinary prose, the language filter
  sees Catalan, and a few hundred truncated stubs land in the corpus. :func:`is_teaser` looks
  for the pitch and for the truncation, and a higher default ``min_chars`` than institutional
  pages use provides the backstop.
* **A refusal to scrape an outlet that is not registered**, so a typo in a host cannot quietly
  produce documents tagged as press from somewhere that is not.

**robots.txt is respected without exception**, and for press it matters more than anywhere
else — an outlet that disallows crawling is simply not collected, and the honest route is to
ask rather than work around it. That requires wiring the fetcher with
:func:`~maia.scraping.http.polite_fetcher`, which retrieves each origin's robots.txt; a bare
``PoliteFetcher(requests_fetch)`` obeys an allow-all policy it never read.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlsplit

from maia.schemas import CorpusDocument, License, Registre, Source
from maia.scraping.extract import extract_main_text
from maia.scraping.http import PoliteFetcher
from maia.scraping.institutional import Extractor, SiteSpec, scrape_site

#: Press text is never publishable. Not a parameter — see the module docstring.
PRESS_LICENSE = License.NO_REDISTRIBUTE

#: Press articles are short by nature, but a real one clears this; a teaser does not.
DEFAULT_MIN_CHARS = 600


@dataclass(frozen=True)
class Outlet:
    """One newspaper: its registered domain and the name recorded in ``topic``."""

    domain: str
    name: str


#: The outlets named in the Phase-1 plan. Keyed by registered domain; subdomains match too.
PRESS_OUTLETS: tuple[Outlet, ...] = (
    Outlet("diariandorra.ad", "Diari d'Andorra"),
    Outlet("bondia.ad", "Bondia"),
    Outlet("elperiodic.ad", "El Periòdic d'Andorra"),
    Outlet("altaveu.com", "Altaveu"),
)

#: Phrases that only appear in a subscription wall, not in an article body.
_PAYWALL_MARKERS = (
    "per continuar llegint",
    "per seguir llegint",
    "continua llegint",
    "aquest contingut és exclusiu",
    "contingut exclusiu per a subscriptors",
    "fes-te subscriptor",
    "fes-te'n subscriptor",
    "subscriu-te",
    "inicia sessió per llegir",
    "article per a subscriptors",
    "para seguir leyendo",
    "hazte suscriptor",
    "suscríbete",
)

#: A body ending on one of these was cut off rather than finished.
_TRUNCATION_SUFFIXES = ("…", "...", "[…]")


def outlet_for(url: str) -> Outlet:
    """The registered outlet publishing ``url``.

    Raises:
        ValueError: if the host is not in :data:`PRESS_OUTLETS`. Refusing keeps a typo in a
            host from producing documents tagged ``premsa`` that came from somewhere else.
    """
    host = (urlsplit(url).hostname or "").lower()
    for outlet in PRESS_OUTLETS:
        if host == outlet.domain or host.endswith(f".{outlet.domain}"):
            return outlet
    raise ValueError(
        f"{host or url!r} is not a registered Andorran press outlet; known outlets: "
        f"{', '.join(o.domain for o in PRESS_OUTLETS)}"
    )


def is_teaser(text: str, *, min_chars: int = DEFAULT_MIN_CHARS) -> bool:
    """Whether ``text`` is a paywalled stub rather than an article.

    Three signals. A **subscription pitch** is conclusive — no article body asks the reader to
    subscribe. **Truncation** (a body ending in an ellipsis) is the metered-preview signature.
    And **length** is the backstop for a wall that says nothing recognisable: press articles
    are short, but a real one clears ``min_chars`` where a two-paragraph preview does not.

    This is the failure mode that makes a press scrape look successful while collecting
    nothing — every other filter in the pipeline sees ordinary Catalan prose.
    """
    stripped = text.strip()
    lowered = stripped.lower()
    if any(marker in lowered for marker in _PAYWALL_MARKERS):
        return True
    if stripped.endswith(_TRUNCATION_SUFFIXES):
        return True
    return len(stripped) < min_chars


def press_spec(*, min_chars: int = DEFAULT_MIN_CHARS) -> SiteSpec:
    """The §3.1 metadata every press document carries."""
    return SiteSpec(
        source=Source.PREMSA,
        license=PRESS_LICENSE,
        registre=Registre.ESTANDARD,
        min_chars=min_chars,
    )


def scrape_press(
    fetcher: PoliteFetcher,
    urls: Iterable[str],
    *,
    fetched_at: datetime | None = None,
    extractor: Extractor = extract_main_text,
    min_chars: int = DEFAULT_MIN_CHARS,
    topic: Iterable[str] | None = None,
) -> Iterator[CorpusDocument]:
    """Yield §3.1 documents for the press articles among ``urls``.

    Every URL is resolved to a registered outlet **before** being fetched, so an unregistered
    host fails fast rather than after a request. Each article's outlet name is prepended to
    its ``topic`` so the corpus can be filtered by newspaper.

    Pages disallowed by robots.txt, unreachable, or detected as paywalled teasers are
    skipped. Wire ``fetcher`` with :func:`~maia.scraping.http.polite_fetcher` so the policy is
    actually retrieved.
    """
    extra_topics = list(topic) if topic is not None else []
    spec = press_spec(min_chars=min_chars)

    for url in urls:
        outlet = outlet_for(url)
        for document in scrape_site(
            fetcher,
            [url],
            spec,
            fetched_at=fetched_at,
            extractor=extractor,
            topic=[outlet.name, *extra_topics],
        ):
            if is_teaser(document.text, min_chars=min_chars):
                continue
            yield document
