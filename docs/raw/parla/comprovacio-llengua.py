"""Comprova que una peça sigui realment en català i no en una altra llengua.

Sembla innecessari fins que passa. La càpsula #65 d'AR+I es va registrar durant
divuit tandes com «la conversa més valuosa trobada amb drets nets» **sense que
ningú n'hagués llegit ni una frase**: venia d'una font andorrana amb títol en
català, i això es va prendre per la llengua del contingut. És una entrevista
**en castellà**, perquè un dels dos interlocutors és alemany i parlen en
castellà.

La prova és barata i el cost de no fer-la és tenir castellà dins d'un corpus de
llengua andorrana. Es fa comptant mots funcionals que **només** existeixen en
una de les dues llengües: no mots de contingut, que es confonen.

    python comprovacio-llengua.py docs/raw/parla/*/transcripcio-asr-marcada.txt
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Mots funcionals exclusius. Es trien perquè són freqüents i no es comparteixen.
CASTELLA = {
    "pues",
    "entonces",
    "pero",
    "porque",
    "también",
    "muy",
    "desde",
    "hasta",
    "cuando",
    "siempre",
    "nada",
    "algo",
    "eso",
    "esto",
    "ese",
    "esa",
    "los",
    "las",
    "con",
    "sin",
    "sus",
    "muchos",
    "mucha",
    "nosotros",
    "vosotros",
    "ellos",
    "está",
    "están",
    "hacer",
    "hace",
    "tiene",
}
CATALA = {
    "doncs",
    "llavors",
    "però",
    "perquè",
    "també",
    "molt",
    "des",
    "fins",
    "quan",
    "sempre",
    "res",
    "alguna",
    "això",
    "allò",
    "aquest",
    "aquesta",
    "els",
    "les",
    "amb",
    "sense",
    "seus",
    "molts",
    "moltes",
    "nosaltres",
    "vosaltres",
    "ells",
    "està",
    "estan",
    "fer",
    "fa",
    "té",
}


def mots(text: str) -> list[str]:
    net = re.sub(r"^\[[^\]]+\]\s*", "", text, flags=re.M)
    net = re.sub(r"\[\?|\]", " ", net)
    return re.findall(r"\b[\wáéíóúñàèòçïü']+\b", net.lower())


def examina(cami: Path) -> tuple[str, int, int, int, str]:
    w = mots(cami.read_text(encoding="utf-8"))
    cast = sum(1 for m in w if m in CASTELLA)
    cat = sum(1 for m in w if m in CATALA)
    total = cast + cat
    if total < 20:
        return cami.parent.name, len(w), cast, cat, "poques dades"
    quota = cat * 100 / total
    if quota < 40:
        estat = "NO ÉS CATALÀ"
    elif quota < 75:
        estat = "MESCLAT — mirar"
    else:
        estat = "català"
    return cami.parent.name, len(w), cast, cat, estat


def main() -> None:
    camins = [Path(a) for a in sys.argv[1:]]
    if not camins:
        camins = sorted(Path("docs/raw/parla").glob("*/transcripcio-asr-marcada.txt"))

    print(f"{'peça':28s}{'mots':>7s}{'cast.':>7s}{'cat.':>7s}{'% català':>10s}  veredicte")
    for cami in camins:
        nom, w, cast, cat, estat = examina(cami)
        quota = cat * 100 / max(cast + cat, 1)
        print(f"{nom[:27]:28s}{w:7d}{cast:7d}{cat:7d}{quota:9.0f}%  {estat}")


if __name__ == "__main__":
    main()
