"""Genera una auditoria regenerable dels expedients fora del canon."""
from __future__ import annotations
import csv, hashlib, json, wave
from pathlib import Path

ROOT = Path(__file__).parents[1]
CANDIDATES = ROOT / "proveniencia" / "candidats"
OUT = ROOT / "proveniencia" / "auditoria-candidats.tsv"
SUMMARY = ROOT / "proveniencia" / "auditoria-candidats.md"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def count_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(encoding="utf-8", newline="") as handle:
        return max(0, sum(1 for _ in csv.DictReader(handle, delimiter="\t")))


def asr_segments(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return 0
    return sum(1 for row in data.get("transcription", []) if str(row.get("text", "")).strip() not in {"", "#"})


def main() -> None:
    rows: list[dict[str, str]] = []
    for folder in sorted(p for p in CANDIDATES.iterdir() if p.is_dir() and p.name.startswith("lead-")):
        audio = folder / "audio.wav"
        with wave.open(str(audio)) as handle:
            duration = handle.getnframes() / handle.getframerate()
        source_file = folder / "source-url.txt"
        source_lines = source_file.read_text(encoding="utf-8").splitlines() if source_file.exists() else []
        source_page = source_lines[0] if source_lines else ""
        json_files = sorted((folder / "asr").glob("*.json"))
        base_json = [p for p in json_files if "base" in p.stem]
        small_json = [p for p in json_files if "base" not in p.stem]
        forms_path = folder / "formes-consens.tsv"
        clips_path = folder / "formes-clips.tsv"
        # Joan Verdú conserva la mateixa cua amb el nom històric formes-joan-clips.tsv.
        if not clips_path.exists():
            clips_path = folder / "formes-joan-clips.tsv"
        acoustic_path = folder / "analisi-acustica.tsv"
        rows.append({
            "id_candidat": folder.name,
            "source_page": source_page,
            "audio_s": f"{duration:.3f}",
            "audio_sha256": sha256(audio),
            "n_asr_models": str(len(small_json) + len(base_json)),
            "segments_small": str(asr_segments(small_json[0]) if small_json else 0),
            "segments_base": str(asr_segments(base_json[0]) if base_json else 0),
            "n_formes_consens": str(count_rows(forms_path)),
            "n_clips": str(count_rows(clips_path)),
            "n_acoustic": str(count_rows(acoustic_path)),
            "estat": "separat-del-canon; pendent-d-audicio",
            "veu_confirmada": "pendent",
            "termes_confirmats": "pendent",
        })
    fields = list(rows[0]) if rows else ["id_candidat"]
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    total_clips = sum(int(row["n_clips"]) for row in rows)
    total_forms = sum(int(row["n_formes_consens"]) for row in rows)
    lines = [
        "# Auditoria dels candidats fora del cànon", "",
        f"Aquesta taula resumeix **{len(rows)} expedients** que conserven àudio local, ASR, inventari de formes i cua de clips sense entrar a `persones.tsv` ni al graf canònic.", "",
        f"Total de clips de candidats: **{total_clips}**; files d'inventari de formes: **{total_forms}**.", "",
        "La veu, les variants i els termes d'ús continuen `pendent` en tots els expedients. Les formes i els descriptors són priorització automàtica i no confirmen cap tret dialectal.", "",
        "| candidat | àudio | ASR | formes | clips | acústica | estat |", "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        minutes = float(row["audio_s"]) / 60
        lines.append(f"| `{row['id_candidat']}` | {minutes:.2f} min | {row['n_asr_models']} models | {row['n_formes_consens']} | {row['n_clips']} | {row['n_acoustic']} | {row['estat']} |")
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} candidats · {total_clips} clips · {total_forms} files de formes")


if __name__ == "__main__":
    main()
