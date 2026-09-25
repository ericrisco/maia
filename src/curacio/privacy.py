"""E6: detectors conservadors de dades personals, sense emmascarament."""

from __future__ import annotations

import csv
import re
from pathlib import Path

from cervell.model import Font
from curacio.model import Chunk, CuratedDoc

EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE = re.compile(r"(?<!\w)(?:\+376[ -]?)?[0-9]{3}[ -]?[0-9]{3}(?!\w)")
NRT = re.compile(r"\b[CFGJPU]-?\d{6}-?[A-Z0-9]\b", re.I)
ADDRESS = re.compile(r"\b(?:carrer|avinguda|plaça|placeta|passatge)\s+[A-ZÀ-Þ]", re.I)
NON_PERSON_NAMES = {
    "diada andorrana",
    "nova reforma",
    "consell de la terra",
    "copríncep episcopal",
    "periòdic d'andorra",
}


def load_whitelist(path: Path, docs: list[CuratedDoc], fonts: list[Font] | None = None) -> set[str]:
    """Reads public-person decisions and adds subjects of public-person branches."""
    names: set[str] = set()
    if path.exists():
        with path.open(encoding="utf-8", newline="") as source:
            for row in csv.DictReader(source, delimiter="\t"):
                if row.get("nom", "").strip():
                    names.add(row["nom"].strip().casefold())
    for doc in docs:
        if doc.doc_id.startswith(("temes/persones/", "temes/esports/")):
            names.add(doc.title.casefold())
        if doc.data.get("type") == "parla" and doc.data.get("parlant"):
            speaker = doc.data["parlant"]
            if isinstance(speaker, dict) and speaker.get("nom"):
                names.add(str(speaker["nom"]).casefold())
    for font in fonts or []:
        for key in ("autor", "author"):
            authors = font.data.get(key, [])
            candidates = authors if isinstance(authors, list) else [authors]
            for author in candidates:
                if isinstance(author, str):
                    names.update(
                        name.strip().casefold()
                        for name in re.split(r"[;\n]", author)
                        if name.strip()
                    )
    return names


def contains_pii(text: str, whitelist: set[str]) -> bool:
    """Checks direct identifiers and unlisted contemporary multi-part names."""
    if EMAIL.search(text) or PHONE.search(text) or NRT.search(text) or ADDRESS.search(text):
        return True
    name_pattern = re.compile(r"\b[A-ZÀ-Þ][a-zà-ÿ]+(?:\s+[A-ZÀ-Þ][a-zà-ÿ]+){1,2}\b")
    for name in name_pattern.findall(text):
        folded = name.casefold()
        if folded in NON_PERSON_NAMES or folded.split()[0] in {"el", "la", "els", "les"}:
            continue
        if folded not in whitelist and not re.search(r"\b(?:1[0-8][0-9]{2}|19[0-2][0-4])\b", text):
            return True
    return False


def mark_pii(chunks: list[Chunk], whitelist: set[str]) -> None:
    """Marks chunks as pending where any direct or unlisted PII signal appears."""
    for chunk in chunks:
        chunk.pii = contains_pii(chunk.text, whitelist)
        if chunk.pii:
            chunk.decision = "pendent"
            chunk.reason = "detector PII activat; revisió humana necessària"
