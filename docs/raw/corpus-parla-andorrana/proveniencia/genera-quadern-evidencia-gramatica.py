"""Genera un quadern llegible dels patrons gramaticals candidates."""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "quadern-evidencia-gramatica.md"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def clean(value: str) -> str:
    return " ".join((value or "").replace("|", "\\|").split())


def main() -> None:
    evidence = read(PROV / "evidencia-gramatica.tsv")
    people = {row["id_persona"]: row for row in read(ROOT / "persones.tsv")}
    by_category: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in evidence:
        by_category[row["categoria"]].append(row)
    category_counts = Counter(row["categoria"] for row in evidence)
    lines = [
        "# Quadern d'evidència gramatical i de contacte",
        "",
        f"La passada automàtica conserva **{len(evidence):,} contextos** de **{len(category_counts)} categories** en les 66 transcripcions. Són patrons candidats extrets de l'ASR; no confirmen morfosintaxi, contacte ni pronunciació fins que s'escolti el fragment corresponent.",
        "",
        "| categoria | contextos | parlants | estat |",
        "|---|---:|---:|---|",
    ]
    for category in sorted(category_counts):
        rows = by_category[category]
        lines.append(f"| `{category}` | {len(rows)} | {len({row['id_persona'] for row in rows})} | candidat ASR; pendent d'audició |")
    lines.append("")
    for category in sorted(category_counts):
        rows = by_category[category]
        selected: list[dict[str, str]] = []
        seen: set[str] = set()
        for row in rows:
            if row["id_persona"] not in seen:
                selected.append(row); seen.add(row["id_persona"])
            if len(selected) == 3:
                break
        lines.extend([f"## {category}", "", f"**{len(rows)} contextos** en **{len({row['id_persona'] for row in rows})} parlants**.", "", "| parlant | forma ASR | context | fitxa |", "|---|---|---|---|"])
        for row in selected:
            name = clean(people.get(row["id_persona"], {}).get("nom_public", row["id_persona"]))
            lines.append(f"| {name} (`{row['id_persona']}`) | `{clean(row['forma'])}` | {clean(row['context'])} | [informe](../persones/{row['id_persona']}.md) |")
        lines.extend(["", "**Estat:** exemple textual ASR; requereix escolta i no entra al graf com a tret confirmat.", ""])
    lines.append("Font de dades: `evidencia-gramatica.tsv` i `resum-evidencia-gramatica.tsv`.")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(evidence)} contextos · {len(category_counts)} categories · {OUT}")


if __name__ == "__main__":
    main()
