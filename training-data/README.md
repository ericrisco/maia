# Maia Training Data

Àrea de treball dels dos datasets de Maia: `knowledge` ensenya coneixement
documentat sobre Andorra; `language` preserva català andorrà contemporani
produït per persones. El [pla actiu](PLAN.md) exigeix cobertura completa i
revisió tema per tema.

## Estructura

```text
training-data/
├── PLAN.md
├── RESTART-PLAN.md
├── knowledge/
│   ├── starter/       # quatre exemples per calibrar el to
│   ├── review/        # converses aprovades i procedència
│   ├── work/          # inventari i seguiment de cobertura
│   ├── output/        # exports train, validation i test
│   └── reports/       # cobertura i resum d'exportació
└── language/
    ├── starter/       # política del pilot, separat de Knowledge
    ├── work/          # elegibilitat i verificació de la parla
    ├── output/        # material lingüístic aprovat
    └── reports/       # inclusions, exclusions i qualitat
```

Cada conversa revisada té una entrada de procedència. Les exportacions de
fine-tuning contenen només `messages`; els drets, els identificadors i els
estats editorials queden als registres interns. Vegeu
[`knowledge/review/CONVERSATION-GUIDE.md`](knowledge/review/CONVERSATION-GUIDE.md)
i [`knowledge/review/EXEMPLES.md`](knowledge/review/EXEMPLES.md).
