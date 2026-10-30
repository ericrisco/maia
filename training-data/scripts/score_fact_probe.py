"""Scores fact recall on the held-out probe questions, before and after training.

Each probe question in training-data/facts/canon-facts-probe.jsonl lists the groups of keywords
a correct answer must contain ("expect": every group must match at least one of its alternatives).
The samples come from training/train.py (`samples_before.md` and `samples.md`, written with greedy
decoding).

Usage:
    python training-data/scripts/score_fact_probe.py runs/<run>/output
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROBE = ROOT / "training-data" / "facts" / "canon-facts-probe.jsonl"


def read_samples(path: Path) -> dict[str, str]:
    """Question -> answer, from a samples markdown file (## question, blank line, answer)."""
    blocks = re.split(r"^## ", path.read_text(encoding="utf-8"), flags=re.M)[1:]
    out = {}
    for block in blocks:
        question, _, answer = block.partition("\n")
        out[question.strip()] = answer.strip()
    return out


def recalls(answer: str, expect: list[list[str]]) -> bool:
    text = answer.lower()
    return all(any(alt.lower() in text for alt in group) for group in expect)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output", type=Path, help="run output folder with samples_before.md and samples.md"
    )
    args = parser.parse_args()

    probes = [json.loads(line) for line in PROBE.open(encoding="utf-8")]
    files = {"before": args.output / "samples_before.md", "after": args.output / "samples.md"}
    samples = {k: read_samples(p) for k, p in files.items() if p.exists()}
    scores = {k: 0 for k in samples}
    lines = []
    for probe in probes:
        marks = []
        for k, answers in samples.items():
            ok = recalls(answers.get(probe["question"], ""), probe["expect"])
            scores[k] += ok
            marks.append(f"{k}={'✓' if ok else '✗'}")
        lines.append(f"{' '.join(marks)}  {probe['fact_id']}")
    print("\n".join(lines))
    for k, n in scores.items():
        print(f"{k}: {n}/{len(probes)} facts recalled ({100 * n / len(probes):.0f} %)")


if __name__ == "__main__":
    main()
