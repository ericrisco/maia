# Inventari de Maia Knowledge

`coverage.csv` llista els 1.477 fitxers Markdown de `docs/temes/`, inclosos 129 índexs. L'estat de cobertura s'ha reiniciat: els registres de l'arxiu eren candidats sense aprovar i no compten com a coneixement representat al dataset.

`coverage-items.jsonl` conserva afirmacions de proves anteriors. Els ítems marcats `superseded` són històrics i no s'han de tractar com a cobertura activa. Després d'aprovar converses amb el criteri actual, actualitza afirmacions i `conversation_ids`.

La procedència es preomple a partir de les fonts declarades als documents quan hi ha una fitxa de font. Confirma cada atribució i condició de redistribució abans d'exportar.
