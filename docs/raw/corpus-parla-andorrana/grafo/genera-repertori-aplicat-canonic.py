"""Agrupa el repertori aplicat per persona canònica sense perdre mostres."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = ROOT / "grafo" / "repertori-aplicat-canonic.tsv"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return " | ".join(seen)


def main() -> None:
    canonical = read(PROV / "persones-canonics.tsv")
    applied = read(ROOT / "grafo" / "repertori-aplicat.tsv")
    canonical_by_source = {row["id_persona"]: row for row in canonical}
    source_ids: dict[str, list[str]] = defaultdict(list)
    names: dict[str, str] = {}
    for row in canonical:
        source_ids[row["id_parlant"]].append(row["id_persona"])
        names[row["id_parlant"]] = row["nom_public"]
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in applied:
        mapping = canonical_by_source.get(row["id_persona"])
        if mapping:
            grouped[(mapping["id_parlant"], row["categoria"], row["candidat"])].append(row)
    rows: list[dict[str, str]] = []
    for (speaker, category, candidate), values in sorted(grouped.items()):
        rows.append(
            {
                "id_parlant": speaker,
                "nom_public": names[speaker],
                "mostres_id": ",".join(sorted(source_ids[speaker])),
                "n_mostres": str(len(source_ids[speaker])),
                "categoria": category,
                "candidat": candidate,
                "referencia": unique_join([row["referencia"] for row in values]),
                "indicador_automatic": unique_join([row["indicador_automatic"] for row in values]),
                "estat_indicador": unique_join([row["estat_indicador"] for row in values]),
                "observacio_auditiva": unique_join([row["observacio_auditiva"] for row in values]),
            }
        )
    fields = list(rows[0])
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} files · {len(names)} parlants canònics · {OUT}")


if __name__ == "__main__":
    main()
