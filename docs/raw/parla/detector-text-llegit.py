"""Detecta si una peça és parla o és un text escrit llegit en veu alta.

La regla del recol·lector diu «sempre parla real, mai text escrit per algú
altre», i una gravació no ho porta escrit al damunt: un ponent que llegeix un
guió sona igual de bé que un que parla. La tanda 7 va estar a punt d'entrar al
corpus sent un text llegit.

Dos indicis, i el primer és gairebé decisiu:

1. **Passat simple sintètic** (*passaren*, *impulsaren*, *digué*, *arribà*). En
   català central i pirinenc **ningú no el diu parlant**: és exclusiu de
   l'escrit. Una sola ocurrència ja fa sospitar; dues, el cas està tancat.
   El plural es busca **per patró** (-aren/-eren/-iren) i no per llista, perquè
   una llista se'n deixa sempre alguna: va passar dues vegades.
2. **Densitat de marcadors discursius**, la interrogació de represa inclosa. Qui
   parla de debò diu *doncs*, *clar*, *bueno*, i sobretot *no?*, que **interpel·la
   algú que escolta**. Un text escrit no interpel·la ningú.

El segon indici sol, NO decideix: una xerrada preparada i ben dita en té pocs
sense ser llegida. Per això el veredicte només és ferm quan hi ha passat simple.

    python detector-text-llegit.py docs/raw/parla/*/transcripcio-asr-marcada.txt
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MARCADORS = ["vull dir", "bueno", "clar", "doncs", "o sigui", "vale"]

# Terceres persones del passat simple. Deliberadament curta i segura: només
# formes que no es poden confondre amb un present o un participi.
# La 3a persona del PLURAL del passat simple és un patró, no una llista: acaba
# sempre en -aren, -eren o -iren. Comprovar-ho amb un patró i no amb un
# inventari és el que fa que no se n'escapi cap.
#
# Aquesta lliçó ha costat dues peces. La llista tenia `foren` i no `tingueren`
# (tanda 19) i després no tenia `impulsaren` (tanda 29): les dues vegades el
# detector va deixar passar un guió llegit, i les dues vegades es va descobrir
# perquè algú va llegir la transcripció. **Un inventari de formes sempre és
# incomplet; un patró, no.**
PLURAL_SIMPLE = re.compile(r"\b\w{3,}(?:aren|eren|iren)\b", re.I)

# El singular sí que s'ha de llistar: -à, -é, -í coincideixen amb massa coses
# (noms, adverbis, mots estrangers) per fer-ne un patró segur.
SINGULAR_SIMPLE = re.compile(
    r"\b(?:"
    r"fou|hagué|vingué|digué|féu|volgué|pogué|tingué|esdevingué|"
    r"arribà|començà|quedà|restà|parlà|entrà|passà|acabà|trobà|deixà|impulsà|"
    r"nasqué|morí|construí|sortí|obrí|establí|sorgí"
    r")\b",
    re.I,
)

# El patró té un forat que NO es pot tancar del tot sense diccionari: els verbs
# amb l'arrel acabada en -ar, -er o -ir fan un PRESENT que acaba igual que un
# passat simple. `parlaren` (passat, de parlar) i `preparen` (present, de
# preparar) acaben totes dues en -aren, i ortogràficament no es distingeixen.
#
# Per això el detector **no condemna amb una sola forma**: una és «sospitós» i
# obliga a llegir. Buscades a les 37 peces admeses —totes parla comprovada—,
# només n'hi surt una: `preparen`, dues vegades. El forat existeix i és petit.
EXCEPCIONS = {
    # arrel en -ar
    "preparen",
    "comparen",
    "separen",
    "declaren",
    "aclaren",
    "disparen",
    "reparen",
    "amparen",
    "encaren",
    # arrel en -er
    "esperen",
    "consideren",
    "superen",
    "generen",
    "operen",
    "toleren",
    "moderen",
    "recuperen",
    "alteren",
    "cooperen",
    "exageren",
    "enumeren",
    # arrel en -ir
    "miren",
    "giren",
    "tiren",
    "retiren",
    "admiren",
    "inspiren",
    "aspiren",
    "adquiren",
    "expiren",
}


def cos(text: str) -> str:
    return re.sub(r"^\[[^\]]+\]\s*", "", text, flags=re.M)


def examina(cami: Path) -> tuple[str, int, float, float, list[str]]:
    parla = cos(cami.read_text(encoding="utf-8"))
    mots = len(parla.split())
    marcadors = sum(len(re.findall(r"\b" + m + r"\b", parla, re.I)) for m in MARCADORS)
    # La interrogació de represa compta com a marcador: interpel·la algú que
    # escolta, i un text escrit no interpel·la ningú. Sense això, una entrevista
    # que fa servir 'no?' en lloc de 'doncs' quedava marcada com a possible guió.
    represes = len(re.findall(r"\bno\?", parla))
    marcadors += represes
    trobats = {m.group(0).lower() for m in PLURAL_SIMPLE.finditer(parla)} - EXCEPCIONS
    trobats |= {m.group(0).lower() for m in SINGULAR_SIMPLE.finditer(parla)}
    simples = sorted(trobats)
    nom = cami.parent.name
    return nom, mots, marcadors * 1000 / mots, represes * 1000 / mots, simples


# Per sota d'aquest llindar, cap peça del corpus no ha ensenyat una rectificació.
# No és un límit mesurat: és on van quedar les peces que, llegides, semblen guió.
LLINDAR_GUIO = 3.0


def veredicte(simples: list[str], densitat: float) -> str:
    """Tres estats, i el del mig és el que importa.

    El passat simple condemna. La manca de marcadors NO condemna —una xerrada
    ben dita en té pocs— però tampoc no absol: deixa la peça en un limbe que
    aquest detector no pot resoldre i que només es tanca escoltant.
    """
    if len(simples) >= 2:
        return "TEXT LLEGIT"
    if simples:
        return "sospitós"
    if densitat < LLINDAR_GUIO:
        return "POT SER LLEGIDA"
    return "parla"


def main() -> None:
    camins = [Path(a) for a in sys.argv[1:]]
    if not camins:
        camins = sorted(Path("docs/raw/parla").glob("*/transcripcio-asr-marcada.txt"))

    capcalera = f"{'peça':22s}{'mots':>7s}{'marc/1000':>11s}{'no?/1000':>10s}  "
    print(capcalera + f"{'veredicte':22s}passat simple")
    for cami in camins:
        nom, mots, dens, rep, simples = examina(cami)
        print(
            f"{nom[:21]:22s}{mots:7d}{dens:11.1f}{rep:10.1f}  "
            f"{veredicte(simples, dens):22s}{', '.join(simples) or '-'}"
        )


if __name__ == "__main__":
    main()
