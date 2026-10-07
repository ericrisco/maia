# Eines de Knowledge

`build_document_inventory.py` inventaria tots els Markdown de `docs/temes/`, associa converses a les seves fonts i genera el resum de cobertura.

Executa'l des de l'arrel de `maia/` amb:

```bash
uv run python training-data/knowledge/scripts/build_document_inventory.py
```

El procés valida el format de les converses i la procedència. No marca cap fitxa com a completa per tenir converses: cal una revisió semàntica i deixar els buits documentats a `work/document-status.json`.
