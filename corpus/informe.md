# Informe del corpus curat

## Snapshot E0

- Documents d'entrada: **1,388**; words en fitxers Markdown inclòs frontmatter: **2,187,109**.
- SHA determinista del conjunt d'entrades: `27fd7fd18e9fccea2ecc20aec36035af02618abca470f9931fe15c8e2d27d300`. És SHA-256 dels parells ordenats `doc_id + SHA blob`, no el commit Git, perquè no canviï en commitejar la sortida.
- Docs de parla: **40** transcripcions curades; buits de mostra exclosos de RAFT.
- Fonts reconegudes: **627**; documents malformats sense parsejar: **0**.

| Mesura d'entrada | Partida | Ara | Diferència |
| --- | ---: | ---: | ---: |
| Documents | 1,388 | 1,388 | +0.0% |
| Articles | 1,348 | 1,348 | +0.0% |
| Parla | 40 | 40 | +0.0% |
| Fitxes de font | 627 | 627 | +0.0% |
| Paraules Markdown | 2,150,000 | 2,187,109 | +1.7% |
| Auditories | 387 | 166 | -57.1% |
| Fragments ratllats | 2,523 | 2,740 | +8.6% |
| Enllaços a raw/ | 1,263 | 1,263 | +0.0% |
| Enllaços interns | 15,966 | 15,753 | -1.3% |
| Marques de negreta | 128,867 | 130,368 | +1.2% |
| Segments de parla | 15,963 | 15,963 | +0.0% |
| Marques incertes | 8,450 | 8,314 | -1.6% |
| Buits registrats (paraules) | 18.6% | 17.5% | -1.1% pp |
| El que falta (paraules) | 5.5% | 4.9% | -0.6% pp |
| Related (paraules) | 3.1% | 4.1% | +1.0% pp |

## Resultats per ús

| Ús | Chunks | Paraules | Ja aprovats a `decisions.jsonl` |
| --- | ---: | ---: | ---: |
| llengua | 40 | 99,554 | 0 |
| coneixement | 3391 | 851,469 | 21 |
| raft-context | 3519 | 880,528 | 23 |
| raft-sense-oracle | 4174 | 217,322 | 0 |

Les paraules de llengua són parla originària contemporània sense normalització.
Només les etiquetes `approved` es compten com a revisades; `pendent-escolta`
continua pendent i no és llengua verificada.

## Resultats per domini

| Domini | Chunks | Paraules d'entrada | Paraules conservades en chunks |
| --- | ---: | ---: | ---: |
| costums | 45 | 25,938 | 11,398 |
| cultura | 165 | 88,891 | 39,872 |
| economia | 304 | 172,650 | 81,136 |
| esports | 356 | 181,698 | 62,265 |
| gastronomia | 27 | 11,514 | 5,911 |
| historia | 683 | 331,519 | 171,862 |
| institucions | 1031 | 590,452 | 269,157 |
| llengua | 151 | 98,025 | 42,802 |
| parla | 40 | 261,094 | 99,554 |
| persones | 63 | 31,974 | 12,250 |
| politica | 91 | 50,650 | 25,639 |
| societat | 444 | 257,905 | 118,469 |
| territori | 126 | 71,596 | 30,536 |
| vida-quotidiana | 33 | 13,203 | 7,897 |

## Paraules per ús × domini

| Ús | Domini | Paraules |
| --- | --- | ---: |
| coneixement | costums | 10,773 |
| coneixement | cultura | 37,689 |
| coneixement | economia | 78,166 |
| coneixement | esports | 51,059 |
| coneixement | gastronomia | 5,911 |
| coneixement | historia | 171,113 |
| coneixement | institucions | 264,278 |
| coneixement | llengua | 41,638 |
| coneixement | persones | 11,923 |
| coneixement | politica | 25,367 |
| coneixement | societat | 115,457 |
| coneixement | territori | 30,198 |
| coneixement | vida-quotidiana | 7,897 |
| llengua | parla | 99,554 |
| raft-context | costums | 11,398 |
| raft-context | cultura | 39,872 |
| raft-context | economia | 81,136 |
| raft-context | esports | 62,545 |
| raft-context | gastronomia | 5,911 |
| raft-context | historia | 172,564 |
| raft-context | institucions | 269,157 |
| raft-context | llengua | 42,802 |
| raft-context | persones | 12,250 |
| raft-context | politica | 25,639 |
| raft-context | societat | 118,821 |
| raft-context | territori | 30,536 |
| raft-context | vida-quotidiana | 7,897 |
| raft-sense-oracle | costums | 4,440 |
| raft-sense-oracle | cultura | 11,786 |
| raft-sense-oracle | economia | 23,983 |
| raft-sense-oracle | esports | 16,147 |
| raft-sense-oracle | gastronomia | 1,437 |
| raft-sense-oracle | historia | 36,945 |
| raft-sense-oracle | institucions | 67,173 |
| raft-sense-oracle | llengua | 3,110 |
| raft-sense-oracle | persones | 4,558 |
| raft-sense-oracle | politica | 4,696 |
| raft-sense-oracle | societat | 32,504 |
| raft-sense-oracle | territori | 9,994 |
| raft-sense-oracle | vida-quotidiana | 549 |

## Paraules per ús × llicència

