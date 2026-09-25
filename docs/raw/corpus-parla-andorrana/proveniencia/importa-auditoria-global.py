"""Valida y proyecta el TSV exportado por l'auditoria global.

Per defecte només simula. Les files canòniques es projecten al registre mestre
amb ``--write``; les files dels candidats es conserven separades.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
TARGET = PROV / "registre-audicio.tsv"
CANDIDATE_TARGET = PROV / "anotacions-auditoria-global-candidats.tsv"
VALID = {"sí", "no", "incerta", "pendent", ""}


def clean(value: str) -> str:
    return (value or "").replace("\t", " ").replace("\n", " ").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida i importa l'exportació de l'auditoria global")
    parser.add_argument("tsv", type=Path, help="TSV descarregat de auditoria-global.html")
    parser.add_argument("--write", action="store_true", help="escriu els canvis canònics i les anotacions de candidats")
    args = parser.parse_args()

    with args.tsv.open(encoding="utf-8", newline="") as handle:
        annotations = list(csv.DictReader(handle, delimiter="\t"))
    if not annotations:
        raise SystemExit("el TSV no té cap anotació")
    ids = [row.get("id", "") for row in annotations]
    if any(not value for value in ids):
        raise SystemExit("hi ha una anotació sense id")
    if len(ids) != len(set(ids)):
        raise SystemExit("hi ha ids duplicats al TSV")

    with TARGET.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        canonical_rows = list(reader)
        fields = reader.fieldnames or []
    canonical_by_key = {(row["id_persona"], row["forma"], row["clip"]): row for row in canonical_rows}
    canonical_updates = []
    candidate_rows = []
    errors = []

    for annotation in annotations:
        decision = clean(annotation.get("decision", "pendent"))
        if decision not in VALID:
            errors.append(f"decisió desconeguda {decision!r}: {annotation['id']}")
            continue
        origin = clean(annotation.get("origen", ""))
        if origin == "canònic" or annotation["id"].startswith("canon::"):
            parts = annotation["id"].split("::", 3)
            if len(parts) != 4 or parts[0] != "canon":
                errors.append(f"id canònic mal format: {annotation['id']}")
                continue
            person, form = parts[1], parts[2]
            clip = clean(annotation.get("clip", ""))
            if clip.startswith("proveniencia/"):
                clip = clip[len("proveniencia/"):]
            target = canonical_by_key.get((person, form, clip))
            if target is None:
                errors.append(f"no hi ha coincidència canònica exacta: {(person, form, clip)}")
                continue
            state = {"sí": "confirmada", "no": "descartada", "incerta": "incerta", "pendent": "pendent", "": "pendent"}[decision]
            confirmed = {"sí": "sí", "no": "no", "incerta": "incerta", "pendent": "", "": ""}[decision]
            speaker = clean(annotation.get("speaker", "pendent"))
            note = clean(annotation.get("note", ""))
            if speaker and speaker != "pendent":
                note = f"veu={speaker}" + (f"; {note}" if note else "")
            values = {
                "estat_audicio": state,
                "forma_confirmada_auditivament": confirmed,
                "variant_transcrita": clean(annotation.get("variant", "")),
                "trets_fonetics_observats": clean(annotation.get("phon", "")),
                "observacions_prosodiques": clean(annotation.get("pros", "")),
                "nota_audicio": note,
            }
            for field, value in values.items():
                if field not in fields:
                    continue
                current = target.get(field, "")
                if value and current not in ("", "pendent", "pendent-audicio", value):
                    errors.append(f"conflicte a {field}: {annotation['id']}")
            canonical_updates.append((target, values))
        else:
            candidate_rows.append({key: clean(value) for key, value in annotation.items()})

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print(f"anotacions llegides: {len(annotations)}; canòniques actualitzables: {len(canonical_updates)}; candidats separats: {len(candidate_rows)}")
    if not args.write:
        print("simulació: usa --write para modificar el registro maestro y escribir las anotaciones de candidatos")
        return

    for target, values in canonical_updates:
        for field, value in values.items():
            if field in fields:
                target[field] = value
    with TARGET.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(canonical_rows)
    candidate_fields = ["id", "origen", "persona", "forma", "clip", "speaker", "decision", "variant", "phon", "pros", "note"]
    with CANDIDATE_TARGET.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=candidate_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows({key: row.get(key, "") for key in candidate_fields} for row in candidate_rows)
    print(f"escrit {TARGET} i {CANDIDATE_TARGET}")


if __name__ == "__main__":
    main()
