# Maia Knowledge

Font: `docs/temes/`. El dataset ensenya coneixement sobre Andorra mitjançant converses que responen dubtes humans. No converteix cada paràgraf o dada en una pregunta.

- `review/`: exemples i candidats multitor, sempre no exportables mentre no estiguin aprovats.
- `work/`: inventari, cobertura i procedència; mai no s'injecta als missatges.
- `reports/`: resultats de revisió i cobertura.
- `output/`: només converses aprovades i amb drets d'ús revisats.

La cobertura completa de `docs/temes/` és a `work/coverage.csv`.

Format previst d'una línia: `{"messages":[{"role":"user","content":"…"},{"role":"assistant","content":"…"}]}`. Un diàleg pot tenir més torns. Cap metadada editorial no forma part de `messages`.
