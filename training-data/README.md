# Maia Training Data

Aquesta carpeta prepara dades de fine-tuning en dos conjunts separats:

- **Knowledge** ensenya a respondre dubtes sobre Andorra amb informació documentada a `docs/temes/`.
- **Language** conserva l'ús real del català andorrà contemporani a partir de parla humana elegible a `docs/parla/`.

## Estructura

```text
training-data/
├── PLAN.md
├── README.md
├── scripts/                  # eines compartides
├── knowledge/
│   ├── review/               # converses candidates i criteris editorials
│   ├── work/                 # evidència i decisions de cobertura
│   ├── reports/              # resum de cobertura i qualitat
│   ├── scripts/
│   └── output/               # només registres aprovats
└── language/
    ├── review/               # revisió de fragments humans
    ├── work/                 # selecció i incerteses
    ├── reports/
    ├── scripts/
    └── output/               # només material aprovat
```

A `PLAN.md` defineix el procés. La guia `knowledge/review/QUESTION-DESIGN.md` explica com començar per un dubte humà i quan afegir un seguiment. `knowledge/review/EXEMPLES.md` mostra converses editorials per acordar l'estil; no són preguntes reals ni registres aprovats. `knowledge/review/conversations.jsonl` és el lot actiu de converses candidates; la traça corresponent va a `knowledge/review/provenance.jsonl`. Les converses antigues que no passaven el criteri actual es conserven a `knowledge/review/quarantine/` i no formen part del lot actiu.

Llegeix [PLAN.md](PLAN.md) abans de preparar registres. No barregis Knowledge i Language. No omplis `output/` fins que el contingut i els drets hagin passat revisió.
