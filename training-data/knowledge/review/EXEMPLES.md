# Exemples de conversa: criteri de naturalitat

> Estat: guia de revisió. Els exemples no validen automàticament les 54
> converses existents. L'estructura i els drets passen un validador; la
> naturalitat encara requereix lectura humana.

Els registres antics sovint preguntaven pel nom d'una secció, una fila o un
fragment de fitxa. Això només ho preguntaria algú que estigués fent un examen
sobre el document. Una conversa de training ha de començar pel dubte que el
contingut ajuda a resoldre.

Els exemples següents mostren formes possibles de conversa. Les afirmacions
aprovades en registres concrets tenen la seva procedència i els seus límits a
`provenance.jsonl`.

Una conversa pot tenir un sol intercanvi. «Multitorn» vol dir conservar els
seguiments que una persona faria, no afegir seguiments a cada registre.

## La Dama Blanca i el llop

```json
{"messages":[{"role":"user","content":"A l'escultura de la Dama Blanca d'Aubinyà també hi surt un llop. Quin paper té en la llegenda?"},{"role":"assistant","content":"L'escultura metàl·lica de Toni Cruz la mostra amb un llop; també se l'anomena Dama Blanca d'Andorra. En la llegenda, després que desaparegui el bisbe d'Urgell, un llop negre comença a sembrar la mort i el terror; un síndic el caça. Però després té malsons i embogeix: el relat diu que el llop duia dins seu l'ànima negra del bisbe."},{"role":"user","content":"Així que el llop és el bisbe, d'alguna manera?"},{"role":"assistant","content":"Dins la llegenda, sí: el llop conté l'ànima del bisbe. És part del relat llegendari, no una afirmació sobre un fet històric."},{"role":"user","content":"I la Dama pot salvar el síndic, quan comença a embogir?"},{"role":"assistant","content":"No. Els ciutadans li demanen ajuda, però no el pot guarir i el síndic acaba morint. Després, el llop i el bisbe deixen de manifestar-se. Per això el relat no acaba amb una victòria neta: també mostra el cost de plantar cara al poder."}]}
```

**Per què funciona:** la pregunta sorgeix d'un element visible de l'escultura;
els dos seguiments neixen del relat: primer aclareixen qui és el llop i després
pregunten pel destí del síndic. L'assistent marca que es tracta d'una llegenda.

## Ficció televisiva i història

```json
{"messages":[{"role":"user","content":"La minisèrie «Andorra, entre el torb i la Gestapo» és fidel als fets o s'inventa part de la història?"},{"role":"assistant","content":"És una ficció basada en fets reals i en el llibre autobiogràfic de Francesc Viadiu. La trama dramatitza una xarxa d'evasió per Andorra que ajuda aviadors britànics ferits i perseguits per la Gestapo."},{"role":"user","content":"Aleshores, per explicar què va passar de debò, em puc basar només en la minisèrie?"},{"role":"assistant","content":"No. La pots fer servir per parlar de com la sèrie explica aquests fets, però no per provar que cada escena va passar tal com es veu. Per explicar la història, cal contrastar-ne la trama amb fonts documentals."}]}
```

**Per què funciona:** la primera resposta separa l'origen autobiogràfic de la
dramatització. El seguiment pregunta per una conseqüència concreta i rep un
límit d'evidència clar.

## Patrons que cal rebutjar

```text
Què explica la secció «El relat» de la fitxa «La troballa de Meritxell»?
Què indica aquesta fila?
Quina resposta dona el segon paràgraf?
La baixada és igual a totes les edats? I als joves? I a la gent gran?
```

Les primeres preguntes depenen del document o semblen un qüestionari. L'última
encadena subpreguntes sense deixar que la resposta anterior motivi el torn
següent.

També cal revisar una conversa que sona plausible però repeteix sempre el mateix
motlle: pregunta inicial, resposta llarga, pregunta de confirmació i resposta
que reformula l'anterior. Si el seguiment no demana una aclaració concreta ni
obre una conseqüència útil, elimina'l.

## Una consulta concreta pot ser d'un sol torn

```json
{"messages":[{"role":"user","content":"On puc veure alguna obra de Josep Viladomat a Barcelona?"},{"role":"assistant","content":"En pots veure, per exemple, a la plaça de Catalunya (*Dona amb nen i flabiol*), a la Casa de la Ciutat (*Maternitat*) i als jardins de Joan Maragall (*Dos Tritons*)."}]}
```

**Per què funciona:** parteix d'un pla plausible —voler veure obres a la ciutat—
i resol la petició en un torn. No cal inventar un seguiment.

## Un seguiment ha de néixer de la resposta

```json
{"messages":[{"role":"user","content":"Vull veure alguna obra de Josep Viladomat a Barcelona. Quines em recomanes?"},{"role":"assistant","content":"Pots començar per *Dona amb nen i flabiol*, a la plaça de Catalunya; *Maternitat*, a la Casa de la Ciutat; o *Dos Tritons*, als jardins de Joan Maragall."},{"role":"user","content":"I *La Puntaire* també és a Barcelona?"},{"role":"assistant","content":"Sí. *La Puntaire*, del 1972, és al parc de Montjuïc, també a Barcelona."}]}
```

**Per què funciona:** el seguiment pregunta per una obra concreta després que
l'assistent n'hagi situat d'altres a Barcelona. Si no hi hagués aquest interès
nou, la conversa podria acabar després de la primera resposta.

## Prova final

Llegeix només els missatges, sense veure la fitxa font. Si no s'entén què vol
saber l'usuari, si la conversa sona com una tasca d'extracció o si algun torn
només hi és per fer-la més llarga, reescriu-la.
