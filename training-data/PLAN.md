# Pla de Maia Training Data

## Objectiu

Preparar dos conjunts separats a partir de `docs/`:

- **Knowledge**: respostes fiables a dubtes reals sobre Andorra, basades en `docs/temes/`.
- **Language**: llengua humana autèntica de `docs/parla/`, sense convertir monòlegs en diàlegs inventats.

La qualitat de les converses és més important que el volum. Primer calibrem amb pocs exemples; no ampliem la cua fins que l’usuari n’aprovi el to.

## Com escriure preguntes de Knowledge

1. Entén la informació i les seves fonts abans de redactar.
2. Formula el dubte com si la persona no hagués vist cap fitxa. Escriu la pregunta sense mirar-ne el títol ni els subtítols.
3. Usa paraules corrents i context suficient perquè la pregunta s’entengui tota sola.
4. Respon el dubte concret. No recitis el document ni n’exposis l’estructura.
5. Afegeix un seguiment només quan una persona probablement preguntaria més després de llegir la resposta.
6. Verifica totes les afirmacions. Registra separadament la procedència, els drets i els dubtes.

### Com sonen les preguntes humanes

Les persones pregunten perquè volen entendre una cosa, aclarir una confusió, situar un fet o saber què se’n pot afirmar. Sovint fan preguntes curtes. Una pregunta pot tenir context, però aquest context ha de ser necessari i creïble.

Exemples de formes útils:

- «La imatge de Meritxell que hi ha ara és l’original?»
- «Què va passar amb el santuari després de l’incendi?»
- «La Marratxa és el nom del ball o d’un objecte?»
- «Això és una història documentada o una llegenda?»
- «Les fonts coincideixen sobre la data?»

No s’ha de fabricar una anècdota («m’han dit», «he llegit») per donar aparença humana a una pregunta. Tampoc no s’han d’esmentar fitxes, seccions, files, corpus o IDs.

## Multitorn sense farciment

Una conversa pot tenir un o més intercanvis. No exigim que sigui multitorn. Un seguiment vàlid depèn del que s’acaba de dir i aprofundeix en el mateix dubte. Ha de poder llegir-se com una continuació natural, amb referents clars.

No afegim «i què més?» ni una pregunta nova només per arribar a més torns. Si la resposta ja resol la necessitat, la conversa s’acaba. Els exemples de `knowledge/examples/` mostren aquest criteri.

## Com redactar les respostes

- Comença per la resposta directa.
- Escriu com una persona que ajuda, no com una fitxa ni una taula.
- Afegeix només el context necessari per entendre la resposta.
- Explica amb claredat si una dada és una llegenda, una interpretació o un fet documentat.
- Si les fonts discrepen o no permeten concloure, digues-ho sense inventar una resolució.
- No diguis que una cosa no va passar només perquè la font no en parli.
- Mantén noms, dates, llocs i pronoms clars.

## Revisió dels exemples

Abans d’acceptar una conversa, revisa-la sense tenir la font al davant:

1. La pregunta inicial podria sorgir en una conversa real?
2. S’entén tota sola i evita pressupòsits innecessaris?
3. La resposta resol el dubte en llenguatge natural?
4. El seguiment és una reacció probable a la resposta anterior?
5. Cada afirmació i cada matís tenen suport a les fonts?

Si la pregunta sembla un examen sobre un document, si el seguiment sembla obligatori o si la resposta només copia fragments, reescriu-la o descarta-la. No cal salvar tots els exemples.

## Format i drets

El format de conversa és una línia JSONL amb `messages` i rols `user` i `assistant`. La procedència es guarda en un fitxer separat. Els exemples de calibratge no són dades d’entrenament. Cap conversa entra a l’export fins que se n’hagin revisat la qualitat factual i els drets de les fonts.

Cada conversa nova s’afegeix després de revisar-la. Durant la calibració no generem lots ni multipliquem reformulacions d’una mateixa dada.

## Maia Language

Només s’hi considera material humà amb veu originària, època contemporània i `apte_llengua: true`. Cal revisar parlant, transcripció i drets. No s’inventen preguntes per convertir monòlegs en xats. Quan una transcripció és incerta, només es poden aprofitar fragments verificats.

## Etapes

1. Revisar els exemples de calibratge amb l’usuari.
2. Ajustar el criteri fins que les preguntes i respostes sonin bé.
3. Només llavors reprendre la cobertura de Knowledge, tema a tema, amb procedència i drets.
4. Auditar les peces de Language i verificar transcripcions i drets.
5. Revisar duplicats, cobertura i splits; exportar només registres aprovats.
