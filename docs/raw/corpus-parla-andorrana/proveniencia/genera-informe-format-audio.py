"""Resumeix el format i la normalització dels WAV del corpus."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-format-audio.md"


def main() -> None:
    with (PROV / "auditoria-integritat-audio.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    sources = [row for row in rows if row["tipus"] == "font"]
    clips = [row for row in rows if row["tipus"] == "clip"]
    source_formats = Counter((row["sample_rate_hz"], row["canals"]) for row in sources)
    clip_formats = Counter((row["sample_rate_hz"], row["canals"]) for row in clips)
    source_lines = ", ".join(f"{count} a {rate} Hz/{channels} canals" for (rate, channels), count in sorted(source_formats.items()))
    clip_lines = ", ".join(f"{count} a {rate} Hz/{channels} canals" for (rate, channels), count in sorted(clip_formats.items()))
    clips_ok = sum(row["sample_rate_hz"] == "16000" and row["canals"] == "1" and row["estat"] == "ok" for row in clips)
    sources_ok = sum(row["estat"] == "ok" for row in sources)
    lines = [
        "# Auditoria de format d'àudio",
        "",
        f"Les **{len(sources)} fonts** originals conserven el seu format d'origen: {source_lines}. Els **{len(clips)} clips d'audició** estan normalitzats a {clip_lines}.",
        "",
        f"- Fonts amb encapçalament WAV vàlid: **{sources_ok}/{len(sources)}**.",
        f"- Clips d'audició en PCM mono 16 kHz: **{clips_ok}/{len(clips)}**.",
        "- La normalització només afecta els clips derivats; els WAV font no es reescriuen.",
        "- Aquest control valida el contenidor i el format, no la identitat de veu ni cap tret fonètic.",
        "",
        "Font de dades: `auditoria-integritat-audio.tsv`.",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"fonts={len(sources)} clips={len(clips)} · clips_16k_mono={clips_ok} · {OUT}")


if __name__ == "__main__":
    main()
