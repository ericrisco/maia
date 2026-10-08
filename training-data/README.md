# Maia Training Data

Aquest espai prepara dos conjunts diferents a partir de `docs/`:

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb informació documentada.
- **Language** conserva trets del català andorrà contemporani a partir de parla humana autoritzada.

No barregem els objectius. Les mostres editorials no són registres d'entrenament. Els fitxers `output/` només contindran exportacions revisades i aprovades.

## Estat

Ara fixem el to amb tres converses de mostra a `knowledge/review/examples.jsonl`. Encara no hi ha cap registre aprovat per exportar. El pla és a [`PLAN.md`](PLAN.md).

## Estructura

- `knowledge/review/`: converses candidates, mostres i evidència de revisió.
- `knowledge/work/`: inventaris i intermedis regenerables.
- `knowledge/reports/`: cobertura, qualitat i decisions pendents.
- `knowledge/output/`: train, validation i test quan estiguin aprovats.
- `language/`: flux independent per a material lingüístic autèntic i amb drets verificats.
