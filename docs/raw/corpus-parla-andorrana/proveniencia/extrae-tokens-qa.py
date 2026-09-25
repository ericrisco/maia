"""Extreu temps i probabilitats dels tokens que formen la candidata."""

from pathlib import Path
import csv
import json
import re
import unicodedata

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    return "".join(ch for ch in value if unicodedata.category(ch) != "Mn")


def start_of(interval: str) -> float:
    return float(interval.split("-", 1)[0])


def extract(row: dict, payload: dict):
    tokens = []
    for segment in payload.get("transcription", []):
        tokens.extend(segment.get("tokens", []))
    clean = []
    stream = []
    mapping = []
    for token_index, token in enumerate(tokens):
        text = token.get("text", "")
        if text.startswith("[_") and text.endswith("]"):
            continue
        normalized = norm(text)
        if not normalized:
            continue
        clean.append(token)
        for char in normalized:
            stream.append(char)
            mapping.append(len(clean) - 1)
    stream = "".join(stream)
    target = norm(row["forma"])
    matches = []
    for match in re.finditer(r"(?<!\w)" + re.escape(target) + r"(?!\w)", stream):
        first = mapping[match.start()]
        last = mapping[match.end() - 1]
        selected = clean[first : last + 1]
        if not selected:
            continue
        offsets = [t.get("offsets", {}) for t in selected]
        start_ms = min(int(x.get("from", 0)) for x in offsets)
        end_ms = max(int(x.get("to", 0)) for x in offsets)
        probabilities = [float(t.get("p", 0.0)) for t in selected if t.get("p") is not None]
        matches.append({
            "id_persona": row["id_persona"],
            "forma": row["forma"],
            "clip": row["clip"],
            "ocurrencia": str(len(matches) + 1),
            "local_start_s": f"{start_ms / 1000:.3f}",
            "local_end_s": f"{end_ms / 1000:.3f}",
            "absolute_start_s": f"{start_of(row['interval_escolta']) + start_ms / 1000:.3f}",
            "absolute_end_s": f"{start_of(row['interval_escolta']) + end_ms / 1000:.3f}",
            "tokens": "".join(t.get("text", "") for t in selected).strip(),
            "prob_min": f"{min(probabilities):.4f}" if probabilities else "",
            "prob_mean": f"{sum(probabilities) / len(probabilities):.4f}" if probabilities else "",
            "tokens_count": str(len(selected)),
            "coincidencia_token": "sí",
            "estat": "ASR; pendent d'audicio",
        })
    if matches:
        return matches
    return [{
        "id_persona": row["id_persona"], "forma": row["forma"], "clip": row["clip"],
        "ocurrencia": "", "local_start_s": "", "local_end_s": "",
        "absolute_start_s": "", "absolute_end_s": "", "tokens": "",
        "prob_min": "", "prob_mean": "", "tokens_count": "0",
        "coincidencia_token": "no", "estat": "ASR; pendent d'audicio",
    }]


def main() -> None:
    with (PROV / "qa-clips-json-full.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    output_rows = []
    for row in rows:
        payload = json.loads((PROV / row["json_full"]).read_text(encoding="utf-8"))
        # The absolute interval is joined below from the canonical priority table.
        output_rows.extend(extract({**row, "interval_escolta": "0-0"}, payload))
    # Replace local zero offsets with the absolute clip interval from the queue.
    intervals = {}
    with (PROV / "prioritat-audicio.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            intervals[(row["id_persona"], row["forma"])] = row["interval_escolta"]
    for row in output_rows:
        interval = intervals[(row["id_persona"], row["forma"])]
        if row["local_start_s"]:
            start = start_of(interval)
            row["absolute_start_s"] = f"{start + float(row['local_start_s']):.3f}"
            row["absolute_end_s"] = f"{start + float(row['local_end_s']):.3f}"
    output = PROV / "qa-formes-tokens.tsv"
    fields = list(output_rows[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"{len(output_rows)} coincidències/token files · {output}")


if __name__ == "__main__":
    main()
