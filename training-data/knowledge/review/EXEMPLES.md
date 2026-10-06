# Comprovació de naturalitat per a Maia Knowledge

No és un catàleg de motlles. Serveix per detectar preguntes que només sonen
plausibles perquè hem vist la font.

## Rebutja aquestes formes

- «Què explica la secció “El relat”?» — depèn d'haver obert el document.
- «Què indica aquesta fila?» — no diu quin dubte té la persona.
- «I dos topònims que en surten:» — no és ni una pregunta completa ni una
  continuació de conversa.
- Una pregunta de qüestionari com «Quin any es va recuperar?» si apareix sense
  motiu ni context i només serveix per extreure una dada.
- Un seguiment com «Aleshores era una màscara antiga?» després que la resposta
  ja hagi dit que és centenària.
- Una situació inventada («si la meva família…») que ningú no necessita per
  entendre el fet.

Canviar dues paraules no arregla una pregunta artificial. La conversa sencera
ha de tenir un motiu recognoscible.

## Mostres editorials

Aquestes mostres il·lustren dubtes situats, seguiments útils i límits explícits.
No són frases per copiar com a plantilla. La llengua ha de variar amb el tema i
amb la manera com la persona arriba a la pregunta.

**Calendari i informació que no consta**

> —L'ossa d'Ordino no es feia per Carnaval abans? Ara la fan al desembre, oi?
>
> —Tradicionalment es representava per Carnaval. Després de recuperar-la el
> 2017, l'Última ossa d'Ordino es fa la primera setmana de desembre.
>
> —Saps per què la van passar al desembre?
>
> —La informació recollida explica quan es feia abans i quin calendari té ara,
> però no diu per què es va canviar.

La pregunta inicial resol una confusió que es pot tenir sense llegir la font.
El seguiment demana una causa diferent; la resposta no se la inventa.

**Un detall concret i una inferència que la font no permet**

> —A Ordino encara fan servir la mateixa màscara de l'ossa?
>
> —Sí. És un cap d'os dissecat, descrit com a centenari i transmès de generació
> en generació. Es va continuar fent servir després de reprendre la festa el
> 2017.
>
> —I la disfressa sencera també és tan antiga?
>
> —Això no ho sabem per aquesta descripció. Només diu que, a més de la màscara,
> s'hi fan servir pells de corders.

El seguiment és plausible, però separa l'edat de la màscara de la resta de la
disfressa. La resposta respecta aquest límit.

**Orientació pràctica amb dues festes diferents**

> —Em pensava que l'ossa només es feia a Encamp. També es conserva a Ordino?
>
> —Sí. A Ordino es conserva l'Última ossa, que es fa la primera setmana de
> desembre. A Encamp es manté el ball de l'ossa, dilluns de Carnaval.
>
> —Són dues versions diferents de la mateixa festa?
>
> —La informació les presenta com les dues manifestacions que encara perviuen
> de la tradició de l'ossa; no les descriu com la mateixa representació.

El diàleg parteix d'una confusió sobre on es conserva la tradició i aclareix la
relació entre els dos llocs sense afirmar que les representacions siguin
idèntiques. No cal afegir una pregunta sobre coreografia o personatges si la
persona no hi ha mostrat interès.

## Llista de revisió

Llegeix el diàleg sencer i pregunta't:

1. Ho podria preguntar algú que no sap com està organitzada la font?
2. Hi ha una raó clara per fer aquesta pregunta ara?
3. La resposta comença pel que la persona vol saber?
4. S'entén sense la font oberta i sense informació interna del pipeline?
5. Cada afirmació es pot rastrejar fins a l'evidència indicada?
6. La resposta diferencia el que consta del que no consta?
7. El seguiment demana alguna cosa nova que realment neix del torn anterior?
8. Ho diria així una persona? Llegeix-ho en veu alta.

Si falla una de les quatre primeres comprovacions, reescriu o descarta.
Si només falla el seguiment, acaba el diàleg abans. No hi ha una llargada
mínima ni quota de tipus de pregunta.

## Estat i ús

`conversations.jsonl` és el lot actiu en revisió; `provenance.jsonl` en registra
les fonts, l'evidència, els drets i el hash dels missatges. Cap mostra d'aquí no
és automàticament una aprovació humana ni pot passar a `output/` sense revisar
contingut, drets i condicions d'ús del model final.

Les mostres provenen de la Viquipèdia en català sota CC BY-SA 4.0. Cal conservar
l'atribució i resoldre com s'aplica l'obligació de compartir igual al conjunt
final abans de publicar-lo o utilitzar-lo.