| Ús | Llicència i redistribució | Paraules |
| --- | --- | ---: |
| coneixement | Accés obert al repositori IEC; no hi consta una llicència de reutilització · pendent | 1,867 |
| coneixement | Accés obert al repositori institucional; no hi consta una llicència de reutilització · pendent | 1,177 |
| coneixement | Article acadèmic distribuït en PDF; no hi consta una llicència oberta de redistribució · no | 414 |
| coneixement | Article consultable a RACO; termes de redistribució del text no verificats · no | 368 |
| coneixement | Article editorial consultable en obert; no s’hi especifica una llicència general de redistribució · no | 534 |
| coneixement | Article en accés obert amb llicència CC BY 3.0 · pendent | 493 |
| coneixement | Article web editorial en obert; no hi consta una llicència general de reutilització · pendent | 817 |
| coneixement | Avís legal general de l'Arxiu Nacional; ús dels continguts reservat llevat d'autorització específica · pendent | 85 |
| coneixement | CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària · si | 24,976 |
| coneixement | CC BY 4.0; declaració explícita al PDF p. 26 · pendent | 134 |
| coneixement | CC BY-SA 4.0 (Wikipedia) · institucional (alturgell.cat) · pendent | 211 |
| coneixement | CC BY-SA 4.0 (Wikipedia) · premsa, drets reservats (obituari) · pendent | 194 |
| coneixement | CC BY-SA 4.0 · pendent | 2,789 |
| coneixement | CC BY-SA 4.0 · si | 89,880 |
| coneixement | Catàleg institucional; termes de reutilització no especificats · no | 2,772 |
| coneixement | Catàleg públic del Govern d’Andorra; condicions del portal · pendent | 1,225 |
| coneixement | Condicions generals d'utilització de la informació a la seu electrònica del BOPA; permeten còpia, difusió, adaptació, extracció, reordenació, combinació i distribució amb les condicions indicades. · si | 603 |
| coneixement | Domini públic segons la fitxa; cal citar l’autoria coneguda i la procedència · pendent | 427 |
| coneixement | Fitxa amb View, Preview i Download; sense llicència específica de reutilització · pendent | 1,071 |
| coneixement | Fitxa institucional; termes de reutilització no especificats · no | 420 |
| coneixement | Fitxa pública amb consulta i rendicions; no consta una llicència específica de reutilització · no | 728 |
| coneixement | Fitxa pública amb consulta, previsualització i descàrrega; drets legals atribuïts a Joan Vehils · no | 104 |
| coneixement | Fitxa pública amb consulta, previsualització i descàrrega; no consta una llicència específica de reutilització · no | 3,949 |
| coneixement | Fitxa pública amb permisos de consulta i descàrrega; no consta una llicència específica de reutilització · no | 1,964 |
| coneixement | Fitxes amb View, Preview i Download; sense llicència específica de reutilització · pendent | 1,204 |
| coneixement | Fitxes públiques amb consulta i rendicions; no consta una llicència específica de reutilització · no | 450 |
| coneixement | Fitxes públiques amb permisos de consulta i descàrrega; no consta una llicència específica de reutilització · no | 213 |
| coneixement | L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 204,346 |
| coneixement | La Library of Congress declara no tenir constancia de cap restriccio de drets sobre l'item · si | 377 |
| coneixement | Licence Etalab 2.0 per a l'edició digital CARo; l'edició bibliogràfica original conserva els seus drets · pendent | 317 |
| coneixement | Memòria tècnica institucional; no hi consta una llicència oberta de redistribució · no | 378 |
| coneixement | Nota estadística institucional; no hi consta una llicència de reutilització · pendent | 768 |
| coneixement | PDF d’accés obert; no hi consta una llicència de reutilització · pendent | 886 |
| coneixement | Publicacio institucional en obert, sense llicencia declarada als llibres d'actes. La sintesi de Guillamet (2024) SI que porta prohibicio expressa de reproduccio. · pendent | 58,540 |
| coneixement | Publicacio oficial de l'Estat andorra. Les bases reguladores publicades al BOPA num. 1 del 1989 (base d) diuen: les disposicions reproduides al BOPA es poden inserir total o parcialment en altres publicacions sempre que convingui citar-les o transcriure-les, pero NO es poden publicar soles o en colleccio sense autoritzacio escrita previa de l'autoritat de que emanin. · pendent | 5,505 |
| coneixement | Publicació acadèmica en accés públic; no hi consta una llicència específica de redistribució · no | 564 |
| coneixement | Publicació institucional en obert, sense llicència declarada · pendent | 461 |
| coneixement | Publicació institucional en obert; llicència específica de reutilització no indicada · no | 1,701 |
| coneixement | Publicació institucional i memòria arqueològica en accés públic; no hi consta una llicència específica de reutilització · no | 415 |
| coneixement | Publicació oficial; no s'ha localitzat una llicència específica de reutilització de la digitalització · pendent | 3,400 |
| coneixement | Pàgina i imatge institucionals; termes de reutilització no especificats · no | 393 |
| coneixement | Pàgina i imatges institucionals; termes de reutilització no especificats · no | 892 |
| coneixement | Pàgina periodística en obert, sense llicència de reutilització declarada · no | 601 |
| coneixement | Pàgines públiques; llicència específica de reutilització no indicada · pendent | 894 |
| coneixement | Registres institucionals i transcripció web; no hi consta una llicència específica de reutilització · pendent | 534 |
| coneixement | Text complet visible a ResearchGate; la pàgina indica que pot estar subjecte a drets d’autor · no | 409 |
| coneixement | Transcripció institucional en obert; no hi consta una llicència de reutilització · pendent | 660 |
| coneixement | accés obert al Dipòsit Digital de la UB · pendent | 2,619 |
| coneixement | acta formalitzada d'una administració comunal andorrana; document públic · pendent | 506 |
| coneixement | butlletí oficial espanyol de 1894; domini públic per antiguitat · si | 814 |
| coneixement | condicions de reproducció i reutilització dels Archives diplomatiques; el portal mostra llicència Etalab per al web · pendent | 1,193 |
| coneixement | condicions de reutilització pendents per peça · pendent | 67 |
| coneixement | condicions generals d'utilització de la informació de la seu electrònica del BOPA · si | 11,505 |
| coneixement | condicions variables per document; identitat gràfica reservada · pendent | 4,376 |
| coneixement | contingut editorial amb drets reservats · no | 113 |
| coneixement | contingut periodístic amb drets reservats · no | 6,894 |
| coneixement | document de divulgació per a ensenyants; sense llicència explícita · pendent | 880 |
| coneixement | document parlamentari oficial de 1895; domini públic per antiguitat · si | 2,207 |
| coneixement | domini públic per antiguitat; digitalització de Google Books a partir d'un exemplar de biblioteca · si | 12,190 |
| coneixement | domini públic per antiguitat; digitalització de Google Books · si | 29,786 |
| coneixement | drets específics del llibre pendents; portal general amb drets reservats · pendent | 2,584 |
| coneixement | drets específics dels informes pendents; sense llicència oberta general acreditada · pendent | 299 |
| coneixement | drets reservats pels titulars respectius · no | 8,779 |
| coneixement | drets reservats · citació breu amb atribució · no | 226 |
| coneixement | drets reservats — obra d'autor viu, reedició del 2019, sense llicència explícita identificada · no | 2,575 |
| coneixement | drets reservats; cap llicència declarada al document ni al portal · no | 12,161 |
| coneixement | drets reservats; cap llicència declarada ni al document ni al portal · no | 1,237 |
| coneixement | drets reservats; cap llicència oberta declarada al volum · no | 4,203 |
| coneixement | drets reservats; cap llicència oberta declarada · no | 5,373 |
| coneixement | drets reservats; copyright de l'autor i de l'edició, cap llicència oberta · no | 931 |
| coneixement | drets reservats; copyright de les autores i de l'edició, cap llicència oberta · no | 2,589 |
| coneixement | drets reservats; dos titulars declarats a la pàgina de crèdits, cap llicència oberta · no | 15,141 |
| coneixement | drets reservats; reutilització sotmesa a autorització expressa · no | 54 |
| coneixement | drets reservats; reutilització subjecta a autorització del titular · pendent | 225 |
| coneixement | drets reservats; sense autorització general de redistribució · no | 3,993 |
| coneixement | edició institucional amb drets editorials; accés obert per Dialnet · pendent | 535 |
| coneixement | informació institucional pública · si | 924 |
| coneixement | instrument de descripció públic; condicions del portal d’arxius · no | 231 |
| coneixement | llicència no consta · pendent | 38 |
| coneixement | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 73,228 |
| coneixement | obra literària amb drets reservats · no | 462 |
| coneixement | pendent de determinar per a la peça concreta · pendent | 105 |
| coneixement | pendent · pendent | 39 |
| coneixement | pendent; PDF accessible al repositori de l'IEC, sense llicència específica identificada a la peça · pendent | 1,273 |
| coneixement | premsa digital, sense llicència declarada · pendent | 510 |
| coneixement | premsa digital, sense llicència oberta declarada · pendent | 156 |
| coneixement | premsa, drets reservats; citació breu · no | 519 |
| coneixement | publicació acadèmica de l'IEC, accés obert · pendent | 9,255 |
| coneixement | publicació acadèmica de la Societat Andorrana de Ciències · pendent | 17,079 |
| coneixement | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 130,123 |
| coneixement | publicació acadèmica en accés obert (repositori de l'Institut d'Estudis Catalans) · pendent | 11,597 |
| coneixement | publicació acadèmica en accés obert · pendent | 19,198 |
| coneixement | publicació acadèmica en accés obert; sense llicència de redistribució declarada · pendent | 270 |
| coneixement | publicació acadèmica, IEC; ús de recerca · pendent | 807 |
| coneixement | publicació associativa, sense llicència declarada · pendent | 139 |
| coneixement | publicació editorial, sense llicència declarada · pendent | 777 |
| coneixement | publicació institucional del Govern d'Andorra; sense llicència oberta identificada · no | 423 |
| coneixement | publicació institucional en accés obert al web de l'IEA · pendent | 1,308 |
| coneixement | publicació institucional en accés públic; sense llicència de redistribució declarada · pendent | 434 |
| coneixement | publicació institucional i tècnica en accés públic; sense llicència de redistribució declarada · pendent | 495 |
| coneixement | publicació institucional, sense llicència declarada · pendent | 830 |
| coneixement | publicació institucional; llicència específica no indicada · pendent | 928 |
| coneixement | publicació institucional; termes de reutilització no especificats · no | 554 |
| coneixement | pàgina institucional amb drets reservats · no | 59 |
| coneixement | pàgina institucional en accés obert; els drets dels documents reproduïts resten dels titulars · pendent | 633 |
| coneixement | pàgina institucional; llicència específica no indicada · pendent | 661 |
| coneixement | registre institucional i article acadèmic d'accés obert; condicions específiques per peça · pendent | 123 |
| coneixement | reutilització autoritzada, comercial i no comercial, per la Decisió 2011/833/UE · si | 2,100 |
| coneixement | reutilització autoritzada, comercial i no comercial, per la Decisió 2011/833/UE. Els textos consolidats, CC BY 4.0 · si | 1,495 |
| coneixement | sense llicència declarada; el document no porta pàgina de crèdits, ni ISBN, ni dipòsit legal · no | 585 |
| coneixement | sense llicència ni estat de drets declarats a l'ítem digital; termini espanyol per a defuncions anteriors a 1987, vuitanta anys post mortem · pendent | 18,631 |
| coneixement | text normatiu oficial, ús públic · pendent | 105 |
| coneixement | web i publicació institucionals, sense llicència oberta identificada · no | 117 |
| coneixement | web institucional, drets reservats; sense llicència oberta identificada · no | 93 |
| llengua | Llicència estàndard de YouTube. El Consell General no declara cap llicència oberta. · pendent | 74,871 |
| llengua | Publicacio institucional en obert, sense llicencia declarada als llibres d'actes. La sintesi de Guillamet (2024) SI que porta prohibicio expressa de reproduccio. · pendent | 0 |
| llengua | YouTube declara Creative Commons Attribution en vídeos individuals; verificació per peça, no per sèrie. Verificada a #34, #49, #56, #57, #60 i #65. · pendent | 24,683 |
| raft-context | Accés obert al repositori IEC; no hi consta una llicència de reutilització · pendent | 1,867 |
| raft-context | Accés obert al repositori institucional; no hi consta una llicència de reutilització · pendent | 1,177 |
| raft-context | Article acadèmic distribuït en PDF; no hi consta una llicència oberta de redistribució · no | 414 |
| raft-context | Article consultable a RACO; termes de redistribució del text no verificats · no | 368 |
| raft-context | Article editorial consultable en obert; no s’hi especifica una llicència general de redistribució · no | 534 |
| raft-context | Article en accés obert amb llicència CC BY 3.0 · pendent | 493 |
| raft-context | Article web editorial en obert; no hi consta una llicència general de reutilització · pendent | 817 |
| raft-context | Avís legal general de l'Arxiu Nacional; ús dels continguts reservat llevat d'autorització específica · pendent | 85 |
| raft-context | CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària · si | 27,707 |
| raft-context | CC BY 4.0; declaració explícita al PDF p. 26 · pendent | 134 |
| raft-context | CC BY-SA 4.0 (Wikipedia) · institucional (alturgell.cat) · pendent | 211 |
| raft-context | CC BY-SA 4.0 (Wikipedia) · premsa, drets reservats (obituari) · pendent | 194 |
| raft-context | CC BY-SA 4.0 · pendent | 2,938 |
| raft-context | CC BY-SA 4.0 · si | 103,530 |
| raft-context | Catàleg institucional; termes de reutilització no especificats · no | 2,772 |
| raft-context | Catàleg públic del Govern d’Andorra; condicions del portal · pendent | 1,225 |
| raft-context | Condicions generals d'utilització de la informació a la seu electrònica del BOPA; permeten còpia, difusió, adaptació, extracció, reordenació, combinació i distribució amb les condicions indicades. · si | 603 |
| raft-context | Domini públic segons la fitxa; cal citar l’autoria coneguda i la procedència · pendent | 427 |
| raft-context | Fitxa amb View, Preview i Download; sense llicència específica de reutilització · pendent | 1,071 |
| raft-context | Fitxa institucional; termes de reutilització no especificats · no | 420 |
| raft-context | Fitxa pública amb consulta i rendicions; no consta una llicència específica de reutilització · no | 728 |
| raft-context | Fitxa pública amb consulta, previsualització i descàrrega; drets legals atribuïts a Joan Vehils · no | 104 |
| raft-context | Fitxa pública amb consulta, previsualització i descàrrega; no consta una llicència específica de reutilització · no | 3,949 |
| raft-context | Fitxa pública amb permisos de consulta i descàrrega; no consta una llicència específica de reutilització · no | 1,964 |
| raft-context | Fitxes amb View, Preview i Download; sense llicència específica de reutilització · pendent | 1,204 |
| raft-context | Fitxes públiques amb consulta i rendicions; no consta una llicència específica de reutilització · no | 450 |
| raft-context | Fitxes públiques amb permisos de consulta i descàrrega; no consta una llicència específica de reutilització · no | 213 |
| raft-context | L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 206,936 |
| raft-context | La Library of Congress declara no tenir constancia de cap restriccio de drets sobre l'item · si | 377 |
| raft-context | Licence Etalab 2.0 per a l'edició digital CARo; l'edició bibliogràfica original conserva els seus drets · pendent | 317 |
| raft-context | Memòria tècnica institucional; no hi consta una llicència oberta de redistribució · no | 378 |
| raft-context | Nota estadística institucional; no hi consta una llicència de reutilització · pendent | 1,210 |
| raft-context | PDF d’accés obert; no hi consta una llicència de reutilització · pendent | 886 |
| raft-context | Publicacio institucional en obert, sense llicencia declarada als llibres d'actes. La sintesi de Guillamet (2024) SI que porta prohibicio expressa de reproduccio. · pendent | 58,540 |
| raft-context | Publicacio oficial de l'Estat andorra. Les bases reguladores publicades al BOPA num. 1 del 1989 (base d) diuen: les disposicions reproduides al BOPA es poden inserir total o parcialment en altres publicacions sempre que convingui citar-les o transcriure-les, pero NO es poden publicar soles o en colleccio sense autoritzacio escrita previa de l'autoritat de que emanin. · pendent | 5,505 |
| raft-context | Publicació acadèmica en accés públic; no hi consta una llicència específica de redistribució · no | 564 |
| raft-context | Publicació institucional en obert, sense llicència declarada · pendent | 461 |
| raft-context | Publicació institucional en obert; llicència específica de reutilització no indicada · no | 1,701 |
| raft-context | Publicació institucional i memòria arqueològica en accés públic; no hi consta una llicència específica de reutilització · no | 415 |
| raft-context | Publicació oficial; no s'ha localitzat una llicència específica de reutilització de la digitalització · pendent | 3,400 |
| raft-context | Pàgina i imatge institucionals; termes de reutilització no especificats · no | 393 |
| raft-context | Pàgina i imatges institucionals; termes de reutilització no especificats · no | 892 |
| raft-context | Pàgina periodística en obert, sense llicència de reutilització declarada · no | 601 |
| raft-context | Pàgines públiques; llicència específica de reutilització no indicada · pendent | 894 |
| raft-context | Registres institucionals i transcripció web; no hi consta una llicència específica de reutilització · pendent | 534 |
| raft-context | Text complet visible a ResearchGate; la pàgina indica que pot estar subjecte a drets d’autor · no | 409 |
| raft-context | Transcripció institucional en obert; no hi consta una llicència de reutilització · pendent | 660 |
| raft-context | accés obert al Dipòsit Digital de la UB · pendent | 2,619 |
| raft-context | acta formalitzada d'una administració comunal andorrana; document públic · pendent | 1,058 |
| raft-context | butlletí oficial espanyol de 1894; domini públic per antiguitat · si | 814 |
| raft-context | condicions de reproducció i reutilització dels Archives diplomatiques; el portal mostra llicència Etalab per al web · pendent | 1,193 |
| raft-context | condicions de reutilització pendents per peça · pendent | 67 |
| raft-context | condicions generals d'utilització de la informació de la seu electrònica del BOPA · si | 12,593 |
| raft-context | condicions variables per document; identitat gràfica reservada · pendent | 4,376 |
| raft-context | contingut editorial amb drets reservats · no | 113 |
| raft-context | contingut periodístic amb drets reservats · no | 7,484 |
| raft-context | document de divulgació per a ensenyants; sense llicència explícita · pendent | 880 |
| raft-context | document parlamentari oficial de 1895; domini públic per antiguitat · si | 2,207 |
| raft-context | domini públic per antiguitat; digitalització de Google Books a partir d'un exemplar de biblioteca · si | 12,469 |
| raft-context | domini públic per antiguitat; digitalització de Google Books · si | 30,125 |
| raft-context | drets específics del llibre pendents; portal general amb drets reservats · pendent | 2,584 |
| raft-context | drets específics dels informes pendents; sense llicència oberta general acreditada · pendent | 299 |
| raft-context | drets reservats pels titulars respectius · no | 8,779 |
| raft-context | drets reservats · citació breu amb atribució · no | 226 |
| raft-context | drets reservats — obra d'autor viu, reedició del 2019, sense llicència explícita identificada · no | 2,575 |
| raft-context | drets reservats; cap llicència declarada al document ni al portal · no | 12,630 |
| raft-context | drets reservats; cap llicència declarada ni al document ni al portal · no | 1,237 |
| raft-context | drets reservats; cap llicència oberta declarada al volum · no | 4,203 |
| raft-context | drets reservats; cap llicència oberta declarada · no | 5,373 |
| raft-context | drets reservats; copyright de l'autor i de l'edició, cap llicència oberta · no | 931 |
| raft-context | drets reservats; copyright de les autores i de l'edició, cap llicència oberta · no | 2,589 |
| raft-context | drets reservats; dos titulars declarats a la pàgina de crèdits, cap llicència oberta · no | 15,141 |
| raft-context | drets reservats; reutilització sotmesa a autorització expressa · no | 54 |
| raft-context | drets reservats; reutilització subjecta a autorització del titular · pendent | 265 |
| raft-context | drets reservats; sense autorització general de redistribució · no | 4,615 |
| raft-context | edició institucional amb drets editorials; accés obert per Dialnet · pendent | 535 |
| raft-context | informació institucional pública · si | 1,128 |
| raft-context | instrument de descripció públic; condicions del portal d’arxius · no | 231 |
| raft-context | llicència no consta · pendent | 38 |
| raft-context | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 75,930 |
| raft-context | obra literària amb drets reservats · no | 462 |
| raft-context | pendent de determinar per a la peça concreta · pendent | 105 |
| raft-context | pendent per a les peces; condicions generals del portal amb drets reservats · pendent | 85 |
| raft-context | pendent · pendent | 39 |
| raft-context | pendent; PDF accessible al repositori de l'IEC, sense llicència específica identificada a la peça · pendent | 1,273 |
| raft-context | premsa digital, sense llicència declarada · pendent | 510 |
| raft-context | premsa digital, sense llicència oberta declarada · pendent | 156 |
| raft-context | premsa, drets reservats; citació breu · no | 519 |
| raft-context | publicació acadèmica de l'IEC, accés obert · pendent | 9,255 |
| raft-context | publicació acadèmica de la Societat Andorrana de Ciències · pendent | 17,363 |
| raft-context | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 131,235 |
| raft-context | publicació acadèmica en accés obert (repositori de l'Institut d'Estudis Catalans) · pendent | 11,991 |
| raft-context | publicació acadèmica en accés obert · pendent | 19,704 |
| raft-context | publicació acadèmica en accés obert; sense llicència de redistribució declarada · pendent | 270 |
| raft-context | publicació acadèmica, IEC; ús de recerca · pendent | 807 |
| raft-context | publicació associativa, sense llicència declarada · pendent | 139 |
| raft-context | publicació editorial, sense llicència declarada · pendent | 1,008 |
| raft-context | publicació institucional del Govern d'Andorra; sense llicència oberta identificada · no | 423 |
| raft-context | publicació institucional en accés obert al web de l'IEA · pendent | 1,308 |
| raft-context | publicació institucional en accés públic; sense llicència de redistribució declarada · pendent | 434 |
| raft-context | publicació institucional i tècnica en accés públic; sense llicència de redistribució declarada · pendent | 495 |
| raft-context | publicació institucional, sense llicència declarada · pendent | 830 |
| raft-context | publicació institucional; llicència específica no indicada · pendent | 928 |
| raft-context | publicació institucional; termes de reutilització no especificats · no | 554 |
| raft-context | pàgina institucional amb drets reservats · no | 59 |
| raft-context | pàgina institucional en accés obert; els drets dels documents reproduïts resten dels titulars · pendent | 633 |
| raft-context | pàgina institucional; llicència específica no indicada · pendent | 661 |
| raft-context | registre institucional i article acadèmic d'accés obert; condicions específiques per peça · pendent | 123 |
| raft-context | reutilització autoritzada, comercial i no comercial, per la Decisió 2011/833/UE · si | 2,100 |
| raft-context | reutilització autoritzada, comercial i no comercial, per la Decisió 2011/833/UE. Els textos consolidats, CC BY 4.0 · si | 1,495 |
| raft-context | sense llicència declarada; el document no porta pàgina de crèdits, ni ISBN, ni dipòsit legal · no | 585 |
| raft-context | sense llicència ni estat de drets declarats a l'ítem digital; termini espanyol per a defuncions anteriors a 1987, vuitanta anys post mortem · pendent | 18,631 |
| raft-context | text normatiu oficial, ús públic · pendent | 105 |
| raft-context | web i publicació institucionals, sense llicència oberta identificada · no | 117 |
| raft-context | web institucional, drets reservats; sense llicència oberta identificada · no | 93 |
| raft-sense-oracle | Accés obert al repositori IEC; no hi consta una llicència de reutilització · pendent | 226 |
| raft-sense-oracle | Accés obert al repositori institucional; no hi consta una llicència de reutilització · pendent | 229 |
| raft-sense-oracle | Article web editorial en obert; no hi consta una llicència general de reutilització · pendent | 105 |
| raft-sense-oracle | Avís legal general de l'Arxiu Nacional; ús dels continguts reservat llevat d'autorització específica · pendent | 52 |
| raft-sense-oracle | CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària · si | 5,431 |
| raft-sense-oracle | CC BY 4.0; declaració explícita al PDF p. 26 · pendent | 351 |
| raft-sense-oracle | CC BY-SA 4.0 (Wikipedia) · institucional (alturgell.cat) · pendent | 103 |
| raft-sense-oracle | CC BY-SA 4.0 (Wikipedia) · premsa, drets reservats (obituari) · pendent | 135 |
| raft-sense-oracle | CC BY-SA 4.0 · pendent | 1,472 |
| raft-sense-oracle | CC BY-SA 4.0 · si | 29,232 |
| raft-sense-oracle | Catàleg institucional; termes de reutilització no especificats · no | 66 |
| raft-sense-oracle | Condicions generals d'utilització de la informació a la seu electrònica del BOPA; permeten còpia, difusió, adaptació, extracció, reordenació, combinació i distribució amb les condicions indicades. · si | 253 |
| raft-sense-oracle | Domini públic segons la fitxa; cal citar l’autoria coneguda i la procedència · pendent | 308 |
| raft-sense-oracle | Fitxa amb View, Preview i Download; sense llicència específica de reutilització · pendent | 252 |
| raft-sense-oracle | Fitxa pública amb consulta i rendicions; no consta una llicència específica de reutilització · no | 334 |
| raft-sense-oracle | Fitxa pública amb consulta, previsualització i descàrrega; drets legals atribuïts a Joan Vehils · no | 74 |
| raft-sense-oracle | Fitxa pública amb consulta, previsualització i descàrrega; no consta una llicència específica de reutilització · no | 1,939 |
| raft-sense-oracle | Fitxa pública amb permisos de consulta i descàrrega; no consta una llicència específica de reutilització · no | 716 |
| raft-sense-oracle | Fitxes amb View, Preview i Download; sense llicència específica de reutilització · pendent | 329 |
| raft-sense-oracle | Fitxes públiques amb consulta i rendicions; no consta una llicència específica de reutilització · no | 219 |
| raft-sense-oracle | Fitxes públiques amb permisos de consulta i descàrrega; no consta una llicència específica de reutilització · no | 69 |
| raft-sense-oracle | L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 61,012 |
| raft-sense-oracle | Nota estadística institucional; no hi consta una llicència de reutilització · pendent | 459 |
| raft-sense-oracle | PDF d’accés obert; no hi consta una llicència de reutilització · pendent | 184 |
| raft-sense-oracle | Publicacio institucional en obert, sense llicencia declarada als llibres d'actes. La sintesi de Guillamet (2024) SI que porta prohibicio expressa de reproduccio. · pendent | 1,480 |
| raft-sense-oracle | Publicacio oficial de l'Estat andorra. Les bases reguladores publicades al BOPA num. 1 del 1989 (base d) diuen: les disposicions reproduides al BOPA es poden inserir total o parcialment en altres publicacions sempre que convingui citar-les o transcriure-les, pero NO es poden publicar soles o en colleccio sense autoritzacio escrita previa de l'autoritat de que emanin. · pendent | 646 |
| raft-sense-oracle | Publicació oficial; no s'ha localitzat una llicència específica de reutilització de la digitalització · pendent | 747 |
| raft-sense-oracle | Pàgina i imatge institucionals; termes de reutilització no especificats · no | 86 |
| raft-sense-oracle | Pàgina i imatges institucionals; termes de reutilització no especificats · no | 200 |
| raft-sense-oracle | Pàgines públiques; llicència específica de reutilització no indicada · pendent | 287 |
| raft-sense-oracle | accés obert al Dipòsit Digital de la UB · pendent | 324 |
| raft-sense-oracle | acta formalitzada d'una administració comunal andorrana; document públic · pendent | 372 |
| raft-sense-oracle | butlletí oficial espanyol de 1894; domini públic per antiguitat · si | 161 |
| raft-sense-oracle | condicions de reproducció i reutilització dels Archives diplomatiques; el portal mostra llicència Etalab per al web · pendent | 360 |
| raft-sense-oracle | condicions de reutilització pendents per peça · pendent | 287 |
| raft-sense-oracle | condicions generals d'utilització de la informació de la seu electrònica del BOPA · si | 3,171 |
| raft-sense-oracle | condicions variables per document; identitat gràfica reservada · pendent | 1,045 |
| raft-sense-oracle | contingut editorial amb drets reservats · no | 34 |
| raft-sense-oracle | contingut periodístic amb drets reservats · no | 2,705 |
| raft-sense-oracle | document de divulgació per a ensenyants; sense llicència explícita · pendent | 876 |
| raft-sense-oracle | document parlamentari oficial de 1895; domini públic per antiguitat · si | 245 |
| raft-sense-oracle | domini públic per antiguitat; digitalització de Google Books a partir d'un exemplar de biblioteca · si | 4,225 |
| raft-sense-oracle | domini públic per antiguitat; digitalització de Google Books · si | 11,123 |
| raft-sense-oracle | drets específics del llibre pendents; portal general amb drets reservats · pendent | 513 |
| raft-sense-oracle | drets específics dels informes pendents; sense llicència oberta general acreditada · pendent | 539 |
| raft-sense-oracle | drets reservats pels titulars respectius · no | 215 |
| raft-sense-oracle | drets reservats — obra d'autor viu, reedició del 2019, sense llicència explícita identificada · no | 492 |
| raft-sense-oracle | drets reservats; cap llicència declarada al document ni al portal · no | 808 |
| raft-sense-oracle | drets reservats; cap llicència oberta declarada al volum · no | 521 |
| raft-sense-oracle | drets reservats; copyright de les autores i de l'edició, cap llicència oberta · no | 99 |
| raft-sense-oracle | drets reservats; dos titulars declarats a la pàgina de crèdits, cap llicència oberta · no | 2,092 |
| raft-sense-oracle | drets reservats; reutilització sotmesa a autorització expressa · no | 152 |
| raft-sense-oracle | drets reservats; reutilització subjecta a autorització del titular · pendent | 451 |
| raft-sense-oracle | drets reservats; sense autorització general de redistribució · no | 785 |
| raft-sense-oracle | informació institucional pública · si | 54 |
| raft-sense-oracle | instrument de descripció públic; condicions del portal d’arxius · no | 76 |
| raft-sense-oracle | llicència no consta · pendent | 44 |
| raft-sense-oracle | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 16,814 |
| raft-sense-oracle | obra literària amb drets reservats · no | 535 |
| raft-sense-oracle | pendent de determinar per a la peça concreta · pendent | 152 |
| raft-sense-oracle | pendent per a les peces; condicions generals del portal amb drets reservats · pendent | 235 |
| raft-sense-oracle | pendent · pendent | 175 |
| raft-sense-oracle | pendent; PDF accessible al repositori de l'IEC, sense llicència específica identificada a la peça · pendent | 501 |
| raft-sense-oracle | pendent; avís legal sense llicència específica de reutilització del BPA identificada · pendent | 176 |
| raft-sense-oracle | premsa digital, sense llicència declarada · pendent | 234 |
| raft-sense-oracle | premsa digital, sense llicència oberta declarada · pendent | 95 |
| raft-sense-oracle | premsa, drets reservats; citació breu · no | 242 |
| raft-sense-oracle | publicació acadèmica de l'IEC, accés obert · pendent | 886 |
| raft-sense-oracle | publicació acadèmica de la Societat Andorrana de Ciències · pendent | 4,229 |
| raft-sense-oracle | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 39,900 |
| raft-sense-oracle | publicació acadèmica en accés obert (repositori de l'Institut d'Estudis Catalans) · pendent | 4,107 |
| raft-sense-oracle | publicació acadèmica en accés obert · pendent | 2,139 |
| raft-sense-oracle | publicació associativa, sense llicència declarada · pendent | 62 |
| raft-sense-oracle | publicació editorial, sense llicència declarada · pendent | 354 |
| raft-sense-oracle | publicació institucional en accés obert al web de l'IEA · pendent | 582 |
| raft-sense-oracle | publicació institucional en accés públic; sense llicència de redistribució declarada · pendent | 72 |
| raft-sense-oracle | publicació institucional, sense llicència declarada · pendent | 670 |
| raft-sense-oracle | pàgina institucional amb drets reservats · no | 112 |
| raft-sense-oracle | sense llicència ni estat de drets declarats a l'ítem digital; termini espanyol per a defuncions anteriors a 1987, vuitanta anys post mortem · pendent | 6,144 |
| raft-sense-oracle | text normatiu oficial, ús públic · pendent | 141 |

