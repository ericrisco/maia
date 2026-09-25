"""Genera timestamps i probabilitats token per als clips consensuals amb ASR base."""

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
OUT = PROV / "qa-consens-base-json"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-base.bin")


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    return "".join(ch for ch in value if unicodedata.category(ch) != "Mn")


def stem(row: dict[str, str]) -> str:
    value = row["clip"].replace("clips/", "").replace(".wav", "")
    return re.sub(r"[^a-zA-Z0-9_\-]+", "_", value)


def millis(value: str) -> int:
    parts = value.replace(",", ".").split(":")
    return int(round((int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])) * 1000))


def words(tokens: list[dict]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for token in tokens:
        text = token.get("text", "")
        if text.startswith(("[_", "<|")) or not re.search(r"\w", text):
            continue
        if text.startswith(" ") or not out:
            out.append({"text": text.strip(), "p": float(token.get("p", 0)), "from": int(token["offsets"]["from"]), "to": int(token["offsets"]["to"])})
        else:
            out[-1]["text"] = f"{out[-1]['text']}{text}".strip()
            out[-1]["p"] = min(float(out[-1]["p"]), float(token.get("p", 0)))
            out[-1]["to"] = int(token["offsets"]["to"])
    return out


def run_one(row: dict[str, str]) -> tuple[dict[str, str], dict]:
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
            raise RuntimeError(f"fallada JSON base {row['id_persona']} {row['forma']}")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    target = norm(row["forma"])
    matches = []
    for segment in payload.get("transcription", []):
        seq = words(segment.get("tokens", []))
        for i in range(len(seq)):
            for j in range(i + 1, min(len(seq), i + 4) + 1):
                candidate = norm(" ".join(str(item["text"]) for item in seq[i:j]))
                if candidate == target:
                    start_abs = float(row["interval_escolta"].split("-")[0]) + float(seq[i]["from"]) / 1000
                    end_abs = float(row["interval_escolta"].split("-")[0]) + float(seq[j - 1]["to"]) / 1000
                    matches.append({"start": start_abs, "end": end_abs, "p_min": min(float(item["p"]) for item in seq[i:j]), "text": " ".join(str(item["text"]) for item in seq[i:j])})
    return {
        "id_persona": row["id_persona"],
        "forma": row["forma"],
        "interval_escolta": row["interval_escolta"],
        "clip": row["clip"],
        "json_base": f"qa-consens-base-json/{json_path.name}",
        "n_matches": str(len(matches)),
        "token_match": "sí" if matches else "no",
        "token_matches": json.dumps(matches, ensure_ascii=False, separators=(",", ":")),
    }, payload


def main() -> None:
    with (PROV / "qa-clips-consens.tsv").open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["consens_textual"] == "sí"]
    OUT.mkdir(exist_ok=True)
    results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(run_one, row): (row["id_persona"], row["forma"]) for row in rows}
        for future in as_completed(futures):
            result, _payload = future.result()
            results[(result["id_persona"], result["forma"])] = result
    output = PROV / "qa-consens-tokens-base.tsv"
    fields = ["id_persona", "forma", "interval_escolta", "clip", "json_base", "n_matches", "token_match", "token_matches"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(results[(row["id_persona"], row["forma"])])
    print(f"{len(rows)} clips consensuals · {sum(r['token_match'] == 'sí' for r in results.values())} amb token localitzat · {output}")


if __name__ == "__main__":
    main()
