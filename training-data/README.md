# Maia Training Data

Àrea de treball dels datasets de Maia. Separa dos objectius: `knowledge`
ensenya coneixement documentat sobre Andorra; `language` preserva català
andorrà contemporani produït per persones.

Llegeix el [pla](PLAN.md) i la [guia de converses](knowledge/review/CONVERSATION-GUIDE.md)
abans de revisar o afegir registres. La cobertura continua incompleta; els
informes mostren l'estat real i no indiquen que el dataset estigui acabat.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── review/       # converses candidates, exemples i procedència
│   ├── work/         # inventari i seguiment de cobertura
│   ├── output/       # exportacions train, validation i test
│   └── reports/      # cobertura i resum d'exportació
└── language/
    ├── work/         # inventari i verificació de parla
    ├── output/       # registres de llengua aprovats
    └── reports/      # elegibilitat, exclusions i qualitat
```

`knowledge` i `language` no es barregen. Les exportacions contenen només
missatges de conversa; la procedència i els drets es conserven en els registres
interns.
