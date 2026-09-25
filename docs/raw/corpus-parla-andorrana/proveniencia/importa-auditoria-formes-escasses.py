"""Valida i projecta l'exportació del reproductor de formes escasses."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
TARGET = PROV / "registre-audicio-formes-escasses.tsv"
QUEUE = PROV / "cua-audicio-formes-escasses.tsv"
VALID = {"confirmada", "descartada", "incerta", "pendent", ""}
MAP = {
    "confirmada": ("confirmada", "sí"),
    "descartada": ("descartada", "no"),
    "incerta": ("incerta", "incerta"),
    "pendent": ("pendent", ""),
    "": ("pendent", ""),
}


def clean(value: str) -> str:
    return (value or "").replace("\t", " ").replace("\n", " ").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida l'exportació de formes escasses")
    parser.add_argument("tsv", type=Path, help="TSV descarregat de auditoria-formes-escasses.html")
    parser.add_argument("--write", action="store_true", help="escriu les anotacions vàlides al registre mestre")
    args = parser.parse_args()

    with args.tsv.open(encoding="utf-8", newline="") as handle:
        annotations = list(csv.DictReader(handle, delimiter="\t"))
    if not annotations:
        raise SystemExit("el TSV no té cap fila")
    ids = [clean(row.get("id", "")) for row in annotations]
    errors = []
    if any(not value for value in ids):
        errors.append("hi ha una fila sense id")
    if len(ids) != len(set(ids)):
        errors.append("hi ha ids duplicats")

    with QUEUE.open(encoding="utf-8", newline="") as handle:
        scarce_rows = list(csv.DictReader(handle, delimiter="\t"))
    scarce_keys = {(row["id_persona"], row["forma"], row["clip"]) for row in scarce_rows}
    with TARGET.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        master = list(reader)
        fields = reader.fieldnames or []
    by_key = {(row["id_persona"], row["forma"], row["clip"]): row for row in master}
    updates = []
    decisions = {key: 0 for key in VALID if key}
    for annotation in annotations:
        ident = clean(annotation.get("id", ""))
        person = clean(annotation.get("person", ""))
        form = clean(annotation.get("form", ""))
        clip = clean(annotation.get("clip", ""))
        key = (person, form, clip)
        if key not in scarce_keys:
            errors.append(f"fila fora de la cua de formes escasses: {ident or key}")
            continue
        target = by_key.get(key)
        if target is None:
            errors.append(f"no hi ha coincidència al registre mestre: {key}")
            continue
        status = clean(annotation.get("status", "pendent")) or "pendent"
        if status not in VALID:
            errors.append(f"decisió desconeguda {status!r}: {ident}")
            continue
        state, confirmed = MAP[status]
        values = {
            "estat_audicio": state,
            "forma_confirmada_auditivament": confirmed,
            "variant_transcrita": clean(annotation.get("variant", "")),
            "trets_fonetics_observats": clean(annotation.get("phon", "")),
            "observacions_prosodiques": clean(annotation.get("pros", "")),
            "nota_audicio": clean(annotation.get("note", "")),
        }
        for field, value in values.items():
            if field not in fields or not value:
                continue
            current = target.get(field, "")
            if current not in ("", "pendent", "pendent-audicio", value):
                errors.append(f"conflicte a {field}: {ident or key}")
        if status != "pendent" or any(values[field] for field in values if field != "estat_audicio"):
            updates.append((target, values))
            decisions[status] += 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print(f"files llegides: {len(annotations)}; actualitzacions vàlides: {len(updates)}; decisions: {decisions}")
    if not args.write:
        print("simulació: usa --write per modificar registre-audicio-formes-escasses.tsv")
        return
    for target, values in updates:
        for field, value in values.items():
            if field in fields:
                target[field] = value
    with TARGET.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(master)
    print(f"escrit {TARGET}")


if __name__ == "__main__":
    main()
