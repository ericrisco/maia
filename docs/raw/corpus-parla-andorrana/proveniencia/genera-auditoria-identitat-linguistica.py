"""Genera la cua d'auditoria d'identitat territorial i lingüística."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-identitat-linguistica.tsv"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    canonical = read(PROV / "persones-canonics.tsv")
    sources = {row["id_persona"]: row for row in read(ROOT / "persones.tsv")}
    contexts = {row["id_persona"]: row for row in read(PROV / "context-persones.tsv")}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in canonical:
        grouped[row["id_parlant"]].append(row)
    rows = []
    for speaker, records in sorted(grouped.items()):
        source_rows = [sources[row["id_persona"]] for row in records]
        # Una fila només documenta context si conserva una font contextual.
        # Les identificacions basades únicament en títol o metadades continuen
        # sent pendents i no poden fer passar el parlant a context documentat.
        context_rows = [
            contexts[row["id_persona"]]
            for row in records
            if row["id_persona"] in contexts and contexts[row["id_persona"]].get("font_contextual")
        ]
        names = sorted({row["nom_public"] for row in records})
        channels = sorted({row["tipus_font"] for row in source_rows})
        geographic = sorted({row.get("parroquia_o_ambit", "") for row in context_rows if row.get("parroquia_o_ambit")})
        evidence = " | ".join(row.get("evidencia", "") for row in context_rows)
        rows.append(
            {
                "id_parlant": speaker,
                "nom_public": "; ".join(names),
                "n_mostres": str(len(records)),
                "canals": "; ".join(channels),
                "ambit_documentat": "; ".join(geographic),
                "evidencia_contextual": evidence,
                "estat": "context territorial documentat; llengua inicial pendent" if context_rows else "font andorrana; biografia lingüística pendent",
                "accio": "confirmar lloc de socialització, llengües d'ús i veu al clip",
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} parlants")


if __name__ == "__main__":
    main()
