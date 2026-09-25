"""Valida i projecta l'exportació de les sessions canòniques.

Per defecte només simula. ``--write`` és necessari per modificar
``registre-audicio.tsv``; les files pendents no escriuen cap decisió.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
TARGET = PROV / "registre-audicio.tsv"
VALID = {"sí", "no", "incerta", "pendent", ""}
MAP = {
    "sí": ("confirmada", "sí"),
    "no": ("descartada", "no"),
    "incerta": ("incerta", "incerta"),
    "pendent": ("pendent", ""),
    "": ("pendent", ""),
}


def clean(value: str) -> str:
    return (value or "").replace("\t", " ").replace("\n", " ").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida l'exportació de les sessions canòniques")
    parser.add_argument("tsv", type=Path, help="TSV descarregat de auditoria-sessions-canoniques.html")
    parser.add_argument("--write", action="store_true", help="escriu les anotacions vàlides al registre mestre")
    args = parser.parse_args()

    with args.tsv.open(encoding="utf-8", newline="") as handle:
        annotations = list(csv.DictReader(handle, delimiter="\t"))
    if not annotations:
        raise SystemExit("el TSV no té cap fila")
    ids = [clean(row.get("id_global", "")) for row in annotations]
    errors = []
    if any(not value for value in ids):
        errors.append("hi ha una fila sense id_global")
    if len(ids) != len(set(ids)):
        errors.append("hi ha id_global duplicats")

    with TARGET.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        master = list(reader)
        fields = reader.fieldnames or []
    by_key = {(row["id_persona"], row["forma"], row["clip"]): row for row in master}
    updates = []
    for annotation in annotations:
        ident = clean(annotation.get("id_global", ""))
        if not ident.startswith("canon::"):
            errors.append(f"fila fora de les sessions canòniques: {ident}")
            continue
        parts = ident.split("::", 3)
        if len(parts) != 4:
            errors.append(f"id_global mal format: {ident}")
            continue
        person, form = parts[1], parts[2]
        clip = clean(annotation.get("clip", ""))
        target = by_key.get((person, form, clip))
        if target is None:
            errors.append(f"no hi ha coincidència exacta: {(person, form, clip)}")
            continue
        decision = clean(annotation.get("decision", "pendent"))
        if decision not in VALID:
            errors.append(f"decisió desconeguda {decision!r}: {ident}")
            continue
        note = clean(annotation.get("note", ""))
        if decision in {"sí", "no", "incerta"} and not note:
            errors.append(f"falta nota justificativa per a {ident}")
            continue
        state, confirmed = MAP[decision]
        speaker = clean(annotation.get("speaker", "pendent"))
        if speaker and speaker != "pendent":
            note = f"veu={speaker}; {note}" if note else f"veu={speaker}"
        values = {
            "estat_audicio": state,
            "forma_confirmada_auditivament": confirmed,
            "variant_transcrita": clean(annotation.get("variant", "")),
            "trets_fonetics_observats": clean(annotation.get("phon", "")),
            "observacions_prosodiques": clean(annotation.get("pros", "")),
            "nota_audicio": note,
        }
        for field, value in values.items():
            if field not in fields or not value:
                continue
            current = target.get(field, "")
            if current not in ("", "pendent", "pendent-audicio", value):
                errors.append(f"conflicte a {field}: {ident}")
        if decision != "pendent" or any(values[field] for field in values if field != "estat_audicio"):
            updates.append((target, values))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print(f"files llegides: {len(annotations)}; actualitzacions vàlides: {len(updates)}")
    if not args.write:
        print("simulació: usa --write per modificar registre-audicio.tsv")
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
