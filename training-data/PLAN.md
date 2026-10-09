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

Un sol criteri fallit és motiu per reescriure o rebutjar. El volum no és un objectiu de qualitat.

## Cobertura de Maia Knowledge

L'inventari recorre totes les fitxes de `docs/temes/`, les seccions, les taules, les llistes i els enllaços. La cobertura es mesura sobre coneixement útil identificat, no sobre quantes preguntes hem escrit. Una conversa pot ensenyar diverses afirmacions relacionades; una dada ja ben coberta no necessita una variació cosmètica.

Per cada tema: llegir la font sencera, apuntar què és útil, marcar dubtes humans possibles, redactar només els que valgui la pena respondre, verificar-los i actualitzar cobertura. Registrar també què s'exclou i per què.

## Maia Language

Incloure només peces que compleixin els criteris del corpus per a veu originària, època contemporània i ús lingüístic apte. Respectar la incertesa de les transcripcions i excloure els fragments no verificats segons la política documentada. Preservar lèxic, sintaxi i estil amb normalització mínima. Agrupar els splits per peça o parlant per evitar filtracions.

## Exports

`output/` es manté buit fins que hi hagi revisió humana, comprovació de drets, deduplicació i separació correcta entre train, validation i test. L'export conté només els missatges `user` i `assistant`. Procedència, evidències i decisions editorials queden fora.

Ordre de treball: estructura i criteris → exemples de referència aprovats → cobertura per tema → converses revisades de Knowledge → selecció revisada de Language → deduplicació i validació → splits i exports. No barrejar els dos objectius.

## Treball incremental

Treballar a `main`, tema a tema. Cada conversa nova és un canvi funcional separat: revisar el diàleg i la procedència, executar la validació corresponent, revisar `git status` i el diff, afegir només els fitxers d'aquella conversa, fer-ne un commit i pujar-lo a `origin/main`. No començar la conversa següent fins que el push s'hagi confirmat. No incloure canvis locals aliens al dataset.
