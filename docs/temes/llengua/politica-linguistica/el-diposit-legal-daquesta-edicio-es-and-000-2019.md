---
type: article
title: El dipòsit legal d'aquesta edició és AND. 000-2019
description: "La sisena onada de l'enquesta sociolingüística es va publicar amb el dipòsit legal i l'ISBN sense omplir, marcats en vermell. I el seu gràfic de l'indicador contradiu el text de la seva pròpia pàgina."
tema: temes/llengua/politica-linguistica
veu: compilada
epoca: contemporania
apte_llengua: false
font: spl-coneixements-usos-linguistics-2018
timestamp: 2026-09-15T18:00:00Z
tags: [llengua, sociolinguistica, dades, metodologia, serie-historica, discrepancia, verificacio, prioritari]
---

# El dipòsit legal d'aquesta edició és AND. 000-2019

## La unitat llegida

***Coneixements i usos lingüístics de la població d'Andorra. Situació actual i
evolució (1995-2018)***, **44 pàgines**. **Sisena onada.** L'estudi el fa el
**Centre de Recerca Sociològica de l'Institut d'Estudis Andorrans** per encàrrec
del **Servei de Política Lingüística**; **la presentació la signa Sílvia Riva
González, ministra de Cultura i Esports**
([fitxa](../../../fonts/spl-coneixements-usos-linguistics-2018.md)).

**Era l'última peça del fons de l'enquesta que el corpus no havia obert**: en
tenia **només la pàgina 32**, llegida per arbitrar una discrepància
([la sèrie que no és una sèrie](./la-serie-que-no-es-una-serie.md)). **Ara està
llegida sencera**, amb verificació sobre pàgina renderitzada, i **una part fins a
400 ppp**.

## El que hi ha a la pàgina de crèdits

**No es pot citar aquesta edició per l'ISBN ni pel dipòsit legal, perquè no en
té.** La pàgina de crèdits imprimeix:

> Servei de Política Lingüística · Govern d'Andorra
> Estudi: Centre de Recerca Sociològica de l'Institut d'Estudis Andorrans
> Impressió: Impremta Solber
> **Dipòsit legal: AND. 000-2019**
> **ISBN: 978-99920-0-000-0**

**Les dues últimes línies són plantilla sense omplir.** `AND. 000-2019` i
`978-99920-0-000-0` **no són números: són el forat on havien d'anar.**

**I es veu que ningú no els va omplir perquè encara hi ha la marca.** **Aquelles
dues línies estan impreses en vermell** i **tota la resta de la pàgina en negre**.
`Comprovat sobre la pàgina renderitzada a 150 ppp.` **És el color amb què un
taller marca el que falta**, i **va sortir imprès així.**

### Què vol dir això, en pràctica

**Les tres altres edicions del fons es poden identificar per un número que no
depèn de ningú**: 1995-2009, **AND. 908-2011**; 1995-2014, **AND. 188-2016**;
1995-2022, **AND. 361-2023**. **Aquesta, no.**

**Els únics identificadors estables que té són l'URL del portal, el contingut i
el hash del fitxer.** El corpus la cita **per títol, any d'onada i pàgina**, i
**registra el SHA-256 a la fitxa de font**.

> **I hi ha una segona incoherència a la mateixa obertura.** **La pàgina de
> crèdits diu «Centre de Recerca Sociològica»**; **la presentació de la ministra,
> dues pàgines més enllà, diu «Centre de Recerca i Estudis Sociològics»**. **Dos
> noms per al mateix organisme en el mateix llibret.** El corpus **no arbitra** i
> **cita el de la pàgina de crèdits**, que és el que les altres tres edicions
> repeteixen.

## El gràfic que contradiu el text de la seva pròpia pàgina

**El corpus tenia aquesta discrepància registrada des de l'edició del 2022, i hi
havia deixat una suposició**: *«El mateix gràfic surt igual a l'edició del 2018,
de manera que l'error ve d'abans i s'ha reimprimit»*
([la sèrie que no és una sèrie](./la-serie-que-no-es-una-serie.md)). **Es va
escriure havent llegit el text d'aquella pàgina i no el dibuix.**

**Ara el dibuix està vist.** **La suposició era correcta.**

**El text de la pàgina impresa 32 diu:**

> «L'indicador lingüístic del **català** el 2018 és de **56,8**, un punt menys
> respecte del 2014. L'indicador lingüístic del **castellà** és de **57,6**, una
> mica més d'un punt en comparació de l'enquesta anterior.»

I, a la columna del costat:

> «després que el **2014 el català avancés el castellà per primera vegada des del
> 1995**, **la tendència s'ha tornat a invertir**.»

**El gràfic de la mateixa pàgina dibuixa una altra cosa.** La llegenda assigna
**verd al català i morat al castellà**. `Verificat a 400 ppp sobre el tram
2009-2018.`

| Any | Línia de dalt | Línia de baix |
| --- | --- | --- |
| 1995-2009 | **morat** (castellà) | verd (català) |
| **2014** | **verd** (català), **57,7** | morat (castellà), **56,4** |
| **2018** | **verd** (català), **57,6** | morat (castellà), **56,8** |

**El gràfic dibuixa el creuament del 2014 i no dibuixa el de tornada.** **Al
2018 el verd segueix a dalt**, de manera que **assigna al català el 57,6 i al
castellà el 56,8**, **exactament al revés del text que té a sobre** i **al revés
de la frase que diu que la tendència s'ha invertit**.

**Aquest és el gràfic que l'edició del 2022 reimprimeix**, i **és l'única figura
sobre la qual aquella edició construeix la seva conclusió principal.** **L'error
neix aquí, l'any 2019, i es reimprimeix el 2023.**

### Arbitrat el 18-09-2026: el text tenia raó i el gràfic no

