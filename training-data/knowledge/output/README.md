# Exports de Knowledge

`train.jsonl`, `validation.jsonl` i `test.jsonl` encara no s'han generat. Les converses de `review/` són candidats, no registres aprovats, i un estat de drets `exportable: true` no substitueix la revisió de naturalitat i exactitud.

Segons el pla, l'exportació es farà quan s'hagi revisat la cobertura de `docs/temes/`, resolt els drets de cada conversa inclosa, deduplicat els exemples i agrupat les converses relacionades abans de crear els splits. La procedència i les decisions de revisió es conservaran fora dels fitxers de missatges destinats al fine-tuning.
