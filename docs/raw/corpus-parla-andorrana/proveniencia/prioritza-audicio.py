"""Combina els senyals automàtics per ordenar la revisió humana dels clips."""

from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def read(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def flag(value: str) -> bool:
    return value.strip().lower() in {"sí", "si", "yes", "1"}


def main() -> None:
    queue = {(r["id_persona"], r["forma"]): r for r in read(PROV / "pla-audicio.tsv")}
    qa = {(r["id_persona"], r["forma"]): r for r in read(PROV / "qa-clips.tsv")}
    rows = []
    for key, row in queue.items():
        q = qa[key]
        temporal = flag(row["coincidencia_temporal_asr"])
        consens = flag(row["consens_dos_asr"])
        qa_match = flag(q["forma_en_qa"])
        score = (4 if consens else 0) + (3 if temporal else 0) + (2 if qa_match else 0)
        if consens and temporal and qa_match:
            categoria = "A-triple-consens"
        elif consens and qa_match:
            categoria = "B-doble-ASR"
        elif qa_match:
            categoria = "C-una-passada"
        else:
            categoria = "D-divergent"
        rows.append({
            "prioritat_global": row.get("prioritat_global", ""),
            "score_evidencia": str(score),
            "categoria": categoria,
            "forma": row["forma"],
            "id_persona": row["id_persona"],
            "interval_escolta": row["interval_escolta"],
            "clip": q["clip"],
            "consens_dos_asr": "sí" if consens else "no",
            "coincidencia_temporal_asr": "sí" if temporal else "no",
            "forma_en_qa": "sí" if qa_match else "no",
            "conf_min_segment": row["conf_min_segment"],
            "conf_min_base_segment": row["conf_min_base_segment"],
            "estat_audicio": row["estat_audicio"],
        })
    rows.sort(key=lambda r: (-int(r["score_evidencia"]), r["prioritat_global"], r["id_persona"], r["forma"]))
    output = PROV / "prioritat-audicio.tsv"
    fields = list(rows[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    from collections import Counter
    print(len(rows), Counter(r["categoria"] for r in rows))


if __name__ == "__main__":
    main()
