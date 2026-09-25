"""Construeix una vista de candidats que reapareixen en la quarta passada ASR."""

from collections import defaultdict
from itertools import combinations
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = ROOT / "grafo"


def read_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    rows = read_rows(PROV / "qa-clips.tsv")
    by_form = defaultdict(set)
    by_person = defaultdict(set)
    for row in rows:
        if row["forma_en_qa"] != "sí":
            continue
        by_form[row["forma"]].add(row["id_persona"])
        by_person[row["id_persona"]].add(row["forma"])

    trait_rows = []
    for form in sorted(by_form):
        people = sorted(by_form[form])
        if len(people) < 3:
            continue
        total = sum(
            1 for row in rows
            if row["forma"] == form and row["forma_en_qa"] == "sí"
        )
        trait_rows.append({
            "forma": form,
            "parlants": ",".join(people),
            "comptatge_total": str(total),
            "veredicte": "candidat textual quarta passada; revisió auditiva pendent",
        })
    with (OUT / "trets-qa.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["forma", "parlants", "comptatge_total", "veredicte"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(trait_rows)

    edge_rows = []
    for left, right in combinations(sorted(by_person), 2):
        shared = sorted(by_person[left] & by_person[right])
        if len(shared) < 3:
            continue
        edge_rows.append({
            "origen": left,
            "desti": right,
            "relacio": "semblança textual provisional",
            "pes": str(len(shared)),
            "formes_compartides": ",".join(shared),
            "evidencia": "coincidència en clips de la quarta passada; revisió auditiva pendent",
        })
    with (OUT / "arestes-parlants-qa.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["origen", "desti", "relacio", "pes", "formes_compartides", "evidencia"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(edge_rows)

    with (OUT / "graf-parlants-qa.mmd").open("w", encoding="utf-8") as handle:
        handle.write("graph LR\n")
        for row in edge_rows:
            label = f"{row['pes']} formes QA"
            handle.write(f"  {row['origen']} ---|{label}| {row['desti']}\n")
    print(f"trets={len(trait_rows)} arestes={len(edge_rows)}")


if __name__ == "__main__":
    main()
