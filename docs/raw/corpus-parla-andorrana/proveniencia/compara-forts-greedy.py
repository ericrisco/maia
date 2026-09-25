"""Compara les tres decodificacions dels 109 clips forts."""

from collections import Counter, defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Tercera descodificació dels clips forts"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def replace_section(text: str, marker: str, section: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + section
    start = text.index(marker)
    next_heading = text.find("\n### ", start + len(marker))
    end = len(text) if next_heading == -1 else next_heading + 1
    return text[:start].rstrip() + "\n" + section.rstrip() + "\n\n" + text[end:].lstrip()


def main() -> None:
    forts = read("candidats-forts.tsv")
    small = {(r["id_persona"], r["forma"]): r for r in read("qa-clips.tsv")}
    base = {(r["id_persona"], r["forma"]): r for r in read("qa-clips-base.tsv")}
    greedy = {(r["id_persona"], r["forma"]): r for r in read("qa-clips-forts-greedy.tsv")}
    rows = []
    by_person: dict[str, Counter[str]] = defaultdict(Counter)
    for row in forts:
        key = (row["id_persona"], row["forma"])
        values = {
            "small": small[key]["forma_en_qa"] == "sí",
            "base": base[key]["forma_en_base"] == "sí",
            "greedy": greedy[key]["forma_en_greedy"] == "sí",
        }
        names = [name for name, yes in values.items() if yes]
        if len(names) == 3:
            category = "A-tres-models"
        elif len(names) == 2:
            category = "B-dos-models"
        elif len(names) == 1:
            category = "C-un-model"
        else:
            category = "D-cap-model"
        row_out = {
            "id_persona": row["id_persona"], "forma": row["forma"], "clip": row["clip"],
            "small": "sí" if values["small"] else "no", "base": "sí" if values["base"] else "no", "greedy": "sí" if values["greedy"] else "no",
            "categoria": category, "text_small": small[key]["text_qa"], "text_base": base[key]["text_base"], "text_greedy": greedy[key]["text_greedy"],
        }
        rows.append(row_out)
        by_person[row["id_persona"]][category] += 1
    fields = list(rows[0])
    with (PROV / "qa-clips-forts-consens.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    counts = Counter(row["categoria"] for row in rows)
    lines = ["# Comparació de tres descodificacions dels clips forts", "", f"La cua té **{len(rows)} clips**. La tercera passada és una descodificació greedy del mateix model small; cap categoria substitueix l'escolta humana.", "", "| Categoria | Clips |", "|---|---:|"]
    lines.extend(f"| {category} | {counts.get(category, 0)} |" for category in ("A-tres-models", "B-dos-models", "C-un-model", "D-cap-model"))
    lines += ["", "## Divergències que mereixen escolta prioritària", ""]
    for row in rows:
        if row["categoria"] != "A-tres-models":
            lines.append(f"- **{row['id_persona']} · {row['forma']}** ({row['categoria']}): small=`{row['text_small']}`; base=`{row['text_base']}`; greedy=`{row['text_greedy']}` — `{row['clip']}`")
    (PROV / "informe-forts-greedy.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    reports = ROOT / "persones"
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        all_people = [row["id_persona"] for row in csv.DictReader(handle, delimiter="\t")]
    for pid in all_people:
        person_counts = by_person.get(pid, Counter())
        report = reports / f"{pid}.md"
        text = report.read_text(encoding="utf-8")
        details = "; ".join(f"{k}={v}" for k, v in sorted(person_counts.items())) or "cap clip fort"
        section = f"\n{MARKER}\n\nEn els clips forts d'aquesta persona, la tercera descodificació dona **{sum(person_counts.values())} casos**: {details}. És una priorització de divergències entre models i continua pendent d'escolta.\n"
        report.write_text(replace_section(text, MARKER, section), encoding="utf-8")
    print(" ".join(f"{key}={counts.get(key, 0)}" for key in ("A-tres-models", "B-dos-models", "C-un-model", "D-cap-model")))


if __name__ == "__main__":
    main()
