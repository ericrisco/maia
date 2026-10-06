# Maia Training Data

Àrea de treball per preparar dos conjunts separats a partir de `docs/`:

- **Knowledge** ensenya a respondre preguntes reals sobre Andorra amb informació documentada.
- **Language** conserva català andorrà contemporani produït per persones.

Per a Knowledge, cada conversa ha de començar d'un dubte que algú podria tenir sense haver obert la font. No convertim títols, apartats, taules o paràgrafs en preguntes automàtiques. El criteri i les mostres són a `knowledge/review/EXEMPLES.md`.

## Estructura

- `knowledge/review/`: converses candidates, rúbrica editorial i procedència.
- `knowledge/review/quarantine/`: registres antics preservats, fora del lot actiu.
- `knowledge/output/`: futurs `train.jsonl`, `validation.jsonl` i `test.jsonl`; no s'hi exporta res fins que passi la revisió i els drets.
- `knowledge/reports/`: cobertura i controls editorials.
- `language/review/`: fragments i converses candidates extrets de parla elegible.
- `language/output/`: futurs splits de Language.
- `language/reports/`: elegibilitat, exclusions i cobertura de Language.
- `PLAN.md`: procés de creació, criteris i pròxims passos.

Cada línia JSONL és una conversa completa amb missatges alternats `user` i `assistant`. Les notes de revisió i la procedència van en fitxers separats, mai dins dels missatges d'entrenament.

`knowledge/review/conversations.jsonl` conté tres mostres editorials per acordar l'estàndard. No són aprovades ni llestes per entrenar. Les carpetes `output/` són deliberadament buides fins que hi hagi registres revisats i drets compatibles amb l'ús final.
