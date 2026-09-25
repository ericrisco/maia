"""Construeix la cua humana de les divergències dels clips forts."""

from collections import defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    disagreements = [row for row in read("qa-clips-forts-consens.tsv") if row["categoria"] != "A-tres-models"]
    master = {(row["id_persona"], row["forma"]): row for row in read("registre-audicio.tsv")}
    acoustic = {(row["id_persona"], row["forma"]): row for row in read("analisi-acustica-divergencies.tsv")}
    acoustic_fields = ["token_interval_absolute", "token_duration_s", "f0_token_hz", "f1_token_hz", "f2_token_hz", "f3_token_hz", "intensity_token_db", "f0_persona_median_hz", "delta_f0_clip_persona_hz", "centroid_clip_hz", "veu_clip", "pausa_clip_s"]
    fields = list(master[next(iter(master))]) + ["categoria_tres_models", "text_small", "text_base", "text_greedy", "prioritat_manual"] + acoustic_fields
    out_rows = []
    for index, row in enumerate(disagreements, start=1):
        key = (row["id_persona"], row["forma"])
        base = dict(master[key])
        base.update({
            "categoria_tres_models": row["categoria"],
            "text_small": row["text_small"],
            "text_base": row["text_base"],
            "text_greedy": row["text_greedy"],
            "prioritat_manual": str(index),
        })
        base.update({field: acoustic[key].get(field, "") for field in acoustic_fields})
        out_rows.append(base)
    with (PROV / "registre-audicio-forts-divergencies.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(out_rows)
    grouped = defaultdict(list)
    for row in out_rows:
        grouped[row["id_persona"]].append(row)
    lines = ["# Cua d'audició — divergències dels clips forts", "", f"Aquesta cua conté **{len(out_rows)} clips** on les tres decodificacions no coincideixen. Els camps humans es mantenen buits fins a escoltar el WAV.", ""]
    for pid in sorted(grouped):
        lines += [f"## {pid}", ""]
        for row in grouped[pid]:
            lines += [
                f"### {row['prioritat_manual']}. {row['forma']} · {row['categoria_tres_models']}",
                f"- **Àudio:** [{row['clip']}](<./{row['clip']}>)",
                f"- **Interval:** {row['interval_escolta']} · **Probabilitat token:** {row['token_prob_min']}",
                f"- **Small:** {row['text_small']}",
                f"- **Base:** {row['text_base']}",
                f"- **Greedy:** {row['text_greedy']}",
                f"- **Acústica:** token {row['token_interval_absolute']} · durada {row['token_duration_s']} s · F0 {row['f0_token_hz'] or '—'} Hz · F1/F2/F3 {row['f1_token_hz'] or '—'}/{row['f2_token_hz'] or '—'}/{row['f3_token_hz'] or '—'} Hz · intensitat {row['intensity_token_db'] or '—'} dB",
                "- **Decisió auditiva:**",
                "- **Variant escoltada:**",
                "- **Trets fonètics:**",
                "- **Prosòdia:**",
                "- **Nota:**",
                "",
            ]
    (PROV / "quadern-audicio-forts-divergencies.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(out_rows)} divergències · {len(grouped)} persones")


if __name__ == "__main__":
    main()
