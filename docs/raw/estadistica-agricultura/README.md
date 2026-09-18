# Estadística d'agricultura — evidència primària

Consulta del **18-09-2026**. Provinença registrada a
`02-DOCS/raw/sources/estadistica-ad.md` i a `docs/fonts/estadistica-ad.md`.
Informació estadística pròpia del Departament sota **CC BY 4.0** segons l'avís
legal conservat a `docs/raw/estadistica-poblacio/avis-legal-2026-09-13.txt`;
els articles n'atribueixen autoria i data.

| Fitxer | Procedència | Lectura |
| --- | --- | --- |
| [a107-2025-07-21.pdf](a107-2025-07-21.pdf) · [text](a107-2025-07-21.txt) | [PDF original](https://sig.govern.ad/SIGDDE.Public/Files/Documents/Notes_premsa_noticies/A107_20250721_A.pdf), nota `NP_A107_20250721`, publicació **21-07-2025**, referència **any 2024** | Resum, §1.1 i §1.2 llegits i comprovats aritmèticament; nota metodològica llegida |
| [a112-2026-05-26.pdf](a112-2026-05-26.pdf) · [text](a112-2026-05-26.txt) | [PDF original](https://sig.govern.ad/SIGDDE.Public/Files/Documents/Notes_premsa_noticies/A112_20260526_A.pdf), nota `NP_A112_20260526`, publicació **26-05-2026**, referència **any 2025** | Els onze fulls llegits sencers: §1.1, §1.2, §1.3, §2, §3 i la metodologia. Totes les taules comprovades aritmèticament |
| [a106-2025-05-27.pdf](a106-2025-05-27.pdf) · [text](a106-2025-05-27.txt) | [PDF original](https://sig.govern.ad/SIGDDE.Public/Files/Documents/Notes_premsa_noticies/A106_20250527_A.pdf), nota `NP_A106_20250527`, publicació **27-05-2025**, referència **any 2024** | Full únic llegit sencer. **No conté cap dada**: remet a un enllaç |
| [a109-2025-05-27.pdf](a109-2025-05-27.pdf) · [text](a109-2025-05-27.txt) | [PDF original](https://sig.govern.ad/SIGDDE.Public/Files/Documents/Notes_premsa_noticies/A109_20250527_A.pdf), nota `NP_A109_20250527`, publicació **27-05-2025**, referència **any 2024** | Full únic llegit sencer. **No conté cap dada**: remet a un enllaç |

## Com s'ha trobat

**El catàleg del Pla estadístic** (`docs/raw/estadistica-pla/catalog-activitats-2026.md`)
dona el codi **A107, «Estadística sobre produccions dels cultius»**, i el
calendari del 17-09-2026 no en tenia cap data. **S'ha sondejat el patró d'URL
per dates**, primer sobre el 2026 —sense resultat— i després sobre el 2025:
**`A107_20250721_A.pdf`**. **A106 i A109 s'han localitzat el 18-09-2026**, en un segon sondeig
del 01-06-2024 al 30-09-2025 —1.041 peticions `HEAD`, només dies feiners—:
**totes dues són del `20250527`**. **El sondeig exhaustiu anterior no les tenia
perquè la seva finestra començava l'01-10-2025**, i elles són de cinc mesos
abans. **A105 segueix sense localitzar.**

## A106 i A109 no contenen cap dada

**Les dues notes són d'una pàgina i no en donen ni una xifra.** Citen
l'article 33 i l'article 37.5.a de la Llei 2/2013 i acaben: «**Les dades es
poden consultar al següent enllaç**». **El mateix fenomen que el corpus ja
tenia registrat per A070 i A071**: la nota de premsa no publica, remet.

L'enllaç és invisible al text extret —és una anotació del PDF—. S'ha tret amb
`re.finditer(rb'/URI\s*\((.*?)\)', pdf, re.S)`, i les dues notes donen el
mateix destí:

```
https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-medi-ambient-agricultura-i-ramaderia/agricultura-i-ramaderia/estadistiques
```

## On són les dades de debò

**En aquella pàgina, i no a `estadistica.ad`.** És una pàgina de Liferay que
serveix un esquelet de 1,4 MB; els enllaços no són `.pdf` sinó
`www.govern.ad/documents/d/guest/<nom>?download=true`, i **la pàgina té 174
documents** repartits en tres registres:

| Registre | Sèries | Anys |
| --- | --- | --- |
| **Registre d'Explotacions Agràries** | Tipus d'explotacions · Explotacions i superfície de conreu per parròquia · Gràfic de superfícies · Piràmide d'edats de titulars i delegats · Activitat apícola · Superfície per categoria agrícola harmonitzada | fins a **2003** enrere segons la sèrie |
| **Padral** | Evolució de la cabana ramadera · Caps de bestiar per parròquia | **1988-2026** i **2003-2026** |
| **Ramaders d'Andorra** | Vedells, bous, corders i equins sacrificats per mesos, evolució i històric | **1999-2019**, aturat |

**El sacrifici s'atura el 2019 en totes quatre espècies.** No hi ha fitxer del
2020 ençà. Registrat, no explicat.

## Drets: l'enllaç porta d'una llicència oberta a una de tancada

**Les notes A106 i A109 són del Departament d'Estadística, que publica sota
CC BY 4.0.** L'enllaç que donen porta a `www.govern.ad`, **l'avís legal del
qual reserva els drets**: «no es podran fer actes totals o parcials de
reproducció, publicació, tractament informàtic, distribució, difusió,
transformació, compilació, modificació, distribució o comunicació pública dels
webs sense el consentiment previ i per escrit del Govern», i «els usuaris
només podran fer un ús privat i personal dels continguts».

**La difusió d'una estadística pública, manada per l'article 37.5.a de la Llei
2/2013, acaba en un portal que en prohibeix la redistribució.** Registrat com
a fet, sense judici.

Conseqüència pràctica, i s'aplica: **els set fitxers descarregats del
Departament d'Agricultura no es versionen** —hi ha regla a `.gitignore`—,
segons [govern-andorra-web](../../fonts/govern-andorra-web.md),
`redistribucio: no`. **Els articles en citen les xifres amb atribució**, que és
el que la fitxa de font permet.

### Els set fitxers consultats el 18-09-2026

| Fitxer local | Origen | SHA-256 (16) |
| --- | --- | --- |
| `explotacions-tipus-2025.pdf` | `documents/d/guest/explotacions_2025` | `a5ebb28618d99712` |
| `superficie-conreu-parroquia-2025.pdf` | `documents/d/guest/superficie_cultius_annuals_2025` | `f12289a96f2f4bc9` |
| `superficie-categoria-harmonitzada-2025.pdf` | `documents/d/guest/superficie-segons-categoria-agricola_2025` | `85fb0a437df7dd32` |
| `evolucio-cabana-1988-2026.pdf` | `documents/d/guest/evolucio_bestiar_1988_2026-1` | `c17328bd3dea259d` |
| `bestiar-parroquia-2026.pdf` | `documents/d/guest/bestiar_per_parroquia_2026` | `b01c83a275145683` |
| `piramide-edats-2025.pdf` | `documents/d/guest/piramide_edats_2025` | `23c17fd2016e4a5d` |
| `apicultura-2025.pdf` | `documents/d/guest/apicultura_2025` | `8ae27d0535f8e7b5` |

Tots set porten `?download=true` al final de l'URL i tots set s'han extret amb
`pdftotext -layout`.

## Comprovacions fetes

- **Les columnes de 1990, 2000, 2010 i 2023 sumen exactament el seu total.**
- **La columna del 2024 suma 109.039 i el total imprès és 109.038**:
  **un quilogram d'arrodoniment**, registrat i no corregit.
- **El text del resum atribueix un −28,6% a Sant Julià de Lòria**; **la taula el
  dona a Escaldes-Engordany**, i **Sant Julià hi surt amb un −1,9%**.
  **Discrepància del document amb ell mateix, registrada i no corregida.**

### A112

- **Les set parròquies sumen exactament 340 explotacions.**
- **Les vuit línies d'ajut del 2025 sumen exactament 3.595.108 €**, i amb els
  comuns, **3.709.026 €**. **Les quatre sublínies de qualitat controlada sumen
  exactament 452.439 €**, i **la producció ecològica, 21.498 €**.
- **Tres sumes fallen per un euro**: l'ajut de muntanya per parròquia (2.376.329
  contra 2.376.328), el dall dels prats (403.729 contra 403.728) i el total de
  les vuit línies del 2024 (3.230.135 contra 3.230.134). **Arrodoniment,
  registrat i no corregit.**
- **El resum diu 0,1% del PIB nominal i la taula de ràtios diu 0,09%.**
  Registrat.
- **La nota adverteix que la partida dels comuns d'Ordino i Sant Julià és
  supòsit**, no liquidació, i que **la dada comunal del 2024 s'ha corregit**
  respecte de l'edició anterior. **La sèrie comunal no és comparable entre
  edicions.**
- **La paraula «tabac» no surt cap vegada** en els onze fulls.

## La sèrie de superfícies de conreu, 2004-2025

**Vint-i-dues edicions descarregades el 18-09-2026** de
`documents/d/guest/superficie_cultius_annuals_<any>` i variants
(`superficie_conreu_<any>`, i els anys sols `2004`…`2018` per als més antics),
extretes amb `pdftotext -layout` a `serie-conreu/`. **No es versionen**, per la
mateixa raó de drets que la resta: `.gitignore` les exclou.

**Totes vint-i-dues tenen la mateixa estructura** —fila «Total país» amb
explotacions, dall, tabac, peixeder, patates, hort, erm, altres, total i SAU—
**amb columnes que apareixen i desapareixen** (`Pam` només del 2011 al 2016,
`Vinya` des del 2011, `Varis` des del 2009). **La columna del tabac hi és els
vint-i-dos anys.**

Destil·lada a
[Cent hectàrees de tabac](../../temes/economia/tabac/cent-hectarees-de-tabac.md):
**−45,0% de terra de tabac del 2004 al 2025**, **−11,5% el sol any 2020** —la
caiguda més gran de la sèrie, i **el mateix any del mínim històric de collita**—,
i **superfície declarada total pràcticament estable** (+0,9%), amb el peixeder
guanyant el que perden el tabac i el dall.
