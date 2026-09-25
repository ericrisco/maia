"""Genera la vista provisional de DJ Neura contra el graf canònic complet."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
CAND = PROV / "candidats" / "lead-rtva-003-dj-neura"
OUT = CAND / "graf"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    candidate_forms = {
        row["forma"]
        for row in read(CAND / "formes-consens.tsv")
        if row["consens"] == "sí"
    }
    canonical = read(ROOT / "grafo" / "nodes-formes-completa.tsv")
    edges = []
    for node in canonical:
        shared = sorted(candidate_forms & set(filter(None, node["formes"].split(","))))
        if len(shared) >= 2:
            edges.append({
                "id_a": "lead-rtva-003-dj-neura",
                "id_b": node["id_parlant"],
                "n_formes_compartides": len(shared),
                "formes": ",".join(shared),
                "estat": "candidat RTVA; consens ASR textual; pendent d'audició",
            })

    OUT.mkdir(exist_ok=True)
    with (OUT / "nodes.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["id_parlant", "nom_public", "n_formes", "formes", "estat"])
        writer.writerow(["lead-rtva-003-dj-neura", "DJ Neura", len(candidate_forms), ",".join(sorted(candidate_forms)), "candidat separat; pendent de veu i audició"])
        for node in canonical:
            writer.writerow([node["id_parlant"], node["nom_public"], node["n_formes"], node["formes"], "persona canònica; graf ASR complet"])
    with (OUT / "arestes.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["id_a", "id_b", "n_formes_compartides", "formes", "estat"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(edges)
    with (OUT / "trets.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["forma", "font", "estat"])
        writer.writerows([[form, "DJ Neura + graf canònic complet", "consensual ASR; pendent d'audició"] for form in sorted(candidate_forms)])
    names = {node["id_parlant"]: node["nom_public"].replace('"', '\\"') for node in canonical}
    lines = ['graph TD', '  C["DJ Neura — candidat"]']
    for edge in sorted(edges, key=lambda row: (-row["n_formes_compartides"], row["id_b"])):
        node_id = edge["id_b"]
        lines.append(f'  {node_id}["{names[node_id]}"]')
        lines.append(f'  C -- "{edge["n_formes_compartides"]} formes" --> {node_id}')
    (OUT / "graf.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        f"""# Graf provisional — DJ Neura

Aquesta vista manté el candidat RTVA separat del graf canònic. Usa **{len(candidate_forms)} formes** presents en small i base i connecta DJ Neura amb **{len(edges)} persones** que en comparteixen almenys dues segons la matriu ASR completa.

Les arestes són semblances textuals; no indiquen dialecte, identitat lingüística ni veu confirmada. DJ Neura no entra encara al recompte canònic.
""", encoding="utf-8")
    print(f"{len(candidate_forms)} formes · {len(edges)} arestes · {len(canonical)+1} nodes")


if __name__ == "__main__":
    main()
