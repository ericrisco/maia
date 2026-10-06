# Maia Training Data

Àrea de treball per preparar dos datasets independents a partir de `docs/`:

- **Knowledge** ensenya què sap Maia sobre Andorra.
- **Language** conserva com parlen persones andorranes en material oral elegible.

Ara només hi ha una prova editorial petita per a Knowledge. No hi ha encara
cap dataset aprovat ni fitxers `train`, `validation` o `test`. Els exemples de
revisió no s'han d'entrenar directament.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── work/                # ledgers interns regenerables, ignorats per Git
│   ├── reports/             # inventari i cobertura
│   ├── review/
│   │   ├── conversations.jsonl
│   │   ├── EXEMPLES.md
│   │   ├── provenance.jsonl
│   │   └── quality-rubric.md
│   └── output/README.md
└── language/
    ├── README.md
    ├── work/                # extraccions internes regenerables
    ├── reports/             # elegibilitat, incertesa i splits
    ├── review/README.md
    └── output/README.md
```

Cada línia de `conversations.jsonl` té el format de conversa que pot acabar al
dataset. La traça, l'estat de revisió i les notes editorials van en fitxers
paral·lels; mai dins del JSONL d'entrenament.

Per regenerar els inventaris, executa des de l'arrel de `maia/`:

```sh
python3 training-data/scripts/build_inventory.py
```

Algunes fitxes de font exigeixen atribució i compartir les obres derivades amb
la mateixa llicència. Aquestes condicions també s'han de complir en qualsevol
dataset exportat.

## Baseline actual

L'extracció estructural ha llegit els **1.477** Markdown de `docs/temes/` sense
errors: **10.749** seccions, **3.130** taules, **22.537** files de taula i
**87.339** unitats d'evidència. Aquestes unitats són material per revisar, no
87.339 preguntes ni registres ja entrenables. El report és a
[`knowledge/reports/inventory.json`](knowledge/reports/inventory.json).

Per a Language, hi ha **45** entrades sota `docs/parla/`, de les quals **40** són
peces de parla i **38** compleixen els filtres bàsics de veu, època i
metadades. Tenen **8.449** fragments marcats com incerts; no s'hi han trobat
torns user/assistant explícits, i els **40** vincles a fonts indiquen
redistribució pendent. Per tant, encara no hi ha mostres Language exportables.
Vegeu [`language/reports/eligibility.json`](language/reports/eligibility.json).

Continuarem amb Knowledge pregunta a pregunta. Les fonts amb permisos pendents,
la parla incerta i les exclusions quedaran visibles; no comptaran com a dades
llestes per entrenar fins que se'n resolgui l'estat.
