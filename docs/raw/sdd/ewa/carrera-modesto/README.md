# Carrera / Modesto — materials bruts de recerca

Captura: 12 de setembre de 2026.

Aquest directori conserva les respostes i els documents originals emprats per
desambiguar `Carrera Gasol Modesto`, `Modest Carrera i Gasol` i el registre
francès `CARRERA, Modesto`. No és un corpus normalitzat: els HTML, JSON, CSV i
ZIP es mantenen com a evidència bruta, amb errors, camps buits i duplicats.

## Procedència

| Directori | Proveïdor i URL d'origen | Abast | Condicions conegudes |
|---|---|---|---|
| `adg/` | Arxiu Diocesà de Girona, <https://www.arxiuadg.org/index.php/arxius/parroquies> i API pública de <https://arxiubisbatgirona.org/> | Catàleg de Sant Cristòfol de Beget i descripció del llibre `B6`, 1881–1914 | Còpia de treball del catàleg. No s'ha obtingut ni redistribuït cap imatge del llibre; el visor requereix identificació. Drets de reproducció no determinats. |
| `censo-guia/` | Ministeri de Cultura, <https://censoarchivos.cultura.gob.es/CensoGuia/> | Fitxes HTML del fons `ES.8019.ATSJC/.6` i del centre custodial | Informació pública administrativa. Condicions específiques de reutilització no verificades; conservar com a evidència de recerca. |
| `gasol-1922/` | *Gaceta de Madrid* / BOE, <https://www.boe.es/gazeta/dias/1922/05/19/pdfs/GMD-1922-139.pdf> | Número 139 de 19/05/1922, OCR i render de la p. PDF 4 / p. impresa 652, on apareix `Modesto Carrera Gasol` | Publicació oficial històrica servida pel BOE. Còpia íntegra de preservació i derivats locals de lectura; conservar atribució. |
| `google-books/` | Google Books, volum `itqzHiFA0NYC`, <https://books.google.es/books?id=itqzHiFA0NYC>, i mostra bibliogràfica de GBV | Respostes JSON del cercador intern, fragments breus de l'índex i mostra de tres pàgines del *Libro Memorial* | Metadades, fragments de cerca i mostra pública, no una còpia del llibre. Subjectes a les condicions dels proveïdors i als drets de l'edició de 2006; no emprar com a text d'entrenament. |
| `local-beget/` | Càntut, Can Jeroni, Ajuntament de Camprodon / *Annals del CECR*, Arxiu Comarcal de la Garrotxa i FamilySearch | Control biogràfic de Joan Carrera i Molas, canvi `Baget`–`Beget`, relació d'encausats i via d'accés als registres municipals de Girona | Còpies de treball per a verificació. Els PDF i les pàgines conserven els drets i les condicions de cada editor; no s'incorporen automàticament a cap corpus d'entrenament. |
| `memoire-des-hommes/` | Ministère des Armées, <https://www.memoiredeshommes.defense.gouv.fr/conflits-operations/telechargement-des-bases> | Exportació oficial *Morts en déportation*, HTML de resultats i resposta del motor | La pàgina oficial autoritza la reutilització de les dades amb menció de la font i de la data d'actualització. ZIP ofert el 29/01/2026. |
| `memorial-democratic/` | Memorial Democràtic, <https://banc.memoria.gencat.cat/ca/results/deportats>, i descripció del fons <https://memoria.gencat.cat/ca/que-fem/banc-de-la-memoria/fons/deportats-catalans-i-espanyols-als-camps-nazis> | Resultat nominal i registres públics `deportats/2976`, `informant/15098`, tren, camps, kommandos, arxius i publicacions relacionades | Dades públiques d'un projecte del Memorial Democràtic, l'Amical de Mauthausen i la UPF. Conservar atribució; els paquets JavaScript de l'aplicació s'exclouen perquè incorporen codi de connexió que no cal redistribuir. |
| `pares/` | Ministeri de Cultura, Portal de Víctimes i <https://pares.cultura.gob.es/Deportados/servlets/ServletController> | Formularis, resultats de control, fitxa pública `495531` i cerques actuals per `Carrera`, `Modesto` i `Birba` | Còpies HTML de consulta pública. No contenen cookies ni credencials. Condicions específiques de reutilització no verificades. |
| `reparacio-juridica/` | Arxiu Nacional de Catalunya / Dades Obertes, <https://analisi.transparenciacatalunya.cat/api/v3/views/3bjt-k7vu/export.csv?accessType=DOWNLOAD> | Exportació completa de la llista de reparació jurídica, versió consultada el 12/09/2026 | Conjunt oficial de dades obertes; cal conservar l'atribució i la data de descàrrega. |

