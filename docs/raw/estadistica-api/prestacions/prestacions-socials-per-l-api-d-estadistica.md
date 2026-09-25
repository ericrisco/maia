---
title: "Prestacions socials per l'API d'Estadística"
---

# Prestacions socials per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../l-api-publica-del-departament-d-estadistica.md).

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


## Discrepància de cobertura en les sol·licituds del 2025

La captura del 18-09-2026 dóna **59** a la divisió 2829 per al 2025; la divisió
2830 desglossa **31 favorables i 28 desfavorables**, que també sumen 59. La
publicació posterior d’A052 consultada el 25-09-2026 informa **62 sol·licituds**
i explica que tres encara no s’havien resolt ([extracte i captura oficial](../../estadistica-prestacions/a052-2025-transparencia-extracte-2026-09-25.txt)). La captura API no incorpora aquestes tres al total malgrat que la sèrie diu «sol·licituds». No s’ha trobat una nota metodològica que n’expliqui el motiu. Es manté el bolcat sense alteració; per a l’article es fa servir 62 i 50,0% de l’A052 i es registra el desacord. La divisió 2834 continua confirmant les 31 prestacions concedides per nacionalitat.
