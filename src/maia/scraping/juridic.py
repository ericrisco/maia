"""Juridical ingestion + chunk-by-article — PLAN M1.06.

Turns the **consolidated text (*text refós vigent*)** of an Andorran norm into §3.1 corpus
documents, **one document per article** — the natural unit of legal retrieval and citation
(decision D8: *concepts in the weights, articles in RAG, chunk-by-article, official sources
only*).

Three things this module owns:

1. :func:`split_law` — the parser. Recognizes the structural skeleton of an Andorran
   consolidated text (``Llibre``/``Títol``/``Capítol``/``Secció``), the articles
   (``Article 5``, ``Article 2 bis``, with or without a rubric) and the closing
   *disposicions* (addicionals, transitòries, derogatòries, finals — both the
   ``Disposició final primera`` form and the ``Disposicions finals`` + ``Primera.`` form).
2. :func:`parse_law` — chunk → §3.1 document with :class:`~maia.schemas.Legal` metadata
   (``rang``, ``article``, ``consolidacio_data``, ``llei``).
3. :func:`license_for` — the compliance gate. Only official routes are ingestible
   (``portaljuridicandorra.ad``, ``consellgeneral.ad``, ``bopa.ad``); anything else — most
   pointedly ``leslleis.com`` — raises. BOPA maps to ``no-redistribute`` because its
   disposals may be reproduced *when cited within a publication* but not published as a
   standalone collection, so BOPA text is RAG-internal/grounding only.

Every chunk's text opens with a **citation line** (``<norma> — <estructura> — Article N``).
That is deliberate on two counts: it is the contextual-retrieval trick (a chunk that names
its own law and article embeds and cites far better), and it makes the §3.1 content id
unique — without it, the boilerplate final provision shared by dozens of laws would hash to
one single id and the consolidation pass would collapse distinct articles into one.

The *download* of the real laws is **blocked-by-resource** (network + per-law URLs and
consolidation dates from the official portals). :func:`fetch_law` is the live seam; the
parsing and compliance logic below is fully exercised offline against fixtures.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from urllib.parse import urlsplit

from maia.schemas import CorpusDocument, Legal, License, Rang, Registre, Source, normalize_text
from maia.scraping.extract import extract_main_text
from maia.scraping.http import PoliteFetcher

# ─────────────────────────────────────────────────────────────
# Official routes — the compliance gate (ANEXO §8)
# ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class LegalRoute:
    """One official ingestion route and the license its texts carry."""

    license: License
    note: str


#: Registered domains for legal ingestion. Nothing outside this table may be ingested:
#: private compilations (leslleis.com) carry a redistribution risk and are banned outright.
LEGAL_ROUTES: dict[str, LegalRoute] = {
    "portaljuridicandorra.ad": LegalRoute(
        License.PUBLIC_OFFICIAL,
        "official consolidated-text portal — the primary route for a text refós vigent",
    ),
    "consellgeneral.ad": LegalRoute(
        License.PUBLIC_OFFICIAL,
        "Consell General archive — per-law publication of approved norms",
    ),
    "bopa.ad": LegalRoute(
        License.NO_REDISTRIBUTE,
        "reproducible when cited within a publication, not as a standalone collection — "
        "RAG-internal and grounding only, never in the public dataset",
    ),
}


def license_for(url: str) -> License:
    """Return the §3.1 license for a legal source URL.

    Raises:
        ValueError: if the host is not one of :data:`LEGAL_ROUTES` — legal text is ingested
            from official sources only.
    """
    host = (urlsplit(url).hostname or "").lower()
    for domain, route in LEGAL_ROUTES.items():
        if host == domain or host.endswith(f".{domain}"):
            return route.license
    raise ValueError(
        f"{host or url!r} is not an official Andorran legal source; allowed hosts: "
        f"{', '.join(sorted(LEGAL_ROUTES))}"
    )


# ─────────────────────────────────────────────────────────────
# Structural grammar of an Andorran consolidated text
# ─────────────────────────────────────────────────────────────

_ORDINALS = (
    "única|únic|unica|unic|primera|primer|segona|segon|tercera|tercer|quarta|quart|"
    "cinquena|cinquè|sisena|sisè|setena|setè|vuitena|vuitè|novena|novè|desena|desè"
)
_ARTICLE_SUFFIX = "bis|ter|quater|quinquies|sexies|septies|octies"
_SEPARATOR = r"[.\-\u2013\u2014:)]"

# "Article 5", "Article 2 bis", optionally followed by a separator then a rubric or the body
# (disambiguated by _rubric_and_body_start).
_ARTICLE = re.compile(
    rf"^[ \t]*Article[ \t]+(?P<num>\d+(?:[ \t]+(?:{_ARTICLE_SUFFIX}))?)[ \t]*{_SEPARATOR}?[ \t]*",
    re.MULTILINE,
)

# "Títol II. Dels drets i llibertats", "Capítol primer", "Secció segona", "Llibre I".
_STRUCTURE = re.compile(
    r"^[ \t]*(?P<kind>Llibre|T[íi]tol|Cap[íi]tol|Secci[óo]|Subsecci[óo])"
    rf"[ \t]+(?P<desig>[IVXLCDM]+|\d+|preliminar|{_ORDINALS})"
    rf"[ \t]*(?:{_SEPARATOR}[^\n]*)?[ \t]*$",
    re.MULTILINE | re.IGNORECASE,
)

# "Disposició final", "Disposició derogatòria única", "Disposicions transitòries".
_DISPOSICIO = re.compile(
    r"^[ \t]*(?P<noun>Disposicions|Disposici[óo])"
    r"[ \t]+(?P<kind>addicionals?|transit[òo]ri(?:a|es)|derogat[òo]ri(?:a|es)|finals?)"
    rf"(?:[ \t]+(?P<ord>{_ORDINALS}))?[ \t]*{_SEPARATOR}?[ \t]*",
    re.MULTILINE | re.IGNORECASE,
)

# "Primera." / "Segona" — a sub-item, meaningful only under a plural disposicions heading.
_ORDINAL_ITEM = re.compile(
    rf"^[ \t]*(?P<ord>{_ORDINALS})[ \t]*(?:{_SEPARATOR}[ \t]*|(?=\n|$))",
    re.MULTILINE | re.IGNORECASE,
)

#: Structural depth and canonical spelling, keyed by the accent-stripped heading word — the
#: official texts are accented, extracted copies sometimes are not.
_STRUCTURE_LEVELS: dict[str, tuple[int, str]] = {
    "llibre": (0, "Llibre"),
    "titol": (1, "Títol"),
    "capitol": (2, "Capítol"),
    "seccio": (3, "Secció"),
    "subseccio": (4, "Subsecció"),
}

#: Canonical singular of each *disposició* kind, keyed by its accent-stripped form.
_DISPOSICIO_SINGULAR: dict[str, str] = {
    "addicional": "addicional",
    "addicionals": "addicional",
    "transitoria": "transitòria",
    "transitories": "transitòria",
    "derogatoria": "derogatòria",
    "derogatories": "derogatòria",
    "final": "final",
    "finals": "final",
}

#: Canonical plural, for the heading of a *disposicions* group.
_DISPOSICIO_PLURAL: dict[str, str] = {
    "addicional": "addicionals",
    "transitòria": "transitòries",
    "derogatòria": "derogatòries",
    "final": "finals",
}


def _normalize_designator(number: str) -> str:
    """Canonical form of an article ordinal — ``"01 bis"`` and ``"1 bis"`` are the same article."""
    head, _, tail = number.partition(" ")
    return f"{int(head)} {tail}".strip() if head.isdigit() else number


def _fold(word: str) -> str:
    """Lowercase and strip accents — the key into the tables above."""
    decomposed = unicodedata.normalize("NFD", word.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


#: A rubric this short is accepted whenever the next line opens a new block.
_MAX_RUBRIC_CHARS = 60
#: Beyond this, a same-line heading tail is body text whatever follows it.
_MAX_LONG_RUBRIC_CHARS = 90

#: A numbered legal paragraph — "1. Andorra és…", the usual first line of an article body.
_NUMBERED_PARAGRAPH = re.compile(r"^[ \t]*\d+\.[ \t]*\S")

#: Characters that end a sentence, so the following line starts a new one.
_SENTENCE_END = '.:;!?»"”'
#: An enumerated item — "a)", "2.", "—" — where a line break carries meaning.
_ENUMERATOR = re.compile(r"^(?:\d+[.)]|[a-zA-Z][.)]|[-\u2013\u2014\u2022*])[ \t]")


@dataclass(frozen=True)
class ArticleChunk:
    """One legal unit: an article or a *disposició*.

    Attributes:
        label: the unit as printed — ``"Article 2 bis"``, ``"Disposició final primera"``.
        designator: what goes in §3.1 ``legal.article`` — ``"2 bis"`` for articles, the full
            label for *disposicions* (they have no number to cite).
        rubric: the article's own title when the source prints one, else ``None``.
        structure: the enclosing hierarchy, outermost first — ``("Llibre I", "Títol I")``.
        body: the article's text, with the heading line removed.
    """

    label: str
    designator: str
    rubric: str | None
    structure: tuple[str, ...]
    body: str


@dataclass(frozen=True)
class LawSplit:
    """The result of splitting a consolidated text.

    ``preamble`` holds everything before the first recognized unit (the norm's title, the
    *preàmbul* / *exposició de motius*). It is returned rather than discarded so callers can
    decide what to do with it; :func:`parse_law` does not turn it into a document, because
    it is not a citable article.
    """

    preamble: str
    articles: tuple[ArticleChunk, ...]


@dataclass(frozen=True)
class _Marker:
    """An internal heading match, before bodies are sliced."""

    start: int
    end: int
    kind: str  # "structure" | "group" | "unit" | "ordinal"
    label: str
    designator: str
    level: int = -1
    disposicio: str = ""


def _is_heading_line(line: str) -> bool:
    """Whether ``line`` opens a structural unit — an article, a *disposició*, a Títol…"""
    return any(
        pattern.match(line) for pattern in (_ARTICLE, _STRUCTURE, _DISPOSICIO, _ORDINAL_ITEM)
    )


def _unwrap(text: str) -> str:
    """Rejoin lines that a fixed-width source broke mid-sentence.

    Official texts arrive hard-wrapped near 80-90 columns (per-law PDFs especially), which
    would otherwise leave a newline in the middle of every other sentence of the corpus. A
    line is a continuation when the previous line has no sentence-ending punctuation and it
    does not itself open an enumerated item (``a)``, ``2.``, ``—``) — the one case where the
    break is meaningful.

    A **heading line never absorbs the line after it**, so ``Article 5. Sancions`` keeps its
    rubric instead of swallowing the first line of its body. The asymmetry is deliberate: a
    heading is protected as the *source* of a join, never as the *target*. That is exactly what
    tells a real heading apart from a wrapped cross-reference — ``…que estableix l'`` followed
    by ``Article 7 de la Llei…`` is one unfinished sentence, so it is joined, and the parser
    never sees a fabricated article there.
    """
    joined: list[str] = []
    for line in text.split("\n"):
        previous = joined[-1] if joined else ""
        if (
            previous
            and line
            and previous[-1] not in _SENTENCE_END
            and not _ENUMERATOR.match(line)
            and not _is_heading_line(previous)
        ):
            joined[-1] = f"{previous} {line}"
        else:
            joined.append(line)
    return "\n".join(joined)


def _clean(text: str) -> str:
    """Normalize the whitespace of extracted legal text without touching its words."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = _unwrap(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _rubric_and_body_start(text: str, pos: int) -> tuple[str | None, int]:
    """Decide whether the rest of the heading line at ``pos`` is a rubric or already body.

    Andorran consolidated texts write both ``Article 1. Principi de legalitat`` (a rubric,
    body on the next line) and ``Article 1. No serà castigada cap acció...`` (body already
    on the heading line). Two signals separate them:

    * **Shape of the tail** — a rubric is short and is not a sentence (no closing
      punctuation). Extracted text is hard-wrapped near 80-90 columns, so a tail that long
      is almost always the first wrapped line of the body.
    * **What follows** — after a rubric the next line opens a new block (blank, or a
      numbered paragraph such as ``1.``); after a wrapped body line it continues the same
      sentence.

    Returns the rubric (or ``None``) and the offset where the body starts.
    """
    line_end = text.find("\n", pos)
    if line_end == -1:
        line_end = len(text)
    tail = text[pos:line_end].strip()
    if not tail:
        return None, line_end
    if len(tail) > _MAX_LONG_RUBRIC_CHARS or tail[-1] in ".:;,":
        return None, pos

    next_line_end = text.find("\n", line_end + 1)
    next_line = text[line_end + 1 : next_line_end if next_line_end != -1 else len(text)]
    new_block = not next_line.strip() or bool(_NUMBERED_PARAGRAPH.match(next_line))
    short_and_titled = len(tail) <= _MAX_RUBRIC_CHARS and next_line[:1].isupper()
    if tail[0].isupper() and (new_block or short_and_titled):
        return tail, line_end
    return None, pos


