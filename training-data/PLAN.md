# Pla: converses que faria una persona

## Problema observat

Les preguntes que es refereixen a «aquesta secció», «la fitxa» o «aquesta fila» només tenen sentit si l'usuari ja està llegint el corpus. Les respostes fragmentàries tampoc resolen el dubte. Això ensenya a contestar qüestionaris sobre documents, no a ajudar una persona.

## Principi editorial

Escriu cada conversa com si comencés en un xat nou. Parteix d'una curiositat, una confusió o una necessitat real. La persona no coneix els títols ni l'estructura interna de Maia.

La primera resposta ha de resoldre el dubte principal. El seguiment ha de néixer del que s'acaba de dir i demanar una cosa nova. No hi ha una llargada fixa: cada missatge ha de tenir una funció. Una conversa amb seguiments artificials no s'aprova.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── review/
│   │   ├── CRITERIS.md
│   │   ├── EXEMPLES.md
│   │   ├── conversations.jsonl
│   │   └── provenance.jsonl
│   ├── work/coverage.csv
│   ├── reports/
│   ├── scripts/
│   └── output/                 # buit fins a l'aprovació
└── language/
    ├── README.md
    ├── work/
    ├── reports/
    ├── scripts/
    └── output/                 # només text humà elegible
```

## Procés per a cada conversa

1. Tria una idea útil d'una o més fitxes i comprova el context complet.
2. Escriu la pregunta sense copiar el títol, els subtítols o les etiquetes de la font.
3. Respon de manera directa, completa i natural. No afegeixis dades per fer la resposta més lluïda.
4. Continua el fil només si algú, després d'aquesta resposta, preguntaria de debò una altra cosa.
5. Revisa cada afirmació contra les fonts i registra els fitxers d'origen i l'estat dels drets a `provenance.jsonl`.
6. Llegeix només la conversa. Si sona a examen o no s'entén sense la font, reescriu-la.
7. Marca cobertura i revisió. No exportis candidats pendents.

## Etapes

1. Acordar el criteri editorial amb les mostres de `knowledge/review/`.
2. Revisar les converses antigues contra aquest criteri; descartar les que sonin a preguntes de corpus.
3. Cobrir `docs/temes/` tema a tema, amb varietat d'intencions i converses que necessitin més d'una font quan sigui natural.
4. Revisar exactitud, naturalitat, incertesa, duplicats, cobertura i drets.
5. Treballar `language/` de manera separada. Usar només fragments humans elegibles segons `docs/CONTRACT.md`.
6. Preparar exports i splits després de l'aprovació, agrupant per tema o font per evitar filtracions entre particions.

Cada pas funcional es revisa i valida abans d'un commit petit. Es fa push abans de començar el pas següent. No s'inclouen dades personals ni fitxers de `docs/` en aquests commits.

## Regla d'exportació

Els missatges exportats només contenen la conversa. IDs, rutes, notes editorials, evidència, llicències i estats de revisió queden als fitxers de treball. Cap registre s'exporta amb drets pendents o contingut no revisat.
