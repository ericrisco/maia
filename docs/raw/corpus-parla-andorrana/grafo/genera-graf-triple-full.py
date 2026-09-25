"""Genera el graf estricte de les coincidències dels tres models."""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
GRAFO = ROOT / "grafo"


def read(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main():
    mapping = {row["id_persona"]: row for row in read(PROV / "persones-canonics.tsv")}
    people = {row["id_parlant"]: row for row in mapping.values()}
    rows = [row for row in read(PROV / "qa-clips-triple-full.tsv") if row["categoria"] == "A-tres-models"]
    forms = sorted({row["forma"] for row in rows})
    by_person = defaultdict(set)
    counts = Counter()
    for row in rows:
        speaker = mapping[row["id_persona"]]["id_parlant"]
        by_person[speaker].add(row["forma"])
        counts[(speaker, row["forma"])] += 1

    traits = []
    for form in forms:
        speakers = sorted({mapping[row["id_persona"]]["id_parlant"] for row in rows if row["forma"] == form})
        traits.append({"forma": form, "n_parlants": len(speakers), "n_ocurrencies": sum(row["forma"] == form for row in rows), "parlants": ",".join(speakers), "estat": "triple ASR; pendent d’audició; no és tret dialectal"})
    with (GRAFO / "trets-triple-full.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(traits[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(traits)

    edges = []
    for first, second in combinations(sorted(by_person), 2):
        shared = sorted(by_person[first] & by_person[second])
        if len(shared) >= 3:
            edges.append({"id_a": first, "id_b": second, "n_formes_compartides": len(shared), "formes": ",".join(shared), "estat": "triple ASR; semblança textual provisional; pendent d’audició"})
    with (GRAFO / "arestes-parlants-triple-full.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = list(edges[0]) if edges else ["id_a", "id_b", "n_formes_compartides", "formes", "estat"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(edges)

    nodes = []
    for speaker in sorted(people):
        speaker_forms = sorted(by_person.get(speaker, set()))
        nodes.append({"id_parlant": speaker, "nom_public": people[speaker]["nom_public"], "n_formes_triple": len(speaker_forms), "formes": ",".join(speaker_forms), "estat": "perfil triple ASR; pendent d’audició"})
    with (GRAFO / "nodes-triple-full.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(nodes[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(nodes)

    matrix = []
    for speaker in sorted(people):
        for form in forms:
            value = counts[(speaker, form)]
            matrix.append({"id_parlant": speaker, "forma": form, "n_ocurrencies": value, "present": "sí" if value else "no", "estat": "triple ASR; pendent d’audició"})
    with (GRAFO / "matriu-formes-triple-full.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(matrix[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(matrix)

    lines = ["graph TD"]
    for edge in sorted(edges, key=lambda row: (-row["n_formes_compartides"], row["id_a"], row["id_b"])):
        if edge["n_formes_compartides"] >= 4:
            lines.append(f"  {edge['id_a']}[{people[edge['id_a']]['nom_public']}] ---|{edge['n_formes_compartides']} formes| {edge['id_b']}[{people[edge['id_b']]['nom_public']}]")
    (GRAFO / "graf-parlants-triple-full.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} clips triples · {len(forms)} formes · {len(people)} nodes canònics · {len(edges)} arestes >=3")


if __name__ == "__main__":
    main()
