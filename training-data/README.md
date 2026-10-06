# Maia Training Data

Àrea de treball per preparar dos conjunts separats a partir de `docs/`:

- **Knowledge** ensenya a respondre preguntes reals sobre Andorra amb informació documentada.
- **Language** conserva català andorrà contemporani produït per persones.

La regla editorial central és simple: cada conversa ha de sonar com una interacció que podria passar entre una persona curiosa i un assistent útil. No convertim títols, seccions o paràgrafs en preguntes automàtiques.

## Estructura

- `knowledge/review/`: converses candidates per revisar i fitxer de procedència.
- `knowledge/output/`: futurs `train.jsonl`, `validation.jsonl` i `test.jsonl`; no s'hi exporta res fins que passi la revisió i els drets.
- `knowledge/reports/`: cobertura i controls editorials.
- `language/review/`: fragments i converses candidates extrets de parla elegible.
- `language/output/`: futurs splits de Language.
- `language/reports/`: elegibilitat, exclusions i cobertura de Language.
- `PLAN.md`: procés de creació, criteris i pròxims passos.

Cada línia JSONL és una conversa amb missatges alternats `user` i `assistant`. Les notes de revisió i la procedència van en fitxers separats, mai dins dels missatges d'entrenament.

Els exemples actuals són un pilot editorial. No són aprovació de drets ni dades llestes per entrenar.
