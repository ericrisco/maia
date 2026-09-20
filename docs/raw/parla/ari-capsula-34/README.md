---
title: "Càpsula #34 — «Les falles d'Andorra», per Albert Roig"
---

# Càpsula #34 — «Les falles d'Andorra», per Albert Roig

Material de partida de la **tanda 6 de parla**. La fitxa viu a
`docs/parla/oral/les-falles-albert-roig.md`.

## La peça

| | |
| --- | --- |
| Peça | Càpsula #34. Les falles d'Andorra, per Albert Roig. |
| Sèrie | [Càpsules d'història d'AR+I](../../../fonts/ari-capsules.md) |
| URL | https://youtu.be/2Khh9Z7edcI |
| Publicada | 2020-05-28 |
| Durada | 1397 s (23 min 17 s) |
| Llicència declarada | **Creative Commons Attribution (reuse allowed)** |
| Consultada | 2026-09-13 |

## L'àudio

```
font   : https://youtu.be/2Khh9Z7edcI
wav    : 16 kHz, mono, 1397 s
sha256 : 627f05924e9b2e07ac15ec7533c3267606ef2ad81f3858c0abc4d3111d122ee2
```

## Transcripció

**867 segments, 121 paraules marcades, 3.292 mots.**

```
whisper-cli -m ggml-large-v3-turbo-q5_0.bin -l ca \
  --vad --vad-model ggml-silero-v6.2.0.bin -ojf -ml 0 -et 2.8
```

**És la transcripció més neta de les sis tandes**, amb diferència: 121 marques
en 867 segments. Les entrevistes del Consell Constituent en tenien 212 en 221.
La diferència és la gravació: aquesta està feta a l'aire lliure però amb el
parlant a prop del micròfon i parlant a poc a poc, perquè està explicant.

## El que aquesta peça permet fer per primera vegada

**Comprovar un article del corpus contra parla.**

El corpus ja té [Les falles](../../../temes/costums/falles/falles.md), escrit a
partir de **Pere Canturri**, font escrita. Diu que la falla era **escorça de beç
(bedoll)** i que el mànec era un **bastó de boix**.

Aquest parlant, que és fallaire i ho explica davant de l'arbre, diu
independentment: l'escorça es pela i s'enfila **«en un pal, ja sigui de boix o bé
amb una branca del mateix [?Ves]»** (00:01:01).

**Boix per al mànec, i l'arbre que whisper escriu «Ves».** Coincideix amb
Canturri sense conèixer-lo. És la primera vegada que el corpus pot contrastar
una descripció etnogràfica compilada amb algú fent-ho.

## «Ves» és quasi segur *beç*, i la mateixa peça ho demostra

Whisper escriu **«Ves»** i **«[?Vesos]»** per a l'arbre fallaire. El corpus
escriu **beç**, forma pirinenca de *bedoll*.

El que ho fa gairebé segur és que **dins la mateixa peça hi ha les dues formes**:
quan el parlant **cita un text històric** de Ramon Violant i Simorra, whisper hi
escriu **«la primera pela de [?badoll]»** (00:07:03), és a dir **bedoll**, i
**«escorça d'[?àlvar]»**, és a dir **àlber**.

**El text escrit que cita fa servir la forma estàndard; ell, quan parla pel seu
compte, en fa servir una altra.** Exactament el que la branca busca.

**No s'ha corregit «Ves» a «beç».** Correspon a qui escolti.

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | Transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua. |
| `paraules-marcades.txt` | Les 121 paraules marcades amb la seva probabilitat. |
