# Candidat RTVA — Ian Moya

Aquest expedient és independent del recompte canònic. La pàgina RTVA identifica Ian Moya com a d'Escaldes-Engordany, però l'àudio és una entrevista de ràdio amb torns alterns i encara no té diarització auditiva.

## Procedència i derivats

- Font: [RTVA — Entrevista a Ian Moya, Les coses grans (23/02/2026)](https://www.rtva.ad/programes/entrevista-a-l-ian-moya-el-primer-concursant-d-euforia-andorra-les-coses-grans-23-02-2026).
- Actiu directe: la URL queda conservada a `source-url.txt`; el fitxer original és `audio-original.mp3`.
- Àudio WAV: `audio.wav`, 23.71 minuts, SHA-256 `6aab86bcd8fdcb40d247e85f27cec1ed3ef07807bdc238bf286438ccdac005be`.
- Àudio original MP3: SHA-256 `33a1f035f56e9a86dec3e1d08d984ee81c3a840f99368479273d2b4a535366c1`.
- ASR: `whisper-cli`, models `ggml-small.bin` i `ggml-base.bin`, llengua `ca`, beam 5, 8 fils.
- Termes: RTVA no declara una llicència oberta a la página; els derivats es conserven per a recerca local i no es redistribueix l'original.

## Cobertura automàtica

- `small`: 470 segments i 4669 tokens aproximats; `base`: 494 segments.
- `formes.tsv`: 299 ocurrències de les 35 formes candidates entre els dos models; 14 formes apareixen en ambdós.
- Marcadors small més freqüents: perquè=36; llavors=25; doncs=21; o sigui=20; clar=15; no?=12; bé=10; de fet=6; a veure=5; Escaldes=3; vull dir=3; a nivell=3.
- Lèxic territorial small localitzat: país=4; català=4; eufòria=13; cançó=7; andorra=3; escaldes=1.

## Lectura lingüística provisional

- El registre radiofònic combina la veu d'Ian amb la de la persona entrevistadora; cap forma es pot atribuir a Ian sense escolta i anotació de veu.
- Els connectors i les formes territorials són candidats textuals; les grafies ASR no permeten decidir obertura vocàlica, consonants finals, prosòdia, clítics ni contacte lingüístic.
- La baixa similitud entre les dues passades ASR s'ha conservat a `comparacio-asr.md` i justifica una revisió directa dels clips.

## Mesures formàntiques instrumentals

`formants.tsv` i `formants.md` conserven F0/F1/F2/F3 dels 15 clips. Són mesures exploratòries i no permeten inferir el vocalisme de Ian Moya sense audició.

## Perfil acústic instrumental

`analisi-acustica.tsv` i `analisi-acustica.md` conserven durada, proporció de veu, F0, energia, centroid espectral i pauses dels 15 clips. Són descriptors exploratoris; no substitueixen l’audició ni confirmen trets dialectals.

## Revisió preparada

- `formes-clips.tsv`, `quadern-clips-formes.md` i `auditoria.html` preparen 15 clips representatius.
- El candidat no entra a `persones.tsv` ni als grafs canònics fins a confirmar la veu, la transcripció i els termes d'ús.

## Buits registrats

- No s'ha separat encara la veu d'Ian de l'entrevistador.
- No hi ha decisions auditives, variants escoltades ni anotació fonètica/prosòdica.
- La pàgina no declara una llicència oberta; l'ús es limita a recerca local.
