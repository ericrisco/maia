# Maia Training Data

Dos conjunts separats, construïts a partir del corpus de `docs/`:

- **Maia Knowledge** transforma coneixement documentat d'Andorra en converses naturals. La font factual és `docs/temes/`.
- **Maia Language** conserva fragments de català andorrà contemporani produïts per persones. La font és `docs/parla/`.

No s'han de barrejar. Les respostes redactades de Knowledge no són mostra de parla autèntica; Language no s'amplia amb respostes inventades.

## On és cada cosa

- [`PLAN.md`](PLAN.md): flux de treball, criteri de naturalitat i porta de qualitat.
- [`knowledge/examples/`](knowledge/examples/): diàlegs editorials per ensenyar l'estil. No són entrenables ni compten per cobertura.
- [`knowledge/review/`](knowledge/review/): converses candidates pendents de revisió humana, amb procedència en un fitxer separat.
- [`knowledge/archive/`](knowledge/archive/): esborranys rebutjats, exclosos de cobertura i exportació.
- [`knowledge/work/`](knowledge/work/): inventari de documents, evidències i cobertura.
- [`knowledge/reports/`](knowledge/reports/): resum d'estat i qualitat.
- [`knowledge/output/`](knowledge/output/): splits finals només després de revisar contingut i drets.
- [`language/`](language/): selecció, revisió i sortides de material lingüístic autèntic.

Els missatges d'entrenament no porten metadades de pipeline. Les fonts, evidències i drets s'auditen a part. Els outputs romanen buits fins que els registres compleixen els criteris de qualitat, revisió i drets.
