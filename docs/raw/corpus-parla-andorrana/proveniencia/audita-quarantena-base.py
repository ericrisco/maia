"""Corrobora les finestres de quarantena amb el model base."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
import hashlib
import re
import subprocess

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "qa-quarantena-base"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-base.bin")


def stem(row: dict[str, str]) -> str:
    return Path(row["clip"]).stem


def run_one(row: dict[str, str]) -> dict[str, str]:
    clip = PROV / row["clip"]
    prefix = OUT / stem(row)
    txt = prefix.with_suffix(".txt")
    log = prefix.with_suffix(".log")
    if not txt.exists():
        cmd = ["whisper-cli", "-m", str(MODEL), "-l", "ca", "-t", "8", "-mc", "0", "-bs", "5", "-bo", "5", "-nf", "-otxt", "-of", str(prefix), str(clip)]
        with log.open("w", encoding="utf-8") as handle:
            result = subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"fallada quarantena base {row['id_persona']} {row['inici_s']}")
    text = txt.read_text(encoding="utf-8", errors="replace").strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "id_persona": row["id_persona"], "inici_s": row["inici_s"], "durada_s": row["durada_s"], "clip": row["clip"],
        "transcripcio_base": f"qa-quarantena-base/{txt.name}", "text_base": " ".join(lines),
        "linies_base": str(len(lines)), "linies_uniques_base": str(len(set(lines))),
        "ratio_uniques_base": f"{len(set(lines)) / len(lines):.4f}" if lines else "0.0000",
        "sha256": hashlib.sha256(clip.read_bytes()).hexdigest(),
    }


def main() -> None:
    with (PROV / "qa-quarantena.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    OUT.mkdir(exist_ok=True)
    results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(run_one, row): (row["id_persona"], row["inici_s"]) for row in rows}
        for future in as_completed(futures):
            result = future.result(); results[(result["id_persona"], result["inici_s"])] = result
    fields = ["id_persona", "inici_s", "durada_s", "clip", "transcripcio_base", "text_base", "linies_base", "linies_uniques_base", "ratio_uniques_base", "sha256"]
    output = PROV / "qa-quarantena-base.tsv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows: writer.writerow(results[(row["id_persona"], row["inici_s"])])
    print(f"{len(rows)} finestres · {output}")


if __name__ == "__main__":
    main()
