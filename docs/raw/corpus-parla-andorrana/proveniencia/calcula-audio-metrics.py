"""Extracta pauses i volum del WAV, independentment de l'ASR."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from statistics import median

ROOT = Path(__file__).parents[1]
SILENCE = re.compile(r"silence_duration: ([0-9.]+)")
MEAN = re.compile(r"mean_volume: ([^ ]+) dB")
MAX = re.compile(r"max_volume: ([^ ]+) dB")


def measure(pid: str) -> dict[str, str]:
    audio = ROOT / "audios" / pid / "audio.wav"
    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(audio),
            "-af",
            "silencedetect=noise=-35dB:d=0.30,volumedetect",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    log = result.stderr
    pauses = [float(v) for v in SILENCE.findall(log)]
    mean = MEAN.search(log)
    peak = MAX.search(log)
    return {
        "id_persona": pid,
        "pauses_audio": str(len(pauses)),
        "silenci_total_s": f"{sum(pauses):.2f}",
        "silenci_mediana_s": f"{median(pauses) if pauses else 0:.2f}",
        "silenci_max_s": f"{max(pauses) if pauses else 0:.2f}",
        "mean_volume_db": mean.group(1) if mean else "",
        "max_volume_db": peak.group(1) if peak else "",
    }


def main() -> None:
    pids = sorted(p.parent.name for p in (ROOT / "audios").glob("pa-*/audio.wav"))
    rows = [measure(pid) for pid in pids]
    out = ROOT / "proveniencia" / "analisi-audio-metrics.tsv"
    fields = list(rows[0])
    with out.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(fields) + "\n")
        for row in rows:
            handle.write("\t".join(row[field] for field in fields) + "\n")
    print(f"{len(rows)} àudios · {out}")


if __name__ == "__main__":
    main()
