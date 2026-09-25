"""Genera clips d'audició per a les formes amb poca cobertura."""
from __future__ import annotations

import csv
import hashlib
import re
import subprocess
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "cua-audicio-formes-escasses.tsv"
CLIPS = PROV / "clips-formes-escasses"


def slug(value: str) -> str:
    value = unicodedata.normalize("NFD", value.casefold())
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    forms = {
        row["forma"]
        for row in csv.DictReader((ROOT / "grafo" / "trets-formes-completa.tsv").open(encoding="utf-8"), delimiter="\t")
        if int(row["n_persones_canoniques"]) < 10
    }
    evidence = [
        row
        for row in csv.DictReader((PROV / "evidencia-formes-vtt.tsv").open(encoding="utf-8"), delimiter="\t")
        if row["forma"] in forms
    ]
    by_form: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen: dict[str, set[str]] = defaultdict(set)
    for row in sorted(evidence, key=lambda item: (item["forma"], item["id_persona"], int(item["ocurrencia"]))):
        if row["id_persona"] not in seen[row["forma"]] and len(seen[row["forma"]]) < 3:
            by_form[row["forma"]].append(row)
            seen[row["forma"]].add(row["id_persona"])
    rows = []
    CLIPS.mkdir(parents=True, exist_ok=True)
    for order, forma in enumerate(sorted(forms), start=1):
        for rank, row in enumerate(by_form[forma], start=1):
            start = max(0.0, float(row["start_s"]) - 0.25)
            end = float(row["end_s"]) + 0.25
            relative = Path("clips-formes-escasses") / f"{slug(forma)}__{row['id_persona']}__{rank}.wav"
            output = PROV / relative
            audio = ROOT / "audios" / row["id_persona"] / "audio.wav"
            if not output.exists():
                subprocess.run(
                    ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-i", str(audio), "-t", f"{end-start:.3f}", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(output)],
                    check=True,
                )
            rows.append(
                {
                    "ordre": str(order),
                    "forma": forma,
                    "categoria": "territorial" if forma != "aviam" else "discurs",
                    "rang": str(rank),
                    "id_persona": row["id_persona"],
                    "interval_vtt": row["interval_vtt"],
                    "clip": str(relative),
                    "text_asr": row["text_segment"],
                    "sha256": sha256(output),
                    "decisio_humana": "pendent",
                    "observacio": "cua de revisió per cobertura escassa; ASR no confirmat",
                }
            )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} clips · {len(forms)} formes escasses · {OUT}")


if __name__ == "__main__":
    main()
