# Maia Knowledge

Converses en català sobre Andorra, basades en `docs/temes/`. Cada registre
respon un dubte humà, conserva els límits de les fonts i passa els criteris de
[`CONVERSATION-GUIDE.md`](review/CONVERSATION-GUIDE.md).

- `review/conversations.jsonl`: converses revisades, una per línia.
- `review/provenance.jsonl`: fonts, drets i estat editorial de cada conversa.
- `work/document-inventory.json`: inventari de les fitxes del corpus.
- `work/document-status.json`: seguiment del que s'ha revisat per fitxa.
- `output/`: exportacions JSONL amb només `messages`.
- `reports/coverage-summary.md`: cobertura del corpus.
- `reports/export-summary.md`: registres exportats i distribució dels splits.

El [pla](../PLAN.md) defineix el procés. El dataset continua incomplet fins que
la cobertura i la qualitat hagin estat auditades per a totes les fitxes.
