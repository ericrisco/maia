"""Diari del Consell General — acquisition, PDF repair, whitelist (PLAN M1.04-05).

M1.04 built the parser and M1.05 named the whitelist as a PO input; neither could reach a real
session, because the archive publishes **PDFs** and nothing here could read one. This module is
the missing half: find the sessions, fetch the PDF, and turn it into text the parser can trust.

**The PDF layer is not a formality.** Extracting text from `consellgeneral.ad`'s PDFs produces
Catalan that is subtly wrong in ways that survive every downstream check:

* **371 broken apostrophes in a single 54-page session.** The extractor emits ``d ’acord``,
  ``l ’article``, ``se ’m`` — a space before every apostrophe. Left alone, the corpus teaches the
  model to write Catalan elisions with a space in them. Nothing downstream would catch it: it is
  well-formed UTF-8, it is in Catalan, it passes the language detector, and it is wrong on almost
  every line.
* **53 repeated page footers**, each cutting a sentence in half where the page broke. They read as
  sentence fragments in the middle of an intervention.
* **Hyphenated line breaks**, where a word split across lines becomes two words.

:func:`repair_pdf_text` fixes those three and nothing else. It never touches the words themselves —
same rule as :func:`~maia.scraping.diari.clean_oral` — because a "helpful" normaliser is exactly
how genuine Andorran lexicon gets rewritten into standard Catalan.

**Whose interventions.** :func:`~maia.scraping.diari.parse_session` keeps only whitelisted
speakers, and the whitelist is a PO decision (M1.05, D-0046). The purpose is **register and
lexicon**: how Andorran Catalan is spoken in a formal setting, which words are used. It is not to
reproduce an identifiable person's voice, and D7 forbids using this subcorpus for that.

Be clear about where that protection actually lives, because it is easy to assume it is
structural and it is not. The §3.1 schema has a ``speaker`` field, it is deliberate (traceability:
a quotation has to be attributable back to who said it), and this pipeline fills it in. **The
corpus therefore can be filtered down to one person.** Nothing in the data prevents it. What
prevents the harm is downstream and has to keep being enforced: generation mixes speakers, D7
governs use, and M6.01 (:mod:`maia.publication.compliance`) checks before publication that no
example attributes a position to a named politician. A reader of this module should not come away
thinking the ingest made the misuse impossible.

The fetch is **blocked-by-resource** only in the sense that it needs the network; the polite
fetcher from M1 step 1 handles robots.txt and rate limiting, and every function below is
exercised offline against a fixture built from a real session.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path

from maia.schemas import CorpusDocument
from maia.scraping.diari import norm_name, parse_session
from maia.scraping.http import PoliteFetcher

#: The archive index for one year of sessions.
ARCHIVE = "https://www.consellgeneral.ad/ca/arxiu/diari-oficial-del-consell-general-1/any-{year}"

#: Plone's download view. Appended to a session URL, it returns the PDF.
DOWNLOAD_SUFFIX = "/at_download/pdf"

#: The archive's real extent, verified against the live site on 2026-08-02: `any-1990` through
#: `any-2023` return 200 and `any-2024` onward return 404. Sessions from the IX legislature are
#: published somewhere else — recorded in gaps.md rather than guessed at here, because a scraper
#: that silently returns nothing for recent years is worse than one that says it does not cover
#: them.
FIRST_ARCHIVED_YEAR = 1990
LAST_ARCHIVED_YEAR = 2023

#: Session pages look like ``.../any-2023/dcg-01-2023``. Matched rather than guessed: numbering
#: has gaps (``dcg-2-2021`` and ``dcg-28-2021`` both exist, with no zero padding in the first),
#: so constructing URLs from a counter would silently skip sessions.
_SESSION_HREF = re.compile(
    r'href="(?P<url>https://www\.consellgeneral\.ad/ca/arxiu/'
    r'diari-oficial-del-consell-general-1/any-\d{4}/dcg-[^"/]+)"'
)

#: The running footer, which repeats on every page and interrupts whatever sentence was in
#: progress.
#:
#: Matched by *shape* — a line that begins with the publication's name and ends in a page number —
#: rather than by enumerating the wording. The first version spelled out "celebrada el dia" and
#: silently missed every two-day sitting, which prints "celebrada els dies 02 i 03": seven footers
#: survived into a 2.1M-character corpus before a count caught them. The wording varies (spacing
#: after "núm.", singular vs plural dates); the shape does not.
_FOOTER = re.compile(
    r"^[ \t]*Diari oficial del Consell General[ \t]*[\u2013-].*?\d+[ \t]*$",
    re.IGNORECASE | re.MULTILINE,
)

#: A space (or newline) wedged before an apostrophe: ``d ’acord`` becomes ``d’acord``. Both
#: the typographic and the ASCII apostrophe appear in these files.
_LOOSE_APOSTROPHE = re.compile(r"(\w)\s+([’'])\s*(\w)")

#: A word split across a line break by a hyphen. Tolerates the blank line the footer removal
#: leaves behind, because the most common place for a word to be split is exactly where the page
#: broke — which is where the footer was.
_HYPHEN_BREAK = re.compile(r"(\w)-[ \t]*\n{1,2}[ \t]*(\w)")


@dataclass(frozen=True)
class Session:
    """One published session: where it lives and where its PDF lives."""

    url: str
    year: int

    @property
    def pdf_url(self) -> str:
        """The PDF behind this session page."""
        return f"{self.url}{DOWNLOAD_SUFFIX}"

    @property
    def slug(self) -> str:
        """``dcg-01-2023``. Useful as a cache key and in logs."""
        return self.url.rstrip("/").rsplit("/", 1)[-1]


def find_sessions(html: str, *, year: int) -> list[Session]:
    """Session pages linked from one year's archive index, in document order, deduplicated.

    The index also links neighbouring sessions from each entry, so the same URL appears several
    times; order is preserved because a caller fetching a year expects them in the published
    sequence rather than sorted as strings (``dcg-10`` before ``dcg-2``).
    """
    seen: set[str] = set()
    sessions: list[Session] = []
    for match in _SESSION_HREF.finditer(html):
        url = match.group("url")
        if url not in seen:
            seen.add(url)
            sessions.append(Session(url=url, year=year))
    return sessions


def repair_pdf_text(text: str) -> str:
    """Undo the three ways PDF extraction corrupts Catalan. Nothing else.

    Order matters twice over. Footers go first, so a footer's own text cannot be joined to the
    sentence it interrupted — and the footer is replaced by nothing rather than by a newline,
    because the newlines that surrounded its line are still there: substituting one more would
    leave three, and the hyphen rule below (deliberately bounded at two) would stop recognising
    the word split that happens at exactly that spot.
    """
    text = _FOOTER.sub("", text)
    text = _HYPHEN_BREAK.sub(r"\1\2", text)
    text = _LOOSE_APOSTROPHE.sub(r"\1’\3", text)
    # Page breaks leave runs of blank lines that would read as paragraph boundaries.
    text = re.sub(r"[ \t]+\n", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def extract_pdf_text(data: bytes) -> str:
    """Text of a PDF, repaired.

    ``pypdf`` is imported here rather than at module scope so importing :mod:`maia.scraping`
    stays cheap for the many callers that never touch a PDF.

    Raises:
        ValueError: when the bytes are not a readable PDF. A silent empty string would be
            indistinguishable from a session that happened to contain no interventions.
    """
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError

    try:
        reader = PdfReader(BytesIO(data))
        pages = [page.extract_text() or "" for page in reader.pages]
    except (PdfReadError, OSError, ValueError) as exc:
        raise ValueError(f"unreadable PDF: {exc}") from exc
    if not any(page.strip() for page in pages):
        raise ValueError(
            "the PDF has no extractable text: it is probably a scan, which needs OCR rather "
            "than extraction"
        )
    return repair_pdf_text("\n".join(pages))


@dataclass(frozen=True)
class Acquired:
    """What one fetch produced: the documents, and **everyone who spoke**.

    The speaker list is not decoration. Without it the caller cannot tell "the whitelist matched
    nobody" from "nobody said anything", and those need opposite responses.
    """

    documents: tuple[CorpusDocument, ...] = ()
    speakers: tuple[str, ...] = ()

    def __add__(self, other: Acquired) -> Acquired:
        return Acquired(self.documents + other.documents, self.speakers + other.speakers)


def fetch_session_documents(
    fetcher: PoliteFetcher,
    session: Session,
    *,
    whitelist: Iterable[WhitelistEntry],
    fetched_at: datetime | None = None,
    topic: Iterable[str] | None = None,
) -> Acquired:
    """Fetch one session: its whitelisted interventions, and every speaker it contained.

    Returns empty — rather than raising — when the session is unreachable or unreadable: a run
    over a year of sessions must not stop because one of them is a scanned procedural sitting.
    """
    payload = fetcher.fetch_bytes(session.pdf_url)
    if payload is None:
        return Acquired()
    try:
        transcript = extract_pdf_text(payload)
    except ValueError:
        return Acquired()
    documents = parse_session(
        transcript,
        whitelist=names_for_year(whitelist, session.year),
        session_url=session.url,
        fetched_at=fetched_at or datetime.now(UTC),
        topic=topic,
    )
    return Acquired(tuple(documents), tuple(speaker_counts(transcript)))


def scrape_year(
    fetcher: PoliteFetcher,
    year: int,
    *,
    whitelist: Iterable[WhitelistEntry],
    limit: int | None = None,
    fetched_at: datetime | None = None,
    topic: Iterable[str] | None = None,
) -> Acquired:
    """Every whitelisted intervention published in ``year``, plus everyone who spoke."""
    index = fetcher.fetch(ARCHIVE.format(year=year))
    if index is None:
        return Acquired()
    sessions = find_sessions(index, year=year)
    if limit is not None:
        sessions = sessions[:limit]
    acquired = Acquired()
    for session in sessions:
        acquired += fetch_session_documents(
            fetcher, session, whitelist=whitelist, fetched_at=fetched_at, topic=topic
        )
    return acquired


def speaker_counts(transcript: str) -> dict[str, int]:
    """How many interventions each speaker has, for choosing a whitelist.

    A whitelist is only as good as knowing who actually speaks: the session's attendance list
    names every member present, and most of them never take the floor.
    """
    from maia.scraping.diari import split_interventions

    counts: dict[str, int] = {}
    for turn in split_interventions(transcript):
        counts[turn.speaker] = counts.get(turn.speaker, 0) + 1
    return counts


#: A whitelist line: a name, optionally scoped to a range of years — ``cap de Govern [2019-2023]``.
_ENTRY = re.compile(r"^(?P<name>[^\[]+?)\s*(?:\[(?P<first>\d{4})\s*-\s*(?P<last>\d{4})\])?$")


@dataclass(frozen=True)
class WhitelistEntry:
    """One whitelisted speaker, as printed, optionally valid only for a range of years.

    **The years are not a convenience, they are a correctness control.** The Diari does not print
    a speaker the same way twice across a decade: in 2022 it writes ``El Sr. Xavier Espot:`` and in
    2021 it writes ``El Sr. cap de Govern:`` for the same person — which cost ~100 interventions
    before anyone noticed, because "Xavier Espot" *did* appear twice that year, so nothing was
    reported as unmatched.

    The obvious fix, adding ``cap de Govern`` to the whitelist, is a worse bug than the one it
    fixes: the office belonged to somebody else before 2019, so an unscoped alias silently
    attributes one politician's words to another. An office alias carries the years it was held.
    """

    name: str
    first_year: int | None = None
    last_year: int | None = None

    def applies_to(self, year: int) -> bool:
        """Whether this entry is valid for a session published in ``year``."""
        if self.first_year is not None and year < self.first_year:
            return False
        return not (self.last_year is not None and year > self.last_year)

    @property
    def is_office(self) -> bool:
        """Whether this entry is scoped, i.e. an office rather than a person."""
        return self.first_year is not None or self.last_year is not None


def load_whitelist(path: Path) -> list[WhitelistEntry]:
    """Read the M1.05 whitelist, including office aliases with their year ranges.

    Raises:
        ValueError: on a line that is neither a name nor ``name [YYYY-YYYY]``, and on a range whose
            end precedes its start. A malformed line silently ignored is a speaker silently
            missing, which is the failure mode this whole area keeps producing.
    """
    entries: list[WhitelistEntry] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.split("#", 1)[0].strip()
        if not stripped:
            continue
        match = _ENTRY.match(stripped)
        if not match:
            raise ValueError(f"{path}:{number}: cannot read whitelist entry {stripped!r}")
        first = int(match["first"]) if match["first"] else None
        last = int(match["last"]) if match["last"] else None
        if first is not None and last is not None and last < first:
            raise ValueError(f"{path}:{number}: range ends before it starts: {stripped!r}")
        entries.append(WhitelistEntry(match["name"].strip(), first, last))
    return entries


def names_for_year(entries: Iterable[WhitelistEntry], year: int) -> set[str]:
    """The names to match against a session published in ``year``."""
    return {entry.name for entry in entries if entry.applies_to(year)}


@dataclass(frozen=True)
class WhitelistMatch:
    """Which whitelisted speakers were actually found, and which were not.

    This exists because the failure it reports is **silent**. The Diari prints a member's full
    name in the attendance list (``M. I. Sr. Raul Ferré Bonet``) and a shorter form on each
    intervention (``El Sr. Raul Ferré:``). A whitelist copied from the attendance list — the
    obvious place to copy it from — therefore matches nothing at all, and the run completes
    successfully having ingested zero interventions from that person. Nobody finds out until
    somebody wonders why the corpus is smaller than expected, months later.
    """

    matched: tuple[str, ...] = ()
    unmatched: tuple[str, ...] = ()
    #: Names present in the sessions that look like an unmatched entry: ``{wanted: [candidates]}``.
    suggestions: Mapping[str, tuple[str, ...]] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """True when every whitelisted speaker was found at least once."""
        return not self.unmatched

    def report(self) -> str:
        """Lines for the acquisition log. Empty when everything matched."""
        if self.ok:
            return ""
        lines = []
        for name in self.unmatched:
            line = f"whitelist entry never spoke: {name!r}"
            if hints := self.suggestions.get(name):
                line += " — did you mean " + " / ".join(repr(hint) for hint in hints) + "?"
            lines.append(line)
        return "\n".join(lines)


def match_whitelist(speakers: Iterable[str], whitelist: Iterable[str]) -> WhitelistMatch:
    """Compare the speakers a run saw against the whitelist it was given.

    Suggestions are made on **surname overlap**, which is what the two printed forms of a name
    have in common. Deliberately loose: a wrong suggestion costs a glance, a missing one costs a
    silently empty subcorpus.
    """
    seen = {norm_name(name): name for name in speakers}
    matched: list[str] = []
    unmatched: list[str] = []
    suggestions: dict[str, tuple[str, ...]] = {}

    for wanted in whitelist:
        if norm_name(wanted) in seen:
            matched.append(wanted)
            continue
        unmatched.append(wanted)
        wanted_parts = set(norm_name(wanted).split())
        hints = tuple(
            printed
            for key, printed in sorted(seen.items())
            if wanted_parts & set(key.split()) and len(key.split()) > 1
        )
        if hints:
            suggestions[wanted] = hints
    return WhitelistMatch(tuple(matched), tuple(unmatched), suggestions)


def summarise(documents: Sequence[CorpusDocument]) -> str:
    """One line per run, for the acquisition log."""
    characters = sum(len(document.text) for document in documents)
    return f"{len(documents)} intervention(s), {characters:,} characters"


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point: acquire whitelisted interventions for a range of years.

    Writes §3.1 JSONL. Live by default, because unlike the GPU stages this one only needs the
    network — but ``--dry-run`` lists what it would fetch, which is the right first command when
    the site's layout may have changed under us.
    """
    import argparse
    import json
    import sys
    from pathlib import Path

    from maia.scraping.http import polite_fetcher

    parser = argparse.ArgumentParser(
        description="Acquire the Diari del Consell General (M1.04-05). The archive covers "
        f"{FIRST_ARCHIVED_YEAR}-{LAST_ARCHIVED_YEAR}; later sessions are published elsewhere "
        "(see gaps.md). Respects robots.txt and rate-limits by default."
    )
    parser.add_argument("--from-year", type=int, default=LAST_ARCHIVED_YEAR)
    parser.add_argument("--to-year", type=int, default=LAST_ARCHIVED_YEAR)
    parser.add_argument(
        "--whitelist", type=Path, default=Path("configs/parlamentaris.txt"), help="M1.05 whitelist"
    )
    parser.add_argument("--out", type=Path, help="write §3.1 JSONL here")
    parser.add_argument("--cache", type=Path, help="cache directory for fetched pages and PDFs")
    parser.add_argument("--limit", type=int, help="at most this many sessions per year")
    parser.add_argument("--min-interval", type=float, default=2.0, help="seconds between requests")
    parser.add_argument("--dry-run", action="store_true", help="list sessions, fetch no PDFs")
    args = parser.parse_args(argv)

    if not args.whitelist.is_file():
        print(f"error: no whitelist at {args.whitelist}", file=sys.stderr)
        return 1
    try:
        whitelist = load_whitelist(args.whitelist)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not whitelist:
        print(f"error: {args.whitelist} lists no speakers", file=sys.stderr)
        return 1

    fetcher = polite_fetcher(min_interval=args.min_interval, cache_dir=args.cache)
    documents: list[CorpusDocument] = []
    speakers: set[str] = set()
    for year in range(args.from_year, args.to_year + 1):
        if args.dry_run:
            index = fetcher.fetch(ARCHIVE.format(year=year))
            found = find_sessions(index, year=year) if index else []
            print(f"{year}: {len(found)} session(s)")
            for session in found[: args.limit] if args.limit else found:
                print(f"  {session.slug} -> {session.pdf_url}")
            continue
        acquired = scrape_year(fetcher, year, whitelist=whitelist, limit=args.limit)
        print(f"{year}: {summarise(acquired.documents)}")
        documents.extend(acquired.documents)
        speakers.update(acquired.speakers)

    if fetcher.disallowed:
        print(f"robots.txt disallowed {len(fetcher.disallowed)} URL(s)", file=sys.stderr)
    if args.dry_run:
        return 0

    # A whitelist entry that never matched is the failure mode this pipeline is most likely to
    # hit and least likely to notice, so it is a warning on every run and not a debug flag.
    match = match_whitelist(speakers, (entry.name for entry in whitelist))
    if not match.ok:
        print(match.report(), file=sys.stderr)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8") as handle:
            for document in documents:
                handle.write(json.dumps(document.model_dump(mode="json"), ensure_ascii=False))
                handle.write("\n")
        print(f"wrote {len(documents)} document(s) to {args.out}")
    # No documents is a failure worth an exit code: it means the layout changed, the whitelist
    # names nobody who spoke, or robots blocked everything — never "the sessions were empty".
    return 0 if documents else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
