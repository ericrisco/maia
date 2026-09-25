"""Genera una resegmentació curta i reproducible de les veus en quarantena.

La sortida és evidència ASR auxiliar: no substitueix la transcripció canònica i
no marca cap decisió d'escolta. Les finestres curtes redueixen els bucles que
apareixen quan Whisper manté massa context en aquestes tres fonts.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import statistics
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
CLIP_DIR = PROV / "clips-quarantena-20s"
OUT_DIR = PROV / "qa-quarantena-20s"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-base.bin")
PERSONES = ("pa-044", "pa-047", "pa-050")
WINDOW_S = 20


def duration_seconds(audio: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def run_window(person: str, start: int, total: float) -> dict[str, str]:
    stem = f"{person}__{start:04d}"
    clip = CLIP_DIR / f"{stem}.wav"
    prefix = OUT_DIR / stem
    txt = prefix.with_suffix(".txt")
    vtt = prefix.with_suffix(".vtt")
    js = prefix.with_suffix(".json")
    if not clip.exists():
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(start), "-t", str(WINDOW_S), "-i", str(ROOT / "audios" / person / "audio.wav"), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(clip)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    if not txt.exists() or not vtt.exists() or not js.exists():
        subprocess.run(
            ["whisper-cli", "-m", str(MODEL), "-l", "ca", "-t", "8", "-mc", "0", "-bs", "5", "-bo", "5", "-nf", "-sow", "-otxt", "-ovtt", "-oj", "-of", str(prefix), str(clip)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    text = txt.read_text(encoding="utf-8", errors="replace")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "id_persona": person,
        "inici_s": str(start),
        "durada_s": f"{min(WINDOW_S, max(0.0, total - start)):.3f}",
        "clip": f"clips-quarantena-20s/{clip.name}",
        "transcripcio": f"qa-quarantena-20s/{txt.name}",
        "vtt": f"qa-quarantena-20s/{vtt.name}",
        "json": f"qa-quarantena-20s/{js.name}",
        "sha256": hashlib.sha256(clip.read_bytes()).hexdigest(),
        "linies": str(len(lines)),
        "linies_uniques": str(len(set(lines))),
        "ratio_uniques": f"{len(set(lines)) / len(lines):.4f}" if lines else "0.0000",
        "estat": "pendent-audicio",
    }


def main() -> None:
    CLIP_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)
    rows: list[dict[str, str]] = []
    for person in PERSONES:
        audio = ROOT / "audios" / person / "audio.wav"
        total = duration_seconds(audio)
        for start in range(0, math.ceil(total), WINDOW_S):
            rows.append(run_window(person, start, total))
    manifest = PROV / "qa-quarantena-20s.tsv"
    fields = list(rows[0])
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    for person in PERSONES:
        person_rows = [row for row in rows if row["id_persona"] == person]
        combined: list[str] = []
        for row in person_rows:
            txt = (PROV / row["transcripcio"]).read_text(encoding="utf-8", errors="replace")
            previous = None
            for line in (part.strip() for part in txt.splitlines()):
                if not line or line == previous:
                    continue
                combined.append(f"[{row['inici_s']}–{float(row['inici_s']) + float(row['durada_s']):g} s] {line}")
                previous = line
        (OUT_DIR / f"{person}-combinada.txt").write_text("\n".join(combined) + "\n", encoding="utf-8")
    report = [
        "# Resegmentació curta de les veus en quarantena",
        "",
        "Aquesta passada usa finestres no solapades de 20 segons i `ggml-base.bin`, sense context acumulat. És una transcripció ASR auxiliar per reduir bucles; no és una validació humana ni entra al graf.",
        "",
        "| veu | finestres | mitjana de línies úniques | finestres < 0,80 | transcripció combinada |",
        "|---|---:|---:|---:|---|",
    ]
    for person in PERSONES:
        person_rows = [row for row in rows if row["id_persona"] == person]
        ratios = [float(row["ratio_uniques"]) for row in person_rows]
        report.append(
            f"| {person} | {len(person_rows)} | {statistics.mean(ratios):.3f} | {sum(ratio < 0.80 for ratio in ratios)} | [`{person}-combinada.txt`](qa-quarantena-20s/{person}-combinada.txt) |"
        )
    report.extend([
        "",
        "Els fragments amb text coherent són candidats per a escolta i revisió. Les formes, variants, fonètica i prosòdia continuen pendents d'anotació auditiva.",
    ])
    (PROV / "informe-quarantena-20s.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"{len(rows)} finestres · {manifest}")


if __name__ == "__main__":
    main()
