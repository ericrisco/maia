# Maia Training Data

Àrea de treball per preparar dades de fine-tuning sobre Andorra. El dataset
comença buit. Les mostres de `knowledge/review/calibration.jsonl` només serveixen
per acordar el to i el fil conversacional; no són dades aprovades ni exportables.

## Dues línies separades

- `knowledge/` transforma fets de `docs/temes/` en respostes conversacionals.
- `language/` conserva llengua humana real de `docs/parla/`, amb drets i
  transcripcions revisats. No s'inventen torns per convertir monòlegs en xats.

Llegiu primer el [pla](PLAN.md). No s'afegeixen més registres fins que els
exemples de calibratge tinguin el to desitjat.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── review/       # exemples de calibratge i procedència
│   ├── work/         # inventaris de cobertura futurs
│   ├── output/       # buit fins a l'aprovació
│   └── reports/      # buit fins que hi hagi mètriques
└── language/
    ├── work/         # inventari i verificació de parla
    ├── output/       # buit fins que hi hagi mostres autoritzades
    └── reports/      # elegibilitat, exclusions i qualitat
```
