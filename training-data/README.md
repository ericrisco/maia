# Maia Training Data

Aquí preparem dos conjunts separats a partir de `docs/`.

- **Knowledge** ensenya a respondre dubtes documentats sobre Andorra.
- **Language** conserva trets de parla humana andorrana contemporània.

`knowledge/review/conversations.jsonl` conté mostres editorials i converses revisades. Les mostres no són dades d'entrenament; cada conversa revisada ha de tenir fonts i drets aptes registrats. `output/` continua buit mentre es construeixen la cobertura i els splits. La procedència de cada registre és a `knowledge/review/provenance.jsonl`.

Abans d'afegir registres nous, llegiu [`PLAN.md`](PLAN.md) i la guia [`knowledge/review/EXEMPLES.md`](knowledge/review/EXEMPLES.md). La regla clau: la pregunta ha de sonar com un dubte que una persona faria sense tenir una fitxa al davant; el seguiment ha de néixer de la resposta.