## Paraules per domini × llicència

| Domini | Llicència i redistribució | Paraules |
| --- | --- | ---: |
| costums | CC BY-SA 4.0 · si | 4,558 |
| costums | condicions generals d'utilització de la informació de la seu electrònica del BOPA · si | 1,887 |
| costums | contingut periodístic amb drets reservats · no | 8,263 |
| costums | publicació acadèmica de l'IEC, accés obert · pendent | 594 |
| costums | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 9,029 |
| costums | publicació acadèmica en accés obert (repositori de l'Institut d'Estudis Catalans) · pendent | 2,280 |
| cultura | CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària · si | 1,755 |
| cultura | CC BY-SA 4.0 · si | 24,912 |
| cultura | Publicacio oficial de l'Estat andorra. Les bases reguladores publicades al BOPA num. 1 del 1989 (base d) diuen: les disposicions reproduides al BOPA es poden inserir total o parcialment en altres publicacions sempre que convingui citar-les o transcriure-les, pero NO es poden publicar soles o en colleccio sense autoritzacio escrita previa de l'autoritat de que emanin. · pendent | 1,944 |
| cultura | condicions generals d'utilització de la informació de la seu electrònica del BOPA · si | 11,024 |
| cultura | condicions variables per document; identitat gràfica reservada · pendent | 470 |
| cultura | contingut periodístic amb drets reservats · no | 808 |
| cultura | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 8,292 |
| cultura | obra literària amb drets reservats · no | 1,459 |
| cultura | premsa digital, sense llicència declarada · pendent | 849 |
| cultura | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 28,305 |
| cultura | publicació acadèmica en accés obert (repositori de l'Institut d'Estudis Catalans) · pendent | 5,180 |
| cultura | publicació acadèmica en accés obert · pendent | 2,026 |
| cultura | publicació editorial, sense llicència declarada · pendent | 1,657 |
| cultura | registre institucional i article acadèmic d'accés obert; condicions específiques per peça · pendent | 246 |
| cultura | web i publicació institucionals, sense llicència oberta identificada · no | 234 |
| cultura | web institucional, drets reservats; sense llicència oberta identificada · no | 186 |
| economia | CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària · si | 16,330 |
| economia | CC BY-SA 4.0 · pendent | 1,681 |
| economia | CC BY-SA 4.0 · si | 14,692 |
| economia | Catàleg públic del Govern d’Andorra; condicions del portal · pendent | 488 |
| economia | Fitxa amb View, Preview i Download; sense llicència específica de reutilització · pendent | 447 |
| economia | Fitxa pública amb consulta, previsualització i descàrrega; drets legals atribuïts a Joan Vehils · no | 282 |
| economia | Fitxa pública amb consulta, previsualització i descàrrega; no consta una llicència específica de reutilització · no | 1,825 |
| economia | Fitxes amb View, Preview i Download; sense llicència específica de reutilització · pendent | 735 |
| economia | L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 46,179 |
| economia | condicions generals d'utilització de la informació de la seu electrònica del BOPA · si | 350 |
| economia | contingut periodístic amb drets reservats · no | 1,950 |
| economia | document de divulgació per a ensenyants; sense llicència explícita · pendent | 2,636 |
| economia | document parlamentari oficial de 1895; domini públic per antiguitat · si | 2,581 |
| economia | domini públic per antiguitat; digitalització de Google Books · si | 7,971 |
| economia | drets específics del llibre pendents; portal general amb drets reservats · pendent | 5,681 |
| economia | drets reservats — obra d'autor viu, reedició del 2019, sense llicència explícita identificada · no | 3,827 |
| economia | drets reservats; cap llicència oberta declarada al volum · no | 1,773 |
| economia | drets reservats; sense autorització general de redistribució · no | 3,485 |
| economia | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 32,559 |
| economia | premsa, drets reservats; citació breu · no | 819 |
| economia | publicació acadèmica de l'IEC, accés obert · pendent | 920 |
| economia | publicació acadèmica de la Societat Andorrana de Ciències · pendent | 11,359 |
| economia | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 19,777 |
| economia | publicació acadèmica en accés obert · pendent | 1,770 |
| economia | sense llicència ni estat de drets declarats a l'ítem digital; termini espanyol per a defuncions anteriors a 1987, vuitanta anys post mortem · pendent | 3,168 |
| esports | CC BY-SA 4.0 · pendent | 236 |
| esports | CC BY-SA 4.0 · si | 109,893 |
| esports | drets reservats pels titulars respectius · no | 12,236 |
| esports | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 1,570 |
| esports | premsa digital, sense llicència oberta declarada · pendent | 407 |
| esports | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 5,168 |
| esports | publicació institucional, sense llicència declarada · pendent | 241 |
| gastronomia | CC BY-SA 4.0 · si | 1,512 |
| gastronomia | contingut periodístic amb drets reservats · no | 544 |
| gastronomia | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 11,203 |
| historia | Accés obert al repositori IEC; no hi consta una llicència de reutilització · pendent | 3,960 |
| historia | Accés obert al repositori institucional; no hi consta una llicència de reutilització · pendent | 2,583 |
| historia | Article acadèmic distribuït en PDF; no hi consta una llicència oberta de redistribució · no | 828 |
| historia | Article consultable a RACO; termes de redistribució del text no verificats · no | 736 |
| historia | Article editorial consultable en obert; no s’hi especifica una llicència general de redistribució · no | 1,068 |
| historia | Article en accés obert amb llicència CC BY 3.0 · pendent | 986 |
| historia | Article web editorial en obert; no hi consta una llicència general de reutilització · pendent | 1,739 |
| historia | Avís legal general de l'Arxiu Nacional; ús dels continguts reservat llevat d'autorització específica · pendent | 222 |
| historia | CC BY-SA 4.0 · si | 29,237 |
| historia | Catàleg institucional; termes de reutilització no especificats · no | 5,610 |
| historia | Catàleg públic del Govern d’Andorra; condicions del portal · pendent | 888 |
| historia | Domini públic segons la fitxa; cal citar l’autoria coneguda i la procedència · pendent | 514 |
| historia | Fitxa amb View, Preview i Download; sense llicència específica de reutilització · pendent | 1,141 |
| historia | Fitxa institucional; termes de reutilització no especificats · no | 840 |
| historia | Fitxa pública amb consulta i rendicions; no consta una llicència específica de reutilització · no | 1,153 |
| historia | Fitxa pública amb consulta, previsualització i descàrrega; no consta una llicència específica de reutilització · no | 3,811 |
| historia | Fitxa pública amb permisos de consulta i descàrrega; no consta una llicència específica de reutilització · no | 4,644 |
| historia | Fitxes amb View, Preview i Download; sense llicència específica de reutilització · pendent | 507 |
| historia | Fitxes públiques amb consulta i rendicions; no consta una llicència específica de reutilització · no | 859 |
| historia | Fitxes públiques amb permisos de consulta i descàrrega; no consta una llicència específica de reutilització · no | 495 |
| historia | L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 85,358 |
| historia | La Library of Congress declara no tenir constancia de cap restriccio de drets sobre l'item · si | 754 |
| historia | Licence Etalab 2.0 per a l'edició digital CARo; l'edició bibliogràfica original conserva els seus drets · pendent | 634 |
| historia | Memòria tècnica institucional; no hi consta una llicència oberta de redistribució · no | 756 |
| historia | Nota estadística institucional; no hi consta una llicència de reutilització · pendent | 2,437 |
| historia | Publicacio institucional en obert, sense llicencia declarada als llibres d'actes. La sintesi de Guillamet (2024) SI que porta prohibicio expressa de reproduccio. · pendent | 29,256 |
| historia | Publicació acadèmica en accés públic; no hi consta una llicència específica de redistribució · no | 1,128 |
| historia | Publicació institucional en obert, sense llicència declarada · pendent | 922 |
| historia | Publicació institucional en obert; llicència específica de reutilització no indicada · no | 3,402 |
| historia | Publicació institucional i memòria arqueològica en accés públic; no hi consta una llicència específica de reutilització · no | 830 |
| historia | Publicació oficial; no s'ha localitzat una llicència específica de reutilització de la digitalització · pendent | 7,547 |
| historia | Pàgina i imatge institucionals; termes de reutilització no especificats · no | 872 |
| historia | Pàgina i imatges institucionals; termes de reutilització no especificats · no | 803 |
| historia | Pàgina periodística en obert, sense llicència de reutilització declarada · no | 1,202 |
| historia | Pàgines públiques; llicència específica de reutilització no indicada · pendent | 2,075 |
| historia | Text complet visible a ResearchGate; la pàgina indica que pot estar subjecte a drets d’autor · no | 818 |
| historia | Transcripció institucional en obert; no hi consta una llicència de reutilització · pendent | 758 |
| historia | accés obert al Dipòsit Digital de la UB · pendent | 5,562 |
| historia | butlletí oficial espanyol de 1894; domini públic per antiguitat · si | 1,789 |
| historia | condicions de reproducció i reutilització dels Archives diplomatiques; el portal mostra llicència Etalab per al web · pendent | 2,746 |
| historia | contingut periodístic amb drets reservats · no | 1,944 |
| historia | document parlamentari oficial de 1895; domini públic per antiguitat · si | 2,078 |
| historia | domini públic per antiguitat; digitalització de Google Books a partir d'un exemplar de biblioteca · si | 28,884 |
| historia | domini públic per antiguitat; digitalització de Google Books · si | 32,930 |
| historia | drets reservats; cap llicència oberta declarada · no | 10,746 |
| historia | drets reservats; dos titulars declarats a la pàgina de crèdits, cap llicència oberta · no | 412 |
| historia | instrument de descripció públic; condicions del portal d’arxius · no | 538 |
| historia | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 3,360 |
| historia | publicació acadèmica de l'IEC, accés obert · pendent | 1,041 |
| historia | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 42,516 |
| historia | publicació acadèmica en accés obert (repositori de l'Institut d'Estudis Catalans) · pendent | 2,984 |
| historia | publicació acadèmica en accés obert · pendent | 9,478 |
| historia | publicació acadèmica en accés obert; sense llicència de redistribució declarada · pendent | 540 |
| historia | publicació acadèmica, IEC; ús de recerca · pendent | 1,614 |
| historia | publicació institucional del Govern d'Andorra; sense llicència oberta identificada · no | 846 |
| historia | publicació institucional en accés obert al web de l'IEA · pendent | 3,198 |
| historia | publicació institucional en accés públic; sense llicència de redistribució declarada · pendent | 940 |
| historia | publicació institucional i tècnica en accés públic; sense llicència de redistribució declarada · pendent | 990 |
| historia | publicació institucional; llicència específica no indicada · pendent | 1,856 |
| historia | publicació institucional; termes de reutilització no especificats · no | 1,108 |
| historia | pàgina institucional en accés obert; els drets dels documents reproduïts resten dels titulars · pendent | 1,266 |
| historia | pàgina institucional; llicència específica no indicada · pendent | 1,322 |
| historia | sense llicència ni estat de drets declarats a l'ítem digital; termini espanyol per a defuncions anteriors a 1987, vuitanta anys post mortem · pendent | 18,561 |
| institucions | CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària · si | 5,873 |
| institucions | CC BY-SA 4.0 · si | 9,510 |
| institucions | Catàleg públic del Govern d’Andorra; condicions del portal · pendent | 1,074 |
| institucions | Condicions generals d'utilització de la informació a la seu electrònica del BOPA; permeten còpia, difusió, adaptació, extracció, reordenació, combinació i distribució amb les condicions indicades. · si | 1,459 |
| institucions | Fitxa amb View, Preview i Download; sense llicència específica de reutilització · pendent | 806 |
| institucions | Fitxa pública amb consulta i rendicions; no consta una llicència específica de reutilització · no | 368 |
| institucions | Fitxa pública amb consulta, previsualització i descàrrega; no consta una llicència específica de reutilització · no | 2,285 |
| institucions | Fitxes amb View, Preview i Download; sense llicència específica de reutilització · pendent | 419 |
| institucions | L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 298,117 |
| institucions | Publicacio institucional en obert, sense llicencia declarada als llibres d'actes. La sintesi de Guillamet (2024) SI que porta prohibicio expressa de reproduccio. · pendent | 89,304 |
| institucions | Pàgina i imatges institucionals; termes de reutilització no especificats · no | 1,181 |
| institucions | Registres institucionals i transcripció web; no hi consta una llicència específica de reutilització · pendent | 1,068 |
| institucions | Transcripció institucional en obert; no hi consta una llicència de reutilització · pendent | 562 |
| institucions | acta formalitzada d'una administració comunal andorrana; document públic · pendent | 1,936 |
| institucions | condicions de reutilització pendents per peça · pendent | 75 |
| institucions | condicions generals d'utilització de la informació de la seu electrònica del BOPA · si | 3,558 |
| institucions | condicions variables per document; identitat gràfica reservada · pendent | 5,922 |
| institucions | contingut periodístic amb drets reservats · no | 324 |
| institucions | domini públic per antiguitat; digitalització de Google Books · si | 30,133 |
| institucions | drets reservats — obra d'autor viu, reedició del 2019, sense llicència explícita identificada · no | 1,815 |
| institucions | drets reservats; sense autorització general de redistribució · no | 1,713 |
| institucions | edició institucional amb drets editorials; accés obert per Dialnet · pendent | 1,070 |
| institucions | informació institucional pública · si | 2,106 |
| institucions | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 56,639 |
| institucions | pendent de determinar per a la peça concreta · pendent | 362 |
| institucions | publicació acadèmica de l'IEC, accés obert · pendent | 232 |
| institucions | publicació acadèmica de la Societat Andorrana de Ciències · pendent | 10,082 |
| institucions | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 34,554 |
| institucions | publicació acadèmica en accés obert · pendent | 9,194 |
| institucions | reutilització autoritzada, comercial i no comercial, per la Decisió 2011/833/UE · si | 4,200 |
| institucions | reutilització autoritzada, comercial i no comercial, per la Decisió 2011/833/UE. Els textos consolidats, CC BY 4.0 · si | 2,990 |
| institucions | sense llicència ni estat de drets declarats a l'ítem digital; termini espanyol per a defuncions anteriors a 1987, vuitanta anys post mortem · pendent | 21,677 |
| llengua | CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària · si | 3,457 |
| llengua | L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 3,883 |
| llengua | drets reservats; cap llicència declarada al document ni al portal · no | 25,599 |
| llengua | drets reservats; cap llicència declarada ni al document ni al portal · no | 2,474 |
| llengua | drets reservats; copyright de l'autor i de l'edició, cap llicència oberta · no | 1,862 |
| llengua | drets reservats; copyright de les autores i de l'edició, cap llicència oberta · no | 5,277 |
| llengua | drets reservats; dos titulars declarats a la pàgina de crèdits, cap llicència oberta · no | 15,211 |
| llengua | drets reservats; sense autorització general de redistribució · no | 2,094 |
| llengua | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 2,032 |
| llengua | publicació acadèmica de l'IEC, accés obert · pendent | 11,274 |
| llengua | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 7,193 |
| llengua | publicació acadèmica en accés obert · pendent | 6,024 |
| llengua | sense llicència declarada; el document no porta pàgina de crèdits, ni ISBN, ni dipòsit legal · no | 1,170 |
| parla | Llicència estàndard de YouTube. El Consell General no declara cap llicència oberta. · pendent | 74,871 |
| parla | Publicacio institucional en obert, sense llicencia declarada als llibres d'actes. La sintesi de Guillamet (2024) SI que porta prohibicio expressa de reproduccio. · pendent | 0 |
| parla | YouTube declara Creative Commons Attribution en vídeos individuals; verificació per peça, no per sèrie. Verificada a #34, #49, #56, #57, #60 i #65. · pendent | 24,683 |
| persones | CC BY-SA 4.0 (Wikipedia) · institucional (alturgell.cat) · pendent | 525 |
| persones | CC BY-SA 4.0 (Wikipedia) · premsa, drets reservats (obituari) · pendent | 523 |
| persones | CC BY-SA 4.0 · pendent | 5,282 |
| persones | CC BY-SA 4.0 · si | 10,795 |
| persones | contingut editorial amb drets reservats · no | 260 |
| persones | drets reservats pels titulars respectius · no | 5,537 |
| persones | drets reservats · citació breu amb atribució · no | 452 |
| persones | llicència no consta · pendent | 120 |
| persones | premsa digital, sense llicència declarada · pendent | 405 |
| persones | premsa, drets reservats; citació breu · no | 461 |
| persones | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 2,208 |
| persones | publicació associativa, sense llicència declarada · pendent | 340 |
| persones | publicació editorial, sense llicència declarada · pendent | 482 |
| persones | publicació institucional, sense llicència declarada · pendent | 1,111 |
| persones | pàgina institucional amb drets reservats · no | 230 |
| politica | CC BY-SA 4.0 · si | 4,582 |
| politica | L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 2,702 |
| politica | PDF d’accés obert; no hi consta una llicència de reutilització · pendent | 1,956 |
| politica | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 6,143 |
| politica | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 40,319 |
| societat | CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària · si | 29,435 |
| societat | CC BY-SA 4.0 · si | 6,118 |
| societat | Domini públic segons la fitxa; cal citar l’autoria coneguda i la procedència · pendent | 648 |
| societat | Fitxa pública amb consulta i rendicions; no consta una llicència específica de reutilització · no | 269 |
| societat | Fitxa pública amb consulta, previsualització i descàrrega; no consta una llicència específica de reutilització · no | 1,916 |
| societat | Fitxes amb View, Preview i Download; sense llicència específica de reutilització · pendent | 1,076 |
| societat | Fitxes públiques amb consulta i rendicions; no consta una llicència específica de reutilització · no | 260 |
| societat | L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 9,520 |
| societat | Publicacio oficial de l'Estat andorra. Les bases reguladores publicades al BOPA num. 1 del 1989 (base d) diuen: les disposicions reproduides al BOPA es poden inserir total o parcialment en altres publicacions sempre que convingui citar-les o transcriure-les, pero NO es poden publicar soles o en colleccio sense autoritzacio escrita previa de l'autoritat de que emanin. · pendent | 9,712 |
| societat | condicions de reutilització pendents per peça · pendent | 346 |
| societat | condicions generals d'utilització de la informació de la seu electrònica del BOPA · si | 9,909 |
| societat | condicions variables per document; identitat gràfica reservada · pendent | 3,405 |
| societat | contingut periodístic amb drets reservats · no | 3,250 |
| societat | drets reservats; cap llicència oberta declarada al volum · no | 7,154 |
| societat | drets reservats; dos titulars declarats a la pàgina de crèdits, cap llicència oberta · no | 10,683 |
| societat | drets reservats; reutilització subjecta a autorització del titular · pendent | 941 |
| societat | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 38,017 |
| societat | publicació acadèmica de l'IEC, accés obert · pendent | 652 |
| societat | publicació acadèmica de la Societat Andorrana de Ciències · pendent | 17,230 |
| societat | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 92,106 |
| societat | publicació acadèmica en accés obert (repositori de l'Institut d'Estudis Catalans) · pendent | 17,251 |
| societat | publicació acadèmica en accés obert · pendent | 5,555 |
| societat | publicació institucional, sense llicència declarada · pendent | 978 |
| societat | text normatiu oficial, ús públic · pendent | 351 |
| territori | CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària · si | 1,264 |
| territori | CC BY 4.0; declaració explícita al PDF p. 26 · pendent | 619 |
| territori | CC BY-SA 4.0 · si | 6,123 |
| territori | L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 26,535 |
| territori | condicions generals d'utilització de la informació de la seu electrònica del BOPA · si | 541 |
| territori | drets específics dels informes pendents; sense llicència oberta general acreditada · pendent | 1,137 |
| territori | drets reservats; dos titulars declarats a la pàgina de crèdits, cap llicència oberta · no | 6,068 |
| territori | drets reservats; reutilització sotmesa a autorització expressa · no | 260 |
| territori | drets reservats; sense autorització general de redistribució · no | 2,101 |
| territori | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 9,062 |
| territori | pendent per a les peces; condicions generals del portal amb drets reservats · pendent | 320 |
| territori | pendent · pendent | 253 |
| territori | pendent; PDF accessible al repositori de l'IEC, sense llicència específica identificada a la peça · pendent | 3,047 |
| territori | pendent; avís legal sense llicència específica de reutilització del BPA identificada · pendent | 176 |
| territori | publicació acadèmica de l'IEC, accés obert · pendent | 1,565 |
| territori | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 7,626 |
| territori | publicació acadèmica en accés obert · pendent | 4,031 |
| vida-quotidiana | CC BY-SA 4.0 · si | 710 |
| vida-quotidiana | norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 8,298 |
| vida-quotidiana | publicació acadèmica de l'IEC, accés obert · pendent | 3,118 |
| vida-quotidiana | publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 1,254 |
| vida-quotidiana | publicació acadèmica en accés obert · pendent | 2,963 |

