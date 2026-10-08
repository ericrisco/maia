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

Encara no s'ha aprovat cap nou lot de converses Knowledge després d'aquest
canvi de criteri. `knowledge/review/conversations.jsonl` conserva el lot antic,
que s'ha de revisar registre per registre abans de reutilitzar-lo. Els exemples
són editorials; no s'exporten a `output/`.
