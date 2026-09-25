# Candidat Consell General — Xavier Espot

Aquest expedient és independent del recompte canònic. La pàgina del Consell General documenta el discurs-programa de Xavier Espot davant la cambra; l'extracte local és només el primer tram de la sessió i encara no té validació auditiva.

## Procedència i derivats

- Font: [Consell General — Discurs-programa de Xavier Espot](https://www.consellgeneral.ad/ca/videos/sessions-del-consell-general/any-2019/discurs-programa-del-candidat-xavier-espot-zamora).
- Font audiovisual: la URL del vídeo complet queda conservada a `source-url.txt`; l'àudio local és un extracte inicial de 120 segons.
- Àudio WAV: `audio.wav`, 2.00 minuts, SHA-256 `748c588fe7403ee9bd33115814357e212f8963f9aef77dad1295956d348be405`.
- ASR: `whisper-cli`, models `ggml-small.bin` i `ggml-base.bin`, llengua `ca`, beam 5, 8 fils.
- Termes: Consell General no declara una llicència oberta a la pàgina; els derivats es conserven per a recerca local i no es redistribueix l'original.

## Cobertura automàtica

- `small`: 32 segments i 312 tokens aproximats; `base`: 36 segments.
- `formes.tsv`: 7 ocurrències de les 35 formes candidates entre els dos models; 3 formes apareixen en ambdós.
- Marcadors small més freqüents: perquè=1; andorrana=1; per tant=1; comú=1.
- Lèxic territorial small localitzat: andorrana=1.

## Lectura lingüística provisional

- El registre parlamentari pot incloure torns institucionals fora del fragment; cap forma es pot atribuir a Xavier Espot sense escolta i anotació de veu.
- Els connectors i les formes territorials són candidats textuals; les grafies ASR no permeten decidir obertura vocàlica, consonants finals, prosòdia, clítics ni contacte lingüístic.
- La baixa similitud entre les dues passades ASR s'ha conservat a `comparacio-asr.md` i justifica una revisió directa dels clips.

## Perfil acústic instrumental

`analisi-acustica.tsv` i `analisi-acustica.md` conserven durada, proporció de veu, F0, energia, centroid espectral i pauses dels 4 clips. Són descriptors exploratoris; no substitueixen l’audició ni confirmen trets dialectals.

## Mesures formàntiques instrumentals

`formants.tsv` i `formants.md` conserven F0/F1/F2/F3 dels 4 clips. Són mesures exploratòries i no permeten inferir el vocalisme de Xavier Espot sense audició.

## Revisió preparada

- `formes-clips.tsv`, `quadern-clips-formes.md` i `auditoria.html` preparen 4 clips representatius.
- El candidat no entra a `persones.tsv` ni als grafs canònics fins a confirmar la veu, la transcripció i els termes d'ús.

## Buits registrats

- No s'ha validat encara que totes les paraules del fragment siguin de Xavier Espot.
- No hi ha decisions auditives, variants escoltades ni anotació fonètica/prosòdica.
- La pàgina no declara una llicència oberta; l'ús es limita a recerca local.