**El corpus ho havia deixat registrat i no arbitrat.** **L'API pública del
Departament d'Estadística el resol**, amb les divisions **1971 i 1972**, font
declarada **Departament de Política Lingüística**:

| Indicador lingüístic | 1995 | 1999 | 2004 | 2009 | 2014 | **2018** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Català** | **56,3** | 53,9 | 48,5 | 48,2 | **57,7** | **56,8** |
| **Castellà** | 50,0 | **58,2** | **60,8** | **59,1** | 56,4 | **57,6** |
| Francès | 18,5 | 17,9 | 18,5 | 16,7 | 14,5 | 16,9 |
| Portuguès | 7,3 | 8,5 | 11,4 | 15,3 | 13,9 | 13,9 |

**El 2018 el català és 56,8 i el castellà 57,6**, tal com diu **el text** de la
publicació. **El gràfic està equivocat**, i amb ell **la conclusió principal de
l'edició del 2022 que s'hi basa.**

**I la sèrie sencera diu una cosa que ni el text ni el gràfic no diuen.** El
creuament no és un: **n'hi ha tres.**

| Període | Qui va davant |
| --- | --- |
| **1995** | **català**, per 6,3 punts |
| **1999-2009** | **castellà**, i la distància arriba a **12,3 punts el 2004** |
| **2014** | **català**, per 1,3 punts |
| **2018** | **castellà**, per 0,8 punts |

**El 2004 i el 2009 són el sòl del català** —**48,5 i 48,2**— i **el 2014 és el
sostre de tota la sèrie, 57,7**. **La imatge d'una caiguda contínua és falsa:
el que hi ha és una caiguda fins al 2009, una recuperació forta el 2014 i un
retrocés petit el 2018.**

`Els valors 48,5 (2004) i 57,7 (2014) coincideixen exactament amb els que
aquesta fitxa havia llegit del gràfic i de l'edició del 2011. La font de l'API
és la mateixa que la de la publicació; no és una comprovació independent, però
sí que és la sèrie sense passar per cap figura.`

## Una xifra reproduïda que no és la impresa: 75,4 contra 77,5

**Aquesta edició dona, per a la seva pròpia onada, valors que l'edició del 2022
no reprodueix bé.**

| Si s'adreça a algú en català i li respon en castellà… | **Edició de 2018** | **Reproduït a l'edició de 2022** |
| --- | ---: | ---: |
| **Continua en castellà** | **75,4 %** | **77,5 %** |
| **Segueix en català** | **19,2 %** | **19,4 %** |
| Interromp la conversa | 1,1 % | 1,1 % |
| Demana si li poden parlar en català | 3,5 % | 3,5 % |
| Mai s'adreça a ningú en català | 10,8 % | 10,8 % |
| No contesta | 3,0 % | 3,0 % |

**Quatre files idèntiques i dues que no.** **La més gran, 2,1 punts.**

**I el text d'aquesta edició sosté el seu propi número**: «el percentatge ha
passat **del 65,5 % al 75,4 %**». **Ho diu amb lletres, a la mateixa pàgina.**

> **I l'aritmètica hi afegeix una cosa més.** **Amb els valors d'aquesta edició,
> les quatre opcions d'acció sumen 99,2**; **amb els que en reprodueix l'edició
> del 2022, sumen 101,5.** `Comprovació del corpus.`
>
> **Això confirma la hipòtesi que el corpus havia deixat marcada una tanda
> abans**: **a les onades del 2014 endavant, les quatre accions es calculen sobre
> el subgrup que s'adreça en català, i per això sumen prop de 100** — **la base
> que l'edició del 2009 imprimeix en lletres**
> ([quaranta-vuit coma cinc, no quaranta-vuit coma sis](./quaranta-vuit-coma-cinc-no-quaranta-vuit-coma-sis.md)).
> **La columna original del 2018 hi encaixa; la reproduïda, no.**

**La sèrie, amb el valor original del 2018:**

| Qui continua en castellà, sobre els qui s'adrecen en català | 2009 | 2014 | **2018** | 2022 |
| --- | ---: | ---: | ---: | ---: |
| | **79,4 %** | 78,2 %* | **75,4 %** | **74,8 %** |

`*El 2014 és rebasat pel corpus; els altres tres són valors impresos a la seva
edició original.` **Baixa quatre onades seguides, sense un sol sotrac.**

## La ruptura de sèrie que l'informe declara, i el que això fa a una conclusió del corpus

**Les conclusions d'aquesta edició diuen una cosa que canvia com s'ha de llegir
la sèrie de l'Administració pública:**

> «En aquesta enquesta **s'hi han afegit àmbits com l'Hospital i els centres
> d'atenció primària**. **Això ha fet baixar els percentatges d'ús del català
> –que, per tant, no són del tot comparables amb els dels estudis anteriors**–,
> però les dades permeten comprovar una presència inferior del català en el
> sector de la salut respecte d'altres àmbits de l'Administració pública.»

**El corpus té, com a titular, que el 2022 «l'atenció exclusiva en català a
l'Administració és la més baixa de tota la sèrie històrica»**
([la sèrie que no és una sèrie](./la-serie-que-no-es-una-serie.md)), **posat al
costat del millor indicador de català des del 1995.**

**Aquesta frase l'obliga a matisar-se.** **Des del 2018, «Administració pública»
inclou la sanitat**, que és el sector on el mateix informe diu que el català és
menys present. **Una part de la caiguda és el canvi de perímetre**, i **la font
ho declara.** **El corpus no pot dir quina part**: el document no publica la
sèrie amb i sense els nous àmbits.

> **`Conclusió del corpus`**: **el mínim històric de l'atenció en català a
> l'Administració es mesura sobre un àmbit més ample que el que el va precedir**,
> i **així s'ha de citar**. **No es retira el fet; se li posa la vora.**

## La base del 64 % que el corpus va publicar fa una tanda

