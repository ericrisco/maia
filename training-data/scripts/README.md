# Scripts del pipeline

Els scripts són repetibles des de qualsevol directori, amb sortides deterministes i sense sobreescriure registres revisats.

## Inventari Knowledge

Des de l'arrel de `maia/`, executa:

```sh
python3 training-data/scripts/build_knowledge_inventory.py
```

El parser llegirà `docs/`, extractarà les unitats de `docs/temes/` i registrarà seccions, taules, files, enllaços, procedència i errors. Els ledgers grans van a `knowledge/work/` i es poden regenerar. El resum és `knowledge/reports/inventory.json`.

Els pròxims passos són reconciliar cada unitat amb converses o exclusions justificades, afegir revisió natural i de drets, i després construir deduplicació, splits i validadors d'exportació. El generador literal antic no s'ha d'utilitzar per crear preguntes d'entrenament: produeix formes com «Què explica la secció?» que incompleixen `knowledge/review/EXEMPLES.md`.

## Cobertura Knowledge

```sh
python3 training-data/scripts/build_knowledge_coverage.py
```

El script valida les traces i els hashes, vincula cada registre revisat amb els seus IDs d'evidència i genera un resum per branca temàtica. Els esborranys no compten com a evidència coberta per registres aprovats ni com a exportables.

## Auditoria Language

```sh
python3 training-data/scripts/build_language_review.py
```

L'auditoria aplica els camps d'elegibilitat del contracte del corpus, conserva spans humans literals, detecta marques d'incertesa i només forma converses a partir de torns explícits. No inventa preguntes per omplir peces sense diàleg.
