# Maia Knowledge

Conversa natural sobre el coneixement d'Andorra documentat a `docs/temes/`.
Les preguntes no fan referència a fitxes, apartats o files: parteixen d'un dubte
que una persona podria tenir sobre el tema.

## Fitxers

- `review/conversations.jsonl`: converses pilot per revisar; encara no són dades
  aprovades per entrenar.
- `review/EXEMPLES.md`: convencions i exemples d'edició de preguntes naturals.
- `review/provenance.jsonl`: font, evidència i estat de drets de cada exemple.
- `review/quality-rubric.md`: criteris per acceptar, reescriure o descartar.
- `output/`: buit fins que hi hagi registres aprovats i exportables.

El JSONL de cada conversa només conté `messages`. No hi afegim IDs, cites,
notes internes ni estats de revisió.
