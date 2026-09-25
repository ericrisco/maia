"""Calcula descriptors acústics orientatius per a cada clip d'audició."""

from pathlib import Path
import csv
import wave
import numpy as np

ROOT = Path(__file__).parents[1]
RATE = 16000
FRAME = 640
HOP = 320
FFT = 2048
THRESH = 10 ** (-35 / 20)


def pitch(frame: np.ndarray):
    spectrum = np.abs(np.fft.rfft(frame * np.hanning(len(frame)), n=FFT))
    lo = int(70 * FFT / RATE)
    hi = int(350 * FFT / RATE)
    band = spectrum[lo : hi + 1]
    if not len(band) or float(np.max(band)) <= 0:
        return None
    index = int(np.argmax(band)) + lo
    if 0 < index < len(spectrum) - 1:
        left, peak, right = spectrum[index - 1 : index + 2]
        den = left - 2 * peak + right
        if den:
            index += 0.5 * (left - right) / den
    return index * RATE / FFT


def read_frames(path: Path):
    with wave.open(str(path), "rb") as audio:
        channels = audio.getnchannels()
        rate = audio.getframerate()
        raw = audio.readframes(audio.getnframes())
    values = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768
    if channels > 1:
        values = values.reshape(-1, channels).mean(axis=1)
    if rate != RATE:
        raise ValueError(f"taxa inesperada {rate} a {path}")
    return values


def quantile(values, q, default=0.0):
    return float(np.percentile(values, q)) if len(values) else default


def measure(row: dict) -> dict:
    path = ROOT / "proveniencia" / row["clip"]
    values = read_frames(path)
    frames = []
    for start in range(0, max(0, len(values) - FRAME + 1), HOP):
        frames.append(values[start : start + FRAME])
    if not frames and len(values):
        frames = [np.pad(values, (0, max(0, FRAME - len(values))))[:FRAME]]
    energies = np.asarray([float(np.sqrt(np.mean(frame * frame))) for frame in frames])
    zcr = np.asarray([float(np.mean(frame[:-1] * frame[1:] < 0)) for frame in frames])
    voiced = energies >= THRESH
    f0 = []
    centroid = []
    frequencies = np.fft.rfftfreq(FFT, 1 / RATE)
    for index, frame in enumerate(frames):
        if index % 2 == 0:
            spectrum = np.abs(np.fft.rfft(frame * np.hanning(len(frame)), n=FFT))
            centroid.append(float((frequencies * spectrum).sum() / spectrum.sum()) if spectrum.sum() else 0.0)
            if voiced[index]:
                value = pitch(frame)
                if value is not None:
                    f0.append(value)
    runs = []
    start = None
    for index, is_voice in enumerate(voiced):
        if is_voice and start is None:
            start = index
        if not is_voice and start is not None:
            runs.append((start, index))
            start = None
    if start is not None:
        runs.append((start, len(voiced)))
    pauses = [(b[0] - a[1]) * HOP / RATE for a, b in zip(runs, runs[1:])]
    db = lambda value: 20 * np.log10(max(float(value), 1e-9))
    return {
        "forma": row["forma"],
        "id_persona": row["id_persona"],
        "interval_escolta": row["interval_escolta"],
        "clip": row["clip"],
        "forma_en_qa": row.get("forma_en_qa", ""),
        "durada_s": f"{len(values) / RATE:.3f}",
        "veu_proporcio": f"{float(np.mean(voiced)) if len(voiced) else 0:.4f}",
        "rms_p10_db": f"{db(quantile(energies, 10)):.2f}",
        "rms_p50_db": f"{db(quantile(energies, 50)):.2f}",
        "rms_p90_db": f"{db(quantile(energies, 90)):.2f}",
        "zcr_p10": f"{quantile(zcr, 10):.4f}",
        "zcr_p90": f"{quantile(zcr, 90):.4f}",
        "f0_median_hz": f"{quantile(f0, 50):.2f}",
        "f0_iqr_hz": f"{quantile(f0, 75) - quantile(f0, 25):.2f}",
        "centroid_median_hz": f"{quantile(centroid, 50):.2f}",
        "centroid_p90_hz": f"{quantile(centroid, 90):.2f}",
        "segments_veu": str(len(runs)),
        "pausa_mediana_s": f"{quantile(pauses, 50):.3f}",
        "mostres_f0": str(len(f0)),
        "nota": "descriptor orientatiu; no és anotació fonètica",
    }


def main() -> None:
    with (ROOT / "proveniencia" / "qa-clips.tsv").open(encoding="utf-8", newline="") as handle:
        qa = {(r["id_persona"], r["forma"]): r for r in csv.DictReader(handle, delimiter="\t")}
    with (ROOT / "proveniencia" / "clips-audicio.tsv").open(encoding="utf-8", newline="") as handle:
        clips = list(csv.DictReader(handle, delimiter="\t"))
    rows = []
    for clip in clips:
        joined = dict(clip)
        joined["forma_en_qa"] = qa[(clip["id_persona"], clip["forma"])]["forma_en_qa"]
        rows.append(measure(joined))
    output = ROOT / "proveniencia" / "analisi-acustica-clips.tsv"
    fields = list(rows[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} clips · {output}")


if __name__ == "__main__":
    main()
