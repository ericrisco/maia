# Maia Training Data

Projecte per preparar dos datasets de fine-tuning separats a partir de
`docs/`: **Knowledge** ensenya informació documentada sobre Andorra;
**Language** preserva català andorrà contemporani de parlants reals.

La primera feina és calibrar què compta com una conversa bona. Les mostres
editorials són a `knowledge/review/EXEMPLES.md`; no són registres d'entrenament.
Els JSONL actius només s'ompliran amb converses aprovades, una per una, amb
procedència i estat de drets registrats. Encara no es generen exports finals.

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
