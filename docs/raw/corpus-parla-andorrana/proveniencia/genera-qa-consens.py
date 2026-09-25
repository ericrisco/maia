"""Combina les dues passades ASR independents i genera una capa de consens."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
GRAPH = ROOT / "grafo"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    small = read(PROV / "qa-clips.tsv")
    base = {(r["id_persona"], r["forma"]): r for r in read(PROV / "qa-clips-base.tsv")}
    consensus = []
    speakers: dict[str, set[str]] = defaultdict(set)
    for row in small:
        other = base[(row["id_persona"], row["forma"])]
        small_yes = row["forma_en_qa"] == "sí"
        base_yes = other["forma_en_base"] == "sí"
        both = small_yes and base_yes
        if both:
            speakers[row["forma"]].add(row["id_persona"])
        consensus.append(
            {
                "id_persona": row["id_persona"],
                "forma": row["forma"],
                "interval_escolta": row["interval_escolta"],
                "clip": row["clip"],
                "sha256": row["sha256"],
                "coincidencia_small": "sí" if small_yes else "no",
                "coincidencia_base": "sí" if base_yes else "no",
                "consens_textual": "sí" if both else "no",
                "text_small": row["text_qa"],
                "text_base": other["text_base"],
            }
        )
    write(
        PROV / "qa-clips-consens.tsv",
        ["id_persona", "forma", "interval_escolta", "clip", "sha256", "coincidencia_small", "coincidencia_base", "consens_textual", "text_small", "text_base"],
        consensus,
    )

    trait_rows = [
        {"forma": form, "tipus": "consens-ASR-small-base", "n_parlants": str(len(ids)), "parlants": ",".join(sorted(ids))}
        for form, ids in sorted(speakers.items())
        if len(ids) >= 3
    ]
    write(GRAPH / "trets-base-consens.tsv", ["forma", "tipus", "n_parlants", "parlants"], trait_rows)
    edge_rows = []
    for form, ids in sorted(speakers.items()):
        if len(ids) < 3:
            continue
        for person in sorted(ids):
            edge_rows.append({"id_persona": person, "forma": form, "relacio": "consens-ASR-small-base", "pes": "1"})
    write(GRAPH / "arestes-parlants-base-consens.tsv", ["id_persona", "forma", "relacio", "pes"], edge_rows)
    lines = ["graph TD"]
    for i, row in enumerate(trait_rows, 1):
        node = f"F{i}"
        lines.append(f'  {node}["{row["forma"]}\\n{row["n_parlants"]} parlants"]')
        for j, person in enumerate(row["parlants"].split(","), 1):
            pnode = f"P{person.replace('-', '')}"
            lines.append(f'  {pnode}("{person}")')
            lines.append(f"  {pnode} --> {node}")
    (GRAPH / "graf-parlants-base-consens.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    both = sum(row["consens_textual"] == "sí" for row in consensus)
    print(f"{len(consensus)} clips · {both} consensos · {len(trait_rows)} formes amb >=3 parlants")


if __name__ == "__main__":
    main()
