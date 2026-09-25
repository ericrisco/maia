"""Construeix una cua temporal i estratificada per a l'escolta humana.

No etiqueta cap forma com a confirmada: només combina el primer interval de
cada parlant/forma amb la confiança ASR, el consens entre dos passades i les
mètriques acústiques del WAV.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]


def _base_hits(pid: str, form: str) -> list[tuple[float, float, float, str]]:
    path = ROOT / "proveniencia" / pid / "qa-base" / "transcripcio.json"
    if not path.exists():
        return []
    pattern = re.compile(r"(?i)(?<!\w)" + re.escape(form) + r"(?!\w)")
    hits = []
    data = json.loads(path.read_bytes().decode("utf-8", errors="replace"))
    for segment in data.get("transcription", []):
        text = segment.get("text", "")
        if not pattern.search(text):
            continue
        start = segment["offsets"]["from"] / 1000
        end = segment["offsets"]["to"] / 1000
        probs = [float(token["p"]) for token in segment.get("tokens", []) if re.search(r"\w", token.get("text", ""))]
        hits.append((start, end, min(probs) if probs else 1.0, text.strip()))
    return hits


def main() -> None:
    prosody = {}
    with (ROOT / "proveniencia" / "analisi-prosodia.tsv").open(encoding="utf-8", newline="") as handle:
        prosody = {row["id_persona"]: row for row in csv.DictReader(handle, delimiter="\t")}
    cross = {}
    with (ROOT / "proveniencia" / "auditoria-creuada-asr.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            cross[(row["id_persona"], row["forma"])] = row
    rows = []
    with (ROOT / "grafo" / "auditoria-formes.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            interval = row["segments_temporals"].split(",", 1)[0]
            start, end = (float(value) for value in interval.split("-", 1))
            start = max(0.0, start - 0.75)
            end += 0.75
            qa = cross.get((row["parlant"], row["forma"]), {})
            ac = prosody.get(row["parlant"], {})
            base_hits = _base_hits(row["parlant"], row["forma"])
            base_interval = ""
            base_conf = ""
            overlap = "no"
            for base_start, base_end, base_min, _ in base_hits:
                if base_end >= start and base_start <= end:
                    base_interval = f"{base_start:.2f}-{base_end:.2f}"
                    base_conf = f"{base_min:.3f}"
                    overlap = "sí"
                    break
            slug = re.sub(r"[^a-z0-9]+", "-", row["forma"].lower()).strip("-")
            consensus = qa.get("consens_dos_asr", "") == "sí"
            rows.append(
                {
                    "forma": row["forma"],
                    "id_persona": row["parlant"],
                    "estat_persona": ac.get("estat", ""),
                    "interval_font": interval,
                    "interval_escolta": f"{start:.2f}-{end:.2f}",
                    "interval_base": base_interval,
                    "coincidencia_temporal_asr": overlap,
                    "conf_min_segment": row["conf_min_segment"],
                    "conf_min_base_segment": base_conf,
                    "prioritat_asr": row["prioritat"],
                    "consens_dos_asr": "sí" if consensus else "no",
                    "ratio_veu_wav": ac.get("ratio_veu", ""),
                    "f0_median_hz_orientatiu": ac.get("f0_median_hz", ""),
                    "clip_suggerit": f"clips/{row['parlant']}__{slug}__{start:.2f}.wav",
                    "estat_audicio": "pendent",
                    "forma_confirmada_auditivament": "",
                    "nota_audicio": "",
                    "trets_fonetics_observats": "",
                }
            )
    out = ROOT / "proveniencia" / "cua-audicio.tsv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} intervals · {out}")


if __name__ == "__main__":
    main()
