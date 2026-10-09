# Pla de Maia Training Data

## Objectiu

Preparar dos conjunts d'entrenament separats a partir de `docs/`:

- **Maia Knowledge**: respostes útils sobre Andorra, basades en `docs/temes/`.
- **Maia Language**: català andorrà contemporani produït per persones, a partir de `docs/parla/`.

Knowledge ensenya què pot explicar Maia. Language conserva com s'expressa la gent. No es redactaran respostes noves fent veure que són parla real.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── examples/       # Converses de referència, mai incloses a l'export
│   ├── calibration/    # Mostra de redacció; no són registres d'entrenament
│   ├── review/         # Candidats amb conversa i procedència separada
│   ├── archive/        # Candidats rebutjats, amb motiu
│   ├── work/           # Inventari i mapa de cobertura auditables
│   ├── reports/        # Estat, incidències i cobertura
│   ├── scripts/        # Eines de lectura i validació
│   └── output/         # Exports només després d'aprovar-los
└── language/
    ├── review/         # Decisions sobre fragments i transcripcions
    ├── work/           # Fragments de treball amb origen identificat
    ├── reports/        # Drets, incertesa i cobertura
    └── output/         # Exports només després d'aprovar-los
```

Els fitxers de `review/` tenen converses llegibles i un fitxer de procedència separat. Els missatges d'entrenament no inclouen IDs interns, noms de fitxer ni notes editorials.

## Com escriure Knowledge

### Pla de recuperació: corregir la manera de preguntar

Els registres que pregunten què explica una secció, què diu una fila o què
indica un gràfic no passen la revisió. Fan que l'usuari sembli llegir el mateix
document que qui l'ha escrit, i sovint produeixen respostes penjades o massa
curtes. No s'han de reparar canviant només «secció» per «text»: cal tornar a la
necessitat humana que podria haver originat la consulta.

Per a cada conversa nova, treballa en aquest ordre:

1. **Anota el dubte humà en una frase interna**, per exemple: «vol saber si un
   cònsol podia ser demandat per un deute» o «ha sentit dues xifres i vol saber
   si es contradiuen». Aquesta nota no entra als missatges.
2. **Amaga títols, subtítols, IDs i estructura de la fitxa.** Redacta la primera
   pregunta només a partir del dubte. Dona el context històric necessari i no
   pressuposis que l'usuari coneix un terme local.
3. **Contesta de cara.** La primera frase ha de resoldre la pregunta. Després
   afegeix el matís que evita una conclusió errònia.
4. **Continua des de la resposta.** El torn següent ha de ser una aclaració
   plausible que una persona faria després d'escoltar-la. No canviïs de tema ni
   preguntis el mateix amb altres paraules.
5. **Llegeix-ho sense la font.** Si sona a examen, a visita guiada per una fitxa
   o a pregunta escrita per encabir una dada, reescriu-ho o descarta-ho.
6. **Verifica cada afirmació i la procedència** després de tenir una conversa
   natural. No deixis que una bona pregunta justifiqui una resposta no
   documentada.

La pregunta no s'ha de redactar davant d'una taula o d'un fragment i després
«naturalitzar» superficialment. El context pot sortir de la font, però la
motivació de la pregunta ha de ser comprensible fora d'aquella font.

#### Ordre del nou treball

1. Mantenir els registres defectuosos fora de qualsevol exportació i revisar-los
   un per un; no donar-los per bons perquè tinguin dos torns o provenance.
2. Preparar un grup curt d'exemples de calibratge en
   `knowledge/calibration/`. Són referències d'edició, no dades d'entrenament ni
   exemples exportables.
3. Revisar els exemples en veu alta i amb la porta de qualitat d'aquesta guia.
   Només després d'aprovar-los com a patró, redactar registres nous per tema.
4. Treballar en lots petits. Per cada lot, revisar naturalitat, fidelitat,
   procedència i drets abans de passar al tema següent.
5. Quan el patró sigui estable, reprendre la cobertura exhaustiva. No generar
   volum per compensar preguntes que no funcionen.

### 1. Comença per la necessitat d'una persona

Abans de redactar, descriu en una frase què vol saber o resoldre la persona. Per exemple: «vol anar a una festa i entendre què veurà», «ha sentit un terme i vol saber què implica» o «dues fonts li han donat dates diferents».

La pregunta no s'ha de generar a partir del títol, una secció, una fila o un paràgraf. No fer preguntes com «Què explica aquesta fitxa?» o «Què diu aquesta taula?». Si no trobem una curiositat humana al darrere, deixem aquella informació al mapa de cobertura sense forçar una conversa.

### 2. Escriu una pregunta que s'entengui sense el corpus

La primera intervenció ha de donar el context necessari amb paraules normals. Pot sonar informal o incloure una premissa equivocada, però no ha de fingir una experiència personal ni afegir detalls que la font no documenta.

Comprova-ho així: mostra només la pregunta a algú que no hagi vist la fitxa. Si no pot entendre què pregunta, afegeix context. Si només té sentit davant d'una pàgina concreta, torna a formular-la des de la necessitat de la persona.

### 3. Contesta primer; matisa després

La primera frase resol la pregunta. Després s'hi pot afegir el context que ajudi a entendre la resposta. No començar amb fragments penjats, llistes sense introducció ni fórmules del tipus «tres coses que el corpus registra».

Distingeix entre un fet documentat, una afirmació atribuïda a una font i una interpretació. Si la font no ho diu, no ho completis amb el que sembli més probable.

### 4. Fes multitorn només quan hi ha continuació natural

Cada registre de Knowledge ha de tenir diversos torns: com a mínim dues preguntes de l'usuari, amb una resposta entre elles. Després de cada resposta, pregunta't què voldria aclarir algú de debò. El seguiment ha de dependre del que s'acaba de dir i demanar una cosa nova. Si no surt cap seguiment natural, busca una connexió legítima amb una altra dada del tema; no inventis una curiositat ni forcis un canvi de tema.

No afegeixis seguiments només per arribar al mínim de torns. No repeteixis la pregunta amb altres paraules. No facis que l'usuari conegui d'entrada un terme local si el diàleg pot introduir-lo de manera natural. Si la informació no permet una continuació honesta, marca la unitat com a coberta sense conversa i documenta el motiu; la qualitat i la veracitat tenen prioritat sobre el format multitorn.

### 5. Revisa el diàleg sense mirar les fonts

Llegeix tots els torns en veu alta, com una conversa. Rebutja o reescriu el registre si sona a examen, índex, interrogatori, resum escolar o intercanvi construït per encaixar una dada. Després comprova cada afirmació contra la font i registra la procedència fora del text visible.

## Porta de qualitat

Un candidat només entra a `knowledge/review/` si:

- la primera pregunta expressa una curiositat recognoscible i s'entén tota sola;
- la resposta resol la pregunta amb naturalitat i sense preàmbuls interns;
- cada seguiment és plausible, aporta una pregunta nova i neix del torn anterior;
- no s'han inventat context, intencions, causes, dates ni detalls;
- les discrepàncies, els límits i les atribucions queden clars;
- les afirmacions es poden rastrejar fins a una font amb drets registrats;
- el diàleg funciona llegit en veu alta, sense veure el títol de la fitxa.

Prova ràpida per a cada torn: **«Ho preguntaria algú que no té la fitxa oberta?**
**La resposta li serveix sense haver de preguntar què vol dir la pregunta?»**
Si alguna resposta és no, el registre no està llest.

Un sol criteri fallit és motiu per reescriure o rebutjar. El volum no és un objectiu de qualitat.

## Cobertura de Maia Knowledge

L'inventari recorre totes les fitxes de `docs/temes/`, les seccions, els paràgrafs, les taules, les llistes i els enllaços. La cobertura es mesura sobre coneixement útil identificat, no sobre quantes preguntes hem escrit. Una conversa pot ensenyar diverses afirmacions relacionades; una dada ja ben coberta no necessita una variació cosmètica.

Per cada tema: llegir la font sencera, apuntar què és útil, marcar dubtes humans possibles, redactar les converses que valgui la pena respondre, verificar-les i actualitzar cobertura. Registrar també què s'exclou i per què.

**Cap tema ni unitat útil no queda sense decisió.** Cada afirmació, xifra, relació, excepció o límit identificat ha d'acabar en una d'aquestes situacions:

1. cobert per una conversa natural amb evidència i procedència;
2. reservat per a retrieval perquè és volàtil o necessita actualització;
3. exclòs amb un motiu concret, com ara contingut estructural, manca de suport o absència d'una pregunta humana possible.

La decisió és traçable al registre de cobertura. Una conversa pot cobrir diverses unitats, però una unitat no es marca coberta només perquè aparegui al mateix document.

## Maia Language

Auditar totes les peces de `docs/parla/`. Incloure només fragments amb parlant original, català contemporani, `apte_llengua == true`, transcripció prou fiable i procedència/drets registrats. Respectar la incertesa i documentar cada inclusió i exclusió.

Language conserva llengua humana real. Si la peça conté una pregunta real de l'entrevistador i una resposta, es pot mantenir aquell intercanvi. No s'inventa una pregunta per a un monòleg ni es reescriu la resposta per imitar la persona. Preservar lèxic, sintaxi i estil amb normalització mínima. Agrupar train, validation i test per peça o parlant per evitar filtracions.

## Exports

`output/` es manté buit fins que hi hagi revisió humana, comprovació de drets, deduplicació i separació correcta entre train, validation i test. L'export conté només els missatges `user` i `assistant`. Procedència, evidències i decisions editorials queden fora.

Ordre de treball: estructura i criteris → exemples de referència aprovats → cobertura per tema → converses revisades de Knowledge → selecció revisada de Language → deduplicació i validació → splits i exports. No barrejar els dos objectius.

## Definició d'acabament

Maia Training Data no es considera complet fins que:

- totes les fitxes de `docs/temes/` tenen cobertura revisada i cap unitat útil queda sense una de les decisions anteriors;
- totes les peces de `docs/parla/` tenen decisió d'elegibilitat, transcripció i drets;
- Knowledge i Language tenen converses de qualitat, deduplicades i amb procedència separada;
- train, validation i test són exportats i validados sense filtració entre conjunts ni entre parlants/peces;
- els informes de cobertura, exclusions, drets, volum i qualitat concorden amb els exports.

Els fets volàtils —com ara legislació vigent, preus, càrrecs i horaris— es documenten i es comptabilitzen, però es reserven per a retrieval segons la constitució del projecte; no s'entrenen als pesos.

## Treball incremental

Treballar a `main`, tema a tema. Cada conversa nova és un canvi funcional separat: revisar el diàleg i la procedència, executar la validació corresponent, revisar `git status` i el diff, afegir només els fitxers d'aquella conversa, fer-ne un commit i pujar-lo a `origin/main`. No començar la conversa següent fins que el push s'hagi confirmat. No incloure canvis locals aliens al dataset.
