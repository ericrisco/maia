"""Genera una fitxa provisional per a una mostra ASR del corpus independent.

La fitxa automàtica només descriu metadades i candidats observables. No afirma
cap tret dialectal: això exigeix escolta i comparació entre parlants.

    python genera-fitxa.py pa-004
"""

from __future__ import annotations

import json
import re
import sys
import csv
from collections import Counter
from pathlib import Path
from statistics import median

ROOT = Path(__file__).parents[1]
MARKERS = [
    "bé",
    "de fet",
    "és a dir",
    "aleshores",
    "evidentment",
    "diguem",
    "crec",
    "bueno",
    "clar",
    "vull dir",
    "o sigui",
    "llavors",
    "a veure",
    "aviam",
    "doncs",
    "perquè",
    "a nivell",
    "tirar endavant",
    "ensenyança",
    "reformeta",
]


def count(text: str, form: str) -> int:
    return len(re.findall(r"(?i)(?<!\w)" + re.escape(form) + r"(?!\w)", text))


def make(pid: str) -> Path:
    out = ROOT / "persones" / f"{pid}.md"
    # The first three records contain hand-written linguistic analysis. Keep
    # those reports intact when the automatic batch is regenerated.
    if out.exists() and re.search(r"^estat: analitzada-provisional(?:-[\w-]+)?$", out.read_text(encoding="utf-8"), re.MULTILINE):
        return out
    source = json.loads((ROOT / "proveniencia" / pid / "source.info.json").read_text())
    text = (ROOT / "transcripcions" / f"{pid}.txt").read_text()
    data = json.loads((ROOT / "transcripcions" / f"{pid}.json").read_text())
    audio_metrics = {}
    metrics_path = ROOT / "proveniencia" / "analisi-audio-metrics.tsv"
    if metrics_path.exists():
        with metrics_path.open(encoding="utf-8", newline="") as handle:
            audio_metrics = next(
                (row for row in csv.DictReader(handle, delimiter="\t") if row["id_persona"] == pid),
                {},
            )
    tokens = [
        token
        for segment in data["transcription"]
        for token in segment["tokens"]
        if not token["text"].startswith("[_") and re.search(r"\w", token["text"])
    ]
    words = re.findall(r"\b[\wàèéíòóúïüç']+\b", text.lower())
    bigrams = Counter(
        " ".join(pair)
        for pair in zip(words, words[1:])
        if all(len(part) >= 3 for part in pair)
    )
    recurrent = ", ".join(f"«{phrase}» ({n})" for phrase, n in bigrams.most_common(10) if n >= 2)
    low = [
        token["text"].strip().lower()
        for token in tokens
        if token["p"] < 0.55 and len(re.sub(r"[^\wàèéíòóúïüç]", "", token["text"])) >= 3
    ]
    low_counts = Counter(low)
    candidates = ", ".join(f"{word} ({n})" for word, n in low_counts.most_common(12))
    markers = "; ".join(f"**{form}** ({count(text, form)})" for form in MARKERS if count(text, form))
    starts = [segment["offsets"]["from"] for segment in data["transcription"]]
    ends = [segment["offsets"]["to"] for segment in data["transcription"]]
    durations = [max(0, end - start) for start, end in zip(starts, ends) if end >= start]
    gaps = [max(0, starts[i] - ends[i - 1]) for i in range(1, len(starts))]
    span_ms = max(0, (max(ends) if ends else 0) - (min(starts) if starts else 0))
    active_ms = sum(durations)
    lexical_count = len(tokens)
    low_ratio = (len(low) / lexical_count * 100) if lexical_count else 0
    confidence = (sum(token["p"] for token in tokens) / lexical_count) if lexical_count else 0
    pause_s = sum(gaps) / 1000
    pause_ratio = (sum(gaps) / span_ms * 100) if span_ms else 0
    words_per_min = (len(words) / (span_ms / 60000)) if span_ms else 0
    duration = source.get("duration", "")
    name = source.get("person_name") or source.get("title", pid).split("—")[-1].strip()
    if " per " in name:
        name = name.rsplit(" per ", 1)[-1].strip("»\" “”")
    body = f'''---
id_persona: {pid}
nom_public: {name}
font: {source.get("channel", "")}
estat: analitzada-provisional-automatica
---

# {pid} — {name}

## Inclusió provisional

Mostra audiovisual pública del canal **{source.get("channel", "")}**, titulada
«{source.get("title", "") }». La durada declarada és de {duration} segons. La
biografia lingüística i el lloc de socialització s'han de documentar abans de
considerar la mostra una veu nadiua.

## Transcripció i qualitat ASR

- Àudio: `../audios/{pid}/audio.wav`.
- Text: `../transcripcions/{pid}.txt`.
- VTT: `../transcripcions/{pid}.vtt`.
- JSON amb tokens: `../transcripcions/{pid}.json`.
- Incerteses: `../transcripcions/{pid}-marcada.txt`.
- {len(data['transcription'])} segments, {len(words)} mots aproximats i
  {len(low)} tokens per sota de probabilitat 0,55.

## Formes observables per revisar

Marcadors detectats: {markers or "cap amb el recompte automàtic"}.

Les formes amb més baixa confiança de l'ASR són: {candidates or "cap"}. Són
candidats d'escolta i no variants publicables.

## Mesures de ritme i confiança

- Extensió temporal coberta per l'ASR: **{span_ms / 1000:.1f} s**; {len(data['transcription'])} segments.
- Paraules aproximades: **{len(words)}**; ritme sobre l'extensió coberta: **{words_per_min:.1f} paraules/minut**.
- Durada acumulada dels segments: **{active_ms / 1000:.1f} s**; pauses estimades entre segments: **{pause_s:.1f} s** ({pause_ratio:.1f}% de l'extensió).
- Durada mediana d'un segment: **{(median(durations) / 1000) if durations else 0:.2f} s**.
- Tokens lèxics amb confiança inferior a 0,55: **{len(low)} de {lexical_count}** ({low_ratio:.1f}%); confiança mitjana dels tokens: **{confidence:.3f}**.
- Mesura directa del WAV: **{audio_metrics.get('pauses_audio', 'pendent')}** silencis detectats a -35 dB, **{audio_metrics.get('silenci_total_s', 'pendent')} s** acumulats; la taula completa és `../proveniencia/analisi-audio-metrics.tsv`.

Aquestes mesures comparen la sortida del model i els intervals temporals. Les
pauses són una estimació dels buits entre segments i no una anotació acústica;
cal escoltar-les abans d'interpretar velocitat, hesitació o prosòdia.

### Seqüències recurrents

{recurrent or "No hi ha cap bigrama recurrent amb aquest recompte automàtic."}

Són seqüències ortogràfiques repetides a la sortida de Whisper. Serveixen per
localitzar fragments de revisió i no es presenten com a construccions locals
fins que es contrastin amb el senyal.

## Anàlisi provisional

### Discurs i prosòdia

La mostra s'ha de classificar per situació comunicativa, torns, pauses,
repeticions, reformulacions i marcadors. Aquest informe conserva els recomptes
automàtics però no converteix cap freqüència en tret dialectal.

### Morfosintaxi

Cal revisar perífrasis, pronoms febles, concordances, subordinació i temps
verbals contra l'àudio. Les paraules produïdes per ASR poden ser errors de
segmentació o d'ortografia.

### Lèxic

Cal separar lèxic local, terminologia de l'entrevista, noms propis i formes
col·loquials. Només una forma repetida en parlants independents pot passar al
graf com a candidat compartit.

### Fonètica

La grafia de Whisper no mesura vocals, accent, /r/, palatalització ni prosòdia.
Qualsevol hipòtesi fonètica necessita un fragment temporal i escolta manual.

## Buits registrats

- biografia lingüística i parròquia de socialització;
- revisió manual de tokens de baixa confiança;
- anotació acústica i comparació amb altres parlants;
- separació de veus si la peça conté entrevistador o més d'un participant.
'''
    out.write_text(body)
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("ús: python genera-fitxa.py pa-004")
    print(make(sys.argv[1]))
