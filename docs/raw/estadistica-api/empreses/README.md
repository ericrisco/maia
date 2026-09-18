# Demografia d'empreses i societats per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../README.md).

| | |
| --- | --- |
| **Fitxer** | `empreses-api-2026-09-18.tsv` — **2.860 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **22 divisions**, **2016-2025** |

## Dos comptadors que no són el mateix

**Aquesta és la confusió que la branca convida a fer**, i el corpus la registra
abans de citar-ne cap xifra:

| Comptador | Activitat | Què compta | 2025 |
| --- | --- | --- | ---: |
| **Demografia harmonitzada d'empreses** | **A097** | **empreses**, hi hagi societat mercantil o no | **23.939** |
| **Registre de Societats** | **A099** | **societats inscrites** | **17.784** |

**Les dues són oficials, del mateix Departament, i del mateix any.** **La
diferència són els negocis que no són societats mercantils**: **persona física**
n'hi ha **5.834** al primer comptador.

## La supervivència es llegeix per files, no per columnes

**Les divisions 2674 i 2675 són matrius de cohort**: cada fila és **l'any de
naixement** i cada columna **l'any d'observació**. **La diagonal és el primer
any de vida** (sempre entre 97,6% i 98,9%) i **el corpus no ha de llegir una
columna com si fos una sèrie temporal d'un mateix grup d'empreses.**
