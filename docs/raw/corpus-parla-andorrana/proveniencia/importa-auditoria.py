"""Incorpora un TSV exportat pel revisor HTML al registre d'audició."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
TARGET = PROV / "registre-audicio.tsv"
FIELDS = [
    "forma_confirmada_auditivament",
    "variant_transcrita",
    "trets_fonetics_observats",
    "observacions_prosodiques",
    "nota_audicio",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv", type=Path, help="TSV descarregat de l'auditoria HTML")
    parser.add_argument("--write", action="store_true", help="escriu el registre actualitzat")
    args = parser.parse_args()
    with args.tsv.open(encoding="utf-8", newline="") as handle:
        annotations = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}
    with TARGET.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    updated = 0
    decisions = {"confirmada": 0, "descartada": 0, "incerta": 0, "pendent": 0}
    for row in rows:
        key = f"{row['id_persona']}::{row['forma']}::{row['interval_escolta']}"
        annotation = annotations.get(key)
        if not annotation:
            continue
        status = annotation.get("status", "pendent")
        if status not in decisions:
            raise SystemExit(f"estat desconegut: {status!r} ({key})")
        row["estat_audicio"] = status
        row["forma_confirmada_auditivament"] = {"confirmada": "sí", "descartada": "no", "incerta": "incerta", "pendent": ""}[status]
        row["variant_transcrita"] = annotation.get("variant", "")
        row["trets_fonetics_observats"] = annotation.get("phon", "")
        row["observacions_prosodiques"] = annotation.get("pros", "")
        row["nota_audicio"] = annotation.get("note", "")
        decisions[status] += 1
        updated += 1
    print(f"anotacions llegides: {len(annotations)}; files actualitzables: {updated}; decisions: {decisions}")
    if not args.write:
        print("simulació: usa --write per modificar registre-audicio.tsv")
        return
    with TARGET.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"escrit {TARGET}")


if __name__ == "__main__":
    main()