## Llicències

| Llicència declarada · estat de redistribució | Chunks |
| --- | ---: |
| Accés obert al repositori IEC; no hi consta una llicència de reutilització · pendent | 8 |
| Accés obert al repositori institucional; no hi consta una llicència de reutilització · pendent | 5 |
| Article acadèmic distribuït en PDF; no hi consta una llicència oberta de redistribució · no | 2 |
| Article consultable a RACO; termes de redistribució del text no verificats · no | 2 |
| Article editorial consultable en obert; no s’hi especifica una llicència general de redistribució · no | 2 |
| Article en accés obert amb llicència CC BY 3.0 · pendent | 2 |
| Article web editorial en obert; no hi consta una llicència general de reutilització · pendent | 4 |
| Avís legal general de l'Arxiu Nacional; ús dels continguts reservat llevat d'autorització específica · pendent | 1 |
| CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària · si | 98 |
| CC BY 4.0; declaració explícita al PDF p. 26 · pendent | 1 |
| CC BY-SA 4.0 (Wikipedia) · institucional (alturgell.cat) · pendent | 1 |
| CC BY-SA 4.0 (Wikipedia) · premsa, drets reservats (obituari) · pendent | 1 |
| CC BY-SA 4.0 · pendent | 17 |
| CC BY-SA 4.0 · si | 537 |
| Catàleg institucional; termes de reutilització no especificats · no | 13 |
| Catàleg públic del Govern d’Andorra; condicions del portal · pendent | 6 |
| Condicions generals d'utilització de la informació a la seu electrònica del BOPA; permeten còpia, difusió, adaptació, extracció, reordenació, combinació i distribució amb les condicions indicades. · si | 2 |
| Domini públic segons la fitxa; cal citar l’autoria coneguda i la procedència · pendent | 4 |
| Fitxa amb View, Preview i Download; sense llicència específica de reutilització · pendent | 5 |
| Fitxa institucional; termes de reutilització no especificats · no | 2 |
| Fitxa pública amb consulta i rendicions; no consta una llicència específica de reutilització · no | 5 |
| Fitxa pública amb consulta, previsualització i descàrrega; drets legals atribuïts a Joan Vehils · no | 1 |
| Fitxa pública amb consulta, previsualització i descàrrega; no consta una llicència específica de reutilització · no | 29 |
| Fitxa pública amb permisos de consulta i descàrrega; no consta una llicència específica de reutilització · no | 11 |
| Fitxes amb View, Preview i Download; sense llicència específica de reutilització · pendent | 6 |
| Fitxes públiques amb consulta i rendicions; no consta una llicència específica de reutilització · no | 3 |
| Fitxes públiques amb permisos de consulta i descàrrega; no consta una llicència específica de reutilització · no | 1 |
| L'obra impresa de 1904 és de domini públic per antiguitat. La BnF indica reutilització no comercial gratuïta dels documents de Gallica amb atribució; reutilització comercial subjecta a llicència. El TXT local de Google Books reprodueix una petició d'ús personal, no comercial i sense consultes automatitzades. L'elegibilitat del material per al destí d'entrenament de Maia resta pendent.
 · pendent | 749 |
