---
title: "Testimoni del Consell Constituent — Olga Adellach Coma"
---

# Testimoni del Consell Constituent — Olga Adellach Coma

Material de partida de la **tanda 4 de parla**. La fitxa viu a
`docs/parla/oral/testimoni-constituent-adellach.md`.

## La peça

| | |
| --- | --- |
| Peça | #ConsellConstituent - Olga Adellach Coma |
| Sèrie | [Testimonis del Consell Constituent](../../../fonts/consell-general-constituent.md) |
| URL | https://youtu.be/Zkb4kXbYIJc |
| Durada | 792 s (13 min 12 s) |
| Llicència declarada | **Cap.** Llicència estàndard de YouTube. |
| Consultada | 2026-09-13 |

## El consentiment

**Consta**, igual que a la tanda 3: consellera general, entrevista donada a la
institució i publicada per la institució amb el seu nom. **Els drets no**:
redistribució `pendent`.

## L'àudio

```
font   : https://youtu.be/Zkb4kXbYIJc
wav    : 16 kHz, mono, 792.128 s
sha256 : 821f15d5ba5c0f61090f2319ac5b0e5d5d6780022df6a041a6703c01f4d3213c
```

## Transcripció

```
whisper-cli -m ggml-large-v3-turbo-q5_0.bin -l ca \
  --vad --vad-model ggml-silero-v6.2.0.bin -ojf -ml 0 -et 2.8
```

**114 segments, 181 paraules marcades, 2.153 mots.**

### Atenció a la proporció de marques

**181 marques en 114 segments** és la densitat més alta de les quatre tandes
(la #56 en tenia 69 en 77; la #57, 147 en 232; la Mandicó, 243 en 454). Els
segments aquí són més llargs, però **la peça és clarament la menys fiable de
les quatre** i la fitxa s'ha de llegir amb això al davant.

Una part de la culpa és del **discurs reportat**: parla citant el que li deien
—«podries ser rebedor de comptes», «no veus que et van a cremar»— i whisper
s'entrebanca a les cometes, que obre i tanca malament.

### El que aquesta peça diu dels marcadors

| Marcador | Adellach (2.153 mots) | Mandicó (3.768 mots) |
| --- | --- | --- |
| `vull dir` | **2** | **167** |
| `doncs` | **36** | 44 |
| `no?` de represa | **15** | **149** |
| `bueno` | 6 | 54 |

**Dues testimonis de la mateixa cohort, la mateixa sèrie i el mateix format, amb
perfils de marcadors oposats.** La Mandicó fa servir `vull dir` cada vint-i-dos
mots; l'Adellach, dues vegades en tota l'entrevista, i carrega sobre `doncs`.

Això és el primer avís seriós del corpus contra generalitzar: **`vull dir` no és
«andorrà», és d'aquella parlant**. Calen moltes veus abans de dir que res és
d'aquí.

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | Transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua. |
| `paraules-marcades.txt` | Les 181 paraules marcades amb la seva probabilitat. |
