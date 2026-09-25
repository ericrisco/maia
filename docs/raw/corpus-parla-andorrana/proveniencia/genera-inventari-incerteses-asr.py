"""Genera un inventari localitzable dels tokens ASR de baixa confiança.

La taula és una cua de revisió: no corregeix la transcripció ni declara cap
variant dialectal. Cada fila conserva el segment JSON, l'interval d'àudio i,
si n'hi ha, els clips de formes que el contenen.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
THRESHOLD = 0.55
TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)


def seconds(value: str) -> float:
    h, m, s = value.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def clean_token(text: str) -> str:
    return text.strip().replace('\n', ' ')


def main() -> None:
    people = sorted((ROOT / "transcripcions").glob("*.json"))
    clips = []
    with (PROV / "cua-audicio.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            start, end = row["interval_escolta"].split("-")
            clips.append({
                **row,
                "start": float(start),
                "end": float(end),
            })

    rows = []
    for json_path in people:
        person = json_path.stem
        data = json.loads(json_path.read_text(encoding="utf-8"))
        for index, segment in enumerate(data.get("transcription", []), start=1):
            tokens = segment.get("tokens", [])
            low = []
            for token in tokens:
                text = clean_token(token.get("text", ""))
                probability = float(token.get("p", 0.0))
                if probability < THRESHOLD and TOKEN_RE.search(text) and not text.startswith("[_"):
                    low.append((text, probability))
            if not low:
                continue
            start = seconds(segment["timestamps"]["from"])
            end = seconds(segment["timestamps"]["to"])
            overlapping = [clip for clip in clips if clip["id_persona"] == person and clip["start"] < end and clip["end"] > start]
            forms = sorted({clip["forma"] for clip in overlapping})
            rows.append({
                "id_persona": person,
                "segment": index,
                "inici_s": f"{start:.3f}",
                "final_s": f"{end:.3f}",
                "token_baix": " | ".join(text for text, _ in low),
                "probabilitats_baixes": " | ".join(f"{p:.4f}" for _, p in low),
                "n_tokens_baixos": str(len(low)),
                "text_segment_asr": clean_token(segment.get("text", "")),
                "formes_cobertes": ";".join(forms),
                "clips_coberts": ";".join(clip["clip_suggerit"] for clip in overlapping),
                "llindar": f"p < {THRESHOLD:.2f}",
                "estat": "pendent d'audició",
            })

    output = PROV / "inventari-incerteses-asr.tsv"
    fields = list(rows[0]) if rows else [
        "id_persona", "segment", "inici_s", "final_s", "token_baix",
        "probabilitats_baixes", "n_tokens_baixos", "text_segment_asr",
        "formes_cobertes", "clips_coberts", "llindar", "estat",
    ]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    person_counts = Counter(row["id_persona"] for row in rows)
    form_counts = Counter(form for row in rows for form in row["formes_cobertes"].split(";") if form)
    summary = PROV / "inventari-incerteses-asr.md"
    lines = [
        "# Inventari d'incerteses ASR",
        "",
        f"La taula `inventari-incerteses-asr.tsv` conserva **{len(rows)} segments** amb almenys un token de probabilitat inferior a **{THRESHOLD:.2f}**. Cada fila apunta al segment JSON, al text ASR i als clips de la cua que el contenen.",
        "",
        "Aquesta és una cua d'audició i correcció de transcripció. Les formes i tokens són hipòtesis del model; no són variants dialectals ni observacions fonètiques.",
        "",
        f"- Persones amb almenys un segment: **{len(person_counts)}** de {len(people)}.",
        f"- Segments associats a algun clip de forma: **{sum(bool(row['clips_coberts']) for row in rows)}**.",
        "",
        "## Formes amb més segments incerts",
        "",
    ]
    for form, count in form_counts.most_common(20):
        lines.append(f"- `{form}`: {count} segments.")
    lines += [
        "",
        "Per tancar una fila cal escoltar l'interval i registrar la decisió, la variant escoltada i les observacions pertinents a `registre-audicio.tsv`.",
    ]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} segments incerts · {len(person_counts)} persones · {sum(bool(row['clips_coberts']) for row in rows)} amb clip")


if __name__ == "__main__":
    main()
