---
title: "Seguretat, infraccions i detencions per l'API d'Estadística"
---

# Seguretat, infraccions i detencions per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../l-api-publica-del-departament-d-estadistica.md).

| | |
| --- | --- |
| **Fitxer** | `seguretat-api-2026-09-18.tsv` — **9.156 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **85 divisions de 90**; **2007-2025** per a infraccions i detencions, **2016-2025** per a efectius |

## Cinc divisions no hi són

**Quatre s'han deixat fora expressament**: **1816, 1817, 1818 i 1821**, que són
**«infraccions per article»** i **«per lloc i article»**. **Sumen 118.012 dels
127.168 valors baixats** —el 92,8%— perquè creuen **cada article del Codi penal
per cada lloc de comissió i cada any**, i **gairebé tot el creuament és zero**.
**El bolcat pesava 26 MB i ara en pesa 1,6.** `Es poden tornar a demanar a
l'API quan calgui l'article concret: el catàleg les té.`

## La divisió 1840 no s'ha pogut baixar

**`QUANTITAT INTERVINGUDA D'ESTUPEFAENTS, ALTRES TIPUS EN GRAMS PER TIPUS
D'ESTUPEFAENT`** **fa *timeout*** a l'API el 18-09-2026. **Les altres 89 sí.**

## Infraccions no vol dir delictes

**La divisió 1815 separa dues coses que el total ajunta:**

| | 2007 | 2025 |
| --- | ---: | ---: |
| **Delictes** | 1.631 | **2.255** |
| **Contravencions penals** | **2.684** | 1.754 |
| Total infraccions | 4.315 | 4.009 |

**Citar «infraccions» com si fossin delictes inverteix el sentit de la sèrie**:
**el total és gairebé pla i la composició s'ha girat.**

## Les detencions de menors s'aturen el 2013

**Els trams «de 12 a 15» i «de 16 a 17» donen entre 0 i 18 detencions l'any
fins al 2012** i **entre 0 i 3 del 2013 ençà.** **El corpus no sap si és un
canvi de pràctica policial, de llei o de recompte**, i **no llegeix el zero com
a absència de delinqüència juvenil.**

## Dues taules de nacionalitat que no diuen el mateix

**La divisió 1824 compta per nacionalitat** (Espanya, Portugal, Andorra…) i
**la 1825 per situació d'immigració** (andorrans, residents, fronterers, no
residents). **Els «andorrans» de la 1825 i l'«Andorra» de la 1824 coincideixen
gairebé sempre i no sempre**: **el 2012 en donen 194 i 188, i el 2019, 355 i
353.** **El corpus cita la 1825 per a la lectura de residència.**
