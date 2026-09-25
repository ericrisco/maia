"""Verifica que cada persona té el paquet mínim del corpus."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]


def main() -> None:
    registry = list(csv.DictReader((ROOT / "persones.tsv").open(), delimiter="\t"))
    rows = []
    for person in registry:
        pid = person["id_persona"]
        source = ROOT / "proveniencia" / pid / "source.info.json"
        required = {
            "audio": ROOT / "audios" / pid / "audio.wav",
            "transcripcio": ROOT / "transcripcions" / f"{pid}.json",
            "marcada": ROOT / "transcripcions" / f"{pid}-marcada.txt",
            "informe": ROOT / "persones" / f"{pid}.md",
            "procedencia": ROOT / "proveniencia" / pid / "README.md",
        }
        row = {
            "id_persona": pid,
            "nom_public": person["nom_public"],
            "estat": person["estat"],
            "llicencia_registrada": "sí" if source.exists() else "no",
        }
        for key, path in required.items():
            row[key] = "sí" if path.exists() and path.stat().st_size else "no"
        rows.append(row)
    out = ROOT / "proveniencia" / "cobertura.tsv"
    fields = list(rows[0])
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    missing = [row["id_persona"] for row in rows if any(row[key] == "no" for key in fields[3:])]
    print(f"{len(rows)} persones · {out}")
    if missing:
        raise SystemExit("paquets incomplets: " + ", ".join(missing))


if __name__ == "__main__":
    main()
