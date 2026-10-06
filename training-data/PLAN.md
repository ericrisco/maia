# Maia Training Data: pla de conversa

## Objectiu

Preparar dos conjunts separats a partir de `docs/`:

- **Knowledge**: converses que resolen dubtes reals sobre Andorra, amb fets sustentats per `docs/temes/`.
- **Language**: parla humana andorrana contemporània, conservada des de `docs/parla/` segons el contracte del corpus.

Aquest pla fixa com escriure exemples. No converteix cada secció, fila o dada en una pregunta. La cobertura s'audita per separat: si una dada no dona peu a una pregunta humana, es registra com a no representada i no es força.

## La regla principal

**Primer imaginem el dubte d'una persona; després busquem si el corpus el pot respondre.**

No escrivim una pregunta mirant un títol, una fila o una unitat de cobertura. La fitxa és evidència, no l'escena de la conversa.

Una bona pregunta ha de passar aquestes proves:

1. **Sentit propi:** s'entén sense obrir una fitxa ni llegir una nota editorial.
2. **Motiu humà:** és un dubte, una curiositat, una decisió pràctica o una confusió que una persona podria tenir.
3. **Llengua parlada:** sona natural en veu alta i no sembla un enunciat d'examen.
4. **Abast clar:** demana una cosa principal. No apila lloc, data, participants i significat en una sola pregunta.
5. **Resposta possible:** el corpus conté evidència suficient, o bé permet dir clarament què no se sap.

Si una pregunta només existeix per cobrir una dada, es descarta. La dada es manté al report de cobertura amb el motiu «no hi ha una pregunta natural identificada».

## Com escriure cada conversa

1. **Llegeix la fitxa sencera i les seves fonts.** Revisa també correccions, límits i divergències.
2. **Anota el dubte humà en una frase interna.** Per exemple: «He sentit una cosa sorprenent i vull saber si és certa» o «vull entendre què veuré si hi vaig».
3. **Escriu només la intervenció de l'usuari.** No copiïs el vocabulari del títol si una persona no l'usaria.
4. **Llegeix-la sense resposta ni font.** Si no s'entén, afegeix només el context que una persona diria de debò. Si continua sonant forçada, elimina-la.
5. **Contesta al principi.** Després afegeix el context necessari per entendre la resposta. No aboquis tota la fitxa.
6. **Afegeix un seguiment només si neix del torn anterior.** Ha de demanar una cosa nova que ara és natural voler saber. No ha de repetir, examinar ni obrir un qüestionari.
7. **Revisa cada afirmació contra l'evidència i la procedència.** Marca una llegenda com a llegenda, una interpretació com a interpretació i una discrepància com a no resolta.
8. **Llegeix el diàleg sencer en veu alta.** Si cap persona no el diria així, reescriu-lo o descarta'l.

No hi ha una llargada obligatòria. Un intercanvi és suficient si resol el dubte. Un multitorn és millor només quan la conversa avança de manera creïble.

## Patrons útils, no plantilles

Busca situacions com aquestes, sense convertir-les en fórmules repetides:

- Algú ha sentit una afirmació sorprenent i vol comprovar-la.
- Algú ha vist una festa o un costum i vol entendre què hi passa.
- Algú confon dues coses semblants i vol saber la diferència.
- Algú planeja anar a un lloc o acte i necessita un detall concret.
- Una resposta genera una pregunta de seguiment sobre un element que acaba d'aparèixer.
- Dues versions no coincideixen i la persona vol saber si s'ha pogut aclarir.

No inventis una experiència personal de qui pregunta. «M'han dit que...» pot introduir un dubte corrent; «jo hi era i vaig veure...» només es pot fer servir si la conversa humana original existeix.

## Respostes

- Resol la pregunta abans de donar context.
- Fes servir llengua natural i prou detall perquè la resposta serveixi.
- No copiïs etiquetes de taula ni llistes de metadades.
- No afegeixis fets que només semblen plausibles.
- No presentis una pràctica històrica com a regla actual.
- Quan la font no ho permet, digues-ho amb claredat i sense especular.
- No incloguis IDs, procedència, estats editorials ni comentaris del pipeline als missatges entrenables.

## Registre intern i sortida

`knowledge/review/conversations.jsonl` desa una conversa candidata per línia, amb només `messages`. La seva traça de fonts, evidència, drets i revisió viu separada a `provenance.jsonl`. Els exemples de `EXEMPLES.md` són editorials i no són registres aprovats.

`work/` i `reports/` serveixen per inventariar evidència i auditar cobertura. No són missatges d'entrenament. `output/` només conté registres revisats per al destí previst i amb drets compatibles. Knowledge i Language no es barregen.

Abans d'incloure material d'una font, registra'n llicència i condicions a `docs/raw/` i `docs/fonts/`. Accés públic no implica permís de redistribució ni d'entrenament.

## Revisió abans d'acceptar una mostra

- La pregunta sona com una cosa que algú demanaria sense veure la fitxa?
- El context de la pregunta és creïble i necessari?
- La resposta contesta de seguida i no s'allarga per buidar la font?
- Cada afirmació surt de les evidències registrades?
- El seguiment és una reacció natural i demana una dada nova?
- La incertesa o el límit de la font es conserva?
- La llicència, l'atribució i el permís d'ús són traçables?

Un «no» a naturalitat o evidència vol dir reescriure o descartar. Un permís pendent impedeix exportar per al destí que el requereix.

## Ordre de treball

1. Inventariar tots els documents, seccions, taules, llistes, relacions, incerteses i buits de `docs/temes/`.
2. Reconciliar cada unitat d'evidència amb una conversa natural, una conversa existent o una exclusió raonada. No ometre contingut en silenci.
3. Generar candidates des de dubtes recognoscibles, no des de files de cobertura. Fer revisió editorial i factual abans d'acceptar-les.
4. Revisar totes les peces de `docs/parla/` segons el contracte. Conservar llengua humana; no convertir monòlegs en diàlegs inventats.
5. Registrar procedència i drets, validar cada mostra, actualitzar cobertura i mantenir quarantena per a registres rebutjats o antics.
6. Deduplicar per intenció i contingut. Agrupar exemples relacionats abans de crear `train`, `validation` i `test`.
7. Exportar només registres aprovats per al seu ús previst i publicar recomptes, exclusions, qualitat i limitacions.

La prioritat és correcció, naturalitat, cobertura, diversitat i després volum. Cap quota de registres justifica una conversa artificial.
