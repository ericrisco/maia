"""E2: normalització tipogràfica sense modificar dades ni noms."""

from __future__ import annotations

import re
import textwrap

LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
PAREN_LINK = re.compile(r"\s*\(\s*(?:\[[^\]]+\]\([^)]+\)\s*(?:;\s*)?)+\)")
EMPHASIS = re.compile(r"(\*\*|__)(.+?)\1|(?<!\*)\*([^*\n]+)\*(?!\*)|(?<!_)_([^_\n]+)_(?!_)")
URL_LINK = re.compile(r"\]\((?:https?://|mailto:)[^)]+\)")


def strip_work_sentences(text: str) -> tuple[str, bool, str]:
    """Retira només frases editorials amb inici tancat; retorna motiu de revisió."""
    patterns = (
        r"Tota la font\b[^.!?]*(?:[.!?]|$)",
        r"El material era al corpus\b[^.!?]*(?:[.!?]|$)",
        r"Aquest corpus\b[^.!?]*(?:[.!?]|$)",
        r"El corpus\b[^.!?]*(?:[.!?]|$)",
        r"Tancat el\b[^.!?]*(?:[.!?]|$)",
    )
    original = text
    text = re.sub(r"[*_`]", "", text)
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    if text != original and text.strip():
        return text.strip(), False, "frase de treball eliminada"
    if text != original:
        return "", True, "frase de treball exclosa"
    return text.strip(), False, ""


def is_work_note(text: str) -> tuple[bool, str]:
    """Classifica notes del procés segons les regles finites del README."""
    if "~~" in text:
        return True, "paràgraf amb text ratllat; anotació editorial exclosa"
    normalized = re.sub(r"\s+", " ", text.strip())
    normalized = re.sub(r"[*_`]", "", normalized).lstrip("> ").replace("’", "'").casefold()
    if normalized.startswith("tanda ") and " de parla" in normalized:
        return False, ""
    corpus_subject = re.compile(
        r"\b(?:el|aquest) corpus\s+(?:no\s+|ja\s+|encara\s+|només\s+)?"
        r"(?:és|es|era|té|tenia|tindrà|fa|faria|reté|conté|conserva|manté|"
        r"reconeix|identifica|registra|documenta|subratlla|segueix|sap|troba|"
        r"marca|cita|busca|buscava|ha|havia|va|pot|ho|en|les|la|el)\b",
        re.I,
    )
    if re.match(r"(?:el corpus|aquest corpus)\b", normalized) or corpus_subject.search(normalized):
        return True, "el subjecte és «el corpus»"
    if normalized.startswith("el que sí que pot fer"):
        if "conjectura" in normalized:
            return True, "el subjecte és «el corpus» (anuncia conjectura)"
        return True, "el subjecte és «el corpus»"
    if normalized.startswith("tancat el"):
        if "raw/" in normalized:
            return True, "paràgraf que comença per «Tancat el» + enllaç a raw/"
        return True, "paràgraf que comença per «Tancat el»"
    if re.search(r"(?:^|[ (])(?:\.\./|\./)*(?:docs/)?raw/", normalized):
        return True, "referència local a raw/; paràgraf exclòs per higiene del chunk"
    if normalized.startswith("auditat el"):
        return True, "blockquote d'auditoria"
    if ("fonts/" in normalized or "raw/" in normalized) and any(
        verb in normalized
        for verb in ("conserva", "s'ha revisat", "s'ha transcrit", "s'ha consultat")
    ):
        if "s'ha revisat" in normalized:
            return True, "paràgraf de procedència editorial (enllaç a fonts/ + «s'ha revisat»)"
        return True, "enllaç a fonts/raw amb verb de procés"
    return False, ""


def normalize_inline(text: str) -> str:
    """Neteja marques markdown i enllaços, preservant anchors i signes."""
    text = PAREN_LINK.sub("", text)
    text = LINK.sub(r"\1", text)
    text = EMPHASIS.sub(lambda match: next(group for group in match.groups()[1:] if group), text)
    text = text.replace("**", "").replace("__", "")
    text = text.replace("*", "")
    text = text.replace("’", "'")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def wrap_paragraph(text: str, width: int = 80) -> str:
    """Wraps normalized prose in the examples' 79/80-column form."""
    clean = normalize_inline(text).replace("\n", " ")
    wrap_width = 80 if clean.startswith("«") else 79
    return textwrap.fill(clean, width=wrap_width, break_long_words=False, break_on_hyphens=False)


def normalize_prose(text: str) -> str:
    """Cleans and wraps multiple Markdown paragraphs without flattening them."""
    parts = [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]
    return "\n\n".join(wrap_paragraph(part) for part in parts)
