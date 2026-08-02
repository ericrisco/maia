"""RTVA audio acquisition — the daily editorial of *Avui serà un bon dia* (PLAN M1.13).

M1.13 built everything that happens *after* a transcript: segment merging, hallucination
filtering, oral cleaning, the ``no-redistribute`` stamp. What it never had was a way to get the
audio. This module is that: find the episodes, find the MP3 behind each one, fetch it, and write a
manifest so the transcription step — which needs a GPU and does not exist yet — can be a separate,
resumable pass over files already on disk.

**Why this programme.** The editorial is the most useful oral Andorran Catalan available on a
predictable schedule: one instalment every weekday, a single speaker in continuous prose rather
than an interview, always the same recording conditions. For a corpus that needs *register and
lexicon* — how Andorrans actually speak, which words they reach for — that regularity is worth
more than a larger pile of mixed material.

**Three things about the source, verified 2026-08-02.**

* ``rtva.ad/robots.txt`` allows everything except ``/admin/``, ``/mobile/`` and **``/api/``**. So
  this uses the public programme pages and the sitemap, and never the site's API. That is not a
  technicality: the API would have been the obvious way to enumerate episodes.
* The MP3 lives on a separate CDN host and its path contains an opaque per-episode hash
  (``…/audio/2026/03/31/69cb7d35/…mp3``). URLs cannot be constructed from a date; the episode page
  has to be read. :func:`audio_url` does that.
* The sitemap is the only complete index. Browsing the programme's own pages gives the recent
  ones; the sitemap gave **151** editorials in one fetch, which is both more polite and more
  complete.

**Licence is not negotiable and is not decided here.** Everything from RTVA is stamped
``no-redistribute`` by :mod:`maia.scraping.radio`, which has no parameter to override it. The audio
and its transcript are grounding and register only: they feed the RAG index and ground generated
examples, and only paraphrased knowledge ever reaches a public artifact. D7 applies too — this is
one identifiable person speaking, and the subcorpus exists for how Andorran Catalan sounds, never
to reproduce his voice or his opinions.

Transcription itself stays **blocked-by-resource**: ``whisper-large-v3-ca`` needs a GPU, and no
transcription service is configured. :class:`~maia.scraping.radio.Transcriber` is the seam that
already exists; this module stops at audio on disk plus a manifest that names what to transcribe.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from maia.scraping.http import PoliteFetcher
from maia.scraping.radio import ProgrammeSpec

#: The sitemap index. Four gzipped sub-sitemaps, ~165k URLs, one polite fetch each.
SITEMAP = "https://www.rtva.ad/sitemap/sitemap.xml"

#: The programme, as RTVA slugs it.
PROGRAMME = "Avui serà un bon dia"

#: Episode pages are ``…/programes/l-editorial-avui-sera-un-bon-dia-DD-MM-YYYY``, sometimes with a
#: ``-0``/``-2`` suffix when the same date was published twice. The date is the useful part: it is
#: the only per-episode metadata available without fetching the page.
EPISODE_URL = re.compile(
    r"https://www\.rtva\.ad/ca/programes/l-editorial-avui-sera-un-bon-dia-"
    r"(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})(?:-\d+)?/?$"
)

_LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")

#: The audio on the CDN. Matched loosely on purpose: the host and the path scheme are RTVA's to
#: change, and the one stable fact is that the page links an mp3.
_AUDIO = re.compile(r"https?://[^\"'\s]+\.mp3(?:\?[^\"'\s]*)?")


@dataclass(frozen=True)
class Episode:
    """One published instalment of the editorial."""

    url: str
    broadcast: date

    @property
    def slug(self) -> str:
        """``2026-03-31``. The filename stem, so a directory listing sorts chronologically."""
        return self.broadcast.isoformat()

    def spec(self) -> ProgrammeSpec:
        """§3.1 provenance for the documents this episode will eventually produce."""
        return ProgrammeSpec(programme=PROGRAMME, url=self.url, topic=("editorial", "actualitat"))


def find_episodes(sitemap_xml: str) -> list[Episode]:
    """Episodes named in one sitemap, newest last, deduplicated by broadcast date.

    A date published twice (the ``-0`` suffix) is kept once: the second upload is the same
    editorial, and two copies in the corpus is duplicated training data that no downstream
    deduplication would catch, because the *audio* differs even when the words do not.
    """
    by_date: dict[date, Episode] = {}
    for url in _LOC.findall(sitemap_xml):
        match = EPISODE_URL.match(url.strip())
        if not match:
            continue
        broadcast = date(int(match["year"]), int(match["month"]), int(match["day"]))
        by_date.setdefault(broadcast, Episode(url=url.strip(), broadcast=broadcast))
    return [by_date[key] for key in sorted(by_date)]


def sitemap_parts(index_xml: str) -> list[str]:
    """The sub-sitemap URLs listed in a sitemap index."""
    return [url for url in (u.strip() for u in _LOC.findall(index_xml)) if "sitemap" in url]


def read_sitemap(fetcher: PoliteFetcher, url: str) -> str:
    """Fetch a sitemap, transparently decompressing ``.xml.gz``.

    Returns an empty string when the fetch fails or the body is not readable as XML: a sitemap is
    an index, and one unavailable part must not end a discovery run over the other three.
    """
    payload = fetcher.fetch_bytes(url)
    if not payload:
        return ""
    if payload[:2] == b"\x1f\x8b":  # gzip magic
        try:
            payload = gzip.decompress(payload)
        except (OSError, EOFError):
            return ""
    return payload.decode("utf-8", errors="replace")


def discover(fetcher: PoliteFetcher, *, sitemap: str = SITEMAP) -> list[Episode]:
    """Every editorial RTVA's sitemap knows about."""
    index = read_sitemap(fetcher, sitemap)
    episodes: dict[date, Episode] = {}
    for part in sitemap_parts(index):
        for episode in find_episodes(read_sitemap(fetcher, part)):
            episodes.setdefault(episode.broadcast, episode)
    return [episodes[key] for key in sorted(episodes)]


