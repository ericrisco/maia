---
title: "Hàbits culturals, esportius i voluntariat per l'API d'Estadística"
---

# Hàbits culturals, esportius i voluntariat per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../README.md).

| | |
| --- | --- |
| **Fitxer** | `cultura-i-esport-api-2026-09-18.tsv` — **552 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **100 divisions**; **2019 i 2024** per als hàbits, **2010-2024** per al voluntariat |

## Dues onades, no una sèrie

**L'enquesta d'hàbits culturals i esportius té dos punts: 2019 i 2024.** **No
és una sèrie** i **el corpus no en llegeix cap moviment com a tendència**: en
llegeix **una diferència entre dos anys**, un d'ells anterior i l'altre
posterior a la pandèmia.

## Un defecte de la font, comprovat

**Les divisions 2061 i 2062 no quadren.** El **nombre de voluntaris total**
(2061) i la **suma d'homes i dones** (2062) **coincideixen del 2010 al 2021 i
divergeixen del 2022 al 2024**:

| Any | Total (2061) | Homes + dones (2062) |
| --- | ---: | ---: |
| 2021 | 100 | 100 |
| **2022** | **468** | **242** |
| **2023** | **517** | **260** |
| **2024** | **476** | **281** |

**El corpus no cita cap de les dues xifres per a aquests tres anys.**

## El «nombre d'entitats» no és el registre d'associacions

**La divisió 2059 dona entre 2 i 16 entitats l'any.** **No és el cens
d'associacions del país**: pel context de la branca (voluntariat, esdeveniments)
**són les entitats que participen en una activitat concreta**, no totes les
registrades. `La font no en dona la definició i el corpus no la cita com a cens.`
