"""Calcula mètriques acústiques orientatives per comparar les veus.

Les mesures provenen del WAV, no de l'ASR. El F0 és una estimació espectral
simple i serveix per prioritzar l'escolta; no és una anotació fonètica.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parents[1]
RATE = 16_000
FRAME = 640  # 40 ms
HOP = 320  # 20 ms
FFT = 2048


def _frames(audio: Path):
    proc = subprocess.Popen(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(audio),
            "-ac",
            "1",
            "-ar",
            str(RATE),
            "-f",
            "s16le",
            "-",
        ],
        stdout=subprocess.PIPE,
    )
    assert proc.stdout is not None
    carry = np.empty(0, dtype=np.float32)
    while True:
        chunk = proc.stdout.read(RATE * 2)
        if not chunk:
            break
        samples = np.frombuffer(chunk, dtype="<i2").astype(np.float32) / 32768.0
        data = np.concatenate((carry, samples))
        stop = ((len(data) - FRAME) // HOP + 1) * HOP if len(data) >= FRAME else 0
        for start in range(0, stop, HOP):
            yield data[start : start + FRAME]
        carry = data[stop:]
    proc.wait()
    if proc.returncode:
        raise RuntimeError(f"ffmpeg ha fallat amb codi {proc.returncode}: {audio}")


def _pitch(frame: np.ndarray) -> float | None:
    windowed = frame * np.hanning(len(frame))
    spectrum = np.abs(np.fft.rfft(windowed, n=FFT))
    lo = int(70 * FFT / RATE)
    hi = int(350 * FFT / RATE)
    band = spectrum[lo : hi + 1]
    if not len(band) or float(np.max(band)) <= 0:
        return None
    index = int(np.argmax(band)) + lo
    if index <= 0 or index >= len(spectrum) - 1:
        return index * RATE / FFT
    left, peak, right = spectrum[index - 1 : index + 2]
    denom = left - 2 * peak + right
    correction = 0.5 * (left - right) / denom if denom else 0.0
    return (index + correction) * RATE / FFT


def measure(pid: str, status: str) -> dict[str, str]:
    rms: list[float] = []
    zcr: list[float] = []
    pitches: list[float] = []
    total_frames = 0
    voiced_frames = 0
    for index, frame in enumerate(_frames(ROOT / "audios" / pid / "audio.wav")):
        total_frames += 1
        value = float(np.sqrt(np.mean(frame * frame)))
        rms.append(value)
        zcr.append(float(np.mean(frame[:-1] * frame[1:] < 0)))
        # -35 dBFS matches the silence threshold used by calcula-audio-metrics.py.
        if value >= 10 ** (-35 / 20):
            voiced_frames += 1
            if index % 5 == 0:
                pitch = _pitch(frame)
                if pitch is not None:
                    pitches.append(pitch)
    rms_array = np.asarray(rms)
    zcr_array = np.asarray(zcr)
    voiced = np.asarray(pitches)
    duration = total_frames * HOP / RATE
    return {
        "id_persona": pid,
        "estat": status,
        "duracio_s": f"{duration:.2f}",
        "frames_veu": str(voiced_frames),
        "frames_total": str(total_frames),
        "ratio_veu": f"{voiced_frames / total_frames if total_frames else 0:.4f}",
        "rms_db_median": f"{20 * np.log10(max(float(np.median(rms_array)), 1e-9)):.2f}",
        "zcr_median": f"{float(np.median(zcr_array)) if len(zcr_array) else 0:.4f}",
        "f0_median_hz": f"{float(np.median(voiced)) if len(voiced) else 0:.2f}",
        "f0_p10_hz": f"{float(np.percentile(voiced, 10)) if len(voiced) else 0:.2f}",
        "f0_p90_hz": f"{float(np.percentile(voiced, 90)) if len(voiced) else 0:.2f}",
        "mostres_f0": str(len(voiced)),
    }


def main() -> None:
    status = {}
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            status[row["id_persona"]] = row["estat"]
    rows = [measure(pid, status[pid]) for pid in sorted(status)]
    out = ROOT / "proveniencia" / "analisi-prosodia.tsv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} àudios · {out}")


if __name__ == "__main__":
    main()
