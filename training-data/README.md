# Maia Training Data

Aquesta carpeta prepara dos datasets separats a partir de `docs/`.

- **Knowledge**: converses que ensenyen el coneixement andorrà del corpus.
- **Language**: parla andorrana contemporània autèntica, produïda per persones.

`knowledge/review/conversations.jsonl` ja conté tres converses aprovades. Encara no són els exports `train`, `validation` i `test`: abans cal completar cobertura, deduplicació i splits.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── review/       # converses i procedència
│   ├── work/         # inventari i estat de cobertura
│   ├── reports/      # cobertura, qualitat i exclusions
│   ├── scripts/      # inventari i validació
│   └── output/       # exports després de la revisió
└── language/
    ├── review/       # fragments humans i procedència
    ├── work/         # elegibilitat i verificació
    ├── reports/      # peces incloses i exclusions
    └── output/       # exports després de la revisió
```

No es creen fitxers d'export buits.
