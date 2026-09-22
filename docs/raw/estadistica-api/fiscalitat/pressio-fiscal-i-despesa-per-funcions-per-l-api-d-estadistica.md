---
title: "Pressió fiscal i despesa per funcions, per l'API d'Estadística"
---

# Pressió fiscal i despesa per funcions, per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../l-api-publica-del-departament-d-estadistica.md).

| | |
| --- | --- |
| **Fitxer** | `fiscalitat-i-despesa-api-2026-09-18.tsv` |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **pressió fiscal 2000-2025**; **COFOG 2018-2024**; **declaracions d'impostos 2015-2024 i trimestrals des del 2016** |

## Un defecte de la font, comprovat

**A la taula COFOG (divisió 3504), les columnes del 2022 i del 2023 són
idèntiques valor a valor**, incloses les xifres amb cèntims
(**1.033.181.241,xx** de despesa total els dos anys, i cada una de les desenes
de línies de funció). **Això no és una coincidència: és el 2022 repetit.**

**El corpus cita el 2018-2022 i el 2024, i no cita el 2023 d'aquesta taula.**

## Les dues taules de pressió fiscal

- **2213 — en percentatge del PIB.** És la que el corpus cita.
- **2887 — impostos meritats en euros.** La mateixa estructura, en valor
  absolut.

**Totes dues arriben al 2025**, i **totes dues fan servir la nomenclatura SEC**
—`D2`, `D21`, `D211`, `D5`, `D51`, `D61`—, no els noms dels impostos andorrans.
**La correspondència entre `D211 Taxes tipus IVA` i l'IGI, l'IMI o l'IAC la fa
la taula 2887 en subfiles**, i **el corpus no l'ha comprovada contra les lleis
fiscals.**
