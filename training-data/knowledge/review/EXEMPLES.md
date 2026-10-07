# Exemples per calibrar converses Knowledge

Aquests exemples defineixen el to i el ritme. **No són registres d'entrenament** i no compten per a la cobertura. La procedència és aquí per facilitar la revisió; al dataset només hi entren missatges `user` i `assistant`.

## Buscar una festa major per a una escapada

**Usuari:** Volem venir a Andorra a l'estiu i ens faria gràcia coincidir amb una festa major. N'hi ha una de tot el país o cada parròquia va a la seva?

**Maia:** Cada parròquia té la seva festa major, i en moltes també en fan les viles. Per això no hi ha una sola data de «la festa major d'Andorra»; cal saber a quina parròquia o poble voleu anar.

**Usuari:** Encara no ho sabem. Si venim a finals de juny, ja n'enganxarem alguna?

**Maia:** Les festes majors que recull el corpus són a l'estiu, però no hi consten les dates concretes de cada parròquia. A finals de juny sí que hi ha Sant Joan i les falles, el dia 23.

*Per què funciona:* la persona planifica un viatge. La segona pregunta surt de la finestra de dates i rep una resposta útil sense inventar un programa actual.

*Fonts per contrastar:* `docs/temes/costums/calendari-festiu/calendari-festiu.md` i `docs/temes/costums/falles/falles.md`.

## Distingir la Passa dels balls

**Usuari:** Al programa de Sant Julià hi ha la Passa, el Cerdà i la Marratxa. M'han dit que són tres balls, però em sembla que la Passa és diferent. Ho recordo bé?

**Maia:** Sí. El Cerdà i la Marratxa són balls; la Passa és una cercavila de parelles de fadrins pels carrers de Sant Julià.

**Usuari:** I qui va al davant?

**Maia:** Les parelles que es casaran aquell any. La resta les segueix ordenada de més grans a més joves.

**Usuari:** Ah, doncs no és només una cercavila festiva.

**Maia:** Exacte: l'ordre fa visible qui es casa aquell any i com es distribueixen les altres parelles per edat. La fitxa no explica com es formen les parelles ni què passa si algú no en té.

*Per què funciona:* parteix d'una confusió plausible en mirar un programa. El seguiment aprofundeix en el detall que la resposta acaba de donar i marca un límit real de la informació.

*Fonts per contrastar:* `docs/temes/costums/ritus-de-pas/la-passa.md`, `docs/temes/costums/danses/el-ball-del-cerda.md` i `docs/temes/costums/danses/la-marratxa.md`.

## Explicar la llegenda sense presentar-la com un fet

**Usuari:** A Meritxell hi ha una història d'una imatge que tornava al mateix lloc, oi? No n'acabo de recordar els detalls.

**Maia:** Segons la llegenda, un pastor va trobar la imatge sota una gavernera florida el dia de Reis. La van dur a Canillo i després la van tancar a Encamp, però totes dues vegades hauria tornat al lloc de la troballa.

**Usuari:** I així és com expliquen que el santuari quedés just allà?

**Maia:** Sí. Dins del relat, els veïns van entendre que la imatge volia quedar-se en aquell lloc i hi van construir el santuari. La fitxa explica aquesta tradició, però no n'estableix una datació històrica.

*Per què funciona:* la persona vol recordar un relat conegut. La resposta l'explica amb atribució clara i no converteix la llegenda en una afirmació històrica.

*Font per contrastar:* `docs/temes/cultura/llegendes/la-troballa-de-meritxell.md`.

## No confondre un calendari judicial amb les festes populars

**Usuari:** Estic mirant un document de 1902 sobre els dies que tancaven els tribunals. No hi surt Sant Antoni. Això vol dir que no el celebraven?

**Maia:** No. El document recull els dies en què s'aturava l'activitat judicial; no és un calendari de festes populars. Que no hi aparegui Sant Antoni només vol dir que aquella llista no el recull.

**Usuari:** Llavors, per què m'han dit que és una font important per estudiar les festes?

**Maia:** Serveix per saber quines celebracions tenien efecte en el calendari dels tribunals. També permet veure que no s'ha de prendre una llista institucional com si descrivís totes les celebracions del país.

*Per què funciona:* és un dubte plausible de qui consulta un document històric. La conversa evita deduir que una pràctica no existia perquè una font amb un altre propòsit no l'esmenta.

*Fonts per contrastar:* `docs/temes/costums/calendari-festiu/calendari-festiu.md` i `docs/temes/institucions/justicia/els-tribunals-tancaven-per-la-fira-dorganya.md`.

## Exemples que no s'han de generar

| Pregunta | Problema | Reescriptura necessària |
| --- | --- | --- |
| «Què explica la secció “El relat”?» | Només té sentit amb la fitxa al davant. | Preguntar pel dubte que el relat genera a una persona. |
| «Què indica aquesta fila?» | No diu què està comprovant l'usuari. | Afegir un context plausible o descartar-la. |
| «Digues dos topònims i tres dates.» | És una ordre d'extracció, no una conversa. | No convertir una llista en preguntes si no hi ha una necessitat real. |
| «I què més? I quan? I qui?» | No hi ha continuïtat clara; només s'allarga el registre. | Fer una pregunta cada vegada i seguir la resposta anterior. |
| «Què diu la fitxa sobre la festa?» | Entrena a parlar del corpus, no a resoldre el dubte. | Preguntar directament per la festa o per la decisió que la persona vol prendre. |

## Forma d'exportació

Les notes editorials, els títols i les fonts no s'exporten. Una conversa aprovada queda així:

```json
{"messages":[{"role":"user","content":"Al programa de Sant Julià hi ha la Passa, el Cerdà i la Marratxa. M'han dit que són tres balls, però em sembla que la Passa és diferent. Ho recordo bé?"},{"role":"assistant","content":"Sí. El Cerdà i la Marratxa són balls; la Passa és una cercavila de parelles de fadrins pels carrers de Sant Julià."},{"role":"user","content":"I qui va al davant?"},{"role":"assistant","content":"Les parelles que es casaran aquell any. La resta les segueix ordenada de més grans a més joves."}]}
```
