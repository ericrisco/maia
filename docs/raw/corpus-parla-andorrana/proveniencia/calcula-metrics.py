"""Calcula mètriques comparables de ritme, pauses i confiança de cada ASR.

Les mètriques descriuen el senyal i la sortida del model; no són etiquetes
dialectals. El resultat és regenerable a ``analisi-metrics.tsv``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from statistics import median

ROOT = Path(__file__).parents[1]
WORD_RE = re.compile(r"\b[\wàèéíòóúïüç']+\b", re.UNICODE)


def metrics(pid: str) -> dict[str, str]:
    data = json.loads((ROOT / "transcripcions" / f"{pid}.json").read_text())
    segments = data["transcription"]
    text = (ROOT / "transcripcions" / f"{pid}.txt").read_text()
    words = WORD_RE.findall(text.lower())
    lexical = [
        token
        for segment in segments
        for token in segment["tokens"]
        if not token["text"].startswith(("[_", "<|")) and re.search(r"\w", token["text"])
    ]
    starts = [segment["offsets"]["from"] for segment in segments]
    ends = [segment["offsets"]["to"] for segment in segments]
    durations = [max(0, end - start) for start, end in zip(starts, ends) if end >= start]
    gaps = [max(0, starts[i] - ends[i - 1]) for i in range(1, len(starts))]
    span_ms = max(0, (max(ends) if ends else 0) - (min(starts) if starts else 0))
    active_ms = sum(durations)
    low = sum(1 for token in lexical if token["p"] < 0.55)
    ps = [float(token["p"]) for token in lexical]
    return {
        "id_persona": pid,
        "segments": str(len(segments)),
        "paraules": str(len(words)),
        "durada_asr_s": f"{span_ms / 1000:.2f}",
        "paraules_minut_span": f"{(len(words) / (span_ms / 60000)) if span_ms else 0:.2f}",
        "durada_segments_s": f"{active_ms / 1000:.2f}",
        "pausa_estimada_s": f"{sum(gaps) / 1000:.2f}",
        "pausa_percent_span": f"{(sum(gaps) / span_ms * 100) if span_ms else 0:.2f}",
        "segment_mitja_s": f"{(sum(durations) / len(durations) / 1000) if durations else 0:.2f}",
        "segment_mediana_s": f"{(median(durations) / 1000) if durations else 0:.2f}",
        "tokens_lexics": str(len(lexical)),
        "tokens_baixa_conf": str(low),
        "percent_baixa_conf": f"{(low / len(lexical) * 100) if lexical else 0:.2f}",
        "confiança_mitjana": f"{(sum(ps) / len(ps)) if ps else 0:.3f}",
    }


def main() -> None:
    rows = [metrics(path.stem) for path in sorted((ROOT / "transcripcions").glob("pa-*.json"))]
    out = ROOT / "proveniencia" / "analisi-metrics.tsv"
    fields = list(rows[0])
    with out.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(fields) + "\n")
        for row in rows:
            handle.write("\t".join(row[field] for field in fields) + "\n")
    print(f"{len(rows)} mostres · {out}")


if __name__ == "__main__":
    main()
