# Maia Training Data

Aquesta àrea prepara dos conjunts separats:

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb fets traçables a `docs/temes/`.
- **Language** conserva formes reals del català andorrà a partir de material humà elegible de `docs/parla/`.

No es barregen. Les converses de calibratge són exemples editorials: no entrenen el model i no compten per a cobertura. Comença per [PLAN.md](PLAN.md). La guia i els registres de calibratge són a `knowledge/review/`.

L'export encara no està creat: els fitxers de `output/` són instruccions, no datasets. `knowledge/review/conversations.jsonl` conté registres en revisió i no s'ha d'entrenar directament. `knowledge/review/calibration.jsonl` conté tres exemples per revisar la naturalitat de les preguntes, la continuïtat dels seguiments i la qualitat de les respostes.
