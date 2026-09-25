"""E3: metadades derivades amb les correccions separades de les fonts."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

from curacio.model import Block


def normalize_redistribution(value: Any) -> tuple[str, str]:
    """Returns the closed redistribution enum and the untouched source value."""
    detail = str(value if value is not None else "pendent").strip()
    token = detail.casefold().strip(" \"'")
    if token in {"si", "sí", "yes", "true", "1"}:
        return "si", detail
    if token in {"no", "false", "0"} or any(
        phrase in token
        for phrase in ("no es publica", "no es publiquen", "recerca interna", "sense difusió")
    ):
        return "no", detail
    if token in {"pendent", "pending", "unknown", "desconegut", ""}:
        return "pendent", detail
    return "pendent", detail


def load_families(path: Path) -> dict[str, str]:
    """Loads explicit human overrides; unmatched sources remain their own family."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as source:
        rows = csv.DictReader(source, delimiter="\t")
        return {
            row["font"].strip(): row["familia_font"].strip()
            for row in rows
            if row.get("font", "").strip() and row.get("familia_font", "").strip()
        }


def family_for(font: str, families: dict[str, str]) -> str:
    """Uses a checked-in family mapping or a conservative one-source family."""
    return families.get(font, font or "sense-font")


def domain_for(tema: str) -> str:
    """First thematic path component, or a visible unknown marker."""
    return tema.split("/", maxsplit=1)[0] if tema else "sense-domini"


def years_in(text: str) -> list[int]:
    """Unique four-digit years, returned in textual order."""
    return list(
        dict.fromkeys(int(match) for match in re.findall(r"\b(?:1[0-9]{3}|20[0-9]{2})\b", text))
    )


def entities_in(text: str) -> list[str]:
    """A deterministic candidate list of proper-name spans for later inspection."""
    pattern = re.compile(r"\b[A-ZÀ-Þ][a-zà-ÿ]+(?:[ -][A-ZÀ-Þ][a-zà-ÿ]+){1,3}\b")
    return list(dict.fromkeys(pattern.findall(text)))


def volatility_for(text: str) -> float:
    """Adds each volatility signal once and caps the result at one."""
    lowered = text.casefold()
    score = 0.0
    if re.search(r"\b(?:19|20)\d{2}\s*[-–—]\s*(?:avui|avui dia|$|[|])", lowered):
        score += 0.5
    if any(term in lowered for term in ("en exercici", "en actiu", "actual", "actualment", "avui")):
        score += 0.4
    if re.search(r"\b20(?:2[0-9]|[3-9][0-9])\b", text):
        score += 0.3
    if re.search(r"\b[Ll]lei\b.{0,80}\b(?:article|art\.)\s*\d", text, re.I):
        score += 0.3
    return min(score, 1.0)


def enrich_blocks(blocks: list[Block]) -> None:
    """Annotates volatility per block without mutating its source text."""
    for block in blocks:
        block.volatility = volatility_for(block.raw)
