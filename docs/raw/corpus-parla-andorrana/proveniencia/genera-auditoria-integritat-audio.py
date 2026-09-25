"""Audita els encapçalaments WAV dels àudios font i dels clips escoltables."""
from __future__ import annotations

import csv
import wave
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-integritat-audio.tsv"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def inspect(path: Path) -> tuple[str, str, str, str, str]:
    try:
        with wave.open(str(path)) as handle:
            channels = handle.getnchannels()
            sample_rate = handle.getframerate()
            frames = handle.getnframes()
            duration = frames / sample_rate if sample_rate else 0.0
            if channels < 1 or sample_rate < 8000 or frames == 0 or duration <= 0:
                return (f"{duration:.3f}", str(sample_rate), str(channels), "error", "encapçalament buit o invàlid")
            return (f"{duration:.3f}", str(sample_rate), str(channels), "ok", "")
    except (OSError, EOFError, wave.Error) as exc:
        return ("", "", "", "error", f"{type(exc).__name__}: {exc}")


def main() -> None:
    rows: list[dict[str, str]] = []
    for path in sorted((ROOT / "audios").glob("pa-*/audio.wav")):
        duration, rate, channels, state, note = inspect(path)
        rows.append(
            {
                "tipus": "font",
                "id": path.parent.name,
                "fitxer": str(path.relative_to(ROOT)),
                "durada_s": duration,
                "sample_rate_hz": rate,
                "canals": channels,
                "bytes": str(path.stat().st_size),
                "estat": state,
                "nota": note,
            }
        )
    for source in read(PROV / "clips-audicio.tsv"):
        path = PROV / source["clip"]
        duration, rate, channels, state, note = inspect(path)
        rows.append(
            {
                "tipus": "clip",
                "id": f"{source['id_persona']}::{source['forma']}::{source['interval_escolta']}",
                "fitxer": source["clip"],
                "durada_s": duration,
                "sample_rate_hz": rate,
                "canals": channels,
                "bytes": str(path.stat().st_size) if path.exists() else "",
                "estat": state,
                "nota": note,
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = ["tipus", "id", "fitxer", "durada_s", "sample_rate_hz", "canals", "bytes", "estat", "nota"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    errors = sum(row["estat"] == "error" for row in rows)
    print(f"{len(rows)} WAV auditats · errors={errors} · {OUT}")


if __name__ == "__main__":
    main()
