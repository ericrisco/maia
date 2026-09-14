"""Quant de cada peça és conjectura de la màquina, en una mesura que es pot comparar.

Fins a la tanda 15 això es reportava com a **marques per segment**, i era una
mesura enganyosa: els segments no tenen la mateixa llargada, de manera que una
peça amb segments curts sembla pitjor que una amb segments llargs encara que la
transcripció sigui igual de bona. Dues fitxes van arribar a dir coses falses per
això i s'han hagut de corregir.

La mesura estable és **marques per cent mots**: quina proporció del que es diu
és conjectura no verificada.

    python qualitat-transcripcions.py [fitxers...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ARREL = Path("docs/raw/parla")

# Per damunt d'aquí, una peça s'ha de LLEGIR abans de decidir res. No és un
# llindar de rebuig: és un llindar d'atenció.
#
# A la tanda 23 es va fer servir com a llindar de rebuig i **va ser un error**.
# Es van descartar tres testimonis al 12,9 %, 16,2 % i 16,6 % sense llegir-ne
# dos. En llegir-los a la tanda 24 va resultar que **totes tres es segueixen
# perfectament**: les marques cauen sobretot a mots funcionals i a noms, no al
# contingut. Es van readmetre.
#
# La proporció de marques diu **quanta conjectura hi ha**, no **si el text es
# pot fer servir**. Dues peces amb el mateix percentatge poden ser una
# llegible i l'altra inintel·ligible, segons si les marques s'agrupen o es
# reparteixen. Això només ho veu qui llegeix.
LLINDAR_ATENCIO = 10.0


def mesura(cami: Path) -> tuple[str, int, int, float]:
    text = cami.read_text(encoding="utf-8")
    cos = re.sub(r"^\[[^\]]+\]\s*", "", text, flags=re.M)
    mots = len(cos.split())
    marques = len(re.findall(r"\[\?", text))
    return cami.parent.name, mots, marques, marques * 100 / max(mots, 1)


def main() -> None:
    camins = [Path(a) for a in sys.argv[1:]]
    if not camins:
        camins = sorted(ARREL.glob("*/transcripcio-asr-marcada.txt"))
        camins += sorted((ARREL / "descartades").glob("*/transcripcio-asr-marcada.txt"))
        camins += sorted((ARREL / "pendents").glob("*/transcripcio-asr-marcada.txt"))

    # Descartades i pendents es mesuren però NO compten al total: no són el corpus.
    # Es mesuren perquè un número que no es mira no serveix de res el dia que una
    # pendent es reobre; s'exclouen perquè el total ha de dir què hi ha a dins.
    fora = {c.parent.name for c in camins if {"descartades", "pendents"} & set(c.parts)}
    pendents = {c.parent.name for c in camins if "pendents" in c.parts}
    files = sorted((mesura(c) for c in camins), key=lambda r: r[3])

    print(f"{'peça':28s}{'mots':>7s}{'marques':>9s}{'% dels mots':>13s}")
    for nom, mots, marques, pct in files:
        if nom in pendents:
            marca = "  (pendent)"
        elif nom in fora:
            marca = "  (descartada)"
        elif pct > LLINDAR_ATENCIO:
            marca = "  <- llegir-la abans de citar-la"
        else:
            marca = ""
        print(f"{nom[:27]:28s}{mots:7d}{marques:9d}{pct:12.1f}%{marca}")

    admeses = [r for r in files if r[0] not in fora]
    total_mots = sum(r[1] for r in admeses)
    total_marques = sum(r[2] for r in admeses)
    print(f"\n{len(admeses)} peces admeses · {total_mots} mots · {total_marques} marques")
    print(
        f"{total_marques * 100 / total_mots:.1f} % del corpus de parla és conjectura no verificada."
    )


if __name__ == "__main__":
    main()
