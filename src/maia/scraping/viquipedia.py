"""Viquipèdia (Catalan Wikipedia) dump parser — PLAN M1.02.

Parses a MediaWiki XML export (``*-pages-articles.xml``) into :class:`CorpusDocument`
objects. Streaming (``iterparse`` + root clearing) so a multi-GB dump is processed with
bounded memory. Filters to main-namespace, non-redirect, Andorra-relevant articles and
converts wikitext to plain text.

Licensing: Viquipèdia is CC-BY-SA; every document is tagged ``license=cc-by-sa-3.0`` and
``source=viquipedia`` (§3.1). Relevance is decided by an explicit category allowlist when
given (the production path: the resolved "Andorra" category + subcategories), else by a
keyword fallback on title/categories.

The full dump download is a runtime/bandwidth concern (blocked-by-resource); the parsing
and filtering logic here is fully exercised by fixtures.
"""

from __future__ import annotations

import contextlib
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import IO
from urllib.parse import quote
from xml.etree.ElementTree import Element, iterparse

import mwparserfromhell

from maia.schemas import CorpusDocument, License, Registre, Source, normalize_text

#: Fallback relevance keywords (lowercased substrings) when no allowlist is given.
DEFAULT_ANDORRA_KEYWORDS: frozenset[str] = frozenset(
    {
        "andorra",
        "andorran",
        "coprincipat",
        "parròquia",
        "parroquia",
        "escaldes",
        "encamp",
        "canillo",
        "ordino",
        "la massana",
        "sant julià de lòria",
        "consell general",
    }
)

_CATEGORY_PREFIXES = ("categoria:", "category:")


@dataclass(frozen=True)
class RawPage:
    """A single ``<page>`` extracted from the dump."""

    title: str
    ns: int
    is_redirect: bool
    wikitext: str


def _local(tag: str) -> str:
    """Local name of a possibly namespaced XML tag."""
    return tag.rpartition("}")[2]


def _find_text(elem: Element, name: str) -> str | None:
    for child in elem.iter():
        if _local(child.tag) == name:
            return child.text
    return None


def _has_child(elem: Element, name: str) -> bool:
    return any(_local(child.tag) == name for child in elem.iter())


def iter_pages(source: str | Path | IO[bytes]) -> Iterator[RawPage]:
    """Stream ``RawPage`` objects from a MediaWiki XML export with bounded memory."""
    context = iterparse(source, events=("start", "end"))
    _, root = next(context)  # the <mediawiki> root
    for event, elem in context:
        if event != "end" or _local(elem.tag) != "page":
            continue
        title = _find_text(elem, "title") or ""
        ns_text = (_find_text(elem, "ns") or "0").strip()
        wikitext = _find_text(elem, "text") or ""
        yield RawPage(
            title=title,
            ns=int(ns_text) if ns_text.lstrip("-").isdigit() else 0,
            is_redirect=_has_child(elem, "redirect"),
            wikitext=wikitext,
        )
        root.clear()  # free processed pages


def extract_categories(wikitext: str) -> list[str]:
    """Category names referenced by the wikitext (prefix stripped, order-preserving)."""
    code = mwparserfromhell.parse(wikitext)
    out: list[str] = []
    seen: set[str] = set()
    for link in code.filter_wikilinks():
        target = str(link.title).strip()
        low = target.lower()
        for prefix in _CATEGORY_PREFIXES:
            if low.startswith(prefix):
                name = target[len(prefix) :].split("|", 1)[0].strip()
                if name and name.lower() not in seen:
                    seen.add(name.lower())
                    out.append(name)
                break
    return out


_DROP_LINK_PREFIXES = (
    "categoria:",
    "category:",
    "fitxer:",
    "file:",
    "imatge:",
    "image:",
)


def wikitext_to_text(wikitext: str) -> str:
    """Convert wikitext to normalized plain text.

    Category/file/image links are removed first (``strip_code`` would otherwise leak their
    ``Categoria:…`` titles into the body); remaining markup is stripped and blank-line runs
    are collapsed.
    """
    code = mwparserfromhell.parse(wikitext)
    for link in list(code.filter_wikilinks()):
        if str(link.title).strip().lower().startswith(_DROP_LINK_PREFIXES):
            with contextlib.suppress(ValueError):  # node may already be detached
                code.remove(link)
    stripped = code.strip_code(normalize=True, collapse=True)
    text = re.sub(r"\n{3,}", "\n\n", stripped)
    return text.strip()


def is_relevant(
    page: RawPage,
    categories: Iterable[str],
    *,
    keywords: Iterable[str] = DEFAULT_ANDORRA_KEYWORDS,
    category_allowlist: Iterable[str] | None = None,
) -> bool:
    """Decide whether a page belongs to the Andorra corpus.

    If ``category_allowlist`` is given (production: the resolved Andorra category tree),
    a page is relevant iff one of its categories is in the allowlist. Otherwise a keyword
    fallback matches title or categories.
    """
    if category_allowlist is not None:
        allow = {c.lower() for c in category_allowlist}
        return any(c.lower() in allow for c in categories)
    kws = [k.lower() for k in keywords]
    haystacks = [page.title.lower(), *(c.lower() for c in categories)]
    return any(kw in hay for kw in kws for hay in haystacks)


def _article_url(title: str) -> str:
    return f"https://ca.wikipedia.org/wiki/{quote(title.replace(' ', '_'), safe='/:')}"


def to_document(
    page: RawPage,
    categories: list[str],
    text: str,
    *,
    fetched_at: datetime,
    max_topics: int = 8,
) -> CorpusDocument:
    """Build a §3.1 document from a relevant Viquipèdia page and its clean text."""
    return CorpusDocument(
        text=text,
        source=Source.VIQUIPEDIA,
        url=_article_url(page.title),  # type: ignore[arg-type]
        fetched_at=fetched_at,
        lang="ca",
        topic=categories[:max_topics],
        license=License.CC_BY_SA_3_0,
        registre=Registre.ESTANDARD,
    )


def parse_dump(
    source: str | Path | IO[bytes],
    *,
    keywords: Iterable[str] = DEFAULT_ANDORRA_KEYWORDS,
    category_allowlist: Iterable[str] | None = None,
    min_chars: int = 200,
    fetched_at: datetime | None = None,
) -> Iterator[CorpusDocument]:
    """Yield Andorra-relevant §3.1 documents from a MediaWiki XML dump.

    Skips non-main-namespace pages, redirects, irrelevant pages, and articles whose clean
    text is shorter than ``min_chars`` (boilerplate/stubs).
    """
    stamp = fetched_at or datetime.now(UTC)
    for page in iter_pages(source):
        if page.ns != 0 or page.is_redirect:
            continue
        categories = extract_categories(page.wikitext)
        if not is_relevant(
            page, categories, keywords=keywords, category_allowlist=category_allowlist
        ):
            continue
        text = wikitext_to_text(page.wikitext)
        if len(normalize_text(text)) < min_chars:
            continue
        yield to_document(page, categories, text, fetched_at=stamp)
