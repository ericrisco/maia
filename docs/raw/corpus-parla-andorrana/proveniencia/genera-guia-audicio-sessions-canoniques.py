"""Construeix una guia de revisió lingüística per a les sessions 01–02, 05 i 06."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "guia-audicio-sessions-canoniques.tsv"

FORM_CATEGORIES = {
    "a nivell": "discurs", "a veure": "discurs", "aleshores": "discurs", "aviam": "discurs",
    "bueno": "discurs", "bé": "discurs", "clar": "discurs", "de fet": "discurs",
    "diguem": "discurs", "doncs": "discurs", "evidentment": "discurs", "llavors": "discurs",
    "no?": "discurs", "o sigui": "discurs", "per tant": "discurs", "perquè": "discurs",
    "vull dir": "discurs", "és a dir": "discurs", "Canillo": "territorial", "Escaldes": "territorial",
    "Massana": "territorial", "Ordino": "territorial", "Sant Julià": "territorial", "aiguats": "territorial",
    "andorrana": "territorial", "comunal": "territorial", "comunals": "territorial", "comuns": "territorial",
    "comú": "territorial", "copríncep": "territorial", "coprínceps": "territorial", "padrí": "territorial",
    "parròquia": "territorial", "santuari": "territorial", "veguer": "territorial",
    "crec": "morfosintaxi", "ensenyança": "lèxic", "reformeta": "lèxic", "tirar endavant": "lèxic",
}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def cues(category: str, form: str) -> str:
    if category == "territorial":
        return "confirmar lèxic local; accent i realització de vocals/consonants; separar nom propi o terminologia institucional"
    if category == "lèxic":
        return "confirmar la paraula i el sentit; separar lèxic general, col·loquialisme, derivació i possible ús local"
    if category == "morfosintaxi":
        return "confirmar persona, temps i règim verbal; escoltar pronúncia dels clítics i la prosòdia de la construcció"
    if form in {"bé", "bueno", "clar", "doncs", "llavors", "vull dir", "a veure", "per tant", "evidentment"}:
        return "confirmar funció discursiva; escoltar reducció vocàlica, contacte entre mots, accent i frontera prosòdica"
    return "confirmar si és la forma candidata; escoltar vocals, consonants finals, ritme, pausa i entonació"


def main() -> None:
    sessions = []
    for name in ("sessio-01.tsv", "sessio-02.tsv", "sessio-05.tsv", "sessio-06.tsv"):
        sessions.extend(read(PROV / "sessions" / name))
    rows = []
    for row in sessions:
        if row.get("origen") != "canònic":
            continue
        category = FORM_CATEGORIES.get(row["forma"], "altres")
        rows.append(
            {
                "id_global": row["id_global"],
                "sessio": "",
                "persona": row["persona"],
                "forma": row["forma"],
                "categoria": category,
                "clip": row["clip"],
                "prioritat": row["prioritat"],
                "prob_min": row["prob_min"],
                "text_small": row.get("text_small", ""),
                "text_base": row.get("text_base", ""),
                "f0_median_hz": row.get("f0_median_hz", ""),
                "f0_iqr_hz": row.get("f0_iqr_hz", ""),
                "pausa_mediana_s": row.get("pausa_mediana_s", ""),
                "f1_hz": row.get("f1_hz", ""),
                "f2_hz": row.get("f2_hz", ""),
                "f3_hz": row.get("f3_hz", ""),
                "guia_observacio": cues(category, row["forma"]),
                "estat": "pendent d'audició",
            }
        )
    # La sessió és la font del fitxer, no una inferència sobre l'ordre.
    cursor = 0
    for name in ("sessio-01.tsv", "sessio-02.tsv", "sessio-05.tsv", "sessio-06.tsv"):
        source = [r for r in read(PROV / "sessions" / name) if r.get("origen") == "canònic"]
        for row in rows[cursor: cursor + len(source)]:
            row["sessio"] = name.removesuffix(".tsv")
        cursor += len(source)
    fields = list(rows[0])
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} clips")


if __name__ == "__main__":
    main()
