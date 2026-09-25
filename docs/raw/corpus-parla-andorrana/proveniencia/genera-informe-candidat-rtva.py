"""Analitza un candidat RTVA fora del recompte canònic fins a la revisió."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[1]
CAND = ROOT / "proveniencia" / "candidats" / "lead-rtva-001"
JSON_PATH = CAND / "asr" / "joan-verdu.json"
FORMS = [
    "a nivell", "a veure", "aleshores", "aviam", "bé", "bueno", "clar",
    "crec", "de fet", "diguem", "doncs", "evidentment", "és a dir",
    "llavors", "no?", "o sigui", "per tant", "perquè", "tirar endavant",
    "vull dir", "ensenyança",
]
TERRITORIAL = [
    "Andorra", "andorrà", "andorrana", "país", "federació", "esquí",
    "esquiant", "muntanya", "pista", "Copa del Món", "dorsal", "Arinsal",
    "Alta Badia", "Lluís Marín", "a casa",
]
WORD_RE = re.compile(r"[^\W_]+(?:['’][^\W_]+)?", re.UNICODE)


def sec(value: str) -> float:
    h, m, s = value.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        while chunk := handle.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    segments = data['transcription']
    occurrences = []
    marker_counts = Counter()
    territorial_counts = Counter()
    tokens = []
    low_segments = 0
    for index, segment in enumerate(segments, start=1):
        text = segment.get('text', '').strip()
        if not text:
            continue
        tokens.extend(WORD_RE.findall(text.lower()))
        probabilities = [float(token.get('p', 0)) for token in segment.get('tokens', []) if not token.get('text', '').startswith('[_')]
        if probabilities and min(probabilities) < 0.55:
            low_segments += 1
        start = sec(segment['timestamps']['from'])
        end = sec(segment['timestamps']['to'])
        for form in FORMS:
            if re.search(rf'(?<![\wà-ÿ]){re.escape(form)}(?![\wà-ÿ])', text, re.I):
                marker_counts[form] += 1
                occurrences.append({
                    'forma': form,
                    'segment': index,
                    'inici_s': f'{start:.3f}',
                    'final_s': f'{end:.3f}',
                    'text_asr': text,
                    'estat': "candidat ASR; pendent d'audició",
                })
        for candidate in TERRITORIAL:
            if re.search(rf'(?<![\wà-ÿ]){re.escape(candidate)}(?![\wà-ÿ])', text, re.I):
                territorial_counts[candidate] += 1

    forms_path = CAND / 'formes.tsv'
    with forms_path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(occurrences[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader(); writer.writerows(occurrences)
    audio = CAND / 'audio.wav'
    duration = float(data.get('result', {}).get('duration', 807.34))
    text_path = CAND / 'asr' / 'joan-verdu.txt'
    report = CAND / 'informe.md'
    lines = [
        '# Candidat RTVA — Joan Verdú',
        '',
        'Aquest expedient és independent del corpus canònic i no incrementa encara el recompte de persones. La incorporació queda pendent de revisar la veu, separar entrevistador i entrevistat i confirmar els termes d\'ús.',
        '',
        '## Procedència i derivats',
        '',
        '- Font: [RTVA — Entrevista completa a Joan Verdú](https://www.rtva.ad/programes/entrevista-completa-joan-verdu).',
        '- Actiu multimèdia: `https://vodov.rtva.hiway.media/vod/migration/entrevista_joan_verdu.mp4`.',
        f'- Àudio local: `audio.wav`; durada aproximada {duration/60:.2f} minuts; SHA-256 `{sha256(audio)}`.',
        '- ASR: `whisper-cli`, `ggml-small.bin`, llengua `ca`, beam 5, 8 fils.',
        '- Derivats: `asr/joan-verdu.txt`, `asr/joan-verdu.vtt`, `asr/joan-verdu.json`.',
        '- Llicència: RTVA no declara una llicència oberta a la pàgina; el derivat queda restringit a recerca local.',
        '',
        '## Cobertura automàtica',
        '',
        f'- {len(segments)} segments ASR; {len(tokens)} tokens ortogràfics aproximats; {len(set(tokens))} tipus; TTR {len(set(tokens))/len(tokens):.4f}.',
        f'- {low_segments} segments contenen algun token amb probabilitat inferior a 0,55.',
        f'- {len(occurrences)} ocurrències de marcadors del repertori en `formes.tsv`; totes són candidats ASR.',
        '',
        '### Marcadors discursius',
        '',
    ]
    for form, count in marker_counts.most_common():
        lines.append(f'- `{form}`: {count} segments.')
    lines += ['', '### Lèxic territorial i esportiu', '']
    for form, count in territorial_counts.most_common():
        lines.append(f'- `{form}`: {count} segments.')
    lines += [
        '',
        '## Lectura lingüística provisional',
        '',
        '- El registre és una entrevista esportiva espontània, amb torns alterns i reformulacions; el text no permet atribuir cada marcador a Joan sense diarització.',
        '- Apareixen connectors i marcadors conversacionals com `bueno`, `a veure`, `o sigui`, `per tant`, `doncs`, `clar`, `evidentment` i `no?`.',
        '- El domini lèxic és l\'esquí alpí i la representació nacional: `Copa del Món`, `dorsal`, `màniga`, `pista`, `entrenament`, `federació` i `país`.',
        '- La transcripció conté hipòtesis ASR visibles (per exemple, topònims i noms propis deformats); cap grafia es considera variant dialectal fins a escoltar el WAV.',
        '- Queden obertes les dimensions de vocalisme, /r/, consonants finals, prosòdia, clítics, contacte i variació generacional.',
        '',
        '## Següent revisió',
        '',
        'Escoltar els intervals de `formes.tsv`, separar les intervencions de l\'entrevistador i completar una decisió auditiva abans de convertir aquest candidat en `pa-067` del corpus canònic.',
    ]
    report.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"{len(segments)} segments · {len(tokens)} tokens · {len(occurrences)} ocurrències · {len(marker_counts)} formes")


if __name__ == '__main__':
    main()
