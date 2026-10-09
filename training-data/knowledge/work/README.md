# Treball intern de Knowledge

`build_inventory.py` crea aquí un ledger de cada document de `docs/temes/`, amb metadades, unitats Markdown, enllaços i estat de procedència. `coverage.csv` té una fila per document; cada unitat ha d'acabar representada en una conversa o amb una exclusió raonada. Les converses públiques es mantenen a `review/`, no en aquest ledger.

Per regenerar-lo, executa `python3 training-data/knowledge/scripts/build_inventory.py` des de l'arrel del repositori. Els fitxers interns són evidència de cobertura, no són exportacions entrenables.
