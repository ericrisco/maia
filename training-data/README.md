# Maia Training Data

Aquest directori prepara dos recursos separats a partir del corpus de Maia:

- **Knowledge** ensenya a respondre preguntes reals sobre Andorra amb fets verificables de `docs/temes/`.
- **Language** conserva trets de català andorrà contemporani a partir de parla humana de `docs/parla/`.

## Punt de partida

Hi ha un pla editorial i cinc converses de calibratge de Knowledge. Les 128 converses candidates anteriors s'han retirat perquè el criteri de qualitat s'ha reiniciat. L'inventari de continguts es conserva, però les files tornen a `pending`: encara no compten com a cobertes. Les mostres de calibratge no són registres aprovats i no es poden exportar per entrenar. No hi ha cap dataset final ni cap split.

## Estructura

- `PLAN.md`: com redactar, revisar i ampliar les converses.
- `knowledge/examples/`: mostres de calibratge i procedència separada.
- `knowledge/review/`: guia de revisió; les noves converses s'hi afegeixen només després de passar la lectura cega.
- `knowledge/work/`: inventari de continguts i seguiment de cobertura. Les anotacions anteriors es conserven com a pistes, no com a cobertura vigent.
- `knowledge/output/`: reservat per a exports aprovats.
- `language/work/`: inventari d'enregistraments i elegibilitat.
- `language/output/`: reservat per a fragments humans aprovats.

Per redactar o revisar registres, segueix [`PLAN.md`](PLAN.md). Una conversa ha de començar amb una pregunta que algú faria sense haver llegit el corpus; cada repregunta ha de seguir el fil i cada resposta ha de ser completa i comprovable.

Les mostres actuals es poden llegir sense obrir cap fitxa. Els seus fets i límits, en canvi, sí que s'han de comprovar a les fonts indicades a `knowledge/examples/provenance.jsonl`.