| La Library of Congress declara no tenir constancia de cap restriccio de drets sobre l'item · si | 2 |
| Licence Etalab 2.0 per a l'edició digital CARo; l'edició bibliogràfica original conserva els seus drets · pendent | 2 |
| Llicència estàndard de YouTube. El Consell General no declara cap llicència oberta. · pendent | 27 |
| Memòria tècnica institucional; no hi consta una llicència oberta de redistribució · no | 2 |
| Nota estadística institucional; no hi consta una llicència de reutilització · pendent | 4 |
| PDF d’accés obert; no hi consta una llicència de reutilització · pendent | 3 |
| Publicacio institucional en obert, sense llicencia declarada als llibres d'actes. La sintesi de Guillamet (2024) SI que porta prohibicio expressa de reproduccio. · pendent | 279 |
| Publicacio oficial de l'Estat andorra. Les bases reguladores publicades al BOPA num. 1 del 1989 (base d) diuen: les disposicions reproduides al BOPA es poden inserir total o parcialment en altres publicacions sempre que convingui citar-les o transcriure-les, pero NO es poden publicar soles o en colleccio sense autoritzacio escrita previa de l'autoritat de que emanin. · pendent | 18 |
| Publicació acadèmica en accés públic; no hi consta una llicència específica de redistribució · no | 2 |
| Publicació institucional en obert, sense llicència declarada · pendent | 2 |
| Publicació institucional en obert; llicència específica de reutilització no indicada · no | 9 |
| Publicació institucional i memòria arqueològica en accés públic; no hi consta una llicència específica de reutilització · no | 2 |
| Publicació oficial; no s'ha localitzat una llicència específica de reutilització de la digitalització · pendent | 16 |
| Pàgina i imatge institucionals; termes de reutilització no especificats · no | 2 |
| Pàgina i imatges institucionals; termes de reutilització no especificats · no | 4 |
| Pàgina periodística en obert, sense llicència de reutilització declarada · no | 3 |
| Pàgines públiques; llicència específica de reutilització no indicada · pendent | 3 |
| Registres institucionals i transcripció web; no hi consta una llicència específica de reutilització · pendent | 3 |
| Text complet visible a ResearchGate; la pàgina indica que pot estar subjecte a drets d’autor · no | 2 |
| Transcripció institucional en obert; no hi consta una llicència de reutilització · pendent | 3 |
| YouTube declara Creative Commons Attribution en vídeos individuals; verificació per peça, no per sèrie. Verificada a #34, #49, #56, #57, #60 i #65. · pendent | 12 |
| accés obert al Dipòsit Digital de la UB · pendent | 9 |
| acta formalitzada d'una administració comunal andorrana; document públic · pendent | 4 |
| butlletí oficial espanyol de 1894; domini públic per antiguitat · si | 3 |
| condicions de reproducció i reutilització dels Archives diplomatiques; el portal mostra llicència Etalab per al web · pendent | 4 |
| condicions de reutilització pendents per peça · pendent | 1 |
| condicions generals d'utilització de la informació de la seu electrònica del BOPA · si | 51 |
| condicions variables per document; identitat gràfica reservada · pendent | 15 |
| contingut editorial amb drets reservats · no | 1 |
| contingut periodístic amb drets reservats · no | 34 |
| document de divulgació per a ensenyants; sense llicència explícita · pendent | 4 |
| document parlamentari oficial de 1895; domini públic per antiguitat · si | 9 |
| domini públic per antiguitat; digitalització de Google Books a partir d'un exemplar de biblioteca · si | 44 |
| domini públic per antiguitat; digitalització de Google Books · si | 102 |
| drets específics del llibre pendents; portal general amb drets reservats · pendent | 9 |
| drets específics dels informes pendents; sense llicència oberta general acreditada · pendent | 2 |
| drets reservats pels titulars respectius · no | 36 |
| drets reservats · citació breu amb atribució · no | 1 |
| drets reservats — obra d'autor viu, reedició del 2019, sense llicència explícita identificada · no | 10 |
| drets reservats; cap llicència declarada al document ni al portal · no | 38 |
| drets reservats; cap llicència declarada ni al document ni al portal · no | 4 |
| drets reservats; cap llicència oberta declarada al volum · no | 14 |
| drets reservats; cap llicència oberta declarada · no | 24 |
| drets reservats; copyright de l'autor i de l'edició, cap llicència oberta · no | 3 |
| drets reservats; copyright de les autores i de l'edició, cap llicència oberta · no | 9 |
| drets reservats; dos titulars declarats a la pàgina de crèdits, cap llicència oberta · no | 53 |
| drets reservats; reutilització sotmesa a autorització expressa · no | 1 |
| drets reservats; reutilització subjecta a autorització del titular · pendent | 2 |
| drets reservats; sense autorització general de redistribució · no | 19 |
| edició institucional amb drets editorials; accés obert per Dialnet · pendent | 2 |
| informació institucional pública · si | 4 |
| instrument de descripció públic; condicions del portal d’arxius · no | 1 |
| llicència no consta · pendent | 1 |
| norma oficial andorrana (pública per naturalesa); la consolidació és feina del projecte · si | 274 |
| obra literària amb drets reservats · no | 2 |
| pendent de determinar per a la peça concreta · pendent | 1 |
| pendent per a les peces; condicions generals del portal amb drets reservats · pendent | 1 |
| pendent · pendent | 1 |
| pendent; PDF accessible al repositori de l'IEC, sense llicència específica identificada a la peça · pendent | 5 |
| premsa digital, sense llicència declarada · pendent | 3 |
| premsa digital, sense llicència oberta declarada · pendent | 1 |
| premsa, drets reservats; citació breu · no | 3 |
| publicació acadèmica de l'IEC, accés obert · pendent | 42 |
| publicació acadèmica de la Societat Andorrana de Ciències · pendent | 63 |
| publicació acadèmica en accés obert (Calaix, Generalitat de Catalunya) · pendent | 488 |
| publicació acadèmica en accés obert (repositori de l'Institut d'Estudis Catalans) · pendent | 45 |
| publicació acadèmica en accés obert · pendent | 77 |
| publicació acadèmica en accés obert; sense llicència de redistribució declarada · pendent | 1 |
| publicació acadèmica, IEC; ús de recerca · pendent | 3 |
| publicació associativa, sense llicència declarada · pendent | 1 |
| publicació editorial, sense llicència declarada · pendent | 5 |
| publicació institucional del Govern d'Andorra; sense llicència oberta identificada · no | 2 |
| publicació institucional en accés obert al web de l'IEA · pendent | 4 |
| publicació institucional en accés públic; sense llicència de redistribució declarada · pendent | 2 |
| publicació institucional i tècnica en accés públic; sense llicència de redistribució declarada · pendent | 2 |
| publicació institucional, sense llicència declarada · pendent | 6 |
| publicació institucional; llicència específica no indicada · pendent | 4 |
| publicació institucional; termes de reutilització no especificats · no | 2 |
| pàgina institucional amb drets reservats · no | 1 |
| pàgina institucional en accés obert; els drets dels documents reproduïts resten dels titulars · pendent | 3 |
| pàgina institucional; llicència específica no indicada · pendent | 3 |
| registre institucional i article acadèmic d'accés obert; condicions específiques per peça · pendent | 1 |
| reutilització autoritzada, comercial i no comercial, per la Decisió 2011/833/UE · si | 8 |
| reutilització autoritzada, comercial i no comercial, per la Decisió 2011/833/UE. Els textos consolidats, CC BY 4.0 · si | 6 |
| sense llicència declarada; el document no porta pàgina de crèdits, ni ISBN, ni dipòsit legal · no | 2 |
| sense llicència ni estat de drets declarats a l'ítem digital; termini espanyol per a defuncions anteriors a 1987, vuitanta anys post mortem · pendent | 62 |
| text normatiu oficial, ús públic · pendent | 1 |
| web i publicació institucionals, sense llicència oberta identificada · no | 1 |
| web institucional, drets reservats; sense llicència oberta identificada · no | 1 |

