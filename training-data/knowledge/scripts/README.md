# Eines de Knowledge

`build_knowledge_inventory.py` recorre tots els Markdown de `docs/temes/` i conserva títols, descripcions, seccions, paràgrafs, llistes, cites, blocs de codi i files de taules com a unitats separades.

```bash
python3 training-data/knowledge/scripts/build_knowledge_inventory.py --check
python3 training-data/knowledge/scripts/build_knowledge_inventory.py
```

`--check` comprova el frontmatter i que no hi hagi identificadors d'unitat duplicats. Sense `--check`, escriu l'inventari regenerable a `work/document-units.jsonl` i el resum a `reports/inventory-summary.md`. Les unitats encara s'han de revisar i mapar a converses; l'inventari no declara cobertura per si sol.

Per validar el lector amb fixtures de Markdown:

```bash
python3 -m unittest discover -s training-data/knowledge/scripts/tests
```
