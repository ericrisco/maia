# Revisió de converses

Aquí es preparen i s'auditen converses abans de l'exportació. Cada candidat ha de guardar, fora dels missatges entrenables:

- la intenció del dubte;
- la conversa completa en torns alterns `user` i `assistant`;
- les afirmacions i passatges que la sostenen;
- la font exacta, la seva llicència, l'atribució requerida i l'estat d'autorització;
- l'estat de revisió i el motiu de qualsevol exclusió.

`records.jsonl` és el registre de procedència i revisió, una línia per conversa. `conversations.jsonl` conté només les converses aprovades, amb l'esquema `{"messages":[...]}` que es pot passar al fine-tuning. Totes dues línies comparteixen l'identificador `id` només al registre intern; aquest identificador no entra al fitxer entrenable.

No s'aprova una conversa només perquè cobreixi una unitat. Les mostres editorials d'`EXEMPLES.md` no formen part de cap JSONL d'entrenament.
