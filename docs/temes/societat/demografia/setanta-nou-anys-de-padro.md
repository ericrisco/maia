---
type: article
title: La població registrada d'Andorra i el seu canvi natural (1947–2025)
description: "L'API publica la població registrada anual des del 1947 i les sèries de naixements i defuncions des del 1953; una sèrie oficial de saldo migratori està disponible des del 2016."
tema: temes/societat/demografia
veu: compilada
epoca: contemporania
apte_llengua: false
font: estadistica-ad
timestamp: 2026-09-25T03:53:00Z
tags: [demografia, societat, migracio, estadistica, serie-historica, segle-xx, segle-xxi]
---

# La població registrada d'Andorra i el seu canvi natural (1947–2025)

Una captura de l'API del Departament d'Estadística, baixada el 18-09-2026,
conté la sèrie anual de població registrada de 1947 a 2025 (divisió 1) i les
sèries de naixements i defuncions de 1953 a 2025 (divisions 22 i 28). També
conté una sèrie publicada de saldo migratori de 2016 a 2025 (divisió 1261).
Les fitxes de procedència i de condicions descriuen el bolcat i la llicència
CC BY 4.0 amb atribució: `docs/raw/estadistica-api/resta-del-cataleg/README.md`,
`docs/raw/estadistica-api/demografia-vital/demografia-vital-per-l-api-d-estadistica.md`
i `docs/raw/estadistica-api/l-api-publica-del-departament-d-estadistica.md`.

La població registrada (divisió 1) i la «població total» (divisió 797,
2009–2025) són sèries diferents. El 2025, la primera dona 94.128 i la segona
89.058: una diferència de 5.070 persones. Aquesta fitxa no tracta els dos
conceptes com si fossin equivalents.

## La sèrie de població registrada

| Any | Població registrada |
| --- | ---: |
| 1947 | 5.385 |
| 1960 | 8.392 |
| 1970 | 19.545 |
| 1980 | 35.460 |
| 1990 | 54.507 |
| 1993 | 65.227 |
| 2000 | 65.844 |
| 2010 | 85.015 |
| 2013 | 76.098 |
| 2020 | 82.887 |
| 2025 | 94.128 |

Entre 1947 i 2025, el valor de la sèrie es multiplica per 17,5. Hi ha deu
descensos anuals, agrupats en cinc períodes:

| Anys amb descens | Valors comparats | Variació entre els extrems |
| --- | --- | ---: |
| 1952–1954 | 6.310 (1951) → 5.503 (1954) | −12,8% |
| 1994–1995 | 65.227 (1993) → 63.859 (1995) | −2,1% |
| 2000 | 65.971 (1999) → 65.844 (2000) | −0,2% |
| 2009 | 84.484 (2008) → 84.082 (2009) | −0,5% |
| 2011–2013 | 85.015 (2010) → 76.098 (2013) | −10,5% |

El descens anual més gran en nombres absoluts és el de 2011: la sèrie passa de
85.015 el 2010 a 78.115 el 2011, una baixada de 6.900 (−8,1%). Les dades
consultades no n'expliquen la causa; no permeten decidir si reflecteix canvis
de residència, una revisió dels registres o altres factors.

## Naixements i defuncions

El canvi natural de cada període es calcula restant les defuncions als
naixements. L'acumulat per períodes és:

| Període | Naixements menys defuncions |
| --- | ---: |
| 1953–1959 | +442 |
| 1960–1969 | +2.016 |
| 1970–1979 | +3.471 |
| 1980–1989 | +3.947 |
| 1990–1999 | +5.131 |
| 2000–2009 | +5.488 |
| 2010–2019 | +3.715 |
| 2020–2025 | +719 |

El saldo natural anual més alt de la sèrie és el de 2008: 875 naixements i
237 defuncions, és a dir, +638. El 2025 hi va haver 508 naixements i 386
defuncions, un saldo de +122. El saldo acumulat de 2020 a 2025 és positiu
(+719); no és correcte descriure'l com si el canvi natural s'hagués acabat.

| Any | Naixements | Defuncions | Saldo natural calculat |
| --- | ---: | ---: | ---: |
| 2008 | 875 | 237 | +638 |
| 2015 | 659 | 282 | +377 |
| 2020 | 539 | 419 | +120 |
| 2025 | 508 | 386 | +122 |

El 2020 registra 419 defuncions, el valor anual més alt de la sèrie
1953–2025. El nombre és un registre de l'any; aquesta taula no n'estableix la
causa.

## El saldo migratori publicat

La divisió 1261 publica un saldo migratori anual per a 2016–2025. Els deu
valors són positius, i el més alt d'aquesta sèrie és el de 2023 (3.407).
Com que aquesta captura no conté valors anteriors a 2016, no permet datar l'any
en què el saldo hauria passat de negatiu a positiu.

| Any | Saldo migratori publicat |
| --- | ---: |
| 2016 | 1.149 |
| 2017 | 1.328 |
| 2018 | 1.214 |
| 2019 | 1.093 |
| 2020 | 383 |
| 2021 | 1.401 |
| 2022 | 1.880 |
| 2023 | 3.407 |
| 2024 | 1.874 |
| 2025 | 1.829 |

La versió anterior d'aquesta fitxa calculava un saldo per a 2010–2025 restant
el canvi natural al canvi de la divisió 797. Aquest càlcul no coincideix
sempre amb la sèrie migratòria publicada; s'ha retirat perquè no es poden
atribuir les diferències ni la data de referència només amb les taules
consultades.

## Buits registrats i límits de les sèries

- «Població registrada» (divisió 1) i «població total» (divisió 797) són
  conceptes separats a l'API. Les diferències entre elles no s'expliquen aquí.
- La sèrie de població registrada no comenta les caigudes de 1952–1954,
  1994–1995, 2000, 2009 ni 2011–2013; aquesta fitxa no n'atribueix les causes.
- El saldo migratori publicat comença el 2016. No es fa servir el canvi de
  població menys el canvi natural per completar-ne els anys absents.
- Els càlculs de saldo natural són sumes o restes dels recomptes publicats; no
  són estimacions de migració ni explicacions causals.
- La captura és una instantània descarregada el 18-09-2026, no una consulta en
  temps real.
