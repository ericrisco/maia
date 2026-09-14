# Càpsula #62 — «Els camins dels cérvols», per Laura de Castellet

Transcrita a la **tanda 29 de parla** i **no admesa al corpus**. **No té fitxa
a `docs/parla/`**, i no n'ha de tenir mentre la provinença no es pugui respondre:
el motiu és a [«Per què queda pendent»](#per-què-queda-pendent), més avall.

## La peça

| | |
| --- | --- |
| Peça | Càpsula #62. Els camins dels cérvols, per Laura de Castellet. |
| Sèrie | [Càpsules d'història d'AR+I](../../../../fonts/ari-capsules.md) |
| URL | https://youtu.be/sFtvDfYb2ao |
| Durada | 798 s (13 min 18 s) |
| Llicència declarada | **Creative Commons Attribution (reuse allowed)** |
| Consultada | 2026-09-14 |

## L'àudio

```
font   : https://youtu.be/sFtvDfYb2ao
wav    : 16 kHz, mono, 798 s
sha256 : 9e0435307041089a251181f2da626dcf6faca7003b30660571e24735124f1c07
```

## Per què queda pendent

**No és per la llengua, ni per la qualitat, ni perquè sigui llegida.** És
**parla real, consentida i en català**, i la transcripció és de les bones de la
sèrie. El problema és un altre, i és el primer d'aquesta mena que troba la
branca de parla: **la parlant diu ella mateixa que no és a Andorra.**

```
[00:00:53.290 --> 00:00:57.470] ha estat excepcional [?i] a mi el confinament em va enganxar
[00:00:53.290 --> 00:00:57.470] no a Andorra, ni tan sols a casa meva, sinó a l'Al [?Urgell,]
[00:00:57.890 --> 00:01:02.800] al poble de [?Tau.]
```

I es presenta, a la primera frase, com a **«civila de la [?seu]»** —molt
probablement *sibil·la de la Seu*, és a dir, la Seu d'Urgell (00:00:18).

Tot el que explica passa **fora del país**: els camins que segueix, les banyes
que troba, els voltors que busca, són de l'Alt Urgell. El brief diu **«recull
andorrà dit per andorrans»**. Aquí **la peça és andorrana** —la publica AR+I—,
però **no consta que ho sigui la parla**, i **consta el contrari del lloc**.

**No es descarta i no s'admet: queda pendent.** La línia 9 del brief diu que el
que no es pot respondre queda pendent i no entra a cap dataset, i això val per
la provinença igual que pel consentiment. Si algun dia es documenta que la
parlant és andorrana de casa o resident de llarg, **la peça entra tal com està**:
la transcripció ja és feta i no cal refer-la.

## El que això obre sobre tota la sèrie AR+I

Aquesta peça és la primera que **obliga a preguntar-se d'on són els altres deu
ponents** admesos de la sèrie. S'ha buscat, a les onze transcripcions, qualsevol
frase on el ponent es col·loqui ell mateix en un lloc:

| Càpsula | Què diu de si mateix | Lectura |
| --- | --- | --- |
| #20, #34, #56, #57, #66 | **«aquí a Andorra»** (fins a quatre vegades a la #20) | Es col·loca **dins** del país mentre parla. Indici feble —un convidat també ho pot dir— però és **a favor**. |
| #11, #13, #27, #40, #45, #49, #70 | **Res.** Cap frase en primera persona que situï el parlant. | **Buit.** Ni a favor ni en contra. |
| **#62** | **«no a Andorra»** | **En contra.** L'única de les dotze. |

Cap de les onze admeses no diu el contrari, i cinc diuen que hi són. **Això no
les acredita**, i el registre ho arrossega com a buit obert des de la tanda 6.
El que ha canviat avui és que **ja no és un buit teòric**: la sèrie convida qui
sap del tema, no qui és del lloc, i almenys una vegada això ha portat una veu de
fora.

## Cribratge previ — i l'avís

```
peça          mots  marc/1000  no?/1000  veredicte         passat simple
cap62         1737        2.3       0.0  POT SER LLEGIDA   -
```

**Cap passat simple sintètic** —per tant **no és condemnable**—, però **2,3
marcadors per mil** la posa per sota del llindar de densitat i el detector la
retorna com a `POT SER LLEGIDA`.

**El detector s'equivoca aquí, i val la pena deixar-ho escrit.** La peça és un
**relat en primera persona** —surt a caminar, troba una banya, torna enrere,
ensuma el camí— i un relat no necessita marcadors: **la seqüència el sosté tot
sol**. Els marcadors (*no?*, *vull dir*, *saps?*, *eh*) apareixen quan el
parlant ha de mantenir el fil o buscar l'acord de qui escolta, i qui explica una
història seguida no ha de fer ni una cosa ni l'altra.

Això és **el segon límit conegut de la mesura de densitat**. El primer, de la
tanda 19: la densitat sola mai no condemna, només el passat simple condemna.
Aquest n'és el revers: **la densitat sola tampoc no absol ni acusa un relat.**
El detector no es canvia —el llindar continua sent un avís i no una porta—, però
la nota queda perquè la pròxima sessió no llegeixi `POT SER LLEGIDA` com si fos
un veredicte.

Llengua: **98 % català** (174 marcadors catalans, 3 castellans).

## Transcripció

**390 segments, 119 paraules marcades, 1.737 mots — 6,9 % dels mots.**

```
whisper-cli -m ggml-large-v3-turbo-q5_0.bin -l ca \
  --vad --vad-model ggml-silero-v6.2.0.bin -ojf -ovtt -ml 0 -et 2.8
```

## Cinc grafies per a un animal

La màquina escriu el mateix animal de cinc maneres dins de la mateixa peça:

| Grafia | Vegades | Marcada |
| --- | --- | --- |
| `cèrbol` | 7 | sí |
| `cervons` | 2 | una sí, una no |
| `cervos` | 1 | no |
| `cèrbolets` | 1 | sí |
| `cérvol` (la normativa) | **0** | — |

**`cèrbol` vs `cérvol` no vol dir res**: en català oriental `b` i `v` són el
mateix so, i la màquina tria una grafia o l'altra sense informació nova.

**`cervons` sí que voldria dir alguna cosa**, perquè no és una grafia
alternativa: és **una síl·laba diferent i un accent diferent** (`cervó`, agut,
contra `cérvol`, pla). Si el so hi és, és un tret; si no, és la màquina
inventant.

**No es pot saber sense escoltar, i ningú no ha escoltat.** Queda com a buit.

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | Transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua. |
| `paraules-marcades.txt` | Les 119 paraules marcades. |
