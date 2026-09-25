"""Assegura un clip local per a cada fila de la cua d'audició."""

from pathlib import Path
import csv
import hashlib
import subprocess

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def parse_interval(value: str) -> tuple[float, float]:
    start, end = value.split("-", 1)
    return float(start), float(end)


def extract(row: dict) -> tuple[str, str]:
    start, end = parse_interval(row["interval_escolta"])
    duration = max(0.10, end - start)
    rel = row["clip_suggerit"]
    path = PROV / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        source = ROOT / "audios" / row["id_persona"] / "audio.wav"
        cmd = [
            "ffmpeg", "-y", "-ss", f"{start:.3f}", "-t", f"{duration:.3f}",
            "-i", str(source), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
            str(path),
        ]
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if result.returncode:
            raise RuntimeError(f"ffmpeg ha fallat per {row['id_persona']} {row['forma']}")
    actual = path.stat().st_size
    if actual == 0:
        raise RuntimeError(f"clip buit: {path}")
    duration_actual = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], text=True).strip()
    return hashlib.sha256(path.read_bytes()).hexdigest(), duration_actual


def main() -> None:
    with (PROV / "cua-audicio.tsv").open(encoding="utf-8", newline="") as handle:
        queue = list(csv.DictReader(handle, delimiter="\t"))
    existing_path = PROV / "clips-audicio.tsv"
    with existing_path.open(encoding="utf-8", newline="") as handle:
        existing = {(r["id_persona"], r["forma"]): r for r in csv.DictReader(handle, delimiter="\t")}
    added = 0
    for row in queue:
        key = (row["id_persona"], row["forma"])
        if key not in existing:
            sha, duration = extract(row)
            existing[key] = {
                "forma": row["forma"],
                "id_persona": row["id_persona"],
                "interval_escolta": row["interval_escolta"],
                "interval_base": row["interval_base"],
                "clip": row["clip_suggerit"],
                "estat_clip": "existent-extraient-sense-overlap",
                "sha256": sha,
                "duracio_s": f"{float(duration):.3f}",
            }
            added += 1
    fields = ["forma", "id_persona", "interval_escolta", "interval_base", "clip", "estat_clip", "sha256", "duracio_s"]
    with existing_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in queue:
            writer.writerow(existing[(row["id_persona"], row["forma"])])
    print(f"clips afegits: {added}; total: {len(queue)}; manifest: {existing_path}")


if __name__ == "__main__":
    main()
