# Maia Training Data

Preparació de dos datasets independents des del corpus Maia. **Knowledge** transforma coneixement sobre Andorra en converses útils; **Language** conserva llengua humana contemporània quan la font, la transcripció i els drets ho permeten.

## Estructura

```text
training-data/
├── PLAN.md
├── scripts/                 # lectors i informes regenerables
├── knowledge/
│   ├── work/                # inventari intern i evidència
│   ├── reports/             # cobertura i qualitat
│   ├── review/              # pilots, procedència i rúbrica
│   └── output/              # només exportacions aprovades
└── language/
    ├── work/                # extraccions internes
    ├── reports/             # elegibilitat i incertesa
    ├── review/              # revisió de peces elegibles
    └── output/              # només exportacions aprovades
```

Els pilots no s’han d’entrenar directament. `review/conversations.jsonl` conté només missatges; la traçabilitat viu a `review/provenance.jsonl`. Els reports d’inventari són una base de cobertura, no una aprovació d’entrenament.

Vegeu [el pla](PLAN.md), [els exemples i anti-exemples](knowledge/review/EXEMPLES.md) i [la rúbrica](knowledge/review/quality-rubric.md).
