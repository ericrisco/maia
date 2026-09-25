"""Genera JSON amb tokens temporals per als 656 clips de la cua d'audició."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
import re
import subprocess

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "qa-cua-small-json"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-small.bin")


def stem(row: dict[str, str]) -> str:
    value = row["clip"].replace("clips/", "").replace(".wav", "")
    return re.sub(r"[^a-zA-Z0-9_\-]+", "_", value)


def run_one(row: dict[str, str]) -> dict[str, str]:
    prefix = OUT / stem(row)
    json_path = prefix.with_suffix(".json")
    log_path = prefix.with_suffix(".log")
    if not json_path.exists():
        cmd = [
            "whisper-cli", "-m", str(MODEL), "-l", "ca", "-t", "8", "-mc", "0",
            "-bs", "5", "-bo", "5", "-nf", "-oj", "-ojf", "-otxt", "-of", str(prefix), str(PROV / row["clip"]),
        ]
        with log_path.open("w", encoding="utf-8") as handle:
            result = subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"fallada JSON cua {row['id_persona']} {row['forma']}")
    return {"id_persona": row["id_persona"], "forma": row["forma"], "interval_escolta": row["interval_escolta"], "clip": row["clip"], "json_small": f"qa-cua-small-json/{json_path.name}", "estat": "pendent-audicio"}


def main() -> None:
    with (PROV / "clips-audicio.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    OUT.mkdir(exist_ok=True)
    results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(run_one, row): (row["id_persona"], row["forma"]) for row in rows}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    fields = ["id_persona", "forma", "interval_escolta", "clip", "json_small", "estat"]
    with (PROV / "qa-cua-small-json.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n"); writer.writeheader()
        for row in rows: writer.writerow(results[(row["id_persona"], row["forma"])])
    print(f"{len(rows)} clips amb JSON small · qa-cua-small-json.tsv")


if __name__ == "__main__":
    main()
