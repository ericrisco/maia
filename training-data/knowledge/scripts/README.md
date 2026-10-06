# Scripts de Knowledge

`python3 training-data/knowledge/scripts/build_document_coverage.py` recorre les fitxes `type: article` de `docs/temes/` i encreua les seves rutes amb la procedència dels candidats.

- El detall per document i secció es desa a `knowledge/work/document-inventory.json` i no es versiona.
- El resum de recompte es desa a `knowledge/reports/coverage-summary.json`.
- Una cita a una fitxa només vol dir que algun candidat l'esmenta. No demostra que se n'hagin cobert tots els fets o totes les seccions.
