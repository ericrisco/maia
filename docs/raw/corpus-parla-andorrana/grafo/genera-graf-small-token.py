"""Construeix el graf de formes a partir de la tokenització small completa."""

from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
GRAPH = ROOT / "grafo"
MARKER = "### Formes QA small compartides"


def read_prov(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def replace_section(text: str, marker: str, section: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + section
    start = text.index(marker)
    next_heading = text.find("\n### ", start + len(marker))
    end = len(text) if next_heading == -1 else next_heading + 1
    return text[:start].rstrip() + "\n" + section.rstrip() + "\n\n" + text[end:].lstrip()


def main() -> None:
    occurrences = read_prov("qa-cua-small-token-occurrences.tsv")
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = list(csv.DictReader(handle, delimiter="\t"))
    by_form: dict[str, set[str]] = defaultdict(set)
    totals = Counter()
    by_person: dict[str, Counter[str]] = defaultdict(Counter)
    for row in occurrences:
        by_form[row["forma"]].add(row["id_persona"]); totals[row["forma"]] += 1; by_person[row["id_persona"]][row["forma"]] += 1
    trait_rows = []
    for form in sorted(by_form):
        speakers = sorted(by_form[form])
        trait_rows.append({"forma": form, "n_parlants": str(len(speakers)), "comptatge_total": str(totals[form]), "parlants": ",".join(speakers), "estat": "tokenització small; pendent d'audició"})
    fields = list(trait_rows[0])
    with (GRAPH / "trets-small-token.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(trait_rows)
    edge_rows = []
    speaker_features = {pid: set(counts) for pid, counts in by_person.items()}
    for a, b in combinations(sorted(speaker_features), 2):
        shared = sorted(speaker_features[a] & speaker_features[b])
        if len(shared) >= 3:
            edge_rows.append({"id_a": a, "id_b": b, "n_formes_compartides": str(len(shared)), "formes": ";".join(shared), "estat": "semblança tokenitzada small; pendent d'audició"})
    edge_fields = list(edge_rows[0]) if edge_rows else ["id_a", "id_b", "n_formes_compartides", "formes", "estat"]
    with (GRAPH / "arestes-parlants-small-token.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=edge_fields, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(edge_rows)
    lines = ["graph TD"]
    for i, row in enumerate(trait_rows, start=1):
        node = f"F{i}"; lines.append(f'  {node}["{row["forma"]}\\n{row["n_parlants"]} parlants"]')
        for pid in row["parlants"].split(","):
            pnode = f"P{pid.replace('-', '')}"; lines.append(f'  {pnode}("{pid}")'); lines.append(f"  {pnode} --> {node}")
    (GRAPH / "graf-parlants-small-token.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    matrix_rows = []
    for person in people:
        pid = person["id_persona"]
        for form in sorted(by_form):
            matrix_rows.append({"id_persona": pid, "forma": form, "recompte_token_small": str(by_person[pid][form]), "estat": "tokenització small; pendent d'audició"})
    with (GRAPH / "matriu-formes-small-token.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(matrix_rows[0]), delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(matrix_rows)
    reports = ROOT / "persones"
    for person in people:
        pid = person["id_persona"]; counts = by_person.get(pid, Counter()); report = reports / f"{pid}.md"; text = report.read_text(encoding="utf-8")
        if counts:
            detail = "; ".join(f"{form}={counts[form]}" for form in sorted(counts))
            section = f"\n{MARKER}\n\nLa tokenització small localitza **{sum(counts.values())} ocurrències** en {len(counts)} formes per a aquesta persona: {detail}. Són candidats automàtics i requereixen escolta.\n"
        else:
            section = f"\n{MARKER}\n\nNo hi ha formes tokenitzades en la cua small per a aquesta persona.\n"
        report.write_text(replace_section(text, MARKER, section), encoding="utf-8")
    print(f"{len(trait_rows)} formes · {len(edge_rows)} arestes · {len(matrix_rows)} cel·les · {len(speaker_features)} parlants amb tokens")


if __name__ == "__main__":
    main()
