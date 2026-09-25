"""Genera un resum Markdown de la cobertura documental per font."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-cobertura-persones.md"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    rows = read(PROV / "auditoria-cobertura-persones.tsv")
    people = {row["id_persona"]: row for row in read(ROOT / "persones.tsv")}
    canonical = {row["id_persona"]: row["id_parlant"] for row in read(PROV / "persones-canonics.tsv")}
    complete = sum(all(row.get(field) == "sí" for field in ("fitxa", "titol", "inventari_35_formes", "perfil_linguistic", "audio_wav", "transcripcio_txt", "procedencia")) for row in rows)
    lines = [
        "# Auditoria de cobertura per persona",
        "",
        f"Aquesta vista resumeix les **{len(rows)} fitxes de font** i comprova la presència d'informe, títol, inventari de 35 formes, perfil lingüístic, àudio, transcripció i procedència. **{complete}/{len(rows)}** tenen tots aquests artefactes documentals. La cua auditiva continua pendent i no es considera una prova dialectal.",
        "",
        "| font | persona canònica | estat | evidència textual | clips | fitxa | formes | àudio | transcripció | procedència |",
        "|---|---|---|---:|---:|---|---|---|---|---|",
    ]
    for row in rows:
        person = people.get(row["id_persona"], {})
        report_link = f"[informe](../persones/{row['id_persona']}.md)"
        lines.append(
            f"| `{row['id_persona']}` | `{canonical.get(row['id_persona'], '—')}` · {person.get('nom_public', '—')} | {row['estat']} | {row['evidencia_textual']} | {row['clips_audicio']} | {report_link} | {row['inventari_35_formes']} | {row['audio_wav']} | {row['transcripcio_txt']} | {row['procedencia']} |"
        )
    lines.extend([
        "",
        "Els camps humans de `registre-audicio.tsv` es conserven separats: aquesta auditoria demostra cobertura documental, no confirmació de veu, variant, fonètica ni prosòdia.",
    ])
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} fitxes · completes={complete} · {OUT}")


if __name__ == "__main__":
    main()
