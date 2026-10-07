# Maia Knowledge

Converses que responen preguntes sobre Andorra a partir de `docs/temes/`.

- `review/EXEMPLES.md` calibra l'estil; no és part del dataset.
- `review/conversations.jsonl` rebrà candidats actius, una conversa JSONL per línia.
- `review/provenance.jsonl` guardarà les fonts i els drets, una entrada per candidat.
- `work/` recollirà inventari i cobertura després de començar la revisió exhaustiva.
- `scripts/` i `reports/` s'ompliran quan hi hagi un procés de revisió i dades suficients.
- `output/` es mantindrà buit fins que els registres estiguin revisats i aprovats.

Les preguntes han de néixer d'una intenció humana. Els seguiments han d'enllaçar amb la resposta anterior. Vegeu [`review/CONVERSATION-GUIDE.md`](review/CONVERSATION-GUIDE.md).
