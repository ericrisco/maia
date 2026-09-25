"""Afig l'inventari complet de formes candidates a cada fitxa de parlant."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).parents[1]
MATRIX = ROOT / "grafo" / "matriu-formes.tsv"
MARKER = "### Inventari complet de formes candidates"
ANCHOR = "### Perfil lingüístic automatitzat\n"


def read_matrix() -> dict[str, list[dict[str, str]]]:
    by_person: dict[str, list[dict[str, str]]] = {}
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            by_person.setdefault(row["id_persona"], []).append(row)
    return by_person


def table(rows: list[dict[str, str]]) -> str:
    lines = [
        MARKER,
        "",
        "La taula cobreix totes les **35 formes candidates** de la matriu de la fitxa. El recompte prové de l'ASR i la columna de clip només indica que hi ha un fragment localitzable; cap fila confirma per si sola la forma parlada.",
        "",
        "| categoria | forma | ocurrències ASR | clip QA | forma en QA | estat |",
        "|---|---|---:|---|---|---|",
    ]
    for row in rows:
        clip = row["clip_qa"] or "—"
        if clip:
            clip = f"`{clip}`"
        lines.append(
            f"| {row['categoria']} | **{row['forma']}** | {row['recompte_asr']} | {clip} | {row['forma_en_qa']} | {row['estat']} |"
        )
    lines.extend(
        [
            "",
            "La font regenerable és `../grafo/matriu-formes.tsv`; la confirmació auditiva, la variant transcrita, la fonètica i la prosòdia es mantenen separades al registre d'audició.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    by_person = read_matrix()
    changed = 0
    for person, rows in by_person.items():
        path = ROOT / "persones" / f"{person}.md"
        text = path.read_text(encoding="utf-8")
        if MARKER in text:
            continue
        if ANCHOR not in text:
            raise SystemExit(f"{path}: no trobo l'àncora del perfil lingüístic")
        text = text.replace(ANCHOR, table(rows) + "\n" + ANCHOR, 1)
        path.write_text(text, encoding="utf-8")
        changed += 1
    if set(by_person) != {p.stem for p in (ROOT / "persones").glob("pa-*.md")}:
        raise SystemExit("la matriu i les fitxes no tenen el mateix conjunt de persones")
    print(f"{sum(len(rows) for rows in by_person.values())} files de formes · {len(by_person)} persones · informes actualitzats: {changed}")


if __name__ == "__main__":
    main()
