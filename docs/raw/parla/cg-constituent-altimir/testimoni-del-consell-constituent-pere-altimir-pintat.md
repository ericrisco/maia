---
title: "Testimoni del Consell Constituent — Pere Altimir Pintat"
---

# Testimoni del Consell Constituent — Pere Altimir Pintat

Material de partida de la **tanda 5 de parla**. La fitxa viu a
`docs/parla/oral/testimoni-constituent-altimir.md`.

## La peça

| | |
| --- | --- |
| Peça | #ConsellConstituent - Pere Altimir Pintat |
| Sèrie | [Testimonis del Consell Constituent](../../../fonts/consell-general-constituent.md) |
| URL | https://youtu.be/aBwACxaRdtQ |
| Durada | 880 s (14 min 40 s) |
| Llicència declarada | **Cap.** Llicència estàndard de YouTube. |
| Consultada | 2026-09-13 |

## L'àudio

```
font   : https://youtu.be/aBwACxaRdtQ
wav    : 16 kHz, mono, 880 s
sha256 : cc811e97836efa607c24b89501f2c9c80f4e0b7273eb88d9596b251f08480e4d
```

## Transcripció

**221 segments, 212 paraules marcades, 2.195 mots.** La pitjor proporció de
marques de totes les tandes fins ara.

```
whisper-cli -m ggml-large-v3-turbo-q5_0.bin -l ca \
  --vad --vad-model ggml-silero-v6.2.0.bin -ojf -ml 0 -et 2.8
```

## El que aquesta peça aporta: un tercer perfil

Aquest parlant **gairebé no fa servir marcadors discursius**. Parla llarg,
articulat i abstracte, amb sintaxi de text escrit.

| Marcador | Mandicó | Adellach | **Altimir** |
| --- | --- | --- | --- |
| `vull dir` | 167 | 2 | **0** |
| `bueno` | 54 | 6 | **1** |
| `clar` | 65 | 13 | **1** |
| `doncs` | 44 | 36 | **3** |
| `no?` de represa | 149 | 15 | **10** |
| *mots totals* | 3.768 | 2.153 | 2.195 |

**Tres testimonis, la mateixa sèrie, la mateixa cohort, el mateix format
d'entrevista, i tres perfils que no s'assemblen gens.**

La tanda 4 ja havia desmentit que els 167 «vull dir» de la tanda 3 fossin cap
signatura nacional. **Aquesta ho confirma amb un tercer punt**: la densitat de
marcadors és **de la persona**, no del país.

## Lèxic: poc, i és una dada

L'escaneig de novetat treu sobretot **vocabulari abstracte** —*convenciment*,
*complicitat*, *desenvolupant*, *insatisfet*— i **cap mot tradicional**. En una
peça de 2.195 mots d'un andorrà de Sant Julià parlant de la seva vida pública,
**no hi ha ni un sol andorranisme lèxic**.

Això no és un fracàs de la tanda: **és la troballa**. El registre formal andorrà
es pot parlar sense cap marca lèxica local, i qui busqui lèxic andorrà l'ha
d'anar a buscar al tema —ofici, casa, terra, festa—, **no a la persona**.

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | Transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua. |
| `paraules-marcades.txt` | Les 212 paraules marcades amb la seva probabilitat. |
