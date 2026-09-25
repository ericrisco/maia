"""Audita audio i derivats ASR dels 124 clips candidats separats."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
SOURCE = PROV / "auditoria-candidats-completa.html"
OUT = PROV / "auditoria-integritat-transcripcions-candidats.tsv"


def load_items() -> list[dict[str, str]]:
    text = SOURCE.read_text(encoding="utf-8")
    match = re.search(r"const items=(\[.*?\]);const key=", text, re.DOTALL)
    if not match:
        raise ValueError(f"no trobo els clips candidats a {SOURCE}")
    return json.loads(match.group(1))


def file_info(path: Path) -> tuple[str, str]:
    if not path.exists():
        return "no", ""
    return "sí", str(path.stat().st_size)


def main() -> None:
    rows = []
    for item in load_items():
        audio = PROV / item["clip"]
        small = PROV / item["small_transcript"]
        base = PROV / item["base_transcript"]
        audio_exists, audio_bytes = file_info(audio)
        small_exists, small_bytes = file_info(small)
        base_exists, base_bytes = file_info(base)
        rows.append({
            "id": item["id"], "candidate": item["candidate"], "forma": item["form"], "clip": item["clip"],
            "audio_sha256": hashlib.sha256(audio.read_bytes()).hexdigest() if audio.exists() else "",
            "audio_exists": audio_exists, "audio_bytes": audio_bytes,
            "transcripcio_small": item["small_transcript"], "small_exists": small_exists, "small_bytes": small_bytes,
            "transcripcio_base": item["base_transcript"], "base_exists": base_exists, "base_bytes": base_bytes,
            "estat": "complet" if audio_exists == small_exists == base_exists == "sí" else "pendent",
        })
    fields = list(rows[0])
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    complete = sum(row["estat"] == "complet" for row in rows)
    print(f"{len(rows)} clips candidats auditats · complets={complete} · {OUT}")


if __name__ == "__main__":
    main()
