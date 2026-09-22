---
title: "Càpsula #11 — «Les moles de farina d'Andorra», per Francina Pons"
---

# Càpsula #11 — «Les moles de farina d'Andorra», per Francina Pons

Material de partida de la **tanda 8 de parla**. La fitxa viu a
`docs/parla/oral/les-moles-de-farina.md`.

## La peça

| | |
| --- | --- |
| Peça | Càpsula #11. Les moles de farina d'Andorra, per Francina Pons. |
| Sèrie | [Càpsules d'història d'AR+I](../../../fonts/ari-capsules.md) |
| URL | https://youtu.be/1X4uGbdg2iY |
| Durada | 837 s (13 min 57 s) |
| Llicència declarada | **Creative Commons Attribution (reuse allowed)** |
| Consultada | 2026-09-13 |

## L'àudio

```
font   : https://youtu.be/1X4uGbdg2iY
wav    : 16 kHz, mono, 837 s
sha256 : 90a5408b967c3ce01abe6d0195aa461a849e58cdcf96652d2d869c39145c641c
```

## Cribratge previ

**Des de la tanda 7, cap peça no s'escriu sense passar abans el detector.**

```
peça          mots  marc/1000  no?/1000  veredicte   passat simple
cap11         1905        5.8       0.5  parla       -
```

**Cap passat simple sintètic.** Passa.

## Transcripció

**145 segments, 79 paraules marcades, 1.905 mots.** Segona millor proporció del
corpus, després de la #34.

```
whisper-cli -m ggml-large-v3-turbo-q5_0.bin -l ca \
  --vad --vad-model ggml-silero-v6.2.0.bin -ojf -ml 0 -et 2.8
```

## Dues marques d'algú de dins

El corpus valora especialment quan **un parlant assenyala ell mateix que una
forma és la d'aquí**, perquè aleshores no cal deduir-ho.

**1. Es tradueix a si mateixa.** «amb **un assecle o rec**» (00:07:31). Diu la
forma i tot seguit en dona l'equivalent general, com qui sap que la primera no
s'entendrà fora.

**2. Cita com en deien.** «**La mola de casa, deien tots**» (00:04:11). No
descriu l'objecte: reporta el nom que li donava la gent.

## `mola`: el mot hi és, el sentit no

Ella fa servir **mola** tretze vegades per **el molí sencer** —l'edifici, el
negoci, la propietat—: «la casa que era més forta podia tenir **una mola** per
ell sol», «**la mola de casa**».

En llengua general **mola** és **la pedra**, i el conjunt és **el molí**. Ella fa
servir totes dues coses a la mateixa peça (*molí* hi surt 10 vegades), de manera
que **no és que no sàpiga el mot**: és que *mola* li serveix per a l'edifici.

**Es registren els dos sentits i no s'arbitra.**

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | Transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua. |
| `paraules-marcades.txt` | Les 79 paraules marcades amb la seva probabilitat. |
