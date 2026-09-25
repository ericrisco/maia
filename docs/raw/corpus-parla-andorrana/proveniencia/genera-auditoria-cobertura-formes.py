"""Resumeix la cobertura de les 35 formes candidates per prioritzar l'audició."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-cobertura-formes.tsv"


def main() -> None:
    with (ROOT / "grafo" / "trets-formes-completa.tsv").open(encoding="utf-8", newline="") as handle:
        source = list(csv.DictReader(handle, delimiter="\t"))
    rows = []
    for row in source:
        speakers = int(row["n_persones_canoniques"])
        level = "escassa" if speakers < 10 else ("intermèdia" if speakers < 30 else "àmplia")
        rows.append(
            {
                "forma": row["forma"],
                "categoria": row["categoria"],
                "n_parlants_canònics": row["n_persones_canoniques"],
                "n_registres_font": row["n_registres_font"],
                "n_ocurrencies_asr": row["n_ocurrencies_asr"],
                "nivell_cobertura": level,
                "prioritat_audicio": "alta" if level == "escassa" else ("mitjana" if level == "intermèdia" else "normal"),
                "estat": row["estat"],
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} formes auditades · escassa={sum(r['nivell_cobertura']=='escassa' for r in rows)} · {OUT}")


if __name__ == "__main__":
    main()
