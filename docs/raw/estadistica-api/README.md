# L'API pública del Departament d'Estadística

**Trobada el 18-09-2026.** **2.709 taules estadístiques** consultables per HTTP
sense clau ni registre, en **JSON-stat 2.0**, **CSV**, **XLSX** i **SDMX 2.1**.

| | |
| --- | --- |
| **Base** | `https://sig.govern.ad/SIGDDE.Public/estadistiquesdades/api/` |
| **Dades** | `data?file=json-stat&idDivision=<id>&language=ca&variation=&startDate=<p>&endDate=<p>&series=&showColumns=<p,p,...>` |
| **Cerca** | `searchDivision?text=<text>&language=ca` |
| **Llicència** | **CC BY 4.0**, la mateixa que les notes de premsa (`../estadistica-poblacio/avis-legal-2026-09-13.txt`) |
| **Redistribució** | **sí**, amb atribució |
| **Script del harness** | `02-DOCS/raw/operations/gap-audit-scripts/estadistica_api.py` |

## Per què el corpus no la tenia

**Perquè buscava al lloc equivocat.** Tot el que el corpus havia fet amb
Estadística era **sondejar noms de fitxer de notes de premsa** al patró
`Files/Documents/Notes_premsa_noticies/<CODI>_<DATA>_A.pdf` —**74.272 + 39.672
peticions `HEAD`** en dos sondeigs.

**Les notes de premsa són el resum; l'API és la base de dades.** I **hi ha
arribat una nota-punter**: **A110 i A111** deien, després de remetre a
`www.govern.ad`, «**o bé, al web d'estadística: `www.estadistica.ad` a
l'apartat Estadístiques/Dades**». Seguint aquell apartat:

1. `www.estadistica.ad` és un **ArcGIS Hub**; el contingut real viu en un
   **`iframe`** servit per `sig.govern.ad/SIGDDE.Public`.
2. La pàgina de cada taula porta un enllaç **«Consulta API per a aquesta
   taula»**, que crida `POST /EstadistiquesDades/ApiQuery` i **retorna l'URL de
   l'API ja muntat**, amb els períodes vàlids d'aquella divisió.
3. Aquell URL respon **sense autenticació**.

**La regla que en surt**: **abans de sondejar noms de fitxer, mira si la font té
API.** Dos sondeigs de 113.944 peticions per arribar on un enllaç de la pàgina
portava directament.

## L'estructura del catàleg

El codi de divisió és jeràrquic. **Tres branques de primer nivell:**

| Codi | Taules | Àmbit |
| --- | ---: | --- |
| **01** | **1.127** | Població i societat |
| **02** | **1.239** | Economia |
| **03** | **343** | Territori i medi ambient |

I, al segon nivell:

| Codi | Taules | Primera taula |
| --- | ---: | --- |
| `0101` | 251 | Població total |
| `0102` | 187 | Nombre d'assalariats |
| `0103` | 64 | Estudiants escolars per centres |
| `0104` | 25 | Despesa pública en salut |
| `0105` | 108 | Llindars de pobresa |
| `0106` | 98 | Casos intervinguts |
| `0107` | 39 | Edificacions |
| `0108` | 90 | Efectius per tipologia |
| `0109` | 129 | Biblioteques |
| `0110` | 16 | Cens d'electors |
| `0111` | 120 | Entitats |
| `0201` | 20 | Estimació del PIB |
| `0202` | 399 | Resultats pressupostaris |
| `0203` | 107 | IPC |
| `0204` | 267 | Estoc d'empreses |
| `0205` | 446 | Ajudes públiques, agricultura, ramaderia |
| `0301` | 37 | Recurs hídric |
| `0303` | 306 | Població per sexe *(territorial)* |

## Els fitxers d'aquesta carpeta

| Fitxer | Què és |
| --- | --- |
| `catalog-divisions-2026-09-18.json` | Les **2.709** divisions amb `IdDivision`, codi i descripció, tal com les torna `searchDivision` |
| `catalog-divisions-2026-09-18.tsv` | El mateix, tabulat, per a `grep` |

