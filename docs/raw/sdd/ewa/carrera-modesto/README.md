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
| `dachau-gedenkbuch/` | KZ-Gedenkstätte Dachau, <https://gedenkbuch.kz-gedenkstaette-dachau.de/en> | Portada, codi públic de consulta i controls nominals del llibre digital de morts | Còpies HTML/JS de treball. El resultat negatiu només descriu el cercador i la versió consultats; no és una prova universal d'absència. No emprar el codi com a corpus d'entrenament. |
| `gasol-1922/` | *Gaceta de Madrid* / BOE, <https://www.boe.es/gazeta/dias/1922/05/19/pdfs/GMD-1922-139.pdf> | Número 139 de 19/05/1922, OCR i render de la p. PDF 4 / p. impresa 652, on apareix `Modesto Carrera Gasol` | Publicació oficial històrica servida pel BOE. Còpia íntegra de preservació i derivats locals de lectura; conservar atribució. |
| `google-books/` | Google Books, volum `itqzHiFA0NYC`, <https://books.google.es/books?id=itqzHiFA0NYC>, i mostra bibliogràfica de GBV | Respostes JSON del cercador intern, fragments breus de l'índex i mostra de tres pàgines del *Libro Memorial* | Metadades, fragments de cerca i mostra pública, no una còpia del llibre. Subjectes a les condicions dels proveïdors i als drets de l'edició de 2006; no emprar com a text d'entrenament. |
| `itinerari/` | Mémorial du KL Natzweiler-Struthof, KZ-Gedenkstätte Neuengamme i Association Française Buchenwald Dora et Kommandos | Històries institucionals o memorials de Dautmergen, Wöbbelin i Emma/Eisenach | Còpies HTML de treball per contrastar cronologies i dependències administratives. Condicions específiques de reutilització no verificades; no emprar com a corpus d'entrenament. |
| `local-beget/` | Càntut, Can Jeroni, Ajuntament de Camprodon / *Annals del CECR*, Arxiu Comarcal de la Garrotxa i FamilySearch | Control biogràfic de Joan Carrera i Molas, canvi `Baget`–`Beget`, relació d'encausats i via d'accés als registres municipals de Girona | Còpies de treball per a verificació. Els PDF i les pàgines conserven els drets i les condicions de cada editor; no s'incorporen automàticament a cap corpus d'entrenament. |
| `memoire-des-hommes/` | Ministère des Armées, <https://www.memoiredeshommes.defense.gouv.fr/conflits-operations/telechargement-des-bases> | Exportació oficial *Morts en déportation*, HTML de resultats i resposta del motor | La pàgina oficial autoritza la reutilització de les dades amb menció de la font i de la data d'actualització. ZIP ofert el 29/01/2026. |
| `memorial-democratic/` | Memorial Democràtic, <https://banc.memoria.gencat.cat/ca/results/deportats>, i descripció del fons <https://memoria.gencat.cat/ca/que-fem/banc-de-la-memoria/fons/deportats-catalans-i-espanyols-als-camps-nazis> | Resultat nominal i registres públics `deportats/2976`, `informant/15098`, tren, camps, kommandos, arxius i publicacions relacionades | Dades públiques d'un projecte del Memorial Democràtic, l'Amical de Mauthausen i la UPF. Conservar atribució; els paquets JavaScript de l'aplicació s'exclouen perquè incorporen codi de connexió que no cal redistribuir. |
| `memorialgenweb/` | MemorialGenWeb, <https://www.memorialgenweb.org/memorial3/deportes/complement.php?id=89352> | Cercador i fitxa derivada `D-89352`, amb comboi, matrícula, referència bibliogràfica i remissió al JORF | Base memorialística col·laborativa, usada com a índex de descoberta i no com a substitut del JORF o dels expedients originals. Conservar atribució; no emprar com a corpus d'entrenament. |
| `legifrance/` | Légifrance, <https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000031047545> | Nota de procedència de la rectificació oficial de 2015; el servidor rebutjà la descàrrega automatitzada amb HTTP 403 | Metadades i resum de treball amb enllaç canònic, no una còpia del JORF. La grafia nominal es conserva literalment. |
| `shd-caen/` | Service historique de la Défense, <https://www.servicehistorique.sga.defense.gouv.fr/ark/97871> | Cerca nominal i descripció del dossier `AC 21 P 433618`, més context institucional de la sèrie | Catàleg públic, no reproducció del dossier. Condicions específiques de reutilització no verificades; conservar com a evidència de localització. |
| `saint-marsal/` | Archives départementales des Pyrénées-Orientales i FranceArchives | Vies de consulta del cens de 1936 de Saint-Marsal i resposta antirobot d'una cerca nominal | Les pàgines institucionals són còpies de treball. La resposta antirobot no és un resultat de cerca; no emprar com a corpus d'entrenament. |
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
- `itinerari/buchenwald-eisenach-emma.html` — SHA-256
  `14eaaaead8261c1e631bb6b5bbd9cad70db8ba5e8500f22feefe20d7f4d8f23f`.
