# Maia Training Data

Projecte per preparar dos datasets de fine-tuning separats a partir de
`docs/`: **Knowledge** ensenya informació documentada sobre Andorra;
**Language** preserva català andorrà contemporani de parlants reals.

La primera feina és calibrar què compta com una conversa bona. Cada conversa
aprovada tindrà procedència, font i estat de drets registrats. Segons el
contracte del corpus, un estat `no` o `pendent` genera un avís i no bloqueja
per si sol la inclusió: l'autorització final correspon al propietari del
projecte. Encara no es generen exports finals fins que hi hagi volum revisat i
splits sense fuga.

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

Vegeu [el pla de treball](PLAN.md), [els exemples de Knowledge](knowledge/review/EXEMPLES.md)
i [la guia per escriure'ls](knowledge/review/CONVERSATION-GUIDE.md).
