# Candidat Consell General — Roser Suñé

Aquest expedient és independent del recompte canònic. La pàgina del Consell General documenta la sessió tradicional de la Constitució, on Roser Suñé intervé com a síndica general; l'àudio local conserva la sessió sencera; l'extracte inicial de 120 segons queda separat per a la revisió ràpida i encara no té validació auditiva.

## Procedència i derivats

- Font: [Consell General — Sessió tradicional de la Constitució de Roser Suñé](https://www.consellgeneral.ad/ca/videos/sessions-del-consell-general/any-2022/14-03-2022-sessio-tradicional-de-la-constitucio).
- Font audiovisual: la URL del vídeo complet queda conservada a `source-url.txt`; l'àudio local complet és `audio.wav`; `audio-extracte-120.wav` conserva també el primer tram de 120 segons.
- Àudio WAV: `audio.wav`, 15.92 minuts, SHA-256 `fa19d408c228361841b944d50a1b2be0b3f993f20f39cdea493abd2367ea0719`.
- ASR: `whisper-cli`, models `ggml-small.bin` i `ggml-base.bin`, llengua `ca`, beam 5, 8 fils.
- Termes: Consell General no declara una llicència oberta a la pàgina; els derivats es conserven per a recerca local i no es redistribueix l'original.

## Cobertura automàtica

- `small`: 308 segments i 2567 tokens aproximats; `base`: 52 segments.
- `formes.tsv`: 3 ocurrències de les 35 formes candidates entre els dos models; 0 formes apareixen en ambdós.
- Marcadors small més freqüents: a nivell=1; és a dir=1; doncs=1.
- Lèxic territorial small localitzat: cap dels termes de control.

## Lectura lingüística provisional

- El registre parlamentari pot incloure torns institucionals fora del fragment; cap forma es pot atribuir a Roser Suñé sense escolta i anotació de veu.
- Els connectors i les formes territorials són candidats textuals; les grafies ASR no permeten decidir obertura vocàlica, consonants finals, prosòdia, clítics ni contacte lingüístic.
- La baixa similitud entre les dues passades ASR s'ha conservat a `comparacio-asr.md` i justifica una revisió directa dels clips.

- La passada `small` reprodueix un tram al final de la sessió; es conserva com a incidència de transcripció i no com a evidència lingüística.
## Perfil acústic instrumental

`analisi-acustica.tsv` i `analisi-acustica.md` conserven durada, proporció de veu, F0, energia, centroid espectral i pauses dels clips seleccionats. Són descriptors exploratoris; no substitueixen l’audició ni confirmen trets dialectals.

## Revisió preparada

- `formes-clips.tsv`, `quadern-clips-formes.md` i `auditoria.html` preparen 3 clips representatius.
- El candidat no entra a `persones.tsv` ni als grafs canònics fins a confirmar la veu, la transcripció i els termes d'ús.

## Buits registrats

- No s'ha validat encara que totes les paraules del fragment siguin de Roser Suñé.
- No hi ha decisions auditives, variants escoltades ni anotació fonètica/prosòdica.
- La repetició detectada a la passada `small` i la diferència amb `base` impedeixen usar l'ASR com a transcripció final.
- La pàgina no declara una llicència oberta; l'ús es limita a recerca local.
