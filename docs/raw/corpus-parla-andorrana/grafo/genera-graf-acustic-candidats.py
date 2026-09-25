"""Genera el graf acústic provisional de los once candidatos separados."""
from __future__ import annotations

import csv
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).parents[1]
CANDIDATES = ROOT / "proveniencia" / "candidats"
OUT = ROOT / "grafo"
FEATURES = ["f0_hz", "f1_hz", "f2_hz", "f3_hz", "pausa_mediana_s", "veu_proporcio", "centroid_median_hz"]
SPEAKERS = {
    "lead-rtva-001": "Joan Verdú",
    "lead-rtva-002-ian-moya": "Ian Moya",
    "lead-rtva-003-dj-neura": "DJ Neura",
    "lead-rtva-004-joan-mico": "Joan Micó",
    "lead-cg-001-xavier-espot": "Xavier Espot",
    "lead-cg-002-pere-lopez": "Pere López",
    "lead-cg-003-roser-sune": "Roser Suñé",
    "lead-rtva-005-carine-montaner": "Carine Montaner",
    "lead-rtva-006-jaume-tomas": "Jaume Tomàs",
    "lead-rtva-007-robert-guirao": "Robert Guirao",
    "lead-rtva-008-mireia-pedescoll": "Mireia Pedescoll",
}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def number(row: dict[str, str], key: str) -> float | None:
    value = row.get(key, "")
    try:
        return float(value) if value not in {"", None} else None
    except (TypeError, ValueError):
        return None


def main() -> None:
    records: list[dict[str, object]] = []
    for folder, person in SPEAKERS.items():
        base = CANDIDATES / folder
        acoustic = {row["clip"]: row for row in read(base / "analisi-acustica.tsv")}
        formants_path = base / "formants.tsv"
        formants = {row["clip"]: row for row in read(formants_path)} if formants_path.exists() else {}
        for clip, row in sorted(acoustic.items()):
            formant = formants.get(clip, {})
            vector = {key: number(row, key) for key in FEATURES}
            for key in ("f0_hz", "f1_hz", "f2_hz", "f3_hz"):
                if number(formant, key) is not None:
                    vector[key] = number(formant, key)
            records.append({
                "id": f"{folder}::{row['forma']}",
                "folder": folder,
                "persona": person,
                "forma": row["forma"],
                "clip": clip,
                "vector": vector,
            })

    centers: dict[str, float] = {}
    scales: dict[str, float] = {}
    for key in FEATURES:
        values = [r["vector"][key] for r in records if r["vector"].get(key) is not None]
        centers[key] = sum(values) / len(values) if values else 0.0
        variance = sum((value - centers[key]) ** 2 for value in values) / len(values) if values else 1.0
        scales[key] = variance**0.5 or 1.0

    edges: list[dict[str, str]] = []
    for first, second in combinations(records, 2):
        shared = [key for key in FEATURES if first["vector"].get(key) is not None and second["vector"].get(key) is not None]
        if len(shared) < 4:
            continue
        distance = (
            sum(
                ((first["vector"][key] - centers[key]) / scales[key] - (second["vector"][key] - centers[key]) / scales[key]) ** 2
                for key in shared
            )
            / len(shared)
        ) ** 0.5
        if distance <= 1.35:
            edges.append({
                "id_a": first["id"],
                "id_b": second["id"],
                "n_dimensions": str(len(shared)),
                "distancia_z": f"{distance:.4f}",
                "dimensions": ",".join(shared),
                "estat": "semblança acústica exploratòria; pendent d’audició",
            })

    node_fields = ["id", "persona", "forma", "clip", *FEATURES, "estat"]
    with (OUT / "nodes-acustic-candidats.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(node_fields)
        for record in records:
            vector = record["vector"]
            writer.writerow([record["id"], record["persona"], record["forma"], record["clip"], *[vector.get(key) or "" for key in FEATURES], "mesura instrumental; pendent d’audició"])

    with (OUT / "arestes-acustic-candidats.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["id_a", "id_b", "n_dimensions", "distancia_z", "dimensions", "estat"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(edges)

    lines = ["graph TD"]
    for record in records:
        lines.append(f'  "{record["id"]}"["{record["persona"]} · {record["forma"]}"]')
    for edge in edges:
        lines.append(f'  "{edge["id_a"]}" -- "z={edge["distancia_z"]}" --> "{edge["id_b"]}"')
    (OUT / "graf-acustic-candidats.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")

    names = ", ".join(SPEAKERS.values())
    (OUT / "README-acustic-candidats.md").write_text(
        f"""# Graf acústic provisional dels candidats

Aquesta capa relaciona els **{len(records)} clips** mesurats dels onze candidats ({names}) amb una distància euclidiana sobre valors estandarditzats de F0, F1, F2, F3, pausa mediana, proporció de veu i centroid espectral. Hi ha **{len(edges)} arestes** amb almenys quatre dimensions disponibles i distància z ≤ 1,35.

Les arestes només indiquen semblança instrumental entre clips. No confirmen que parli la persona candidata, no són una classificació dialectal i no substitueixen l'audició.
""",
        encoding="utf-8",
    )
    print(f"{len(records)} nodes · {len(edges)} arestes · {len(SPEAKERS)} candidats")


if __name__ == "__main__":
    main()
