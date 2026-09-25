"""Filtra candidats A amb probabilitat tokenitzada mínima alta."""

from collections import defaultdict
from itertools import combinations
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = ROOT / "grafo"


def read(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    records = read(PROV / "registre-audicio.tsv")
    strong = []
    for row in records:
        values = [float(value) for value in row["token_prob_min"].split(";") if value]
        if row["categoria"] != "A-triple-consens" or row["token_coincidencia"] != "sí" or not values:
            continue
        if min(values) < 0.80:
            continue
        strong.append({
            "id_persona": row["id_persona"],
            "forma": row["forma"],
            "clip": row["clip"],
            "interval_escolta": row["interval_escolta"],
            "token_intervals_absolute": row["token_intervals_absolute"],
            "token_prob_min": row["token_prob_min"],
            "token_prob_mean": row["token_prob_mean"],
            "veu_proporcio": row["veu_proporcio"],
            "evidencia": "triple ASR + tokens QA amb p mínima >= 0,80; pendent d'audició",
        })
    output = PROV / "candidats-forts.tsv"
    fields = list(strong[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(strong)

    people_by_form = defaultdict(set)
    forms_by_person = defaultdict(set)
    for row in strong:
        people_by_form[row["forma"]].add(row["id_persona"])
        forms_by_person[row["id_persona"]].add(row["forma"])
    traits = [
        {"forma": form, "parlants": ",".join(sorted(people_by_form[form])), "comptatge": str(sum(r["forma"] == form for r in strong)), "estat": "candidat fort ASR; pendent d'audició"}
        for form in sorted(people_by_form) if len(people_by_form[form]) >= 3
    ]
    with (OUT / "trets-forts.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["forma", "parlants", "comptatge", "estat"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(traits)
    edges = []
    for left, right in combinations(sorted(forms_by_person), 2):
        shared = sorted(forms_by_person[left] & forms_by_person[right])
        if len(shared) < 2:
            continue
        edges.append({
            "origen": left, "desti": right, "pes": str(len(shared)),
            "formes_compartides": ",".join(shared),
            "evidencia": "candidats forts ASR; pendent d'audició",
        })
    with (OUT / "arestes-parlants-forts.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["origen", "desti", "pes", "formes_compartides", "evidencia"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(edges)
    with (OUT / "graf-parlants-forts.mmd").open("w", encoding="utf-8") as handle:
        handle.write("graph LR\n")
        for edge in edges:
            handle.write(f"  {edge['origen']} ---|{edge['pes']} formes fortes| {edge['desti']}\n")
    print(f"candidats={len(strong)} trets={len(traits)} arestes={len(edges)}")


if __name__ == "__main__":
    main()
