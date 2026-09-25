"""Afegeix evidència actual a cada dimensió del repertori sense omplir l'audició humana."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv
from statistics import median

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    repertori = read(ROOT / "grafo" / "repertori-aplicat.tsv")
    boundary = [row for row in read(PROV / "qa-clips-boundary.tsv") if row["consens_limit_paraula"] == "sí"]
    acoustic = read(PROV / "analisi-acustica-normalitzada-consens.tsv")
    forms: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in boundary:
        forms[(row["id_persona"], row["forma"])].append(row)
    acoustic_by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in acoustic:
        acoustic_by_person[row["id_persona"]].append(row)
    rows = []
    for row in repertori:
        key = (row["id_persona"], row["candidat"])
        hits = forms.get(key, [])
        person_acoustic = acoustic_by_person.get(row["id_persona"], [])
        out = dict(row)
        out["n_clips_consens_boundary"] = str(len(hits))
        out["intervals_consens_boundary"] = ",".join(hit["interval_escolta"] for hit in hits)
        person_hits = [item for (person, _form), values in forms.items() if person == row["id_persona"] for item in values]
        if hits:
            out["estat_evidencia"] = "consens textual amb límit de paraula"
        elif row["categoria"] == "pragmàtica" and person_hits:
            out["estat_evidencia"] = "marcadors textuals consensuals; forma global pendent"
        elif row["categoria"] == "prosòdia" and person_acoustic:
            out["estat_evidencia"] = "descriptor acústic normalitzat"
        else:
            out["estat_evidencia"] = "sense evidència específica"
        if person_acoustic and row["categoria"] == "prosòdia":
            out["delta_f0_z_median_persona"] = f"{median(float(item['delta_f0_z_persona']) for item in person_acoustic):.3f}"
            out["delta_veu_median_persona"] = f"{median(float(item['delta_veu']) for item in person_acoustic):.4f}"
            out["delta_pausa_median_persona"] = f"{median(float(item['delta_pausa_s']) for item in person_acoustic):.3f}"
        else:
            out["delta_f0_z_median_persona"] = ""
            out["delta_veu_median_persona"] = ""
            out["delta_pausa_median_persona"] = ""
        rows.append(out)
    fields = list(repertori[0]) + ["n_clips_consens_boundary", "intervals_consens_boundary", "estat_evidencia", "delta_f0_z_median_persona", "delta_veu_median_persona", "delta_pausa_median_persona"]
    out_path = PROV / "repertori-evidencia.tsv"
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(rows)
    from collections import Counter
    print(f"{len(rows)} files · {dict(Counter(row['estat_evidencia'] for row in rows))} · {out_path}")


if __name__ == "__main__":
    main()
