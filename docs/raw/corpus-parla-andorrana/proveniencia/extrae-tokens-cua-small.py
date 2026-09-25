"""Localitza les formes candidates dins dels JSON small de la cua completa."""

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


def words(tokens: list[dict]) -> list[dict[str, object]]:
    out = []
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


def main() -> None:
    with (PROV / "qa-cua-small-json.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    result_rows = []
    occurrences = []
    for row in rows:
        payload = json.loads((PROV / row["json_small"]).read_text(encoding="utf-8"))
        target = norm(row["forma"])
        start_clip = float(row["interval_escolta"].split("-")[0])
        matches = []
        for segment in payload.get("transcription", []):
            seq = words(segment.get("tokens", []))
            for i in range(len(seq)):
                for j in range(i + 1, min(len(seq), i + 4) + 1):
                    text = " ".join(str(item["text"]) for item in seq[i:j])
                    if norm(text) != target:
                        continue
                    local_start = float(seq[i]["from"]) / 1000
                    local_end = float(seq[j - 1]["to"]) / 1000
                    match = {"occurrence": len(matches) + 1, "local_start_s": f"{local_start:.3f}", "local_end_s": f"{local_end:.3f}", "absolute_start_s": f"{start_clip + local_start:.3f}", "absolute_end_s": f"{start_clip + local_end:.3f}", "prob_min": f"{min(float(item['p']) for item in seq[i:j]):.4f}", "text": text}
                    matches.append(match)
                    occurrences.append({"id_persona": row["id_persona"], "forma": row["forma"], "clip": row["clip"], **match})
        result_rows.append({"id_persona": row["id_persona"], "forma": row["forma"], "interval_escolta": row["interval_escolta"], "clip": row["clip"], "json_small": row["json_small"], "n_matches": str(len(matches)), "token_match": "sí" if matches else "no", "token_matches": json.dumps(matches, ensure_ascii=False, separators=(",", ":"))})
    fields = ["id_persona", "forma", "interval_escolta", "clip", "json_small", "n_matches", "token_match", "token_matches"]
    with (PROV / "qa-cua-small-tokens.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(result_rows)
    occurrence_fields = ["id_persona", "forma", "clip", "occurrence", "local_start_s", "local_end_s", "absolute_start_s", "absolute_end_s", "prob_min", "text"]
    with (PROV / "qa-cua-small-token-occurrences.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=occurrence_fields, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(occurrences)
    print(f"{len(result_rows)} clips · {sum(r['token_match'] == 'sí' for r in result_rows)} amb token · {len(occurrences)} ocurrències")


if __name__ == "__main__":
    main()
