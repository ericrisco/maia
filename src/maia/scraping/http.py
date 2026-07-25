"""Polite HTTP fetching for scrapers — PLAN M1 step 1.

Respects ``robots.txt``, rate-limits to ≤1 request/second, and caches raw HTML so a re-run is
idempotent (and offline). The network call itself is an injected seam (``fetch_fn``) so the
polite-fetch orchestration is fully testable without a network: production wires
:func:`requests_fetch`, tests pass a fixture-backed callable.

**Use :func:`polite_fetcher` for a live run.** It pairs the fetcher with a :class:`RobotsCache`
that retrieves each origin's robots.txt over the same transport. A bare
``PoliteFetcher(requests_fetch)`` obeys :meth:`RobotsPolicy.allow_all` — which is right for a
site that serves no robots.txt and wrong for one that was never asked.
"""

from __future__ import annotations

import hashlib
import time
from collections.abc import Callable
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

#: Identifies the crawler to servers and in robots.txt matching.
DEFAULT_USER_AGENT = "maia-corpus-bot/0.1 (+https://github.com/ericrisco/maia)"

#: A callable that performs the actual network GET and returns the response body (or None).
FetchFn = Callable[[str], str | None]


class RobotsPolicy:
    """robots.txt decision for a single user-agent.

    Build from fetched robots.txt text (:meth:`from_text`), or let
    :class:`RobotsCache` fetch it for you. :meth:`allow_all` is the correct policy for a site
    that genuinely serves **no** robots.txt — it is *not* a safe default for a site whose
    robots.txt was never requested.
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
        """The policy for a site that serves no robots.txt (HTTP 404 is permissive)."""
        return cls(None, user_agent)

    def can_fetch(self, url: str) -> bool:
        if self._parser is None:
            return True
        return self._parser.can_fetch(self._user_agent, url)


def robots_url_for(url: str) -> str:
    """The robots.txt URL governing ``url`` — ``scheme://host[:port]/robots.txt``."""
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))


class RobotsCache:
    """Fetches and caches one :class:`RobotsPolicy` per origin.

    This is the piece that makes "robots.txt respected" true rather than aspirational. Before
    this existed, :class:`PoliteFetcher` defaulted to :meth:`RobotsPolicy.allow_all` and
    **nothing in the codebase ever requested a robots.txt** — so the live wiring obeyed a policy
    it had never read, while several modules' docstrings claimed otherwise. An adversarial review
    caught the gap.

    A robots.txt that cannot be retrieved is treated as permissive, which is the documented
    convention for a 404. That is a deliberate choice and the one place a caller may want to be
    stricter: pass ``allow_on_error=False`` to refuse an origin whose rules could not be read.
    """

    def __init__(
        self,
        fetch_fn: FetchFn,
        *,
        user_agent: str = DEFAULT_USER_AGENT,
        allow_on_error: bool = True,
    ) -> None:
        self._fetch_fn = fetch_fn
        self._user_agent = user_agent
        self._allow_on_error = allow_on_error
        self._policies: dict[str, RobotsPolicy] = {}
        #: Origins whose robots.txt could not be retrieved (audit trail).
        self.unreachable: list[str] = []

    def policy_for(self, url: str) -> RobotsPolicy:
        """The policy governing ``url``, fetching its robots.txt once per origin."""
        origin = urlsplit(url).netloc
        cached = self._policies.get(origin)
        if cached is not None:
            return cached
        text = self._fetch_fn(robots_url_for(url))
        if text is None:
            self.unreachable.append(origin)
            policy = (
                RobotsPolicy.allow_all(user_agent=self._user_agent)
                if self._allow_on_error
                else RobotsPolicy.from_text(
                    "User-agent: *\nDisallow: /\n", user_agent=self._user_agent
                )
            )
        else:
            policy = RobotsPolicy.from_text(text, user_agent=self._user_agent)
        self._policies[origin] = policy
        return policy

    def can_fetch(self, url: str) -> bool:
        """Whether ``url`` may be fetched under its origin's robots.txt."""
        return self.policy_for(url).can_fetch(url)


class PoliteFetcher:
    """Fetch URLs respecting robots.txt, a rate limit, and an on-disk HTML cache."""

    def __init__(
        self,
        fetch_fn: FetchFn,
        robots: RobotsPolicy | RobotsCache | None = None,
        *,
        min_interval: float = 1.0,
        cache_dir: Path | None = None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._fetch_fn = fetch_fn
        # A robots policy is required in spirit: passing none means "this origin serves no
        # robots.txt", not "do not check". Production callers pass a RobotsCache, which fetches
        # it (see `polite_fetcher`).
        self._robots: RobotsPolicy | RobotsCache = robots or RobotsPolicy.allow_all()
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


def polite_fetcher(
    fetch_fn: FetchFn = None,  # type: ignore[assignment]
    *,
    user_agent: str = DEFAULT_USER_AGENT,
    min_interval: float = 1.0,
    cache_dir: Path | None = None,
) -> PoliteFetcher:
    """A fetcher that actually reads robots.txt before every new origin.

    This is the wiring every scraper should use for a live run: it pairs :class:`PoliteFetcher`
    with a :class:`RobotsCache` over the same ``fetch_fn``, so robots.txt is retrieved with the
    same transport, user agent and (implicitly) courtesy as the pages themselves.
    """
    transport = fetch_fn if fetch_fn is not None else requests_fetch
    return PoliteFetcher(
        transport,
        RobotsCache(transport, user_agent=user_agent),
        min_interval=min_interval,
        cache_dir=cache_dir,
    )


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
