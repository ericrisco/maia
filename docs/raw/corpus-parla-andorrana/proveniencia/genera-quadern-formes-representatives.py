"""Genera una vista llegible de les 35 formes i els seus contextos ASR."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "quadern-formes-representatives.md"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def clean(value: str) -> str:
    return " ".join((value or "").replace("|", "\\|").split())


def main() -> None:
    coverage = read(PROV / "auditoria-cobertura-formes.tsv")
    evidence = read(PROV / "evidencia-formes-vtt.tsv")
    people = {row["id_persona"]: row for row in read(ROOT / "persones.tsv")}
    by_form: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in evidence:
        by_form[row["forma"]].append(row)
    lines = [
        "# Quadern de formes representatives del corpus de parla andorrana",
        "",
        "Aquest quadern resumeix les **35 formes candidates** amb cobertura canònica i tres contextos ASR temporals de parlants diferents quan n'hi ha. Les cites són transcripcions automàtiques localitzables; no confirmen la forma, la variant ni cap tret dialectal fins que s'escolti el WAV.",
        "",
        "La prioritat prové de `auditoria-cobertura-formes.tsv`; els intervals provenen de `evidencia-formes-vtt.tsv`.",
        "",
    ]
    for index, stat in enumerate(coverage, 1):
        form = stat["forma"]
        rows = sorted(by_form.get(form, []), key=lambda row: (row["id_persona"], float(row["start_s"])))
        selected: list[dict[str, str]] = []
        seen: set[str] = set()
        for row in rows:
            if row["id_persona"] not in seen:
                selected.append(row); seen.add(row["id_persona"])
            if len(selected) == 3:
                break
        lines.extend([
            f"## {index}. {form}",
            "",
            f"- **Categoria:** {stat['categoria']} · **parlants canònics:** {stat['n_parlants_canònics']} · **registres de font:** {stat['n_registres_font']} · **ocurrències ASR:** {stat['n_ocurrencies_asr']}",
            f"- **Cobertura:** {stat['nivell_cobertura']} · **prioritat d'audició:** {stat['prioritat_audicio']}",
            "",
        ])
        if not selected:
            lines.append("No hi ha context VTT temporal seleccionable en la taula d'evidència.")
        else:
            lines.extend(["| parlant | interval VTT | context ASR | fitxa |", "|---|---:|---|---|"])
            for row in selected:
                person = people.get(row["id_persona"], {})
                name = clean(person.get("nom_public", row["id_persona"]))
                lines.append(f"| {name} (`{row['id_persona']}`) | {row['interval_vtt']} s | {clean(row['text_segment'])} | [informe](../persones/{row['id_persona']}.md) |")
        lines.extend(["", "**Estat:** evidència ASR temporal; pendent d'audició humana.", ""])
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(coverage)} formes · {sum(len(by_form[row['forma']]) for row in coverage)} contextos VTT · {OUT}")


if __name__ == "__main__":
    main()
