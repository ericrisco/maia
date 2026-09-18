---
type: article
title: Vuitanta-cinc coma nou
description: "El salari mitjà d'una dona andorrana era el 55,8% del d'un home el desembre del 1967 i és el 85,9% el desembre del 2025. Seixanta anys de bretxa salarial, desembre a desembre, i encara falten catorze punts."
tema: temes/societat/dones
veu: compilada
epoca: contemporania
apte_llengua: false
font: estadistica-ad
timestamp: 2026-09-18T20:00:00Z
tags: [dones, treball, salaris, desigualtat, estadistica, serie-historica]
---

# Vuitanta-cinc coma nou

**Baixat de l'API del Departament d'Estadística el 18-09-2026**
(`docs/raw/estadistica-api/treball-mercat/massa-salarial-desembres-2026-09-18.tsv`,
**CC BY 4.0**, [font](../../../fonts/estadistica-ad.md)). **El corpus tenia la
sèrie d'assalariats des del desembre del 1966
([el treball](../treball/treball.md)) i no n'havia tingut mai els salaris.**

> **Per què només desembres.** **La sèrie de la font és mensual des del juliol
> del 1966 i l'API la serveix en un URL que, sencer, fa 5.922 caràcters i
> retorna `500`.** **S'ha demanat el desembre de cada any**, que és **el mateix
> mes que el corpus ja feia servir per a la sèrie d'assalariats** i el que la
> font mateixa fa servir de referència anual.

## La sèrie

**Salari mitjà mensual del desembre, en euros, i la relació entre tots dos:**

| Desembre de | Dones | Homes | **Dones / homes** |
| --- | ---: | ---: | ---: |
| **1966** | 39,27 € | 70,30 € | **55,9%** |
| 1970 | 32,49 € | 47,75 € | 68,0% |
| 1975 | 71,20 € | 116,71 € | 61,0% |
| 1980 | 228,33 € | 334,44 € | 68,3% |
| 1985 | 399,97 € | 586,50 € | 68,2% |
| **1990** | 715,95 € | 993,96 € | **72,0%** |
| 1995 | 1.105,72 € | 1.463,06 € | 75,6% |
| 2000 | 1.313,47 € | 1.726,10 € | 76,1% |
| 2005 | 1.794,08 € | 2.404,67 € | 74,6% |
| **2010** | 2.188,20 € | 2.741,56 € | **79,8%** |
| 2015 | 2.226,22 € | 2.735,22 € | 81,4% |
| 2020 | 2.482,65 € | 3.041,04 € | 81,6% |
| 2024 | 2.860,86 € | 3.365,12 € | 85,0% |
| **2025** | **3.012,97 €** | **3.505,62 €** | **85,9%** |

**El mínim de tota la sèrie és el desembre del 1967: 55,8%.** **El màxim és el
desembre del 2025: 85,9%.** **La bretxa passa de 44 punts a 14 en
cinquanta-vuit anys.**

## Tres coses que la sèrie ensenya i una que no

**La primera: la convergència no és una línia recta.** **Puja fins al 1970,
baixa set punts el 1975, torna a pujar fins al 2000, torna a baixar un punt i
mig fins al 2005** i **des del 2005 puja onze punts seguits.** **Els anys de més
creixement de l'economia andorrana no són els de més convergència.**

**La segona: els cinc últims anys són els de la correcció més ràpida des dels
setanta.** **Del 2020 al 2025 la relació passa de 81,6% a 85,9%: 4,3 punts en
cinc anys**, més del doble del ritme dels quinze anteriors.

**La tercera: la bretxa que queda són 492,65 euros al mes**, i **en euros no
segueix la mateixa corba que en percentatge.** **278 euros de diferència el
1990, 553 el 2010, 493 el 2025**: **creix vint anys i es redueix quinze**, i
**el 2025 encara és més gran que el 1990** tot i que la proporció ha millorat
catorze punts. **Que la relació pugi no vol dir que la distància es tanqui a la
mateixa velocitat.**

**I el que aquesta sèrie no diu**: **si la bretxa ve de cobrar menys pel mateix
o de treballar en altres llocs.** **És un salari mitjà de tots els assalariats
d'un mes, no un salari comparable a igual feina i igual jornada.** `La font no
publica ni les hores ni el tipus de contracte creuats amb el sexe, i sense això
la part de la bretxa que és de segregació i la part que és de retribució no es
poden separar.`

## La massa salarial, que diu una altra cosa

| Desembre de | Dones | Homes | **Part de les dones** |
| --- | ---: | ---: | ---: |
| 1990 | 7,71 M€ | 15,65 M€ | **33,0%** |
| 2000 | 21,30 M€ | 34,76 M€ | 38,0% |
| 2010 | 42,01 M€ | 57,12 M€ | 42,4% |
| **2025** | **70,46 M€** | **91,23 M€** | **43,6%** |

**Les dones cobren el 43,6% de tot el que Andorra paga en salaris el desembre
del 2025**, i **el 33,0% el 1990.** **Deu punts en trenta-cinc anys.**

**Aquesta xifra puja més a poc a poc que la del salari mitjà**, i **la
diferència entre les dues corbes és el nombre de dones assalariades**: **el
salari mitjà compara qui hi és, i la massa salarial compara quantes n'hi ha i
quant cobren alhora.**

## El que falta

- **Les hores treballades i el tipus de contracte per sexe**, sense els quals no
  es pot separar segregació de retribució.
- **La sèrie mensual sencera**, que la font té des del juliol del 1966 i que
  aquest bolcat només porta en desembres.
- **El salari mitjà per sector i sexe**, que el bolcat sí que porta, **però amb
  cel·les molt petites**: el desembre del 2025 la construcció dona **9.388,88 €
  de salari mitjà per a les dones**, que **amb poques assalariades al sector és
  una mitjana que no es pot citar sola.** `Requereix el nombre d'assalariades
  per sector per poder-la ponderar.`
- **Dues divisions que l'API no va servir**: **402 i 411**, els creuaments de
  massa salarial i salari mitjà per sector i edat, que van retornar `502`.
- **Per què la relació cau set punts entre el 1970 i el 1975.**

## Related

- [El treball](../treball/treball.md) — la sèrie d'assalariats, del mateix desembre del 1966.
- [La llei d'igualtat](./la-llei-digualtat.md) — la norma, i la conciliació mesurada.
- [La piràmide de prestigi](../immigracio/la-piramide-de-prestigi.md) — el mateix salari mitjà del desembre, per país d'origen.
- [El salari mínim, de 362 pessetes a 9,05 euros](../treball/el-salari-minim-de-362-pessetes-a-9-euros.md)
- [El sufragi femení](./el-sufragi-femeni.md)
