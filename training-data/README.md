# Maia Training Data

Dos conjunts diferents, perquè cadascun ensenya una habilitat diferent:

- **Knowledge** ensenya a contestar preguntes reals sobre Andorra amb informació de `docs/temes/`.
- **Language** conserva usos reals del català andorrà contemporani a partir de `docs/parla/`. No s'inventen diàlegs per imitar una veu local.

`knowledge/examples/` conté quatre mostres per calibrar el to. Són internes, no aprovades ni exportables. Els candidats antics de `knowledge/review/` queden retirats: no s'han de revisar ni exportar. Els registres nous han d'estar en un fitxer nou i passar el criteri de `PLAN.md`.

No hi ha datasets finals. Els splits es crearan quan hi hagi prou registres revisats, drets comprovats i una separació fiable entre train, validation i test.

**Regla principal:** cada conversa comença amb un dubte que una persona podria tenir sense haver obert cap fitxa. La resposta el resol directament. El seguiment només s'hi afegeix si surt de la resposta anterior. No hi ha quota de torns: un torn també pot ser suficient.
