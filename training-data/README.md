# Maia Training Data

Àrea de treball per preparar dos corpus diferents:

- **Maia Knowledge** ensenya coneixement documentat sobre Andorra.
- **Maia Language** conserva patrons de parla andorrana contemporània a partir de material humà elegible.

Els exemples de calibratge serveixen per acordar com sonen les converses. No són una mostra de volum ni un export d'entrenament. Cap registre passa a `output/` sense revisió de contingut, procedència i drets.

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── scripts/        # Automatització futura, encara sense pipeline
│   ├── examples/       # Mostres de calibratge i procedència
│   ├── review/         # Converses candidates, pendents de revisió
│   ├── work/           # Cobertura i anotacions internes
│   ├── output/         # Només exports aprovats
│   └── reports/        # Cobertura, exclusions i qualitat
└── language/
    ├── README.md
    ├── scripts/        # Automatització futura, encara sense pipeline
    ├── review/         # Fragments humans candidats
    ├── work/           # Elegibilitat, verificació i cobertura
    ├── output/         # Només exports aprovats
    └── reports/        # Peces incloses i excloses
```

Knowledge i Language no comparteixen exemples, fonts ni exports. Ara el projecte només prepara l'estructura i calibra Knowledge; els registres nous es faran després de revisar les mostres.
