"""Main-content extraction from HTML — PLAN M1 step 2.

Wraps trafilatura to pull the readable body out of a page, discarding boilerplate
(nav, footers, cookie banners). Deterministic given the HTML, so fully testable offline.
"""

from __future__ import annotations

import trafilatura


def extract_main_text(html: str, url: str | None = None) -> str | None:
    """Extract the main body text from an HTML document.

    Returns cleaned text, or ``None`` when trafilatura finds no meaningful content.
    """
    if not html.strip():
        return None
    text = trafilatura.extract(
        html,
        url=url,
        favor_precision=True,
        include_comments=False,
        include_tables=False,
        no_fallback=False,
    )
    if text is None:
        return None
    cleaned = text.strip()
    return cleaned or None
