# Maia Knowledge

Conjunt de converses sobre Andorra, basades en `docs/temes/`. La unitat de treball és un dubte humà, no una secció ni una dada a extreure.

- [`review/`](review/): criteri editorial, exemples de calibratge, candidats, procedència i arxiu.
- `work/`: inventari i estat de revisió de cada fitxa.
- `scripts/`: inventari, validació i exportació.
- `reports/`: cobertura, qualitat i exclusions.
- `output/`: només exports aprovats i elegibles.

Els 49 candidats anteriors i la seva procedència es conserven a `review/archive/pre-redesign-2026-10-07/` per auditar-los. No són candidats actius ni compten com a cobertura. La cua activa comença buida per aplicar els criteris de `review/CONVERSATION-GUIDE.md` i `review/EXEMPLES.md` des del primer registre.

Per regenerar l'inventari i el resum de cobertura, executa des de l'arrel de `maia/`:

```bash
python3 training-data/knowledge/scripts/build_document_inventory.py
```

El format candidat és una conversa JSONL per línia, amb rols `user` i `assistant`. La procedència correspon a la mateixa conversa per `example_id`; les metadades internes no entren al text d'entrenament.
