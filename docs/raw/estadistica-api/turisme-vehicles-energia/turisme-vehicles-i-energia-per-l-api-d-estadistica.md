---
title: "Turisme, vehicles i energia per l'API d'Estadística"
---

# Turisme, vehicles i energia per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../l-api-publica-del-departament-d-estadistica.md).

| | |
| --- | --- |
| **Fitxer** | `turisme-vehicles-energia-api-2026-09-18.tsv` — **118.938 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **385 divisions** dels prefixos `020503` permisos i superfície autoritzada, `020504` entrada i matriculació de vehicles, `020506` allotjaments i pernoctacions, `020508` consum d'energia en TEP |
| **Divisions que no responen** | **cap** |

## La sèrie més llarga d'aquest bolcat

**El consum d'energia en tones equivalents de petroli, mensual des del gener del
1993 i per set fonts** —electricitat, gasoil de locomoció, gasolina, fuel
domèstic, butà, propà i carbó—. **Trenta-tres anys.**

**El que en surt** és a
[la transició energètica](../../../temes/economia/energia-i-serveis/la-transicio-energetica.md):
**el màxim del país és del 2005 i no s'hi ha tornat**, **l'electricitat passa del
15,4% al 24,9% del total**, **el butà cau un 75,8%** i, **creuant-la amb el PIB
nominal, la intensitat energètica es pot mesurar per primera vegada**: **89,1
TEP per milió d'euros el 2010 —la xifra que la Llei de transició energètica
declara a l'article 3.u— i 53,4 el 2024.**

## El que queda sense explotar

**Els motius de visita de turistes i excursionistes** (10.548 valors), **la zona,
la categoria i el tipus d'allotjament amb metodologia 2012** (10.584), **les
matriculacions de vehicles per tipus** (3.501), **els permisos d'obra per tipus i
parròquia** (1.827) i **les pernoctacions per tipus i zona** (3.254).

## Una precaució de metodologia

**Diverses taules d'allotjament i pernoctacions porten «(METODOLOGIA 2012)» al
títol.** **El corpus ja ha documentat que la sèrie de visitants travessa quatre
metodologies i que, on se solapen, la del 2012 dona entre un 3,7% i un 5,4% més
que la del 2025** ([els visitants](../../../temes/economia/turisme-i-neu/de-la-fonda-a-lhotel.md)).
**Les xifres d'aquestes taules no es poden encadenar amb les d'una altra
metodologia sense dir-ho.**

## Dues taules no arriben al mateix any, i s'ha de mirar abans de sumar

**Aquest bolcat barreja sèries que acaben en moments diferents.**

| Taula | Últim període | Compte |
| --- | --- | --- |
| **Consum d'energia en TEP** | **2026/07** | **2025 és un any sencer** |
| **Matriculacions de vehicles per tipus** | **2025/05** | **2025 té cinc mesos: no és comparable amb cap any anterior** |

**Sumar els mesos d'una taula mensual per any exigeix comptar-los primer.**
**Amb cinc mesos, el 2025 de matriculacions dona 1.009 turismes contra els 2.390
del 2024**, i **la caiguda seria un artefacte.**
