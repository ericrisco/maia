"""Tests for polite fetching: robots.txt, cache, rate limit (PLAN M1 step 1)."""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

import pytest

from maia.scraping.http import (
    PoliteFetcher,
    RobotsCache,
    RobotsPolicy,
    polite_fetcher,
    requests_fetch,
    requests_fetch_bytes,
    robots_url_for,
)

ROBOTS = """
User-agent: *
Disallow: /private/
"""


class _Clock:
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t


class _Recorder:
    """A fake network fetch that records calls and returns a fixed body (or None)."""

    def __init__(self, body: str | None = "<html>hola</html>") -> None:
        self.body = body
        self.calls: list[str] = []

    def __call__(self, url: str) -> str | None:
        self.calls.append(url)
        return self.body


@pytest.mark.unit
def test_robots_policy_from_text() -> None:
    policy = RobotsPolicy.from_text(ROBOTS)
    assert policy.can_fetch("https://govern.ad/public/page")
    assert not policy.can_fetch("https://govern.ad/private/secret")


@pytest.mark.unit
def test_robots_policy_allow_all() -> None:
    assert RobotsPolicy.allow_all().can_fetch("https://anything.ad/private/x")


@pytest.mark.unit
def test_disallowed_url_is_skipped_and_recorded() -> None:
    net = _Recorder()
    fetcher = PoliteFetcher(net, RobotsPolicy.from_text(ROBOTS))
    assert fetcher.fetch("https://govern.ad/private/x") is None
    assert fetcher.disallowed == ["https://govern.ad/private/x"]
    assert net.calls == []  # never hit the network


@pytest.mark.unit
def test_none_from_network_returns_none() -> None:
    fetcher = PoliteFetcher(_Recorder(body=None))
    assert fetcher.fetch("https://govern.ad/x") is None


@pytest.mark.unit
def test_cache_hit_bypasses_network_and_throttle(tmp_path: Path) -> None:
    net = _Recorder()
    slept: list[float] = []
    fetcher = PoliteFetcher(net, cache_dir=tmp_path, sleep=slept.append)
    first = fetcher.fetch("https://govern.ad/a")
    second = fetcher.fetch("https://govern.ad/a")
    assert first == second == "<html>hola</html>"
    assert net.calls == ["https://govern.ad/a"]  # second served from cache
    assert slept == []


@pytest.mark.unit
def test_rate_limit_sleeps_between_network_fetches() -> None:
    slept: list[float] = []
    clock = _Clock()

    def sleep(seconds: float) -> None:
        slept.append(seconds)
        clock.t += seconds

    fetcher = PoliteFetcher(_Recorder(), min_interval=1.0, sleep=sleep, clock=clock)
    fetcher.fetch("https://govern.ad/a")
    fetcher.fetch("https://govern.ad/b")
    assert slept == [1.0]  # throttled the immediate second fetch


@pytest.mark.unit
def test_cache_file_is_written(tmp_path: Path) -> None:
    fetcher = PoliteFetcher(_Recorder(), cache_dir=tmp_path)
    fetcher.fetch("https://govern.ad/a")
    assert list(tmp_path.glob("*.html"))


@pytest.mark.unit
def test_no_sleep_when_enough_time_elapsed() -> None:
    slept: list[float] = []
    clock = _Clock()
    fetcher = PoliteFetcher(_Recorder(), min_interval=1.0, sleep=slept.append, clock=clock)
    fetcher.fetch("https://govern.ad/a")
    clock.t = 5.0  # plenty of time passed before the next fetch
    fetcher.fetch("https://govern.ad/b")
    assert slept == []


@pytest.mark.unit
def test_requests_fetch_status_handling(monkeypatch: pytest.MonkeyPatch) -> None:
    import requests

    from maia.scraping.http import requests_fetch

    class _Resp:
        def __init__(self, status_code: int, text: str) -> None:
            self.status_code = status_code
            self.text = text

    calls: list[dict[str, object]] = []

    def fake_get(url: str, **kwargs: object) -> _Resp:
        calls.append({"url": url, **kwargs})
        return _Resp(200, "<html>ok</html>") if "ok" in url else _Resp(404, "nope")

    monkeypatch.setattr(requests, "get", fake_get)
    assert requests_fetch("https://govern.ad/ok") == "<html>ok</html>"
    assert requests_fetch("https://govern.ad/missing") is None
    headers = calls[0]["headers"]
    assert isinstance(headers, dict) and "maia-corpus-bot" in headers["User-Agent"]


