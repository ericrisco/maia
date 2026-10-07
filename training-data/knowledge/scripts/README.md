# Knowledge scripts

`build_knowledge_inventory.py` recorre tot `docs/temes/`, llegeix YAML i conserva blocs de text, llistes, cites, taules, codis, seccions i enllaços com a unitats amb ID estable. Genera l'inventari de treball i l'informe estructural. Aquest pas no declara les unitats cobertes ni autoritza entrenament.

`validate_knowledge_review.py` valida els diàlegs i la seva procedència, comprova que cada unitat citada existeix i recalcula l'estat de cobertura. Només les converses amb `review_status: approved` cobreixen unitats.

```bash
python3 -m pip install -r maia/training-data/knowledge/scripts/requirements.txt
python3 maia/training-data/knowledge/scripts/build_knowledge_inventory.py --check
python3 maia/training-data/knowledge/scripts/validate_knowledge_review.py --check
python3 -m unittest discover -s maia/training-data/knowledge/scripts/tests -v
```

La dependència actual és PyYAML. Les decisions d'exclusió per unitat es registren a `review/unit-decisions.jsonl`, amb un motiu i IDs de font.
