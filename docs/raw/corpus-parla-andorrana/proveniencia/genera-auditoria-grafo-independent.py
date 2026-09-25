"""Audita que les capes de graf només usin persones canòniques del subcorpus."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
GRAPH = ROOT / "grafo"
OUT = PROV / "auditoria-grafo-independent.tsv"

ARTIFACTS = (
    ("linguistic_nodes", "grafo/nodes-formes-completa.tsv", ("id_parlant",)),
    ("linguistic_edges", "grafo/arestes-parlants-formes-completa.tsv", ("id_a", "id_b")),
    ("linguistic_matrix", "grafo/matriu-formes-completa.tsv", ("id_parlant",)),
    ("scarce_form_nodes", "grafo/nodes-formes-escasses.tsv", ("id_parlant",)),
    ("scarce_form_edges", "grafo/arestes-parlants-formes-escasses.tsv", ("id_a", "id_b")),
    ("scarce_form_matrix", "grafo/matriu-formes-escasses.tsv", ("id_parlant",)),
    ("acoustic_nodes", "grafo/nodes-acustic-canonic.tsv", ("id",)),
    ("acoustic_edges", "grafo/arestes-acustic-canonic.tsv", ("id_a", "id_b")),
    ("repertory", "grafo/repertori-aplicat-canonic.tsv", ("id_parlant",)),
)


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    canonical = {row["id_parlant"] for row in read(PROV / "persones-canonics.tsv")}
    rows: list[dict[str, str]] = []
    for name, relative, columns in ARTIFACTS:
        path = (ROOT / relative).resolve()
        source = read(path)
        ids = {row[column] for row in source for column in columns if row.get(column)}
        outside = sorted(ids - canonical)
        rows.append(
            {
                "capa": name,
                "fitxer": relative,
                "files": str(len(source)),
                "nodes_canonics": str(len(ids & canonical)),
                "ids_fora": ";".join(outside),
                "estat": "independent" if not outside else "revisar",
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = ["capa", "fitxer", "files", "nodes_canonics", "ids_fora", "estat"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    independent = sum(row["estat"] == "independent" for row in rows)
    print(f"{len(rows)} capes de graf auditades · independents={independent} · {OUT}")


if __name__ == "__main__":
    main()
