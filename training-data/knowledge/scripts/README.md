# Eines de Maia Knowledge

## Inventari estructural del corpus

`build_knowledge_inventory.py` recorre totes les fitxes Markdown de `docs/temes/`, valida el YAML i crea:

- `work/documents.jsonl`: tipus, títol, tema, font, frontmatter i recompte d'unitats per document.
- `work/document-units.jsonl`: unitats estructurals amb text, línia, secció i enllaços interns.
- `reports/inventory-summary.md`: recomptes per tipus, tema i font.

Executar des de l'arrel de `maia/`:

```sh
python3 -m pip install -r training-data/knowledge/scripts/requirements.txt
python3 training-data/knowledge/scripts/build_knowledge_inventory.py --check
python3 training-data/knowledge/scripts/build_knowledge_inventory.py
python3 -m unittest discover -s training-data/knowledge/scripts/tests -v
```

`--check` valida frontmatter i identificadors sense escriure l'inventari. La generació només divideix el Markdown per estructures visibles; una unitat inventariada encara necessita revisió humana abans de donar-la per coberta.
