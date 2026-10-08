# Maia Training Data

Àrea de treball per preparar dos conjunts separats a partir del corpus actual:

- **Maia Knowledge**: converses en català que responen dubtes reals sobre Andorra amb fonts de `docs/temes/`.
- **Maia Language**: mostra de català andorrà contemporani autèntic a partir de `docs/parla/`, sense imitar ni inventar veus.

Les converses de Knowledge han de sonar com una petició d'ajuda normal. No poden parlar de seccions, files o fitxes. Consulta [PLAN.md](PLAN.md) i els quatre [exemples de calibratge](knowledge/examples/README.md) abans de crear registres.

## Estructura

- `knowledge/examples/`: calibratge; exclòs de l'entrenament.
- `knowledge/review/`: cua activa de candidats sense aprovar.
- `knowledge/archive/`: esborranys antics, conservats però fora del flux actiu.
- `knowledge/work/`: inventari, procedència i cobertura interna.
- `knowledge/reports/`: qualitat, cobertura i exclusions.
- `knowledge/output/`: exports aprovats; buit fins que hi hagi dades revisades i drets resolts.
- `language/`: inventari i procés separat per a parla autèntica.

Els candidats antics que hi havia a `knowledge/review/` s'han arxivat per tornar a començar la calibració. No són registres aprovats ni evidència de cobertura actual.
