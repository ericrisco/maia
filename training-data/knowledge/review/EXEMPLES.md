# Criteri i mostres de Maia Knowledge

Una conversa ha de començar amb una necessitat que una persona pugui tenir sense haver llegit cap fitxa. No cal convertir cada document o cada dada en una pregunta. Es pot deixar coneixement sense pregunta quan no hi ha una manera natural d'arribar-hi.

## Mostra: anar a veure una tradició

```json
{"messages":[{"role":"user","content":"Per veure la Passa de Sant Julià, quin dia de la festa major he d'anar-hi?"},{"role":"assistant","content":"Se celebra al migdia del dilluns de la festa major, pels carrers principals de Sant Julià de Lòria."},{"role":"user","content":"I qui va al davant de la cercavila?"},{"role":"assistant","content":"Les parelles que s'han de casar aquell any, anomenades «majors fadrins». Darrere seu desfilen les altres parelles, de més grans a més joves."}]}
```

La primera pregunta té una raó pràctica i es pot entendre sense saber què conté la fitxa. El seguiment reprèn la cercavila que acaba d'esmentar l'assistent i demana un detall concret. La resposta no deixa el lloc ni l'hora per al torn següent.

## Mostra: distingir l'original de la rèplica

```json
{"messages":[{"role":"user","content":"La imatge que es venera ara al santuari de Meritxell és l'original medieval?"},{"role":"assistant","content":"No. La talla de fusta del segle XII es va perdre en l'incendi del santuari la nit del 8 al 9 de setembre de 1972. La imatge actual és una rèplica de l'escultor Sergi Mas."},{"role":"user","content":"I quan es va obrir el santuari nou?"},{"role":"assistant","content":"El santuari nou, projectat per Ricard Bofill, es va inaugurar el 1976."}]}
```

La primera pregunta neix d'una confusió comprensible entre la imatge venerada avui i la talla històrica. El seguiment demana què va passar amb el santuari després del mateix incendi; no canvia de tema ni obliga l'assistent a reservar informació important.

## Mostra: separar una llegenda d'una data comprovada

```json
{"messages":[{"role":"user","content":"Com explica la llegenda que es va triar el lloc del santuari de Meritxell?"},{"role":"assistant","content":"Segons la llegenda, un pastor va trobar una imatge sota una gavernera florida el dia de Reis. La imatge tornava al mateix indret després que la portessin a Canillo i a Encamp; els veïns ho van entendre com un senyal que volia quedar-s'hi."},{"role":"user","content":"Se sap quan es va començar a explicar aquesta història?"},{"role":"assistant","content":"No se'n pot datar l'origen amb les fonts consultades: no s'hi ha localitzat la primera documentació ni la font primària del santuari que permetrien saber quan va començar a circular."}]}
```

La resposta inicial marca el relat com a llegenda. El seguiment pregunta per l'antiguitat de la història, però la resposta no inventa una data ni tracta el relat com un fet comprovat.

## Mostra: comparar pintures sense atribuir-les a la mateixa persona

```json
{"messages":[{"role":"user","content":"Les pintures murals de Sant Martí de la Cortinada tenen alguna cosa en comú amb les de Santa Coloma?"},{"role":"assistant","content":"Sí. Les pintures de Sant Martí, de finals del segle XII, reprenen alguns motius decoratius de Santa Coloma i de Sant Joan de Caselles, però també introdueixen canvis estilístics importants. S'atribueixen al Mestre de la Cortinada."},{"role":"user","content":"Això vol dir que el mateix pintor va treballar a Santa Coloma?"},{"role":"assistant","content":"No es pot deduir que fos el mateix pintor només pels motius compartits. L'atribució de Sant Martí és al Mestre de la Cortinada; les fonts consultades no atribueixen a aquesta mateixa mà les pintures de Santa Coloma."}]}
```

La pregunta compara dues obres conegudes pel seu lloc. El seguiment explora una conclusió possible, i la resposta separa la semblança dels motius de l'autoria que es pot atribuir.

## Regles per revisar cada conversa

- Llegeix els missatges sense títol, ID ni font. Si la pregunta només té sentit amb la fitxa al davant, reescriu-la o descarta-la.
- Evita que l'usuari esmenti seccions, gràfics, files, IDs o «el corpus».
- No facis servir una dada obscura a la pregunta si la persona podria descriure el dubte amb paraules normals.
- Dona context pràctic només quan expliqui de debò per què es pregunta; no inventis biografies ni escenes teatrals.
- Cada resposta ha de resoldre el torn per si sola, amb el context just i els límits que indiquen les fonts.
- En aquesta tanda cada conversa té dues parelles user-assistant. El seguiment ha de néixer d'una idea concreta de la resposta i aportar informació nova. Si no surt naturalment, descarta el fil; no el forcis per arribar a dos torns.
- Revisa cada afirmació contra la font. Distingeix fets, llegendes, interpretacions i dades que no consten.
- Registra fitxes, hashes i drets a `../work/provenance.jsonl`, fora de `messages`. No copiïs una mostra a `output/` sense aprovació de contingut i drets.

## Formulacions que no passen

- «Què explica la secció “El relat” de la fitxa de Meritxell?» — demana conèixer l'estructura interna.
- «Què indica aquesta fila?» — no té context ni diu quin dubte vol resoldre.
- «Quina frase surt al document?» — demana recuperar el text en lloc d'ajudar a entendre Andorra.
- Afegir «he trobat dues versions» o «hi vaig anar amb la família» només per fer veure que la pregunta és natural, si aquesta situació no és necessària.
- Afegir un seguiment d'un tema diferent només per complir el nombre de torns.

La cobertura dels documents es controla per separat: no és motiu per aprovar una pregunta artificial. Consulta també el [pla editorial](../../PLAN.md).
