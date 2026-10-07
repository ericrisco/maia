# Maia Knowledge

Dataset de converses basades en `docs/temes/`. L'objectiu és respondre dubtes
plausibles sobre Andorra amb precisió i naturalitat. No és una conversió de
fitxes a preguntes.

- [`review/EXEMPLES.md`](review/EXEMPLES.md): criteri editorial i mostres de
  calibratge. No són plantilles per generar registres mecànicament.
- `review/conversations.jsonl`: converses revisades que alimentaran els
  exports.
- `review/`: converses candidates/aprovades i fitxers de procedència separats.
- `work/`: inventari de continguts rellevants i estat de revisió.
- `output/`: splits finals, quan existeixin.
- `reports/`: cobertura, qualitat i decisions d'exclusió.

Per reconstruir l'inventari i el report de cobertura des de `docs/temes/`,
executa `python3 training-data/knowledge/scripts/build_document_inventory.py`.

Format exportat: una conversa JSON per línia amb `messages` i només els rols
`user` i `assistant`.
