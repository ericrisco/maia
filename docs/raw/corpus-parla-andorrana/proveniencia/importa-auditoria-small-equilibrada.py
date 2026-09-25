"""Incorpora el TSV exportat per l'auditoria de la mostra equilibrada."""
from __future__ import annotations
import argparse, csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
TARGET = ROOT / "proveniencia" / "cua-audicio-small-equilibrada.tsv"
STATUS = {"sí": "sí", "no": "no", "incerta": "incerta", "pendent": ""}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv", type=Path, help="TSV descarregat del revisor HTML")
    parser.add_argument("--write", action="store_true", help="escriu el TSV de la mostra")
    args = parser.parse_args()
    with args.tsv.open(encoding="utf-8", newline="") as h:
        annotations = {row["id"]: row for row in csv.DictReader(h, delimiter="\t")}
    with TARGET.open(encoding="utf-8", newline="") as h:
        reader = csv.DictReader(h, delimiter="\t")
        rows = list(reader)
        fields = reader.fieldnames or []
    decisions = {"sí": 0, "no": 0, "incerta": 0, "pendent": 0}
    updated = 0
    for row in rows:
        key = f"{row['id_persona']}::{row['forma']}::{row['clip']}"
        note = annotations.get(key)
        if not note:
            continue
        status = note.get("status", "pendent")
        if status not in decisions:
            raise SystemExit(f"decisió desconeguda: {status!r} ({key})")
        row["decisio_auditiva"] = STATUS[status]
        row["variant_transcrita"] = note.get("variant", "")
        row["trets_fonetica"] = note.get("phon", "")
        row["observacions_prosodia"] = note.get("pros", "")
        row["nota_audicio"] = note.get("note", "")
        decisions[status] += 1
        updated += 1
    print(f"anotacions llegides: {len(annotations)}; files actualitzables: {updated}; decisions: {decisions}")
    if not args.write:
        print("simulació: usa --write per modificar cua-audicio-small-equilibrada.tsv")
        return
    with TARGET.open("w", encoding="utf-8", newline="") as h:
        writer = csv.DictWriter(h, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"escrit {TARGET}")

if __name__ == "__main__":
    main()
