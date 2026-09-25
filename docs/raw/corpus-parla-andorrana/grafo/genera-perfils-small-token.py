"""Resumeix la cobertura de tokenització small per parlant."""

from collections import defaultdict
from pathlib import Path
from statistics import median
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
GRAPH = ROOT / "grafo"
MARKER = "### Perfil small comparatiu"


def replace_section(text: str, marker: str, section: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + section
    start = text.index(marker)
    next_heading = text.find("\n### ", start + len(marker))
    end = len(text) if next_heading == -1 else next_heading + 1
    return text[:start].rstrip() + "\n" + section.rstrip() + "\n\n" + text[end:].lstrip()


def main() -> None:
    with (PROV / "qa-cua-small-token-occurrences.tsv").open(encoding="utf-8", newline="") as handle:
        occurrences = list(csv.DictReader(handle, delimiter="\t"))
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = list(csv.DictReader(handle, delimiter="\t"))
    by_person = defaultdict(list)
    for row in occurrences: by_person[row["id_persona"]].append(row)
    rows = []
    for person in people:
        pid = person["id_persona"]; items = by_person.get(pid, []); forms = sorted({row["forma"] for row in items}); probs = [float(row["prob_min"]) for row in items]
        rows.append({"id_persona": pid, "nom_public": person["nom_public"], "estat_persona": person["estat"], "n_formes_small": str(len(forms)), "n_ocurrencies_small": str(len(items)), "prob_median": f"{median(probs):.4f}" if probs else "", "formes": ";".join(forms), "estat": "tokenització small; pendent d'audició"})
        report = ROOT / "persones" / f"{pid}.md"; text = report.read_text(encoding="utf-8")
        section = f"\n{MARKER}\n\nLa cobertura small d'aquesta persona és de **{len(forms)} formes** i **{len(items)} ocurrències** sobre les 20 formes de la cua; la probabilitat mediana és **{median(probs):.4f}**. És un resum comparatiu automàtic i requereix escolta.\n" if items else f"\n{MARKER}\n\nAquesta persona no té formes tokenitzades en la cua small; la cobertura queda pendent d'escolta.\n"
        report.write_text(replace_section(text, MARKER, section), encoding="utf-8")
    with (GRAPH / "nodes-small-token.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(rows)
    print(f"{len(rows)} perfils · {sum(int(r['n_ocurrencies_small']) > 0 for r in rows)} amb ocurrències")


if __name__ == "__main__":
    main()
