"""Ordena els consensos segons la debilitat de l'alineació tokenitzada."""

from __future__ import annotations

from pathlib import Path
import csv
import json

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def main() -> None:
    with (PROV / "qa-consens-tokens-base.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        matches = json.loads(row["token_matches"])
        probabilities = [float(match["p_min"]) for match in matches]
        row["token_p_min"] = f"{min(probabilities):.4f}" if probabilities else ""
        row["token_start_abs"] = f"{min(match['start'] for match in matches):.3f}" if matches else ""
        row["token_end_abs"] = f"{max(match['end'] for match in matches):.3f}" if matches else ""
        row["prioritat_token"] = "A-token-missing" if not probabilities else "B-token-low" if min(probabilities) < 0.55 else "C-token-strong"
    rows.sort(key=lambda row: ({"A-token-missing": 0, "B-token-low": 1, "C-token-strong": 2}[row["prioritat_token"]], float(row["token_p_min"] or 0), row["id_persona"], row["forma"]))
    fields = ["prioritat_token", "token_p_min", "token_start_abs", "token_end_abs", "id_persona", "forma", "interval_escolta", "clip", "json_base", "n_matches", "token_match", "token_matches"]
    out = PROV / "prioritat-consens-token.tsv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    from collections import Counter
    print(len(rows), dict(Counter(row["prioritat_token"] for row in rows)), out)


if __name__ == "__main__":
    main()
