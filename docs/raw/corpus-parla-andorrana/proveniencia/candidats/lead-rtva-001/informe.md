# Candidat RTVA — Joan Verdú

Aquest expedient és independent del corpus canònic i no incrementa encara el recompte de persones. La incorporació queda pendent de revisar la veu, separar entrevistador i entrevistat i confirmar els termes d'ús.

## Procedència i derivats

- Font: [RTVA — Entrevista completa a Joan Verdú](https://www.rtva.ad/programes/entrevista-completa-joan-verdu).
- Actiu multimèdia: `https://vodov.rtva.hiway.media/vod/migration/entrevista_joan_verdu.mp4`.
- Àudio local: `audio.wav`; durada aproximada 13.46 minuts; SHA-256 `5317200bbe5ca24c2262499ccdf03491936bb317accb7311bafe8fd248df099b`.
- ASR: `whisper-cli`, `ggml-small.bin`, llengua `ca`, beam 5, 8 fils.
- Derivats: `asr/joan-verdu.txt`, `asr/joan-verdu.vtt`, `asr/joan-verdu.json`.
- Llicència: RTVA no declara una llicència oberta a la pàgina; el derivat queda restringit a recerca local.

## Cobertura automàtica

- 266 segments ASR; 2394 tokens ortogràfics aproximats; 763 tipus; TTR 0.3187.
- 214 segments contenen algun token amb probabilitat inferior a 0,55.
- 74 ocurrències de marcadors del repertori en `formes.tsv`; totes són candidats ASR.

### Marcadors discursius

- `perquè`: 15 segments.
- `bé`: 13 segments.
- `no?`: 10 segments.
- `doncs`: 8 segments.
- `bueno`: 6 segments.
- `clar`: 5 segments.
- `a veure`: 4 segments.
- `llavors`: 4 segments.
- `per tant`: 3 segments.
- `evidentment`: 3 segments.
- `o sigui`: 1 segments.
- `de fet`: 1 segments.
- `vull dir`: 1 segments.

### Lèxic territorial i esportiu

- `esquí`: 11 segments.
- `pista`: 8 segments.
- `Copa del Món`: 5 segments.
- `país`: 4 segments.
- `dorsal`: 4 segments.
- `esquiant`: 3 segments.
- `Andorra`: 3 segments.
- `a casa`: 2 segments.
- `federació`: 2 segments.
- `Lluís Marín`: 1 segments.

## Lectura lingüística provisional

- El registre és una entrevista esportiva espontània, amb torns alterns i reformulacions; el text no permet atribuir cada marcador a Joan sense diarització.
- Apareixen connectors i marcadors conversacionals com `bueno`, `a veure`, `o sigui`, `per tant`, `doncs`, `clar`, `evidentment` i `no?`.
- El domini lèxic és l'esquí alpí i la representació nacional: `Copa del Món`, `dorsal`, `màniga`, `pista`, `entrenament`, `federació` i `país`.
- La transcripció conté hipòtesis ASR visibles (per exemple, topònims i noms propis deformats); cap grafia es considera variant dialectal fins a escoltar el WAV.
- Queden obertes les dimensions de vocalisme, /r/, consonants finals, prosòdia, clítics, contacte i variació generacional.

## Contrast independent small/base

Les dues transcripcions ASR tenen una similitud textual global de **0.1069**. `formes-consens.tsv` conserva els recomptes per marcador; les coincidències continuen pendents d'audició.

## Separació acústica provisional

`segments-clusters.tsv` agrupa els segments en dos clústers acústics per ajudar a separar entrevistador i entrevistat. La identitat de cada clúster continua desconeguda i requereix escolta; no s’utilitza per comptar formes de Joan.

## Segmentació textual provisional

`segments-speaker-provisional.tsv` marca torns probables a partir de preguntes i primera persona; `formes-joan-provisional.tsv` restringeix els marcadors als segments `joan-probable`. És una hipòtesi de navegació, no una anotació de veu.

## Clips de revisió

`formes-joan-clips.tsv` i `quadern-clips-formes.md` extreuen un clip per a cadascuna de les formes `joan-probable`; les formes presents en els dos ASR queden davant.

## Mesures instrumentals

`formants.tsv` i `formants.md` conserven F0/F1/F2/F3 dels 10 clips curts. Són mesures exploratòries i no permeten inferir el vocalisme de Joan sense audició.

## Següent revisió

Escoltar els intervals de `formes.tsv`, separar les intervencions de l'entrevistador i completar una decisió auditiva abans de convertir aquest candidat en `pa-067` del corpus canònic.