**Aquesta edició dona la xifra que la del 2014 no imprimia enlloc.**

> «augmenta el percentatge d'enquestats que fa **menys de cinc anys** que viuen al
> país (**del 4 % el 2014 al 13 % el 2018**)»

**El 2014, el segment dels arribats feia menys de cinc anys era el 4 % d'una
mostra de 727**: **unes 29 persones**. `Càlcul del corpus.`

**El corpus va publicar fa una tanda** que el 2014 **el 64,1 % d'aquell segment
tenia el català com a única llengua materna, contra el 33,3 % dels nascuts a
Andorra**
([els nouvinguts tenien més català que els nascuts a Andorra](./els-nouvinguts-tenien-mes-catala-que-els-nascuts-a-andorra.md)).
**El fet no canvia i la seva precisió sí**: **aquell 64,1 % són uns dinou d'uns
vint-i-nou**, en una enquesta el marge de la qual —± 3,69 %— **està calculat per
al conjunt i no per a un segment de vint-i-nou persones.**

**El 2018 el mateix segment ja és el 13 % de 742, unes 96 persones.**
`Càlcul del corpus.`

> **Avís de formulació:** **l'edició del 2018 diu «menys de cinc anys» i el gràfic
> del 2014 diu «5 o menys».** **No és exactament el mateix tall**, i el corpus
> **dona la base com un ordre de magnitud, no com un recompte.**

## La fitxa tècnica de la sisena onada

| | **2018** |
| --- | --- |
| **Grandària de la mostra** | **742 persones** |
| **Marc de mostreig** | **«els telèfons fixos i mòbils possibles que hi ha a Andorra»** — **ja no la guia** |
| **Selecció** | quotes de sexe; **ponderació** per nacionalitat i edat |
| **Marge d'error** | **± 3,65 %**, probabilitat **95,5 %** |
| **Tipus d'entrevista** | telefònica, 20/25 minuts |
| **Treball de camp** | **19 de setembre – 19 d'octubre del 2018** |
| **Enquestadors** | **13** |

**Dos canvis, i els dos són els que el corpus tenia registrats sense edició ni
data:**

1. **El marc passa de la guia telefònica a tots els números possibles del país.**
   **La guia excloïa qui no hi sortia**; això ja no. **El canvi és entre el 2014
   i el 2018**, i **és aquesta edició la que el declara.**
2. **El treball de camp torna al setembre-octubre** després de dues onades al
   maig. **La sèrie fa, doncs: tardor, tardor, tardor, primavera, primavera,
   tardor** — i el 2022, primavera altra vegada.

## El que es confirma sense novetat

| Sèrie, valors del 2018 | Edició original | El que el corpus tenia |
| --- | ---: | ---: |
| Llengua materna **catalana** | 35,7 % | 35,7 % ✓ |
| Llengua materna **castellana** | 43,2 % | 43,2 % ✓ |
| Llengua materna **portuguesa** | 17,1 % | 17,1 % ✓ |
| Llengua materna **francesa** | 8,9 % | 8,9 % ✓ |
| Indicador lingüístic **català** | 56,8 | 56,8 ✓ |
| Indicador lingüístic **castellà** | 57,6 | 57,6 ✓ |
| **Comença sempre en català** | 41,9 % | 41,9 % ✓ |

**I el 48,6 del 2004 hi torna a ser**, com a la del 2016 i a la del 2023.
**Tres reimpressions del valor que l'edició del 2011 dona com a 48,5.**

## L'annex d'assalariats, allargat fins al 2017

**Aquesta edició reprodueix l'annex del Departament d'Estadística amb set anys
nous.** **Els tres anys que se solapen amb l'edició del 2014 són idèntics.**
`Comprovació del corpus: 2011 = 37.301, 2012 = 35.777, 2013 = 35.039 a les dues.`

| | 2007 | 2013 | 2017 |
| --- | ---: | ---: | ---: |
| **Total assalariats** | **42.210** | **35.039** | **37.705** |

> **La caiguda: −7.171, el −17,0 %, del 2007 al 2013.**
> **La recuperació: +2.666, el +7,6 %, del 2013 al 2017.**
> **Deu anys després, encara 4.505 assalariats per sota del 2007: el −10,7 %.**
> `Càlcul del corpus.`

**I la construcció no torna.** **15,5 % el 2007 → 8,0 % el 2013 → 7,6 % el
2017**; en persones, **≈ 6.543 → ≈ 2.803 → ≈ 2.866**. **De cada cinc llocs de
treball de la construcció del 2007, el 2017 en quedaven dos.**

**El que creix ocupant el lloc** són **activitats immobiliàries i serveis
empresarials**: del **10,8 %** el 2011 al **13,2 %** el 2017, **≈ 4.029 → ≈
4.977 persones**, **el sector que més guanya de tota la taula.**

## El capítol d'usos lingüístics, destil·lat valor a valor

**Disset pàgines de gràfics apilats** (impreses 15-31). **Llegides sobre la
pàgina renderitzada a 200 ppp**, no sobre la capa de text
(`docs/raw/llengua-usos-linguistics/pages-2018/`, **pàgina impresa = pàgina del
PDF − 2**). **El que segueix són les xifres tal com les imprimeix el document.**

### Primer: el capítol no té UNA sèrie, en té tres

**Abans de cap xifra, el que cal saber per no construir sèries falses.** **El
capítol canvia el conjunt d'onades segons la pregunta**, i **ho fa sense
advertir-ho**:

| Conjunt d'onades | Preguntes que el fan servir |
| --- | --- |
| **Sis** (1995·1999·2004·2009·2014·2018) | a casa, amb els amics, a la feina, indicador d'ús, Administració, i els nou àmbits socioeconòmics |
| **Quatre** (2004·2009·2014·2018) | percentatge de temps que utilitza cada llengua |
| **Tres** (2009·2014·2018) | parella, fills, fills entre ells |
| **Dues** (2014·2018) | companys d'estudis |

