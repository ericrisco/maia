---
title: "Càpsula #70 — «La nissaga dels Martí de les Bons», per Sara Ubach"
---

# Càpsula #70 — «La nissaga dels Martí de les Bons», per Sara Ubach

Material de partida de la **tanda 29 de parla**. La fitxa viu a
`docs/parla/oral/la-nissaga-dels-marti.md`.

## La peça

| | |
| --- | --- |
| Peça | Càpsula #70. La nissaga dels Martí de les Bons, per Sara Ubach. |
| Sèrie | [Càpsules d'història d'AR+I](../../../fonts/ari-capsules.md) |
| URL | https://youtu.be/e1RPheooiDI |
| Durada | 542 s (9 min 2 s) |
| Llicència declarada | **Creative Commons Attribution (reuse allowed)** |
| Consultada | 2026-09-14 |

## L'àudio

```
font   : https://youtu.be/e1RPheooiDI
wav    : 16 kHz, mono, 542 s
sha256 : 975d8e3680363ea51f50bc682b203058515c631bcd6742446acaa653930a9e12
```

## Cribratge previ

```
peça          mots  marc/1000  no?/1000  veredicte   passat simple
cap70          919        9.8       1.1  parla       -
```

**Cap passat simple sintètic**, i **la densitat de marcadors més alta de les
quatre càpsules de la tanda**. Passa amb marge.

Llengua: **100 % català** (90 marcadors exclusius catalans, 0 castellans).

## Transcripció

**108 segments, 45 paraules marcades, 919 mots — 4,9 % dels mots.** És la
**millor proporció de tot el corpus de parla**: cap peça admesa no havia
baixat del 5 %.

```
whisper-cli -m ggml-large-v3-turbo-q5_0.bin -l ca \
  --vad --vad-model ggml-silero-v6.2.0.bin -ojf -ovtt -ml 0 -et 2.8
```

## El que la màquina no sap escriure

La peça es titula **«La nissaga dels Martí»** i la màquina escriu **`missaga`
les tres vegades que el mot surt** al cos de la xerrada — mai `nissaga`.

`nissaga` és al DIEC2 («llinatge»); `missaga` no hi és ni és enlloc del corpus.
Una `n-` inicial que es llegeix `m-` davant de vocal pot ser assimilació real
o pot ser la màquina. **No se sap i no s'arbitra**: queda com a buit registrat
a la fitxa.

## `adot` — el mot que el corpus només tenia dins d'una citació

La ponent diu **`l'adot`** dues vegades, com a mot seu, sense citar ningú
(00:03:25 i 00:03:33).

- **No és al DIEC2.** Consultat el 2026-09-14: zero accepcions. El diccionari
  recull `dot`.
- **És al corpus**, però només **dins d'un document notarial de 1788 citat
  entre cometes** («crescut adot y aixovar»), a
  `docs/temes/historia/antic-regim/dos-capitols-matrimonials-de-1788.md` i
  `docs/temes/historia/antic-regim/lhereu-i-el-cabaler.md`.

O sigui: fins avui el corpus tenia `adot` com a **cita d'arxiu**, i ara el té
com a **mot viu en boca d'una persona el 2026**. Es registren els dos usos i
no s'arbitra si és arcaisme conservat, tecnicisme d'ofici o forma corrent.

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | Transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua. |
| `paraules-marcades.txt` | Les 45 paraules marcades. |