def _collect_markers(text: str) -> list[_Marker]:
    """Find every heading in ``text``, ordered by position, ordinals resolved to units.

    The four patterns cannot overlap: each anchors at the start of a line and consumes no
    newline, and no two of them accept the same opening word.
    """
    markers: list[_Marker] = []

    for match in _STRUCTURE.finditer(text):
        level, canonical = _STRUCTURE_LEVELS[_fold(match.group("kind"))]
        markers.append(
            _Marker(
                start=match.start(),
                end=match.end(),
                kind="structure",
                label=f"{canonical} {match.group('desig')}",
                designator="",
                level=level,
            )
        )

    for match in _ARTICLE.finditer(text):
        # Normalize the ordinal so "Article 01" and "Article 1" are one designator; otherwise
        # the duplicate-designator guard misses them and two documents cite the same article.
        number = _normalize_designator(re.sub(r"\s+", " ", match.group("num")))
        markers.append(
            _Marker(
                start=match.start(),
                end=match.end(),
                kind="unit",
                label=f"Article {number}",
                designator=number,
            )
        )

    for match in _DISPOSICIO.finditer(text):
        kind = _DISPOSICIO_SINGULAR[_fold(match.group("kind"))]
        ordinal = match.group("ord")
        plural = _fold(match.group("noun")) == "disposicions"
        if plural and ordinal is None:
            label = f"Disposicions {_DISPOSICIO_PLURAL[kind]}"
            markers.append(
                _Marker(
                    start=match.start(),
                    end=match.end(),
                    kind="group",
                    label=label,
                    designator=label,
                    disposicio=kind,
                )
            )
            continue
        label = f"Disposició {kind}"
        if ordinal is not None:
            label = f"{label} {ordinal.lower()}"
        markers.append(
            _Marker(
                start=match.start(),
                end=match.end(),
                kind="unit",
                label=label,
                designator=label,
                disposicio=kind,
            )
        )

    for match in _ORDINAL_ITEM.finditer(text):
        markers.append(
            _Marker(
                start=match.start(),
                end=match.end(),
                kind="ordinal",
                label=match.group("ord").lower(),
                designator="",
            )
        )

    markers.sort(key=lambda m: m.start)
    return _resolve_ordinals(markers)


