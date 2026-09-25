"""Normalitza l'acústica dels consensos respecte a la veu completa de cada persona."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import median
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Perfil acústic normalitzat dels consensos"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def value(row: dict[str, str], key: str) -> float:
    return float(row[key])


def fmt(xs: list[float], digits: int = 2) -> str:
    return "—" if not xs else f"{median(xs):.{digits}f}"


def main() -> None:
    clips = read("analisi-acustica-consens.tsv")
    whole = {row["id_persona"]: row for row in read("analisi-prosodia.tsv")}
    dense = {row["id_persona"]: row for row in read("analisi-acustica-densa.tsv")}
    rows = []
    by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_form: dict[str, list[dict[str, str]]] = defaultdict(list)
    for clip in clips:
        person = whole[clip["id_persona"]]
        person_dense = dense[clip["id_persona"]]
        f0_iqr = value(person_dense, "f0_iqr_hz") or 1.0
        row = {
            "id_persona": clip["id_persona"], "forma": clip["forma"], "interval_escolta": clip["interval_escolta"], "clip": clip["clip"],
            "f0_clip_hz": clip["f0_median_hz"], "f0_persona_hz": person["f0_median_hz"], "delta_f0_hz": f"{value(clip, 'f0_median_hz') - value(person, 'f0_median_hz'):.2f}", "delta_f0_z_persona": f"{(value(clip, 'f0_median_hz') - value(person, 'f0_median_hz')) / f0_iqr:.3f}",
            "veu_clip": clip["veu_proporcio"], "veu_persona": person["ratio_veu"], "delta_veu": f"{value(clip, 'veu_proporcio') - value(person, 'ratio_veu'):.4f}",
            "centroid_clip_hz": clip["centroid_median_hz"], "centroid_persona_hz": person_dense["centroid_median_hz"], "delta_centroid_hz": f"{value(clip, 'centroid_median_hz') - value(person_dense, 'centroid_median_hz'):.2f}",
            "pausa_clip_s": clip["pausa_mediana_s"], "pausa_persona_s": person_dense["pausa_veu_mediana_s"], "delta_pausa_s": f"{value(clip, 'pausa_mediana_s') - value(person_dense, 'pausa_veu_mediana_s'):.3f}",
        }
        rows.append(row); by_person[row["id_persona"]].append(row); by_form[row["forma"]].append(row)
    fields = list(rows[0])
    with (PROV / "analisi-acustica-normalitzada-consens.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(rows)
    summary = []
    for form, items in sorted(by_form.items()):
        summary.append({
            "forma": form, "n_clips": str(len(items)), "n_parlants": str(len({row["id_persona"] for row in items})),
            "delta_f0_hz_median": fmt([float(row["delta_f0_hz"]) for row in items]), "delta_f0_z_median": fmt([float(row["delta_f0_z_persona"]) for row in items], 3),
            "delta_veu_median": fmt([float(row["delta_veu"]) for row in items], 4), "delta_centroid_hz_median": fmt([float(row["delta_centroid_hz"]) for row in items]), "delta_pausa_s_median": fmt([float(row["delta_pausa_s"]) for row in items], 3),
        })
    with (PROV / "resum-acustica-normalitzada-formes.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields_summary = list(summary[0]); writer = csv.DictWriter(handle, fieldnames=fields_summary, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(summary)
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle: people = list(csv.DictReader(handle, delimiter="\t"))
    for person in people:
        pid = person["id_persona"]; items = by_person.get(pid, []); report = ROOT / "persones" / f"{pid}.md"; text = report.read_text(encoding="utf-8")
        if MARKER in text: text = text[: text.index(MARKER)].rstrip() + "\n"
        if items:
            section = (f"\n{MARKER}\n\nEn els **{len(items)} clips** consensuals, respecte a la mediana de la veu completa, "
                       f"el delta de F0 és **{fmt([float(r['delta_f0_hz']) for r in items])} Hz**, el delta normalitzat de F0 **{fmt([float(r['delta_f0_z_persona']) for r in items], 3)}**, "
                       f"el delta de proporció de veu **{fmt([float(r['delta_veu']) for r in items], 4)}**, el delta de centroid **{fmt([float(r['delta_centroid_hz']) for r in items])} Hz** i el delta de pausa **{fmt([float(r['delta_pausa_s']) for r in items], 3)} s**.\n\n"
                       "Aquests deltes comparen el fragment amb la mateixa veu per reduir l'efecte de micròfon i parlant; són descriptors exploratoris i no trets dialectals. La taula és `../proveniencia/analisi-acustica-normalitzada-consens.tsv`.\n")
        else: section = f"\n{MARKER}\n\nNo hi ha consensos acústics normalitzables per a aquesta veu.\n"
        report.write_text(text.rstrip() + "\n" + section, encoding="utf-8")
    print(f"{len(rows)} clips normalitzats · {len(summary)} formes · {len(people)} informes")


if __name__ == "__main__":
    main()
