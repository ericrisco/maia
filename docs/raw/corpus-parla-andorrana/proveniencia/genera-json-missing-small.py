"""Contrasta els 14 clips sense token base amb JSON complet del model small."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
import json
import re
import subprocess
import unicodedata

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "qa-token-missing-small-json"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-small.bin")


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    return "".join(ch for ch in value if unicodedata.category(ch) != "Mn")


def stem(row: dict[str, str]) -> str:
    value = row["clip"].replace("clips/", "").replace(".wav", "")
    return re.sub(r"[^a-zA-Z0-9_\-]+", "_", value)


def words(tokens: list[dict]) -> list[str]:
    out: list[str] = []
    for token in tokens:
        text = token.get("text", "")
        if text.startswith(("[_", "<|")) or not re.search(r"\w", text):
            continue
        if text.startswith(" ") or not out:
            out.append(text.strip())
        else:
            out[-1] = f"{out[-1]}{text}".strip()
    return out


def run_one(row: dict[str, str]) -> dict[str, str]:
    prefix = OUT / stem(row)
    json_path = prefix.with_suffix(".json")
    log_path = prefix.with_suffix(".log")
    if not json_path.exists():
        cmd = [
            "whisper-cli", "-m", str(MODEL), "-l", "ca", "-t", "8", "-mc", "0",
            "-bs", "5", "-bo", "5", "-nf", "-ojf", "-otxt", "-of", str(prefix), str(PROV / row["clip"]),
        ]
        with log_path.open("w", encoding="utf-8") as handle:
            result = subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"fallada JSON small {row['id_persona']} {row['forma']}")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    target = norm(row["forma"])
    candidates = []
    for segment in payload.get("transcription", []):
        seq = words(segment.get("tokens", []))
        for i in range(len(seq)):
            for j in range(i + 1, min(len(seq), i + 4) + 1):
                text = " ".join(seq[i:j])
                if norm(text) == target:
                    candidates.append(text)
    return {
        "id_persona": row["id_persona"], "forma": row["forma"], "interval_escolta": row["interval_escolta"],
        "clip": row["clip"], "json_small": f"qa-token-missing-small-json/{json_path.name}",
        "n_token_matches": str(len(candidates)), "token_match_small": "sí" if candidates else "no",
        "token_texts_small": json.dumps(candidates, ensure_ascii=False),
    }


def main() -> None:
    with (PROV / "prioritat-consens-token.tsv").open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["prioritat_token"] == "A-token-missing"]
    OUT.mkdir(exist_ok=True)
    results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(run_one, row): (row["id_persona"], row["forma"]) for row in rows}
        for future in as_completed(futures):
            result = future.result()
            results[(result["id_persona"], result["forma"])] = result
    fields = ["id_persona", "forma", "interval_escolta", "clip", "json_small", "n_token_matches", "token_match_small", "token_texts_small"]
    output = PROV / "qa-token-missing-small.tsv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(results[(row["id_persona"], row["forma"])])
    print(f"{len(rows)} clips · {sum(r['token_match_small'] == 'sí' for r in results.values())} token matches small · {output}")


if __name__ == "__main__":
    main()