- `itinerari/neuengamme-woebbelin.html` — SHA-256
  `18aedf03709795b25456340eee0b72e77a94eab71aba6b20263e3e526d6b9d22`.
- `itinerari/struthof-dautmergen-schoerzingen.html` — SHA-256
  `7c6d03198d3e374ae4b6f0d4d796e206cc3b3d1474d2a5b5016cf8353da61e06`.
- `memorialgenweb/deporte-carrera-modesto-courado-89352.html` — SHA-256
  `dd626828de5b9613de19ac966d44151b5ac909bf01becee36cac6d2291f8a3a2`.
- `shd-caen/dossier-carrera-modesto-ac21p433618.html` — SHA-256
  `e81c9995a3bced73904ac0878db7cb052203b6d3375707c39633ed416d500978`.
- `dachau-gedenkbuch/search-carrera.html` — SHA-256
  `9217766d314d54953f62febe95d2085111bd89c47250c1d4b4f4a9218d12b842`.

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
- Les històries dels camps confirmen que `Emma` era Eisenach/Dürrerhof, vinculat
  a Buchenwald i BMW, i situen el seu tancament cap al 16/02/1945: no encaixa
  amb l'entrada `07/03` del Banc. Wöbbelin era un camp satèl·lit de Neuengamme,
  actiu des del 12/02; Dautmergen era un annex de Natzweiler, evacuat el 18/04.
  Aquest contrast eleva la probabilitat d'una data o relació defectuosa a la
  base, però no substitueix la fitxa individual del presoner.
- La *Gaceta de Madrid* de 1922 situa **Modesto Carrera Gasol** entre els
  soldats del Tercio de extranjeros amb minoria d'edat i manca de consentiment
  comprovades. No dona filiació ni data de naixement i no s'ha de fusionar
  automàticament amb l'agent republicà de 1938, però és incompatible en
  cronologia ordinària amb Carrera Ramon, que aleshores tenia onze anys.
- El cercador antic de deportats de PARES no retorna Modesto Carrera en les
  cerques actuals per cognom o nom, tot i que el Portal de Víctimes conserva la
  fitxa `495531`. Aquesta divergència s'ha preservat, no interpretat com una
  supressió editorial demostrada.
- El JORF de 2015 rectifica oficialment la mort de `Carrera (Modesto, Courado,
  Amédée)`, nascut el mateix dia a Baget, de Dachau 18/11/1944 a Dachau
  29/04/1945. El Banc publica Dautmergen 07/04/1945: són finals incompatibles,
  no variants fusionables. El dossier que pot explicar la rectificació és
  `AC 21 P 433618` a Caen; el catàleg públic en confirma nom i naixement, però
  deixa la defunció buida.
- El llibre digital de morts de Dachau no retorna les variants nominals, el
  lloc de naixement ni la matrícula `74159` en les cerques conservades. És un
  negatiu acotat a aquesta font i versió, no una prova que Carrera fos viu.
- Cap absència en aquestes exportacions s'ha d'interpretar com una prova
  universal d'absència documental.
