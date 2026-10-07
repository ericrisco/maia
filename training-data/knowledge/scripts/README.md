# Knowledge scripts

`build_knowledge_inventory.py` recorre tot `docs/temes/`, llegeix YAML i conserva blocs de text, llistes, cites, taules, codis, seccions i enllaços com a unitats amb ID estable. Genera l'inventari de treball i l'informe estructural. Aquest pas no declara les unitats cobertes ni autoritza entrenament.

```bash
python3 -m pip install -r maia/training-data/knowledge/scripts/requirements.txt
python3 maia/training-data/knowledge/scripts/build_knowledge_inventory.py --check
python3 -m unittest discover -s maia/training-data/knowledge/scripts/tests -v
```

La dependència actual és PyYAML. Les eines de validació de converses, drets, cobertura i exportació s'afegiran en etapes separades.
