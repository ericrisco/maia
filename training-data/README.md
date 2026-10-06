# Maia Training Data

Aquest directori prepara dos conjunts separats per entrenar i avaluar Maia.

- `knowledge/` conté converses redactades a partir de fets documentats a `docs/temes/`.
- `language/` conserva llengua humana real de `docs/parla/`. No s'hi inventen converses.

Els registres de `review/` són candidats editorials pendents de revisió. No són sortides d'entrenament. Només els registres acceptats, amb procedència i drets compatibles amb l'ús previst, poden passar a `output/`.

Comença per [PLAN.md](PLAN.md). Knowledge i Language tenen mètodes diferents i no es barregen.
