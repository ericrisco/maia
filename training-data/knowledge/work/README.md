# Inventari de Maia Knowledge

`coverage.csv` llista els 1.477 fitxers Markdown de `docs/temes/`, inclosos 129 índexs. `pending` vol dir que encara no s'ha treballat el document; `partial` indica que hi ha candidats en revisió, no cobertura aprovada; `complete` només s'usa quan les afirmacions útils estan representades en converses aprovades; `navigation_only` marca índexs sense coneixement propi per convertir en conversa.

`coverage-items.jsonl` conserva afirmacions de proves anteriors i de candidats actuals. Els ítems marcats `superseded` són històrics; els marcats `candidate` encara no compten com a cobertura aprovada. Després d'aprovar converses amb el criteri actual, actualitza afirmacions i `conversation_ids`.

La procedència es preomple a partir de les fonts declarades als documents quan hi ha una fitxa de font. Confirma cada atribució i condició de redistribució abans d'exportar.
