# Maia Knowledge

Aquest conjunt ensenya a respondre preguntes sobre Andorra amb informació de `docs/temes/`. Les converses han de començar per un dubte humà, no per l'estructura d'una fitxa. Consulta [`../PLAN.md`](../PLAN.md) i la [guia de calibratge](review/EXEMPLES.md) abans d'afegir registres.

## Estat

La fase actual defineix l'estructura i calibra el criteri amb tres exemples. Aquests exemples tenen estat `approved_sample`: serveixen per revisar la qualitat, però no s'exporten ni compten com a cobertura. Encara no hi ha una cua nova de registres de producció.

## Carpetes

- `review/records.jsonl`: font de veritat de revisió. Cada línia combina missatges, procedència, drets, límits i estat.
- `review/conversations.jsonl`: export revisable generat pel validador; només inclou registres `approved` i només conserva `messages`.
- `review/EXEMPLES.md`: llindar editorial i exemples de calibratge.
- `review/unit-decisions.jsonl`: decisions sobre unitats excloses o pendents.
- `work/`: inventari regenerable de documents i unitats.
- `reports/`: resultats de cobertura i qualitat.
- `output/`: futurs fitxers d'entrenament; no s'omplen durant el calibratge.

## Afegir converses

1. Comprova drets i evidència a les fonts originals.
2. Escriu la intenció humana que la conversa ha de resoldre.
3. Redacta el diàleg sencer; cada registre de Knowledge aprovat és multitorn, amb seguiments que aporten informació nova.
4. Aplica la lectura a cegues i la checklist de `review/EXEMPLES.md`.
5. Guarda l'evidència i els missatges junts a `records.jsonl`.
6. Executa `python training-data/knowledge/scripts/validate_knowledge_review.py --check` per comprovar l'esquema i regenerar la vista d'export i l'informe de cobertura.

No editis a mà `conversations.jsonl`: és una sortida generada. No converteixis els exemples de calibratge en dades aprovades sense una revisió explícita.
