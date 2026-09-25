"""Obté timestamps JSON de la quarta passada per als clips A."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
import json
import re
import subprocess

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "qa-clips-json"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-small.bin")


def stem(row: dict) -> str:
    value = row["clip"].replace("clips/", "").replace(".wav", "")
    return re.sub(r"[^a-zA-Z0-9_\-]+", "_", value)


def one(row: dict):
    name = stem(row)
    prefix = OUT / name
    json_path = prefix.with_suffix(".json")
    log_path = prefix.with_suffix(".log")
    if not json_path.exists():
        cmd = [
            "whisper-cli", "-m", str(MODEL), "-l", "ca", "-t", "8", "-mc", "0",
            "-bs", "5", "-bo", "5", "-nf", "-oj", "-otxt", "-of", str(prefix),
            str(PROV / row["clip"]),
        ]
        with log_path.open("w", encoding="utf-8") as handle:
            result = subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"fallada JSON {row['id_persona']} {row['forma']}")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    segments = payload.get("transcription", [])
    return {
        "id_persona": row["id_persona"],
        "forma": row["forma"],
        "clip": row["clip"],
        "json": f"qa-clips-json/{json_path.name}",
        "segments": json.dumps(segments, ensure_ascii=False, separators=(",", ":")),
        "estat": "pendent-audicio",
    }


def main() -> None:
    with (PROV / "prioritat-audicio.tsv").open(encoding="utf-8", newline="") as handle:
        rows = [r for r in csv.DictReader(handle, delimiter="\t") if r["categoria"] == "A-triple-consens"]
    OUT.mkdir(exist_ok=True)
    results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(one, row): (row["id_persona"], row["forma"]) for row in rows}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    output = PROV / "qa-clips-json.tsv"
    fields = ["id_persona", "forma", "clip", "json", "segments", "estat"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(results[(row["id_persona"], row["forma"])])
    print(f"{len(rows)} clips A · {output}")


if __name__ == "__main__":
    main()
