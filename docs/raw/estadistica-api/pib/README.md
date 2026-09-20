---
title: "PIB i comptabilitat nacional per l'API d'Estadística"
---

# PIB i comptabilitat nacional per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../README.md).

| | |
| --- | --- |
| **Fitxer** | `pib-api-2026-09-18.tsv` — **7.963 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **20 divisions**; **anual 2000-2025** i **trimestral** per a les sèries desestacionalitzades |

## Nominal, real i PPP no volen dir el mateix

| Sèrie | Què és |
| --- | --- |
| **PIB nominal** | a preus corrents de cada any |
| **PIB real** | a preus constants — descompta la inflació |
| **PPP USD / PPP EU27** | estimació indirecta en paritat de poder adquisitiu |

**El nominal i el real es creuen el 2010** —tots dos valen 2.602,31—, que és
**l'any base de la sèrie real**. **Abans del 2010 el real és més alt que el
nominal i després més baix**, i **el corpus diu sempre quina de les dues cita.**

## Dues poblacions per al PIB per càpita

**Les divisions 792-795 publiquen cada indicador dues vegades**: **sobre
població estimada** i **sobre població registrada**. **Donen xifres diferents**
—35.775 i 33.436 el 2018— i **la sèrie sobre població estimada només arrenca el
2009**. **El corpus diu quina fa servir.**

## La sèrie sectorial s'atura el 2024

**La divisió 605 (agregats) arriba al 2025**; **la 606 (VAB per sectors)
s'atura el 2024.**