def _resolve_ordinals(markers: list[_Marker]) -> list[_Marker]:
    """Bind ordinal sub-items to their plural *disposicions* group; drop stray ones.

    A group with no sub-items of its own (``Disposicions finals`` followed directly by
    prose) degrades into a unit, so its text is never silently dropped.
    """
    resolved: list[_Marker] = []
    group: _Marker | None = None
    group_index: int | None = None
    group_has_items = False

    for marker in markers:
        if marker.kind == "ordinal":
            if group is None:
                continue  # a stray ordinal line outside any group is not a heading
            group_has_items = True
            resolved.append(
                _Marker(
                    start=marker.start,
                    end=marker.end,
                    kind="unit",
                    label=f"Disposició {group.disposicio} {marker.label}",
                    designator=f"Disposició {group.disposicio} {marker.label}",
                    disposicio=group.disposicio,
                )
            )
            continue

        if group is not None and group_index is not None and not group_has_items:
            resolved[group_index] = _Marker(
                start=group.start,
                end=group.end,
                kind="unit",
                label=group.label,
                designator=group.label,
                disposicio=group.disposicio,
            )
        group = group_index = None
        group_has_items = False

        if marker.kind == "group":
            group, group_index = marker, len(resolved)
        resolved.append(marker)

    if group is not None and group_index is not None and not group_has_items:
        resolved[group_index] = _Marker(
            start=group.start,
            end=group.end,
            kind="unit",
            label=group.label,
            designator=group.label,
            disposicio=group.disposicio,
        )
    return resolved


