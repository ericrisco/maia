"""Resumeix la passada ASR alternativa sobre les 237 finestres de quarantena."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "proveniencia" / "qa-quarantena-20s-alt"
OUT = ROOT / "proveniencia" / "qa-quarantena-20s-alt-resum.tsv"


def main() -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(SOURCE.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        texts = [segment.get("text", "").strip() for segment in data.get("transcription", [])]
        joined = " ".join(texts)
        words = re.findall(r"[\wÀ-ÿ']+", joined.casefold())
        trigrams = [tuple(words[i : i + 3]) for i in range(len(words) - 2)]
        ratio = 1 - len(set(trigrams)) / len(trigrams) if trigrams else 0.0
        state = "bucle-asr" if ratio >= 0.5 else ("silenci" if not joined.strip() or joined.strip() == "#" else "text-localitzable")
        rows.append(
            {
                "id_clip": path.stem,
                "transcripcio": path.with_suffix(".txt").name,
                "segments": str(len(texts)),
                "caracters": str(len(joined)),
                "repeticio_trigramas": f"{ratio:.4f}",
                "estat": state,
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} finestres · {dict(Counter(row['estat'] for row in rows))} · {OUT}")


if __name__ == "__main__":
    main()
