"""Executa una tercera descodificació greedy sobre els clips dels candidats RTVA."""

from __future__ import annotations

import csv
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-small.bin")
CANDIDATES = [
    ("lead-rtva-002-ian-moya", "ian-moya"),
    ("lead-rtva-003-dj-neura", "dj-neura"),
    ("lead-rtva-004-joan-mico", "joan-mico"),
    ("lead-cg-001-xavier-espot", "xavier-espot"),
]


def match(text: str, form: str) -> bool:
    return re.search(rf"(?<![\wà-ÿ]){re.escape(form)}(?![\wà-ÿ])", text, re.I) is not None


def transcribe(candidate: str, stem: str) -> tuple[str, dict]:
    base = PROV / "candidats" / candidate
    clip = base / "clips" / f"{stem}.wav"
    out_dir = base / "qa-greedy"
    out_dir.mkdir(exist_ok=True)
    prefix = out_dir / stem
    json_path = prefix.parent / f"{prefix.name}.json"
    if not json_path.exists():
        log = prefix.parent / f"{prefix.name}.log"
        with log.open("w", encoding="utf-8") as handle:
            subprocess.run(
                ["whisper-cli", "-m", str(MODEL), "-l", "ca", "-t", "8", "-mc", "0", "-bs", "1", "-bo", "1", "-nf", "-oj", "-ojf", "-otxt", "-of", str(prefix), str(clip)],
                check=True, stdout=handle, stderr=subprocess.STDOUT,
            )
    data = json.loads(json_path.read_text(encoding="utf-8"))
    text = " ".join(segment.get("text", "").strip() for segment in data.get("transcription", []) if segment.get("text", "").strip())
    return text, data


def main() -> None:
    for candidate, _ in CANDIDATES:
        base = PROV / "candidats" / candidate
        manifest = list(csv.DictReader((base / "formes-clips.tsv").open(encoding="utf-8", newline=""), delimiter="\t"))
        consens = {row["forma"]: row for row in csv.DictReader((base / "formes-consens.tsv").open(encoding="utf-8", newline=""), delimiter="\t")}
        rows = []
        for item in manifest:
            stem = Path(item["clip"]).stem
            text, _ = transcribe(candidate, stem)
            rows.append({
                "forma": item["forma"], "clip": item["clip"], "small": item["small"], "base": item["base"],
                "greedy": "sí" if match(text, item["forma"]) else "no", "text_greedy": text,
                "estat": "tercera ASR greedy; pendent d'audició",
            })
        output = base / "qa-greedy.tsv"
        with output.open("w", encoding="utf-8", newline="") as handle:
            fields = list(rows[0])
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
        categories = Counter()
        for row in rows:
            n = int(row["small"] == "1") + int(row["base"] == "1") + int(row["greedy"] == "sí")
            categories[{3: "A-tres-models", 2: "B-dos-models", 1: "C-un-model", 0: "D-cap-model"}[n]] += 1
        (base / "informe-qa-greedy.md").write_text(
            f"""# Tercera descodificació greedy — {candidate}

La passada `greedy` usa `ggml-small.bin` amb beam 1 sobre els **{len(rows)} clips** de formes. El text és una tercera evidència ASR, no una decisió auditiva ni una atribució de veu.

| categoria | clips |
|---|---:|
""" + "\n".join(f"| {key} | {categories.get(key, 0)} |" for key in ["A-tres-models", "B-dos-models", "C-un-model", "D-cap-model"]) + "\n\nEl detall és a `qa-greedy.tsv`; els JSON i TXT de cada clip es conserven a `qa-greedy/`.\n", encoding="utf-8")
        print(candidate, len(rows), dict(categories))


if __name__ == "__main__":
    main()
