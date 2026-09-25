"""Calcula descriptors acústics orientatius dels 30 clips escassos."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "analisi-acustica-formes-escasses.tsv"


def load_base():
    path = PROV / "calcula-acustica-clips.py"
    spec = importlib.util.spec_from_file_location("calcula_acustica_clips", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"no es pot carregar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    base = load_base()
    with (PROV / "cua-audicio-formes-escasses.tsv").open(encoding="utf-8", newline="") as handle:
        queue = list(csv.DictReader(handle, delimiter="\t"))
    rows = []
    for row in queue:
        measured = base.measure(
            {
                "forma": row["forma"],
                "id_persona": row["id_persona"],
                "interval_escolta": row["interval_vtt"],
                "clip": row["clip"],
                "forma_en_qa": "",
            }
        )
        measured["categoria"] = row["categoria"]
        measured["rang"] = row["rang"]
        measured["sha256"] = row["sha256"]
        rows.append(measured)
    fields = list(rows[0])
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} clips · {OUT}")


if __name__ == "__main__":
    main()
