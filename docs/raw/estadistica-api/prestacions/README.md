---
title: "Prestacions socials per l'API d'Estadística"
---

# Prestacions socials per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../README.md).

| | |
| --- | --- |
| **Fitxer** | `prestacions-api-2026-09-18.tsv` — **5.583 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **91 divisions**; l'any d'inici canvia segons la prestació |

## Cada prestació arrenca en un any diferent

| Prestació | Primer any |
| --- | --- |
| Prestacions de l'habitatge | **2010** |
| Pensions no contributives · ajuts de l'article 20 | **2013** |
| Pensió de solidaritat per a la gent gran (PSGG) | **2016** |
| Prestacions per fills | **2017** |
| Prestacions de discapacitat · prestacions ocasionals | **2018** |
| Desocupació involuntària | **2021** |

**No hi ha cap any en què totes existeixin**, i **cap sèrie no arriba abans del
2010.**

## Dos forats a la sèrie de l'habitatge

**La divisió 1785 salta el 2016**: dona 2010-2015 i 2017-2025. **Cap nota ho
explica.**

## «Nombre» i «import» són divisions separades

**Cada prestació té una parella de divisions**: **nombre de beneficiaris** i
**import concedit**. **No s'han de barrejar**, i **l'import per beneficiari es
calcula dividint-les**, cosa que el corpus fa dient-ho.
