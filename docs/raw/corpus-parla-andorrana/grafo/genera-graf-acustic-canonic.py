"""Genera un graf acústic agregat per persona per al corpus canònic."""
from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = ROOT / "grafo"
FEATURES = ("f0_hz", "f1_hz", "f2_hz", "f3_hz", "pausa_mediana_s", "veu_proporcio")


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def number(row: dict[str, str], field: str) -> float | None:
    try:
        value = float(row[field])
    except (KeyError, TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def main() -> None:
    canonical_rows = read(PROV / "persones-canonics.tsv")
    canonical = {row["id_persona"]: row["id_parlant"] for row in canonical_rows}
    labels = {}
    for row in canonical_rows:
        labels.setdefault(row["id_parlant"], row["nom_public"])
    acoustics = read(PROV / "analisi-acustica-clips.tsv")
    formants = read(PROV / "analisi-formants-cua-small.tsv")
    people = sorted(set(canonical.values()))
    values: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    clip_counts = Counter(canonical.get(row["id_persona"], row["id_persona"]) for row in acoustics)
    formant_counts = Counter(canonical.get(row["id_persona"], row["id_persona"]) for row in formants)
    for row in acoustics:
        person = canonical.get(row["id_persona"], row["id_persona"])
        for field in ("f0_median_hz", "pausa_mediana_s", "veu_proporcio"):
            value = number(row, field)
            if value is not None:
                values[person][field].append(value)
    for row in formants:
        person = canonical.get(row["id_persona"], row["id_persona"])
        for source, target in (("f0_hz", "f0_hz"), ("f1_hz", "f1_hz"), ("f2_hz", "f2_hz"), ("f3_hz", "f3_hz")):
            value = number(row, source)
            if value is not None:
                values[person][target].append(value)
    nodes = []
    for person in people:
        node = {"id": person, "persona": labels.get(person, person), "n_clips": str(clip_counts[person]), "n_formant_tokens": str(formant_counts[person])}
        for field in FEATURES:
            vals = values[person].get(field, [])
            node[field] = f"{median(vals):.4f}" if vals else ""
        nodes.append(node)
    vectors = {node["id"]: {field: float(node[field]) for field in FEATURES if node[field]} for node in nodes}
    centres = {}
    scales = {}
    for field in FEATURES:
        xs = [vector[field] for vector in vectors.values() if field in vector]
        centres[field] = sum(xs) / len(xs) if xs else 0.0
        sd = (sum((x - centres[field]) ** 2 for x in xs) / len(xs)) ** 0.5 if xs else 1.0
        scales[field] = sd or 1.0
    matrix = read(ROOT / "grafo" / "matriu-formes.tsv")
    shared: dict[tuple[str, str], int] = Counter()
    by_form: dict[str, list[str]] = defaultdict(list)
    for row in matrix:
        if int(row["recompte_asr"] or 0) > 0:
            by_form[row["forma"]].append(canonical.get(row["id_persona"], row["id_persona"]))
    for ids in by_form.values():
        for i, a in enumerate(sorted(set(ids))):
            for b in sorted(set(ids))[i + 1:]:
                shared[(a, b)] += 1
    edges = []
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            pairs = [field for field in FEATURES if field in vectors[a["id"]] and field in vectors[b["id"]]]
            if len(pairs) < 4:
                continue
            distance = (
                sum(((vectors[a["id"]][field] - centres[field]) / scales[field] - (vectors[b["id"]][field] - centres[field]) / scales[field]) ** 2 for field in pairs) / len(pairs)
            ) ** 0.5
            if distance <= 1.35:
                key = (a["id"], b["id"])
                edges.append({"id_a": a["id"], "id_b": b["id"], "n_dimensions": str(len(pairs)), "distancia_z": f"{distance:.4f}", "dimensions": ",".join(pairs), "formes_compartides_asr": str(shared.get(key, 0)), "estat": "semblança acústica exploratòria; pendent d'audició"})
    node_fields = ["id", "persona", "n_clips", "n_formant_tokens", *FEATURES, "estat"]
    with (OUT / "nodes-acustic-canonic.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=node_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for node in nodes:
            writer.writerow({**node, "estat": "mesura agregada; pendent d'audició"})
    edge_fields = ["id_a", "id_b", "n_dimensions", "distancia_z", "dimensions", "formes_compartides_asr", "estat"]
    with (OUT / "arestes-acustic-canonic.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=edge_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(edges)
    lines = ["graph TD"]
    for node in nodes:
        lines.append(f'  "{node["id"]}"["{node["persona"]}"]')
    for edge in edges:
        lines.append(f'  "{edge["id_a"]}" -- "z={edge["distancia_z"]}" --> "{edge["id_b"]}"')
    (OUT / "graf-acustic-canonic.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "README-acustic-canonic.md").write_text(
        f"""# Graf acústic agregat del corpus canònic

Aquesta capa resumeix els **{len(nodes)} parlants canònics** a partir de {len(acoustics)} clips acústics i {len(formants)} tokens amb formants. Hi ha {sum(bool(v) for v in vectors.values())} nodes amb mesures i la resta conserva el node sense inventar valors. Cada node mesurat conserva medianes de F0, F1, F2, F3, pausa i proporció de veu. Les **{len(edges)} arestes** tenen almenys quatre dimensions disponibles i distància euclidiana z ≤ 1,35.

La columna `formes_compartides_asr` només indica coincidències textuals potencials. La distància és una semblança instrumental agregada, no una atribució dialectal ni una prova de veu compartida. Cal escolta abans d'interpretar cap relació.
""",
        encoding="utf-8",
    )
    print(f"{len(nodes)} nodes · {len(edges)} arestes")


if __name__ == "__main__":
    main()
