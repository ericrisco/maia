# Maia Knowledge

Dataset de converses basades en `docs/temes/`. L'objectiu és respondre dubtes
plausibles sobre Andorra amb precisió i naturalitat. No és una conversió de
fitxes a preguntes.

- [`examples.jsonl`](examples.jsonl): mostres de calibratge; no són encara una
  autorització per generar-ne centenars amb plantilles.
- `review/`: converses candidates/aprovades i fitxers de procedència separats.
- `work/`: inventari de continguts rellevants i estat de revisió.
- `output/`: splits finals, quan existeixin.
- `reports/`: cobertura, qualitat i decisions d'exclusió.

Format exportat: una conversa JSON per línia amb `messages` i només els rols
`user` i `assistant`.
