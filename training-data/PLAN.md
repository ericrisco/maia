# Pla per crear Maia Training Data

## Objectiu

Preparar dos conjunts separats, a partir de `docs/`:

- **Maia Knowledge** ensenya a respondre dubtes reals sobre Andorra a partir de `docs/temes/`.
- **Maia Language** conserva llengua humana autèntica de `docs/parla/`; no es creen diàlegs artificials a partir de monòlegs.

La prioritat és que cada conversa sigui útil, natural i certa. No hi ha una quota mínima de registres. Els exemples de calibratge serveixen per acordar el to i no són dades d’entrenament.

## La unitat és una conversa humana

Abans d’escriure, llegeix la font i pensa quin dubte podria tenir una persona que no ha vist la fitxa. Formula’l amb paraules corrents, com si demanés ajuda a algú que coneix el tema.

Una bona conversa:

1. Comença amb una pregunta que s’entén tota sola i que té un motiu recognoscible: aclarir una confusió, entendre una tradició, situar un fet o saber què es pot afirmar.
2. Rep una resposta directa i completa, escrita per a aquella persona.
3. Continua només si la resposta provoca una pregunta natural. Cada seguiment depèn del que s’acaba de dir.
4. Acaba quan el dubte ja està resolt. Un sol intercanvi és suficient.

El nombre de torns ve del fil de la conversa, no d’una quota. No afegeixis un seguiment per fer que sembli més conversacional.

## Preguntes que no volem

Descarta preguntes que només tenen sentit davant del document:

- «Què explica la secció “El relat”?»
- «Què indica aquesta fila?»
- «Resumeix la fitxa sobre la Marratxa.»
- «Què diu el corpus sobre aquest tema?»

També descarta preguntes genèriques o de qüestionari que podrien aplicar-se a qualsevol tema:

- «Què és X?» repetida mecànicament per cada títol.
- «Quan va passar?» sense dir a què es refereix.
- Una pregunta amb una premissa que cap persona tindria motiu per fer.
- Una pregunta inventada per encaixar la informació disponible.

No inventis una experiència personal («m’han dit», «hi vaig anar») per fer més humana una pregunta. No copiïs el títol i el subtítol com si fossin una petició.

## Com escriure respostes

- Contesta primer el dubte concret. No comencis amb un fragment, una capçalera ni una llista sense introducció.
- Escriu en català corrent. Fes servir frases completes i identifica clarament persones, dates i llocs.
- Inclou prou context perquè la resposta s’entengui sense llegir la font.
- Diferencia un fet documentat d’una llegenda, una interpretació o una possibilitat.
- Si les fonts discrepen, explica en què i no triïs una versió sense motiu.
- Si la informació no permet respondre, digues què se sap i quin límit té la font. El silenci d’una fitxa no demostra que una cosa no existeixi.
- No afegeixis dades només perquè semblen una continuació plausible.

## Seguiments i multitorn

Un seguiment ha de ser una reacció probable a la resposta anterior, amb referents clars. Pot demanar una conseqüència, aclarir un terme que acaba d’aparèixer o comprovar què vol dir una discrepància.

Abans d’afegir-lo, pregunta’t: «Si algú m’acabés de respondre això, jo preguntaria aquesta cosa?» Si la nova pregunta obre un tema independent, crea un altre registre o no la facis.

No cal que cada registre sigui multitorn. Evita «I què més?», canvis de tema i preguntes seguides que semblen targetes d’estudi.

## Revisió abans d’acceptar un registre

Llegeix la conversa en veu alta sense tenir la fitxa al davant i comprova:

1. La pregunta inicial sona com una petició real d’ajuda?
2. La persona que pregunta podria entendre-la sense conèixer l’organització de Maia?
3. Cada resposta contesta la pregunta completa, en lloc de reproduir un tros de font?
4. El seguiment neix de la resposta i manté el mateix fil?
5. Cada afirmació es pot verificar en les fonts indicades?
6. La resposta manté els matisos i no presenta llegendes, estimacions o dades parcials com a certeses?
7. Els drets de les fonts permeten exportar el registre?

Si un registre falla, reescriu-lo o descarta’l. No cal salvar tots els fets ni produir més registres per compensar un exemple dolent.

## Estructura de treball

- `knowledge/examples/`: converses de calibratge. Mai no s’exporten.
- `knowledge/review/`: candidats a revisar, amb procedència guardada per separat.
- `knowledge/work/`: inventari, cobertura i notes internes; no s’inclouen als xats finals.
- `knowledge/output/`: només exports revisats, deduplicats i amb drets aclarits. Pot quedar buit fins que hi hagi registres aprovats.
- `language/`: inventari i selecció de parla autèntica. No es barreja amb Knowledge.

Una línia JSONL de conversa conté només `messages` amb `role` i `content`. Els IDs, les fonts, els drets i les notes de revisió es guarden en fitxers interns separats.

## Etapes

1. Calibrar el to amb els exemples i ajustar-los amb l’usuari.
2. Aplicar el criteri a Knowledge, tema per tema, revisant cobertura i procedència.
3. Auditar Language segons autenticitat, qualitat de transcripció i drets.
4. Exportar només registres aprovats; revisar duplicats, splits i cobertura.

No s’omple `output/` fins que els registres passin les revisions factuals, de naturalitat i de drets.