## Concentració de fonts

| Família de fonts | Documents | Chunks | Quota de documents |
| --- | ---: | ---: | ---: |
| actes-historiques-consell-general | 161 | 279 | 11.6% |
| brutails-coutume-1904 | 161 | 749 | 11.6% |
| wikipedia | 161 | 171 | 11.6% |
| jurisprudencia-ad | 72 | 274 | 5.2% |
| wikipedia-futbol-femeni-andorra | 60 | 86 | 4.3% |
| viquipedia-ca | 58 | 92 | 4.2% |
| estadistica-ad | 31 | 98 | 2.2% |
| consell-general-constituent | 27 | 27 | 1.9% |
| wikipedia-esquiadors-andorrans | 26 | 26 | 1.9% |
| vilar-andorre-1904 | 24 | 102 | 1.7% |
| bopa-ad | 22 | 51 | 1.6% |
| iec-vocabulari-andorra | 22 | 38 | 1.6% |
| premsa-andorrana | 20 | 34 | 1.4% |
| societat-andorrana-ciencies | 14 | 60 | 1.0% |
| rios-urruti-andorra-1920 | 13 | 62 | 0.9% |
| ari-capsules | 12 | 12 | 0.9% |
| wikipedia-museus-andorra | 10 | 16 | 0.7% |
| historia-ad-relat-cronologic | 9 | 21 | 0.6% |
| la-cuestion-de-andorra-1894 | 9 | 44 | 0.6% |
| wikipedia-escacs-andorra | 9 | 14 | 0.6% |

