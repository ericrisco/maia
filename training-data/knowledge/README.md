# Maia Knowledge

Aquest dataset ensenyarà coneixement sobre Andorra a partir de `maia/docs/temes/`. Les converses revisades i la seva procedència es guarden separadament a `review/`.

- `review/conversations.jsonl`: una conversa per línia, només missatges `user` i `assistant`.
- `review/provenance.jsonl`: fonts i afirmacions que permeten verificar cada conversa.
- `work/`: espai per a inventaris temporals mentre ampliem la cobertura.
- `reports/`: informes de revisió i cobertura.

Les tres converses inicials són una tanda de calibratge. No són una exportació final ni representen cobertura exhaustiva.

`work/coverage.csv` és el registre exhaustiu dels fitxers de `docs/temes/`. Cada fila ha de quedar coberta per converses o exclosa amb motiu abans de declarar complet el dataset. `review/EXEMPLES.md` defineix el to i inclou un contraexemple que cal rebutjar.