# ─────────────────────────────────────────────────────────────
# robots.txt is actually retrieved (it previously never was)
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_robots_url_is_derived_from_the_origin() -> None:
    assert robots_url_for("https://www.govern.ad/a/b?x=1#f") == "https://www.govern.ad/robots.txt"
    assert robots_url_for("http://bopa.ad:8080/x") == "http://bopa.ad:8080/robots.txt"


@pytest.mark.unit
def test_the_cache_fetches_robots_and_applies_it() -> None:
    """The gap an adversarial review found.

    Before `RobotsCache`, `PoliteFetcher` defaulted to `allow_all()` and **nothing in the
    codebase ever requested a robots.txt** — so the live wiring obeyed a policy it had never
    read, while several modules claimed robots.txt was respected without exception.
    """
    served = {"https://www.govern.ad/robots.txt": "User-agent: *\nDisallow: /privat/\n"}
    requested: list[str] = []

    def fetch(url: str) -> str | None:
        requested.append(url)
        return served.get(url)

    cache = RobotsCache(fetch)
    assert cache.can_fetch("https://www.govern.ad/public")
    assert not cache.can_fetch("https://www.govern.ad/privat/x")
    assert requested == ["https://www.govern.ad/robots.txt"]


@pytest.mark.unit
def test_robots_is_fetched_once_per_origin() -> None:
    requested: list[str] = []

    def fetch(url: str) -> str | None:
        requested.append(url)
        return "User-agent: *\nDisallow:\n"

    cache = RobotsCache(fetch)
    for path in ("a", "b", "c"):
        cache.can_fetch(f"https://www.govern.ad/{path}")
    cache.can_fetch("https://www.cultura.ad/x")
    assert requested == [
        "https://www.govern.ad/robots.txt",
        "https://www.cultura.ad/robots.txt",
    ]


@pytest.mark.unit
def test_an_unreachable_robots_is_permissive_and_recorded() -> None:
    # HTTP 404 for robots.txt conventionally means "no rules", but it is still worth an audit
    # trail: a site that 500s on robots.txt looks identical to one that has none.
    cache = RobotsCache(lambda _url: None)
    assert cache.can_fetch("https://www.govern.ad/x")
    assert cache.unreachable == ["www.govern.ad"]


@pytest.mark.unit
def test_a_caller_can_refuse_an_origin_whose_rules_are_unreadable() -> None:
    strict = RobotsCache(lambda _url: None, allow_on_error=False)
    assert not strict.can_fetch("https://www.govern.ad/x")


@pytest.mark.unit
def test_polite_fetcher_wires_robots_to_the_same_transport() -> None:
    served = {
        "https://www.govern.ad/robots.txt": "User-agent: *\nDisallow: /privat/\n",
        "https://www.govern.ad/public": "<html>ok</html>",
    }
    fetcher = polite_fetcher(lambda url: served.get(url), min_interval=0.0)
    assert fetcher.fetch("https://www.govern.ad/public") == "<html>ok</html>"
    assert fetcher.fetch("https://www.govern.ad/privat/y") is None
    assert fetcher.disallowed == ["https://www.govern.ad/privat/y"]


# ── binary fetching (PDFs, audio) ────────────────────────────────────────────


@pytest.mark.unit
def test_fetch_bytes_honours_robots_the_rate_limit_and_the_cache(tmp_path: Path) -> None:
    """The binary path is a second code path through the same rules, and a second code path that
    skipped any of them is the one nobody remembers to audit."""
    calls: list[str] = []
    waits: list[float] = []
    fetcher = PoliteFetcher(
        lambda url: None,
        RobotsPolicy.from_text("User-agent: *\nDisallow: /private/\n"),
        min_interval=5.0,
        cache_dir=tmp_path,
        sleep=waits.append,
        clock=iter([0.0, 0.0, 1.0, 1.0]).__next__,
        fetch_bytes_fn=_recording(calls, b"%PDF-1.4 ..."),
    )

    assert fetcher.fetch_bytes("https://x.ad/a.pdf") == b"%PDF-1.4 ..."
    assert fetcher.fetch_bytes("https://x.ad/private/secret.pdf") is None
    assert fetcher.disallowed == ["https://x.ad/private/secret.pdf"]
    # Second call to the same URL is served from disk: no network, no wait.
    assert fetcher.fetch_bytes("https://x.ad/a.pdf") == b"%PDF-1.4 ..."
    assert calls == ["https://x.ad/a.pdf"]


@pytest.mark.unit
def test_fetch_bytes_caches_under_its_own_extension(tmp_path: Path) -> None:
    """A PDF written into the HTML cache slot would be read back as text by `fetch`."""
    fetcher = PoliteFetcher(
        lambda url: "<html>page</html>",
        cache_dir=tmp_path,
        fetch_bytes_fn=lambda url: b"\x89PDF-binary\xff",
    )
    url = "https://x.ad/thing"
    assert fetcher.fetch_bytes(url) == b"\x89PDF-binary\xff"
    assert fetcher.fetch(url) == "<html>page</html>"
    assert {p.suffix for p in tmp_path.iterdir()} == {".bin", ".html"}


