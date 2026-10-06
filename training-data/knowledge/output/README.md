# Maia Knowledge: sortides

`train.jsonl`, `validation.jsonl` i `test.jsonl` contenen només converses
aprovades, una per línia i amb el camp `messages`. Ara són buits perquè els
exemples de calibratge encara són candidats. No s'ha d'entrenar amb els
candidats.

Quan hi hagi registres aprovats, es regeneren amb:

```bash
python3 training-data/knowledge/scripts/export_approved.py
```
