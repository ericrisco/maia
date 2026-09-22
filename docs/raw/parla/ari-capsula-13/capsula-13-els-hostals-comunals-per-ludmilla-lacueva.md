---
title: "Càpsula #13 — «Els hostals comunals», per Ludmilla Lacueva"
---

# Càpsula #13 — «Els hostals comunals», per Ludmilla Lacueva

Material de partida de la **tanda 14 de parla**. La fitxa viu a
`docs/parla/oral/els-hostals-comunals-lacueva.md`.

## La peça

| | |
| --- | --- |
| Peça | Càpsula #13. Els hostals comunals, per Ludmila Lacueva. |
| Sèrie | [Càpsules d'història d'AR+I](../../../fonts/ari-capsules.md) |
| URL | https://youtu.be/y8DXM2W2QI4 |
| Durada | 949 s (15 min 49 s) |
| Llicència declarada | **Creative Commons Attribution (reuse allowed)** |
| Consultada | 2026-09-14 |

## Per què aquesta peça és única al corpus

**És l'única autora que el corpus té escrita i parlada alhora.**

`docs/fonts/lacueva-hoteleria.md` recull la seva ponència de la 15a Diada
Andorrana (2002), i **cinc articles de `docs/temes/` en surten** — entre ells
[la taba i el mostassà](../../../temes/institucions/comuns-i-parroquies/la-taba-i-el-mostassa.md)
i [els hostals comunals](../../../temes/economia/turisme-i-neu/els-hostals-comunals.md).

Aquells articles són **veu compilada**: un agent llegint-la i reescrivint-la.
Això és **la seva veu**. El contracte del corpus separa les dues coses amb una
regla, i aquí es poden posar de costat.

## Cribratge: aquesta peça **pot ser llegida**

```
peça          mots  marc/1000  no?/1000  veredicte
cap13         2032        2.5       0.0  POT SER LLEGIDA
```

**Cap passat simple**, de manera que no es pot condemnar. Però hi ha senyals que
val més dir que callar:

- «l'any 1556, **any en el qual** vaig trobar la primera referència» — el relatiu
  amb article és de llengua escrita;
- **cap rectificació ni frase a mitges en dos mil mots**;
- fórmula d'obertura elaborada: «Primer de tot voldria agrair a l'Institut
  d'Estudis Andorrans i especialment al Jordi [?Guillemet]…».

**S'admet, i va etiquetada `possiblement-llegida` al frontmatter** perquè qui
munti un dataset la pugui excloure sense haver de tornar a jutjar-la.

### El llindar ha canviat, i també per a una peça ja admesa

El detector donava «parla» a tot el que passés de 2 marcadors per mil, xifra
triada a ull. S'ha pujat a **3** i s'hi ha **inclòs la interrogació de represa**
—`no?` interpel·la algú que escolta, i un text escrit no interpel·la ningú—.

Amb això, **la càpsula #57 (tanda 2), que ja era al corpus, també queda marcada
`POT SER LLEGIDA`** (1,2 per mil, cap `no?`). S'hi ha posat la mateixa etiqueta.
L'Altimir (tanda 5), que abans queia per sota, queda absolt: té 4,6 `no?` per mil.

## L'àudio

```
font   : https://youtu.be/y8DXM2W2QI4
wav    : 16 kHz, mono, 949 s
sha256 : 48c4a398160880887af86b2c4f1f2bbf445eb8551ae23194b3687dc3b2254801
```

## Transcripció

**318 segments, 122 paraules marcades, 2.032 mots.**

## La màquina falla exactament al vocabulari andorrà que el corpus ja té bé

| Ella diu (segons whisper) | La paraula és | Al corpus escrit |
| --- | --- | --- |
| «es regulaven per una **[?etapa]**» | **la taba** | **10 articles** |
| «**el Mostafa**», «**[?mostafà]**» (×7) | **el mostassà** | **8 articles** |

**Els dos termes institucionals andorrans centrals de la seva pròpia obra**, i la
màquina els converteix en *etapa* i en un nom propi àrab.

Que el corpus tingui les formes bones **des del seu text escrit** i la màquina
les perdi **des de la seva veu** és la demostració més neta que hi ha del
problema d'aquesta branca: **el que falla no és el parlant, és la transcripció**,
i falla justament on hi ha Andorra.

**No s'han corregit.**

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | Transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua. |
| `paraules-marcades.txt` | Les 122 paraules marcades amb la seva probabilitat. |
