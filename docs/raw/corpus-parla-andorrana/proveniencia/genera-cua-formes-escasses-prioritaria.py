"""Selecciona un clip local per cadascuna de les deu formes escasses."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
SOURCE = PROV / "cua-audicio-formes-escasses.tsv"
OUT = PROV / "cua-audicio-formes-escasses-prioritaria.tsv"
README = PROV / "cua-audicio-formes-escasses-prioritaria.md"


def main() -> None:
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    selected = [row for row in rows if row["rang"] == "1"]
    selected.sort(key=lambda row: (int(row["ordre"]), row["forma"]))
    fields = list(selected[0])
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(selected)
    lines = [
        "# Primera cua d’audició de formes escasses",
        "",
        f"Aquesta cua conté **{len(selected)} clips**, un per cadascuna de les deu formes amb menys de deu parlants canònics. Són derivats WAV locals amb hash; la decisió, la variant, la fonètica i la prosòdia continuen `pendent`.",
        "",
        f"Registre: `{OUT.name}`. Reproductor complet amb filtres: [auditoria de formes escasses](auditoria-formes-escasses.html).",
        "",
        "| forma | categoria | parlant | interval | clip | ASR | decisió |",
        "|---|---|---|---:|---|---|---|",
    ]
    for row in selected:
        lines.append(f"| **{row['forma']}** | {row['categoria']} | `{row['id_persona']}` | {row['interval_vtt']} s | [escolta]({row['clip']}) | {row['text_asr']} | pendent |")
    README.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(selected)} clips · {len({row['forma'] for row in selected})} formes · {OUT}")


if __name__ == "__main__":
    main()
