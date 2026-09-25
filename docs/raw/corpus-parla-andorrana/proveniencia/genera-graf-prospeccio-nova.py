"""Genera el graf de formes dels expedients descoberts després dels candidats."""
from __future__ import annotations

import csv
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROSPECCIO = ROOT / "proveniencia" / "prospeccio"
OUT = ROOT / "grafo"
LEADS = [
    "lead-rtva-009-isidre-bartumeu",
    "lead-rtva-010-lurdes-riba",
    "lead-rtva-011-josep-dalleres",
    "lead-rtva-012-marc-forne",
    "lead-rtva-013-pere-vilanova",
    "lead-rtva-014-joan-burgues",
    "lead-rtva-015-isidre-baro",
    "lead-rtva-016-josep-areny",
    "lead-rtva-017-simo-duro",
    "lead-rtva-018-ricard-fiter",
    "lead-rtva-019-lisa-cruz",
    "lead-rtva-020-monica-bonell",
    "lead-rtva-021-bonaventura-riberaygua",
    "lead-rtva-022-josep-marsal",
    "lead-rtva-023-josep-maria-cases",
    "lead-rtva-024-denisa-font",
    "lead-rtva-025-albert-gelabert",
    "lead-rtva-026-rosa-maria-mandico",
    "lead-rtva-027-jordi-guillamet",
    "lead-rtva-028-pere-besoli",
    "lead-rtva-029-angelina-mas",
    "lead-rtva-030-casimir-arajol",
    "lead-rtva-031-ramon-rossell",
    "lead-rtva-032-anna-riberaygua",
    "lead-yt-033-david-montane",
    "lead-yt-034-antoni-marti",
    "lead-yt-035-cerni-escale",
    "lead-yt-036-xavier-espot",
    "lead-yt-037-oscar-ribas",
    "lead-yt-038-conxita-marsol",
    "lead-yt-039-marta-roure",
    "lead-yt-040-guillem-forne",
    "lead-yt-041-guillem-areny",
    "lead-yt-042-andreu-gonzalez",
    "lead-yt-043-oriol-agorreta",
    "lead-yt-044-laura-casanovas",
    "lead-yt-045-arnau-rius",
    "lead-yt-046-alberto-villagrasa",
    "lead-yt-047-katia-ustina",
    "lead-yt-048-ander-mirambell",
    "lead-yt-049-joan-piquet",
    "lead-yt-050-pau-chica",
    "lead-yt-051-albert-vilaro",
    "lead-yt-052-valenti-closa",
    "lead-yt-053-sonia-andorrita",
    "lead-yt-054-francesc-solana",
    "lead-yt-055-enric-flix",
    "lead-yt-056-arnau-fortuny",
    "lead-yt-057-gabriel-lezkano",
    "lead-yt-058-nuria-pablos",
    "lead-rtva-059-carles-ensenyat",
    "lead-rtva-060-xavier-espot-actual",
    "lead-rtva-061-antoni-morell",
]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    candidates: dict[str, dict[str, dict[str, str]]] = {}
    for lead in LEADS:
        path = PROSPECCIO / lead / "formes.tsv"
        rows = read(path)
        candidates[lead] = {
            row["forma"]: row
            for row in rows
            if row.get("consens") == "sí"
        }

    nodes: list[dict[str, str]] = []
    for candidate, forms in candidates.items():
        for form, row in sorted(forms.items()):
            nodes.append({
                "id": f"{candidate}::{form}",
                "candidat": candidate,
                "forma": form,
                "categoria": row.get("categoria", ""),
                "small": row.get("small", "0"),
                "base": row.get("base", "0"),
                "clip": row.get("clip", ""),
                "estat": "consens textual; pendent d'audició",
            })

    edges: list[dict[str, str]] = []
    for left, right in combinations(sorted(candidates), 2):
        shared = sorted(set(candidates[left]) & set(candidates[right]))
        if shared:
            edges.append({
                "candidat_a": left,
                "candidat_b": right,
                "n_formes_compartides": str(len(shared)),
                "formes": ";".join(shared),
                "estat": "semblança textual exploratòria; pendent d'audició",
            })

    forms = sorted({form for values in candidates.values() for form in values})
    matrix = []
    for candidate in sorted(candidates):
        for form in forms:
            row = candidates[candidate].get(form)
            matrix.append({
                "candidat": candidate,
                "forma": form,
                "present": "sí" if row else "no",
                "small": row.get("small", "0") if row else "0",
                "base": row.get("base", "0") if row else "0",
                "estat": "ASR consensual; pendent d'audició",
            })

    write(OUT / "nodes-formes-prospeccio.tsv", nodes, list(nodes[0]))
    write(OUT / "arestes-formes-prospeccio.tsv", edges, list(edges[0]) if edges else ["candidat_a", "candidat_b", "n_formes_compartides", "formes", "estat"])
    write(OUT / "matriu-formes-prospeccio.tsv", matrix, list(matrix[0]))
    lines = ["graph TD"]
    for candidate, forms_for_candidate in sorted(candidates.items()):
        lines.append(f'  "{candidate}"["{candidate} · {len(forms_for_candidate)} formes consensuals"]')
    for edge in edges:
        lines.append(f'  "{edge["candidat_a"]}" -- "{edge["n_formes_compartides"]} formes" --> "{edge["candidat_b"]}"')
    (OUT / "graf-formes-prospeccio.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "README-formes-prospeccio.md").write_text(
        f"""# Graf de formes de la prospecció nova

Aquesta capa relaciona **{len(candidates)} expedients** descoberts després del paquet inicial de candidats. Conté **{len(nodes)} nodes**, **{len(edges)} arestes**, **{len(forms)} formes** i **{len(matrix)} cel·les** de la matriu.

Les arestes només indiquen coincidència ortogràfica entre les dues passades ASR locals (`small` i `base`). No confirmen que la forma pertanyi a la persona, no són una classificació dialectal i no enllacen amb `nodes-formes-completa.tsv`, `nodes-formes-candidats.tsv` ni cap graf canònic. La veu, la variant i els termes d'ús continuen pendents d'audició.
""", encoding="utf-8")
    print(f"OK graf prospecció nova: {len(candidates)} expedients · {len(nodes)} nodes · {len(edges)} arestes · {len(forms)} formes")


if __name__ == "__main__":
    main()
