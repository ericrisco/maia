"""Extreu formants i F0 en el centre dels tokens consensuals localitzats."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import median
import csv
import json

import parselmouth

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Mesures instrumentals de formants"


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


def one_measure(row: dict[str, str], match: dict[str, object], sound_cache: dict[str, parselmouth.Sound]) -> dict[str, str]:
    clip_path = str(PROV / row["clip"])
    sound = sound_cache.setdefault(clip_path, parselmouth.Sound(clip_path))
    clip_start = float(row["interval_escolta"].split("-")[0])
    start_abs = float(match["start"])
    end_abs = float(match["end"])
    mid = max(0.01, min(sound.duration - 0.01, ((start_abs + end_abs) / 2) - clip_start))
    formant = sound.to_formant_burg(time_step=0.005, max_number_of_formants=5, maximum_formant=5500, window_length=0.025, pre_emphasis_from=50)
    pitch = sound.to_pitch(time_step=0.005, pitch_floor=60, pitch_ceiling=500)
    values = {}
    for n in (1, 2, 3):
        try:
            v = formant.get_value_at_time(n, mid)
            values[f"f{n}_hz"] = f"{v:.2f}" if v == v else ""
        except Exception:
            values[f"f{n}_hz"] = ""
    try:
        hz = pitch.get_value_at_time(mid)
        values["f0_hz"] = f"{hz:.2f}" if hz == hz else ""
    except Exception:
        values["f0_hz"] = ""
    values.update({
        "id_persona": row["id_persona"], "forma": row["forma"], "interval_escolta": row["interval_escolta"], "clip": row["clip"],
        "token_start_abs": f"{start_abs:.3f}", "token_end_abs": f"{end_abs:.3f}", "token_p_min": f"{float(match['p_min']):.4f}", "centre_rel_s": f"{mid:.3f}",
    })
    return values


def main() -> None:
    rows = read("qa-consens-tokens-base.tsv")
    sound_cache: dict[str, parselmouth.Sound] = {}
    measures = []
    by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_form: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        for match in json.loads(row["token_matches"]):
            result = one_measure(row, match, sound_cache); measures.append(result); by_person[row["id_persona"]].append(result); by_form[row["forma"]].append(result)
    fields = ["id_persona", "forma", "interval_escolta", "clip", "token_start_abs", "token_end_abs", "centre_rel_s", "token_p_min", "f0_hz", "f1_hz", "f2_hz", "f3_hz"]
    out = PROV / "analisi-formants-consens.tsv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(measures)
    summary = []
    for form, items in sorted(by_form.items()):
        def nums(k: str) -> list[float]: return [float(item[k]) for item in items if item.get(k)]
        summary.append({"forma": form, "n_tokens": str(len(items)), "n_parlants": str(len({i['id_persona'] for i in items})), "n_f0": str(len(nums('f0_hz'))), "n_f1": str(len(nums('f1_hz'))), "n_f2": str(len(nums('f2_hz'))), "n_f3": str(len(nums('f3_hz'))), "f0_median_hz": f"{median(nums('f0_hz')):.2f}" if nums('f0_hz') else "", "f1_median_hz": f"{median(nums('f1_hz')):.2f}" if nums('f1_hz') else "", "f2_median_hz": f"{median(nums('f2_hz')):.2f}" if nums('f2_hz') else "", "f3_median_hz": f"{median(nums('f3_hz')):.2f}" if nums('f3_hz') else ""})
    out_summary = PROV / "resum-formants-consens.tsv"
    with out_summary.open("w", encoding="utf-8", newline="") as handle:
        fields_summary = list(summary[0]); writer = csv.DictWriter(handle, fieldnames=fields_summary, delimiter="\t", lineterminator="\n"); writer.writeheader(); writer.writerows(summary)
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle: people = list(csv.DictReader(handle, delimiter="\t"))
    for person in people:
        pid = person["id_persona"]; items = by_person.get(pid, []); report = ROOT / "persones" / f"{pid}.md"; text = report.read_text(encoding="utf-8")
        if items:
            def med(k: str) -> str:
                vals = [float(i[k]) for i in items if i.get(k)]
                return f"{median(vals):.2f}" if vals else "—"
            counts = {k: sum(bool(i.get(k)) for i in items) for k in ("f0_hz", "f1_hz", "f2_hz", "f3_hz")}
            section = (f"\n{MARKER}\n\nEn **{len(items)} tokens** consensuals, la mesura automàtica al centre del token dona medianes de F0 **{med('f0_hz')} Hz**, F1 **{med('f1_hz')} Hz**, F2 **{med('f2_hz')} Hz** i F3 **{med('f3_hz')} Hz**. Hi ha valors disponibles en {counts['f0_hz']} casos per a F0 i en {counts['f1_hz']}, {counts['f2_hz']} i {counts['f3_hz']} casos per a F1, F2 i F3, respectivament.\n\n"
                       "Els formants depenen de finestra, coarticulació, micròfon i alineació; són mesures instrumentals exploratòries i no una confirmació de vocalisme andorrà. La taula és `../proveniencia/analisi-formants-consens.tsv`.\n")
        else: section = f"\n{MARKER}\n\nNo hi ha tokens consensuals amb timestamp per mesurar formants.\n"
        report.write_text(replace_section(text, MARKER, section), encoding="utf-8")
    print(f"{len(measures)} tokens mesurats · {len(summary)} formes · {len(people)} informes")


if __name__ == "__main__":
    main()
