"""Selecciona un clip canònic per cadascuna de les formes del repertori de 20 marcadors."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT_DIR = PROV / "sessions"
ORDER = {"A-triple-token-fort": 0, "B-triple-token-baix": 1, "C-dos-models": 2, "D-un-model": 3, "E-cap-model": 4}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def probability(value: str) -> float:
    values = [float(piece) for piece in value.replace(",", ".").split(";") if piece]
    return min(values) if values else 0.0


def main() -> None:
    prioritat = read(PROV / "prioritat-audicio-triple.tsv")
    first = {row["clip"] for row in read(OUT_DIR / "sessio-01.tsv") if row["origen"] == "canònic"}
    candidates = [row for row in prioritat if row["clip"] not in first]
    candidates.sort(key=lambda row: (ORDER.get(row["prioritat_triple"], 99), -probability(row["token_prob_min"]), row["forma"], row["id_persona"]))
    chosen = {}
    for row in candidates:
        chosen.setdefault(row["forma"], row)
    rows = []
    for index, form in enumerate(sorted(chosen), start=1):
        row = chosen[form]
        rows.append({
            "ordre_sessio": index,
            "id_global": f"canon::{row['id_persona']}::{row['forma']}::{row['ordre_triple']}",
            "origen": "canònic",
            "persona": row["id_persona"],
            "forma": row["forma"],
            "clip": row["clip"],
            "prioritat": row["prioritat_triple"],
            "prob_min": row["token_prob_min"],
            "text": row["text_greedy"],
            "motiu": "cobertura equilibrada: primer clip disponible fora de la sessió 01",
            "estat": "pendent",
        })
    OUT_DIR.mkdir(exist_ok=True)
    fields = list(rows[0])
    with (OUT_DIR / "sessio-02.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    lines = [
        "# Sessió d'audició 02 — cobertura de formes",
        "",
        f"Aquesta sessió conté **{len(rows)} clips canònics**, un per cadascuna de les formes del repertori de 20 marcadors que té un clip disponible fora de la sessió 01. L'ordre prioritza triple ASR i probabilitat de token, però continua pendent d'escolta.",
        "",
        "| ordre | persona | forma | prioritat | clip |",
        "|---:|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['ordre_sessio']} | {row['persona']} | **{row['forma']}** | {row['prioritat']} | `{row['clip']}` |")
    lines += ["", "La sessió es pot obrir amb `../auditoria-global.html`; l'exportació es valida amb `importa-auditoria-global.py`.\n"]
    (OUT_DIR / "sessio-02.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(rows)} formes cobertes")


if __name__ == "__main__":
    main()
