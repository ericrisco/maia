---
title: "L'IPC andorrà per l'API d'Estadística"
---

# L'IPC andorrà per l'API d'Estadística

**Baixat el 18-09-2026** amb
`02-DOCS/raw/operations/gap-audit-scripts/estadistica_api.py`, de l'API pública
descrita a [`../README.md`](../l-api-publica-del-departament-d-estadistica.md).

| | |
| --- | --- |
| **Fitxer** | `ipc-api-2026-09-18.tsv` — **19.210 valors** |
| **Columnes** | `idDivision · taula · serie · periode · valor · font · actualitzat` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **1997-12 → 2026-08**, mensual |

## Les dotze divisions baixades

| id | Taula |
| --- | --- |
| **54** | Índex general. **Base 2001** — *1997-12 → 2017-12* |
| **55** | Índex general, variacions interanuals. Base 2001 |
| **957** | Índex general. **Base 2018** — *2001-01 → 2021-12* |
| **958** | Índex general, variació anual. Base 2018 |
| **2621** | Índex general. **Base 2021** — *2001-01 → 2026-08* |
| **2622** | Índex general, variació anual. Base 2021 |
| **2624** | Índex per **grups** (12 grups COICOP). Base 2021 |
| **2625** | Índex per grups, variació anual. Base 2021 |
| **2630** | Índex per **classes** (**75 classes**). Base 2021 |
| **2633** | Índex per **grups especials** (12). Base 2021 |
| **2636** | **Ponderacions** per grups, **2022-2026** |
| **2639** | Ponderacions per grups especials, 2022-2026 |

## Tres advertències sobre les bases

1. **Hi ha tres bases i cadascuna reescriu el passat.** La sèrie base 2001 i la
   base 2021 **no donen el mateix valor per al mateix mes**: el gener del 2001
   és **98,53** en base 2001 i **71,24** en base 2021. **No són comparables per
   nivell**; sí que ho són **per variació**.
2. **L'única manera d'arribar al 1997 és encadenar.** La base 2021 comença el
   **2001-01**; la base 2001 arriba fins al **1997-12**. El corpus encadena pel
   factor del mes comú (2001-01) **i ho diu cada vegada que ho fa**.
3. **Els noms de les sèries arriben en anglès** encara que es demani
   `language=ca`. El TSV els conserva **tal com els dona la font**; la fitxa del
   corpus els tradueix i **el TSV és l'original**.

## Les classes amb `null`

**Hi ha classes que no publiquen tots els mesos.** El bolcat **omet els nuls**
en comptes d'escriure'ls: una sèrie curta al TSV **no vol dir que la classe no
existeixi**, vol dir que no té valor aquell mes.
