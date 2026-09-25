"""Registra la cobertura documental verificable de cada persona canònica."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-cobertura-persones.tsv"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    matrix = read(ROOT / "grafo" / "matriu-formes.tsv")
    evidence = read(PROV / "evidencia-formes.tsv")
    clips = read(PROV / "clips-audicio.tsv")
    forms = Counter(row["id_persona"] for row in matrix)
    evidences = Counter(row["id_persona"] for row in evidence)
    clip_counts = Counter(row["id_persona"] for row in clips)
    rows = []
    for person in sorted({row["id_persona"] for row in matrix}):
        report = ROOT / "persones" / f"{person}.md"
        source = PROV / person / "README.md"
        audio = ROOT / "audios" / person / "audio.wav"
        transcript = ROOT / "transcripcions" / f"{person}.txt"
        text = report.read_text(encoding="utf-8", errors="replace") if report.exists() else ""
        status = "quarantena" if person in {"pa-044", "pa-047", "pa-050"} else "activa"
        rows.append(
            {
                "id_persona": person,
                "estat": status,
                "fitxa": "sí" if report.exists() else "no",
                "titol": "sí" if any(line.startswith("# ") for line in text.splitlines()) else "no",
                "inventari_35_formes": "sí" if "### Inventari complet de formes candidates" in text else "no",
                "perfil_linguistic": "sí" if "### Perfil lingüístic automatitzat" in text else "no",
                "evidencia_textual": str(evidences[person]),
                "formes_matriu": str(forms[person]),
                "clips_audicio": str(clip_counts[person]),
                "audio_wav": "sí" if audio.exists() else "no",
                "transcripcio_txt": "sí" if transcript.exists() else "no",
                "procedencia": "sí" if source.exists() else "no",
            }
        )
    fields = list(rows[0])
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} persones")


if __name__ == "__main__":
    main()