L'original `memoire-des-hommes/mdh-downloads.html` es conserva en aquest
directori de treball però queda exclòs del Git: la pàgina oficial incorpora un
token del seu proveïdor cartogràfic i la protecció de secrets n'impedeix, amb
raó, la publicació. El ZIP, la resposta JSON del motor i l'HTML de resultats no
contenen aquest valor i són suficients per auditar la descàrrega.

## Integritat dels originals principals

- `memoire-des-hommes/morts-en-deportation-2026-01-29.zip` — SHA-256
  `5300b4ef3419453ae4274b524d67cec4c2f2f05cb4bed931d7b7ec92003dbc7b`.
- `reparacio-juridica/reparacio-juridica-franquisme.csv` — SHA-256
  `816b300b365497d638912fe8e46587d1ef6803050b1ee8a827dc19c51494878c`.
- `gasol-1922/gaceta-madrid-1922-139.pdf` — SHA-256
  `fe4249e20158df743c36f7fb32ee37591d96b81dba70493370e1fb6a269e2588`.
- `google-books/libro-memorial-gbv-523923600.pdf` — SHA-256
  `5edefedec5b14dfb26957d3c4d3d68be0d5656961df9db620611dd7c832b53f7`.
- `memorial-democratic/deportat-2976-full.json` — SHA-256
  `16e124294ab9783565b2e7e80d9b439111bf128c730e2cf7453a376bcf3f8cf2`.
- `memorial-democratic/deportat-2976-person.json` — SHA-256
  `2654ffadddfcdc9a9b97c9b16810383dcffea55401d8ecb24997a3a4b401fcde`.

## Notes de lectura

- La fila objectiu de *Morts en déportation* és al fragment
  `memoire-des-hommes/mdh-morts-open-data/arko_default_6973304a3bc32_s0_9.csv`,
  línia física 6429.
- El ZIP oficial és la còpia canònica; el directori `mdh-morts-open-data/` és
  només l'extracció de treball que permet auditar l'esquema i els camps buits.
- El Banc de la Memòria Democràtica identifica el deportat com **Modesto
  Carrera Ramon**, registre `2976` i persona `15098`: naixement a Beget el
  20/12/1910, darrera residència a Saint-Marsal i mort a Dautmergen el
  07/04/1945. Les seves referències bibliogràfiques acoten el *Libro Memorial*
  a la p. 471 i el *Livre-mémorial* francès a la p. II-913.
- La seqüència publicada pel Banc associa Dachau (`74159`), Buchenwald
  (`75367`), Natzweiler-Struthof, Emma, Wöbbelin i Dautmergen. Les dates i la
  geografia presenten tensions internes; els JSON conserven la resposta sense
  corregir-la i cal contrastar-la amb els arxius citats pel mateix registre.
- La *Gaceta de Madrid* de 1922 situa **Modesto Carrera Gasol** entre els
  soldats del Tercio de extranjeros amb minoria d'edat i manca de consentiment
  comprovades. No dona filiació ni data de naixement i no s'ha de fusionar
  automàticament amb l'agent republicà de 1938, però és incompatible en
  cronologia ordinària amb Carrera Ramon, que aleshores tenia onze anys.
- El cercador antic de deportats de PARES no retorna Modesto Carrera en les
  cerques actuals per cognom o nom, tot i que el Portal de Víctimes conserva la
  fitxa `495531`. Aquesta divergència s'ha preservat, no interpretat com una
  supressió editorial demostrada.
- Cap absència en aquestes exportacions s'ha d'interpretar com una prova
  universal d'absència documental.
