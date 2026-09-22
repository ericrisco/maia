---
title: "Pobresa, desigualtat i llars per l'API d'Estadística"
---

# Pobresa, desigualtat i llars per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../l-api-publica-del-departament-d-estadistica.md).

| | |
| --- | --- |
| **Fitxer** | `pobresa-i-llars-api-2026-09-18.tsv` — **2.176 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **54 divisions**; **2018-2025** per a pobresa i desigualtat, **2010-2025** per a habitatge i llars |

## Les dues enquestes que hi ha al darrere

- **Enquesta de condicions de vida (ECV)**, del **2018** ençà: llindars,
  taxes de risc de pobresa, Gini, quintils, privacions materials, sobrecàrrega
  de l'habitatge.
- **Enquesta de pressupostos familiars / despeses de les llars**, del **2010**
  ençà: règim de tinença, preu del lloguer, membres per llar, equipaments.

## Una regla tècnica que aquest bolcat ha trobat

**El `json-stat` d'algunes divisions torna els noms de sèrie com a codis**
(`0105020500070002`) **en comptes de text**, encara que es demani
`language=ca`. **El `file=csv` de la mateixa divisió sí que els torna
escrits** i **en català**.

> **Si els noms de sèrie arriben com a codis, demana la mateixa divisió en
> `file=csv`.**

Per això aquest bolcat es fa des del CSV i no des del JSON, al contrari que
[`../ipc/`](../ipc/l-ipc-andorra-per-l-api-d-estadistica.md).

## Dues advertències de lectura

1. **El llindar de pobresa canvia de referència el 2021.** Del 2018 al 2020 és
   el **60% dels ingressos medians per unitat de consum del total**; del 2021
   ençà és el **60% dels ingressos medians d'una llar d'un sol adult**. Les dues
   sèries **estan a la mateixa fila del mateix quadre** i **no són la mateixa
   cosa**. Comprovat valor a valor; vegeu
   [el Gini ha pujat vuit punts](../../../temes/societat/proteccio-social/el-gini-ha-pujat-vuit-punts.md).
2. **El «pes de les despeses respecte els ingressos» (divisió 1531) s'atura el
   2021** i el darrer any **no suma 100** (12,4 + 19,0 + 0,5 = 31,9). **La sèrie
   està trencada a la font** i el corpus no la cita.
