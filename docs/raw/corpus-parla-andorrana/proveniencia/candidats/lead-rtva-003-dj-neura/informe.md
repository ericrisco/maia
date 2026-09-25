# Candidat RTVA — DJ Neura

Aquest expedient és independent del recompte canònic. La pàgina RTVA identifica DJ Neura com a productor musical andorrà, però l'àudio és una entrevista de ràdio amb torns alterns i encara no té diarització auditiva.

## Procedència i derivats

- Font: [RTVA — Entrevista a DJ Neura](https://www.rtva.ad/programes/entrevista-dj-neura).
- Actiu directe: la URL queda conservada a `source-url.txt`; el fitxer original és `audio-original.mp3`.
- Àudio WAV: `audio.wav`, 11.69 minuts, SHA-256 `215137090848657e1aae31f5cf3ca144ffdd83e2358ac14905f11754403f91aa`.
- Àudio original MP3: SHA-256 `02d0856611082534b956121557ce01db00e7b8391db07b0423c7fd9472df0502`.
- ASR: `whisper-cli`, models `ggml-small.bin` i `ggml-base.bin`, llengua `ca`, beam 5, 8 fils.
- Termes: RTVA no declara una llicència oberta a la pàgina; els derivats es conserven per a recerca local i no es redistribueix l'original.

## Cobertura automàtica

- `small`: 142 segments i 1688 tokens aproximats; `base`: 189 segments.
- `formes.tsv`: 79 ocurrències de les 35 formes candidates entre els dos models; 8 formes apareixen en ambdós.
- Marcadors small més freqüents: doncs=15; bé=7; bueno=4; aleshores=4; no?=3; clar=3; perquè=2; a veure=1; de fet=1; o sigui=1.
- Lèxic territorial small localitzat: cançó=3; país=5; muntanya=2; andorra=1.

## Lectura lingüística provisional

- El registre radiofònic combina la veu de DJ Neura amb la de la persona entrevistadora; cap forma es pot atribuir a DJ Neura sense escolta i anotació de veu.
- Els connectors i les formes territorials són candidats textuals; les grafies ASR no permeten decidir obertura vocàlica, consonants finals, prosòdia, clítics ni contacte lingüístic.
- La baixa similitud entre les dues passades ASR s'ha conservat a `comparacio-asr.md` i justifica una revisió directa dels clips.

## Mesures formàntiques instrumentals

`formants.tsv` i `formants.md` conserven F0/F1/F2/F3 dels 10 clips. Són mesures exploratòries i no permeten inferir el vocalisme de DJ Neura sense audició.

## Perfil acústic instrumental

`analisi-acustica.tsv` i `analisi-acustica.md` conserven durada, proporció de veu, F0, energia, centroid espectral i pauses dels 10 clips. Són descriptors exploratoris; no substitueixen l’audició ni confirmen trets dialectals.

## Revisió preparada

- `formes-clips.tsv`, `quadern-clips-formes.md` i `auditoria.html` preparen 10 clips representatius.
- El candidat no entra a `persones.tsv` ni als grafs canònics fins a confirmar la veu, la transcripció i els termes d'ús.

## Buits registrats

- No s'ha separat encara la veu de DJ Neura de l'entrevistador.
- No hi ha decisions auditives, variants escoltades ni anotació fonètica/prosòdica.
- La pàgina no declara una llicència oberta; l'ús es limita a recerca local.
