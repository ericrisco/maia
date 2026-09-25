"""Completa l'informe dels clips de consens sense token localitzat."""

from __future__ import annotations

from pathlib import Path
import csv

PROV = Path(__file__).parent
OUT = PROV / "informe-token-missing.md"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    priority = [r for r in read("prioritat-consens-token.tsv") if r["prioritat_token"] == "A-token-missing"]
    consensus = {(r["id_persona"], r["forma"], r["interval_escolta"]): r for r in read("qa-clips-consens.tsv")}
    acoustic = {(r["id_persona"], r["forma"], r["interval_escolta"]): r for r in read("analisi-acustica-consens.tsv")}
    lines = [
        "# Incidències de tokenització en consensos ASR",
        "",
        "Aquest informe recull els **14 clips** on `ggml-small.bin` i `ggml-base.bin` "
        "coincideixen a nivell de text del fragment, però la passada JSON base no troba "
        "una seqüència de tokens que coincideixi exactament amb la forma. No són "
        "descartes: són els primers casos per escoltar i decidir si hi ha segmentació, "
        "reducció fonètica, variant lèxica o error ASR.",
        "",
        "Cada entrada conserva l'àudio, el JSON complet i els descriptors acústics.",
        "",
    ]
    for row in priority:
        key = (row["id_persona"], row["forma"], row["interval_escolta"])
        q = consensus[key]
        a = acoustic[key]
        lines.extend([
            f"## {row['id_persona']} — {row['forma']} — {row['interval_escolta']}",
            "",
            f"- Àudio: [`{row['clip']}`]({row['clip']})",
            f"- JSON base: [`{row['json_base']}`]({row['json_base']})",
            f"- Text small: {q['text_small']}",
            f"- Text base: {q['text_base']}",
            f"- Interval: {row['interval_escolta']} s · F0: {a['f0_median_hz']} Hz · veu: {a['veu_proporcio']} · pausa: {a['pausa_mediana_s']} s · centroid: {a['centroid_median_hz']} Hz",
            "- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.",
            "- Decisió auditiva: `pendent`",
            "- Variant escoltada:",
            "- Trets fonètics:",
            "- Prosòdia / pauses:",
            "- Nota:",
            "",
        ])
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(priority)} casos documentats a {OUT}")


if __name__ == "__main__":
    main()
