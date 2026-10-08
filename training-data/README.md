# Maia Training Data

Aquesta carpeta prepara dos conjunts separats per al fine-tuning de Maia:

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb informació documentada.
- **Language** conserva la manera de parlar en català andorrà a partir de mostres humanes reals.

La carpeta s'ha reiniciat per corregir el criteri de les preguntes. Els exemples actuals són només una guia d'estil. No són registres aprovats ni formen part dels fitxers d'entrenament.

## Estat actual

- `knowledge/examples/`: cinc converses de calibratge amb procedència separada.
- `knowledge/review/`: buit; aquí es proposaran i revisaran registres nous.
- `knowledge/output/`: encara no conté datasets finals.
- `language/`: estructura preparada; encara no conté registres.

No s'han creat fitxers `train.jsonl`, `validation.jsonl` ni `test.jsonl`. Aquests es generaran quan hi hagi prou registres revisats i es puguin separar sense filtracions entre splits.

Consulta [`PLAN.md`](PLAN.md) abans de proposar converses noves.
