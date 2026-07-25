"""Polite HTTP fetching for scrapers — PLAN M1 step 1.

Respects ``robots.txt``, rate-limits to ≤1 request/second, and caches raw HTML so a
re-run is idempotent (and offline). The network call itself is an injected seam
(``fetch_fn``) so the polite-fetch orchestration is fully testable without a network:
production wires :func:`requests_fetch`, tests pass a fixture-backed callable.
"""

from __future__ import annotations

import hashlib
import time
from collections.abc import Callable
from pathlib import Path
from urllib.robotparser import RobotFileParser

#: Identifies the crawler to servers and in robots.txt matching.
DEFAULT_USER_AGENT = "maia-corpus-bot/0.1 (+https://github.com/ericrisco/maia)"

#: A callable that performs the actual network GET and returns the response body (or None).
FetchFn = Callable[[str], str | None]


class RobotsPolicy:
    """robots.txt decision for a single user-agent.

    Build from fetched robots.txt text (:meth:`from_text`) or use :meth:`allow_all` when a
    site has no robots.txt (the standard permissive default).
    """

    def __init__(self, parser: RobotFileParser | None, user_agent: str) -> None:
        self._parser = parser
        self._user_agent = user_agent

    @classmethod
    def from_text(cls, text: str, *, user_agent: str = DEFAULT_USER_AGENT) -> RobotsPolicy:
        parser = RobotFileParser()
        parser.parse(text.splitlines())
        return cls(parser, user_agent)

    @classmethod
    def allow_all(cls, *, user_agent: str = DEFAULT_USER_AGENT) -> RobotsPolicy:
        return cls(None, user_agent)

    def can_fetch(self, url: str) -> bool:
        if self._parser is None:
            return True
        return self._parser.can_fetch(self._user_agent, url)


class PoliteFetcher:
    """Fetch URLs respecting robots.txt, a rate limit, and an on-disk HTML cache."""

    def __init__(
        self,
        fetch_fn: FetchFn,
        robots: RobotsPolicy | None = None,
        *,
        min_interval: float = 1.0,
        cache_dir: Path | None = None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._fetch_fn = fetch_fn
        self._robots = robots or RobotsPolicy.allow_all()
        self._min_interval = min_interval
        self._cache_dir = cache_dir
        self._sleep = sleep
        self._clock = clock
        self._last_fetch: float | None = None
        #: URLs skipped because robots.txt disallowed them (audit trail).
        self.disallowed: list[str] = []

    def _cache_path(self, url: str) -> Path | None:
        if self._cache_dir is None:
            return None
        digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return self._cache_dir / f"{digest}.html"

    def _throttle(self) -> None:
        if self._last_fetch is not None:
            elapsed = self._clock() - self._last_fetch
            wait = self._min_interval - elapsed
            if wait > 0:
                self._sleep(wait)
        self._last_fetch = self._clock()

    def fetch(self, url: str) -> str | None:
        """Return the HTML for ``url``, or ``None`` if disallowed or empty.

        Cache hits bypass both robots and the rate limit (no network happens).
        """
        cache_path = self._cache_path(url)
        if cache_path is not None and cache_path.is_file():
            return cache_path.read_text(encoding="utf-8")

        if not self._robots.can_fetch(url):
            self.disallowed.append(url)
            return None

        self._throttle()
        html = self._fetch_fn(url)
        if html is None:
            return None

        if cache_path is not None:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(html, encoding="utf-8")
        return html


def requests_fetch(
    url: str, *, user_agent: str = DEFAULT_USER_AGENT, timeout: float = 30.0
) -> str | None:
    """Default network fetch via ``requests`` (blocked-by-resource: needs the network).

    Returns the response text on HTTP 200, else ``None``. Kept import-local so the rest of
    the module (and its tests) need no network stack.
    """
    import requests  # local import: only the live path needs requests

    response = requests.get(url, headers={"User-Agent": user_agent}, timeout=timeout)
    if response.status_code != 200:
        return None
    return response.text
