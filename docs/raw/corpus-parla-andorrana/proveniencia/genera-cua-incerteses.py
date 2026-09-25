"""Selecciona una mostra equilibrada de clips que contenen tokens ASR incerts."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
TARGET = 100


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    inventory = read("inventari-incerteses-asr.tsv")
    master = read("registre-audicio.tsv")
    refs: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in inventory:
        for clip in row["clips_coberts"].split(";"):
            if clip:
                refs[clip].append(row)
    candidates = []
    for row in master:
        linked = refs.get(row["clip"], [])
        if not linked:
            continue
        probs = [float(value) for item in linked for value in item["probabilitats_baixes"].split(" | ") if value]
        candidates.append({
            **row,
            "segments_incerts": str(len(linked)),
            "min_prob_incert": f"{min(probs):.4f}" if probs else "",
        })
    candidates.sort(key=lambda row: (row["id_persona"], float(row["min_prob_incert"]), row["forma"], row["clip"]))
    selected: list[dict[str, str]] = []
    seen_people: set[str] = set()
    for row in candidates:
        if row["id_persona"] not in seen_people:
            selected.append(row)
            seen_people.add(row["id_persona"])
    for row in sorted(candidates, key=lambda item: (float(item["min_prob_incert"]), item["id_persona"], item["forma"], item["clip"])):
        if len(selected) >= TARGET:
            break
        if row["clip"] not in {item["clip"] for item in selected}:
            selected.append(row)
    if len(selected) != TARGET:
        raise SystemExit(f"mostra incerta amb {len(selected)} clips; calen {TARGET}")
    selected.sort(key=lambda row: (float(row["min_prob_incert"]), row["id_persona"], row["forma"], row["clip"]))
    output = PROV / "cua-audicio-incerteses.tsv"
    fields = list(master[0]) + ["segments_incerts", "min_prob_incert"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(selected)
    lines = [
        "# Cua d'audició d'incerteses ASR",
        "",
        f"Mostra de **{TARGET} clips** de `registre-audicio.tsv` que contenen almenys un token ASR amb probabilitat inferior a 0,55.",
        "",
        "La selecció cobreix primer una fila per persona i després prioritza la probabilitat més baixa. No és una mostra dialectològica: serveix per corregir transcripció i decidir quins fragments mereixen anotació fonètica o prosòdica.",
        "",
        "- Font: `inventari-incerteses-asr.tsv` i `registre-audicio.tsv`.",
        "- Camps humans: es mantenen buits fins a l'escolta.",
        "- Importació: `importa-auditoria.py` pot projectar anotacions si la clau exacta coincideix.",
        "",
        "| ordre | persona | forma | clip | segments incerts | probabilitat mínima | estat |",
        "|---:|---|---|---|---:|---:|---|",
    ]
    for index, row in enumerate(selected, start=1):
        lines.append(f"| {index} | {row['id_persona']} | {row['forma']} | `{row['clip']}` | {row['segments_incerts']} | {row['min_prob_incert']} | {row['estat_audicio']} |")
    (PROV / "quadern-audicio-incerteses.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(selected)} clips · {len(seen_people)} persones · {len(refs)} clips amb segments incerts")


if __name__ == "__main__":
    main()
