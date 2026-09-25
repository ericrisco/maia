"""Genera VTT de QA amb timestamps limitats a la durada real del WAV.

Els VTT originals i les transcripcions canòniques no es modifiquen. Els derivats
només resolen la inconsistència estructural de temps; la repetició ASR de pa-047
continua marcada per a escolta humana.
"""

from __future__ import annotations

import csv
import re
import wave
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-remediacio-transcripcions.tsv"
TIMESTAMP = re.compile(r"^(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})(.*)$")


def seconds(value: str) -> float:
    hours, minutes, rest = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(rest)


def stamp(value: float) -> str:
    milliseconds = max(0, int(round(value * 1000)))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"


def process(person: str) -> dict[str, str]:
    source = ROOT / "transcripcions" / f"{person}.vtt"
    audio = ROOT / "audios" / person / "audio.wav"
    target = PROV / person / "qa-corrected" / "transcripcio-clipped.vtt"
    target.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(audio)) as handle:
        duration = handle.getnframes() / handle.getframerate()
    lines = source.read_text(encoding="utf-8").splitlines()
    output: list[str] = []
    original = 0
    kept = 0
    clipped = 0
    max_end = 0.0
    i = 0
    while i < len(lines):
        match = TIMESTAMP.match(lines[i])
        if not match:
            output.append(lines[i])
            i += 1
            continue
        original += 1
        start = seconds(match.group(1))
        end = seconds(match.group(2))
        max_end = max(max_end, end)
        body: list[str] = []
        i += 1
        while i < len(lines) and lines[i].strip():
            body.append(lines[i])
            i += 1
        if start >= duration:
            continue
        new_end = min(end, duration)
        if new_end <= start:
            continue
        if new_end != end:
            clipped += 1
        kept += 1
        output.append(f"{stamp(start)} --> {stamp(new_end)}{match.group(3)}")
        output.extend(body)
        output.append("")
    target.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    issue = "timestamp fora de la durada del WAV"
    if person == "pa-047":
        issue += "; repetició ASR conservada"
    return {
        "id_persona": person,
        "transcripcio_font": str(source.relative_to(ROOT.parent)),
        "derivat_qa": str(target.relative_to(ROOT.parent)),
        "durada_audio_s": f"{duration:.3f}",
        "max_timestamp_original_s": f"{max_end:.3f}",
        "cues_originals": str(original),
        "cues_conservades": str(kept),
        "cues_limitades": str(clipped),
        "incidencia": issue,
        "estat": "derivat-qa-pendent-audicio",
    }


def main() -> None:
    rows = [process(person) for person in ("pa-028", "pa-047")]
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} derivats QA generats · {OUT}")


if __name__ == "__main__":
    main()
