"""Calcula descriptors acústics orientatius per a la cua curta de quarantena."""

from __future__ import annotations

import csv
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
QUEUE = PROV / "cua-audicio-quarantena-20s.tsv"
OUT = PROV / "analisi-acustica-quarantena-20s.tsv"
REPORT_MARKER = "### Perfil acústic de la cua curta"
RATE, FRAME, HOP, FFT = 16000, 640, 320, 2048
THRESH = 10 ** (-35 / 20)


def read_frames(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as audio:
        channels, rate, raw = audio.getnchannels(), audio.getframerate(), audio.readframes(audio.getnframes())
    values = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768
    if channels > 1:
        values = values.reshape(-1, channels).mean(axis=1)
    if rate != RATE:
        raise ValueError(f"taxa inesperada {rate}: {path}")
    return values


def pitch(frame: np.ndarray) -> float | None:
    spectrum = np.abs(np.fft.rfft(frame * np.hanning(len(frame)), n=FFT))
    lo, hi = int(70 * FFT / RATE), int(350 * FFT / RATE)
    band = spectrum[lo : hi + 1]
    if not len(band) or float(np.max(band)) <= 0:
        return None
    return float((np.argmax(band) + lo) * RATE / FFT)


def q(values: list[float] | np.ndarray, percentile: float) -> float:
    return float(np.percentile(values, percentile)) if len(values) else 0.0


def measure(row: dict[str, str]) -> dict[str, str]:
    values = read_frames(PROV / row["clip"])
    frames = [values[start : start + FRAME] for start in range(0, max(0, len(values) - FRAME + 1), HOP)]
    if not frames and len(values):
        frames = [np.pad(values, (0, max(0, FRAME - len(values))))[:FRAME]]
    energies = np.asarray([float(np.sqrt(np.mean(frame * frame))) for frame in frames])
    zcr = np.asarray([float(np.mean(frame[:-1] * frame[1:] < 0)) for frame in frames])
    voiced = energies >= THRESH
    f0, centroids = [], []
    freqs = np.fft.rfftfreq(FFT, 1 / RATE)
    for index, frame in enumerate(frames):
        if index % 2 == 0:
            spectrum = np.abs(np.fft.rfft(frame * np.hanning(len(frame)), n=FFT))
            centroids.append(float((freqs * spectrum).sum() / spectrum.sum()) if spectrum.sum() else 0.0)
            if voiced[index]:
                value = pitch(frame)
                if value is not None:
                    f0.append(value)
    runs, start = [], None
    for index, is_voice in enumerate(voiced):
        if is_voice and start is None:
            start = index
        if not is_voice and start is not None:
            runs.append((start, index)); start = None
    if start is not None:
        runs.append((start, len(voiced)))
    pauses = [(b[0] - a[1]) * HOP / RATE for a, b in zip(runs, runs[1:])]
    db = lambda value: 20 * np.log10(max(float(value), 1e-9))
    return {
        "ordre": row["ordre"], "id_persona": row["id_persona"], "inici_s": row["inici_s"], "clip": row["clip"],
        "durada_s": f"{len(values) / RATE:.3f}", "veu_proporcio": f"{float(np.mean(voiced)) if len(voiced) else 0:.4f}",
        "rms_p50_db": f"{db(q(energies, 50)):.2f}", "zcr_p90": f"{q(zcr, 90):.4f}",
        "f0_median_hz": f"{q(f0, 50):.2f}", "f0_iqr_hz": f"{q(f0, 75) - q(f0, 25):.2f}",
        "centroid_median_hz": f"{q(centroids, 50):.2f}", "segments_veu": str(len(runs)),
        "pausa_mediana_s": f"{q(pauses, 50):.3f}", "mostres_f0": str(len(f0)),
        "nota": "descriptor orientatiu; no és anotació fonètica",
    }


def main() -> None:
    with QUEUE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    measured = [measure(row) for row in rows]
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(measured[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(measured)
    for person in sorted({row["id_persona"] for row in measured}):
        report = ROOT / "persones" / f"{person}.md"
        text = report.read_text(encoding="utf-8")
        if REPORT_MARKER in text:
            text = text[: text.index(REPORT_MARKER)].rstrip() + "\n"
        items = [row for row in measured if row["id_persona"] == person]
        lines = [REPORT_MARKER, "", "Descriptors calculats directament sobre els WAV de la cua curta. Són mesures instrumentals orientatives i no etiquetes fonètiques.", "", "| inici | veu activa | F0 mediana | IQR F0 | pausa mediana |", "|---:|---:|---:|---:|---:|"]
        lines.extend(f"| {row['inici_s']} s | {row['veu_proporcio']} | {row['f0_median_hz']} Hz | {row['f0_iqr_hz']} Hz | {row['pausa_mediana_s']} s |" for row in items)
        report.write_text(text.rstrip() + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(measured)} clips · {OUT}")


if __name__ == "__main__":
    main()
