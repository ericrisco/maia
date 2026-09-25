# Candidat RTVA — Mireia Pedescoll

Aquest expedient és independent del recompte canònic. La pàgina RTVA identifica Mireia Pedescoll com a cap de servei de desenvolupament de Projectes Turístics del Comú d’Andorra la Vella, però l'àudio és una entrevista de ràdio amb torns alterns i encara no té diarització auditiva.

## Procedència i derivats

- Font: [RTVA — Entrevista a Mireia Pedescoll](https://www.rtva.ad/programes/entrevista-mireia-pedescoll).
- Actiu directe: la URL queda conservada a `source-url.txt`; el fitxer original és `audio-original.mp3`.
- Àudio WAV: `audio.wav`, 23.01 minuts, SHA-256 `99092a10edeccecfcab0f7596a18600545f5a9c11243d083e5e92e287e96a39c`.
- Àudio original MP3: SHA-256 `4a8af3b965b5de0e17fe2088f6a280f901347293cbbcd4a2160a87143391596c`.
- ASR: `whisper-cli`, models `ggml-small.bin` i `ggml-base.bin`, llengua `ca`, beam 5, 8 fils.
- Termes: RTVA no declara una llicència oberta a la pàgina; els derivats es conserven per a recerca local i no es redistribueix l'original.

## Cobertura automàtica

- `small`: 501 segments i 4458 tokens aproximats; `base`: 516 segments.
- `formes.tsv`: 366 ocurrències de les 35 formes candidates entre els dos models; 16 formes apareixen en ambdós.
- Marcadors small més freqüents: doncs=32; perquè=26; bé=21; no?=16; clar=15; a veure=14; aleshores=13; bueno=9; per tant=8; evidentment=7; vull dir=7; Escaldes=3.
- Lèxic territorial small localitzat: escaldes=2; país=13; andorra=1; muntanya=10; parròquia=2; català=4.

## Lectura lingüística provisional

- El registre radiofònic combina la veu de Mireia Pedescoll amb la de la persona entrevistadora; cap forma es pot atribuir a Mireia Pedescoll sense escolta i anotació de veu.
- Els connectors i les formes territorials són candidats textuals; les grafies ASR no permeten decidir obertura vocàlica, consonants finals, prosòdia, clítics ni contacte lingüístic.
- La baixa similitud entre les dues passades ASR s'ha conservat a `comparacio-asr.md` i justifica una revisió directa dels clips.

## Perfil acústic instrumental

`analisi-acustica.tsv` i `analisi-acustica.md` conserven durada, proporció de veu, F0, energia, centroid espectral i pauses dels 19 clips. Són descriptors exploratoris; no substitueixen l’audició ni confirmen trets dialectals.

## Revisió preparada

- `formes-clips.tsv`, `quadern-clips-formes.md` i `auditoria.html` preparen 19 clips representatius.
- El candidat no entra a `persones.tsv` ni als grafs canònics fins a confirmar la veu, la transcripció i els termes d'ús.

## Buits registrats

- No s'ha separat encara la veu de Mireia Pedescoll de l'entrevistador.
- No hi ha decisions auditives, variants escoltades ni anotació fonètica/prosòdica.
- La pàgina no declara una llicència oberta; l'ús es limita a recerca local.
