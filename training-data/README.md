# Maia Training Data

Aquesta carpeta conté dos fluxos separats per preparar dades de fine-tuning.

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb informació del corpus.
- **Language** conserva català andorrà contemporani produït per persones.

Ara només hi ha una estructura inicial i tres converses de calibratge a `knowledge/review/calibration.jsonl`. Serveixen per revisar el criteri. No són exports d'entrenament.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── review/       # guia i converses de calibratge o revisió
│   ├── work/         # inventari i decisions de cobertura
│   ├── reports/      # cobertura, qualitat i exclusions
│   └── output/       # train/validation/test quan estiguin aprovats
└── language/
    ├── review/       # fragments humans i procedència
    ├── work/         # elegibilitat, verificació i agrupació
    ├── reports/      # peces incloses i exclusions
    └── output/       # exports quan estiguin preparats
```

No es creen fitxers d'export buits. Cada export apareixerà quan contingui registres revisats.
