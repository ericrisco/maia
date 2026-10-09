# Eines d'inventari de Knowledge

`build_inventory.py` recorre el corpus de `docs/`, extreu unitats semàntiques i
relacions, i actualitza `work/`, `reports/` i el registre `coverage.csv`.
La cua de `review/` ha de contenir parelles de fitxers JSONL alineades; si encara
no hi ha candidats, tots dos fitxers poden ser buits.

Des de l'arrel del repositori Maia:

```bash
PYTHONPATH=src python3 training-data/knowledge/scripts/build_inventory.py
```

Els fitxers de `work/` i alguns reports són sortides generades. No s'editen a mà;
els canvis editorials van a les converses de revisió o als registres manuals de
decisions, i després es torna a executar el lector.
