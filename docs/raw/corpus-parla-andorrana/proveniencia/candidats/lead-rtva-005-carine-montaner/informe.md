# Candidat RTVA — Carine Montaner

Aquest expedient és independent del recompte canònic. La pàgina RTVA identifica Carine Montaner com a presidenta del grup parlamentari Andorra Endavant, però l'àudio és una entrevista de ràdio amb torns alterns i encara no té diarització auditiva.

## Procedència i derivats

- Font: [RTVA — Entrevista a Carine Montaner](https://www.rtva.ad/programes/entrevista-presidenta-grup-parlamentari-andorra-endavant-carine).
- Actiu directe: la URL queda conservada a `source-url.txt`; el fitxer original és `audio-original.mp3`.
- Àudio WAV: `audio.wav`, 51.68 minuts, SHA-256 `d48772ec308ba4fc686b2811b0f6ec4988ee9f95dcf4993c542785886b913840`.
- Àudio original MP3: SHA-256 `5a15ddace098684954f3edc05f7f2c367c9bd9cb5d9fac2f6871e09d0a7e89a7`.
- ASR: `whisper-cli`, models `ggml-small.bin` i `ggml-base.bin`, llengua `ca`, beam 5, 8 fils.
- Termes: RTVA no declara una llicència oberta a la pàgina; els derivats es conserven per a recerca local i no es redistribueix l'original.

## Cobertura automàtica

- `small`: 1107 segments i 9072 tokens aproximats; `base`: 1056 segments.
- `formes.tsv`: 736 ocurrències de les 35 formes candidates entre els dos models; 21 formes apareixen en ambdós.
- Marcadors small més freqüents: perquè=90; clar=62; doncs=36; és a dir=30; per tant=27; bé=20; a nivell=19; no?=14; bueno=11; llavors=10; a veure=5; comunals=4.
- Lèxic territorial small localitzat: andorra=5; país=7; parròquia=1; català=3.

## Lectura lingüística provisional

- El registre radiofònic combina la veu de Carine Montaner amb la de la persona entrevistadora; cap forma es pot atribuir a Carine Montaner sense escolta i anotació de veu.
- Els connectors i les formes territorials són candidats textuals; les grafies ASR no permeten decidir obertura vocàlica, consonants finals, prosòdia, clítics ni contacte lingüístic.
- La baixa similitud entre les dues passades ASR s'ha conservat a `comparacio-asr.md` i justifica una revisió directa dels clips.

## Perfil acústic instrumental

`analisi-acustica.tsv` i `analisi-acustica.md` conserven durada, proporció de veu, F0, energia, centroid espectral i pauses dels 22 clips. Són descriptors exploratoris; no substitueixen l’audició ni confirmen trets dialectals.

## Revisió preparada

- `formes-clips.tsv`, `quadern-clips-formes.md` i `auditoria.html` preparen 22 clips representatius.
- El candidat no entra a `persones.tsv` ni als grafs canònics fins a confirmar la veu, la transcripció i els termes d'ús.

## Buits registrats

- No s'ha separat encara la veu de Carine Montaner de l'entrevistador.
- No hi ha decisions auditives, variants escoltades ni anotació fonètica/prosòdica.
- La pàgina no declara una llicència oberta; l'ús es limita a recerca local.
