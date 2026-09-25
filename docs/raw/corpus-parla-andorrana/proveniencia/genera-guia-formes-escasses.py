"""Genera una guia d'escolta per a les deu formes amb cobertura escassa."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "guia-audicio-formes-escasses.tsv"


def guidance(category: str) -> str:
    if category == "territorial":
        return "Confirmar la forma i el sentit; escoltar vocalisme, consonants finals, accent i contacte amb article o preposició; anotar una variant local només si és audible."
    if category == "discurs":
        return "Confirmar la funció discursiva; escoltar reducció vocàlica, contacte entre mots, accent, ritme i frontera prosòdica."
    if category == "morfosintaxi":
        return "Confirmar persona, temps i règim; escoltar clítics, vocals àtones, contacte entre mots i prosòdia de la construcció."
    return "Confirmar la paraula i el sentit; separar lèxic general, col·loquialisme, derivació i possible ús local."


def main() -> None:
    with (PROV / "auditoria-cobertura-formes.tsv").open(encoding="utf-8", newline="") as handle:
        coverage = [row for row in csv.DictReader(handle, delimiter="\t") if row["nivell_cobertura"] == "escassa"]
    with (PROV / "cua-audicio-formes-escasses.tsv").open(encoding="utf-8", newline="") as handle:
        queue = list(csv.DictReader(handle, delimiter="\t"))
    by_form: dict[str, list[dict[str, str]]] = {}
    for row in queue:
        by_form.setdefault(row["forma"], []).append(row)
    rows = []
    for row in coverage:
        clips = by_form.get(row["forma"], [])
        rows.append(
            {
                "forma": row["forma"],
                "categoria": row["categoria"],
                "n_parlants_canònics": row["n_parlants_canònics"],
                "n_ocurrencies_asr": row["n_ocurrencies_asr"],
                "n_clips": str(len(clips)),
                "clips": ";".join(f"{clip['id_persona']}::{clip['clip']}" for clip in clips),
                "guia_observacio": guidance(row["categoria"]),
                "camps_a_omplir": "decisió, variant, trets fonètics, prosòdia/pauses i observació",
                "estat": "pendent d'audició",
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} formes · {sum(int(row['n_clips']) for row in rows)} clips · {OUT}")


if __name__ == "__main__":
    main()
