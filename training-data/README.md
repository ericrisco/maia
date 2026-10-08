# Maia Training Data

Aquest espai prepara dues fonts d'aprenentatge independents:

- [**Knowledge**](knowledge/README.md): converses útils sobre Andorra, basades
  en el corpus `docs/temes/`.
- [**Language**](language/README.md): català andorrà contemporani extret de
  parla humana elegible a `docs/parla/`.

El [pla](PLAN.md) fixa com escriure converses naturals. Les [mostres de
Knowledge](knowledge/review/EXEMPLES.md) serveixen per calibrar l'estil; no
són registres d'entrenament. Les preguntes parteixen d'un dubte humà i els
seguiments mantenen el fil sense allargar-lo per obligació.

Les 89 primeres converses de `knowledge/review/conversations.jsonl` són del lot
antic i s'han de revisar registre per registre abans de reutilitzar-les. Les
converses afegides després s'aproven individualment amb procedència. Encara no
hi ha cap exportació Knowledge final. Els exemples són editorials i no
s'exporten a `output/`.
