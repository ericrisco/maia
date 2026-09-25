"""Valida una exportació de la cua de candidats sense tocar el registre canònic."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
QUEUE = PROV / "cua-audicio-candidats-prioritaria.tsv"
ALLOWED_DECISIONS = {"pendent", "sí", "no", "incerta"}
ALLOWED_SPEAKERS = {"pendent", "persona-candidata", "entrevistador", "mixt", "incerta"}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("export", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    current = read(QUEUE)
    exported = read(args.export)
    by_id = {row["id"]: row for row in current}
    if set(by_id) != {row.get("id") for row in exported} or len(exported) != len(current):
        raise SystemExit("claus de clip incompletes o duplicades")
    for row in exported:
        if row.get("estat_audicio") not in ALLOWED_DECISIONS or row.get("forma_confirmada") not in ALLOWED_DECISIONS or row.get("veu_confirmada") not in ALLOWED_SPEAKERS:
            raise SystemExit(f"estat humà invàlid per a {row.get('id')}")
        if row["id"] not in by_id or row["candidate"] != by_id[row["id"]]["candidate"] or row["clip"] != by_id[row["id"]]["clip"]:
            raise SystemExit(f"clau immutable inconsistent per a {row.get('id')}")
    if args.write:
        updates = {row["id"]: row for row in exported}
        fields = list(current[0])
        for row in current:
            update = updates[row["id"]]
            for field in ("estat_audicio", "veu_confirmada", "forma_confirmada", "variant_transcrita", "trets_fonetics_observats", "observacions_prosodiques", "nota_audicio"):
                row[field] = update.get(field, row.get(field, ""))
        with QUEUE.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
            writer.writeheader(); writer.writerows(current)
    print(f"OK: {len(exported)} anotacions candidates validades" + (" i escrites" if args.write else "; simulació"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
