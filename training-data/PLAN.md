# Pla de Maia Training Data

## Objectiu

Crear dos datasets independents i traçables a partir de `docs/`:

- **Knowledge** ha d'ensenyar a respondre preguntes reals sobre Andorra amb el coneixement de `docs/temes/`.
- **Language** ha de conservar trets del català andorrà contemporani que apareixen en material humà elegible de `docs/parla/`.

L’objectiu és completar els dos conjunts. El calibratge inicial ja dona el patró editorial; la feina continua ara amb inventari exhaustiu, cobertura tema a tema, revisió de drets i producció progressiva de converses. No es generen splits fins que hi hagi prou registres aprovats.

## Com ha de sonar una conversa de Knowledge

Escriu una conversa que podria tenir lloc entre una persona curiosa i un assistent ben informat. La persona no sap com està organitzat el corpus i no ha de parlar com si estigués omplint un qüestionari.

Cada conversa té un fil:

1. La primera pregunta expressa un dubte, una confusió o una curiositat concreta.
2. La resposta resol aquest dubte de seguida. No guarda la informació principal per a més tard.
3. El seguiment neix d'un detall de la resposta i demana una precisió, una conseqüència, un límit o una comparació útil.
4. La resposta següent incorpora el context del diàleg i afegeix valor. No repeteix la resposta anterior.

El pilot ha de mostrar converses de dos o més torns d'usuari. En la producció, el nombre de torns dependrà del tema: no afegim repreguntes de farciment per complir una quota. Si una pregunta no admet un seguiment natural, la deixem com a conversa d'un sol torn.

Les persones poden fer servir pronoms, el·lipsis i expressions espontànies —«llavors», «i en aquest cas?», «però això vol dir que…?»— quan el context del diàleg les fa clares. No inventem experiències personals, emocions, argot ni errors per fer veure que la conversa és humana.

## Preguntes que no passen el criteri

No preguntis pel document. Pregunta pel món que el document ajuda a entendre.

- Rebutja: «Què explica la secció “El relat”?»
- Millor: «Com explica la llegenda que la imatge acabés al lloc del santuari?»
- Rebutja: «Què indica aquesta fila?»
- Millor: «El gràfic i el text donen les mateixes xifres per al català i el castellà?»
- Rebutja: «Quines coses registra el corpus?»
- Millor: pregunta per la distinció concreta que importa a la persona.

També rebutja preguntes que només canvien el nom o la data d'una plantilla, seguiments com «i què més?» sense una intenció clara, i preguntes amb una premissa tan estranya que ningú no les faria sense haver vist la fitxa.

## Respostes

- Comença per la resposta directa; després explica el perquè o el context necessari.
- Usa frases completes i identifica clarament de qui o de què parles.
- Distingeix fets, llegendes, interpretacions, estimacions i hipòtesis.
- Acota la resposta al cas i al període documentats.
- Si les fonts discrepen o no permeten saber una cosa, explica el límit amb naturalitat.
- No converteixis una absència de documentació en una afirmació que una cosa no va passar.
- No facis servir etiquetes, fragments copiats, llistes sense explicació ni referències al corpus, a les fitxes o al pipeline.
- Inclou només els detalls que ajudin a resoldre la pregunta o a entendre el seguiment.

## Revisió abans d'acceptar una conversa

Llegeix només els missatges, en veu alta si cal:

1. La pregunta inicial sona com una cosa que algú preguntaria sense haver llegit la fitxa?
2. La resposta contesta aquesta pregunta sense ajornar la informació principal?
3. El seguiment sorgeix de debò del torn anterior?
4. La conversa avança, en lloc de repetir o enumerar?
5. Cada afirmació, data, quantitat i grau de certesa es pot verificar a les fonts?
6. La resposta manté els referents clars dins del diàleg?

Si falla qualsevol punt, reescriu o descarta la conversa. Una conversa natural però imprecisa també falla.

## Procedència i separació dels fitxers

El JSONL conversacional només conté `messages` amb rols `user` i `assistant`. La procedència, els documents de suport, els drets, les decisions de revisió i la cobertura es guarden en fitxers de treball separats. Les converses amb drets desconeguts o pendents no passen a `output/`.

Una conversa de Knowledge pot sintetitzar més d'una fitxa si això resol una pregunta real. Cada conversa ha d'enllaçar amb tots els documents i fonts que sostenen la resposta.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── examples/       # calibratge editorial; mai no s'exporta
│   ├── review/         # candidates noves pendents de validació
│   ├── work/           # inventari, cobertura i notes de curació
│   ├── output/         # splits aprovats
│   └── reports/        # cobertura, qualitat, drets i exclusions
├── language/
│   ├── review/         # fragments humans pendents de verificar
│   ├── work/           # inventari, procedència i decisions
│   ├── output/         # només material humà aprovat
│   └── reports/
└── scripts/            # validació i generació, després d'acordar el format
```

## Fases

1. Mantenir el criteri editorial a `knowledge/review/EXEMPLES.md` i els exemples només com a calibratge.
2. Inventariar totes les fitxes de `docs/temes/`; després desglossar cada fitxa en unitats de contingut verificables i cobrir-les amb una o més converses.
3. Per cada conversa Knowledge, actualitzar `review/conversations.jsonl`, `review/provenance.jsonl` i la cobertura corresponent; revisar-la i fer-ne un commit i push independent.
4. Auditar totes les peces de `docs/parla/` per elegibilitat, veu, transcripció, parlant, procedència i drets; conservar material humà sense inventar diàlegs.
5. Deduplicar, revisar drets i qualitat, i crear splits agrupats per document o parlant sense filtracions.
6. Generar i validar exports només quan el contingut estigui aprovat i els drets permetin l’ús previst.

Cada entrega és petita i revisable. Abans de donar-la per tancada, validar el contingut i la procedència, revisar `git status` i el diff, i registrar el pas segons les instruccions de treball del projecte. No s'exporta cap candidat només perquè estigui escrit.

## Criteris de finalització

**Knowledge** no està acabat fins que totes les fitxes de `docs/temes/` tinguin una decisió traçable, el coneixement rellevant estigui cobert, les converses siguin naturals i correctes, els drets siguin compatibles i els splits i informes passin validació.

**Language** no està acabat fins que totes les peces de `docs/parla/` tinguin una decisió traçable, el material inclòs sigui humà, fiable i reutilitzable, i els splits i informes passin validació sense filtracions evidents.
