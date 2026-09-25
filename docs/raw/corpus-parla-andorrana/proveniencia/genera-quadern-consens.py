"""Genera un quadern Markdown per auditar els clips amb doble consens ASR."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "quadern-audicio-consens.md"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    consens = [row for row in read("qa-clips-consens.tsv") if row["consens_textual"] == "sí"]
    acoustic = {
        (row["id_persona"], row["forma"], row["interval_escolta"]): row
        for row in read("analisi-acustica-consens.tsv")
    }
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in consens:
        grouped[row["id_persona"]].append(row)
    lines = [
        "# Quadern d'audició dels consensos ASR",
        "",
        f"{len(consens)} clips on `ggml-small.bin` i `ggml-base.bin` coincideixen textualment. "
        "La coincidència orienta l'escolta i no confirma la pronúncia.",
        "",
        "Per cada clip, escoltar l'àudio i completar: **sí/no/incerta**, variant escoltada, "
        "trets fonètics, prosòdia i nota. Les dades automàtiques no són una decisió humana.",
        "",
    ]
    for person in sorted(grouped):
        items = sorted(grouped[person], key=lambda r: (r["forma"], r["interval_escolta"]))
        lines.extend([f"## {person} ({len(items)} clips)", ""])
        for row in items:
            key = (row["id_persona"], row["forma"], row["interval_escolta"])
            a = acoustic[key]
            lines.extend(
                [
                    f"### {row['forma']} · {row['interval_escolta']}",
                    "",
                    f"- Àudio: [`{row['clip']}`]({row['clip']})",
                    f"- Text small: {row['text_small']}",
                    f"- Text base: {row['text_base']}",
                    f"- F0 mediana: {a['f0_median_hz']} Hz · IQR F0: {a['f0_iqr_hz']} Hz · veu: {a['veu_proporcio']} · pausa: {a['pausa_mediana_s']} s · centroid: {a['centroid_median_hz']} Hz",
                    "- Decisió auditiva: `pendent`",
                    "- Variant escoltada:",
                    "- Trets fonètics observats:",
                    "- Prosòdia / pauses:",
                    "- Nota:",
                    "",
                ]
            )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generat {OUT} amb {len(consens)} clips i {len(grouped)} persones")


if __name__ == "__main__":
    main()
