"""Selecciona la primera sessió d'audició amb evidència textual alta."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT_DIR = PROV / "sessions"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    canonical = read(PROV / "prioritat-audicio-triple.tsv")
    selected = [row for row in canonical if row["prioritat_triple"] == "A-triple-token-fort"][:20]
    selected += [row for row in canonical if row["prioritat_triple"] == "B-triple-token-baix"][:10]
    rows = []
    for index, row in enumerate(selected, start=1):
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
            "motiu": row["justificacio"],
            "estat": "pendent",
        })
    candidate_sets = [
        ("lead-rtva-001", "Joan Verdú", "formes-joan-clips.tsv"),
        ("lead-rtva-002-ian-moya", "Ian Moya", "formes-clips.tsv"),
        ("lead-rtva-003-dj-neura", "DJ Neura", "formes-clips.tsv"),
    ]
    for folder, label, manifest_name in candidate_sets:
        for row in read(PROV / "candidats" / folder / manifest_name):
            rows.append({
                "ordre_sessio": len(rows) + 1,
                "id_global": f"{folder}::{row['forma']}::{len(rows)+1}",
                "origen": label,
                "persona": label,
                "forma": row["forma"],
                "clip": f"candidats/{folder}/{row['clip']}",
                "prioritat": row.get("prioritat", "candidat-ASR"),
                "prob_min": row.get("small", ""),
                "text": "",
                "motiu": "candidat separat; confirmar identitat de veu i forma",
                "estat": "pendent",
            })
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / "sessio-01.tsv"
    fields = list(rows[0])
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    lines = [
        "# Sessió d'audició 01",
        "",
        f"Aquesta sessió conté **{len(rows)} clips**: 30 canònics (20 triples forts i 10 triples de probabilitat baixa) i 35 dels tres candidats RTVA. L'ordre canònic prioritza tres models ASR i timestamp de token; no és una decisió lingüística.",
        "",
        "| ordre | origen | persona | forma | prioritat | clip |",
        "|---:|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['ordre_sessio']} | {row['origen']} | {row['persona']} | **{row['forma']}** | {row['prioritat']} | `{row['clip']}` |")
    lines += [
        "",
        "Per anotar-la, obre `../auditoria-global.html` i filtra per origen, o usa aquest TSV com a manifest. Les decisions s'exporten des de l'auditoria global i es validen amb `importa-auditoria-global.py`.",
        "",
    ]
    (OUT_DIR / "sessio-01.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(rows)} clips · 30 canònics · {len(rows)-30} candidats")


if __name__ == "__main__":
    main()
