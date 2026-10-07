# Cobertura de Maia Knowledge

Informe generat amb `scripts/build_coverage_inventory.py`.
La cobertura és per document citat i és només un límit inferior: una cita no prova que totes les seccions, files o afirmacions del document tinguin conversa.

## Inventari

- Fitxers Markdown a `docs/temes/`: **1477**.
- Fitxes factuals (`type: article`): **1348**.
- Índexs (`type: index`): **129**; s'usen per navegar, no com a font factual autònoma.
- Seccions: **11884**.
- Files de taula incloent capçaleres: **19056**.
- Elements de llista: **14348**.
- Enllaços Markdown: **17005**.

## Cobertura citada per tema principal

| Tema | Fitxes article | Amb conversa citada | Sense conversa citada |
|---|---:|---:|---:|
| `costums` | 23 | 3 | 20 |
| `cultura` | 72 | 8 | 64 |
| `economia` | 95 | 0 | 95 |
| `esports` | 272 | 0 | 272 |
| `gastronomia` | 15 | 0 | 15 |
| `historia` | 226 | 1 | 225 |
| `institucions` | 338 | 0 | 338 |
| `llengua` | 43 | 0 | 43 |
| `persones` | 43 | 0 | 43 |
| `politica` | 19 | 0 | 19 |
| `societat` | 142 | 0 | 142 |
| `territori` | 49 | 0 | 49 |
| `vida-quotidiana` | 11 | 0 | 11 |

## Backlog per branca del corpus

Aquest índex més fi permet avançar branca per branca. `Amb conversa` segueix sent una mesura documental, no una garantia que tots els fets de la branca estiguin ensenyats.