**El catàleg s'ha obtingut per unió de cerques** (`a`, `e`, `i`, `o`, `u`, `de`,
`la`, `per`, `1`, `2`, `0`, `tot`, `nombre`, `%`, `·`): **cinc vocals ja en
donen 2.709 i cap consulta posterior no n'afegeix cap.** `No hi ha endpoint de
llistat complet documentat; el nombre 2.709 és un mínim comprovat, no un màxim
demostrat.`

## Com es fa servir

```
python3 02-DOCS/raw/operations/gap-audit-scripts/estadistica_api.py "produccio de tabac"
python3 02-DOCS/raw/operations/gap-audit-scripts/estadistica_api.py --serie 2404
```

El mòdul també s'importa: `search(text)`, `data(idDivision)` —JSON-stat sencer,
amb `source` i `updated`— i `serie(idDivision)` —parells `(període, valor)`.

**`api_url(idDivision)` és la peça que ho fa funcionar**: demana a la pàgina
mateixa quins períodes té aquella divisió, perquè **l'API retorna `400 Bad
Request` si `showColumns` no coincideix amb la periodicitat real de la taula.**

## Què s'ha bolcat, a 18-09-2026

**2.287 de les 2.709 divisions** —**el 84,4%**— i **771.854 valors**, en
**trenta carpetes**, **totes amb README de procedència, llicència i defectes
registrats**.

| Carpeta | Divisions | Valors |
| --- | ---: | ---: |
| `pressupostos` | 391 | 115.240 |
| `turisme-vehicles-energia` | 385 | 118.938 |
| `comparacio-internacional` | 298 | 50.726 |
| `empreses-sector-exterior` | 249 | 201.574 |
| `demografia-vital` | 191 | 55.358 |
| `salut-cultura-medi` | 189 | 12.437 |
| `qualitat-de-vida` | 153 | 4.073 |
| `treball-mercat` | 121 | 77.787 |
| `cultura` | 100 | 552 |
| `prestacions` | 91 | 5.583 |
| `seguretat` | 85 | 9.156 |
| `tic` | 78 | 6.158 |
| `educacio` | 64 | 21.905 |
| `pobresa` | 54 | 2.176 |
| `llengua` | 44 | 1.090 |
| `comuns` | 32 | 12.613 |
| `empreses` | 22 | 2.860 |
| `cura`, `pib` | 20 c/u | 56 · 7.963 |
| `accidents` | 17 | 1.395 |
| `eleccions` | 16 | 342 |
| `assalariats`, `caca-pesca` | 15 c/u | 28.345 · 860 |
| `allotjament`, `habitatges`, `hipoteques` | 14 c/u | 2.524 · 3.536 · 624 |
| `ipc`, `poblacio` | 12 c/u | 19.210 · 4.482 |
| `fiscalitat` | 10 | 3.990 |
| `infancia` | 7 | 301 |

`La suma de la columna «divisions» dona 2.733 i les divisions úniques són
2.287: algunes cauen sota dos prefixos i surten a dues carpetes.`

**El que queda sense bolcar és, sobretot**: **`0205` ajudes, permisos, vehicles
i allotjament (el que no ha entrat a `turisme-vehicles-energia`)**, **la resta
de `0101` població (251 divisions)**, **`0203` IPC detallat (107)**, **`0106`
(98)**, **`0108` (90)** i **`0107` (39)**.

## Dues regles d'ús que han costat de trobar

1. **Si els noms de sèrie arriben com a codis** —`0105020500070002`— **en
   json-stat i amb `language=ca`, demana la mateixa divisió amb `file=csv`**:
   els retorna escrits en català.
2. **Si l'API respon `500`, l'URL és massa llarg.** Una divisió mensual des del
   1966 genera un `showColumns` de 5.922 caràcters. **Retalla'l a un període per
   any** —els desembres—; **si encara falla amb `502`, retalla el rang d'anys.**

## Primer ús

**La sèrie de producció de tabac, 1973-2025, any per any** —cinquanta-tres
anys— que el corpus declarava com a buit perquè **la nota A107 només en
dibuixava un gràfic sense etiquetes**:
[quant tabac es cull avui](../../temes/economia/tabac/quant-tabac-es-cull-avui.md).
