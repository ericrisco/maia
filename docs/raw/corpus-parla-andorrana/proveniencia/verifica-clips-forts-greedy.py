"""Tercera decodificació dels clips forts amb cerca greedy.

És una comprovació de sensibilitat del descodificador small, no una decisió
auditiva. La forma només es conserva com a candidata fins a escoltar el clip.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
import hashlib
import re
import subprocess
import unicodedata

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "qa-clips-forts-greedy"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-small.bin")


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
            "-bs", "1", "-bo", "1", "-nf", "-otxt", "-of", str(prefix), str(clip),
        ]
        with log.open("w", encoding="utf-8") as handle:
            result = subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"whisper-cli greedy ha fallat: {row['id_persona']} {row['forma']}")
    text = txt.read_text(encoding="utf-8", errors="replace").strip().replace("\n", " ")
    target = norm(row["forma"])
    return {
        "id_persona": row["id_persona"],
        "forma": row["forma"],
        "interval_escolta": row["interval_escolta"],
        "clip": row["clip"],
        "sha256": hashlib.sha256(clip.read_bytes()).hexdigest(),
        "transcripcio_greedy": f"qa-clips-forts-greedy/{txt.name}",
        "text_greedy": text,
        "forma_en_greedy": "sí" if target in norm(text) else "no",
    }


def main() -> None:
    with (PROV / "candidats-forts.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    OUT.mkdir(exist_ok=True)
    results: dict[tuple[str, str], dict[str, str]] = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(run_one, row): (row["id_persona"], row["forma"]) for row in rows}
        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()
            print(key, results[key]["forma_en_greedy"])
    fields = ["id_persona", "forma", "interval_escolta", "clip", "sha256", "transcripcio_greedy", "text_greedy", "forma_en_greedy"]
    with (PROV / "qa-clips-forts-greedy.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(results[(row["id_persona"], row["forma"])])
    print(f"{len(rows)} clips forts · {sum(r['forma_en_greedy'] == 'sí' for r in results.values())} coincidències · qa-clips-forts-greedy.tsv")


if __name__ == "__main__":
    main()
