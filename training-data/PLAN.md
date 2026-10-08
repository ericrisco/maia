# Pla de Maia Training Data

## Objectiu

Preparar dos datasets independents i traçables a partir de `docs/`:

- **Knowledge**: converses útils sobre el coneixement d’Andorra de `docs/temes/`.
- **Language**: material oral o escrit real de `docs/parla/`, preservat sense fabricar diàlegs.

Primer calibratem la qualitat amb uns quants exemples. Després ampliem el contingut per tema, registre a registre. No generem exports fins que les converses, les fonts i els drets estiguin revisats.

## Com crear una conversa de Knowledge

1. Llegeix la font i identifica una afirmació que valgui la pena explicar.
2. Pensa en una necessitat humana concreta: entendre què va passar, aclarir una confusió, comparar dues coses o saber què es pot afirmar amb seguretat.
3. Escriu la primera pregunta sense mirar el títol ni els subtítols. Ha de tenir prou context per entendre-la sola.
4. Respon directament i amb el grau de certesa que permet la font.
5. Afegeix un seguiment només si neix d’un detall de la resposta i ajuda a entendre’l millor.
6. Llegeix només els missatges. Si semblen fets per demostrar que s’ha llegit una fitxa, reescriu-los.
7. Verifica cada dada contra les fonts i registra la procedència i els drets en un fitxer separat.

## Quines preguntes busquem

Cada tema pot generar preguntes de tipus diferent, si el material les sosté:

- **Entendre**: «Per què es va construir el santuari de Meritxell en aquell lloc?»
- **Aclarir**: «La imatge que es venera avui és l’original?»
- **Comprovar una coincidència o contradicció**: «Se sap si la data de la festa de Meritxell està relacionada amb la del Pareatge?»
- **Comparar**: «Què diferencia una festa nacional d’una festa major parroquial?»
- **Acotar el que se sap**: «Això és un fet documentat o forma part de la llegenda?»

No cal cobrir tots els tipus per a cada tema. La varietat ha de venir del contingut, no de canviar paraules dins una plantilla.

## Multitorn amb sentit

Una conversa pot tenir d’un a quatre torns d’usuari. La primera resposta resol la pregunta. Cada seguiment surt d’un fet, matís o incertesa que acaba d’aparèixer. No afegim «i què més?» ni saltem a una dada nova només per fer-la multitorn. Una bona resposta completa d’un sol torn és preferible a una conversa artificial.

## Qualitat i precisió

- La pregunta inicial ha de ser comprensible per algú que no ha vist el corpus.
- No esmentis seccions, files, fitxes, corpus, IDs ni camps interns.
- No inventis una experiència personal, una motivació ni argot per fer que el diàleg sembli humà.
- La resposta comença per la informació que resol el dubte. Afegeix només el context útil.
- Distingeix fets, llegendes, interpretacions i hipòtesis.
- No converteixis «la font no ho diu» en «això no va passar».
- Mantén clars els noms, les dates, els llocs i els pronoms al llarg del diàleg.
- Si dues fonts discrepen, conserva la discrepància; no triïs una versió sense base.

## Revisió abans d’acceptar

Una persona revisa cada registre amb tres lectures:

1. **Lectura humana**: sona com una conversa que podria començar sense haver llegit la fitxa?
2. **Lectura factual**: cada afirmació es pot trobar a la font i té el mateix abast?
3. **Lectura de continuïtat**: cada seguiment depèn del diàleg i aporta alguna cosa nova?

Si una lectura falla, es revisa o es descarta. Una conversa natural però inexacta tampoc no passa.

## Format i procedència

El JSONL conversacional té una conversa per línia i només conté `messages` amb rols `user` i `assistant`. Els exemples de `knowledge/examples/` són per calibrar; no s’exporten. Les candidates noves van a `knowledge/review/`. La procedència, les afirmacions i els drets van en un JSONL paral·lel.

Cada conversa aprovada s’afegeix i es valida per separat. Seguint la instrucció de treball, cada conversa tindrà el seu propi commit i push. Els exports només contindran registres aprovats amb drets compatibles amb l’ús previst.

## Maia Language

No convertim monòlegs o transcripcions en preguntes i respostes inventades. Incloem només material humà amb transcripció prou fiable, parlant i font traçables, i drets compatibles. Les peces no elegibles queden anotades a l’inventari amb el motiu.

## Etapes

1. Calibrar preguntes i respostes amb `knowledge/examples/`.
2. Revisar amb l’usuari el criteri i els primers exemples.
3. Crear converses Knowledge tema a tema, amb procedència separada i un commit per conversa.
4. Auditar les peces de Language per veu humana, transcripció i drets.
5. Deduplicar, revisar cobertura i preparar splits per document o parlant.
6. Generar i validar els exports d’entrenament.

Ara mateix només s’ha completat l’etapa 1. Els fitxers de revisió i d’export són buits.
