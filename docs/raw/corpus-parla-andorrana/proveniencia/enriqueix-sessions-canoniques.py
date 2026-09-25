"""Afegeix context ASR i mesures instrumentals a les sessions canòniques.

Els camps nous són suport per a l'audició. No omplen cap decisió humana del
registre mestre ni canvien l'estat ``pendent`` de les files.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
SESSIONS = ("sessio-01.tsv", "sessio-02.tsv")
EXTRA = (
    "text_small",
    "text_base",
    "rol_provisional",
    "motiu_rol",
    "f0_median_hz",
    "f0_iqr_hz",
    "pausa_mediana_s",
    "f1_hz",
    "f2_hz",
    "f3_hz",
    "estat_instrumental",
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def clip_key(clip: str) -> str:
    return Path(clip).stem.replace(".", "_")


def text_from_json(path: Path) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    parts = [x.get("text", "").strip() for x in data.get("transcription", [])]
    return " ".join(x for x in parts if x and x != "#").strip()


def read_small(clip: str) -> str:
    key = clip_key(clip)
    directory = PROV / "qa-cua-small-json"
    for suffix in (".json", ".txt", ".log"):
        path = directory / f"{key}{suffix}"
        if path.exists():
            if suffix == ".json":
                return text_from_json(path)
            return path.read_text(encoding="utf-8", errors="replace").strip()
    return ""


def seconds(value: str) -> float:
    value = value.replace(",", ".")
    parts = value.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    return float(value)


def clip_start(clip: str) -> float:
    match = re.search(r"__(\d+(?:\.\d+)?)\.wav$", clip)
    return float(match.group(1)) if match else 0.0


def transcript_segments(person: str) -> list[tuple[float, float, str]]:
    path = PROV / person / "qa-base" / "transcripcio.json"
    if not path.exists():
        return []
    try:
        raw = path.read_bytes()
        try:
            data = json.loads(raw.decode("utf-8"))
        except UnicodeDecodeError:
            data = json.loads(raw.decode("cp1252"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return []
    out = []
    for item in data.get("transcription", []):
        text = item.get("text", "").strip()
        stamps = item.get("timestamps", {})
        if not text or not stamps:
            continue
        out.append((seconds(stamps.get("from", "0")), seconds(stamps.get("to", "0")), text))
    return out


def base_text(person: str, clip: str, acoustic: dict[str, str]) -> str:
    start = clip_start(clip)
    duration = float(acoustic.get("durada_s", "0") or 0)
    centre = start + duration / 2
    segments = transcript_segments(person)
    overlaps = [text for begin, end, text in segments if end >= start and begin <= start + duration]
    if overlaps:
        return " ".join(overlaps)
    if segments:
        return min(segments, key=lambda x: abs((x[0] + x[1]) / 2 - centre))[2]
    return ""


def main() -> None:
    acoustic = {row["clip"]: row for row in read_tsv(PROV / "analisi-acustica-clips.tsv")}
    formants: dict[str, dict[str, str]] = {}
    for row in read_tsv(PROV / "analisi-formants-cua-small.tsv"):
        formants.setdefault(row["clip"], row)

    for session in SESSIONS:
        path = PROV / "sessions" / session
        rows = read_tsv(path)
        for row in rows:
            if row.get("origen") != "canònic":
                continue
            clip = row["clip"]
            ar = acoustic.get(clip, {})
            fr = formants.get(clip, {})
            row.update(
                {
                    "text_small": read_small(clip),
                    "text_base": base_text(row["persona"], clip, ar),
                    "rol_provisional": "",
                    "motiu_rol": "segment canònic; el rol es confirma amb l'audició",
                    "f0_median_hz": ar.get("f0_median_hz", ""),
                    "f0_iqr_hz": ar.get("f0_iqr_hz", ""),
                    "pausa_mediana_s": ar.get("pausa_mediana_s", ""),
                    "f1_hz": fr.get("f1_hz", ""),
                    "f2_hz": fr.get("f2_hz", ""),
                    "f3_hz": fr.get("f3_hz", ""),
                    "estat_instrumental": "suport automàtic; pendent d'audició",
                }
            )
        fields = list(rows[0])
        fields.extend(field for field in EXTRA if field not in fields)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        print(f"{session}: {sum(bool(row.get('text_small')) for row in rows)} textos small")


if __name__ == "__main__":
    main()
