"""Compara una transcripció de parla amb el corpus ja escrit i en treu els candidats.

Fins a la tanda 3 això es feia a mà, mot a mot. El risc de fer-ho a mà no és
cansar-se: és que **només es troba el que ja se sospitava**. Aquest escaneig
recorre TOT el vocabulari de la peça i en treu el que el corpus no té enlloc.

No decideix res. Un mot que surti aquí pot ser un tret andorrà, un nom propi o
un error de la màquina; qui escriu la fitxa ho mira un per un. El que fa
l'escaneig és **garantir que ningú no ha de confiar en la seva memòria**.

    python escaneig-novetat.py <transcripcio-marcada.txt> [arrel-docs]
"""

from __future__ import annotations

import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

MARCADORS = ["vull dir", "bueno", "clar", "doncs", "vale", "o sigui", "aleshores", "llavors"]

# Mots que surten a qualsevol prosa i que no diuen res sobre la parla.
PROU_VISTOS = 3


def cos(text: str) -> str:
    """Treu les marques de temps i deixa només el que es va dir."""
    return re.sub(r"^\[[^\]]+\]\s*", "", text, flags=re.M)


def mots(text: str) -> list[str]:
    net = re.sub(r"\[\?|\]", " ", text)
    return re.findall(r"\b[\wàèéíòóúïüçñ·']{3,}\b", net.lower())


def sense_accents(paraula: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", paraula) if not unicodedata.combining(c))


def vocabulari_corpus(arrel: Path) -> set[str]:
    vist: set[str] = set()
    for md in arrel.rglob("*.md"):
        vist.update(mots(md.read_text(encoding="utf-8")))
    return vist


def main() -> None:
    origen = Path(sys.argv[1])
    arrel = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("docs/temes")
    text = origen.read_text(encoding="utf-8")
    parla = cos(text)

    print(f"peça: {origen.name}")
    print(f"mots: {len(parla.split())}")

    print("\n--- marcadors discursius ---")
    for m in MARCADORS:
        n = len(re.findall(r"\b" + re.escape(m) + r"\b", parla, re.I))
        if n:
            print(f"  {m:12s} {n:4d}")
    represes = len(re.findall(r"\bno\?", parla))
    print(f"  {'no? (represa)':12s} {represes:4d}")

    coneguts = vocabulari_corpus(arrel)
    coneguts_pelats = {sense_accents(p) for p in coneguts}

    frec = Counter(mots(parla))
    nous = [
        (p, n)
        for p, n in frec.most_common()
        if p not in coneguts and sense_accents(p) not in coneguts_pelats
    ]

    print(f"\n--- absents de {arrel} ({len(nous)} formes) ---")
    for paraula, n in nous:
        dubtoses = len(re.findall(r"\[\?" + re.escape(paraula) + r"[\],.;]", text, re.I))
        estat = f"{n - dubtoses} net/{dubtoses} dub" if dubtoses else "tot net   "
        ctx = ""
        m = re.search(r".{0,60}\b" + re.escape(paraula) + r"\b.{0,50}", parla, re.I | re.S)
        if m:
            ctx = re.sub(r"\s+", " ", m.group(0))
        marca = "  <-- repetit" if n >= PROU_VISTOS else ""
        print(f"  [{estat}] {paraula:18s} x{n}{marca}\n            ...{ctx}")


if __name__ == "__main__":
    main()
