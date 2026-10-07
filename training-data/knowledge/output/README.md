# Maia Knowledge: sortides

`train.jsonl`, `validation.jsonl` i `test.jsonl` contenen només converses
aprovades, una per línia i amb el camp `messages`. Ara són buits: el lot
anterior no compleix encara el criteri editorial nou i és a
`../archive/previous-batch-2026-10/`. No s'ha d'entrenar amb aquell arxiu ni
amb candidats sense aprovar.

Quan hi hagi registres aprovats, es regeneren amb:

```bash
python3 training-data/knowledge/scripts/export_approved.py
```