**Qui llegeixi el capítol de pressa donarà per fet que totes les sèries comencen
el 1995.** **Quatre de les seves preguntes no existien encara.**

### Percentatge de temps que utilitza cada llengua (p. 15)

| Llengua | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: |
| **Català** | 40,5 | 42,1 | **47,0** | 45,9 |
| **Castellà** | **43,0** | 41,5 | 37,5 | 39,1 |
| Francès | 7,0 | 6,9 | 5,2 | 6,5 |
| Portuguès | 5,5 | 7,5 | 5,4 | 3,9 |
| Anglès | 1,2 | 1,0 | 2,1 | 3,2 |
| Altres | 1,7 | 1,0 | 0,8 | 0,7 |
| **Suma** | 98,9 | **100,0** | 98,0 | 99,3 |

**Dues coses que el text de la pàgina no diu.** **La primera**: **només la
columna del 2009 suma 100.** **La segona, i és la important**: **el màxim del
català en tota la sèrie és el 2014, no el 2018.** **Entre 2014 i 2018 el català
PERD 1,1 punts i el castellà en GUANYA 1,6**, i **la pàgina ho descriu com que
«el català manté la primera posició»**. **És cert i és incomplet.**

### A casa (p. 16) — les dues preguntes, sis onades

**Llengües en què parla a casa:**

| | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sempre català | **41,2** | 31,9 | 25,4 | 26,2 | 33,9 | 29,3 |
| Sempre castellà | 20,5 | 26,8 | 28,4 | **28,9** | 26,9 | 24,4 |
| Català i castellà | 13,2 | 14,9 | 14,4 | 12,9 | 11,7 | **16,8** |
| Sempre francès | 5,2 | 4,6 | 4,3 | 3,8 | 2,3 | 4,1 |
| Sempre portuguès | 4,6 | 6,6 | 7,3 | 9,4 | **12,1** | 8,6 |
| Altres situacions | 15,3 | 15,2 | **20,2** | 18,9 | 13,1 | 16,8 |

**Llengua més utilitzada a casa:**

| | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Català | **46,9** | 37,9 | 31,1 | 29,9 | 37,5 | 33,9 |
| Castellà | 29,5 | 34,2 | **39,4** | 36,0 | 30,7 | 30,4 |
| Català = castellà | 3,6 | 5,6 | 3,9 | 6,5 | 6,0 | **9,0** |
| Francès | **6,8** | 6,3 | 6,1 | 5,9 | 3,2 | 4,3 |
| Portuguès | 6,7 | 8,2 | 12,2 | 14,3 | **14,4** | 10,0 |
| Altres situacions | 6,7 | 7,8 | 7,3 | 7,5 | 7,9 | **12,5** |

**Aquestes dues taules sumen 100 a totes les onades** (amb decimals d'arrodoniment
de ±0,3). **Són les sèries més netes del capítol.**

**La prosa de la pàgina arrodoneix sistemàticament cap amunt i el corpus ho
registra**: diu **«34%»** on el gràfic imprimeix **33,9**, **«27%»** on
imprimeix **26,9**, **«17%»** on imprimeix **16,8**. **Cap d'aquests
arrodoniments no altera cap conclusió**, però **qui citi el text en comptes del
gràfic estarà citant xifres que el document no ha mesurat.**

### Transmissió generacional (pp. 17-18) — només tres onades

**Amb la parella** (multiresposta, per això suma més de 100):

| | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: |
| Català | 35,1 | **43,6** | 43,4 |
| Castellà | **48,2** | 38,4 | 47,9 |
| Francès | 8,8 | 6,4 | 8,8 |
| Portuguès | **17,6** | 14,3 | 11,4 |
| Altres | 5,5 | 5,0 | 3,6 |

**Amb els fills** (multiresposta):

| | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: |
| Català | 47,0 | 51,7 | **55,3** |
| Castellà | **43,1** | 38.8 | 39,3 |
| Francès | **12,4** | 7,5 | 10,1 |
| Portuguès | **21,3** | 15,0 | 13,4 |
| Altres | 3,3 | 4,3 | 3,1 |

**Els fills entre ells** (multiresposta):

| | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: |
| Català | 65,3 | **71,9** | 61,7 |
| Castellà | **44,2** | 39,1 | 37,7 |
| Francès | **15,1** | 10,2 | 10,7 |
| Portuguès | **13,1** | 8,0 | 8,1 |
| Altres | 2,5 | 2,0 | 1,7 |

> **Una errata tipogràfica de la font, registrada perquè és una xifra:** el valor
> del castellà amb els fills el 2014 s'imprimeix **`38.8%`, amb punt decimal**,
> mentre **tots els altres valors de la pàgina fan servir coma**. **És l'única
> del capítol.**

**I aquí hi ha el fet que el capítol no comenta.** **El document titula la secció
«transmissió lingüística generacional» i conclou que és «favorable al català».**
**Ho és en una direcció i no en l'altra:**

| Direcció | 2014 | 2018 | Variació |
| --- | ---: | ---: | ---: |
| **Pares → fills** (català) | 51,7 | 55,3 | **+3,6** |
| **Fills ↔ fills** (català) | 71,9 | 61,7 | **−10,2** |

**Els pares transmeten més català que fa quatre anys i els germans en parlen
deu punts menys entre ells.** **La pàgina dona les dues xifres i només
n'interpreta una.** **El català segueix sent, amb diferència, la llengua més
usada entre germans** —61,7 % contra 37,7 % del castellà—, **però és l'única
sèrie del capítol que cau deu punts en una sola onada.**

### Amb els amics (p. 19)

**Llengües en què parla amb els amics:**

| | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sempre català | **33,8** | 21,6 | 23,5 | 22,4 | 27,6 | 25,4 |
| Sempre castellà | 16,3 | 17,5 | 28,6 | **30,4** | 24,8 | 19,3 |
| Català i castellà | 23,7 | **29,4** | 19,5 | 19,8 | 23,4 | 26,7 |
| Sempre francès | **4,6** | 1,9 | 3,2 | 2,8 | 1,4 | 2,2 |
| Sempre portuguès | 2,8 | 2,3 | 2,6 | **5,2** | 2,8 | 2,1 |
| Altres situacions | 18,8 | **27,3** | 22,6 | 19,5 | 19,8 | 24,2 |

**Llengua més utilitzada amb els amics:**

| | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Català | **45,5** | 37,5 | 34,0 | 30,1 | 42,1 | 37,9 |
| Castellà | 24,5 | 29,4 | **41,6** | 38,0 | 31,8 | 31,6 |
| Català = castellà | 11,2 | **13,7** | 5,7 | 10,5 | 8,2 | **13,7** |
| Francès | **6,0** | 4,3 | 5,7 | 3,8 | 2,5 | 2,6 |
| Portuguès | 4,1 | 4,9 | 6,2 | **7,7** | 5,4 | 4,6 |
| Altres situacions | 8,8 | **10,2** | 6,8 | 9,8 | 9,5 | 9,7 |

> **Un error d'aritmètica a la prosa de la font.** La pàgina escriu que els que
> usen igual el català i el castellà amb els amics **«augmenten gairebé cinc
> punts (del 8% al 13,7%)»**. **El gràfic dona 8,2 → 13,7**, que són **5,5
> punts**. **Amb la xifra arrodonida que la mateixa frase fa servir, 8 → 13,7,
> en són 5,7.** **Per cap de les dues vies no és «gairebé cinc»: és més de
> cinc.** **La font subestima el seu propi resultat.**

**I el 2018 passa una cosa que el capítol no assenyala**: **«català i castellà»
(26,7 %) supera «sempre català» (25,4 %).** **Només havia passat el 1999.**

### A la feina (pp. 20-21), i la columna que no suma 100

**Llengües en què parla a la feina:**

| | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sempre català | 32,3 | 27,3 | 23,5 | 29,2 | 30,7 | **33,4** |
| Sempre castellà | 21,3 | **27,1** | 24,4 | 24,4 | 21,2 | 18,1 |
| Català i castellà | 26,6 | 24,6 | **31,2** | 25,4 | 28,1 | 24,2 |
| Sempre francès | 3,3 | 2,5 | **4,0** | 2,0 | 1,3 | 1,6 |
| Altres situacions | 16,5 | 18,5 | 16,9 | **18,9** | 17,6 | 17,8 |
| **Suma** | 100,0 | 100,0 | 100,0 | 99,9 | 98,9 | **95,1** |

**La columna del 2018 suma 95,1.** **No és un error de lectura ni d'impressió**:
**el text de la pàgina ho diu** —«*si bé en l'enquesta actual hi ha un **5%** que
no han contestat la pregunta*»— **i el gràfic no ho dibuixa.** **Conseqüència
pràctica**: **els percentatges del 2018 d'aquesta pregunta estan calculats sobre
una base diferent de la de les altres onades**, i **comparar-los directament
infla la caiguda del castellà i desinfla la pujada del català.** **El 33,4 % de
«sempre català» del 2018 val, sobre base comparable, uns 35 %.**

**Llengua més utilitzada a la feina — relacions INTERNES** (és el gràfic al qual
es refereix la prosa de la pàgina 20):

| | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Català | **48,2** | 38,8 | 37,9 | 38,2 | 43,4 | 43,0 |
| Castellà | 31,5 | 37,9 | **42,4** | 36,4 | 32,1 | 27,0 |
| Català = castellà | 7,3 | 10,8 | 6,7 | 10,0 | 9,0 | **12,1** |
| Francès | **6,2** | 4,5 | 5,9 | 4,2 | 2,0 | 1,9 |
| Altres situacions | 6,8 | 8,0 | 7,1 | 11,3 | **12,4** | 11,2 |
| **Suma** | 100,0 | 100,0 | 100,0 | 100,1 | 98,9 | **95,2** |

**Llengua més utilitzada a la feina — relacions EXTERNES** (clients i proveïdors):

| | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Català | 46,6 | 32,3 | 46,9 | 45,1 | 38,7 | **51,8** |
| Castellà | 28,8 | 24,6 | **34,5** | 29,8 | **11,3** | 24,8 |
| Català = castellà | 10,2 | 26,5 | 11,2 | 11,4 | **27,5** | 13,3 |
| Francès | **7,3** | 6,8 | 2,7 | 5,2 | 1,2 | 0,7 |
| Altres situacions | 7,1 | 9,8 | 4,8 | 8,5 | **20,5** | 9,2 |
| **Suma** | 100,0 | 100,0 | 100,1 | 100,0 | 99,2 | 99,8 |

