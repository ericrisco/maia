"""Genera el registre d'audició propi de les formes escasses."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
QUEUE = PROV / "cua-audicio-formes-escasses.tsv"
OUT = PROV / "registre-audicio-formes-escasses.tsv"
FIELDS = [
    "ordre", "categoria", "forma", "rang", "id_persona", "interval_escolta", "clip", "text_qa",
    "estat_audicio", "forma_confirmada_auditivament", "variant_transcrita",
    "trets_fonetics_observats", "observacions_prosodiques", "nota_audicio",
]
HUMAN_FIELDS = FIELDS[8:]


def main() -> None:
    with QUEUE.open(encoding="utf-8", newline="") as handle:
        queue = list(csv.DictReader(handle, delimiter="\t"))
    previous = {}
    if OUT.exists():
        with OUT.open(encoding="utf-8", newline="") as handle:
            previous = {(row["id_persona"], row["forma"], row["clip"]): row for row in csv.DictReader(handle, delimiter="\t")}
    rows = []
    for source in queue:
        key = (source["id_persona"], source["forma"], source["clip"])
        old = previous.get(key, {})
        row = {
            "ordre": source["ordre"],
            "categoria": source["categoria"],
            "forma": source["forma"],
            "rang": source["rang"],
            "id_persona": source["id_persona"],
            "interval_escolta": source["interval_vtt"],
            "clip": source["clip"],
            "text_qa": source["text_asr"],
            "estat_audicio": old.get("estat_audicio") or source.get("decisio_humana") or "pendent",
            "forma_confirmada_auditivament": old.get("forma_confirmada_auditivament", ""),
            "variant_transcrita": old.get("variant_transcrita", ""),
            "trets_fonetics_observats": old.get("trets_fonetics_observats", ""),
            "observacions_prosodiques": old.get("observacions_prosodiques", ""),
            "nota_audicio": old.get("nota_audicio", ""),
        }
        rows.append(row)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"generat {OUT} amb {len(rows)} files; anotacions existents conservades")


if __name__ == "__main__":
    main()
