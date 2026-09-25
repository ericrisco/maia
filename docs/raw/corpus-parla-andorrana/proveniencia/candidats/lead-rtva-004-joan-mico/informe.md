# Candidat RTVA — Joan Micó

Aquest expedient és independent del recompte canònic. La pàgina RTVA identifica Joan Micó com a coordinador de sociologia d'Andorra Recerca + Innovació, però l'àudio és una entrevista de ràdio amb torns alterns i encara no té diarització auditiva.

## Procedència i derivats

- Font: [RTVA — Entrevista a Joan Micó](https://www.rtva.ad/programes/entrevista-joan-mico).
- Actiu directe: la URL queda conservada a `source-url.txt`; el fitxer original és `audio-original.mp3`.
- Àudio WAV: `audio.wav`, 25.11 minuts, SHA-256 `7e7372265a56c2a33f955856288d76b2fe4552b3f710d61280436d3b38b4cfbe`.
- Àudio original MP3: SHA-256 `31de7b084b689d9dfd3f31982e11507b1d9a49ef2ad16fcee55162c0478167bc`.
- ASR: `whisper-cli`, models `ggml-small.bin` i `ggml-base.bin`, llengua `ca`, beam 5, 8 fils.
- Termes: RTVA no declara una llicència oberta a la pàgina; els derivats es conserven per a recerca local i no es redistribueix l'original.

## Cobertura automàtica

- `small`: 337 segments i 3834 tokens aproximats; `base`: 457 segments.
- `formes.tsv`: 327 ocurrències de les 35 formes candidates entre els dos models; 12 formes apareixen en ambdós.
- Marcadors small més freqüents: no?=36; vull dir=32; perquè=30; clar=19; doncs=17; bueno=12; bé=12; llavors=7; o sigui=5; de fet=3; per tant=2; comuns=1.
- Lèxic territorial small localitzat: país=4; andorra=1.

## Lectura lingüística provisional

- El registre radiofònic combina la veu de Joan Micó amb la de la persona entrevistadora; cap forma es pot atribuir a Joan Micó sense escolta i anotació de veu.
- Els connectors i les formes territorials són candidats textuals; les grafies ASR no permeten decidir obertura vocàlica, consonants finals, prosòdia, clítics ni contacte lingüístic.
- La baixa similitud entre les dues passades ASR s'ha conservat a `comparacio-asr.md` i justifica una revisió directa dels clips.

## Perfil acústic instrumental

`analisi-acustica.tsv` i `analisi-acustica.md` conserven durada, proporció de veu, F0, energia, centroid espectral i pauses dels 4 clips. Són descriptors exploratoris; no substitueixen l’audició ni confirmen trets dialectals.

## Mesures formàntiques instrumentals

`formants.tsv` i `formants.md` conserven F0/F1/F2/F3 dels 12 clips. Són mesures exploratòries i no permeten inferir el vocalisme de Joan Micó sense audició.

## Revisió preparada

- `formes-clips.tsv`, `quadern-clips-formes.md` i `auditoria.html` preparen 12 clips representatius.
- El candidat no entra a `persones.tsv` ni als grafs canònics fins a confirmar la veu, la transcripció i els termes d'ús.

## Buits registrats

- No s'ha separat encara la veu de Joan Micó de l'entrevistador.
- No hi ha decisions auditives, variants escoltades ni anotació fonètica/prosòdica.
- La pàgina no declara una llicència oberta; l'ús es limita a recerca local.
