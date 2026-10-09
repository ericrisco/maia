# Scripts de Maia Knowledge

`build_inventory.py` recorre `docs/` y vuelve a generar el ledger de evidencias, las fichas de fuente, las relaciones internas y el CSV de cobertura.

Desde el repositorio `maia/`, ejecútalo así:

```bash
python3 training-data/knowledge/scripts/build_inventory.py
```

El script no redacta preguntas ni respuestas. Lee las conversaciones activas de `review/` para atribuir cobertura a sus evidencias. No reactiva conversaciones archivadas.

Los artefactos generados quedan en `knowledge/work/` y `knowledge/reports/`. Comprueba los contadores y los problemas de procedencia antes de crear registros nuevos.
