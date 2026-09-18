# Infraccions per article del Codi penal

**Bolcat el 18-09-2026** de l'API del Departament d'Estadística
(`02-DOCS/raw/operations/gap-audit-scripts/estadistica_api.py`), amb un temps
d'espera de **900 s** per petició.

| Fitxer | Valors |
| --- | ---: |
| `infraccions-per-article-2026-09-18.tsv` | **118.066** |

Columnes: `idDivision · taula · codi · serie · periode · valor`.

## Què hi ha

| Divisió | Taula | Anys | Nota |
| ---: | --- | --- | --- |
| **1816** | Infraccions denunciades per article | 2007-2025 | 454 files de jerarquia |
| **1817** | Infraccions denunciades per títol i lloc de comissió | 2007-2025 | per parròquia |
| **1818** | Infraccions denunciades per article i lloc de comissió | 2007-2025 | 434 articles × parròquia |
| **1821** | Infraccions resoltes per article | 2007-2025 | mateixa jerarquia que la 1816 |
| **1840** | Quantitat intervinguda d'estupefaents, altres tipus, en grams | 2017-2025 | **54 valors, 47 dels quals zero** |

## Per què no hi era abans

Aquestes divisions s'havien deixat fora de
[`resta-del-cataleg/`](../resta-del-cataleg/README.md) **expressament**, perquè
el creuament article × parròquia és gairebé tot zero: **la 1818 sola fa 94.490
valors** per a poc més de 4.000 infraccions l'any. La 1840, a més, **es donava
per «no respon»**, i el 18-09-2026 s'ha comprovat que **era un temps d'espera
del client, no un límit del servidor** — la mateixa correcció que
[`les-que-no-responien/`](../les-que-no-responien/README.md).

## Advertiments de lectura

- **La jerarquia de la sèrie té tres nivells** —`1. Delictes` → `1.1. Vida
  humana independent` → `1.1.102. Homicidi`— **i els nivells se sumen entre
  ells**: sumar totes les files compta cada infracció tres cops.
- **Creuar 1816 amb 1821 dona la taxa de resolució per article**, i està
  destil·lat a
  [`docs/temes/institucions/justicia/dues-mil-dues-centes-cinquanta-cinc-i-mil-set-centes-cinquanta-quatre.md`](../../../temes/institucions/justicia/dues-mil-dues-centes-cinquanta-cinc-i-mil-set-centes-cinquanta-quatre.md).
- **Els números d'article canvien el desembre del 2026** amb la Llei 18/2026 del
  Codi penal. La taula d'equivalències és a
  [`les-penes-del-codi-penal.md`](../../../temes/institucions/justicia/les-penes-del-codi-penal.md).

## Procedència i ús

Departament d'Estadística del Govern d'Andorra, dades públiques publicades a
`sig.govern.ad`. Mateixes condicions que la resta de
[`estadistica-api/`](../README.md).
