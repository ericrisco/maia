"""Agrupa provisionalment els segments del candidat RTVA per veu acústica.

És una ajuda de diarització, no una identificació de Joan ni de l'entrevistador.
"""
from __future__ import annotations

import csv
import json
import wave
from pathlib import Path

import numpy as np
from scipy.cluster.vq import kmeans2, whiten

ROOT = Path(__file__).parents[1]
CAND = ROOT / "proveniencia" / "candidats" / "lead-rtva-001"
AUDIO = CAND / "audio.wav"
JSON_PATH = CAND / "asr" / "joan-verdu.json"


def sec(value: str) -> float:
    h, m, s = value.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def features(samples: np.ndarray, rate: int) -> np.ndarray:
    samples = samples.astype(np.float32) / 32768.0
    if len(samples) < rate // 4:
        samples = np.pad(samples, (0, rate // 4 - len(samples)))
    window = np.hanning(len(samples))
    spectrum = np.abs(np.fft.rfft(samples * window)) + 1e-9
    freqs = np.fft.rfftfreq(len(samples), 1 / rate)
    total = spectrum.sum()
    centroid = float((freqs * spectrum).sum() / total)
    spread = float(np.sqrt(((freqs - centroid) ** 2 * spectrum).sum() / total))
    rms = float(np.sqrt(np.mean(samples * samples)))
    zcr = float(np.mean(np.abs(np.diff(np.signbit(samples)))))
    # Stable low-dimensional spectral profile for unsupervised clustering.
    bins = np.array([0, 300, 600, 1000, 1500, 2200, 3200, 4500, 6500, 8000])
    band = []
    for lo, hi in zip(bins[:-1], bins[1:]):
        mask = (freqs >= lo) & (freqs < hi)
        band.append(float(np.log1p(spectrum[mask].mean() if mask.any() else 0)))
    return np.array([np.log1p(rms * 1000), zcr, centroid / 1000, spread / 1000, *band])


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    with wave.open(str(AUDIO), 'rb') as handle:
        rate = handle.getframerate()
        audio = np.frombuffer(handle.readframes(handle.getnframes()), dtype=np.int16)
    rows = []
    vectors = []
    for index, segment in enumerate(data['transcription'], start=1):
        start = sec(segment['timestamps']['from'])
        end = sec(segment['timestamps']['to'])
        if end - start < 0.6:
            continue
        a, b = int(start * rate), min(len(audio), int(end * rate))
        if b <= a:
            continue
        vectors.append(features(audio[a:b], rate))
        rows.append((index, start, end, segment.get('text', '').strip()))
    matrix = np.array(vectors)
    scaled = whiten(matrix)
    centers, labels = kmeans2(scaled, 2, minit='++', seed=17)
    distances = np.sqrt(((scaled - centers[labels]) ** 2).sum(axis=1))
    output = CAND / 'segments-clusters.tsv'
    fields = ['segment', 'inici_s', 'final_s', 'cluster_acustic', 'distancia_centre', 'text_asr', 'estat']
    with output.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        for (index, start, end, text), label, distance in zip(rows, labels, distances):
            writer.writerow({
                'segment': index,
                'inici_s': f'{start:.3f}',
                'final_s': f'{end:.3f}',
                'cluster_acustic': int(label),
                'distancia_centre': f'{distance:.4f}',
                'text_asr': text,
                'estat': 'agrupació acústica provisional; identitat pendent',
            })
    summary = CAND / 'clusters-veus.md'
    lines = ['# Agrupació acústica provisional de veus', '', 'Els segments s’han agrupat en dos clústers amb energia, creuament per zero i perfil espectral. La clusterització no identifica quin clúster és Joan ni quin és l’entrevistador i pot separar també canvis de micròfon, soroll o prosòdia.', '']
    for label in range(2):
        selected = [row for row, current in zip(rows, labels) if current == label]
        duration = sum(end - start for _, start, end, _ in selected)
        lines.append(f'- **Clúster {label}:** {len(selected)} segments, {duration:.1f} s.')
        for _, start, end, text in selected[:5]:
            lines.append(f'  - {start:.2f}–{end:.2f} s: {text or "(sense text)"}')
    lines += ['', 'La taula `segments-clusters.tsv` només serveix per obrir fragments i intentar separar torns abans de l’audició humana.']
    summary.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    # Append a short, explicit caveat to the candidate report.
    report = CAND / 'informe.md'
    text = report.read_text(encoding='utf-8')
    marker = '## Següent revisió\n'
    addition = '## Separació acústica provisional\n\n`segments-clusters.tsv` agrupa els segments en dos clústers acústics per ajudar a separar entrevistador i entrevistat. La identitat de cada clúster continua desconeguda i requereix escolta; no s’utilitza per comptar formes de Joan.\n\n'
    if '## Separació acústica provisional' not in text:
        text = text.replace(marker, addition + marker, 1)
        report.write_text(text, encoding='utf-8')
    print(f'{len(rows)} segments agrupats · {sum(labels==0)} / {sum(labels==1)}')


if __name__ == '__main__':
    main()
