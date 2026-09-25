"""Genera un grafo textual independiente para los candidatos fuera del canon."""
from __future__ import annotations
import csv
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).parents[1]
CAND_ROOT = ROOT / "proveniencia" / "candidats"
OUT = ROOT / "grafo"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    candidates: dict[str, dict[str, dict[str, str]]] = {}
    for folder in sorted(p for p in CAND_ROOT.iterdir() if p.is_dir() and p.name.startswith("lead-")):
        rows = read(folder / "formes-consens.tsv")
        candidates[folder.name] = {
            row["forma"]: row for row in rows if row.get("consens") == "sí"
        }
    node_rows: list[dict[str, str]] = []
    for candidate, forms in candidates.items():
        for form, row in sorted(forms.items()):
            node_rows.append({
                "id": f"{candidate}::{form}",
                "candidat": candidate,
                "categoria": row.get("categoria", ""),
                "forma": form,
                "small": row.get("small", "0"),
                "base": row.get("base", "0"),
                "estat": "consens textual; pendent d'audició",
            })
    edge_rows: list[dict[str, str]] = []
    for a, b in combinations(sorted(candidates), 2):
        shared = sorted(set(candidates[a]) & set(candidates[b]))
        if shared:
            edge_rows.append({
                "candidat_a": a,
                "candidat_b": b,
                "n_formes_compartides": str(len(shared)),
                "formes": ";".join(shared),
                "estat": "semblança textual exploratòria; pendent d'audició",
            })
    node_path = OUT / "nodes-formes-candidats.tsv"
    edge_path = OUT / "arestes-formes-candidats.tsv"
    with node_path.open("w", encoding="utf-8", newline="") as handle:
        fields = list(node_rows[0]) if node_rows else ["id"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(node_rows)
    with edge_path.open("w", encoding="utf-8", newline="") as handle:
        fields = list(edge_rows[0]) if edge_rows else ["candidat_a", "candidat_b", "n_formes_compartides", "formes", "estat"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(edge_rows)
    lines = ["graph TD"]
    for candidate, forms in sorted(candidates.items()):
        lines.append(f'  "{candidate}"["{candidate} · {len(forms)} formes consensuals"]')
    for edge in edge_rows:
        lines.append(f'  "{edge["candidat_a"]}" -- "{edge["n_formes_compartides"]} formes" --> "{edge["candidat_b"]}"')
    (OUT / "graf-formes-candidats.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    nonempty = sum(bool(forms) for forms in candidates.values())
    common_forms = sorted({form for forms in candidates.values() for form in forms})
    (OUT / "README-formes-candidats.md").write_text(
        f"""# Graf de formes dels candidats fora del cànon

Aquesta capa independent relaciona **{len(candidates)} candidats**; {nonempty} tenen almenys una forma amb coincidència textual entre `small` i `base`. Conté **{len(node_rows)} nodes forma-candidat**, **{len(edge_rows)} arestes entre candidats** i **{len(common_forms)} formes** observades almenys una vegada.

Les arestes només indiquen coincidència ortogràfica entre dues passades ASR. No confirmen que parli la persona candidata, no són una classificació dialectal i no enllacen amb `nodes-formes-completa.tsv` ni cap altre graf canònic. La veu, la variant i els termes d'ús continuen pendents.
""", encoding="utf-8")
    print(f"{len(candidates)} candidats · {len(node_rows)} nodes · {len(edge_rows)} arestes · {len(common_forms)} formes")


if __name__ == "__main__":
    main()