def audio_url(page_html: str) -> str | None:
    """The MP3 linked from an episode page, or ``None`` if the page has none.

    The trailing ``?t=`` RTVA appends is stripped: it is an empty cache-buster, and leaving it on
    makes two URLs for one file, which defeats the on-disk cache.
    """
    match = _AUDIO.search(page_html)
    if not match:
        return None
    return match.group(0).split("?", 1)[0]


@dataclass(frozen=True)
class Downloaded:
    """One episode's audio on disk, and where it came from."""

    episode: Episode
    path: Path
    audio_url: str
    bytes_written: int

    def manifest_entry(self) -> dict[str, object]:
        """The record the transcription pass reads.

        Provenance travels with the audio rather than being recoverable from the filename,
        because a filename is the first thing to be renamed.
        """
        return {
            "broadcast": self.episode.broadcast.isoformat(),
            "programme": PROGRAMME,
            "page_url": self.episode.url,
            "audio_url": self.audio_url,
            "path": self.path.name,
            "bytes": self.bytes_written,
            "licence": "no-redistribute",
        }


def download(
    fetcher: PoliteFetcher, episode: Episode, destination: Path, *, overwrite: bool = False
) -> Downloaded | None:
    """Fetch one episode's audio into ``destination``.

    Returns ``None`` — rather than raising — when the page is unreachable, links no audio, or the
    audio itself cannot be fetched: a run over a year of daily episodes must survive a gap.

    Existing files are skipped unless ``overwrite``, so an interrupted run resumes rather than
    re-downloading hundreds of megabytes.
    """
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / f"{episode.slug}.mp3"

    page = fetcher.fetch(episode.url)
    if page is None:
        return None
    url = audio_url(page)
    if url is None:
        return None

    if path.is_file() and not overwrite:
        return Downloaded(episode, path, url, path.stat().st_size)

    payload = fetcher.fetch_bytes(url)
    if not payload:
        return None
    path.write_bytes(payload)
    return Downloaded(episode, path, url, len(payload))


def write_manifest(downloads: Iterable[Downloaded], path: Path) -> int:
    """Write the transcription manifest as JSONL. Returns how many entries were written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for item in downloads:
            handle.write(json.dumps(item.manifest_entry(), ensure_ascii=False))
            handle.write("\n")
            count += 1
    return count


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point: discover episodes and download their audio.

    Transcription is a separate pass and needs a GPU; this one only needs the network, so it runs
    for real. ``--dry-run`` lists what it found without downloading anything.
    """
    from maia.scraping.http import polite_fetcher

    parser = argparse.ArgumentParser(
        description=f"Acquire the daily editorial of «{PROGRAMME}» from RTVA (M1.13). Audio is "
        "no-redistribute: grounding and register only, never republished. Respects robots.txt "
        "(which disallows /api/, so this uses the sitemap and the public pages)."
    )
    parser.add_argument("--out", type=Path, default=Path("data/rtva/editorial"))
    parser.add_argument("--manifest", type=Path, help="write the transcription manifest here")
    parser.add_argument("--cache", type=Path, help="cache directory for fetched pages")
    parser.add_argument("--since", help="only episodes broadcast on or after YYYY-MM-DD")
    parser.add_argument("--limit", type=int, help="at most this many episodes (newest first)")
    parser.add_argument("--min-interval", type=float, default=2.0, help="seconds between requests")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="list episodes, download nothing")
    args = parser.parse_args(argv)

    since: date | None = None
    if args.since:
        try:
            since = date.fromisoformat(args.since)
        except ValueError:
            print(f"error: --since must be YYYY-MM-DD, got {args.since!r}", file=sys.stderr)
            return 1

    fetcher = polite_fetcher(min_interval=args.min_interval, cache_dir=args.cache)
    episodes = discover(fetcher)
    if since is not None:
        episodes = [e for e in episodes if e.broadcast >= since]
    if args.limit:
        episodes = episodes[-args.limit :]

    if not episodes:
        print("no episodes found: the sitemap or the URL pattern has changed", file=sys.stderr)
        return 1
    print(f"{len(episodes)} episode(s), {episodes[0].slug} to {episodes[-1].slug}")

    if args.dry_run:
        for episode in episodes:
            print(f"  {episode.slug}  {episode.url}")
        return 0

    downloads: list[Downloaded] = []
    for episode in episodes:
        result = download(fetcher, episode, args.out, overwrite=args.overwrite)
        if result is None:
            print(f"  {episode.slug}: no audio", file=sys.stderr)
            continue
        downloads.append(result)
        print(f"  {episode.slug}: {result.bytes_written:,} bytes")

    total = sum(item.bytes_written for item in downloads)
    print(f"{len(downloads)}/{len(episodes)} downloaded, {total:,} bytes")
    if args.manifest:
        print(f"wrote {write_manifest(downloads, args.manifest)} manifest entries")
    if fetcher.disallowed:
        print(f"robots.txt disallowed {len(fetcher.disallowed)} URL(s)", file=sys.stderr)
    return 0 if downloads else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
