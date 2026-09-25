"""Genera una auditoria de completitud de les fitxes individuals."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-informes.tsv"


def read_sources() -> list[dict[str, str]]:
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    rows: list[dict[str, str]] = []
    quarantine = {"pa-044", "pa-047", "pa-050"}
    checks = {
        "formes": "### Inventari complet de formes candidates",
        "repertori": "### Repertori lingüístic complet",
        "evidencia_textual": "### Evidència textual localitzable",
        "buits": "## Buits registrats",
        "consens_asr": "### Consens textual de dues passades ASR",
        "perfil_acustic": "### Perfil acústic dels consensos",
        "evidencia_gramatica": "### Evidència gramatical i de contacte textual",
    }
    for source in read_sources():
        pid = source["id_persona"]
        report_path = ROOT / "persones" / f"{pid}.md"
        text = report_path.read_text(encoding="utf-8")
        present = {name: marker in text for name, marker in checks.items()}
        present["transcripcio"] = all(
            f"../transcripcions/{pid}.{ext}" in text for ext in ("txt", "vtt", "json")
        )
        metric_line = text.split("Mesura directa del WAV:", 1)[1].split("\n", 1)[0] if "Mesura directa del WAV:" in text else ""
        present["metrics_audio"] = (
            ("Mesura directa del WAV:" in text and "**pendent**" not in metric_line)
            or "El WAV presenta" in text
        )
        present["cobertura_audicio"] = (
            ("### Comparació ASR de quarantena" in text and "auditoria-quarantena-20s.html" in text)
            if pid in quarantine
            else (("### Sessions operatives" in text or "### Cobertura auditiva canònica compartida" in text) and "clips/" in text)
        )
        gaps = [name for name, ok in present.items() if not ok]
        rows.append(
            {
                "id_persona": pid,
                "informe": str(report_path.relative_to(ROOT.parent)),
                **{name: "sí" if ok else "no" for name, ok in present.items()},
                "estat": "complet-provisional" if not gaps else "revisar",
                "buits": "; ".join(gaps),
            }
        )
    fields = list(rows[0])
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} informes · {OUT}")


if __name__ == "__main__":
    main()
