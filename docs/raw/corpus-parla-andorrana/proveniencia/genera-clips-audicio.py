"""Genera clips mono curts per a l'escolta dels intervals amb doble ASR.

Només crea clips per a files amb coincidència temporal entre les dues passades.
El manifest conserva el hash perquè cada derivat sigui auditable i regenerable.
"""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    queue = ROOT / "proveniencia" / "cua-audicio.tsv"
    clips_root = ROOT / "proveniencia" / "clips"
    clips_root.mkdir(parents=True, exist_ok=True)
    manifest = []
    with queue.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["coincidencia_temporal_asr"] != "sí":
                continue
            start, end = (float(value) for value in row["interval_escolta"].split("-", 1))
            relative = Path(row["clip_suggerit"])
            output = ROOT / "proveniencia" / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            audio = ROOT / "audios" / row["id_persona"] / "audio.wav"
            status = "existent"
            if not output.exists():
                subprocess.run(
                    [
                        "ffmpeg",
                        "-hide_banner",
                        "-loglevel",
                        "error",
                        "-ss",
                        f"{start:.3f}",
                        "-i",
                        str(audio),
                        "-t",
                        f"{max(0.1, end - start):.3f}",
                        "-ac",
                        "1",
                        "-ar",
                        "16000",
                        "-c:a",
                        "pcm_s16le",
                        str(output),
                    ],
                    check=True,
                )
                status = "generat"
            manifest.append(
                {
                    "forma": row["forma"],
                    "id_persona": row["id_persona"],
                    "interval_escolta": row["interval_escolta"],
                    "interval_base": row["interval_base"],
                    "clip": str(relative),
                    "estat_clip": status,
                    "sha256": sha256(output),
                    "duracio_s": f"{max(0.1, end - start):.3f}",
                }
            )
    out = ROOT / "proveniencia" / "clips-audicio.tsv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(manifest)
    print(f"{len(manifest)} clips · {out}")


if __name__ == "__main__":
    main()
