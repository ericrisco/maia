# Maia Training Data

Preparació de dades de fine-tuning en dues branques separades:

- `knowledge/` ensenya fets sobre Andorra a partir de `docs/temes/`.
- `language/` conserva català andorrà humà i verificable de `docs/parla/`.

El [pla](PLAN.md) fixa com escriure converses que una persona preguntaria de
debò. Els exemples de Knowledge són candidats de calibratge; les sortides
`output/` només s'omplen quan una conversa ha passat la revisió factual,
editorial i de drets. Cobrir tots els temes vol dir auditar-los, no fabricar una
pregunta per cada paràgraf.
