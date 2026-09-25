"""Mesura trajectòries instrumentals en cinc punts dels tokens consensuals."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import median
import csv
import json

import parselmouth

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Trajectòries instrumentals de formants"
POINTS = (0.2, 0.35, 0.5, 0.65, 0.8)


def replace_section(text: str, marker: str, section: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + section
    start = text.index(marker)
    next_heading = text.find("\n### ", start + len(marker))
    end = len(text) if next_heading == -1 else next_heading + 1
    return text[:start].rstrip() + "\n" + section.rstrip() + "\n\n" + text[end:].lstrip()


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def finite(value: float | None) -> str:
    return f"{value:.2f}" if value is not None and value == value else ""


def measure(sound: parselmouth.Sound, formant: parselmouth.Formant, pitch: parselmouth.Pitch, intensity: parselmouth.Intensity, time: float) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        f0 = pitch.get_value_at_time(time)
    except Exception:
        f0 = None
    values["f0_hz"] = finite(f0)
    for number in (1, 2, 3):
        try:
            value = formant.get_value_at_time(number, time)
        except Exception:
            value = None
        values[f"f{number}_hz"] = finite(value)
    try:
        value = intensity.get_value(time)
    except Exception:
        value = None
    values["intensity_db"] = finite(value)
    return values


def main() -> None:
    rows = read("qa-consens-tokens-base.tsv")
    cache: dict[str, tuple[parselmouth.Sound, parselmouth.Formant, parselmouth.Pitch, parselmouth.Intensity]] = {}
    output: list[dict[str, str]] = []
    by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_form: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        clip_path = str(PROV / row["clip"])
        if clip_path not in cache:
            sound = parselmouth.Sound(clip_path)
            cache[clip_path] = (
                sound,
                sound.to_formant_burg(time_step=0.005, max_number_of_formants=5, maximum_formant=5500, window_length=0.025, pre_emphasis_from=50),
                sound.to_pitch(time_step=0.005, pitch_floor=60, pitch_ceiling=500),
                sound.to_intensity(minimum_pitch=60),
            )
        sound, formant, pitch, intensity = cache[clip_path]
        clip_start = float(row["interval_escolta"].split("-")[0])
        for match in json.loads(row["token_matches"]):
            absolute_start = float(match["start"])
            absolute_end = float(match["end"])
            relative_start = max(0.015, min(sound.duration - 0.015, absolute_start - clip_start))
            relative_end = max(relative_start + 0.01, min(sound.duration - 0.015, absolute_end - clip_start))
            duration = max(0.01, relative_end - relative_start)
            for point, fraction in enumerate(POINTS, start=1):
                time = relative_start + duration * fraction
                result = measure(sound, formant, pitch, intensity, time)
                result.update({
                    "id_persona": row["id_persona"],
                    "forma": row["forma"],
                    "interval_escolta": row["interval_escolta"],
                    "clip": row["clip"],
                    "token_start_abs": f"{absolute_start:.3f}",
                    "token_end_abs": f"{absolute_end:.3f}",
                    "token_p_min": f"{float(match['p_min']):.4f}",
                    "punt": str(point),
                    "proporcio": f"{fraction:.2f}",
                    "temps_rel_s": f"{time:.3f}",
                })
                output.append(result)
                by_person[row["id_persona"]].append(result)
                by_form[row["forma"]].append(result)
    fields = ["id_persona", "forma", "interval_escolta", "clip", "token_start_abs", "token_end_abs", "token_p_min", "punt", "proporcio", "temps_rel_s", "f0_hz", "f1_hz", "f2_hz", "f3_hz", "intensity_db"]
    with (PROV / "analisi-trajectories-formants.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    summary_fields = ["forma", "n_points", "n_tokens", "n_parlants", "f0_start_median_hz", "f0_end_median_hz", "f1_start_median_hz", "f1_end_median_hz", "f2_start_median_hz", "f2_end_median_hz", "f3_start_median_hz", "f3_end_median_hz", "intensity_start_median_db", "intensity_end_median_db"]
    summary = []
    for form, items in sorted(by_form.items()):
        def nums(key: str, point: str) -> list[float]:
            return [float(item[key]) for item in items if item["punt"] == point and item.get(key)]
        def med(key: str, point: str) -> str:
            values = nums(key, point)
            return f"{median(values):.2f}" if values else ""
        summary.append({
            "forma": form,
            "n_points": str(len(items)),
            "n_tokens": str(len(items) // len(POINTS)),
            "n_parlants": str(len({item['id_persona'] for item in items})),
            "f0_start_median_hz": med("f0_hz", "1"), "f0_end_median_hz": med("f0_hz", "5"),
            "f1_start_median_hz": med("f1_hz", "1"), "f1_end_median_hz": med("f1_hz", "5"),
            "f2_start_median_hz": med("f2_hz", "1"), "f2_end_median_hz": med("f2_hz", "5"),
            "f3_start_median_hz": med("f3_hz", "1"), "f3_end_median_hz": med("f3_hz", "5"),
            "intensity_start_median_db": med("intensity_db", "1"), "intensity_end_median_db": med("intensity_db", "5"),
        })
    with (PROV / "resum-trajectories-formants.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary)
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = list(csv.DictReader(handle, delimiter="\t"))
    for person in people:
        pid = person["id_persona"]
        items = by_person.get(pid, [])
        report = ROOT / "persones" / f"{pid}.md"
        text = report.read_text(encoding="utf-8")
        if items:
            def person_med(key: str, point: str) -> str:
                values = [float(item[key]) for item in items if item["punt"] == point and item.get(key)]
                return f"{median(values):.2f}" if values else "—"
            section = (f"\n{MARKER}\n\nEn **{len(items) // len(POINTS)} tokens** consensuals, les medianes instrumentals entre el primer i l'últim punt són F0 **{person_med('f0_hz', '1')} → {person_med('f0_hz', '5')} Hz**, F1 **{person_med('f1_hz', '1')} → {person_med('f1_hz', '5')} Hz**, F2 **{person_med('f2_hz', '1')} → {person_med('f2_hz', '5')} Hz** i F3 **{person_med('f3_hz', '1')} → {person_med('f3_hz', '5')} Hz**.\n\n"
                       "La trajectòria és una descripció instrumental sensible a la coarticulació, la durada, el micròfon i la segmentació; no és una decisió auditiva ni una confirmació dialectal. La taula completa és `../proveniencia/analisi-trajectories-formants.tsv`.\n")
        else:
            section = f"\n{MARKER}\n\nNo hi ha tokens consensuals amb timestamp per mesurar trajectòries.\n"
        report.write_text(replace_section(text, MARKER, section), encoding="utf-8")
    print(f"{len(output)} punts · {len(output) // len(POINTS)} tokens · {len(summary)} formes · {len(people)} informes")


if __name__ == "__main__":
    main()
