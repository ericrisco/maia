# Scripts del pipeline

Els scripts són repetibles des de qualsevol directori, amb sortides deterministes i sense sobreescriure registres revisats.

## Inventari Knowledge

Des de l'arrel de `maia/`, executa:

```sh
python3 training-data/scripts/build_knowledge_inventory.py
```

El parser llegirà `docs/`, extractarà les unitats de `docs/temes/` i registrarà seccions, taules, files, enllaços, procedència i errors. Els ledgers grans van a `knowledge/work/` i es poden regenerar. El resum és `knowledge/reports/inventory.json`.

Els pròxims passos són reconciliar cada unitat amb converses o exclusions justificades, afegir revisió natural i de drets, i després construir deduplicació, splits i validadors d'exportació. El generador literal antic no s'ha d'utilitzar per crear preguntes d'entrenament: produeix formes com «Què explica la secció?» que incompleixen `knowledge/review/EXEMPLES.md`.
