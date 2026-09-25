"""Mesura formants en totes les ocurrències tokenitzades de la cua small."""

from collections import defaultdict
from pathlib import Path
from statistics import median
import csv

import parselmouth

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Perfil formàntic de la cua completa small"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def fmt(value: float | None) -> str:
    return f"{value:.2f}" if value is not None and value == value else ""


def replace_section(text: str, marker: str, section: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + section
    start = text.index(marker)
    next_heading = text.find("\n### ", start + len(marker))
    end = len(text) if next_heading == -1 else next_heading + 1
    return text[:start].rstrip() + "\n" + section.rstrip() + "\n\n" + text[end:].lstrip()


def main() -> None:
    rows = read("qa-cua-small-token-occurrences.tsv")
    cache = {}
    measures = []
    by_person = defaultdict(list)
    by_form = defaultdict(list)
    for row in rows:
        path = str(PROV / row["clip"])
        if path not in cache:
            sound = parselmouth.Sound(path)
            cache[path] = (sound, sound.to_formant_burg(time_step=0.005, max_number_of_formants=5, maximum_formant=5500, window_length=0.025, pre_emphasis_from=50), sound.to_pitch(time_step=0.005, pitch_floor=60, pitch_ceiling=500))
        sound, formant, pitch = cache[path]
        center = max(0.015, min(sound.duration - 0.015, (float(row["local_start_s"]) + float(row["local_end_s"])) / 2))
        result = dict(row)
        result["centre_rel_s"] = f"{center:.3f}"
        try: result["f0_hz"] = fmt(pitch.get_value_at_time(center))
        except Exception: result["f0_hz"] = ""
        for n in (1, 2, 3):
            try: result[f"f{n}_hz"] = fmt(formant.get_value_at_time(n, center))
            except Exception: result[f"f{n}_hz"] = ""
        result["estat"] = "tokenització small; no és consens de dos models; pendent d'audició"
        measures.append(result); by_person[row["id_persona"]].append(result); by_form[row["forma"]].append(result)
    fields = ["id_persona", "forma", "clip", "occurrence", "local_start_s", "local_end_s", "absolute_start_s", "absolute_end_s", "prob_min", "text", "centre_rel_s", "f0_hz", "f1_hz", "f2_hz", "f3_hz", "estat"]
    with (PROV / "analisi-formants-cua-small.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(measures)
    summary = []
    for form, items in sorted(by_form.items()):
        def med(key: str) -> str:
            values = [float(item[key]) for item in items if item.get(key)]
            return f"{median(values):.2f}" if values else ""
        summary.append({"forma": form, "n_occurrences": str(len(items)), "n_parlants": str(len({i['id_persona'] for i in items})), "f0_median_hz": med("f0_hz"), "f1_median_hz": med("f1_hz"), "f2_median_hz": med("f2_hz"), "f3_median_hz": med("f3_hz")})
    with (PROV / "resum-formants-cua-small.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]), delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(summary)
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = list(csv.DictReader(handle, delimiter="\t"))
    for person in people:
        pid = person["id_persona"]; items = by_person.get(pid, []); report = ROOT / "persones" / f"{pid}.md"; text = report.read_text(encoding="utf-8")
        if items:
            def med(key: str) -> str:
                values = [float(item[key]) for item in items if item.get(key)]
                return f"{median(values):.2f}" if values else "—"
            section = f"\n{MARKER}\n\nLa cua small localitza **{len(items)} ocurrències** per a aquesta persona; les medianes són F0 **{med('f0_hz')} Hz**, F1 **{med('f1_hz')} Hz**, F2 **{med('f2_hz')} Hz** i F3 **{med('f3_hz')} Hz**. És una capa de tokenització automàtica sense consens de models i requereix escolta.\n"
        else:
            section = f"\n{MARKER}\n\nNo hi ha ocurrències tokenitzades per aquesta persona en la cua small.\n"
        report.write_text(replace_section(text, MARKER, section), encoding="utf-8")
    print(f"{len(measures)} ocurrències mesurades · {len(summary)} formes · {len(people)} informes")


if __name__ == "__main__":
    main()
