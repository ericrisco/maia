"""Agrupa les veus actives per mètriques acústiques i de ritme ASR.

És una exploració descriptiva per orientar la revisió, no una classificació
dialectal. Les estimacions de F0 provenen de l'espectre i poden contenir
harmònics, música o efectes d'edició.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).parents[1]
FEATURES = [
    "ratio_veu",
    "rms_db_median",
    "zcr_median",
    "f0_median_hz",
    "f0_p10_hz",
    "f0_p90_hz",
    "paraules_minut_span",
    "pausa_percent_span",
]


def main() -> None:
    with (ROOT / "proveniencia" / "analisi-prosodia.tsv").open(encoding="utf-8", newline="") as handle:
        prosody = {row["id_persona"]: row for row in csv.DictReader(handle, delimiter="\t")}
    with (ROOT / "proveniencia" / "analisi-metrics.tsv").open(encoding="utf-8", newline="") as handle:
        metrics = {row["id_persona"]: row for row in csv.DictReader(handle, delimiter="\t")}
    ids = sorted(pid for pid, row in prosody.items() if row["estat"] != "quarantena-asr")
    matrix = np.asarray(
        [[float(prosody[pid][name] if name in prosody[pid] else metrics[pid][name]) for name in FEATURES] for pid in ids],
        dtype=float,
    )
    scaled = StandardScaler().fit_transform(matrix)
    model = KMeans(n_clusters=4, random_state=42, n_init=20).fit(scaled)
    distances = model.transform(scaled)
    out = ROOT / "proveniencia" / "clusters-prosodia.tsv"
    rows = []
    for index, pid in enumerate(ids):
        rows.append(
            {
                "id_persona": pid,
                "cluster": f"prosodia-{model.labels_[index] + 1}",
                "distancia_centre": f"{distances[index, model.labels_[index]]:.3f}",
                **{name: f"{matrix[index, col]:.4f}" for col, name in enumerate(FEATURES)},
                "estat_cluster": "exploratori; revisió auditiva pendent",
            }
        )
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = ROOT / "proveniencia" / "resum-clusters-prosodia.md"
    with summary.open("w", encoding="utf-8") as handle:
        handle.write("# Agrupacions prosòdiques exploratòries\n\n")
        handle.write("Aquests grups descriuen similituds en mètriques del WAV i el ritme ASR. No són dialectes ni trets lingüístics.\n\n")
        handle.write("| clúster | veus | ràtio veu mediana | F0 mediana orientativa | ritme ASR median |\n|---|---:|---:|---:|---:|\n")
        for label in sorted({row["cluster"] for row in rows}):
            group = [row for row in rows if row["cluster"] == label]
            handle.write(
                f"| {label} | {len(group)} | {np.median([float(r['ratio_veu']) for r in group]):.3f} | "
                f"{np.median([float(r['f0_median_hz']) for r in group]):.1f} Hz | "
                f"{np.median([float(r['paraules_minut_span']) for r in group]):.1f} |\n"
            )
        handle.write("\nCal revisar els clips abans d'usar qualsevol diferència com a observació lingüística.\n")

    edges = ROOT / "grafo" / "arestes-clusters-prosodia.tsv"
    with edges.open("w", encoding="utf-8") as handle:
        handle.write("origen\tdesti\trelacio\tevidencia\n")
        for row in rows:
            handle.write(f"{row['id_persona']}\t{row['cluster']}\tsemblança acústica exploratòria\tWAV; revisió auditiva pendent\n")
    mermaid = ROOT / "grafo" / "graf-prosodia.mmd"
    with mermaid.open("w", encoding="utf-8") as handle:
        handle.write("flowchart LR\n")
        for cluster in sorted({row["cluster"] for row in rows}):
            handle.write(f"  {cluster.replace('-', '')}[\"{cluster}\"]\n")
        for row in rows:
            handle.write(f"  {row['id_persona'].replace('-', '')}[\"{row['id_persona']}\"] --> {row['cluster'].replace('-', '')}\n")
    print(f"{len(rows)} veus · 4 clústers exploratoris · {out}")


if __name__ == "__main__":
    main()
