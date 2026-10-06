# Maia Knowledge

Conversa natural sobre el coneixement d'Andorra documentat a `docs/temes/`.
Les preguntes no fan referència a fitxes, apartats o files: parteixen d'un dubte
que una persona podria tenir sobre el tema.

El baseline processa totes les 1.477 fitxes temàtiques. El recompte de 87.339
unitats és un inventari estructural exhaustiu per auditar; encara falta
classificar-les en converses, exclusions justificades o dubtes de font.

## Fitxers

- `review/conversations.jsonl`: converses pilot per revisar; encara no són dades
  aprovades per entrenar.
- `review/EXEMPLES.md`: convencions i exemples d'edició de preguntes naturals.
- `review/provenance.jsonl`: font, evidència i estat de drets de cada exemple.
- `review/quality-rubric.md`: criteris per acceptar, reescriure o descartar.
- `output/`: buit fins que hi hagi registres aprovats i exportables.
- `reports/inventory.json`: mètriques de lectura del corpus temàtic.
- `work/`: ledgers detallats regenerables; Git els ignora.

El JSONL de cada conversa només conté `messages`. No hi afegim IDs, cites,
notes internes ni estats de revisió.
