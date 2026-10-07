# Maia Training Data

Àrea de treball dels datasets de Maia. Separa dos objectius: `knowledge`
ensenya coneixement documentat sobre Andorra; `language` preserva català
andorrà contemporani produït per persones.

El mètode s’està reiniciant a partir del [pla nou](RESTART-PLAN.md). El pilot
de converses està a `knowledge/starter/`; les dades anteriors resten congelades
fins que el criteri nou s’hagi revisat. La cobertura continua incompleta; els
informes mostren l'estat real i no indiquen que el dataset estigui acabat.

## Estructura

```text
training-data/
├── PLAN.md                 # entrada estable al pla vigent
├── RESTART-PLAN.md         # procés editorial del reinici
├── knowledge/
│   ├── starter/            # quatre converses pilot i procedència
│   ├── review/             # corpus anterior, congelat durant el pilot
│   ├── work/               # inventari i seguiment de cobertura
│   ├── output/             # exportació anterior, no aprovada pel pilot
│   └── reports/            # informes anteriors
└── language/
    ├── starter/            # buit fins que hi hagi material verificat
    ├── work/               # inventari i verificació de parla
    ├── output/             # material lingüístic aprovat
    └── reports/            # elegibilitat, exclusions i qualitat
```

`knowledge` i `language` no es barregen. El fitxer `knowledge/output/` és una
exportació anterior i no s’ha de tractar com a resultat aprovat del pilot. Les exportacions contenen només
missatges de conversa; la procedència i els drets es conserven en els registres
interns.