def split_law(text: str) -> LawSplit:
    """Split a consolidated legal text into its articles and *disposicions*.

    Structural headings (``Llibre``/``Títol``/``Capítol``/``Secció``) are not chunks: they
    are carried on each article as :attr:`ArticleChunk.structure`, which is how a lawyer
    cites and how a retriever benefits. The closing *disposicions* carry no structure —
    they sit outside the articulated body, so inheriting the last article's ``Títol`` would
    fabricate a citation.
    """
    # Headings are found on the *unwrapped* text. On the raw text, a hard wrap that happens to
    # break before a cross-reference ("…que estableix l'\nArticle 7 de la Llei…") looks exactly
    # like a heading: it fabricates an article that cites the wrong law and truncates the real
    # article's body at the wrap. Unwrapping first removes the ambiguity entirely.
    text = _clean(text)
    markers = _collect_markers(text)
    if not markers:
        return LawSplit(preamble=text, articles=())

    preamble = _clean(text[: markers[0].start])
    active: dict[int, str] = {}
    chunks: list[ArticleChunk] = []

    for index, marker in enumerate(markers):
        if marker.kind == "structure":
            active = {level: label for level, label in active.items() if level < marker.level}
            active[marker.level] = marker.label
            continue
        if marker.disposicio:
            active = {}
        if marker.kind != "unit":
            continue
        rubric, body_start = _rubric_and_body_start(text, marker.end)
        body_end = markers[index + 1].start if index + 1 < len(markers) else len(text)
        chunks.append(
            ArticleChunk(
                label=marker.label,
                designator=marker.designator,
                rubric=rubric,
                structure=tuple(label for _, label in sorted(active.items())),
                body=_clean(text[body_start:body_end]),
            )
        )

    return LawSplit(preamble=preamble, articles=tuple(chunks))


