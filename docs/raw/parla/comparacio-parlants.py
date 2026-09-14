"""Compara una forma a través de totes les peces de parla transcrites.

La pregunta que aquest script contesta és l'única que separa una troballa d'una
anècdota: **quants parlants diferents ho diuen?**

Fins a la tanda 4 el corpus va afirmar que 167 «vull dir» eren la signatura de
la parla andorrana. La tanda 5 va ensenyar que era la signatura d'UNA persona.
Una forma que surt en un parlant és idiolecte; una forma que creua parròquies i
generacions és candidata a tret. Mentre no se separin, el corpus generalitza a
partir de qui va tenir la sort de ser transcrit primer.

Compara també contra `docs/temes/`, que és prosa compilada: una forma viva a la
parla i absent de la prosa és exactament el que la branca busca.

    python comparacio-parlants.py sigut inclús feeling "vull dir"
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ARREL = Path("docs/raw/parla")
PROSA = Path("docs/temes")


def cos(text: str) -> str:
    return re.sub(r"^\[[^\]]+\]\s*", "", text, flags=re.M)


def etiqueta(carpeta: str) -> str:
    """El tros que distingeix la peça. 'cg-constituent-altimir' -> 'altimir'."""
    return carpeta.rsplit("-", 1)[-1]


def peces() -> dict[str, str]:
    """Cada transcripció marcada és una peça, i cada peça és un parlant."""
    return {
        etiqueta(t.parent.name): cos(t.read_text(encoding="utf-8"))
        for t in sorted(ARREL.glob("*/transcripcio-asr-marcada.txt"))
    }


def compta(text: str, forma: str) -> int:
    """Vora de mot només on hi ha lletra: 'no?' acaba en signe i no en porta."""
    davant = r"\b" if forma[:1].isalnum() else ""
    darrere = r"\b" if forma[-1:].isalnum() else ""
    return len(re.findall(davant + re.escape(forma) + darrere, text, re.I))


def main() -> None:
    formes = sys.argv[1:]
    if not formes:
        print(__doc__)
        return

    parla = peces()
    if not parla:
        print(f"cap transcripció a {ARREL}")
        return

    prosa = " ".join(p.read_text(encoding="utf-8") for p in PROSA.rglob("*.md"))

    noms = list(parla)
    ample = max(len(f) for f in formes) + 2
    print(
        f"{'forma':{ample}s}"
        + "".join(f"{n[:12]:>13s}" for n in noms)
        + f"{'parlants':>10s}{'prosa':>8s}"
    )

    for forma in formes:
        counts = [compta(parla[n], forma) for n in noms]
        parlants = sum(1 for c in counts if c)
        en_prosa = compta(prosa, forma)
        veredicte = ""
        if parlants >= 3 and not en_prosa:
            veredicte = "  <- candidat a tret"
        elif parlants == 1:
            veredicte = "  <- idiolecte"
        print(
            f"{forma:{ample}s}"
            + "".join(f"{c:13d}" for c in counts)
            + f"{parlants:10d}{en_prosa:8d}{veredicte}"
        )

    print(f"\n{len(noms)} peces · una forma no és tret fins que no creua parlants.")


if __name__ == "__main__":
    main()
