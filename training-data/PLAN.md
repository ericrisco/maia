# Pla editorial de Maia Training Data

## Objectiu

Crear dos conjunts separats a partir de `docs/`:

- **Knowledge** respon dubtes reals sobre Andorra amb informació contrastada de `docs/temes/`.
- **Language** conserva català andorrà produït per persones a `docs/parla/`.

Ara prioritzem la qualitat de les converses Knowledge. Els registres anteriors s'han retirat del pilot perquè moltes preguntes demanaven inspeccionar una fitxa, una secció o una fila. No compten com a cobertura. La feina de Language continua separada i intacta.

## Estructura

```text
training-data/
├── PLAN.md
├── README.md
├── knowledge/
│   ├── review/
│   │   ├── CONVERSATION-GUIDE.md
│   │   ├── EXEMPLES.md          # calibratge editorial; no s'exporta
│   │   ├── conversations.jsonl  # només converses candidates/aprovades
│   │   └── provenance.jsonl     # font i drets, una línia per conversa
│   ├── work/                    # inventari i cobertura interns
│   ├── scripts/
│   ├── reports/
│   └── output/                  # exports aprovats
└── language/
    ├── review/
    ├── work/
    ├── scripts/
    ├── reports/
    └── output/
```

Les mostres d'`EXEMPLES.md` no són dades ni compten com a cobertura. `conversations.jsonl` conté només missatges `user` i `assistant`. La procedència, la revisió i els drets queden en fitxers separats.

## Mètode per a cada conversa

1. Llegir la fitxa sencera i les fonts pertinents. Anotar quina afirmació concreta es pot ensenyar.
2. Imaginar una situació normal en què algú tindria aquest dubte. Si no en surt cap de creïble, no fabricar una pregunta per omplir quota.
3. Escriure l'entrada com ho diria aquella persona, amb el context mínim perquè s'entengui sense haver vist el corpus.
4. Respondre primer el dubte. Fer servir el to d'un assistent informat, no el d'una enciclopèdia ni el d'un extractor.
5. Afegir un seguiment només si neix de la resposta anterior: una conseqüència, una precisió, una sorpresa o una decisió pràctica.
6. Aturar-se quan la persona ja en sap prou. La conversa pot tenir un intercanvi; si hi ha continuació natural, normalment en tindrà dos o tres.
7. Revisar les afirmacions contra les fonts i anotar-ne la procedència, l'estat dels drets de cada font i els límits coneguts.

No cal que cada conversa cobreixi tota la fitxa. Cal que cobreixi informació útil sense convertir cada dada en una pregunta separada. Les relacions entre fitxes només s'utilitzen quan una mateixa persona podria raonablement necessitar-les juntes.

## Què vol dir «multitorn»

Un diàleg multitorn té continuïtat, no només més missatges. Cada nova pregunta ha de dependre del que s'acaba de respondre. Per exemple: la persona pregunta si dues tradicions són el mateix; després de la distinció, demana què passa en una d'elles. No serveix afegir una pregunta sobre una data sense relació només per allargar el registre.

No fixem un mínim de torns. No creem seqüències artificials de quatre preguntes. Un únic bon intercanvi és millor que una conversa forçada.

## Porta de qualitat

Abans d'aprovar una conversa, comprovar:

- La pregunta inicial té sentit fora del corpus i no pressuposa que l'usuari té una fitxa oberta.
- Es pot descriure el motiu humà de la pregunta en una frase concreta.
- La resposta contesta directament i només amplia amb context útil.
- Cada seguiment reprèn el fil anterior i aporta una comprensió nova.
- La conversa sona natural llegida en veu alta, sense notes editorials.
- Les llegendes, les interpretacions, les fonts secundàries i els fets documentats queden distingits.
- Cap resposta transforma un buit de la font en una afirmació sobre el món.
- Cada dada factual es pot rastrejar a la font anotada a `provenance.jsonl`.
- Si una conversa combina fonts, els drets s'anoten per font; no es resumeixen en un únic estat ambigu.

Rebutjar o reescriure si apareix alguna d'aquestes formes sense motiu real: «Què explica la secció…?», «Què indica aquesta fila?», «Enumera…», «Digues dos topònims», preguntes independents encadenades o preguntes que només existeixen per buidar una llista.

## Pilot i següents passos

1. Revisar les mostres d'`knowledge/review/EXEMPLES.md` i ajustar-ne el to.
2. Preparar un pilot de 5–8 converses de temes diferents. Llegir-les com a diàlegs, sense veure les fonts.
3. Revisar el pilot amb l'usuari. Convertir-ne els comentaris en canvis concrets a aquesta guia.
4. Només després, reprendre la cobertura de `docs/temes/` per unitats útils i registrar també els límits del corpus.
5. Revisar Language separadament: veu humana, època, `apte_llengua`, drets i fiabilitat de transcripció.
6. Deduplicar, agrupar per document o peça abans de fer splits, validar i exportar quan el pilot i la cobertura estiguin aprovats.

Prioritats: correctesa, cobertura útil, naturalitat, continuïtat conversacional, diversitat i volum. No s'inventen fets per fer créixer el conjunt.