# ─────────────────────────────────────────────────────────────
# §3.1 documents
# ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class LawSpec:
    """Identity and provenance of one norm — everything §3.1 needs that the text lacks.

    Attributes:
        citation: how the norm is cited, used as the chunk's citation line — e.g.
            ``"Constitució del Principat d'Andorra"``, ``"Llei 9/2005, del 21 de febrer,
            del Codi penal"``.
        rang: constitucio / qualificada / ordinaria / reglament.
        consolidacio_data: the date of the consolidated version being ingested. Mandatory:
            a legal answer without it cannot be trusted, and the quarterly reindexation
            runbook compares against it.
        url: the official source URL; it also determines the license (:func:`license_for`).
        llei: §3.1 ``legal.llei`` — the canonical law citation (``"Llei 9/2005"``, which
            encodes both number and year). ``None`` for the Constitution, which is not a
            *llei*.
        license: an override that may only **tighten** what the URL's route implies. See
            :meth:`resolved_license`.
    """

    citation: str
    rang: Rang
    consolidacio_data: date
    url: str
    llei: str | None = None
    license: License | None = None

    def resolved_license(self) -> License:
        """The license to stamp on this norm's documents.

        The host is checked **always**, even when ``license`` is set, and an override may only
        move towards ``no-redistribute`` — never widen a restricted route to a publishable
        licence, and never skip the official-sources gate.

        An earlier version returned the override directly. That made the one control the wiki
        says is "enforced in code rather than by convention" bypassable with a single keyword
        argument: ``leslleis.com`` became ingestible, and a ``bopa.ad`` document could be
        re-tagged ``public-official`` and then pass the public-upload wall in M1.09.

        Raises:
            ValueError: if the host is not an official route, or if the override would widen
                a ``no-redistribute`` route.
        """
        from_route = license_for(self.url)
        if self.license is None:
            return from_route
        if not from_route.is_public() and self.license.is_public():
            raise ValueError(
                f"cannot relabel {self.url} as {self.license.value}: its route is "
                f"{from_route.value} and an override may only tighten, never widen"
            )
        return self.license


