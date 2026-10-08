# Maia Training Data

Aquest espai prepara dos conjunts separats a partir de `docs/`.

- **Knowledge** ensenya a respondre dubtes sobre Andorra amb informació documentada.
- **Language** conserva trets del català andorrà contemporani a partir de parla humana autèntica i autoritzada.

`knowledge/review/conversations.jsonl` combina mostres editorials i converses revisades; `knowledge/review/provenance.jsonl` n'indica l'estat. Encara no és una exportació per entrenar: `output/` continuarà buit fins que la cobertura del corpus, els drets, la deduplicació i els splits estiguin revisats.

El criteri de naturalitat és a [`knowledge/review/EXEMPLES.md`](knowledge/review/EXEMPLES.md). Vegeu [`PLAN.md`](PLAN.md) per al mètode i les fases.
