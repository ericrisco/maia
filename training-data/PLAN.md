# Pla de Maia Training Data

## Objectiu

Preparar dos datasets independents a partir de `docs/`:

- **Knowledge**: converses útils sobre Andorra, correctes i basades en el corpus.
- **Language**: fragments de parla contemporània andorrana, produïts per persones i verificats.

La prioritat és la qualitat. No convertirem cada títol, paràgraf o fila en una pregunta.

## Fase actual: calibrar les converses

1. Escriure tres converses representatives a `knowledge/review/calibration.jsonl`.
2. Revisar si les preguntes sonen naturals quan es llegeixen soles.
3. Ajustar la guia segons aquesta revisió.
4. Només després, reprendre la cobertura de `docs/temes/` per lots petits.

Els exemples de calibratge no compten com a cobertura ni entren als exports.

## Com crear una conversa Knowledge

1. Identificar què voldria entendre una persona. Aquesta intenció és una nota editorial, no part dels missatges.
2. Comprovar que el corpus respon el dubte i que la font permet l'ús previst.
3. Escriure una primera pregunta que s'entengui sense veure cap fitxa.
4. Respondre directament, amb el context necessari per no confondre recompte, proporció, estimació o causa.
5. Afegir un seguiment només si neix d'un dubte plausible sobre la resposta anterior.
6. Aturar-se quan la persona ja té la resposta. No allargar el fil per complir una quota de torns.
7. Guardar la procedència i les afirmacions cobertes fora de `messages`.

La conversa acostuma a tenir dos o tres intercanvis. Una pregunta simple pot tenir-ne un. No inventem biografies ni experiències personals per fer-la semblar humana.

## Criteri de qualitat

- La pregunta inicial tracta un dubte real, una confusió, una comparació o una decisió.
- No demana què diu una fitxa, una secció, una taula o una fila.
- Cada pregunta s'entén amb el context de la conversa, sense identificadors interns.
- Cada resposta comença per contestar i sona natural en veu alta.
- Les dades porten període i unitat quan cal.
- Una coincidència temporal no es presenta com una causa.
- Les fonts, els drets i els límits consten a la procedència.
- Si el corpus no ho resol, la resposta diu què se sap i què no.
- No s'accepten preguntes gairebé idèntiques només per augmentar volum.

## Cobertura Knowledge

Després d'aprovar l'estil, inspeccionar `docs/temes/` de manera exhaustiva. Cobrir el coneixement útil, incloses dates, xifres, relacions, excepcions, divergències i buits explícits. Una unitat no queda coberta només perquè s'hagi llegit: cal una conversa útil o una exclusió justificada.

Guardar inventari i decisions a `knowledge/work/`. No posar IDs ni metadades internes als missatges d'entrenament. Deduplicar i separar els exemples relacionats abans de crear `train`, `validation` i `test`.

## Maia Language

Mantenir un flux separat. Només admetre material que compleixi `veu == originaria`, `epoca == contemporania` i `apte_llengua == true`. Verificar les transcripcions i conservar les paraules de les persones. No inventar respostes per imitar el català andorrà.

## Exports

No crear exports fins que hi hagi registres aprovats i una revisió de cobertura, procedència, duplicats i splits. Cada línia final serà una conversa JSONL amb `messages`; la informació editorial quedarà en fitxers separats.
