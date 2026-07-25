"""Text normalization and the boilerplate filter — PLAN M1.08, step 2.

Two responsibilities, both deterministic and both applied to every document before it is
deduplicated:

* :func:`clean_text` — Unicode NFC, invisible-character removal, quote/dash unification and
  whitespace tidying. It changes the stored ``text``, which means it changes the document's
  ``id`` (a sha256 of the normalized text), so consolidation always rebuilds the document
  rather than editing it in place. Doing this *before* dedup is what makes dedup work: two
  copies of the same page that differ only by a non-breaking space are not duplicates until
  the text is normalized.
* :func:`boilerplate_score` — how much of a document looks like chrome rather than prose.
  Scrapers already drop pages with too little text, but a page can be long and still be a
  cookie banner plus a navigation menu.

The filter is intentionally conservative: it is better to carry a slightly noisy document
into the RAG index than to silently delete a real one, so every threshold errs towards
keeping and :class:`CleanVerdict` explains itself for the coverage report (M1.10).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

#: Zero-width and bidi-control characters. They survive NFC, are invisible, and defeat both
#: dedup (two identical pages hash differently) and search.
_INVISIBLE = dict.fromkeys(
    [
        0x00AD,  # soft hyphen
        0x200B,  # zero width space
        0x200C,  # zero width non-joiner
        0x200D,  # zero width joiner
        0x200E,  # left-to-right mark
        0x200F,  # right-to-left mark
        0x2060,  # word joiner
        0xFEFF,  # byte order mark
    ]
)

#: Typographic variants folded to their ASCII form. Catalan keeps « » (used in legal text),
#: but curly quotes and the various dashes are noise that splits otherwise-identical text.
_TYPOGRAPHIC = str.maketrans(
    {
        "\u2018": "'",  # left single quotation mark
        "\u2019": "'",  # right single quotation mark (also the typographic apostrophe)
        "\u201a": "'",  # single low-9 quotation mark
        "\u201c": '"',  # left double quotation mark
        "\u201d": '"',  # right double quotation mark
        "\u201e": '"',  # double low-9 quotation mark
        "\u2032": "'",  # prime
        "\u2033": '"',  # double prime
        "\u00a0": " ",  # non-breaking space
        "\u2007": " ",  # figure space
        "\u202f": " ",  # narrow no-break space
        "\u2009": " ",  # thin space
        "\ufb01": "fi",  # fi ligature, common in PDF text layers
        "\ufb02": "fl",  # fl ligature
    }
)

#: Control characters other than tab and newline — PDF and HTML extraction artifacts.
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

#: Phrases that only ever appear in page chrome, not in Andorran prose.
_CHROME_MARKERS = (
    "accepta les cookies",
    "acceptar cookies",
    "política de cookies",
    "politica de cookies",
    "aquest lloc web utilitza cookies",
    "utilitzem cookies",
    "javascript",
    "navegador no és compatible",
    "tots els drets reservats",
    "inicia la sessió",
    "inicieu la sessió",
    "salta al contingut",
    "menú principal",
    "mapa del web",
)


def clean_text(text: str) -> str:
    """Normalize a document's text: NFC, invisibles out, quotes and whitespace unified.

    Words are never altered — only the characters around and between them — so dialectal
    lexicon and legal wording survive untouched.
    """
    text = unicodedata.normalize("NFC", text)
    text = text.translate(_INVISIBLE)
    text = text.translate(_TYPOGRAPHIC)
    text = _CONTROL.sub("", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


@dataclass(frozen=True)
class CleanVerdict:
    """Why a document was kept or dropped, so the coverage report can explain itself."""

    keep: bool
    reason: str
    score: float


def _letter_ratio(text: str) -> float:
    visible = [char for char in text if not char.isspace()]
    if not visible:
        return 0.0
    return sum(char.isalpha() for char in visible) / len(visible)


def _repeated_line_ratio(text: str) -> float:
    """Fraction of lines that are duplicates of an earlier line — the shape of a nav menu."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        return 0.0
    return 1.0 - len(set(lines)) / len(lines)


def _unique_word_ratio(text: str) -> float:
    words = re.findall(r"\w+", text.lower())
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def boilerplate_score(text: str) -> float:
    """How much of ``text`` looks like page chrome, from 0.0 (prose) to 1.0 (menu).

    A blend of three independent signals: the share of duplicated lines, the share of
    non-letter characters, and the presence of phrases that only occur in chrome. Any one of
    them can be fooled; together they separate a cookie wall from an article.
    """
    lowered = text.lower()
    chrome_hits = sum(marker in lowered for marker in _CHROME_MARKERS)
    signals = (
        _repeated_line_ratio(text),
        1.0 - _letter_ratio(text),
        min(chrome_hits / 3.0, 1.0),
    )
    return max(signals)


def assess(
    text: str,
    *,
    min_chars: int = 200,
    max_boilerplate: float = 0.6,
    min_unique_word_ratio: float = 0.15,
) -> CleanVerdict:
    """Decide whether a cleaned document is worth keeping.

    ``min_unique_word_ratio`` catches the pathological case a boilerplate score misses: text
    long and letter-rich but with almost no vocabulary, i.e. one phrase repeated.
    """
    if len(text) < min_chars:
        return CleanVerdict(False, f"shorter than {min_chars} characters", 0.0)
    score = boilerplate_score(text)
    if score > max_boilerplate:
        return CleanVerdict(False, f"boilerplate score {score:.2f} > {max_boilerplate}", score)
    unique_ratio = _unique_word_ratio(text)
    if unique_ratio < min_unique_word_ratio:
        return CleanVerdict(
            False, f"unique-word ratio {unique_ratio:.2f} < {min_unique_word_ratio}", score
        )
    return CleanVerdict(True, "clean", score)
