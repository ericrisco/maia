from pathlib import Path
import csv
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).parents[1]

def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

def one(row: dict, outdir: Path) -> tuple[str, str, int]:
    name = f"{row['id_persona']}__{slug(row['forma'])}"
    clip = ROOT / "proveniencia" / row["clip_suggerit"]
    prefix = outdir / name
    log = outdir / f"{name}.log"
    cmd = [
        "whisper-cli", "-m", "/Users/ericrisco/.codex/local-maia-models/ggml-small.bin",
        "-l", "ca", "-t", "8", "-mc", "0", "-bs", "5", "-bo", "5", "-nf",
        "-otxt", "-of", str(prefix), str(clip),
    ]
    with log.open("w") as handle:
        result = subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT)
    return row["id_persona"], row["forma"], result.returncode

def main() -> None:
    with (ROOT / "proveniencia" / "pla-audicio.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    chosen = {}
    for row in rows:
        if row["id_persona"] not in chosen:
            chosen[row["id_persona"]] = row
    outdir = ROOT / "proveniencia" / "qa-beam"
    outdir.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(one, row, outdir) for row in chosen.values()]
        for future in as_completed(futures):
            print(future.result())
    manifest = ROOT / "proveniencia" / "qa-beam.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["id_persona", "forma", "clip", "transcripcio_beam", "estat"])
        for row in chosen.values():
            name = f"{row['id_persona']}__{slug(row['forma'])}"
            writer.writerow([row["id_persona"], row["forma"], row["clip_suggerit"], f"qa-beam/{name}.txt", "pendent-comparacio"])
    print(f"{len(chosen)} clips · {manifest}")

if __name__ == "__main__":
    main()