> **La columna del 2014 d'aquesta última taula no s'ha de llegir com un fet
> social.** **Tres de les seves cinc categories són molt fora de la tendència de
> totes les altres onades**: el **castellà cau a 11,3** quan val 29,8 abans i
> 24,8 després —**menys de la meitat de les dues veïnes**—, mentre **«català =
> castellà» puja a 27,5** (d'11,4 a 13,3 a les veïnes) i **«altres situacions» a
> 20,5** (de 8,5 a 9,2). **El que sembla que va passar el 2014 és que una part
> del que abans i després es codifica com a «castellà» es va codificar com a
> «totes dues» o «altres».** **El document no declara cap canvi de codificació**,
> i **el corpus no pot demostrar-lo**: `requereix la metodologia de l'onada del
> 2014`. **Però qualsevol sèrie que travessi aquesta columna dibuixarà un
> col·lapse i una recuperació del castellà que probablement no van existir.**

### L'indicador d'ús (p. 22), amb la seva fórmula

**El document en dona la definició en nota**, i **el corpus la reté perquè és el
que fa la xifra interpretable**:

> **Indicador d'ús = (freqüència d'ús a casa + freqüència d'ús amb els amics +
> freqüència d'ús a la feina en les relacions internes) / 3**

**Escala d'1 (gens) a 5 (molt).**

| Llengua | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Català** | **3,4** | 3,2 | 2,9 | 2,9 | 3,2 | 3,2 |
| **Castellà** | 2,7 | 3,1 | **3,2** | **3,2** | 3,0 | 3,0 |
| Francès | 1,4 | 1,4 | 1,4 | 1,4 | 1,3 | 1,3 |
| Portuguès | 1,3 | 1,3 | 1,4 | **1,5** | **1,5** | 1,4 |

**Aquesta taula dibuixa dos creuaments, i tots dos són llegibles a la xifra:**

1. **Entre 1999 i 2004 el castellà passa davant del català** (2,9 contra 3,2).
2. **Entre 2009 i 2014 el català el torna a passar** (3,2 contra 3,0), **i el
   2018 la distància es manté.**

**Compte amb confondre aquest indicador amb l'altre.** **Aquest és l'*indicador
d'ús*, escala 1-5, pàgina impresa 22, i cobreix tres àmbits.** **El de la
[pàgina 32](#el-gràfic-que-contradiu-el-text-de-la-seva-pròpia-pàgina) és
l'*indicador lingüístic*, escala 0-100, i és un altre càlcul.** **Són dues
figures diferents del mateix llibret**, i **el defecte de dibuix que aquest
article documenta és el de la 32, no el de la 22.**

### Companys d'estudis (p. 23), i per què aquesta taula no s'ha de citar

| | 2014 | 2018 |
| --- | ---: | ---: |
| Català | **63,0** | 51,6 |
| Castellà | 17,6 | **31,0** |
| Francès | 5,5 | 6,5 |
| Català/castellà | 8,8 | 1,7 |
| Altres | 5,1 | 9,2 |

**Sembla el moviment més violent de tot el capítol** —**el català perd 11,4
punts i el castellà en guanya 13,4 en quatre anys**— i **el corpus adverteix que
probablement no ho és.** **La nota 8 de la pàgina diu que la pregunta només es
va fer a qui seguia estudis en aquell moment, `N=112`.**

**Amb 112 respostes, el marge d'error al 95 % de confiança és d'uns ±9 punts.**
**Tots dos moviments hi són a prop, i el del català hi cau a dins.** **El
document presenta la xifra sense cap advertiment de base** i **escriu «El català
baixa 10 punts respecte del 2014 i el castellà puja 14 punts» com si fos un fet
mesurat.** **El corpus el registra com el que és: un senyal dins del soroll.**

### L'Administració pública (p. 24), i el buit prioritari del corpus

**Dotze columnes: sis onades × dues preguntes** —**en quina llengua PARLA** l'usuari
i **en quina l'ATENEN**.

| Sempre català | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Parla** | 72,7 | 69,7 | 64,0 | 70,1 | **80,6** | 61,6 |
| **L'atenen** | 80,5 | 82,9 | 74,7 | 82,2 | **91,5** | 62,2 |

| 2018, desglossat | Parla | L'atenen |
| --- | ---: | ---: |
| Sempre català | 61,6 | 62,2 |
| Sempre castellà | 11,6 | 2,6 |
| Català i castellà | 22,6 | 31,5 |
| Altres situacions | 4,1 | 3,7 |

**El document declara el canvi de perímetre i el corpus el transcriu literal:**

> «per valorar aquesta evolució s'ha de tenir en compte que en aquesta enquesta
> es va preguntar pels usos **als CAP i l'Hospital**, que **no s'havien inclòs en
> els estudis anteriors**.»

**El buit que el corpus tenia obert** —quina part de la caiguda és el canvi de
perímetre— **segueix obert, i ara se sap exactament per què**: **el document no
publica la sèrie sense els nous àmbits**, i **sense el desglossament per àmbit
no es pot fer cap repartiment.** `Requereix les taules per àmbit de l'onada del
2018.`

**El que sí que queda establert, i canvia com s'ha de llegir el titular:** **la
caiguda de 29,3 punts es mesura contra el 91,5 % del 2014, que és el valor més
alt de tota la sèrie 1995-2018.** **Contra la mitjana de les quatre onades
anteriors (80,1 %), la caiguda del 2018 és d'uns 18 punts, no de 30.** **Trenta
punts és cert i tria la base més favorable a la mida del titular.**

### Els nou àmbits socioeconòmics (pp. 25-31)

**Contextos preguntats**: metge generalista, metge especialista, grans
magatzems, restaurant, transport públic (autobús i taxi), botigues, bar/pub/
discoteca, banc/assegurances/gestoria, i perruqueria/barberia.

**«Sempre català», l'atenen — les nou sèries completes:**

| Àmbit | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Banc / assegurances / gestoria | 72,0 | 74,6 | 73,4 | 77,7 | **84,5** | 78,3 |
| Administració pública | 80,5 | 82,9 | 74,7 | 82,2 | **91,5** | 62,2 |
| Metge (generalista/especialista) | 56,0 | 53,4 | 54,0 | 53,8 | **66,9** | 46,3 |
| Botiga | 36,0 | 26,0 | 24,4 | 50,0 | **51,8** | 40,5 |
| Perruqueria / barberia | **42,4** | 36,3 | 31,1 | 32,1 | 42,0 | 32,3 |
| Restaurant | 34,8 | 30,0 | 21,2 | 25,0 | **35,5** | 22,7 |
| Taxi / autobús | **29,4** | 24,7 | 18,2 | 26,0 | 20,4 | 20,2 |
| Bar / pub / discoteca | **24,8** | 22,9 | 15,3 | 13,9 | 17,2 | 16,3 |
| Grans magatzems | 12,4 | 9,6 | 9,3 | 5,5 | **15,1** | 8,6 |

**I les mateixes nou, en què PARLA l'enquestat:**

| Àmbit | 1995 | 1999 | 2004 | 2009 | 2014 | 2018 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Banc / assegurances / gestoria | 67,2 | 67,8 | 66,4 | 69,6 | **76,7** | 74,0 |
| Administració pública | 72,7 | 69,7 | 64,0 | 70,1 | **80,6** | 61,6 |
| Metge | 57,6 | 50,4 | 49,6 | 51,1 | **65,7** | 46,5 |
| Botiga | 46,0 | 27,4 | 25,5 | 48,7 | **53,5** | 42,3 |
| Perruqueria / barberia | **42,7** | 36,9 | 30,7 | 33,7 | 42,2 | 33,4 |
| Restaurant | 38,2 | 29,3 | 22,1 | 29,9 | **36,2** | 28,4 |
| Taxi / autobús | **34,9** | 26,2 | 19,9 | 34,3 | 29,5 | 27,8 |
| Bar / pub / discoteca | **33,2** | 23,6 | 16,7 | 20,4 | 26,0 | 20,8 |
| Grans magatzems | 29,2 | 13,3 | 10,4 | 18,3 | 17,3 | **18,3** |

> **El fet que el capítol no diu en cap moment, i que només es veu posant les
> nou sèries juntes.** **El 2014 és el màxim de tota la sèrie 1995-2018 en sis
> dels nou àmbits** —Administració, banc, metge, botiga, restaurant i grans
> magatzems— **i està a quatre dècimes del màxim en un setè** (perruqueria).
> **I el 2018 baixa en els nou.**
>
> **El document explica DOS d'aquests descensos amb canvis de disseny declarats**
> —**els CAP i l'Hospital afegits a l'Administració**, i **«metge i dentista»
> substituït per «metge generalista i especialista»**—, **i no n'explica cap
> dels altres set.** **El banc i la gestoria no tenen cap canvi declarat i el
> seu màxim també és el 2014.**
>
> **El corpus no pot dir què va passar**, i **no dirà que el 2014 fos una onada
> defectuosa**: `requereix la metodologia i el treball de camp de l'onada del
> 2014`. **El que sí que registra és la regla de lectura**: **qualsevol sèrie
> d'aquest fons que prengui el 2014 com a base de comparació exagerarà la
> caiguda del català**, **perquè el 2014 és, en gairebé tots els àmbits, el
> punt més alt que s'ha mesurat mai.**

**La segona cosa que només es veu amb les dues taules al costat.** **Restant
«l'atenen» menys «parla» per al 2018 surt una escala neta de quins sectors
poden respondre en català:**

| Àmbit, 2018 | Parla | L'atenen | Diferència |
| --- | ---: | ---: | ---: |
| Banc / assegurances / gestoria | 74,0 | 78,3 | **+4,3** |
| Administració pública | 61,6 | 62,2 | **+0,6** |
| Metge | 46,5 | 46,3 | −0,2 |
| Taxi / autobús | 27,8 | 20,2 | −7,6 |
| Botiga | 42,3 | 40,5 | −1,8 |
| Perruqueria / barberia | 33,4 | 32,3 | −1,1 |
| Bar / pub / discoteca | 20,8 | 16,3 | −4,5 |
| Restaurant | 28,4 | 22,7 | −5,7 |
| Grans magatzems | 18,3 | 8,6 | **−9,7** |

**On la xifra és positiva, el sector respon en català a gent que no l'hi ha
parlat**: **la banca i l'Administració.** **On és molt negativa, hi ha gent que
parla en català i rep resposta en una altra llengua**: **els grans magatzems,
amb gairebé deu punts, i el restaurant i el taxi.** **És, literalment, el mapa
de quins taulells poden contestar en català.**

**I el signe d'on va la llengua al comerç**: **el 2018 «altres situacions» en
l'atenció arriba al 21,6 % al taxi i autobús i al 20,0 % als grans magatzems**
—**de 9,5 % i 13,9 % el 2014**—, **mentre a la resta d'àmbits es queda entre el
3 % i l'11 %.** **Són els dos únics àmbits on una cinquena part de l'atenció ja
no és ni en català ni en castellà.**

**Les altres set taules socioeconòmiques, completes** (sempre català / sempre
castellà / català i castellà / altres situacions, en el format
`parla → l'atenen` del 2018):

| Àmbit, 2018 | Sempre cat. | Sempre cast. | Cat. i cast. | Altres |
| --- | --- | --- | --- | --- |
| Banc / gestoria | 74,0 → 78,3 | 16,6 → 9,3 | 6,0 → 9,1 | 3,4 → 3,3 |
| Metge | 46,5 → 46,3 | 22,2 → 18,8 | 24,0 → 27,2 | 7,3 → 7,7 |
| Botiga | 42,3 → 40,5 | 26,3 → 21,9 | 27,2 → 32,2 | 4,2 → 5,4 |
| Restaurant | 28,4 → 22,7 | 30,3 → 28,1 | 34,5 → 37,8 | 6,8 → 11,4 |
| Perruqueria | 33,4 → 32,3 | 50,5 → 50,0 | 6,8 → 6,9 | 9,3 → 10,8 |
| Taxi / autobús | 27,8 → 20,2 | 49,3 → 42,5 | 16,0 → 15,7 | 6,9 → 21,6 |
| Bar / pub / discoteca | 20,8 → 16,3 | 41,6 → 39,9 | 30,6 → 31,9 | 7,0 → 11,9 |
| Grans magatzems | 18,3 → 8,6 | 38,8 → 38,7 | 37,1 → 32,7 | 5,8 → 20,0 |

**Tres lectures que el corpus reté d'aquesta taula.** **La primera**: **el
restaurant del 2018 és el primer àmbit de tota la sèrie on «català i castellà»
(37,8 % de l'atenció) és la categoria més gran**, per damunt de les dues
exclusives. **La segona**: **la perruqueria és l'àmbit més castellanitzat del
país** —**la meitat de l'atenció és sempre en castellà**— i **ho és de manera
estable des del 1999.** **La tercera**: **el bar i els grans magatzems són els
dos àmbits on l'atenció en català no ha superat mai el 25 % en cap onada des
del 1995.**

**Un contrast que el document dona i que val la pena retenir**: **per edat, com
més gran, MENYS català** als àmbits socioeconòmics —«*els més grans el fan
servir en un 80 % dels casos, mentre que els més joves en un 97 %*»—, i **per
anys de residència, els nascuts al país hi arriben al 99,5 %.** **Agregant els
nou àmbits en multiresposta**: **84 % fan servir el català, 92 % el castellà,
11 % el portuguès**, i **només el 6 % parla NOMÉS català en tots els àmbits**,
contra **un 64 % que fa servir català i castellà**.

### El que aquesta destil·lació deixa verificat

**Totes les afirmacions numèriques de la prosa del capítol s'han comprovat
contra el seu propi gràfic.** **Quadren totes menys una**, ja anotada: **el
«gairebé cinc punts» de la pàgina 19, que en són 5,5.** **Els arrodoniments de
la prosa són sistemàtics i cap no altera una conclusió.**

## Buits registrats

- **L'ISBN i el dipòsit legal reals d'aquesta edició, si existeixen.** **La
  pàgina de crèdits no en té**, i **el corpus no ha comprovat si figura a cap
  registre bibliogràfic.** `Requereix la Biblioteca Nacional d'Andorra.`
- ~~**Per què el gràfic de l'indicador no dibuixa el creuament del 2018**~~ —
  **`resolt` quant al fet el 18-09-2026**: **el gràfic està equivocat i el text
  té raó**, comprovat contra les divisions 1971 i 1972 de l'API d'Estadística
  («[Arbitrat el 18-09-2026](#arbitrat-el-18-09-2026-el-text-tenia-rao-i-el-grafic-no)»).
  `Per què s'hi va dibuixar malament, i si existeix cap fe d'errates, segueix
  obert. El corpus no ho ha comunicat a ningú.`
- **Quina part de la caiguda de l'atenció en català a l'Administració és el canvi
  de perímetre del 2018.** **`obert`, i el 17-09-2026 confirmat amb el gràfic
  llegit**: **el document no publica la sèrie sense els CAP i l'Hospital**, i
  **sense desglossament per àmbit el repartiment no es pot fer.** `Requereix les
  taules per àmbit de l'onada del 2018.` **El que el corpus ja no ha de donar per
  bo és la mida del titular**: **els 30 punts es mesuren contra el 91,5 % del
  2014, que és el màxim de tota la sèrie**; **contra la mitjana de les quatre
  onades anteriors en són uns 18.** **I el buit s'ha eixamplat**: **el 2014 és el
  màxim històric en sis dels nou àmbits socioeconòmics**, **set dels quals no
  tenen cap canvi de disseny declarat.** `Requereix la metodologia de l'onada del
  2014.`
- ~~**Per què l'edició del 2022 reprodueix 77,5 on aquesta imprimeix 75,4.**~~ —
  **`parcial` el 20-09-2026**: quatre files de la taula coincideixen, però la
  fila principal passa de **75,4 %** a **77,5 %** i les quatre opcions d'acció
  sumen **99,2** a l'edició de 2018 i **101,5** a la reproducció de 2022. La
  discrepància de reproducció queda provada, però cap dels dos documents no
  n'explica la causa.
- ~~**Els capítols d'usos lingüístics (pp. 15-31) no s'han destil·lat valor a
  valor.** Disset pàgines de gràfics apilats.~~ — **`resolt` el 17-09-2026.**
  **Les seves disset pàgines són ara [al cos d'aquest
  article](#el-capítol-dusos-lingüístics-destillat-valor-a-valor)**, llegides
  sobre la pàgina renderitzada: **vint-i-quatre taules, les nou sèries
  socioeconòmiques dobles i l'indicador d'ús amb la seva fórmula.** **Segueix
  obert per a les altres tres edicions** (2009, 2014, 2022), **que declaren el
  mateix buit i el corpus no ha destil·lat.**
- **El nom de l'organisme que fa l'estudi**, que el mateix llibret escriu de dues
  maneres.
- **La font original de l'annex d'assalariats** segueix sense ser al corpus, i
  **la sèrie acaba el 2017** sense desglossament per nacionalitat.
- **Drets tancats.** **Cap llicència declarada.** **Res d'aquesta font no entra
  en cap dataset** i el PDF **no es versiona**. **`no-es-buit`**: és un avís de
  drets, no una pregunta de recerca.

## Related

- [La sèrie que no és una sèrie](./la-serie-que-no-es-una-serie.md) — la setena onada, que reimprimeix aquest gràfic i aquesta taula.
- [Els nouvinguts tenien més català que els nascuts a Andorra](./els-nouvinguts-tenien-mes-catala-que-els-nascuts-a-andorra.md) — la cinquena onada, i el 64 % que aquesta fitxa acota.
- [Quaranta-vuit coma cinc, no quaranta-vuit coma sis](./quaranta-vuit-coma-cinc-no-quaranta-vuit-coma-sis.md) — la quarta onada, i la base que aquesta confirma.
- [La sèrie històrica del català a Andorra](./la-serie-historica.md)
- [Qui parla què](./qui-parla-que.md)
- [La llei de la llengua](./la-llei-de-la-llengua.md)
- [El mercat de treball dual](../../societat/immigracio/el-mercat-de-treball-dual.md) — els sectors de l'annex d'assalariats.
