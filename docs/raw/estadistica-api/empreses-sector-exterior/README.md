---
title: "Estoc d'empreses, comptabilitat empresarial, R+D i associacions — API del Departament d'Estadística"
---

# Estoc d'empreses, comptabilitat empresarial, R+D i associacions — API del Departament d'Estadística

**Baixat el 18-09-2026** amb
`02-DOCS/raw/operations/gap-audit-scripts/estadistica_api.py`, prefix de divisió
**`0204`**.

| | |
| --- | --- |
| **Fitxer** | `empreses-sector-exterior-api-2026-09-18.tsv` (43 MB) |
| **Divisions** | **267** |
| **Taules** | **249** |
| **Valors** | **201.574** |
| **Divisions KO** | **0** |

## Font i drets

- **Departament d'Estadística del Govern d'Andorra**,
  `https://sig.govern.ad/SIGDDE.Public/estadistiquesdades/api/`.
- **Llicència: CC BY 4.0.** Atribució obligatòria al Departament d'Estadística.
- Fitxa de font del corpus: `docs/fonts/estadistica-ad.md`.

## Columnes

`idDivision · taula · codi · serie · periode · valor` — valors normalitzats de
`1.234,56` a `1234.56`.

## Què hi ha

- **Demografia d'empreses**: estoc, empreses nascudes i mortes, desaparicions en
  els tres primers anys de vida, per forma jurídica i per situació de
  l'activitat.
- **Establiments i societats**: nombre, altes, baixes i creació neta, per
  parròquia, secció, divisió i grup, en **dues classificacions paral·leles**,
  **CAEA 1999** i **CAEA 2019**.
- **Comptabilitat empresarial**: balanç de situació i compte de pèrdues i
  guanys, per sector; comptes econòmics per divisió.
- **R+D i innovació**: despesa interna i externa, personal, hores, camp
  científic, finançament, beques, i els factors que dificulten innovar.
- **Associacions, fundacions i professionals titulats**: creació neta per
  parròquia, tipus, sexe i nacionalitat.

## Advertències d'ús

- **Les sèries CAEA 1999 i CAEA 2019 no s'encadenen.** Són dues classificacions
  d'activitat diferents; comparar-les directament dona salts que no són
  econòmics.
- **«Establiment», «societat» i «empresa» són tres unitats diferents** i
  cadascuna té la seva família de taules. No se sumen entre elles.
- Les taules amb `(DISTRIBUCIÓ)` al títol donen **percentatges**, no imports.
