# Maia Training Data

Projecte per preparar dos datasets de fine-tuning separats a partir de
`docs/`: **Knowledge** ensenya informació documentada sobre Andorra;
**Language** preserva català andorrà contemporani de parlants reals.

La feina actual és tornar a calibrar les preguntes de Knowledge: han de partir
d'un dubte humà i mantenir un fil natural entre torns. Les mostres editorials
són a `knowledge/review/EXEMPLES.md`; no són registres d'entrenament. El pilot
anterior s'ha retirat i la cobertura s'ha reiniciat. Language continua separat.
Encara no hi ha registres Knowledge nous aprovats ni exports finals.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── scripts/             # inventari i exportació
│   ├── review/              # exemples, converses aprovades i procedència
│   ├── work/                # inventari i seguiment de cobertura
│   ├── output/              # exports quan hi hagi prou material revisat
│   └── reports/             # cobertura, qualitat i exclusions
└── language/
    ├── review/              # fragments/converses reals i permisos
    ├── work/                # elegibilitat i verificació de transcripcions
    ├── output/              # exports de llengua aprovats
    └── reports/             # inclusió, exclusions i qualitat
```

Vegeu [el pla de treball](PLAN.md), [els exemples de calibratge](knowledge/review/EXEMPLES.md)
i [la guia editorial](knowledge/review/CONVERSATION-GUIDE.md).
