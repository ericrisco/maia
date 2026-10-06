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
│   ├── review/
│   │   ├── examples.jsonl
│   │   ├── provenance.jsonl
│   │   └── quality-rubric.md
│   └── output/README.md
└── language/
    ├── README.md
    ├── review/README.md
    └── output/README.md
```

Cada línia de `examples.jsonl` té el format de conversa que pot acabar al
dataset. La traça, l'estat de revisió i les notes editorials van en fitxers
paral·lels; mai dins del JSONL d'entrenament.

Algunes fitxes de font exigeixen atribució i compartir les obres derivades amb
la mateixa llicència. Aquestes condicions també s'han de complir en qualsevol
dataset exportat.

## Següent pas

Revisar junts els exemples pilot. Quan el to i els criteris ens convencin,
afegirem registres en tandes petites, tema a tema. Només les converses
aprovades i amb fonts aptes per redistribuir podran passar a `output/`.
