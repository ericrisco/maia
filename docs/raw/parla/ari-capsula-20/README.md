---
title: "Càpsula #20 — «Els molins d'aigua d'Andorra», per Alan Ward"
---

# Càpsula #20 — «Els molins d'aigua d'Andorra», per Alan Ward

Material de partida de la **tanda 29 de parla**. La fitxa viu a
`docs/parla/oral/els-molins-daigua.md`.

## La peça

| | |
| --- | --- |
| Peça | Càpsula #20. Els molins d'aigua d'Andorra, per Alan Ward. |
| Sèrie | [Càpsules d'història d'AR+I](../../../fonts/ari-capsules.md) |
| URL | https://youtu.be/OBz__QiZyiQ |
| Durada | 659 s (10 min 59 s) |
| Llicència declarada | **Creative Commons Attribution (reuse allowed)** |
| Consultada | 2026-09-14 |

## L'àudio

```
font   : https://youtu.be/OBz__QiZyiQ
wav    : 16 kHz, mono, 659 s
sha256 : 5aaa893b56bfe843b80573e26953b374efac133fcb513f42112bea69a38288a1
```

## Cribratge previ

```
peça          mots  marc/1000  no?/1000  veredicte   passat simple
cap20         1674        4.8       0.0  parla       -
```

**Cap passat simple sintètic.** Llengua: **99 % català** (140 marcadors
catalans, 1 castellà).

## Transcripció

**432 segments, 111 paraules marcades, 1.674 mots — 6,6 % dels mots.**

```
whisper-cli -m ggml-large-v3-turbo-q5_0.bin -l ca \
  --vad --vad-model ggml-silero-v6.2.0.bin -ojf -ovtt -ml 0 -et 2.8
```

## La segona peça de molins del corpus

El corpus ja tenia la **#11** de Francina Pons
(`docs/parla/oral/les-moles-de-farina.md`, tanda 8), que parlava de **moles de
farina**. Aquesta parla de **la màquina**: la roda, la caiguda d'aigua, el
rendiment. Els dos vocabularis no se solapen gaire, i això és útil: dona dos
parlants sobre el mateix ofici amb lèxics complementaris.

## `[?llat]` — el buit que la tanda 29 tanca a mitges

`[?llat]` era un dels marcatges sense resoldre del registre. Aquesta peça en
dona **tres contextos**:

```
[00:04:12.210 --> 00:04:14.210] cap al segle XV o [?més] [?llat] [?XVI]
[00:09:07.720 --> 00:09:08.600] més [?llat] que fusta
[00:10:06.140 --> 00:10:06.560] més [?llat]
```

Amb un context de més:

```
[00:10:05.660 --> 00:10:06.140] [?Spelton]
[00:10:06.140 --> 00:10:06.560] més [?llat]
[00:10:06.560 --> 00:10:07.140] que Francis
```

Els tres són **«més ___»**, i els tres encaixen amb **`aviat`**, en la locució
**«més aviat (que)»**:

- «cap al segle XV o **més aviat** XVI» — *o millor dit, el XVI*;
- «pels components **més aviat** que fusta» — *ferro i acer en lloc de fusta*;
- «amb turbina Pelton **més aviat** que Francis» — *una en lloc de l'altra*.

La primera lectura provada va ser **`tard`**, i s'aguantava amb un sol context
(«al segle XV o més tard, XVI»). **Amb els tres contextos a la vista no
s'aguanta**: ni el ferro és *més tard que fusta* dins d'aquella frase, ni una
turbina és *més tarda* que una altra. `aviat` els explica tots tres.

**Però no s'escriu a la transcripció.** La regla de la línia 13 del brief diu
marcar el que no se sent, no el que sembla que deia. `[?llat]` es queda tal com
és; la hipòtesi viu aquí, a la fitxa i al registre, i **es tanca escoltant
00:10:06**, no raonant-hi més.

## `caval` — cinc vegades, i no és cap mot

El grup `caval` surt 5 vegades sempre en context de **cabal d'aigua**
(«necessita bastant menys quantitat de caval», «al llarg del seu [?caval]»).
`cabal` és 13 vegades a la prosa del corpus; `caval` cap. És **la màquina
escrivint una `b` com a `v`**, no una forma. Es documenta perquè no torni a
entrar a cap escaneig de novetat com si fos lèxic.

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | Transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua. |
| `paraules-marcades.txt` | Les 111 paraules marcades. |
