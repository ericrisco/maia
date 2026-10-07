# Prototip nou de Maia Training Data

Aquest directori és una proposta revisable. Encara no és la ubicació definitiva
del dataset i no conté registres acceptats per a l'entrenament.

## Estructura proposada

```text
training-data/
├── README.md
├── knowledge/
│   ├── README.md
│   ├── examples/
│   │   ├── conversations.jsonl
│   │   └── sources.md
│   ├── review/
│   ├── output/
│   └── reports/
└── language/
    ├── README.md
    ├── review/
    ├── output/
    └── reports/
```

`examples/` és el banc petit que es revisa amb persones. `review/` rep només
converses que han passat aquesta revisió. `output/` conté exportacions
regenerables; no s'edita a mà. `sources.md` guarda les fonts fora dels diàlegs.
Knowledge i Language continuen separats.

## Què ha de passar abans d'acceptar una conversa

1. La primera pregunta explica una situació o un dubte recognoscible.
2. La primera resposta contesta el dubte sense resumir una fitxa.
3. Cada seguiment depèn del que s'acaba de dir i aporta una precisió nova.
4. El diàleg s'atura quan la persona ja ha entès la resposta.
5. Cada dada es pot comprovar a les fonts indicades a `examples/sources.md`.

Les mostres d'aquest prototip il·lustren el criteri. No compten per a cobertura
ni s'han d'afegir automàticament al dataset.
