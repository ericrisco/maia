# Maia Training Data

Aquest espai prepararà dos materials diferents:

- **Knowledge**: respostes útils sobre Andorra, basades en `maia/docs/temes/`.
- **Language**: català andorrà contemporani extret de parla humana a `maia/docs/parla/`.

No barregem els dos objectius. Les converses Knowledge són exemples de coneixement; Language no inventa ni reescriu veus humanes.

## Punt de partida

El pla de [Knowledge](PLAN.md) comença amb una prova petita de tres converses. Encara no hi ha exportacions ni un dataset complet. Llegiu els missatges de `knowledge/review/conversations.jsonl` sense mirar les fitxes: han de semblar preguntes que algú faria de debò. La procedència de cada conversa és a `knowledge/review/provenance.jsonl`.

Quan l'estil estigui validat, ampliarem el dataset tema per tema i revisarem la cobertura abans de generar cap partició d'entrenament.
