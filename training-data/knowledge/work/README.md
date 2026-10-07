# Treball i cobertura de Knowledge

Inventari per tema i article, amb unitats de coneixement rellevants, converses
que les cobreixen i motius per no generar una pregunta quan no n'hi ha cap de
natural. El nombre d'articles o de registres no substitueix la revisió de
cobertura.

`document-inventory.json` es regenera amb
`python3 training-data/knowledge/scripts/build_document_inventory.py`; el
resum humà queda a `../reports/coverage-summary.md`. Cada conversa es relaciona
amb les seves fonts mitjançant `review/provenance.jsonl`.

No convertir cada paràgraf, fila o dada en una pregunta. Una mateixa conversa
pot cobrir fets relacionats; una fitxa pot requerir diverses converses si hi ha
dubtes diferents.
