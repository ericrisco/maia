# Maia Training Data

Aquest directori prepara dos recursos separats a partir del corpus de Maia:

- **Knowledge** ensenya a respondre preguntes reals sobre Andorra amb fets verificables de `docs/temes/`.
- **Language** conserva trets de català andorrà contemporani a partir de parla humana de `docs/parla/`.

## Punt de partida

Ara hi ha una guia de redacció i cinc converses de calibratge de Knowledge. Serveixen per acordar el to. No són dades aprovades ni es poden exportar per entrenar. No hi ha cap dataset final ni cap split.

## Estructura

- `PLAN.md`: com redactar, revisar i ampliar les converses.
- `knowledge/examples/`: mostres de calibratge i procedència separada.
- `knowledge/review/`: criteris per acceptar o rebutjar registres futurs.
- `knowledge/work/`: inventari i seguiment de cobertura, quan reprenguem la producció.
- `knowledge/output/`: reservat per a exports aprovats.
- `language/work/`: inventari d'enregistraments i elegibilitat.
- `language/output/`: reservat per a fragments humans aprovats.

Les mostres actuals es poden llegir sense obrir cap fitxa. Els seus fets i límits, en canvi, sí que s'han de comprovar a les fonts indicades a `knowledge/examples/provenance.jsonl`.
