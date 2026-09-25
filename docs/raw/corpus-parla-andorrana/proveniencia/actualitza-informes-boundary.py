"""Afegeix el recompte de coincidències amb límit de paraula als informes."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Coincidències amb límit de paraula"


def main() -> None:
    with (PROV / "qa-clips-boundary.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_person[row["id_persona"]].append(row)
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = list(csv.DictReader(handle, delimiter="\t"))
    summary = []
    for person in people:
        pid = person["id_persona"]
        items = by_person.get(pid, [])
        strict = [row for row in items if row["consens_limit_paraula"] == "sí"]
        old = [row for row in items if row["small_subcadena"] == "sí" and row["base_subcadena"] == "sí"]
        false = [row for row in old if row["consens_limit_paraula"] == "no"]
        forms = sorted({row["forma"] for row in strict})
        summary.append({"id_persona": pid, "n_clips": str(len(items)), "n_consens_limit": str(len(strict)), "n_falsos_subcadena": str(len(false)), "formes_consens_limit": ", ".join(forms)})
        report = ROOT / "persones" / f"{pid}.md"
        text = report.read_text(encoding="utf-8")
        if MARKER in text:
            text = text[: text.index(MARKER)].rstrip() + "\n"
        if items:
            section = (
                f"\n{MARKER}\n\n"
                f"Amb límits de paraula estrictes, aquesta veu conserva **{len(strict)}** clips de consens "
                f"i **{len(false)}** coincidències que només eren subcadenes. Les formes estrictes són "
                f"**{', '.join(forms) if forms else 'cap'}**.\n\n"
                "El recompte evita confondre `bé` dins `ben` o altres fragments parcials amb una ocurrència "
                "completa. Continua sent una comprovació textual i requereix escolta. La taula és "
                "`../proveniencia/qa-clips-boundary.tsv`.\n"
            )
        else:
            section = f"\n{MARKER}\n\nAquesta veu no té clips comparables en la cua estricta.\n"
        report.write_text(text.rstrip() + "\n" + section, encoding="utf-8")
    with (PROV / "resum-boundary-per-persona.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["id_persona", "n_clips", "n_consens_limit", "n_falsos_subcadena", "formes_consens_limit"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(summary)
    print(f"{len(people)} informes actualitzats · {len(rows)} clips comparats")


if __name__ == "__main__":
    main()
