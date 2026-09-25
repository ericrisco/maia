"""Genera la cobertura de sesiones de audición por parlante canònic."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-cobertura-sessions.tsv"
SESSION_NAMES = ("sessio-01.tsv", "sessio-02.tsv", "sessio-05.tsv", "sessio-06.tsv")
QUARANTINE = {"pa-044", "pa-047", "pa-050"}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    canonical = read(PROV / "persones-canonics.tsv")
    speaker_to_sources: dict[str, set[str]] = defaultdict(set)
    names: dict[str, str] = {}
    for row in canonical:
        speaker_to_sources[row["id_parlant"]].add(row["id_persona"])
        names[row["id_parlant"]] = row["nom_public"]
    clips: dict[str, list[dict[str, str]]] = defaultdict(list)
    for name in SESSION_NAMES:
        for row in read(PROV / "sessions" / name):
            if row.get("origen") == "canònic":
                clips[row["persona"]].append({**row, "sessio": name.removesuffix(".tsv")})
    rows = []
    for speaker in sorted(speaker_to_sources):
        source_ids = sorted(speaker_to_sources[speaker])
        selected = [row for source in source_ids for row in clips.get(source, [])]
        sessions = sorted({row["sessio"] for row in selected})
        quarantine = sorted(set(source_ids) & QUARANTINE)
        rows.append(
            {
                "id_parlant": speaker,
                "nom_public": names[speaker],
                "id_fonts": ";".join(source_ids),
                "n_clips": str(len(selected)),
                "sessions": ";".join(sessions),
                "clips": ";".join(row["clip"] for row in selected),
                "estat": "quarantena" if quarantine and not selected else ("cobert" if selected else "pendent"),
                "nota": ";".join(quarantine) if quarantine and not selected else "",
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    covered = sum(row["estat"] == "cobert" for row in rows)
    quarantine = sum(row["estat"] == "quarantena" for row in rows)
    print(f"{len(rows)} parlants · coberts={covered} · quarantena={quarantine} · {OUT}")


if __name__ == "__main__":
    main()
