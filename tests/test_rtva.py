"""Tests for RTVA audio acquisition (PLAN M1.13).

Fixtures are cut from the live site, fetched 2026-08-02.
"""

from __future__ import annotations

import gzip
import json
from datetime import date
from pathlib import Path

import pytest

from maia.scraping.rtva import (
    PROGRAMME,
    SITEMAP,
    Downloaded,
    Episode,
    audio_url,
    discover,
    download,
    find_episodes,
    main,
    read_sitemap,
    sitemap_parts,
    write_manifest,
)

BASE = "https://www.rtva.ad/ca/programes/l-editorial-avui-sera-un-bon-dia"
CDN = "https://mediaverse.rtva.hiway.media/audio/2026/03/31/69cb7d35"

SITEMAP_INDEX = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex><sitemap><loc>https://www.rtva.ad/sitemap/sitemap1.xml.gz</loc></sitemap>
<sitemap><loc>https://www.rtva.ad/sitemap/sitemap2.xml.gz</loc></sitemap></sitemapindex>
"""

# Includes the two shapes that must not be mistaken for episodes: a different programme, and a
# news item that merely mentions the show.
SITEMAP_PART = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset>
  <url><loc>{BASE}-31-03-2026</loc></url>
  <url><loc>{BASE}-01-04-2026</loc></url>
  <url><loc>{BASE}-25-03-2026</loc></url>
  <url><loc>https://www.rtva.ad/ca/programes/avui-fem-el-cafe-amb-jordi-jordana-avui-sera-un-bon-dia-05-06-2025</loc></url>
  <url><loc>https://www.rtva.ad/ca/noticies/societat/campanya-especial-avui-sera-bon-dia</loc></url>
</urlset>
"""

EPISODE_HTML = f"""
<html><body>
  <video-js data-setup='{{}}'>
    <source src="{CDN}/20260331-EDITORIAL---20260331-EDITORIAL---.mp3?t=" type="audio/mpeg">
  </video-js>
  <a href="https://vodov.rtva.hiway.media/vod/1601752/hls/manifest.m3u8?t=">hls</a>
</body></html>
"""


class FakeFetcher:
    def __init__(self, pages: dict[str, str], blobs: dict[str, bytes] | None = None) -> None:
        self.pages = pages
        self.blobs = blobs or {}
        self.disallowed: list[str] = []
        self.requested: list[str] = []

    def fetch(self, url: str) -> str | None:
        self.requested.append(url)
        return self.pages.get(url)

    def fetch_bytes(self, url: str) -> bytes | None:
        self.requested.append(url)
        return self.blobs.get(url)


# ── discovery ────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_episodes_are_found_and_dated_from_their_url() -> None:
    """The broadcast date is the only per-episode metadata available without fetching the page,
    and it is what makes the corpus sortable and resumable."""
    episodes = find_episodes(SITEMAP_PART)
    assert [e.broadcast for e in episodes] == [
        date(2026, 3, 25),
        date(2026, 3, 31),
        date(2026, 4, 1),
    ]
    assert episodes[0].slug == "2026-03-25"


@pytest.mark.unit
def test_another_segment_of_the_same_programme_is_not_the_editorial() -> None:
    """`avui-fem-el-cafe-…-avui-sera-un-bon-dia-05-06-2025` is an interview from the same show. A
    looser pattern would quietly fold interviews into a single-speaker corpus."""
    urls = [e.url for e in find_episodes(SITEMAP_PART)]
    assert not any("avui-fem-el-cafe" in url for url in urls)
    assert not any("noticies" in url for url in urls)


@pytest.mark.unit
def test_a_date_published_twice_is_kept_once() -> None:
    """RTVA re-uploads with a `-0` suffix. Two copies of one editorial is duplicated training data
    that no downstream deduplication catches, because the audio differs even when the words do
    not."""
    xml = f"<urlset><url><loc>{BASE}-04-06-2025</loc></url>"
    xml += f"<url><loc>{BASE}-04-06-2025-0</loc></url></urlset>"
    episodes = find_episodes(xml)
    assert len(episodes) == 1
    assert episodes[0].url.endswith("04-06-2025")


@pytest.mark.unit
def test_sitemap_parts_are_read_from_the_index() -> None:
    assert sitemap_parts(SITEMAP_INDEX) == [
        "https://www.rtva.ad/sitemap/sitemap1.xml.gz",
        "https://www.rtva.ad/sitemap/sitemap2.xml.gz",
    ]


@pytest.mark.unit
def test_a_gzipped_sitemap_is_decompressed() -> None:
    fetcher = FakeFetcher({}, {"https://x/s.xml.gz": gzip.compress(SITEMAP_PART.encode("utf-8"))})
    assert "l-editorial" in read_sitemap(fetcher, "https://x/s.xml.gz")  # type: ignore[arg-type]


