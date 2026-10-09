# Treball de Language

Les sortides JSONL són representacions internes per a revisió; poden contenir fragments transcrits i no s'han d'exportar ni entrenar directament.

- `selection.jsonl`: estat d'elegibilitat i fragment per peça.
- `authentic-segments.jsonl`: segments literais extrets del material de parla; la literalitat no vol dir que la transcripció estigui verificada.
- `conversation-candidates.jsonl` i `candidate-messages.jsonl`: parelles humanes detectades. Ara no n'hi ha cap.
- `piece-rights.jsonl`: llicència verificada per peça, separada de l'estat general de la font.

Les incerteses de transcripció, permisos pendents i manca de parelles explícites bloquegen qualsevol exportació.
