"""Calcula descriptors instrumentals dels clips de prospecció.

No fa classificació dialectal ni substitueix l'audició.
"""

from __future__ import annotations

import csv
import wave
from pathlib import Path

import numpy as np


ROOT = Path(__file__).parent
OUT = ROOT / "analisi-acustica.tsv"


def analyse(path: Path):
    with wave.open(str(path), "rb") as handle:
        rate = handle.getframerate()
        frames = handle.readframes(handle.getnframes())
    signal = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if not len(signal):
        return {"durada_s": "0", "rms_db": "", "zcr": "", "centroid_hz": "", "f0_median_hz": "", "veu_activa": "0"}
    frame = max(1, int(rate * 0.025))
    hop = max(1, int(rate * 0.010))
    rms_values, zcr_values, centroid_values, f0_values = [], [], [], []
    window = np.hanning(frame)
    for start in range(0, max(1, len(signal) - frame + 1), hop):
        chunk = signal[start:start + frame]
        if len(chunk) < frame:
            chunk = np.pad(chunk, (0, frame - len(chunk)))
        rms = float(np.sqrt(np.mean(chunk * chunk)))
        rms_values.append(rms)
        zcr_values.append(float(np.mean(np.abs(np.diff(np.signbit(chunk))))))
        spectrum = np.abs(np.fft.rfft(chunk * window))
        freqs = np.fft.rfftfreq(frame, 1 / rate)
        total = spectrum.sum()
        centroid_values.append(float((freqs * spectrum).sum() / total) if total else 0.0)
        if rms >= 0.015:
            corr = np.correlate(chunk, chunk, mode="full")[frame - 1:]
            lo, hi = max(1, int(rate / 500)), int(rate / 60)
            if hi < len(corr) and corr[lo:hi].size:
                lag = lo + int(np.argmax(corr[lo:hi]))
                if lag and corr[lag] > 0.25 * corr[0]:
                    f0_values.append(rate / lag)
    active = [r for r in rms_values if r >= 0.015]
    rms_db = 20 * np.log10(max(float(np.median(rms_values)), 1e-9))
    return {
        "durada_s": f"{len(signal)/rate:.3f}",
        "rms_db": f"{rms_db:.2f}",
        "zcr": f"{float(np.median(zcr_values)):.4f}",
        "centroid_hz": f"{float(np.median(centroid_values)):.1f}",
        "f0_median_hz": f"{float(np.median(f0_values)):.1f}" if f0_values else "",
        "veu_activa": f"{len(active)/len(rms_values):.4f}",
    }


def main():
    rows = []
    for path in sorted((ROOT / "clips").glob("*.wav")):
        row = {"clip": f"clips/{path.name}", **analyse(path), "estat": "descriptor instrumental; pendent d'audició"}
        rows.append(row)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    print(f"OK acústica Joan Burgués: {len(rows)} clips")


if __name__ == "__main__":
    main()
