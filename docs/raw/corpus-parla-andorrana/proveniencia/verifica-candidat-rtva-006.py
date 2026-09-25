"""Verifica l'expedient separat del candidat Jaume Tomàs."""

from __future__ import annotations

import csv
import hashlib
import wave
from pathlib import Path

ROOT = Path(__file__).parents[1]
CAND = ROOT / "proveniencia" / "candidats" / "lead-rtva-006-jaume-tomas"
EXPECTED_SHA = "936cd8a49ad7ce1bcf89c17cfe705c37d8b019fdbe5b2e187b1594d11176ef5c"


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
            if abs(handle.getnframes() / handle.getframerate() - 1460.610625) > 0.01 or handle.getframerate() != 16000 or handle.getnchannels() != 1:
                errors.append("format o durada de l'àudio invàlids")
    for name in ["jaume-tomas.txt", "jaume-tomas.vtt", "jaume-tomas.json", "jaume-tomas-base.txt", "jaume-tomas-base.vtt", "jaume-tomas-base.json"]:
        if not (CAND / "asr" / name).exists():
            errors.append(f"falta asr/{name}")
    forms = rows(CAND / "formes-consens.tsv")
    clips = rows(CAND / "formes-clips.tsv")
    acoustic = rows(CAND / "analisi-acustica.tsv")
    if len(forms) != 35:
        errors.append(f"formes-consens.tsv té {len(forms)} files")
    if len(clips) != 14 or len(acoustic) != 14:
        errors.append("la cua o l'acústica no confirma 14 clips")
    if any(not (CAND / row["clip"]).exists() for row in clips):
        errors.append("falta un WAV de clip")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK candidat rtva-006: Jaume Tomàs · 1460 s · doble ASR · 35 formes · 14 clips · acústica")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