def citation_line(spec: LawSpec, chunk: ArticleChunk) -> str:
    """The self-describing first line of a legal chunk.

    ``Llei 9/2005, del Codi penal — Llibre I, Títol I — Article 1. Principi de legalitat``
    """
    label = f"{chunk.label}. {chunk.rubric}" if chunk.rubric else chunk.label
    parts = [spec.citation]
    if chunk.structure:
        parts.append(", ".join(chunk.structure))
    parts.append(label)
    return " — ".join(parts)


def parse_law(
    text: str,
    spec: LawSpec,
    *,
    fetched_at: datetime | None = None,
    topic: Iterable[str] | None = None,
    min_chars: int = 1,
) -> list[CorpusDocument]:
    """Turn a consolidated legal text into one §3.1 document per article.

    ``min_chars`` defaults to 1 — only empty units are dropped. Unlike a web page, a short
    article is not boilerplate (*"El català és la llengua oficial de l'Estat."* is the whole
    of Constitution art. 2.1), and dropping one would leave a hole in a corpus whose entire
    purpose is exact citation.

    Raises:
        ValueError: if two units resolve to the same designator, which means the split
            misfired. Failing loudly beats emitting two documents that cite the same
            article, or colliding ids that a later consolidation pass would merge.
    """
    stamp = fetched_at or datetime.now(UTC)
    topics = list(topic) if topic is not None else []
    doc_license = spec.resolved_license()
    split = split_law(text)

    counts = Counter(chunk.designator for chunk in split.articles)
    duplicates = sorted(designator for designator, n in counts.items() if n > 1)
    if duplicates:
        raise ValueError(f"duplicate legal designators in {spec.citation!r}: {duplicates}")

    docs: list[CorpusDocument] = []
    for chunk in split.articles:
        if len(normalize_text(chunk.body)) < min_chars:
            continue
        docs.append(
            CorpusDocument(
                text=f"{citation_line(spec, chunk)}\n\n{chunk.body}",
                source=Source.JURIDIC,
                url=spec.url,  # type: ignore[arg-type]
                fetched_at=stamp,
                lang="ca",
                topic=topics,
                license=doc_license,
                registre=Registre.ESTANDARD,
                legal=Legal(
                    rang=spec.rang,
                    article=chunk.designator,
                    consolidacio_data=spec.consolidacio_data,
                    llei=spec.llei,
                ),
            )
        )
    return docs


def fetch_law(
    fetcher: PoliteFetcher,
    spec: LawSpec,
    *,
    fetched_at: datetime | None = None,
    topic: Iterable[str] | None = None,
    min_chars: int = 1,
) -> list[CorpusDocument]:
    """Fetch a norm from its official URL and chunk it by article.

    The live network path is blocked-by-resource; ``fetcher`` is the injected seam, so this
    is exercised offline with a fixture-backed :class:`~maia.scraping.http.PoliteFetcher`.
    Returns ``[]`` when the page is unreachable, disallowed by robots.txt, or empty.
    """
    spec.resolved_license()  # fail fast on a non-official host, before any request
    html = fetcher.fetch(spec.url)
    if html is None:
        return []
    text = extract_main_text(html, spec.url)
    if text is None:
        return []
    return parse_law(text, spec, fetched_at=fetched_at, topic=topic, min_chars=min_chars)
