"""Extreu formants dels tokens localitzats en la cua QA completa."""

from collections import defaultdict
from pathlib import Path
from statistics import median
import csv

import parselmouth

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Perfil formàntic de la cua QA"


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
    rows = [row for row in read("qa-formes-tokens.tsv") if row["coincidencia_token"] == "sí"]
    cache = {}
    measures = []
    by_person = defaultdict(list)
    by_form = defaultdict(list)
    for row in rows:
        path = str(PROV / row["clip"])
        if path not in cache:
            sound = parselmouth.Sound(path)
            cache[path] = (
                sound,
                sound.to_formant_burg(time_step=0.005, max_number_of_formants=5, maximum_formant=5500, window_length=0.025, pre_emphasis_from=50),
                sound.to_pitch(time_step=0.005, pitch_floor=60, pitch_ceiling=500),
            )
        sound, formant, pitch = cache[path]
        local_start = float(row["local_start_s"])
        local_end = float(row["local_end_s"])
        center = max(0.015, min(sound.duration - 0.015, (local_start + local_end) / 2))
        result = {
            "id_persona": row["id_persona"], "forma": row["forma"], "clip": row["clip"],
            "local_start_s": row["local_start_s"], "local_end_s": row["local_end_s"],
            "absolute_start_s": row["absolute_start_s"], "absolute_end_s": row["absolute_end_s"],
            "prob_min": row["prob_min"], "prob_mean": row["prob_mean"], "centre_rel_s": f"{center:.3f}",
        }
        try: result["f0_hz"] = fmt(pitch.get_value_at_time(center))
        except Exception: result["f0_hz"] = ""
        for number in (1, 2, 3):
            try: result[f"f{number}_hz"] = fmt(formant.get_value_at_time(number, center))
            except Exception: result[f"f{number}_hz"] = ""
        result["estat"] = "token QA; no és consens de dos models; pendent d'audició"
        measures.append(result); by_person[row["id_persona"]].append(result); by_form[row["forma"]].append(result)
    fields = ["id_persona", "forma", "clip", "local_start_s", "local_end_s", "absolute_start_s", "absolute_end_s", "prob_min", "prob_mean", "centre_rel_s", "f0_hz", "f1_hz", "f2_hz", "f3_hz", "estat"]
    with (PROV / "analisi-formants-qa.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(measures)
    summary = []
    for form, items in sorted(by_form.items()):
        def med(key: str) -> str:
            values = [float(item[key]) for item in items if item.get(key)]
            return f"{median(values):.2f}" if values else ""
        summary.append({"forma": form, "n_tokens": str(len(items)), "n_parlants": str(len({i['id_persona'] for i in items})), "f0_median_hz": med("f0_hz"), "f1_median_hz": med("f1_hz"), "f2_median_hz": med("f2_hz"), "f3_median_hz": med("f3_hz")})
    with (PROV / "resum-formants-qa.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]), delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(summary)
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = list(csv.DictReader(handle, delimiter="\t"))
    for person in people:
        pid = person["id_persona"]; items = by_person.get(pid, []); report = ROOT / "persones" / f"{pid}.md"; text = report.read_text(encoding="utf-8")
        if items:
            def med(key: str) -> str:
                values = [float(item[key]) for item in items if item.get(key)]
                return f"{median(values):.2f}" if values else "—"
            section = f"\n{MARKER}\n\nLa cua QA té **{len(items)} tokens localitzats** per a aquesta persona; les medianes instrumentals són F0 **{med('f0_hz')} Hz**, F1 **{med('f1_hz')} Hz**, F2 **{med('f2_hz')} Hz** i F3 **{med('f3_hz')} Hz**. Són candidats d'una passada QA i requereixen escolta.\n"
        else:
            section = f"\n{MARKER}\n\nNo hi ha tokens localitzats en aquesta cua QA.\n"
        report.write_text(replace_section(text, MARKER, section), encoding="utf-8")
    print(f"{len(measures)} tokens QA mesurats · {len(summary)} formes · {len(people)} informes")


if __name__ == "__main__":
    main()
