"""Verifica l'expedient separat del candidat Mireia Pedescoll."""

from __future__ import annotations

import csv
import hashlib
import wave
from pathlib import Path

ROOT = Path(__file__).parents[1]
CAND = ROOT / "proveniencia" / "candidats" / "lead-rtva-008-mireia-pedescoll"
EXPECTED_SHA = "99092a10edeccecfcab0f7596a18600545f5a9c11243d083e5e92e287e96a39c"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    errors = []
    audio = CAND / "audio.wav"
    if not audio.exists() or hashlib.sha256(audio.read_bytes()).hexdigest() != EXPECTED_SHA:
        errors.append("hash de l'àudio invàlid")
    else:
        with wave.open(str(audio)) as handle:
            if abs(handle.getnframes() / handle.getframerate() - 1384.3853125) > 0.01 or handle.getframerate() != 16000 or handle.getnchannels() != 1:
                errors.append("format o durada de l'àudio invàlids")
    for name in ["mireia-pedescoll.txt", "mireia-pedescoll.vtt", "mireia-pedescoll.json", "mireia-pedescoll-base.txt", "mireia-pedescoll-base.vtt", "mireia-pedescoll-base.json"]:
        if not (CAND / "asr" / name).exists():
            errors.append(f"falta asr/{name}")
    forms = rows(CAND / "formes-consens.tsv")
    clips = rows(CAND / "formes-clips.tsv")
    acoustic = rows(CAND / "analisi-acustica.tsv")
    if len(forms) != 35:
        errors.append(f"formes-consens.tsv té {len(forms)} files")
    if len(clips) != 19 or len(acoustic) != 19:
        errors.append("la cua o l'acústica no confirma 19 clips")
    if any(not (CAND / row["clip"]).exists() for row in clips):
        errors.append("falta un WAV de clip")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK candidat rtva-008: Mireia Pedescoll · 1384 s · doble ASR · 35 formes · 19 clips · acústica")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
