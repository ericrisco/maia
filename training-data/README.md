# Maia Training Data

Aquesta carpeta separa dos objectius:

- **Knowledge**: respondre preguntes sobre Andorra amb fets documentats.
- **Language**: conservar català andorrà contemporani a partir de parla humana elegible.

No es barregen els dos conjunts. Les converses d'exemple serveixen per calibrar la qualitat; no són dades d'entrenament. No es genera cap export fins que els registres s'hagin revisat.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── examples/   # converses de calibratge i procedència; excloses dels exports
│   ├── review/     # converses candidates, procedència i decisions
│   ├── work/       # inventari i estat de cobertura regenerables
│   ├── reports/    # cobertura, exclusions i qualitat
│   ├── scripts/    # validació i generació
│   └── output/     # exports aprovats
└── language/
    ├── review/     # fragments humans candidats i procedència
    ├── work/       # elegibilitat, verificació i splits
    ├── reports/    # volum i exclusions
    └── output/     # material humà revisat
```

Les converses de `knowledge/examples/` mostren el to i el tipus de seguiment esperats. A `language/` no s'inventen exemples de parla: només s'hi incorporarà material humà elegible i verificat.

- [Pla general](PLAN.md)
- [Maia Knowledge](knowledge/README.md)
- [Maia Language](language/README.md)
