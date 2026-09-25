"""Afegeix el mapa complet de 18 dimensions a cada informe de persona."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
PERSONES = ROOT / "persones"
MARKER = "### Repertori lingüístic complet"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def render(rows: list[dict[str, str]]) -> str:
    lines = [
        MARKER,
        "",
        "Aquest mapa desplega les 18 dimensions del repertori per a aquesta persona. Les columnes d'evidència provenen de l'ASR i de mesures instrumentals; `requereix escolta` i `sense evidència específica` indiquen buits, no absència del tret.",
        "",
        "| categoria | candidat de revisió | referència | indicador automàtic | evidència | clips | observació auditiva |",
        "|---|---|---|---|---|---:|---|",
    ]
    for row in rows:
        clean = lambda value: (value or "").replace("|", "\\|").replace("\n", " ").strip()
        lines.append(
            f"| {clean(row['categoria'])} | **{clean(row['candidat'])}** | {clean(row['referencia'])} | {clean(row['indicador_automatic'])} | {clean(row['estat_evidencia'])} | {clean(row['n_clips_consens_boundary'])} | {clean(row['observacio_auditiva']) or 'pendent'} |"
        )
    lines.extend(
        [
            "",
            "Les referències orienten la revisió i no són etiquetes aplicades. La confirmació ha d'incloure el clip escoltat, la variant, els trets fonètics i la prosòdia quan siguin pertinents.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read(PROV / "repertori-evidencia.tsv"):
        by_person[row["id_persona"]].append(row)
    changed = 0
    for person, rows in sorted(by_person.items()):
        path = PERSONES / f"{person}.md"
        if not path.exists():
            raise SystemExit(f"fitxa absent: {path}")
        text = path.read_text(encoding="utf-8")
        if MARKER in text:
            continue
        anchor = "## Buits registrats\n"
        if anchor not in text:
            raise SystemExit(f"àncora absent: {path}")
        path.write_text(text.replace(anchor, render(rows) + "\n" + anchor, 1), encoding="utf-8")
        changed += 1
    print(f"{sum(len(x) for x in by_person.values())} files de repertori · {len(by_person)} persones · actualitzades {changed}")


if __name__ == "__main__":
    main()