@pytest.mark.unit
def test_an_unavailable_or_corrupt_sitemap_part_does_not_end_discovery() -> None:
    """A sitemap is an index; one bad part must not lose the other three."""
    fetcher = FakeFetcher({}, {"https://x/bad.gz": b"\x1f\x8b not really gzip"})
    assert read_sitemap(fetcher, "https://x/bad.gz") == ""  # type: ignore[arg-type]
    assert read_sitemap(fetcher, "https://x/missing.gz") == ""  # type: ignore[arg-type]


@pytest.mark.unit
def test_discover_walks_the_index_and_merges_the_parts() -> None:
    fetcher = FakeFetcher(
        {},
        {
            SITEMAP: SITEMAP_INDEX.encode("utf-8"),
            "https://www.rtva.ad/sitemap/sitemap1.xml.gz": gzip.compress(
                SITEMAP_PART.encode("utf-8")
            ),
            "https://www.rtva.ad/sitemap/sitemap2.xml.gz": gzip.compress(
                f"<urlset><url><loc>{BASE}-02-04-2026</loc></url></urlset>".encode()
            ),
        },
    )
    episodes = discover(fetcher)  # type: ignore[arg-type]
    assert [e.slug for e in episodes] == ["2026-03-25", "2026-03-31", "2026-04-01", "2026-04-02"]


# ── the audio URL ────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_mp3_is_found_and_its_empty_cache_buster_stripped() -> None:
    """RTVA appends `?t=` with nothing after it. Left on, one file has two URLs and the on-disk
    cache stops working."""
    found = audio_url(EPISODE_HTML)
    assert found == f"{CDN}/20260331-EDITORIAL---20260331-EDITORIAL---.mp3"
    assert "?" not in (found or "")


@pytest.mark.unit
def test_the_hls_stream_is_not_mistaken_for_the_download() -> None:
    """The page also links an m3u8 manifest, which is not a file this pipeline can store."""
    assert ".m3u8" not in (audio_url(EPISODE_HTML) or "")


@pytest.mark.unit
def test_a_page_with_no_audio_returns_none() -> None:
    assert audio_url("<html><body>no media here</body></html>") is None


# ── downloading ──────────────────────────────────────────────────────────────


def _episode() -> Episode:
    return Episode(url=f"{BASE}-31-03-2026", broadcast=date(2026, 3, 31))


def _fetcher(audio: bytes = b"ID3\x04\x00fake mp3") -> FakeFetcher:
    return FakeFetcher(
        {f"{BASE}-31-03-2026": EPISODE_HTML},
        {f"{CDN}/20260331-EDITORIAL---20260331-EDITORIAL---.mp3": audio},
    )


@pytest.mark.unit
def test_audio_lands_under_its_broadcast_date(tmp_path: Path) -> None:
    """Named by date so a directory listing sorts chronologically and a resumed run can tell at a
    glance what it already has."""
    result = download(_fetcher(), _episode(), tmp_path)  # type: ignore[arg-type]
    assert result is not None
    assert result.path == tmp_path / "2026-03-31.mp3"
    assert result.path.read_bytes().startswith(b"ID3")
    assert result.bytes_written == len(b"ID3\x04\x00fake mp3")


@pytest.mark.unit
def test_an_existing_file_is_not_downloaded_again(tmp_path: Path) -> None:
    """An interrupted run over a year of daily episodes must resume, not re-fetch hundreds of
    megabytes."""
    fetcher = _fetcher()
    download(fetcher, _episode(), tmp_path)  # type: ignore[arg-type]
    before = list(fetcher.requested)

    again = download(fetcher, _episode(), tmp_path)  # type: ignore[arg-type]
    assert again is not None
    # The page is re-read (it is cheap and cached); the audio is not re-fetched.
    assert fetcher.requested[len(before) :] == [_episode().url]

    forced = download(fetcher, _episode(), tmp_path, overwrite=True)  # type: ignore[arg-type]
    assert forced is not None
    assert fetcher.requested[-1].endswith(".mp3")


@pytest.mark.unit
def test_a_gap_in_the_archive_does_not_stop_the_run(tmp_path: Path) -> None:
    """Unreachable page, page without audio, audio that will not fetch: all skipped, none fatal."""
    assert download(FakeFetcher({}), _episode(), tmp_path) is None  # type: ignore[arg-type]

    no_audio = FakeFetcher({f"{BASE}-31-03-2026": "<html>nothing</html>"})
    assert download(no_audio, _episode(), tmp_path) is None  # type: ignore[arg-type]

    assert download(_fetcher(audio=b""), _episode(), tmp_path) is None  # type: ignore[arg-type]
    assert list(tmp_path.iterdir()) == []


