# Maia Training Data

Aquest espai prepararà dos materials diferents:

- **Knowledge**: respostes útils sobre Andorra, basades en `maia/docs/temes/`.
- **Language**: català andorrà contemporani extret de parla humana a `maia/docs/parla/`.

No barregem els dos objectius. Les converses Knowledge són exemples de coneixement; Language no inventa ni reescriu veus humanes.

## Punt de partida

El pla de [Knowledge](PLAN.md) comença amb cinc converses de calibratge a `knowledge/review/calibration.jsonl`. Serveixen per revisar el to i el format abans d'ampliar el conjunt. Les fonts i les afirmacions verificables són a `knowledge/review/calibration-provenance.jsonl`. No s'exporten automàticament.

Les converses que ja formen part del conjunt de revisió són a `knowledge/review/conversations.jsonl`; la seva procedència és a `knowledge/review/provenance.jsonl`. Encara no hi ha exportacions ni un dataset complet.

Quan l'estil estigui validat, ampliarem el dataset tema per tema i revisarem la cobertura abans de generar cap partició d'entrenament.
