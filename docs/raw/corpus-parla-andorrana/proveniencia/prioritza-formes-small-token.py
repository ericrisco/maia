"""Ordena les formes small per preparar la revisió auditiva compartida."""

from collections import defaultdict
from pathlib import Path
from statistics import median
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def main() -> None:
    with (PROV / "qa-cua-small-token-occurrences.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["forma"]].append(row)
    ranked = []
    for form, items in grouped.items():
        speakers = sorted({row["id_persona"] for row in items})
        probabilities = [float(row["prob_min"]) for row in items]
        n_speakers = len(speakers); med_p = median(probabilities)
        if n_speakers >= 25 and med_p >= 0.60:
            priority = "A-molts-parlants"
        elif n_speakers >= 20 or med_p >= 0.80:
            priority = "B-cobertura-o-confiança"
        elif n_speakers >= 3:
            priority = "C-cobertura-limitada"
        else:
            priority = "D-escassa"
        ranked.append({"forma": form, "prioritat": priority, "n_parlants": str(n_speakers), "n_ocurrencies": str(len(items)), "prob_median": f"{med_p:.4f}", "prob_min": f"{min(probabilities):.4f}", "parlants": ",".join(speakers), "estat": "tokenització small; pendent d'audició"})
    rank_order = {"A-molts-parlants": 0, "B-cobertura-o-confiança": 1, "C-cobertura-limitada": 2, "D-escassa": 3}
    ranked.sort(key=lambda row: (rank_order[row["prioritat"]], -int(row["n_parlants"]), -float(row["prob_median"]), row["forma"]))
    with (PROV / "prioritat-formes-small-token.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ranked[0]), delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(ranked)
    lines = ["# Cua de formes — tokenització small", "", f"La cua conté **{len(ranked)} formes**, **{len(rows)} ocurrències** i **{len({row['id_persona'] for row in rows})} parlants**. La prioritat només ordena l'escolta.", ""]
    for priority in rank_order:
        forms = [row for row in ranked if row["prioritat"] == priority]
        if not forms: continue
        lines += [f"## {priority}", ""]
        for row in forms:
            lines += [f"### {row['forma']} · {row['n_parlants']} parlants · {row['n_ocurrencies']} ocurrències · p mediana {row['prob_median']}", f"Parlants: {row['parlants']}", ""]
            selected = []
            for occurrence in sorted((item for item in rows if item["forma"] == row["forma"]), key=lambda item: -float(item["prob_min"])):
                if occurrence["id_persona"] in {item["id_persona"] for item in selected}: continue
                selected.append(occurrence)
                if len(selected) >= 5: break
            for occurrence in selected:
                lines.append(f"- [{occurrence['id_persona']} · {occurrence['prob_min']}](<clips/{occurrence['clip'].split('clips/',1)[-1]}>) · {occurrence['absolute_start_s']}-{occurrence['absolute_end_s']} s · `{occurrence['text']}`")
            lines.append("")
    (PROV / "quadern-formes-small-token.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(ranked)} formes · {len(rows)} ocurrències · prioritat-formes-small-token.tsv")


if __name__ == "__main__":
    main()
