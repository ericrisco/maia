# Maia Knowledge: dades exportades

Els fitxers `train.jsonl`, `validation.jsonl` i `test.jsonl` són sortides de
`scripts/export_approved.py`. Cada línia només conté `messages`; la procedència
i l'atribució són a `ATTRIBUTION.md` i `../review/provenance.jsonl`.

L'exportació actual és parcial. Els grups de fonts assignats a un split no es
reparteixen entre splits. Per regenerar-la, executa des de l'arrel de Maia:

```bash
python3 training-data/knowledge/scripts/export_approved.py
```

Els drets i les atribucions s'han de conservar segons `ATTRIBUTION.md`.
