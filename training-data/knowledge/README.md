# Maia Knowledge

Dataset de converses basades en `docs/temes/`. L'objectiu és respondre dubtes
que una persona faria de debò sobre Andorra. No és una conversió de fitxes a
preguntes ni un qüestionari per cobrir cada dada.

- [`review/EXEMPLES.md`](review/EXEMPLES.md): exemples de calibratge, fora del
  dataset actiu.
- `review/conversations.jsonl`: només converses aprovades; ara és buit fins que
  els exemples defineixin el to.
- `review/provenance.jsonl`: font i revisió editorial, fora de les converses.
- `work/`: inventari de continguts rellevants i estat de revisió.
- `output/`: splits finals, quan existeixin.
- `reports/`: cobertura, qualitat i decisions d'exclusió.

Per reconstruir l'inventari i el report de cobertura des de `docs/temes/`,
executa `python3 training-data/knowledge/scripts/build_document_inventory.py`.

Format exportat: una conversa JSON per línia amb `messages` i només els rols
`user` i `assistant`.
