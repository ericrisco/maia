"""Tests for polite fetching: robots.txt, cache, rate limit (PLAN M1 step 1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from maia.scraping.http import PoliteFetcher, RobotsPolicy

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
