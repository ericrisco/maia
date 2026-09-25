"""Genera el resum verificable de cobertura per canal i llicència."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "resum-cobertura-fonts.tsv"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    sources = read(PROV / "fonts-resum.tsv")
    mapping = {row["id_persona"]: row["id_parlant"] for row in read(PROV / "persones-canonics.tsv")}
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in sources:
        groups[row["canal"]].append(row)
    rows = []
    for channel in sorted(groups):
        records = groups[channel]
        rows.append(
            {
                "canal": channel,
                "registres_font": str(len(records)),
                "persones_canoniques": str(len({mapping.get(row["id_persona"], row["id_persona"]) for row in records})),
                "urls": str(sum(bool(row.get("url")) for row in records)),
                "urls_youtube": str(sum("youtube" in row.get("url", "").lower() for row in records)),
                "llicencies_creative_commons": str(sum("creative commons" in row.get("llicencia", "").lower() for row in records)),
                "llicencia_oberta_declarada": "sí" if any("creative commons" in row.get("llicencia", "").lower() for row in records) else "no",
                "nota": "derivats locals per a recerca; confirmar termes abans de redistribuir" if not any("creative commons" in row.get("llicencia", "").lower() for row in records) else "la font declara Creative Commons; conservar atribució",
            }
        )
    fields = list(rows[0])
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} canals · {len(sources)} registres")


if __name__ == "__main__":
    main()
