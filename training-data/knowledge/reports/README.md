# Informes de Maia Knowledge

- [`coverage.jsonl`](coverage.jsonl) inventaria cada fitxa i índex de `docs/temes/`, amb estructura detectada, converses revisades vinculades i estat `pending` o `partial`.
- [`coverage-summary.md`](coverage-summary.md) resumeix el volum per tema i les unitats estructurals detectades.

Regenera'ls des de l'arrel de Maia amb `python3 training-data/knowledge/scripts/build_coverage_report.py`.

`partial` només vol dir que hi ha alguna conversa revisada que cita la fitxa. No vol dir que el tema estigui cobert. Una fitxa només podrà passar a `complete` després de revisar tot el contingut útil: seccions, paràgrafs, llistes, taules i relacions. L'inventari actual encara no marca cap fitxa com a completa. Les mostres editorials no compten com a cobertura.
