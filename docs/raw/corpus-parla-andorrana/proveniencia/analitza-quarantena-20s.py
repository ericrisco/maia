"""Compta formes candidates en les transcripcions curtes de quarantena."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
FORMS = ROOT / "grafo" / "trets-formes-completa.tsv"
OUT = PROV / "qa-quarantena-20s-formes.tsv"
PERSONES = ("pa-044", "pa-047", "pa-050")
MARKER = "### Formes candidates en la resegmentació de 20 segons"


def read_forms() -> list[dict[str, str]]:
    with FORMS.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def count(text: str, form: str) -> int:
    pattern = re.compile(r"(?<!\w)" + re.escape(form) + r"(?!\w)", re.IGNORECASE)
    return len(pattern.findall(text))


def main() -> None:
    forms = read_forms()
    rows: list[dict[str, str]] = []
    texts: dict[str, str] = {}
    for person in PERSONES:
        text_path = PROV / "qa-quarantena-20s" / f"{person}-combinada.txt"
        texts[person] = text_path.read_text(encoding="utf-8", errors="replace") if text_path.exists() else ""
        for form in forms:
            rows.append({
                "id_persona": person,
                "forma": form["forma"],
                "categoria": form["categoria"],
                "ocurrencies_asr_20s": str(count(texts[person], form["forma"])),
                "estat": "candidat ASR; pendent d'audicio",
            })
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    for person in PERSONES:
        report = ROOT / "persones" / f"{person}.md"
        text = report.read_text(encoding="utf-8")
        if MARKER in text:
            text = text[: text.index(MARKER)].rstrip() + "\n"
        values = [row for row in rows if row["id_persona"] == person and int(row["ocurrencies_asr_20s"]) > 0]
        values.sort(key=lambda row: (-int(row["ocurrencies_asr_20s"]), row["forma"]))
        lines = [MARKER, "", "Els recomptes següents provenen només de la transcripció ASR resegmentada; no confirmen cap variant sense escolta.", "", "| categoria | forma | ocurrències ASR 20 s | estat |", "|---|---|---:|---|"]
        lines.extend(f"| {row['categoria']} | **{row['forma']}** | {row['ocurrencies_asr_20s']} | {row['estat']} |" for row in values)
        lines.append("")
        report.write_text(text.rstrip() + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} files de formes · {OUT}")


if __name__ == "__main__":
    main()
