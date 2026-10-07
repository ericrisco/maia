# Exemples de conversa: criteri de naturalitat

Els registres antics sovint preguntaven pel nom d'una secció, una fila o un
fragment de fitxa. Això només ho preguntaria algú que estigués fent un examen
sobre el document. Una conversa de training ha de començar pel dubte que el
contingut ajuda a resoldre.

Els exemples d'aquí són mostres inicials aprovades per calibrar el criteri. La
procedència i els límits de les afirmacions són a `provenance.jsonl`.

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

## Prova final

Llegeix només els missatges, sense veure la fitxa font. Si no s'entén què vol
saber l'usuari, si la conversa sona com una tasca d'extracció o si algun torn
només hi és per fer-la més llarga, reescriu-la.
