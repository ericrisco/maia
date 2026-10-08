# Treball intern de Knowledge

- `coverage.csv` inventaria els documents de `docs/temes/` i indica quins tenen candidats associats.
- `coverage-items.jsonl` desglossa els fets que cal cobrir i enllaça cada fet amb els registres de `review/conversations.jsonl`.
- `provenance.jsonl` conserva les fonts, els drets i el resum de cobertura de cada conversa candidata. El hash ha de correspondre al JSON compacte de la conversa.

Les converses de `review/conversations.jsonl` són candidates, no dades finals aprovades. No s'exporten fins que s'hagin revisat la qualitat, la cobertura, els duplicats, la procedència i els drets de les fonts. La informació interna d'aquests fitxers no forma part del missatge d'entrenament.
