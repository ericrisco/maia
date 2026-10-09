# Pla de Maia Training Data

## Objectiu

Crear converses útils, fidels al corpus i naturals per entrenar dos conjunts separats: `knowledge/` a partir de `docs/temes/` i `language/` a partir de parla humana elegible de `docs/parla/`.

## Criteri principal: una necessitat humana

La guia editorial obligatòria és [`knowledge/review/EXEMPLES.md`](knowledge/review/EXEMPLES.md). Els exemples de [`knowledge/examples/`](knowledge/examples/) ajuden a calibrar l'estil, però no compten com a registres ni com a cobertura.

Abans d'escriure una pregunta, redacta en privat què intenta resoldre la persona: orientar-se abans d'una visita, aclarir un terme, entendre una diferència, comprovar una dada que ha sentit o saber què es pot afirmar quan les fonts discrepen. La pregunta ha de néixer d'aquesta necessitat, no de l'estructura de la fitxa.

Evita preguntes que esmentin «la fitxa», «la secció», «la taula», «aquesta fila» o que demanin resumir un fragment. Evita també preguntes que només es poden entendre llegint la font. Inclou a la primera intervenció el context que necessitaria algú que no ha vist el corpus.

## Converses multitorn sense torns artificials

Les mostres de referència són multitorn. En una conversa nova, afegeix un seguiment només si una persona podria fer-lo després d'escoltar la resposta. Ha de demanar una cosa nova i continuar el fil: aclarir una implicació, posar a prova una premissa, demanar un detall relacionat o decidir què fer amb la informació.

No repeteixis la pregunta amb sinònims, no canviïs de tema per complir una quota i no facis que l'usuari conegui d'entrada noms que encara no s'han introduït. Si el corpus no permet un seguiment natural, conserva la dada a la cobertura i no inventis un torn. Una conversa curta i bona val més que una conversa llarga i forçada.

## Respostes

La primera frase ha de contestar directament. Després, afegeix només el context que ajudi a entendre la resposta. Escriu com un assistent que parla amb una persona: frases completes, referents clars i termes locals explicats quan apareixen. No copiïs camps de metadades ni comencis amb fragments com «tres coses que...». No afegeixis motius, intencions, dates o conclusions que les fonts no sostinguin.

Quan les fonts discrepen, explica què diu cadascuna i què no es pot concloure. Quan una dada no consta, digues-ho sense omplir el buit. Atribueix les interpretacions a qui les proposa.

## Procés per cada candidat

1. Llegeix el document complet i localitza els fets rellevants; no redactis a partir del títol o d'un sol encapçalament.
2. Escriu una frase d'intenció humana que expliqui per què algú faria la pregunta.
3. Redacta la conversa sense mirar el títol de la fitxa. Llegeix-la en veu alta.
4. Verifica cada afirmació i cada seguiment contra les fonts del corpus.
5. Desa la conversa a `knowledge/review/conversations.jsonl` i la procedència, llicència i evidències a `knowledge/review/provenance.jsonl`.
6. Marca la revisió humana i els drets. Cap candidat pendent no és exportable.
7. Registra cobertura, exclusions i dubtes sense convertir cada unitat de coneixement en una pregunta obligatòria.

Treballa sobre `main`. Cada conversa candidata és un canvi separat: una sola conversa, la seva procedència i l'actualització de cobertura. Valida-la, revisa el diff, fes-ne commit i puja-la a `origin/main` abans de redactar la següent.

## Porta de qualitat

Accepta una conversa només si la pregunta inicial és comprensible i plausible sense la fitxa, la resposta resol el dubte, cada seguiment continua el fil amb una pregunta nova, el diàleg sona natural llegit en veu alta, i totes les afirmacions tenen evidència i drets registrats. Si falla un criteri, reescriu o exclou-la.

## Separació de datasets

**Knowledge:** només informació factual derivable de les fonts de Maia. La procedència i les notes editorials no van al text d'entrenament.

**Language:** només peces que compleixen `veu == originaria`, `epoca == contemporania` i `apte_llengua == true`, subjectes a drets i qualitat de transcripció. Les respostes s'han de basar en parla humana autèntica; no s'inventen exemples de «com parlaria un andorrà».

## Cobertura, revisió i exportació

La cobertura es mesura sobre informació útil identificada al corpus, no sobre el nombre de registres. Les dades no han d'aparèixer en una conversa si això la fa artificial. Deduplica abans de separar conjunts. Agrupa Language per peça o parlant per evitar filtracions entre train, validation i test.

Mantén `output/` buit fins que hi hagi revisió humana, drets verificats, deduplicació, splits i validació. L'export conté només missatges `user` i `assistant`; les fonts i decisions es queden als fitxers de procedència.

## Fases

1. Acordar aquest criteri i revisar les mostres de `knowledge/examples/`.
2. Reconstituir l'inventari i el mapa de cobertura des del corpus actual.
3. Crear i revisar converses Knowledge per temes, sense generar variants cosmètiques.
4. Auditar drets, transcripcions i selecció de Language.
5. Deduplicar, fer splits, validar i només llavors exportar.
