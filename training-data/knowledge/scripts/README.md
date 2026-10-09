# Scripts de Maia Knowledge

`build_inventory.py` reconstrueix l'inventari de `docs/`, les unitats d'evidència i el registre de cobertura a partir dels candidats actuals. Executa'l des de l'arrel de Maia amb:

```bash
PYTHONPATH=src python3 training-data/knowledge/scripts/build_inventory.py
```

El registre d'exclusions manuals només cobreix notes editorials i unitats no conversacionals justificades. No s'hi exclou cap dada factual per comoditat.
