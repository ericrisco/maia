"""Selecciona una primera tanda humana de clips candidatos, separada del canon."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
SOURCE = PROV / "auditoria-candidats-completa.html"
OUT = PROV / "cua-audicio-candidats-prioritaria.tsv"
README = PROV / "cua-audicio-candidats-prioritaria.md"
N = 20


def load_items() -> list[dict[str, str]]:
    text = SOURCE.read_text(encoding="utf-8")
    match = re.search(r"const items=(\[.*?\]);const key=", text, re.DOTALL)
    if not match:
        raise ValueError(f"no trobo la càrrega de clips a {SOURCE}")
    return json.loads(match.group(1))


def main() -> None:
    items = [row for row in load_items() if row.get("status", "").replace("’", "'") == "pendent d'audició"]
    priority = {"A-consens-ASR": 0, "B-un-model-ASR": 1, "C-divergència": 2}
    items.sort(key=lambda row: (priority.get(row.get("priority", ""), 9), row["candidate"], float(row["start"]), row["id"]))

    selected: list[dict[str, str]] = []
    seen_candidates: set[str] = set()
    for row in items:
        if row["candidate"] not in seen_candidates:
            selected.append(row)
            seen_candidates.add(row["candidate"])
    for row in items:
        if len(selected) >= N:
            break
        if row not in selected:
            selected.append(row)
    selected = selected[:N]

    fields = [
        "ordre", "id", "candidate", "forma", "clip", "inici_s", "final_s", "prioritat",
        "small", "base", "font", "sha256", "transcripcio_small", "transcripcio_base",
        "estat_audicio", "veu_confirmada", "forma_confirmada",
        "variant_transcrita", "trets_fonetics_observats", "observacions_prosodiques", "nota_audicio",
    ]
    rows = []
    for order, item in enumerate(selected, 1):
        rows.append({
            "ordre": str(order), "id": item["id"], "candidate": item["candidate"],
            "forma": item["form"], "clip": item["clip"], "inici_s": item["start"],
            "final_s": item["end"], "prioritat": item["priority"], "small": item["small"],
            "base": item["base"], "font": item["source"],
            "sha256": hashlib.sha256((PROV / item["clip"]).read_bytes()).hexdigest(),
            "transcripcio_small": item.get("small_transcript", ""),
            "transcripcio_base": item.get("base_transcript", ""),
            "estat_audicio": "pendent",
            "veu_confirmada": "pendent", "forma_confirmada": "pendent", "variant_transcrita": "",
            "trets_fonetics_observats": "", "observacions_prosodiques": "", "nota_audicio": "",
        })
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    candidates = sorted({row["candidate"] for row in rows})
    lines = [
        "# Primera cua d’audició humana dels candidats",
        "",
        f"Aquesta tanda conté **{len(rows)} clips** de **{len(candidates)} candidats**. És una cua de revisió humana separada del cànon; cap resultat entra a `persones.tsv` ni al graf canònic fins que es confirmi la veu i la forma escoltant el WAV.",
        "",
        "La selecció cobreix primer una ocurrència per cadascuna de les 11 veus candidates i completa la tanda amb els casos de prioritat ASR més alta. Els camps humans es mantenen `pendent`.",
        "",
        f"Registre editable: `{OUT.name}`. Àudio i context: [auditoria completa de candidats](auditoria-candidats-completa.html).",
        "",
        "| ordre | candidat | forma | clip | prioritat | àudio | veu | forma |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['ordre']} | `{row['candidate']}` | **{row['forma']}** | `{row['clip']}` | {row['prioritat']} | [escolta]({row['clip']}) | pendent | pendent |"
        )
    README.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} clips · {len(candidates)} candidats · {OUT}")


if __name__ == "__main__":
    main()
