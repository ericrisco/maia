"""Compara les finestres de quarantena small/base i actualitza les fitxes."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Comparació ASR de quarantena"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    small = {(r["id_persona"], r["inici_s"]): r for r in read("qa-quarantena.tsv")}
    base = {(r["id_persona"], r["inici_s"]): r for r in read("qa-quarantena-base.tsv")}
    rows = []
    by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for key, s in small.items():
        b = base[key]
        row = {
            "id_persona": s["id_persona"], "inici_s": s["inici_s"], "durada_s": s["durada_s"], "clip": s["clip"],
            "small_ratio_uniques": s["ratio_uniques"], "base_ratio_uniques": b["ratio_uniques_base"],
            "small_text": Path(PROV / s["transcripcio"]).read_text(encoding="utf-8", errors="replace").strip().replace("\n", " "),
            "base_text": b["text_base"],
        }
        rows.append(row); by_person[s["id_persona"]].append(row)
    fields = ["id_persona", "inici_s", "durada_s", "clip", "small_ratio_uniques", "base_ratio_uniques", "small_text", "base_text"]
    with (PROV / "qa-quarantena-comparativa.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    lines = [
        "# Comparació ASR de les veus en quarantena", "",
        "La passada `small` ja havia produït nou finestres de control. Aquesta comparació afegeix `base` "
        "sobre les mateixes finestres. La proporció de línies úniques és només un indicador de repetició; "
        "no resol si el text és fidel a l'àudio.", "",
    ]
    for pid in sorted(by_person):
        items = by_person[pid]
        lines.extend([f"## {pid}", ""])
        for row in items:
            lines.extend([
                f"### {row['inici_s']}–{float(row['inici_s']) + float(row['durada_s']):g} s",
                f"- Àudio: [`{row['clip']}`]({row['clip']})",
                f"- Unicitat small/base: {row['small_ratio_uniques']} / {row['base_ratio_uniques']}",
                f"- Text small: {row['small_text']}",
                f"- Text base: {row['base_text']}",
                "- Decisió: `pendent-audicio`",
                "",
            ])
        report = ROOT / "persones" / f"{pid}.md"
        text = report.read_text(encoding="utf-8")
        if MARKER in text:
            text = text[: text.index(MARKER)].rstrip() + "\n"
        section = (
            f"\n{MARKER}\n\n"
            f"Les nou finestres de control tenen una segona passada amb `ggml-base.bin`; els textos i les "
            f"proporcions d'unicitat es conserven a `../proveniencia/qa-quarantena-comparativa.tsv`. "
            "La veu continua en quarantena perquè la coherència textual automàtica no substitueix la revisió auditiva.\n\n"
            f"La resegmentació auxiliar en finestres de 20 segons queda a `../proveniencia/qa-quarantena-20s.tsv` "
            f"i la transcripció combinada a `../proveniencia/qa-quarantena-20s/{pid}-combinada.txt`; "
            "aquesta capa redueix els bucles de context però continua sent ASR pendent d'escolta.\n"
        )
        report.write_text(text.rstrip() + "\n" + section, encoding="utf-8")
    (PROV / "informe-quarantena-comparativa.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(rows)} finestres comparades · {len(by_person)} veus")


if __name__ == "__main__":
    main()
