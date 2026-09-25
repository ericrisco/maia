# Candidat RTVA — Robert Guirao

Aquest expedient és independent del recompte canònic. La pàgina RTVA identifica Robert Guirao com a president de la branca andorrana de l’associació internacional de pilots i propietaris d’aeronaus, però l'àudio és una entrevista de ràdio amb torns alterns i encara no té diarització auditiva.

## Procedència i derivats

- Font: [RTVA — Entrevista a Robert Guirao](https://www.rtva.ad/programes/entrevista-robert-guirao).
- Actiu directe: la URL queda conservada a `source-url.txt`; el fitxer original és `audio-original.mp3`.
- Àudio WAV: `audio.wav`, 18.31 minuts, SHA-256 `70e8c005d798cd5f14bcb53e6ae5602c349e6db05aeea46e0faef4eb55a096b3`.
- Àudio original MP3: SHA-256 `f73e5cfad0f3066c01242cb459c3bd5bc18fb9a5647db66301457b95df01b25b`.
- ASR: `whisper-cli`, models `ggml-small.bin` i `ggml-base.bin`, llengua `ca`, beam 5, 8 fils.
- Termes: RTVA no declara una llicència oberta a la pàgina; els derivats es conserven per a recerca local i no es redistribueix l'original.

## Cobertura automàtica

- `small`: 438 segments i 3517 tokens aproximats; `base`: 319 segments.
- `formes.tsv`: 111 ocurrències de les 35 formes candidates entre els dos models; 12 formes apareixen en ambdós.
- Marcadors small més freqüents: perquè=8; doncs=5; bé=4; a veure=4; és a dir=3; evidentment=3; bueno=2; no?=2; o sigui=1; comú=1; diguem=1; de fet=1.
- Lèxic territorial small localitzat: país=3.

## Lectura lingüística provisional

- El registre radiofònic combina la veu de Robert Guirao amb la de la persona entrevistadora; cap forma es pot atribuir a Robert Guirao sense escolta i anotació de veu.
- Els connectors i les formes territorials són candidats textuals; les grafies ASR no permeten decidir obertura vocàlica, consonants finals, prosòdia, clítics ni contacte lingüístic.
- La baixa similitud entre les dues passades ASR s'ha conservat a `comparacio-asr.md` i justifica una revisió directa dels clips.

## Perfil acústic instrumental

`analisi-acustica.tsv` i `analisi-acustica.md` conserven durada, proporció de veu, F0, energia, centroid espectral i pauses dels 13 clips. Són descriptors exploratoris; no substitueixen l’audició ni confirmen trets dialectals.

## Revisió preparada

- `formes-clips.tsv`, `quadern-clips-formes.md` i `auditoria.html` preparen 13 clips representatius.
- El candidat no entra a `persones.tsv` ni als grafs canònics fins a confirmar la veu, la transcripció i els termes d'ús.

## Buits registrats

- No s'ha separat encara la veu de Robert Guirao de l'entrevistador.
- No hi ha decisions auditives, variants escoltades ni anotació fonètica/prosòdica.
- La pàgina no declara una llicència oberta; l'ús es limita a recerca local.
