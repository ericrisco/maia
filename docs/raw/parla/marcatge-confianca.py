"""Marca amb `[?...]` les paraules que la màquina no dona per segures.

Substitueix l'orella que no hi ha. Una transcripció humana escriu `[inaudible]`
allà on no sent; una ASR no calla mai i escriu sempre la seva millor conjectura.
Aquest script fa servir la probabilitat del propi model com a substitut: agrupa
els tokens de whisper.cpp en paraules, es queda amb la probabilitat MÍNIMA de
cada paraula, i marca la que baixa del llindar.

`[?x]` no vol dir «diu x». Vol dir «la màquina proposa x i ningú no ho ha
comprovat contra l'àudio».

Entrada: el JSON complet de `whisper-cli -ojf`.

    python marcatge-confianca.py capsula56_full.json 0.55
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

LLINDAR = 0.55


def hms(ms: int) -> str:
    """Marca de temps absoluta contra l'àudio original."""
    return (
        f"{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d}.{ms % 1000:03d}"
    )


def paraules(tokens: list[dict]) -> list[tuple[str, float]]:
    """Agrupa tokens en paraules. Una paraula val el que val el seu token més dubtós."""
    out: list[list] = []
    for tok in tokens:
        text = tok["text"]
        if text.startswith(("[_", "<|")):
            continue
        if text.startswith(" ") or not out:
            out.append([text, tok["p"]])
        else:
            out[-1][0] += text
            out[-1][1] = min(out[-1][1], tok["p"])
    return [(w.strip(), p) for w, p in out if w.strip()]


def main() -> None:
    origen = Path(sys.argv[1])
    llindar = float(sys.argv[2]) if len(sys.argv) > 2 else LLINDAR
    dades = json.loads(origen.read_text(encoding="utf-8"))

    marcades: list[tuple[int, str, float]] = []
    linies: list[str] = []

    for seg in dades["transcription"]:
        trossos: list[str] = []
        for mot, p in paraules(seg["tokens"]):
            if p < llindar and re.search(r"\w", mot):
                trossos.append(f"[?{mot}]")
                marcades.append((seg["offsets"]["from"], mot, round(p, 2)))
            else:
                trossos.append(mot)
        text = re.sub(r" ([,.;:!?])", r"\1", " ".join(trossos))
        linies.append(f"[{hms(seg['offsets']['from'])} --> {hms(seg['offsets']['to'])}] {text}")

    Path("transcripcio-asr-marcada.txt").write_text("\n".join(linies) + "\n", encoding="utf-8")

    print(f"segments={len(linies)} marcades={len(marcades)} llindar={llindar}")
    for ms, mot, p in marcades:
        print(f"  {hms(ms)}  {mot!r}  p={p}")


if __name__ == "__main__":
    main()
