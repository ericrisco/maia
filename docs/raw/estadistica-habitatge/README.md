# `docs/raw/estadistica-habitatge/` — transaccions i preus de l'habitatge

Notes del **Departament d'Estadística** que ajunten **dues activitats en un sol
document**: **A117. Estadística de transaccions immobiliàries** i **A145.
Estadística de preus de l'habitatge i el sòl**. Periodicitat **trimestral**; la
nota del **primer trimestre de l'any** porta també el tancament de l'any anterior.

| | |
| --- | --- |
| **Font** | [Departament d'Estadística](https://www.estadistica.ad/) · Govern d'Andorra |
| **Patró d'URL** | `https://sig.govern.ad/SIGDDE.Public/Files/Documents/Notes_premsa_noticies/A117_A145_<AAAAMMDD>_A.pdf` |
| **Llicència** | **CC BY 4.0** per a la informació estadística pròpia (avís legal a `../estadistica-poblacio/avis-legal-2026-09-13.txt`) |
| **Redistribució** | **sí**, amb atribució, data i menció de tractament propi |
| **Data de consulta** | 2026-09-17 |
| **Fitxa de font del corpus** | [`estadistica-ad`](../../fonts/estadistica-ad.md) |
| **`apte_dataset`** | **sí** |

## Què hi ha

| Fitxer | Període | Publicació |
| --- | --- | --- |
| `a117-a145-20260209` | **4t trimestre 2025 i any 2025** | 09-02-2026 |
| `a117-a145-20260806` | 2n trimestre 2026 | 06-08-2026 |

## Totes les notes localitzades

`A117_A145_` + `20250210`, `20250515`, `20250807`, `20251106`, `20260209`,
`20260507`, `20260806`.

## Per què costava trobar-les

**El fitxer no es diu com l'activitat.** Una cerca per `A145_<data>` no torna
res: la nota es publica sota el nom **compost** `A117_A145`. Aquesta és la regla
general de la via d'Estadística — **una nota pot cobrir més d'una activitat del
Pla estadístic i el fitxer les concatena** — i és el que justifica el sondeig de
dates descrit a `02-DOCS/wiki/harness/decisions.md`.

## Les xifres clau de l'any 2025

**Preu mitjà per m² dels pisos** (2024 → 2025): Canillo 3.566,3 → 3.752,4 ·
Encamp 3.123,2 → 3.242,0 · Ordino 3.691,7 → 4.134,5 · La Massana 3.296,0 →
3.663,0 · Andorra la Vella 5.063,6 → **4.885,9 (−3,5%)** · Sant Julià de Lòria
2.524,4 → 3.335,1 **(+32,1%)** · Escaldes-Engordany 5.282,4 → **6.117,0** ·
**país 4.053,1 → 4.479,4 (+10,5%)**.

**Transaccions**: **1.608 → 2.175 (+35,3%)**. **Andorra la Vella es queda a 313
exactes** els dos anys.

## Les altres dues activitats d'aquesta carpeta

| Fitxer | Activitat | Període | Publicació |
| --- | --- | --- | --- |
| `a061-edificis-unitats-20251209` | **A061. Edificis i unitats domiciliàries** | any 2024 | 09-12-2025 |
| `a062-caracteristiques-habitatges-20260203` | **A062. Característiques dels habitatges** | any 2024 | 03-02-2026 |

**Calendari**: A061 anual al **desembre** (`20251209`); A062 anual al **febrer**
(`20260203`).

**Compten coses diferents i cal dir-ho en citar-les.** L'**A061** surt del
**Registre Estadístic de Territori** i compta **el que hi ha construït**:
**44.047 habitatges** el 2024, dins de **90.947 unitats domiciliàries** —que
inclouen **20.220 pàrquings** i **12.109 trasters**—, en **10.699 edificacions**.
L'**A062** surt de l'**Enquesta de Pressupostos Familiars** i compta **el que
declaren les llars residents**: **39.271 habitatges** el 2024.

**La resta, 4.776, és el 10,8% del parc**, i **no és el nombre d'habitatges
buits**: hi ha dins els d'ús turístic, les segones residències, els que estan en
obres i els de no residents.

**Tres preus del lloguer per al 2024, i cap no és el mateix**: **9,5 €/m²** de
mitjana del parc llogat (A062), **13,0 €/m²** per a les llars amb menys d'un any
d'antiguitat (A062), **13,5 €/m²** de mitjana de tots els contractes (SICAR, via
la presentació del Govern).

**On s'usa**: [`temes/societat/habitatge/els-habitatges-buits.md`](../../temes/societat/habitatge/els-habitatges-buits.md) ·
[`temes/societat/habitatge/la-crisi-de-lhabitatge.md`](../../temes/societat/habitatge/la-crisi-de-lhabitatge.md).
