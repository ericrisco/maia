---
title: "Cens electoral i participació per l'API d'Estadística"
---

# Cens electoral i participació per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../l-api-publica-del-departament-d-estadistica.md).

| | |
| --- | --- |
| **Fitxer** | `eleccions-api-2026-09-18.tsv` — **342 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **16 divisions**; **generals 2009-2023** (cinc convocatòries) i **comunals** |

## Dos censos, dues participacions

- **Nacional** (2041-2044, 2051-2054): **eleccions generals al Consell
  General**.
- **Parroquial** (2045-2048, 2055-2058): **eleccions comunals**.

**No s'han de barrejar**: el cens parroquial i el nacional no tenen la mateixa
mida ni les mateixes dates.

## La participació no quadra amb els dossiers per entre 1 i 9 vots

**Comparat amb els dossiers de `eleccions.ad`** que el corpus ja tenia:

| Any | Dossier | API |
| --- | ---: | ---: |
| 2009 | 15.289 | **15.286** |
| 2011 | 16.192 | **16.201** |
| 2015 | 16.084 | **16.084** |
| 2019 | 18.639 | **18.638** |
| 2023 | 20.057 | **20.058** |

**Cap de les dues fonts no diu si hi compta els vots nuls.** **El corpus manté
el dossier per a la sèrie de participació i l'API per als desglossaments**,
perquè els desglossaments de l'API sumen entre ells.
Vegeu [l'abstenció](../../../temes/politica/sistema-electoral/labstencio.md).

## Les dates són dates completes

**Els períodes d'aquestes taules són `2023/04/02`, no `2023`.** **La divisió del
cens (2041) sí que usa l'any sol**, i **per tant el cens i la participació del
mateix any tenen etiquetes de període diferents.**
