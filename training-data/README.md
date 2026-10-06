# Maia Training Data

Aquesta carpeta prepara dades de fine-tuning en dos conjunts separats:

- **Knowledge** ensenya a respondre dubtes sobre Andorra amb informació documentada a `docs/temes/`.
- **Language** conserva l'ús real del català andorrà contemporani a partir de parla humana elegible a `docs/parla/`.

A `knowledge/review/EXEMPLES.md` mostra com reescriure preguntes de fitxa com a dubtes que una persona podria tenir. `knowledge/review/conversations.jsonl` és el lot concret de converses candidates; la traça de cada línia va a `knowledge/review/provenance.jsonl`. Les candidates no són registres aprovats ni exportables. Els exemples antics són a `knowledge/review/quarantine/` i no formen part del lot actiu.

Llegeix [PLAN.md](PLAN.md) abans de preparar registres. No barregis Knowledge i Language. No omplis `output/` fins que el contingut i els drets hagin passat revisió.