@pytest.mark.unit
def test_an_empty_body_is_not_cached_as_a_success(tmp_path: Path) -> None:
    fetcher = PoliteFetcher(lambda url: None, cache_dir=tmp_path, fetch_bytes_fn=lambda url: b"")
    assert fetcher.fetch_bytes("https://x.ad/empty.pdf") is None
    assert list(tmp_path.iterdir()) == []


@pytest.mark.unit
def test_a_fetcher_with_no_binary_transport_says_so_instead_of_decoding_a_pdf() -> None:
    """Falling back to the text transport would return a PDF decoded as UTF-8: silent corruption
    that only surfaces as a broken corpus much later."""
    with pytest.raises(RuntimeError, match="no binary transport"):
        PoliteFetcher(lambda url: "text").fetch_bytes("https://x.ad/a.pdf")


# ── the transports never raise ───────────────────────────────────────────────


def _recording(calls: list[str], payload: bytes) -> Callable[[str], bytes]:
    """A binary transport that records the URLs it was asked for."""

    def _fetch(url: str) -> bytes:
        calls.append(url)
        return payload

    return _fetch


class FakeRequestError(Exception):
    """Stands in for `requests.RequestException`, which every real transport error derives from."""


def _fake_requests(monkeypatch: pytest.MonkeyPatch, responses: list[object]) -> list[str]:
    """Install a stand-in `requests` whose GET replays ``responses``.

    A `FakeRequestException` in the list is raised, mirroring `requests.exceptions.ReadTimeout`:
    it must inherit from the module's `RequestException`, or the test would exercise a different
    except clause than production does.
    """
    import types

    seen: list[str] = []
    queue = list(responses)

    def _get(url: str, **kwargs: object) -> object:
        seen.append(url)
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    module = types.ModuleType("requests")
    module.get = _get  # type: ignore[attr-defined]
    module.RequestException = FakeRequestError  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "requests", module)
    return seen


class _Response:
    def __init__(self, status: int = 200, text: str = "ok", content: bytes = b"ok") -> None:
        self.status_code = status
        self.text = text
        self.content = content


@pytest.mark.unit
def test_a_read_timeout_returns_none_instead_of_killing_the_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Learned the hard way: one read timeout 90 sessions into an acquisition propagated out of
    the transport and ended the whole run, discarding every document already collected."""
    seen = _fake_requests(monkeypatch, [FakeRequestError("read timed out")] * 3)
    waits: list[float] = []
    assert requests_fetch("https://x.ad/a", sleep=waits.append) is None
    assert len(seen) == 3  # the original try plus DEFAULT_RETRIES
    assert waits == [1.0, 2.0]  # linear backoff


@pytest.mark.unit
def test_a_transient_failure_is_retried_and_then_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _fake_requests(monkeypatch, [FakeRequestError("blip"), _Response(text="recovered")])
    assert requests_fetch("https://x.ad/a", sleep=lambda _: None) == "recovered"


@pytest.mark.unit
def test_an_http_error_is_not_retried(monkeypatch: pytest.MonkeyPatch) -> None:
    """A 404 on a session that was never published will still be a 404 in two seconds; retrying a
    considered answer from the server only makes a broken run slower."""
    seen = _fake_requests(monkeypatch, [_Response(status=404)])
    assert requests_fetch("https://x.ad/missing", sleep=lambda _: None) is None
    assert len(seen) == 1


@pytest.mark.unit
def test_the_binary_transport_has_the_same_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    _fake_requests(monkeypatch, [_Response(content=b"%PDF")])
    assert requests_fetch_bytes("https://x.ad/a.pdf", sleep=lambda _: None) == b"%PDF"

    _fake_requests(monkeypatch, [FakeRequestError("x")] * 3)
    assert requests_fetch_bytes("https://x.ad/a.pdf", sleep=lambda _: None) is None

    _fake_requests(monkeypatch, [_Response(status=500)])
    assert requests_fetch_bytes("https://x.ad/a.pdf", sleep=lambda _: None) is None


@pytest.mark.unit
def test_polite_fetcher_wires_a_binary_transport_by_default() -> None:
    """Otherwise every caller would have to remember to pass one, and the one who forgets gets a
    RuntimeError in the middle of a long run."""
    fetcher = polite_fetcher(lambda url: None, bytes_fn=lambda url: b"x")
    assert fetcher.fetch_bytes("https://x.ad/a") == b"x"
