# Maia Knowledge

Font: `docs/temes/`. El dataset ensenya coneixement sobre Andorra mitjançant converses que responen dubtes humans. No converteix cada paràgraf o dada en una pregunta.

- `examples/`: exemples de calibratge, sempre no exportables.
- `work/`: inventari, cobertura i procedència; mai no s'injecta als missatges.
- `reports/`: resultats de revisió i cobertura.
- `output/`: només converses aprovades i amb drets d'ús revisats.

Format previst d'una línia: `{"messages":[{"role":"user","content":"…"},{"role":"assistant","content":"…"}]}`. Un diàleg pot tenir més torns. Cap metadada editorial no forma part de `messages`.
