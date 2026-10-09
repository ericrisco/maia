# Maia Language

Objectiu separat de Knowledge: conservar català contemporani produït per persones a partir de `docs/parla/`. No s'inventen preguntes per convertir monòlegs en diàlegs ni es reescriu la parla per fer-la semblar més andorrana.

## Estat de l'inventari

El cribratge actual troba 45 fitxes Markdown: 40 peces de parla i 5 índexs o síntesis. De les peces, 38 compleixen els camps de veu, època i `apte_llengua`; 2 queden excloses. El text conté 8.449 trams marcats com a incerts i 10.510 fragments literals de treball. Encara no hi ha cap parella explícita entre entrevistador i parlant ni cap missatge de Language exportable.

Quatre peces elegibles tenen una llicència Creative Commons Attribution verificada per peça. La reutilització de les altres 35 continua pendent; cap peça és exportable perquè les transcripcions també necessiten verificació i cal revisar el permís aplicable.

Els fragments i les transcripcions queden a `work/` per a revisió interna. No entren als exports. Els registres de `docs/parla/` amb marques `[?...]` no s'han de tractar com a verbatim sense verificar-los.

## Estructura i regeneració

- `work/`: selecció per peça, fragments literals, candidats de conversa i drets.
- `reports/`: recompte d'elegibilitat, incertesa, llicències i inflació.
- `scripts/build_language_inventory.py`: regenera l'inventari a partir de `docs/parla/` i de les captures de llicència per peça que hi hagi a `docs/raw/parla/`.
- `review/`: converses que conserven torns humans reals, quan n'hi hagi i després de revisar transcripció i drets.
- `output/`: train, validation i test aprovats; encara buit.

Executa l'inventari des de l'arrel del repositori:

```bash
PYTHONPATH=src python3 training-data/language/scripts/build_language_inventory.py
```

La guia global de curació és a [`../PLAN.md`](../PLAN.md).
