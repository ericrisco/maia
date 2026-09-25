"""Extracta finestres de les veus en quarantena i les passa per un ASR independent."""

from pathlib import Path
import csv
import hashlib
import re
import subprocess

ROOT = Path(__file__).parents[1]
CLIP_DIR = ROOT / "proveniencia" / "clips-quarantena"
OUT_DIR = ROOT / "proveniencia" / "qa-quarantena"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-small.bin")

# Finestres triades per cobrir inici, desenvolupament i tram final sense usar
# la transcripció canònica com a entrada. La revisió auditiva continua pendent.
WINDOWS = {
    "pa-044": (0, 600, 1200),
    "pa-047": (0, 600, 1200),
    "pa-050": (60, 120, 240),
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def make_clip(person: str, start: int) -> tuple[Path, int]:
    source = ROOT / "audios" / person / "audio.wav"
    clip = CLIP_DIR / f"{person}__{start:04d}.wav"
    if not clip.exists():
        cmd = [
            "ffmpeg", "-y", "-ss", str(start), "-t", "30", "-i", str(source),
            "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(clip),
        ]
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if result.returncode:
            raise RuntimeError(result.stderr.decode(errors="replace"))
    return clip, 0


def transcribe(person: str, start: int, clip: Path) -> tuple[Path, Path]:
    stem = f"{person}__{start:04d}"
    prefix = OUT_DIR / stem
    txt = prefix.with_suffix(".txt")
    log = prefix.with_suffix(".log")
    if not txt.exists():
        cmd = [
            "whisper-cli", "-m", str(MODEL), "-l", "ca", "-t", "8", "-mc", "0",
            "-bs", "5", "-bo", "5", "-nf", "-otxt", "-of", str(prefix), str(clip),
        ]
        with log.open("w", encoding="utf-8") as handle:
            result = subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"whisper-cli ha fallat: {person} {start}")
    return txt, log


def repetition_ratio(text: str) -> tuple[int, int, float]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    unique = len(set(lines))
    return len(lines), unique, unique / len(lines) if lines else 0.0


def main() -> None:
    CLIP_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)
    rows = []
    for person, starts in WINDOWS.items():
        for start in starts:
            clip, _ = make_clip(person, start)
            txt, log = transcribe(person, start, clip)
            text = txt.read_text(encoding="utf-8", errors="replace")
            lines, unique, ratio = repetition_ratio(text)
            rows.append({
                "id_persona": person,
                "inici_s": start,
                "durada_s": 30,
                "clip": f"clips-quarantena/{clip.name}",
                "transcripcio": f"qa-quarantena/{txt.name}",
                "log": f"qa-quarantena/{log.name}",
                "sha256": hashlib.sha256(clip.read_bytes()).hexdigest(),
                "linies": lines,
                "linies_uniques": unique,
                "ratio_uniques": f"{ratio:.4f}",
                "estat": "pendent-audicio",
            })
    manifest = ROOT / "proveniencia" / "qa-quarantena.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} finestres · {manifest}")


if __name__ == "__main__":
    main()
