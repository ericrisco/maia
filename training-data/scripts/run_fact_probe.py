"""Answers the held-out probe questions with a local Ollama model (temperature 0).

Writes a samples markdown file in the format score_fact_probe.py reads (## question, blank line,
answer), so the base model and a fine-tuned GGUF can be compared under the same conditions.
The system prompt is the one used in training (training-data/missatge-sistema.txt).

Usage:
    python training-data/scripts/run_fact_probe.py gemma4:e4b runs/<run>/probe/samples_before.md
    python training-data/scripts/run_fact_probe.py maia-e4b:<tag> runs/<run>/probe/samples.md
    python training-data/scripts/score_fact_probe.py runs/<run>/probe
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROBE = ROOT / "training-data" / "facts" / "canon-facts-probe.jsonl"
SYSTEM = (ROOT / "training-data" / "missatge-sistema.txt").read_text(encoding="utf-8").strip()
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")


def answer(model: str, question: str) -> str:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question},
        ],
        "temperature": 0,
        "max_tokens": 300,
    }
    request = urllib.request.Request(
        f"{OLLAMA}/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=600) as response:
        return json.loads(response.read())["choices"][0]["message"]["content"].strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Ollama model name, e.g. gemma4:e4b")
    parser.add_argument("out", type=Path, help="samples markdown file to write")
    parser.add_argument("--threads", type=int, default=2)
    args = parser.parse_args()

    questions = [json.loads(line)["question"] for line in PROBE.open(encoding="utf-8")]
    with ThreadPoolExecutor(args.threads) as pool:
        answers = list(pool.map(lambda q: answer(args.model, q), questions))
    lines = [f"# Probe answers: {args.model}\n"]
    lines += [f"## {q}\n\n{a}\n" for q, a in zip(questions, answers, strict=True)]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(questions)} answers written to {args.out}")


if __name__ == "__main__":
    main()
