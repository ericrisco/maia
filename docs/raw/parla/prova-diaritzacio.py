"""Experiment FALLIT: partir dues veus sense eina de diarització.

Es guarda perquè la propera sessió no el torni a fer creient que és fàcil.

**El problema.** Les fonts més grans que s'han trobat —RTVA, amb 587 peces i un
programa d'entrevistes de 40-65 minuts— tenen **dues veus per gravació**. Una
transcripció que no sap dir quina frase és de qui **no pot declarar veu
originària**, perquè no se sap si el parlant és andorrà.

**La idea.** Whisper ja dona els segments amb marca de temps. Per a cada segment
es treuen MFCC (mitjana i desviació), es normalitzen i s'agrupen en dos amb
KMeans. Si hi ha dues veus, haurien de sortir dos grups.

**El resultat, mesurat amb silhouette:**

| Peça | Silhouette | Lectura |
| --- | --- | --- |
| #40, una sola veu (control) | 0,081 | cap estructura — correcte |
| #65, dues veus | 0,164 | alguna estructura, **assignació dolenta** |

**Per què no serveix.** El 0,164 sembla millor que el control, però en llegir les
etiquetes es veu que **posa preguntes i respostes al mateix grup**. Dos homes
adults, gravats amb el mateix micròfon i en la mateixa sala, no se separen amb
mitjanes i desviacions de MFCC.

**Què caldria.** Embeddings de locutor de debò (pyannote, speechbrain o
equivalent). En aquesta màquina hi ha `torch`, `numpy`, `scipy` i `sklearn`, però
**cap model de locutor**.

    python prova-diaritzacio.py <audio.wav> <whisper.json>
"""

from __future__ import annotations

import json
import sys

import numpy as np
from scipy.fftpack import dct
from scipy.io import wavfile
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

DURADA_MINIMA_MS = 1200


def mfcc(sig: np.ndarray, sr: int, n: int = 13, nfilt: int = 26) -> np.ndarray:
    """MFCC a mà: preèmfasi, finestres, banc de filtres mel i DCT."""
    sig = sig.astype(np.float64)
    sig = np.append(sig[0], sig[1:] - 0.97 * sig[:-1])
    fl, pas = int(0.025 * sr), int(0.010 * sr)
    n_frames = max(1, 1 + (len(sig) - fl) // pas)
    pad = np.zeros((n_frames - 1) * pas + fl)
    pad[: len(sig)] = sig[: len(pad)]
    idx = np.tile(np.arange(fl), (n_frames, 1))
    idx = idx + np.tile(np.arange(0, n_frames * pas, pas), (fl, 1)).T
    frames = pad[idx.astype(np.int32)] * np.hamming(fl)

    nfft = 512
    potencia = (1.0 / nfft) * np.abs(np.fft.rfft(frames, nfft)) ** 2
    alt = 2595 * np.log10(1 + (sr / 2) / 700)
    punts = np.linspace(0, alt, nfilt + 2)
    hz = 700 * (10 ** (punts / 2595) - 1)
    vora = np.floor((nfft + 1) * hz / sr).astype(int)

    banc = np.zeros((nfilt, nfft // 2 + 1))
    for m in range(1, nfilt + 1):
        esq, mig, dre = vora[m - 1], vora[m], vora[m + 1]
        for k in range(esq, mig):
            banc[m - 1, k] = (k - esq) / max(mig - esq, 1)
        for k in range(mig, dre):
            banc[m - 1, k] = (dre - k) / max(dre - mig, 1)

    energia = np.dot(potencia, banc.T)
    energia = np.where(energia == 0, np.finfo(float).eps, energia)
    return dct(20 * np.log10(energia), type=2, axis=1, norm="ortho")[:, :n]


def main() -> None:
    sr, sig = wavfile.read(sys.argv[1])
    if sig.ndim > 1:
        sig = sig.mean(axis=1)
    with open(sys.argv[2], encoding="utf-8") as f:
        segments = json.load(f)["transcription"]

    trets, quals = [], []
    for i, seg in enumerate(segments):
        a, b = seg["offsets"]["from"], seg["offsets"]["to"]
        if b - a < DURADA_MINIMA_MS:
            continue
        tall = sig[int(a * sr / 1000) : int(b * sr / 1000)]
        if len(tall) < sr // 2:
            continue
        m = mfcc(tall, sr)
        trets.append(np.concatenate([m.mean(0), m.std(0)]))
        quals.append(i)

    matriu = np.array(trets)
    matriu = (matriu - matriu.mean(0)) / (matriu.std(0) + 1e-9)
    km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(matriu)

    print(f"segments útils: {len(quals)}")
    print(f"silhouette: {silhouette_score(matriu, km.labels_):.3f}  (control d'una veu: 0,081)")
    print("--- mostra, per llegir si l'assignació té sentit ---")
    for i, etiqueta in list(zip(quals, km.labels_, strict=True))[:14]:
        print(f"  [{'AB'[etiqueta]}] {segments[i]['text'].strip()[:84]}")


if __name__ == "__main__":
    main()
