"""Mesura acústica específica de les 28 divergències dels clips forts."""

from collections import defaultdict
from pathlib import Path
from statistics import median
import csv
import re

import parselmouth

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_interval(value: str) -> tuple[float, float]:
    start, end = value.split("-", 1)
    return float(start), float(end)


def numeric(value: str) -> str:
    return f"{float(value):.2f}" if value not in {"", None} else ""


def main() -> None:
    divergences = [row for row in read("qa-clips-forts-consens.tsv") if row["categoria"] != "A-tres-models"]
    candidates = {(row["id_persona"], row["forma"]): row for row in read("candidats-forts.tsv")}
    clip_metrics = {(row["id_persona"], row["forma"], row["interval_escolta"]): row for row in read("analisi-acustica-clips.tsv")}
    all_metrics = read("analisi-acustica-clips.tsv")
    baseline: dict[str, dict[str, float]] = {}
    for pid in {row["id_persona"] for row in divergences}:
        subset = [row for row in all_metrics if row["id_persona"] == pid]
        baseline[pid] = {}
        for key in ("f0_median_hz", "centroid_median_hz", "veu_proporcio", "pausa_mediana_s"):
            values = [float(row[key]) for row in subset if row.get(key)]
            baseline[pid][key] = median(values) if values else 0.0
    cache: dict[str, tuple[parselmouth.Sound, parselmouth.Formant, parselmouth.Pitch, parselmouth.Intensity]] = {}
    output = []
    for row in divergences:
        key = (row["id_persona"], row["forma"])
        candidate = candidates[key]
        clip_start, clip_end = parse_interval(candidate["interval_escolta"])
        absolute = candidate["token_intervals_absolute"].split(";")[0]
        token_start, token_end = parse_interval(absolute)
        clip_path = str(PROV / candidate["clip"])
        if clip_path not in cache:
            sound = parselmouth.Sound(clip_path)
            cache[clip_path] = (sound, sound.to_formant_burg(time_step=0.005, max_number_of_formants=5, maximum_formant=5500, window_length=0.025, pre_emphasis_from=50), sound.to_pitch(time_step=0.005, pitch_floor=60, pitch_ceiling=500), sound.to_intensity(minimum_pitch=60))
        sound, formant, pitch, intensity = cache[clip_path]
        rel_start = max(0.015, min(sound.duration - 0.015, token_start - clip_start))
        rel_end = max(rel_start + 0.01, min(sound.duration - 0.015, token_end - clip_start))
        center = rel_start + (rel_end - rel_start) / 2
        try: f0 = pitch.get_value_at_time(center)
        except Exception: f0 = float("nan")
        vals = {"f0_token_hz": f0}
        for n in (1, 2, 3):
            try: vals[f"f{n}_token_hz"] = formant.get_value_at_time(n, center)
            except Exception: vals[f"f{n}_token_hz"] = float("nan")
        try: vals["intensity_token_db"] = intensity.get_value(center)
        except Exception: vals["intensity_token_db"] = float("nan")
        metric = clip_metrics.get((row["id_persona"], row["forma"], candidate["interval_escolta"]), {})
        base = baseline[row["id_persona"]]
        result = dict(row)
        result["interval_escolta"] = candidate["interval_escolta"]
        result["clip"] = candidate["clip"]
        result.update({
            "token_interval_absolute": absolute,
            "token_duration_s": f"{token_end - token_start:.3f}",
            "f0_token_hz": numeric(vals["f0_token_hz"] if vals["f0_token_hz"] == vals["f0_token_hz"] else ""),
            "f1_token_hz": numeric(vals["f1_token_hz"] if vals["f1_token_hz"] == vals["f1_token_hz"] else ""),
            "f2_token_hz": numeric(vals["f2_token_hz"] if vals["f2_token_hz"] == vals["f2_token_hz"] else ""),
            "f3_token_hz": numeric(vals["f3_token_hz"] if vals["f3_token_hz"] == vals["f3_token_hz"] else ""),
            "intensity_token_db": numeric(vals["intensity_token_db"] if vals["intensity_token_db"] == vals["intensity_token_db"] else ""),
            "f0_persona_median_hz": f"{base['f0_median_hz']:.2f}",
            "delta_f0_clip_persona_hz": f"{float(metric.get('f0_median_hz', 0) or 0) - base['f0_median_hz']:.2f}" if metric else "",
            "centroid_clip_hz": metric.get("centroid_median_hz", ""),
            "veu_clip": metric.get("veu_proporcio", ""),
            "pausa_clip_s": metric.get("pausa_mediana_s", ""),
            "estat": "descriptor instrumental; revisió auditiva pendent",
        })
        output.append(result)
    fields = ["id_persona", "forma", "categoria", "clip", "interval_escolta", "token_interval_absolute", "token_duration_s", "f0_token_hz", "f1_token_hz", "f2_token_hz", "f3_token_hz", "intensity_token_db", "f0_persona_median_hz", "delta_f0_clip_persona_hz", "centroid_clip_hz", "veu_clip", "pausa_clip_s", "estat"]
    with (PROV / "analisi-acustica-divergencies.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows({field: row.get(field, "") for field in fields} for row in output)
    print(f"{len(output)} divergències mesurades · {sum(bool(r['f1_token_hz']) for r in output)} amb F1 · {sum(bool(r['f0_token_hz']) for r in output)} amb F0")


if __name__ == "__main__":
    main()
