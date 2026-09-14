#!/usr/bin/env python3
"""El registre de progrés del corpus, regenerat des dels fitxers.

Respon tres preguntes sense haver de rellegir el corpus sencer:

* quina unitat de font s'ha destil·lat,
* en quin article s'ha fet servir,
* què hi queda pendent.

No manté estat propi: ho dedueix del frontmatter `font:` de cada article i de
la secció «Buits registrats» de cada document. Per tant no es pot
desincronitzar, i es pot llançar tantes vegades com calgui.

    uv run python scripts/registre_progres.py > REGISTRE.md
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
CAMP = re.compile(r"^(\w+):\s*(.*)$", re.M)
BUITS = re.compile(r"^##\s+Buits registrats\s*$(.*?)(?=^##\s|\Z)", re.M | re.S)
PUNT = re.compile(r"^[-*]\s+(.+?)(?=^[-*]\s|\Z)", re.M | re.S)


def capcalera(text: str) -> dict[str, str]:
    """El frontmatter d'un document, com a diccionari pla."""
    m = FRONTMATTER.match(text)
    if not m:
        return {}
    return {k: v.strip().strip("\"'") for k, v in CAMP.findall(m.group(1))}


def buits(text: str) -> list[str]:
    """Els punts de la secció «Buits registrats», en una sola línia cadascun."""
    m = BUITS.search(text)
    if not m:
        return []
    return [" ".join(p.split()) for p in PUNT.findall(m.group(1))]


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    if not root.is_dir():
        print(f"no hi ha cap directori {root}", file=sys.stderr)
        return 2

    per_font: dict[str, list[tuple[str, str, int]]] = defaultdict(list)
    fonts: dict[str, str] = {}
    oberts = 0

    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = capcalera(text)
        rel = path.relative_to(root).as_posix()
        pendents = buits(text)
        oberts += len(pendents)

        if fm.get("type") == "font" and "id" in fm:
            fonts[fm["id"]] = rel
        elif fm.get("type") == "article" and "font" in fm:
            per_font[fm["font"]].append((fm.get("title", rel), rel, len(pendents)))

    print("# Registre de progrés del corpus\n")
    print("> Generat per `scripts/registre_progres.py`. No l'editeu a mà.\n")
    print(
        f"**{len(fonts)} fonts registrades · {sum(len(a) for a in per_font.values())} "
        f"articles destil·lats · {oberts} buits declarats oberts.**\n"
    )

    print("## Fonts destil·lades\n")
    print("| Font | Articles | Buits oberts |")
    print("| --- | --- | --- |")
    for fid in sorted(per_font):
        arts = per_font[fid]
        fitxa = f"[`{fid}`]({fonts[fid]})" if fid in fonts else f"`{fid}` ⚠ sense fitxa"
        enllacos = "<br>".join(f"[{t}]({p})" for t, p, _ in sorted(arts))
        print(f"| {fitxa} | {enllacos} | {sum(n for _, _, n in arts)} |")

    orfes = sorted(set(fonts) - set(per_font))
    print("\n## Fonts registrades i encara no destil·lades\n")
    if orfes:
        for fid in orfes:
            print(f"- [`{fid}`]({fonts[fid]}) — cap article no la cita.")
    else:
        print("Cap: totes les fonts registrades tenen almenys un article.")

    sense = sorted(fid for fid in per_font if fid not in fonts)
    if sense:
        print("\n## Articles que citen una font sense fitxa\n")
        for fid in sense:
            for titol, ruta, _ in sorted(per_font[fid]):
                print(f"- [{titol}]({ruta}) cita `{fid}`, que no té fitxa a `fonts/`.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
