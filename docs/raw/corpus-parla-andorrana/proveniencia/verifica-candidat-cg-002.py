"""Verifica l'expedient separat del candidat Pere López."""

from __future__ import annotations

import csv
import hashlib
import wave
from pathlib import Path

ROOT = Path(__file__).parents[1]
CAND = ROOT / "proveniencia" / "candidats" / "lead-cg-002-pere-lopez"
EXPECTED_SHA = "a85aa08e71d2a57346172937b1640f0d30ff2c7252088d32700826053e68a363"


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
            if abs(handle.getnframes() / handle.getframerate() - 120.0) > 0.01 or handle.getframerate() != 16000 or handle.getnchannels() != 1:
                errors.append("format o durada de l'àudio invàlids")
    for name in ["pere-lopez.txt", "pere-lopez.vtt", "pere-lopez.json", "pere-lopez-base.txt", "pere-lopez-base.vtt", "pere-lopez-base.json"]:
        if not (CAND / "asr" / name).exists():
            errors.append(f"falta asr/{name}")
    forms = rows(CAND / "formes-consens.tsv")
    clips = rows(CAND / "formes-clips.tsv")
    acoustic = rows(CAND / "analisi-acustica.tsv")
    if len(forms) != 35:
        errors.append(f"formes-consens.tsv té {len(forms)} files")
    if len(clips) != 2 or len(acoustic) != 2:
        errors.append("la cua o l'acústica no confirma 2 clips")
    if any(not (CAND / row["clip"]).exists() for row in clips):
        errors.append("falta un WAV de clip")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK candidat cg-002: Pere López · 120 s · doble ASR · 35 formes · 2 clips · acústica")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
