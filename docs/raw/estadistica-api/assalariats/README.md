# Assalariats i massa salarial per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../README.md).

| | |
| --- | --- |
| **Fitxer** | `assalariats-api-2026-09-18.tsv` — **28.345 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **15 divisions**; **desembre de cada any, 1966-2025**, més **maig del 2026** |

## Només desembres, i per què

**La font és mensual des del juliol del 1966**: **719 columnes.** **Demanar-les
totes fa un URL de 5.922 caràcters i el servidor respon `500 Internal Server
Error`.** **El bolcat demana només els desembres** més el darrer mes publicat.

> **Si l'API respon `500`, escurça `showColumns`.** L'URL que `api_url()`
> proposa pot ser massa llarg per a la mateixa API que el proposa.

**Per a una anàlisi mensual cal tornar a demanar la divisió amb el rang d'anys
que interessi.** El corpus ho ha fet per al **2024-2025** a
[treball](../../../temes/societat/treball/treball.md#lestacionalitat).

## El 1966 i el 1967 no són ocupació

**97 assalariats el desembre del 1966, 117 el del 1967 i 4.914 el del 1968.**
**El salt no és econòmic: és el registre que comença.** **El corpus no cita els
dos primers anys com a mesura de l'ocupació andorrana.**

## «Origen» és nacionalitat d'origen

**La divisió 395 desglossa per país d'origen**, i **això no és nacionalitat
actual**: **un andorrà naturalitzat pot seguir comptat al seu país d'origen.**
**La font no ho aclareix** i **el corpus no en dedueix res sobre
naturalitzacions.**

**La nomenclatura de països conserva entrades històriques** —`ALEMANYA
ORIENTAL`, `UNIÓ SOVIÈTICA`—, **amb valors vius el 2025**: són **codis d'origen
que no s'han actualitzat**, no països existents.