# ── the manifest ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_manifest_carries_provenance_and_the_licence(tmp_path: Path) -> None:
    """Transcription is a separate pass on a GPU that does not exist yet, so what it needs has to
    travel with the audio — including the licence, which is the one fact that must not be lost
    between the download and whatever is eventually built from it."""
    result = download(_fetcher(), _episode(), tmp_path)  # type: ignore[arg-type]
    assert result is not None
    path = tmp_path / "manifest.jsonl"
    assert write_manifest([result], path) == 1

    entry = json.loads(path.read_text(encoding="utf-8").strip())
    assert entry["licence"] == "no-redistribute"
    assert entry["broadcast"] == "2026-03-31"
    assert entry["programme"] == PROGRAMME
    assert entry["page_url"] == _episode().url
    assert entry["audio_url"].endswith(".mp3")
    assert entry["path"] == "2026-03-31.mp3"


@pytest.mark.unit
def test_the_episode_spec_is_the_one_radio_expects() -> None:
    """`ProgrammeSpec` is what M1.13's transcription pipeline consumes; provenance is the page URL
    because §3.1 has no broadcast-date field."""
    spec = _episode().spec()
    assert spec.programme == PROGRAMME
    assert spec.url == _episode().url
    assert "editorial" in spec.topic


@pytest.mark.unit
def test_a_downloaded_entry_reports_what_was_written(tmp_path: Path) -> None:
    item = Downloaded(_episode(), tmp_path / "x.mp3", "https://cdn/x.mp3", 1234)
    assert item.manifest_entry()["bytes"] == 1234


# ── the CLI ──────────────────────────────────────────────────────────────────


def _wire(monkeypatch: pytest.MonkeyPatch, fetcher: FakeFetcher) -> None:
    monkeypatch.setattr("maia.scraping.http.polite_fetcher", lambda **kwargs: fetcher)


def _full_fetcher(audio: bytes = b"ID3\x04\x00audio") -> FakeFetcher:
    pages = {f"{BASE}-{d}": EPISODE_HTML for d in ("25-03-2026", "31-03-2026", "01-04-2026")}
    return FakeFetcher(
        pages,
        {
            SITEMAP: SITEMAP_INDEX.encode("utf-8"),
            "https://www.rtva.ad/sitemap/sitemap1.xml.gz": gzip.compress(
                SITEMAP_PART.encode("utf-8")
            ),
            "https://www.rtva.ad/sitemap/sitemap2.xml.gz": b"",
            f"{CDN}/20260331-EDITORIAL---20260331-EDITORIAL---.mp3": audio,
        },
    )


@pytest.mark.unit
def test_the_cli_downloads_and_writes_a_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _wire(monkeypatch, _full_fetcher())
    manifest = tmp_path / "manifest.jsonl"
    code = main(["--out", str(tmp_path / "audio"), "--manifest", str(manifest)])
    assert code == 0

    out = capsys.readouterr().out
    assert "3 episode(s)" in out
    assert "3 manifest entries" in out
    assert len(list((tmp_path / "audio").glob("*.mp3"))) == 3


@pytest.mark.unit
def test_the_cli_can_list_without_downloading(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fetcher = _full_fetcher()
    _wire(monkeypatch, fetcher)
    assert main(["--dry-run", "--out", str(tmp_path)]) == 0
    assert not any(tmp_path.glob("*.mp3"))
    assert not any(url.endswith(".mp3") for url in fetcher.requested)


@pytest.mark.unit
def test_since_and_limit_narrow_the_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _wire(monkeypatch, _full_fetcher())
    assert main(["--dry-run", "--since", "2026-03-31", "--out", str(tmp_path)]) == 0
    listed = capsys.readouterr().out
    assert "2026-03-25" not in listed
    assert "2026-03-31" in listed

    _wire(monkeypatch, _full_fetcher())
    assert main(["--dry-run", "--limit", "1", "--out", str(tmp_path)]) == 0
    assert "1 episode(s)" in capsys.readouterr().out


@pytest.mark.unit
def test_a_bad_since_is_rejected_before_any_fetching(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["--since", "last tuesday", "--out", str(tmp_path)]) == 1
    assert "YYYY-MM-DD" in capsys.readouterr().err


@pytest.mark.unit
def test_finding_no_episodes_is_an_error_not_an_empty_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Zero episodes means the sitemap moved or the URL pattern changed — never that RTVA stopped
    broadcasting. A zero exit would let a broken scraper run nightly and report nothing wrong."""
    _wire(monkeypatch, FakeFetcher({}, {SITEMAP: b"<sitemapindex></sitemapindex>"}))
    assert main(["--out", str(tmp_path)]) == 1
    assert "has changed" in capsys.readouterr().err


@pytest.mark.unit
def test_a_run_where_every_download_failed_exits_non_zero(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fetcher = _full_fetcher(audio=b"")
    fetcher.disallowed.append("https://www.rtva.ad/api/blocked")
    _wire(monkeypatch, fetcher)
    assert main(["--out", str(tmp_path)]) == 1
    err = capsys.readouterr().err
    assert "no audio" in err
    assert "robots.txt disallowed 1 URL(s)" in err