| Branca (`tema`) | Fitxes | Amb conversa citada | Sense conversa | Drets sí* | Pendents* | No* | Falta registre* |
|---|---:|---:|---:|---:|---:|---:|---:|
| `temes/costums/calendari-festiu` | 2 | 0 | 2 | 0 | 0 | 2 | 0 |
| `temes/costums/caramelles` | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| `temes/costums/danses` | 7 | 3 | 4 | 3 | 1 | 3 | 0 |
| `temes/costums/falles` | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| `temes/costums/festes-majors` | 2 | 0 | 2 | 0 | 0 | 2 | 0 |
| `temes/costums/gegants` | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| `temes/costums/meritxell` | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| `temes/costums/religiositat` | 5 | 0 | 5 | 2 | 3 | 0 | 0 |
| `temes/costums/ritus-de-pas` | 2 | 0 | 2 | 0 | 1 | 1 | 0 |
| `temes/costums/sant-antoni` | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| `temes/cultura` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/cultura/andorra-vista-de-fora` | 6 | 0 | 6 | 1 | 5 | 0 | 0 |
| `temes/cultura/arquitectura` | 11 | 5 | 6 | 5 | 5 | 1 | 0 |
| `temes/cultura/artesania` | 2 | 0 | 2 | 0 | 2 | 0 | 0 |
| `temes/cultura/arts-visuals` | 8 | 2 | 6 | 3 | 5 | 0 | 0 |
| `temes/cultura/cultura-popular` | 2 | 0 | 2 | 1 | 1 | 0 | 0 |
| `temes/cultura/literatura` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/cultura/llegendes` | 10 | 0 | 10 | 6 | 1 | 3 | 0 |
| `temes/cultura/museus-i-arxius` | 15 | 0 | 15 | 11 | 4 | 0 | 0 |
| `temes/cultura/museus-i-arxius/museus` | 11 | 1 | 10 | 10 | 0 | 1 | 0 |
| `temes/cultura/musica-i-cancons` | 3 | 0 | 3 | 0 | 2 | 1 | 0 |
| `temes/cultura/teatre` | 2 | 0 | 2 | 0 | 2 | 0 | 0 |
| `temes/economia/banca-i-fiscalitat` | 33 | 0 | 33 | 12 | 18 | 3 | 0 |
| `temes/economia/comerc` | 17 | 0 | 17 | 12 | 5 | 0 | 0 |
| `temes/economia/energia-i-serveis` | 4 | 0 | 4 | 2 | 2 | 0 | 0 |
| `temes/economia/les-grans-families` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/economia/ramaderia-i-agricultura` | 11 | 0 | 11 | 2 | 8 | 1 | 0 |
| `temes/economia/tabac` | 5 | 0 | 5 | 3 | 1 | 1 | 0 |
| `temes/economia/transformacio-economica` | 10 | 0 | 10 | 7 | 2 | 1 | 0 |
| `temes/economia/transport` | 5 | 0 | 5 | 5 | 0 | 0 | 0 |
| `temes/economia/turisme-i-neu` | 4 | 0 | 4 | 2 | 2 | 0 | 0 |
| `temes/economia/turisme-i-neu/estacions` | 5 | 0 | 5 | 5 | 0 | 0 | 0 |
| `temes/esports/altres-esports` | 32 | 0 | 32 | 31 | 1 | 0 | 0 |
| `temes/esports/competicio` | 7 | 0 | 7 | 6 | 1 | 0 | 0 |
| `temes/esports/escacs` | 5 | 0 | 5 | 5 | 0 | 0 | 0 |
| `temes/esports/esqui` | 2 | 0 | 2 | 1 | 1 | 0 | 0 |
| `temes/esports/esqui/esquiadors` | 31 | 0 | 31 | 31 | 0 | 0 | 0 |
| `temes/esports/estiu` | 32 | 0 | 32 | 32 | 0 | 0 | 0 |
| `temes/esports/formacio-esportiva` | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| `temes/esports/futbol` | 98 | 0 | 98 | 98 | 0 | 0 | 0 |
| `temes/esports/futbol/clubs-i-competicions` | 6 | 0 | 6 | 6 | 0 | 0 | 0 |
| `temes/esports/futbol/femeni` | 43 | 0 | 43 | 43 | 0 | 0 | 0 |
| `temes/esports/seleccions` | 15 | 0 | 15 | 9 | 0 | 6 | 0 |
| `temes/gastronomia/begudes` | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| `temes/gastronomia/calendari-gastronomic` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/gastronomia/historia-alimentaria` | 5 | 0 | 5 | 0 | 5 | 0 | 0 |
| `temes/gastronomia/plats` | 5 | 0 | 5 | 3 | 2 | 0 | 0 |
| `temes/gastronomia/productes` | 2 | 0 | 2 | 1 | 1 | 0 | 0 |
| `temes/gastronomia/rebosteria` | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| `temes/historia/antic-regim` | 50 | 0 | 50 | 13 | 30 | 7 | 0 |
| `temes/historia/constitucio-1993` | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| `temes/historia/contraban` | 2 | 0 | 2 | 1 | 1 | 0 | 0 |
| `temes/historia/democratitzacio` | 3 | 0 | 3 | 2 | 1 | 0 | 0 |
| `temes/historia/edat-mitjana` | 42 | 0 | 42 | 18 | 22 | 2 | 0 |
| `temes/historia/guerres-i-neutralitat` | 22 | 0 | 22 | 3 | 18 | 1 | 0 |
| `temes/historia/historia-recent` | 7 | 0 | 7 | 6 | 1 | 0 | 0 |
| `temes/historia/historiografia` | 11 | 0 | 11 | 4 | 6 | 1 | 0 |
| `temes/historia/manual-digest` | 5 | 0 | 5 | 2 | 3 | 0 | 0 |
| `temes/historia/moments-historics` | 2 | 0 | 2 | 0 | 2 | 0 | 0 |
| `temes/historia/origens` | 15 | 0 | 15 | 4 | 3 | 8 | 0 |
| `temes/historia/pareatge` | 6 | 1 | 5 | 2 | 4 | 0 | 0 |
| `temes/historia/segle-xix` | 29 | 0 | 29 | 19 | 8 | 2 | 0 |
| `temes/historia/segle-xx-primera-meitat` | 30 | 0 | 30 | 9 | 6 | 15 | 0 |
| `temes/institucions/comuns-i-parroquies` | 35 | 0 | 35 | 6 | 29 | 0 | 0 |
| `temes/institucions/consell-general` | 84 | 0 | 84 | 4 | 79 | 1 | 0 |
| `temes/institucions/coprincipat` | 33 | 0 | 33 | 5 | 28 | 0 | 0 |
| `temes/institucions/govern` | 8 | 0 | 8 | 6 | 1 | 1 | 0 |
| `temes/institucions/justicia` | 138 | 0 | 138 | 24 | 113 | 1 | 0 |
| `temes/institucions/nacionalitat-i-residencia` | 18 | 0 | 18 | 10 | 8 | 0 | 0 |
| `temes/institucions/patrimoni-institucional` | 6 | 0 | 6 | 1 | 4 | 1 | 0 |
| `temes/institucions/petits-estats` | 2 | 0 | 2 | 0 | 2 | 0 | 0 |
| `temes/institucions/quarts-i-veinats` | 2 | 0 | 2 | 0 | 2 | 0 | 0 |
| `temes/institucions/relacions-exteriors` | 8 | 0 | 8 | 6 | 1 | 1 | 0 |
| `temes/institucions/simbols` | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| `temes/llengua/contacte-de-llengues` | 5 | 0 | 5 | 0 | 1 | 4 | 0 |
| `temes/llengua/dialectologia` | 4 | 0 | 4 | 0 | 4 | 0 | 0 |
| `temes/llengua/fonetica` | 2 | 0 | 2 | 0 | 2 | 0 | 0 |
| `temes/llengua/fraseologia` | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| `temes/llengua/historia-de-la-llengua` | 3 | 0 | 3 | 0 | 1 | 2 | 0 |
| `temes/llengua/lexic-andorra` | 3 | 0 | 3 | 0 | 2 | 1 | 0 |
| `temes/llengua/manlleus` | 4 | 0 | 4 | 0 | 2 | 2 | 0 |
| `temes/llengua/morfosintaxi` | 3 | 0 | 3 | 0 | 3 | 0 | 0 |
| `temes/llengua/onomastica` | 3 | 0 | 3 | 0 | 3 | 0 | 0 |
| `temes/llengua/politica-linguistica` | 13 | 0 | 13 | 2 | 4 | 7 | 0 |
| `temes/llengua/registres` | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| `temes/llengua/tractament` | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| `temes/persones` | 43 | 0 | 43 | 24 | 10 | 8 | 1 |
| `temes/politica/identitat-politica` | 3 | 0 | 3 | 0 | 3 | 0 | 0 |
| `temes/politica/parlamentarisme` | 4 | 0 | 4 | 0 | 4 | 0 | 0 |
| `temes/politica/partits` | 3 | 0 | 3 | 3 | 0 | 0 | 0 |
| `temes/politica/sistema-electoral` | 9 | 0 | 9 | 4 | 5 | 0 | 0 |
| `temes/societat` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/societat/associacionisme` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/societat/demografia` | 15 | 0 | 15 | 7 | 6 | 2 | 0 |
| `temes/societat/dones` | 7 | 0 | 7 | 3 | 4 | 0 | 0 |
| `temes/societat/educacio` | 30 | 0 | 30 | 8 | 19 | 3 | 0 |
| `temes/societat/esport` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/societat/familia` | 4 | 0 | 4 | 3 | 1 | 0 | 0 |
| `temes/societat/habitatge` | 9 | 0 | 9 | 6 | 2 | 1 | 0 |
| `temes/societat/immigracio` | 19 | 0 | 19 | 3 | 14 | 2 | 0 |
| `temes/societat/mitjans` | 5 | 0 | 5 | 3 | 2 | 0 | 0 |
| `temes/societat/proteccio-social` | 4 | 0 | 4 | 3 | 0 | 1 | 0 |
| `temes/societat/sanitat` | 19 | 0 | 19 | 7 | 12 | 0 | 0 |
| `temes/societat/treball` | 19 | 0 | 19 | 14 | 5 | 0 | 0 |
| `temes/societat/vida-civica` | 8 | 0 | 8 | 4 | 4 | 0 | 0 |
| `temes/territori/clima-i-muntanya` | 14 | 0 | 14 | 5 | 8 | 1 | 0 |
| `temes/territori/fauna-i-flora` | 5 | 0 | 5 | 3 | 1 | 1 | 0 |
| `temes/territori/geografia-fisica` | 9 | 0 | 9 | 2 | 7 | 0 | 0 |
| `temes/territori/paisatge-construit` | 5 | 0 | 5 | 0 | 5 | 0 | 0 |
| `temes/territori/parroquies/andorra-la-vella` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/territori/parroquies/canillo` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/territori/parroquies/encamp` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/territori/parroquies/escaldes-engordany` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/territori/parroquies/la-massana` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/territori/parroquies/ordino` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/territori/parroquies/sant-julia-de-loria` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `temes/territori/patrimoni-natural` | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| `temes/territori/toponimia` | 5 | 0 | 5 | 1 | 2 | 2 | 0 |
| `temes/territori/urbanisme` | 2 | 0 | 2 | 1 | 1 | 0 | 0 |
| `temes/vida-quotidiana/com-funciona-tot` | 4 | 0 | 4 | 3 | 1 | 0 | 0 |
| `temes/vida-quotidiana/convencions-socials` | 3 | 0 | 3 | 0 | 3 | 0 | 0 |
| `temes/vida-quotidiana/creences` | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| `temes/vida-quotidiana/geografia-mental` | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| `temes/vida-quotidiana/humor` | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| `temes/vida-quotidiana/referents-compartits` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |

* Drets segons només la font principal indicada a la capçalera; cal revisar totes les fonts emprades en cada conversa abans d'exportar.

## Tria inicial de drets a la font principal declarada

Aquesta tria només mira el camp `font` de la capçalera i la seva fitxa a `docs/fonts/`. No comprova totes les fonts citades al cos, ni substitueix una revisió de drets per registre.

| Estat declarat | Fitxes |
|---|---:|
| `yes` | 635 |
| `no` | 108 |
| `pending` | 604 |
| `missing` | 1 |

**Total:** 1348 fitxes article; **12** tenen almenys una conversa citada i **1336** encara no en tenen.

## Límits

- La cobertura citada només indica que una conversa apunta a la fitxa. No acredita cobertura de cada secció, taula, fila, llista, data o excepció.
- Els registres de revisió poden tenir drets pendents i no són exports d'entrenament.
- La font de veritat és el corpus actual; torneu a generar aquest informe després de canvis a `docs/temes/` o als registres de procedència.
