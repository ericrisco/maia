"""Afegeix a cada informe el resum de la doble passada ASR dels clips."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Consens textual de dues passades ASR"


def main() -> None:
    with (PROV / "qa-clips-consens.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_person[row["id_persona"]].append(row)
    people = []
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = list(csv.DictReader(handle, delimiter="\t"))

    summary_rows = []
    for person in people:
        pid = person["id_persona"]
        items = by_person.get(pid, [])
        yes = [row for row in items if row["consens_textual"] == "sí"]
        no = [row for row in items if row["consens_textual"] == "no"]
        yes_forms = sorted({row["forma"] for row in yes})
        no_forms = sorted({row["forma"] for row in no})
        summary_rows.append(
            {
                "id_persona": pid,
                "n_clips": str(len(items)),
                "n_consens": str(len(yes)),
                "n_divergents": str(len(no)),
                "formes_consens": ", ".join(yes_forms),
                "formes_divergents": ", ".join(no_forms),
                "estat_font": person["estat"],
            }
        )
        report = ROOT / "persones" / f"{pid}.md"
        text = report.read_text(encoding="utf-8")
        if MARKER in text:
            text = text[: text.index(MARKER)].rstrip() + "\n"
        if items:
            details = "; ".join(
                f"{row['forma']}={'consens' if row['consens_textual'] == 'sí' else 'divergent'}"
                for row in sorted(items, key=lambda r: (r["forma"], r["interval_escolta"]))
            )
            section = (
                f"\n{MARKER}\n\n"
                f"La doble passada independent (`ggml-small.bin` i `ggml-base.bin`) cobreix "
                f"**{len(items)} clips** d'aquesta veu: **{len(yes)}** tenen coincidència textual "
                f"en tots dos models i **{len(no)}** divergeixen. Les coincidències apareixen en "
                f"**{', '.join(yes_forms) if yes_forms else 'cap forma'}**; les divergències, en "
                f"**{', '.join(no_forms) if no_forms else 'cap forma'}**.\n\n"
                f"Detall per clip: {details}.\n\n"
                "Aquesta secció és evidència ASR localitzable a "
                "`../proveniencia/qa-clips-consens.tsv`; no confirma la realització fonètica "
                "ni substitueix l'escolta del WAV.\n"
            )
        else:
            section = (
                f"\n{MARKER}\n\n"
                "Aquesta veu està en quarantena i no entra en la cua de clips comparables; "
                "la seva verificació queda documentada a `../proveniencia/qa-quarantena.tsv`. "
                "No hi ha consens de les dues passades per interpretar-la.\n"
            )
        report.write_text(text.rstrip() + "\n" + section, encoding="utf-8")

    with (PROV / "resum-consens-per-persona.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["id_persona", "n_clips", "n_consens", "n_divergents", "formes_consens", "formes_divergents", "estat_font"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"{len(summary_rows)} informes actualitzats · {len(rows)} clips resumits")


if __name__ == "__main__":
    main()
