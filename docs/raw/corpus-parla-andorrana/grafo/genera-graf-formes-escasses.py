"""Genera una vista del graf canònic restringida a les formes escasses."""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
GRAPH = ROOT / "grafo"
MIN_SHARED = 2


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write(path: Path, rows: list[dict[str, str]]) -> None:
    fields = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    mapping_rows = read(PROV / "persones-canonics.tsv")
    mapping = {row["id_persona"]: row["id_parlant"] for row in mapping_rows}
    names = {row["id_parlant"]: row["nom_public"] for row in mapping_rows}
    matrix = read(GRAPH / "matriu-formes.tsv")
    full_stats = {row["forma"]: row for row in read(GRAPH / "trets-formes-completa.tsv")}
    rare = sorted(form for form, row in full_stats.items() if int(row["n_persones_canoniques"]) < 10)
    by_speaker: dict[str, Counter[str]] = defaultdict(Counter)
    categories = {row["forma"]: row["categoria"] for row in matrix}
    for row in matrix:
        if row["forma"] in rare:
            by_speaker[mapping[row["id_persona"]]][row["forma"]] += int(row["recompte_asr"])
    speakers = sorted(names)
    traits = [{key: full_stats[form][key] for key in full_stats[form]} for form in rare]
    write(GRAPH / "trets-formes-escasses.tsv", traits)
    node_rows = []
    for speaker in speakers:
        present = sorted(form for form in rare if by_speaker[speaker][form] > 0)
        node_rows.append({
            "id_parlant": speaker, "nom_public": names[speaker], "n_formes_escasses": str(len(present)),
            "n_ocurrencies_asr": str(sum(by_speaker[speaker].values())), "formes": ",".join(present),
            "estat": "ASR provisional; formes escasses; pendent d'audició",
        })
    write(GRAPH / "nodes-formes-escasses.tsv", node_rows)
    edge_rows = []
    for first, second in combinations(speakers, 2):
        shared = sorted(set(form for form in rare if by_speaker[first][form] > 0) & set(form for form in rare if by_speaker[second][form] > 0))
        if len(shared) >= MIN_SHARED:
            edge_rows.append({"id_a": first, "id_b": second, "n_formes_escasses_compartides": str(len(shared)), "formes": ",".join(shared), "estat": "semblança textual ASR provisional; pendent d'audició"})
    write(GRAPH / "arestes-parlants-formes-escasses.tsv", edge_rows)
    matrix_rows = []
    for speaker in speakers:
        for form in rare:
            value = by_speaker[speaker][form]
            matrix_rows.append({"id_parlant": speaker, "forma": form, "categoria": categories[form], "recompte_asr": str(value), "present": "sí" if value else "no", "estat": "ASR agrupat per persona canònica; pendent d'audició"})
    write(GRAPH / "matriu-formes-escasses.tsv", matrix_rows)
    lines = ["graph TD"]
    for edge in sorted(edge_rows, key=lambda row: (-int(row["n_formes_escasses_compartides"]), row["id_a"], row["id_b"])):
        lines.append(f'  {edge["id_a"]}["{names[edge["id_a"]]}"] ---|{edge["n_formes_escasses_compartides"]} formes escasses| {edge["id_b"]}["{names[edge["id_b"]]}"]')
    (GRAPH / "graf-parlants-formes-escasses.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (GRAPH / "README-formes-escasses.md").write_text(
        f"""# Graf canònic de formes escasses

Aquesta vista restringeix la matriu canònica a les **{len(rare)} formes** amb menys de deu parlants canònics. Agrupa els 66 registres en {len(speakers)} persones canòniques i conserva només semblança textual ASR provisional.

- `trets-formes-escasses.tsv`: {len(rare)} formes territorials o discursives amb cobertura baixa.
- `nodes-formes-escasses.tsv`: {len(node_rows)} perfils canònics.
- `arestes-parlants-formes-escasses.tsv`: {len(edge_rows)} parelles amb almenys {MIN_SHARED} formes escasses compartides.
- `matriu-formes-escasses.tsv`: {len(matrix_rows)} cel·les persona-forma.
- `graf-parlants-formes-escasses.mmd`: vista Mermaid de les arestes.

Les arestes no són proximitat dialectal ni confirmació de veu: només ordenen l'audició de les deu formes amb cobertura escassa. La cua inicial és `../proveniencia/cua-audicio-formes-escasses-prioritaria.tsv`.
""", encoding="utf-8")
    print(f"{len(speakers)} nodes · {len(rare)} formes escasses · {len(edge_rows)} arestes · {len(matrix_rows)} cel·les")


if __name__ == "__main__":
    main()
