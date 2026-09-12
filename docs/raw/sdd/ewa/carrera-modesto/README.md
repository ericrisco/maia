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
| `google-books/` | Google Books, volum `itqzHiFA0NYC`, <https://books.google.es/books?id=itqzHiFA0NYC> | Respostes JSON del cercador intern i fragments breus de l'índex | Metadades i fragments de cerca, no una còpia del llibre. Subjectes a les condicions de Google Books i als drets de l'edició de 2006; no emprar com a text d'entrenament. |
| `local-beget/` | Càntut, Can Jeroni, Ajuntament de Camprodon / *Annals del CECR*, Arxiu Comarcal de la Garrotxa i FamilySearch | Control biogràfic de Joan Carrera i Molas, canvi `Baget`–`Beget`, relació d'encausats i via d'accés als registres municipals de Girona | Còpies de treball per a verificació. Els PDF i les pàgines conserven els drets i les condicions de cada editor; no s'incorporen automàticament a cap corpus d'entrenament. |
| `memoire-des-hommes/` | Ministère des Armées, <https://www.memoiredeshommes.defense.gouv.fr/conflits-operations/telechargement-des-bases> | Exportació oficial *Morts en déportation*, HTML de resultats i resposta del motor | La pàgina oficial autoritza la reutilització de les dades amb menció de la font i de la data d'actualització. ZIP ofert el 29/01/2026. |
| `pares/` | Ministeri de Cultura, <https://pares.cultura.gob.es/victimasGCFPortal/> | Formularis, resultats de control i fitxa pública `495531` | Còpies HTML de consulta pública. No contenen cookies ni credencials. Condicions específiques de reutilització no verificades. |
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

## Notes de lectura

- La fila objectiu de *Morts en déportation* és al fragment
  `memoire-des-hommes/mdh-morts-open-data/arko_default_6973304a3bc32_s0_9.csv`,
  línia física 6429.
- El ZIP oficial és la còpia canònica; el directori `mdh-morts-open-data/` és
  només l'extracció de treball que permet auditar l'esquema i els camps buits.
- Cap absència en aquestes exportacions s'ha d'interpretar com una prova
  universal d'absència documental.