Els estats `no` i `pendent` es registren sense vetar automàticament el corpus,
d'acord amb la constitució §24. L'elegibilitat de publicació continua sent una
decisió del propietari.

## Qualitat i incidències

- Blocs amb `revisar`: 0/20964 (0.00%).
- Blocs classificats com a `nota-treball` i exclosos: 5162.
- Chunks amb detector de PII: 1459; marcats `pendent`, sense emmascarar.
- Paràgrafs de plantilla exactes en tres documents o més: 27; presents en 216 documents; 5 chunks afectats.
- Chunks exclosos per marques ratllades o referències `raw/` residuals: 3.
- Mida de chunks: 11/3559 excepcions (0.31%); límit <2%. Són: `temes/esports/competicio/andorra-als-jocs-olimpics#c3` (69 paraules), `temes/esports/competicio/andorra-als-jocs-olimpics#c4` (574 paraules), `temes/esports/futbol/femeni/futbol-femeni-index-de-fitxes#c1` (38 paraules), `temes/historia/edat-mitjana/del-plet-dels-emprius-al-tribunal-reial-1510-1556#c1` (45 paraules), `temes/historia/edat-mitjana/del-plet-dels-emprius-al-tribunal-reial-1510-1556#c2` (640 paraules), `temes/historia/edat-mitjana/els-privilegis#c1` (142 paraules), `temes/historia/edat-mitjana/els-privilegis#c2` (527 paraules), `temes/historia/moments-historics/la-cronologia-dandorra#c5` (614 paraules), `temes/institucions/consell-general/el-consell-de-la-terra#c4` (136 paraules), `temes/institucions/justicia/cinc-respostes-a-la-mateixa-pregunta#c2` (109 paraules), `temes/societat/educacio/index-legislatiu-en-educacio#c3` (148 paraules).
- Decisions de revisió copiades a chunks: 1316; estats: {'approved': 23, 'pending': 1293, 'unreviewed': 2243}.
- Overrides explícits de `curacio/decisions/overrides.tsv` aplicats: 0; només accepten IDs de chunk existents i mai no reobren PII ni higiene.
- Buits mantinguts: 5246; `raft-sense-oracle` només els conserva com a preguntes, mai com a negacions.
- Paraules exportades a `buits/`: 217,322 (9.9% de l'entrada), per sota del ~24.1% inicial perquè els estats `resolt` i `no-es-buit`, els buits de parla i el text de plantilla no s'exporten.
- Source fonts absents o metadades incoherents consten a `correccions.tsv`.
- Quasi-duplicats marcats: 0; llindar Jaccard ≥ 0.90 sobre shingles de cinc tokens; els casos queden `pendent` i s'informen al motiu de l'inventari.
- Retenció/exclusió: `raft-context` i `coneixement` es filtren per volatilitat; veu de parla segueix separada.
- La comparació d'entrada amb chunks no és una taxa de pèrdua de dades: l'entrada inclou frontmatter, capçaleres,
  enllaços i material editorial. Les notes, plantilles i gaps s'inventarien o es deriven a fitxers separats;
  els chunks `pendent` continuen presents i compten com a conservats. Les xifres per domini mostren aquesta diferència.

### Desviacions que requereixen explicació

- `costums`: 56.1% de paraules fora de chunks entrenables o d'ús (entrada 25,938; retingudes 11,398; diferència 14,540).
- `cultura`: 55.1% de paraules fora de chunks entrenables o d'ús (entrada 88,891; retingudes 39,872; diferència 49,019).
- `economia`: 53.0% de paraules fora de chunks entrenables o d'ús (entrada 172,650; retingudes 81,136; diferència 91,514).
- `esports`: 65.7% de paraules fora de chunks entrenables o d'ús (entrada 181,698; retingudes 62,265; diferència 119,433).
- `gastronomia`: 48.7% de paraules fora de chunks entrenables o d'ús (entrada 11,514; retingudes 5,911; diferència 5,603).
- `historia`: 48.2% de paraules fora de chunks entrenables o d'ús (entrada 331,519; retingudes 171,862; diferència 159,657).
- `institucions`: 54.4% de paraules fora de chunks entrenables o d'ús (entrada 590,452; retingudes 269,157; diferència 321,295).
- `llengua`: 56.3% de paraules fora de chunks entrenables o d'ús (entrada 98,025; retingudes 42,802; diferència 55,223).
- `parla`: 61.9% de paraules fora de chunks entrenables o d'ús (entrada 261,094; retingudes 99,554; diferència 161,540).
- `persones`: 61.7% de paraules fora de chunks entrenables o d'ús (entrada 31,974; retingudes 12,250; diferència 19,724).
- `politica`: 49.4% de paraules fora de chunks entrenables o d'ús (entrada 50,650; retingudes 25,639; diferència 25,011).
- `societat`: 54.1% de paraules fora de chunks entrenables o d'ús (entrada 257,905; retingudes 118,469; diferència 139,436).
- `territori`: 57.3% de paraules fora de chunks entrenables o d'ús (entrada 71,596; retingudes 30,536; diferència 41,060).
- `vida-quotidiana`: 40.2% de paraules fora de chunks entrenables o d'ús (entrada 13,203; retingudes 7,897; diferència 5,306).
- Auditories: 166 vs 387 de partida (-57.1%); la partida comptava blockquotes d'auditoria; ara es compten les ocurrències literals «Auditat el» (les anotacions ja són material exclòs).
- Fragments ratllats: 2,740 vs 2,523 de partida (+8.6%); ara es compten parells `~~...~~` dins de cada línia; el recompte inclou les actualitzacions acumulades a docs/.
- Buits registrats: 17.5% ara vs 18.6% de partida (-6.0%); ara es calcula sobre paraules de fitxers Markdown i extracció de seccions tipades.
- El que falta: 4.9% ara vs 5.5% de partida (-10.4%); ara es calcula sobre paraules de fitxers Markdown i extracció de seccions tipades.
- Related: 4.1% ara vs 3.1% de partida (+31.1%); ara es calcula sobre paraules de fitxers Markdown i extracció de seccions tipades.
- Documents amb plantilles: 216 vs 152 de partida (+42.1%); el recompte complet inclou notes, auditoria, navegació i parla, mentre només els chunks entrenables s'exclouen de l'ús.

## Decisions preses

| Decisió | Raó | Fragments afectats |
| --- | --- | ---: |
| Les fixtures daurades tenen prioritat sobre `estat_revisio` dins del Markdown. L'estat es posa a la fila de chunk d'`inventari.tsv`. | Afegir-lo al frontmatter trencaria la reproducció byte a byte; el valor és traçable a l'inventari sense tocar els oracles. | 3559 |
| La llicència o el permís de redistribució no concloent es conserva com a `pendent`; el detall original continua traçable a les metadades. | Opció conservadora i reversible; no s'inventa una autorització. | 2060 |
| Gaps amb estat `resolt` o `no-es-buit` queden fora de `buits/`; els de parla queden només com a anotacions de mostra. | Evita convertir una resposta coneguda o una limitació en una pregunta falsa. | 1072 |
| Paràgrafs amb ratllats o referències a `raw/` queden fora dels chunks utilitzables. | Són anotacions editorials o rutes locals, no coneixement publicable. | 658 |

## Decisions obertes

- Publicació del corpus i ús redistribuïble: pendent del propietari; 850 documents usen font `no` o `pendent`.
- Tall històric: pendent del propietari; 1423 chunks contenen fets datats abans de 1925.
- Retallada del domini esports: pendent del propietari; 351 chunks d'esports preservats i traçables.
- Llicències no obertes o no concloents es mantenen marcades, no s'han tractat com aprovació de publicació.
- Llengua parlada sense escolta: 40 mostres `pendent-escolta`; marques d'incertesa i perfil no es corregeixen automàticament.
- Llindar de quasi-duplicats i agrupacions addicionals de `familia_font` poden rebre overrides humans als TSV de `curacio/decisions/`.
