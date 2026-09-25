"""Sincronitza els clips de les sessions canòniques 01–02 i 05."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
PERSONES = ROOT / "persones"
MARKER = "### Sessions operatives 01–02 i 05"
OLD_MARKER = "### Sessions operatives 01–02"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def block(rows: list[dict[str, str]]) -> str:
    lines = [
        MARKER,
        "",
        "Aquesta selecció operativa mostra els clips prioritzats per iniciar l'audició. Els textos i les mesures són suport automàtic; la forma, la variant, la fonètica i la prosòdia continuen pendents fins a escoltar el WAV.",
        "",
        "| sessió | forma | clip | prioritat | text small | text base |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        clean = lambda value: (value or "").replace("|", "\\|").replace("\n", " ").strip()
        lines.append(
            f"| {row['sessio']} | **{clean(row['forma'])}** | `{clean(row['clip'])}` | {clean(row['prioritat'])} | {clean(row.get('text_small', ''))} | {clean(row.get('text_base', ''))} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for name in ("sessio-01.tsv", "sessio-02.tsv", "sessio-05.tsv", "sessio-06.tsv"):
        for row in read(PROV / "sessions" / name):
            if row.get("origen") != "canònic":
                continue
            item = dict(row)
            item["sessio"] = name.removesuffix(".tsv")
            by_person[row["persona"]].append(item)
    changed = 0
    for person, rows in by_person.items():
        path = PERSONES / f"{person}.md"
        if not path.exists():
            raise SystemExit(f"fitxa absent: {path}")
        text = path.read_text(encoding="utf-8")
        anchor = "## Buits registrats\n"
        if anchor not in text:
            raise SystemExit(f"àncora absent: {path}")
        start = text.find(MARKER)
        if start < 0:
            start = text.find(OLD_MARKER)
        if start >= 0:
            section_endings = [position for position in (text.find("### Repertori lingüístic complet", start), text.find(anchor, start)) if position >= 0]
            end = min(section_endings) if section_endings else -1
            if end < 0:
                raise SystemExit(f"àncora final absent: {path}")
            text = text[:start] + block(rows) + "\n" + text[end:]
        else:
            text = text.replace(anchor, block(rows) + "\n" + anchor, 1)
        path.write_text(text, encoding="utf-8")
        changed += 1
    print(f"{sum(len(x) for x in by_person.values())} clips · {len(by_person)} fitxes · actualitzades {changed}")


if __name__ == "__main__":
    main()
