# Pla de treball de Maia Training Data

## Objectiu

Crear dos datasets separats i complets: **Maia Knowledge**, que representi tot
el coneixement entrenable de `docs/temes/`, i **Maia Language**, que incorpori
tot el material lingüístic humà elegible de `docs/parla/`. Es treballa tema a
tema i conversa a conversa. No s'omet cap tema perquè sigui gran o difícil.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── review/
│   │   ├── EXEMPLES.md          # mostres editorials, no són dades d'entrenament
│   │   ├── CONVERSATION-GUIDE.md
│   │   ├── conversations.jsonl  # només converses aprovades
│   │   └── provenance.jsonl     # font i revisió, fora de l'export
│   ├── work/                    # inventari i cobertura
│   ├── scripts/
│   ├── output/                  # exports quan n'hi hagi prou
│   └── reports/
└── language/
    ├── README.md
    ├── review/
    ├── work/
    ├── output/
    └── reports/
```

## Com decidim si una conversa val la pena

1. Tria una necessitat recognoscible: planificar una visita, entendre una
   tradició, aclarir una diferència, comprovar una afirmació o saber què se sap.
2. Escriu la pregunta com la diria algú que no té la fitxa al davant. No preguntis
   per seccions, files, gràfics ni pel corpus.
3. Respon primer el dubte. Afegeix només el context necessari per no induir a
   error.
4. Afegeix un seguiment només si neix del que acaba de dir Maia. Una conversa
   d'un sol intercanvi és vàlida.
5. Contrasta cada afirmació amb les fonts i conserva els matisos: data, lloc,
   incertesa, llegenda o desacord.
6. Rebutja la conversa si la pregunta només serveix per buidar una fitxa, si
   repeteix una altra amb sinònims o si la resposta sona a camps d'una taula.

### Forma d'una conversa

- La primera pregunta ha de tenir un motiu recognoscible i prou context per
  entendre-la sense obrir cap fitxa.
- En cada torn, l'usuari pregunta el que probablement voldria aclarir després
  de sentir la resposta anterior. El seguiment no és una segona pregunta
  independent disfressada de diàleg.
- S'accepten converses d'un sol torn. No s'allarga un diàleg només per fer-lo
  semblar multitorn.
- Les preguntes poden ser directes i informals. Evita fórmules de qüestionari,
  referències a apartats o taules, i peticions de llistes sense cap propòsit.
- Les mostres de `knowledge/review/EXEMPLES.md` són converses completes de
  calibratge, però no compten com a dades ni com a cobertura.

No hi ha una quota fixa de preguntes per document. Però cal revisar totes les
fitxes i representar tot el coneixement útil: una conversa pot cobrir diversos
fets relacionats, i un tema pot necessitar moltes converses. Si una unitat no
admet una pregunta natural per si sola, busca una conversa on ajudi a explicar
un concepte més ampli. Només es deixa fora si no aporta coneixement entrenable;
la decisió i el motiu queden al report de cobertura. No es pot marcar un tema
complet si queda contingut útil sense revisar.

## Revisió abans d'afegir un registre

- La pregunta té sentit sense veure cap document.
- Es podria imaginar una persona fent-la en aquella situació.
- La resposta contesta de seguida i no afegeix una explicació de farciment.
- Cada torn posterior reprèn clarament el fil.
- No es presenta una llegenda, interpretació o hipòtesi com un fet verificat.
- La procedència i els drets consten a `provenance.jsonl`.
- El registre no duplica una conversa existent.

Les mostres de `knowledge/review/EXEMPLES.md` fixen el to. No s'han de copiar
com a plantilles.

## Registre i separació dels datasets

Una conversa aprovada ocupa una línia de `knowledge/review/conversations.jsonl`
i només conté `messages` amb rols `user` i `assistant`. La font, la llicència,
la revisió i els avisos de drets queden a `provenance.jsonl`, mai al text que
aprèn el model. Els valors `no` i `pendent` s'han de mostrar com a avisos segons
`docs/CONTRACT.md`; no es canvien ni s'amaguen.

Maia Language segueix un procés separat. Cal inspeccionar totes les peces de
`docs/parla/` i incloure el material contemporani elegible de veu humana quan
es pugui conservar amb fidelitat. No es creen preguntes o respostes fictícies
per convertir monòlegs en diàlegs. Els fragments dubtosos s'exclouen o es
marquen amb el motiu; els splits s'agrupen per entrevista o parlant.

## Etapes

1. Revisar cada branca i article de `docs/temes/`. Anotar unitats de coneixement,
   buits, conflictes i relacions abans de redactar converses.
2. Redactar converses a partir d'intencions humanes, contrastar-les amb les
   fonts i afegir-les només quan passin la guia editorial. Després de cada
   conversa aprovada: validar-la, fer un commit específic i pujar-lo a `main`.
3. Tancar cada branca amb una auditoria de cobertura; tornar als articles si
   queda cap unitat útil sense conversa ni justificació.
4. Revisar una per una totes les peces elegibles de `docs/parla/`, preservar
   intervencions humanes autèntiques i documentar inclusions i exclusions.
5. Deduplicar i dividir train/validation/test sense barrejar fragments de la
   mateixa entrevista entre splits.
6. Validar JSONL, procedència, drets, cobertura i qualitat dels exports.

Els exports només es consideren complets quan tots els temes i totes les peces
de llengua elegibles tenen un estat auditable i els informes mostren la
cobertura final.
