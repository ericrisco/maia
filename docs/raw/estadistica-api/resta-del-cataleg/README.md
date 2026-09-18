# La resta del catàleg — API del Departament d'Estadística

**Baixat el 18-09-2026.** **No és una branca temàtica: són totes les divisions
del catàleg que cap de les trenta carpetes anteriors no havia agafat**, siguin
del prefix que siguin.

| | |
| --- | --- |
| **Fitxer** | `resta-cataleg-api-2026-09-18.tsv` (103 MB) |
| **Divisions demanades** | **422** |
| **Divisions amb dades** | **388** |
| **Taules** | **388** |
| **Valors** | **611.952** |
| **Divisions KO** | **16** |

## Font i drets

- **Departament d'Estadística del Govern d'Andorra**,
  `https://sig.govern.ad/SIGDDE.Public/estadistiquesdades/api/`.
- **Llicència: CC BY 4.0.** Atribució obligatòria al Departament d'Estadística.
- Fitxa de font del corpus: `docs/fonts/estadistica-ad.md`.

## Columnes

`idDivision · taula · codi · serie · periode · valor` — valors normalitzats de
`1.234,56` a `1234.56`.

## Què hi ha, per volum

| Família | Valors |
| --- | ---: |
| **Comerç exterior** (importacions i exportacions per capítol, país i quantitat) | **194.014** |
| **IPC i índexs de preus** (subgrups i classes, bases 2001 i 2021, variacions) | **130.479** |
| **Infraccions** (denunciades i resoltes, per article i per lloc) | **118.012** |
| **Població** (per parròquia, edat en trams d'un any, sexe i nacionalitat) | **58.107** |
| **Immigració i autoritzacions** (en vigor, per tipus, edat i temps de residència) | **53.228** |
| Altres | 58.112 |

**La taula més gran de totes és `INFRACCIONS DENUNCIADES PER LLOC I ARTICLE`**,
amb **94.490 valors**.

## Les setze divisions que no responen

**Totes van donar `TimeoutError` dues vegades seguides o `502`**, amb el mateix
client que ha baixat les altres 388:

| idDivision | Taula |
| ---: | --- |
| 70, 71 | **Exportacions per països**, en valor i en quantitat |
| 76, 77 | **Importacions per països**, en valor i en quantitat |
| 391, 402, 411 | Assalariats, massa salarial i salari mitjà **per sector i edat** |
| 778-783 | Assalariats, massa salarial i salari mitjà **per sexe** i per sector i sexe |
| 246, 247 | Abonaments per servei i tràfic telefònic |
| 558 | **Autoritzacions d'immigració d'hivern acordades per quota** |

`Són les taules més grosses del catàleg: l'URL que l'API genera per a elles
supera el que el servidor tolera. La regla del corpus per a aquests casos
—retallar columnes i després anys— no s'hi ha aplicat en aquesta tanda.
Segueixen obertes.`

**Les de comerç exterior per països i les de salaris per sexe són les dues
absències que més pesen**: **la primera diria amb qui comercia Andorra i la
segona és la desagregació per sexe de la massa salarial**, que el corpus té per
altres talls
(`docs/raw/estadistica-api/treball-mercat/`).

## Advertències d'ús

- **Els índexs de preus hi són amb dues bases, 2001 i 2021, i no s'encadenen.**
- **Les taules d'infraccions per article donen el número d'article del Codi
  penal i el seu enunciat**, en una jerarquia de tres nivells
  (`1. Delictes` → `1.14. Seguretat col·lectiva` → `1.14.268. Conducció sota
  l'efecte de drogues`). **Els nivells se solapen: sumar totes les files d'una
  taula compta la mateixa infracció tres vegades.**
- **Les taules de població per trams d'un any són les úniques que permeten
  construir piràmides**; la resta del corpus fa servir trams quinquennals.
