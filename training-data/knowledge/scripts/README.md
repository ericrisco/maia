# Knowledge inventory script

`build_inventory.py` recorre `docs/`, extrae un ledger de cada bloque Markdown de `docs/temes/` y genera `knowledge/work/coverage.csv`, con una fila por documento. Los JSONL internos guardan las unidades, enlaces, fiches de font, errors i exclusions.

També llegeix `knowledge/review/conversations.jsonl` i `provenance.jsonl` per comptar unitats cobertes per candidates i registres aprovats. Una unitat no representada continua pendent; una pregunta candidata no compta com a cobertura aprovada.

Des de l'arrel del projecte:

```bash
python3 training-data/knowledge/scripts/build_inventory.py
```

El ledger serveix per rastrejar cobertura; no és el dataset de entrenamiento.
