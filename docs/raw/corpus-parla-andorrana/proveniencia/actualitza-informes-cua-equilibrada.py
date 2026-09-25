"""Copia la mostra equilibrada d'audició dins de les 66 fitxes."""
from collections import defaultdict
from pathlib import Path
import csv
import re

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
SAMPLE = PROV / "cua-audicio-small-equilibrada.tsv"
MARKER = "### Mostra equilibrada small per a l'audició"


def replace_section(text: str, marker: str, section: str) -> str:
    """Reemplaça només la secció marcada i conserva les que venen després."""
    if marker in text:
        start = text.index(marker)
        next_heading = re.search(r"\n#{2,3} ", text[start + len(marker) :])
        if next_heading:
            end = start + len(marker) + next_heading.start() + 1
            suffix = text[end:].lstrip("\n")
            return text[:start].rstrip() + "\n\n" + section.rstrip() + "\n\n" + suffix
        return text[:start].rstrip() + "\n\n" + section.rstrip() + "\n"
    return text.rstrip() + "\n\n" + section.rstrip() + "\n"


def main():
    with SAMPLE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    by_person = defaultdict(list)
    for row in rows:
        by_person[row["id_persona"]].append(row)
    updated = 0
    for report in sorted((ROOT / "persones").glob("pa-*.md")):
        person = report.stem
        text = report.read_text(encoding="utf-8")
        selected = by_person.get(person, [])
        lines = [MARKER, "", "Aquesta fitxa forma part de la mostra equilibrada de 100 clips small. La selecció cobreix els 63 parlants amb ocurrències tokenitzades i les 20 formes; és una cua de priorització i continua pendent d'escolta.", ""]
        if selected:
            forms = ", ".join(sorted({r["forma"] for r in selected}))
            n_clips = len(selected)
            n_forms = len(forms.split(", "))
            clips_label = "clip" if n_clips == 1 else "clips"
            forms_label = "forma" if n_forms == 1 else "formes"
            lines.append(f"La mostra inclou **{n_clips} {clips_label}** i **{n_forms} {forms_label}** per a aquesta veu: {forms}.")
            lines.append("")
            for row in sorted(selected, key=lambda r: float(r["absolute_start_s"])):
                name = Path(row["clip"]).name
                lines.append(f"- **{row['forma']}** · [{name}](../proveniencia/clips/{name}) · {row['absolute_start_s']}–{row['absolute_end_s']} s · p={row['prob_min']} · decisió auditiva: pendent")
        else:
            lines.append("Aquesta veu no té una ocurrència tokenitzada small en la mostra; queda coberta per la cua global de 656 clips.")
        lines += ["", "Els camps de variant, fonètica i prosòdia es completen només després d'escoltar el WAV.", ""]
        report.write_text(replace_section(text, MARKER, "\n".join(lines)), encoding="utf-8")
        updated += 1
    print(f"OK: {updated} informes actualitzats")


if __name__ == "__main__":
    main()
