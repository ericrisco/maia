# Knowledge inventory script

`build_inventory.py` recorre `docs/`, extrae un ledger auditable de cada bloque Markdown en `docs/temes/` y genera `knowledge/work/coverage.csv` con una fila por documento. Los JSONL internos guardan las unidades, enlaces, fichas de fuente, errores y exclusiones.

Desde la raíz del proyecto, ejecútalo con:

```bash
python3 training-data/knowledge/scripts/build_inventory.py
```

El ledger sirve para rastrear cobertura; no es el dataset de entrenamiento. Los registros de conversación y las decisiones de revisión se mantienen separados.
