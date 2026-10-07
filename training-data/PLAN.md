# Pla de Maia Training Data

## Objectiu

Crear dos datasets separats i complets a partir del corpus `docs/`:

- **Knowledge:** tot el coneixement entrenable de `docs/temes/`.
- **Language:** senyal lingüístic humà autèntic de `docs/parla/`.

La prioritat és correctesa, cobertura, naturalitat, drets i absència d'al·lucinacions. El volum ve després.

## Maia Knowledge: cobertura completa

S'ha de revisar cada fitxa de `docs/temes/`, tema per tema. Cal llegir-ne cada afirmació, apartat, llista, taula, data, relació, discrepància, correcció i buit explícit. Els índexs i enllaços serveixen per trobar relacions entre fitxes. No es marca una fitxa com a coberta només perquè tingui una conversa.

Abans de redactar, registrar per a cada fitxa: elegibilitat, font i llicència, unitats de coneixement detectades, unitats cobertes, incerteses i preguntes obertes. Si una font té drets pendents o no permet la reutilització prevista, no se n'afegeix contingut al dataset fins a resoldre-ho.

## Com escriure cada conversa

1. Escriure en una frase què vol aclarir una persona i per què ho preguntaria.
2. Formular la pregunta sense tenir la fitxa al davant. Ha de ser completa i comprensible per si sola.
3. Contestar el dubte directament a la primera frase, amb el context que calgui per no induir a error.
4. Fer seguiments que surtin de la resposta anterior. Normalment hi ha dos o tres intercanvis; no allargar si el dubte ja està resolt.
5. Comprovar cada afirmació contra fonts amb drets compatibles. No convertir interpretacions, tradicions o correlacions en fets provats.
6. Llegir només els torns d'usuari: han de formar una conversa coherent i plausible, no una llista d'exercicis.

No s'accepten preguntes sobre «la secció», «la fila» o «la fitxa»; respostes fragmentàries; preguntes que demanen llistes sense motiu; seguiments desconnectats; ni afirmacions que la font no sosté. No s'inventen experiències personals.

## Registres Knowledge i traçabilitat

`knowledge/review/conversations.jsonl` conté una conversa per línia en format de fine-tuning: només `messages`, amb rols alterns `user` i `assistant`. La procedència és paral·lela a `knowledge/review/provenance.jsonl`, mai dins del diàleg.

Per cada conversa s'afegeix exactament una línia a cadascun dels dos fitxers. Cada conversa acceptada és un commit separat a `main`, i es fa push abans de continuar amb la següent. El commit inclou també l'actualització d'estat o cobertura necessària per saber quines unitats queden pendents.

`knowledge/review/calibration.jsonl` i `EXEMPLES.md` són exemples editorials, no dades actives i no compten per a cobertura.

## Knowledge: revisions i sortida

Cada conversa passa revisió factual, editorial, de drets, naturalitat i duplicats. Les respostes han de ser autosuficients i no han d'afegir informació només per fer-les més llargues. Les dades actuals han de dur una data i una font vigent.

Abans dels exports, s'han de cobrir tots els documents elegibles i informar de les exclusions. Es dedupliquen preguntes i respostes sense eliminar varietat útil. Train, validation i test se separen per tema/font o grup de converses relacionades, no a l'atzar després de crear paràfrasis. Els exports són `knowledge/output/{train,validation,test}.jsonl`.

## Maia Language

La font és `docs/parla/`. Només és elegible el material que compleix `veu: originaria`, `epoca: contemporania` i `apte_llengua: true`, després de revisar drets i fiabilitat de transcripció.

La resposta ha de provenir de parla humana autèntica, amb normalització mínima i documentada. No s'inventen frases «com les diria un andorrà», ni contextos o seguiments que no siguin fidels a la peça. Si una transcripció és incerta, se n'exclou el fragment dubtós o tota la peça segons el cas, i se'n registra el motiu.

Les peces elegibles s'inventarien totes. Els splits s'agrupen per entrevista, peça i, quan es pugui, parlant, per evitar leakage. Els exports són `language/output/{train,validation,test}.jsonl`.

## Estructura de treball

- `knowledge/review/`: guia, calibratge, converses actives i procedència.
- `knowledge/work/`: inventari, elegibilitat i cobertura per fitxa/unitat.
- `knowledge/scripts/`: generació, validació, deduplicació i splits.
- `knowledge/reports/`: cobertura, drets, exclusions i qualitat.
- `knowledge/output/`: exports revisats.
- `language/`: mateixes fases, amb criteris propis de fidelitat lingüística.

## Definition of done

Knowledge no està acabat fins que totes les fitxes elegibles de `temes/` s'han inspeccionat, les unitats útils tenen cobertura, les fonts i drets són traçables, les converses són naturals i correctes, els duplicats s'han revisat i els tres splits passen els validadors.

Language no està acabat fins que totes les peces de `parla/` s'han inspeccionat, només s'ha inclòs material elegible i fiable, la parla humana es conserva, els drets són clars, no hi ha leakage entre splits i els validadors passen.
