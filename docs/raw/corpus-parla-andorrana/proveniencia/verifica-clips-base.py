"""Segona corroboració ASR dels 656 clips amb el model base independent."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
import hashlib
import re
import subprocess
import unicodedata

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "qa-clips-base"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-base.bin")


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    return "".join(ch for ch in value if unicodedata.category(ch) != "Mn")


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", norm(value)).strip("-")


def run_one(row: dict[str, str]) -> dict[str, str]:
    clip = PROV / row["clip"]
    stem = f"{row['id_persona']}__{slug(row['forma'])}__{row['interval_escolta'].replace('.', '_').replace('-', '_')}"
    prefix = OUT / stem
    txt = prefix.with_suffix(".txt")
    log = prefix.with_suffix(".log")
    if not txt.exists():
        cmd = [
            "whisper-cli", "-m", str(MODEL), "-l", "ca", "-t", "8", "-mc", "0",
            "-bs", "5", "-bo", "5", "-nf", "-otxt", "-of", str(prefix), str(clip),
        ]
        with log.open("w", encoding="utf-8") as handle:
            result = subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"whisper-cli base ha fallat: {row['id_persona']} {row['forma']}")
    text = txt.read_text(encoding="utf-8", errors="replace").strip().replace("\n", " ")
    target = norm(row["forma"])
    transcript = norm(text)
    return {
        "forma": row["forma"],
        "id_persona": row["id_persona"],
        "interval_escolta": row["interval_escolta"],
        "clip": row["clip"],
        "sha256": hashlib.sha256(clip.read_bytes()).hexdigest(),
        "transcripcio_base": f"qa-clips-base/{txt.name}",
        "text_base": text,
        "forma_en_base": "sí" if target in transcript else "no",
    }


def main() -> None:
    with (PROV / "clips-audicio.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    OUT.mkdir(exist_ok=True)
    results: dict[tuple[str, str], dict[str, str]] = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(run_one, row): (row["id_persona"], row["forma"]) for row in rows}
        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()
            print(key, results[key]["forma_en_base"])
    output = PROV / "qa-clips-base.tsv"
    fields = ["forma", "id_persona", "interval_escolta", "clip", "sha256", "transcripcio_base", "text_base", "forma_en_base"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(results[(row["id_persona"], row["forma"])])
    print(f"{len(rows)} clips · {output}")


if __name__ == "__main__":
    main()
