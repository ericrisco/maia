# Maia Training Data

Aquesta carpeta prepara dades de fine-tuning en dos conjunts separats:

- **Knowledge** ensenya a respondre dubtes sobre Andorra amb informació documentada a `docs/temes/`.
- **Language** conserva l'ús real del català andorrà contemporani a partir de parla humana elegible a `docs/parla/`.

A `PLAN.md` defineix el criteri de treball. `knowledge/review/EXEMPLES.md` conté unes poques mostres per acordar l'estil: són exemples editorials, no preguntes reals ni registres aprovats. `knowledge/review/conversations.jsonl` és el lot actiu de converses candidates; la traça corresponent va a `knowledge/review/provenance.jsonl`. Les converses antigues que no passaven el nou criteri es conserven a `knowledge/review/quarantine/` i no formen part del lot actiu.

Llegeix [PLAN.md](PLAN.md) abans de preparar registres. No barregis Knowledge i Language. No omplis `output/` fins que el contingut i els drets hagin passat revisió.
