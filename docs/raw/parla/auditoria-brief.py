"""Comprova que cada fitxa de parla compleixi les regles del recol·lector.

Les regles són les del brief de l'investigador de parla, i es comproven totes
les que es poden comprovar mecànicament:

| Línia | Regla | Com es comprova |
| --- | --- | --- |
| 9 | El consentiment va primer | el cos de la fitxa l'ha de declarar |
| 15 | Cita minut i segon, sempre | marques de temps al cos |
| 17 | Qui parla: parròquia, generació, de casa o
       vingut, llengua primera | els quatre camps hi han de sortir |
| 21 | Cada fitxa acaba amb «Buits registrats» | la secció hi ha de ser |
| 23 | Veu recollida i apte_llengua true, a docs/parla/ | frontmatter i ruta |

**No comprova si el contingut és bo**: comprova que hi sigui. La primera vegada
que es va passar, **setze de vint-i-quatre fitxes no declaraven el consentiment**
—estava a la fitxa de font i al registre, però no a la peça—, i això obligava qui
llegís una fitxa a anar-lo a buscar a una altra banda.

    python auditoria-brief.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ARREL = Path("docs/parla")

CAMPS_PERFIL = [
    ("parròquia", r"parròquia"),
    ("generació", r"generació"),
    ("de casa o vingut", r"de casa"),
    ("llengua primera", r"llengua primera"),
]


def parts(text: str) -> tuple[dict, str]:
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, text[m.end() :]


def revisa(cami: Path) -> list[str]:
    fm, cos = parts(cami.read_text(encoding="utf-8"))
    problemes: list[str] = []
    if fm.get("veu") != "originaria":
        problemes.append("L23 veu no és originaria")
    if fm.get("apte_llengua") is not True:
        problemes.append("L23 apte_llengua no és true")
    if not re.search(r"consent", cos, re.I):
        problemes.append("L9 no declara el consentiment")
    if len(re.findall(r"\[\d\d:\d\d:\d\d\.\d+ -->", cos)) < 5:
        problemes.append("L15 sense marques de temps")
    for etiqueta, patro in CAMPS_PERFIL:
        if not re.search(patro, cos, re.I):
            problemes.append(f"L17 falta {etiqueta}")
    if "Buits registrats" not in cos:
        problemes.append("L21 sense «Buits registrats»")
    return problemes


def main() -> None:
    fitxes = [f for f in sorted(ARREL.rglob("*.md")) if f.name != "README.md"]
    dolentes = {f: revisa(f) for f in fitxes}
    dolentes = {f: p for f, p in dolentes.items() if p}

    print(f"fitxes de parla: {len(fitxes)}")
    if not dolentes:
        print("✓ totes compleixen L9, L15, L17, L21 i L23")
        return
    for cami, problemes in dolentes.items():
        print(f"✗ {cami.name}")
        for p in problemes:
            print(f"    {p}")
    sys.exit(1)


if __name__ == "__main__":
    main()
