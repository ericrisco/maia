# Maia Training Data

Prepararem dos conjunts separats a partir del corpus de `docs/`:

- **Knowledge** respon dubtes reals sobre Andorra amb informació de `docs/temes/`.
- **Language** conserva mostres de català andorrà contemporani produïdes per persones, a partir de material elegible de `docs/parla/`.

Ara només hi ha exemples editorials per calibrar Knowledge. No són registres d'entrenament. Les cues candidates comencen buides i no hi ha cap export preparat.

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── review/       # criteris, exemples, candidats i procedència
│   ├── work/         # inventari i estat de revisió del corpus
│   ├── scripts/      # eines de cobertura, validació i exportació
│   ├── reports/      # cobertura, qualitat i exclusions
│   └── output/       # exports aprovats; buit durant el calibratge
└── language/
    ├── review/       # fragments humans candidats i procedència
    ├── work/         # elegibilitat i fiabilitat de transcripció
    ├── scripts/
    ├── reports/
    └── output/       # exports aprovats; buit durant el calibratge
```

Comença per [`PLAN.md`](PLAN.md) i [`knowledge/review/EXEMPLES.md`](knowledge/review/EXEMPLES.md). La procedència dels exemples és a [`knowledge/review/examples-provenance.md`](knowledge/review/examples-provenance.md). La procedència dels registres reals es guardarà separada del text de conversa.
