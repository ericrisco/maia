# Maia Training Data

Àrea per preparar dos datasets independents a partir de `docs/`.

- `knowledge/` prepara respostes sobre Andorra a partir de `docs/temes/`.
- `language/` conserva català andorrà contemporani de parla humana elegible a `docs/parla/`.

No barregem els objectius. A Knowledge, cada registre de revisió guarda la conversa i la seva procedència en una sola línia de `knowledge/review/records.jsonl`. Les mostres de calibratge ajuden a fixar la qualitat, però no són entrenables. Les sortides entrenables es guardaran a `output/` quan hi hagi registres aprovats suficients.

El pla de treball és a [`PLAN.md`](PLAN.md). La guia d'estil i els exemples són a [`knowledge/review/EXEMPLES.md`](knowledge/review/EXEMPLES.md).
