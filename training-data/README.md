# Maia Training Data

Conté dos datasets independents per especialitzar Maia en Andorra:

- **Knowledge:** respostes correctes a preguntes reals sobre el contingut de `docs/temes/`.
- **Language:** mostres de català andorrà contemporani produïdes per persones, extretes de `docs/parla/` amb els criteris d'elegibilitat del corpus.

Les preguntes de Knowledge no es fabriquen a partir de títols o seccions. Cada conversa ha de començar amb un dubte que una persona formularia sense veure la fitxa. Els seguiments només s'afegeixen quan neixen de la resposta anterior. Language no comparteix registres ni criteris de redacció amb Knowledge.

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── review/       # exemples editorials, candidats, procedència i arxiu
│   ├── work/         # inventari i cobertura per document
│   ├── scripts/      # inventari, validació i exportació
│   ├── reports/      # cobertura, qualitat i exclusions
│   └── output/       # només datasets aprovats
└── language/
    ├── review/       # fragments candidats i procedència
    ├── work/         # elegibilitat i fiabilitat de transcripcions
    ├── scripts/
    ├── reports/
    └── output/       # només datasets aprovats
```

`knowledge/review/EXEMPLES.md` calibra l'estil i no és entrenament. Els 49 candidats anteriors s'han apartat de la cua activa perquè cal revisar-los sota el criteri nou; la seva procedència i l'estat de cobertura es conserven a `knowledge/review/archive/pre-redesign-2026-10-07/`. No compten com a cobertura ni s'exporten.

La cua activa comença buida. Encara no hi ha exports preparats. Per revisar la cobertura de Knowledge, executa des de l'arrel de `maia/`:

```bash
python3 training-data/knowledge/scripts/build_document_inventory.py
```

Cada línia de `conversations.jsonl` és una conversa sencera amb `messages` de rols `user` i `assistant`. La procedència, els drets i les afirmacions recolzades es guarden en una línia corresponent de `provenance.jsonl`. Cada nova conversa es revisa, valida, commiteja i puja abans d'afegir-ne una altra.
