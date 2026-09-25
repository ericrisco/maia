"""Genera el graf canònic a partir de les 35 formes de la matriu ASR."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
GRAPH = ROOT / "grafo"
MIN_SHARED = 3
MERMAID_MIN_SHARED = 5


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    mapping_rows = read(PROV / "persones-canonics.tsv")
    mapping = {row["id_persona"]: row for row in mapping_rows}
    people = {row["id_parlant"]: row for row in mapping_rows}
    matrix = read(GRAPH / "matriu-formes.tsv")

    by_person_form: dict[str, Counter[str]] = defaultdict(Counter)
    form_category: dict[str, str] = {}
    for row in matrix:
        speaker = mapping[row["id_persona"]]["id_parlant"]
        form = row["forma"]
        count = int(row["recompte_asr"])
        by_person_form[speaker][form] += count
        form_category[form] = row["categoria"]

    forms = sorted(form_category)
    speaker_forms = {
        speaker: {form for form, count in counts.items() if count > 0}
        for speaker, counts in by_person_form.items()
    }

    trait_rows = []
    for form in forms:
        speakers = sorted(speaker for speaker in people if form in speaker_forms.get(speaker, set()))
        records = sorted(row["id_persona"] for row in matrix if row["forma"] == form and int(row["recompte_asr"]) > 0)
        total = sum(int(row["recompte_asr"]) for row in matrix if row["forma"] == form)
        trait_rows.append({
            "forma": form,
            "categoria": form_category[form],
            "n_persones_canoniques": len(speakers),
            "n_registres_font": len(records),
            "n_ocurrencies_asr": total,
            "persones": ",".join(speakers),
            "estat": "matriu ASR completa; semblança textual; pendent d'audició",
        })
    write_tsv(
        GRAPH / "trets-formes-completa.tsv",
        trait_rows,
        ["forma", "categoria", "n_persones_canoniques", "n_registres_font", "n_ocurrencies_asr", "persones", "estat"],
    )

    edge_rows = []
    for first, second in combinations(sorted(people), 2):
        shared = sorted(speaker_forms.get(first, set()) & speaker_forms.get(second, set()))
        if len(shared) >= MIN_SHARED:
            edge_rows.append({
                "id_a": first,
                "id_b": second,
                "n_formes_compartides": len(shared),
                "formes": ",".join(shared),
                "estat": "matriu ASR completa; semblança textual provisional; pendent d'audició",
            })
    write_tsv(
        GRAPH / "arestes-parlants-formes-completa.tsv",
        edge_rows,
        ["id_a", "id_b", "n_formes_compartides", "formes", "estat"],
    )

    node_rows = []
    for speaker in sorted(people):
        counts = by_person_form.get(speaker, Counter())
        present = sorted(form for form in forms if counts[form] > 0)
        source_count = sum(1 for row in mapping_rows if row["id_parlant"] == speaker)
        node_rows.append({
            "id_parlant": speaker,
            "nom_public": people[speaker]["nom_public"],
            "n_registres_font": source_count,
            "n_formes": len(present),
            "n_ocurrencies_asr": sum(counts.values()),
            "formes": ",".join(present),
            "estat": "perfil canònic ASR; pendent d'audició",
        })
    write_tsv(
        GRAPH / "nodes-formes-completa.tsv",
        node_rows,
        ["id_parlant", "nom_public", "n_registres_font", "n_formes", "n_ocurrencies_asr", "formes", "estat"],
    )

    matrix_rows = []
    for speaker in sorted(people):
        counts = by_person_form.get(speaker, Counter())
        for form in forms:
            value = counts[form]
            matrix_rows.append({
                "id_parlant": speaker,
                "forma": form,
                "categoria": form_category[form],
                "recompte_asr": value,
                "present": "sí" if value else "no",
                "estat": "ASR agrupat per persona canònica; pendent d'audició",
            })
    write_tsv(
        GRAPH / "matriu-formes-completa.tsv",
        matrix_rows,
        ["id_parlant", "forma", "categoria", "recompte_asr", "present", "estat"],
    )

    labels = {speaker: people[speaker]["nom_public"].replace('"', '\\"') for speaker in people}
    lines = ["graph TD"]
    for edge in sorted(edge_rows, key=lambda row: (-int(row["n_formes_compartides"]), row["id_a"], row["id_b"])):
        if int(edge["n_formes_compartides"]) >= MERMAID_MIN_SHARED:
            first, second = edge["id_a"], edge["id_b"]
            lines.append(f'  {first}["{labels[first]}"] ---|{edge["n_formes_compartides"]} formes| {second}["{labels[second]}"]')
    (GRAPH / "graf-parlants-formes-completa.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (GRAPH / "README-formes-completa.md").write_text(
        f"""# Graf canònic de les 35 formes candidates

Aquesta capa agrupa els **66 registres de font en {len(people)} persones canòniques** i calcula presència i freqüència per a les **{len(forms)} formes** de `matriu-formes.tsv`. Les formes provenen de l'ASR i no són trets dialectals confirmats.

- `nodes-formes-completa.tsv`: {len(node_rows)} perfils canònics.
- `trets-formes-completa.tsv`: {len(trait_rows)} formes amb cobertura i freqüència.
- `arestes-parlants-formes-completa.tsv`: {len(edge_rows)} parelles amb almenys {MIN_SHARED} formes compartides.
- `matriu-formes-completa.tsv`: {len(matrix_rows)} cel·les persona-forma.
- `graf-parlants-formes-completa.mmd`: vista Mermaid que mostra només les parelles amb almenys {MERMAID_MIN_SHARED} formes.

Les arestes expressen semblança textual entre transcripcions, no identitat de veu ni proximitat dialectal. La confirmació es farà al registre d'audició, que conserva variant, fonètica i prosòdia com a camps separats.
""",
        encoding="utf-8",
    )
    print(f"{len(people)} nodes · {len(forms)} formes · {len(edge_rows)} arestes >= {MIN_SHARED} · {len(matrix_rows)} cel·les")


if __name__ == "__main__":
    main()
