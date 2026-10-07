# Maia Training Data

Projecte per preparar dos datasets de fine-tuning separats a partir de
`docs/`: **Knowledge** ensenya informació documentada sobre Andorra;
**Language** preserva català andorrà contemporani de parlants reals.

La primera feina és calibrar què compta com una conversa bona. Els exemples
actuals són editorials: no són aprovats per entrenar fins que se'n resolgui
l'estat de drets. Encara no es generen exports massius ni s'omplen els
directoris `output/`.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── examples.jsonl       # mostres editorials, només missatges
│   ├── review/              # converses aprovades i procedència
│   ├── work/                # inventari i seguiment de cobertura
│   ├── output/              # exports quan hi hagi prou material revisat
│   └── reports/             # cobertura, qualitat i exclusions
└── language/
    ├── review/              # fragments/converses reals i permisos
    ├── work/                # elegibilitat i verificació de transcripcions
    ├── output/              # exports de llengua aprovats
    └── reports/             # inclusió, exclusions i qualitat
```

Vegeu [el pla de treball](PLAN.md), [les mostres de Knowledge](knowledge/examples.jsonl)
i [la guia per escriure-les](knowledge/review/CONVERSATION-GUIDE.md).
