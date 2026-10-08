# Maia Knowledge

Ensenya fets, context i relacions sobre Andorra que estiguin documentats a `docs/temes/`. No ensenya la llengua parlada; aquesta és la feina separada de Maia Language.

- `examples/conversations.jsonl`: mostres per acordar naturalitat, context i seguiments. Són només de calibratge.
- `examples/provenance.jsonl`: fitxes del corpus que sostenen cada mostra i estat de revisió dels drets.
- `review/conversations.jsonl`: registres nous pendents de validació, una conversa per línia.
- `work/coverage.csv`: inventari de tots els documents de `docs/temes/` i estat de cobertura.
- `work/provenance.jsonl`: fonts, hashes i estat de drets per conversa. No forma part dels missatges entrenables.
- `output/`: converses aprovades, una per línia JSONL i només amb `messages`.
- `reports/`: cobertura, duplicats, exclusions i decisions de revisió.

Una dada només compta com a coberta quan apareix en una resposta útil i verificable, no pel fet d'haver generat una pregunta sobre el document.
