"""Resumeix quines dimensions del repertori tenen evidència i quines són buits."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
GRAPH = ROOT / "grafo"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    reference = read(GRAPH / "repertori-referencia.tsv")
    applied = read(GRAPH / "repertori-aplicat.tsv")
    evidence = read(PROV / "repertori-evidencia.tsv")
    by_dimension: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in evidence:
        by_dimension[(row["categoria"], row["candidat"])].append(row)
    rows = []
    for item in reference:
        group = by_dimension[(item["categoria"], item["candidat"])]
        states = Counter(row["estat_evidencia"] for row in group)
        indicators = Counter(row["estat_indicador"] for row in group)
        rows.append({
            "categoria": item["categoria"],
            "candidat": item["candidat"],
            "referencia": item["evidencia_referencia"],
            "n_persones": len(group),
            "n_amb_evidencia": sum(n for state, n in states.items() if state != "sense evidència específica"),
            "n_sense_evidencia": states.get("sense evidència específica", 0),
            "estats_evidencia": "; ".join(f"{state}={n}" for state, n in sorted(states.items())),
            "indicadors": "; ".join(f"{state}={n}" for state, n in sorted(indicators.items())),
            "estat_global": "pendent d'audició" if not any(row["observacio_auditiva"].strip() for row in group) else "amb observacions auditives",
        })
    out = PROV / "resum-cobertura-repertori.tsv"
    fields = list(rows[0])
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    lines = [
        "# Cobertura del repertori lingüístic",
        "",
        f"El repertori té **{len(reference)} dimensions** aplicades a **{len(applied)} files** (66 persones × 18 candidats). El resum separa evidència textual o acústica de buits i no transforma cap indicador automàtic en tret dialectal.",
        "",
        "| categoria | dimensió | amb evidència | sense evidència específica | estat global |",
        "|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row['categoria']} | **{row['candidat']}** | {row['n_amb_evidencia']} | {row['n_sense_evidencia']} | {row['estat_global']} |")
    lines += [
        "",
        "La major part de les dimensions fonètiques, morfològiques, sintàctiques i de variació no són inferibles de la grafia ASR. Els 61 indicadors textuals de pragmàtica i els 62 descriptors acústics de prosòdia només orienten la cua d'audició.",
        "",
        "El detall regenerable és `proveniencia/resum-cobertura-repertori.tsv`; les observacions humanes s'han d'escriure a `grafo/repertori-aplicat.tsv` després d'escoltar el clip corresponent.",
        "",
    ]
    (GRAPH / "informe-cobertura-repertori.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(rows)} dimensions · {len(applied)} files · {sum(int(row['n_amb_evidencia']) for row in rows)} observacions automàtiques")


if __name__ == "__main__":
    main()
