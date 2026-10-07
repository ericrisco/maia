# Exemples de conversa per a Maia Knowledge

Els tres primers exemples són registres aprovats de [`records.jsonl`](records.jsonl) i apareixen a l'export `conversations.jsonl`. Cada conversa de Knowledge aprovada ha de tenir almenys dues preguntes d'usuari. El segon dubte ha de néixer del primer i demanar informació nova; no es divideix una resposta en fragments per forçar el multitorn.

## Llindar d'aprovació: conversa humana, no exercici sobre la fitxa

Abans d'aprovar una conversa, aplica aquestes cinc comprovacions:

1. **Pregunta d'entrada:** algú que no ha llegit el corpus podria preguntar això per entendre o resoldre una curiositat real?
2. **Primera resposta:** contesta el dubte inicial de seguida i s'entén sense obrir la font.
3. **Motiu del seguiment:** després de la resposta, es pot explicar en una frase per què aquella mateixa persona voldria saber el següent?
4. **Valor nou:** el seguiment obté una dada, matís, conseqüència o comparació que no s'ha donat ja.
5. **Font i límits:** cada afirmació està sostinguda; una interpretació, llegenda o incertesa no es presenta com un fet comprovat.

Si falla una comprovació, es reescriu o es descarta. «Així és multitorn» i «així cobrim una unitat» no justifiquen un seguiment artificial.

## Com reformulem les preguntes artificials

La font pot orientar la resposta, però no ha de dictar la veu de l'usuari. Aquests exemples mostren el canvi d'intenció; abans d'aprovar-los com a registres, cal associar-hi unitats de cobertura i procedència revisada.

### De «què explica la secció» a un dubte sobre el cas

```text
Usuari: Si un cònsol et devia diners, el podies portar davant d'un jutge?
Assistent: Depenia de quan i de quin tipus de deute. Abans de la Reforma de 1866, qualsevol demanda civil contra una autoritat requeria autorització prèvia, fins i tot per un deute personal. Després, el permís només calia per reclamar deutes contrets en exercici del càrrec.
Usuari: I si l'acusaves d'un delicte?
Assistent: Per a una persecució criminal no calia aquella autorització. La protecció especial afectava les demandes civils.
```

La pregunta no demana que l'assistent expliqui una regla titulada per l'editor. El seguiment explora la distinció important entre les vies civil i criminal.

### De «què indica aquesta fila» a aclarir una contradicció

```text
Usuari: En l'enquesta d'usos lingüístics del 2018, el gràfic i el text semblen intercanviar les xifres del català i del castellà. Quina dada és la bona?
Assistent: El text coincideix amb la sèrie de l'Estadística: el 2018 l'indicador és 56,8 per al català i 57,6 per al castellà. El gràfic etiqueta les dues xifres al revés.
Usuari: El gràfic també s'equivoca amb les dades del 2014?
Assistent: No en aquell punt: el 2014 la sèrie dona 57,7 per al català i 56,4 per al castellà. La discrepància documentada és la inversió dels valors del 2018 al gràfic.
```

El diàleg posa nom al fenomen i a la pregunta real: quina versió cal prendre per bona. La dada prové de l'API estadística i no reprodueix text de l'informe.

### De la contradicció aparent a la diferència entre contractes

```text
Usuari: Com s'explica que alguns préstecs fossin al 3,33% i d'altres al 5%?
Assistent: No era el mateix tipus de contracte: el 3,33% corresponia als censals i el 5% s'acceptava per a la resta de préstecs.
Usuari: I el tipus dels censals encara era el mateix el 1895?
Assistent: Sí. El decret del 1895 diu que el tipus dels censals continuava essent el que establia la llei de la Vall, mentre que per a la resta s'acceptava el 5%.
```

El seguiment comprova la conseqüència temporal de la resposta i no torna a preguntar què vol dir cada percentatge. No cal esmentar el nom de la fitxa ni copiar l'encapçalament de la font.

## 1. Entendre una paraula i la funció que descriu

```text
Usuari: Què és un estripagec?
Assistent: És un barrot metàl·lic amb punxes irregulars als costats, que es posava a les finestres de cases i bordes. Si un lladre hi passava el braç, les punxes li podien estripar el gec, és a dir, la jaqueta. D'aquí ve el nom.
Usuari: Se'n troben només a Andorra o també en altres llocs?
Assistent: No. N'hi ha al Pirineu i també en altres indrets, com el Ripollès, Osona i el Vallès.
```

La primera resposta resol què és i per què té aquest nom. El seguiment amplia l'abast geogràfic; no demana que es repeteixi la definició.

## 2. Entendre per què les pintures són fora de l'església

```text
Usuari: Per què les pintures de Santa Coloma no són totes dins l'església?
Assistent: Les van despenjar el 1932 i les van portar a Barcelona per restaurar-les. Després van passar per diverses col·leccions; el Govern d'Andorra les va adquirir el 2007 i avui el gruix s'exposa a l'Espai Columba.
Usuari: I a l'església no n'hi queda cap?
Assistent: Sí que n'hi queda un fragment: l'Anyell de Déu continua al seu lloc. Dels fragments de sants, sant Silvestre és a l'Amherst College i no se sap on és sant Gregori després de la subhasta de 1955.
```

El seguiment pregunta per una conseqüència natural de la primera resposta. La conversa distingeix el gruix de les pintures dels fragments que van seguir altres camins.

## 3. Aclarir dues parts d'una llegenda

```text
Usuari: Els minairons neixen de l'herba menaironera?
Assistent: Algunes versions de la llegenda diuen que sí: l'herba floreix i grana per Sant Joan.
Usuari: I què passa si algú obre el canó on els guarda?
Assistent: La llegenda diu que en surten milers demanant feina. Si l'amo no els en mana, el maten.
```

El seguiment continua la història amb una conseqüència del relat. La resposta manté explícit que són fets llegendaris.

## Exemples que rebutgem

```text
Usuari: Què explica la secció «El relat» de la fitxa «La troballa de Meritxell»?
Assistent: Se la va endur a Canillo i la va posar sobre l'altar major.
```

La pregunta parla de la fitxa, i la resposta comença a mitja història. Cal formular el dubte que tindria una persona i donar-hi context; si no es pot fer sense inventar-lo, no es crea el registre.

```text
Usuari: Què indica aquesta fila?
Assistent: 2014: verd 57,7; morat 56,4.
```

Sense saber quin gràfic mira, la persona no pot entendre la pregunta ni la resposta. No es converteix una fila descontextualitzada en conversa.

```text
Usuari: Què és un estripagec?
Assistent: És un barrot amb punxes.
Usuari: I on n'hi ha?
Assistent: Al Pirineu.
Usuari: I què vol dir el nom?
Assistent: Estripar jaquetes.
```

La resposta inicial hauria d'incloure la funció principal. No dividim una explicació curta en torns artificials només per fer-la multitorn.

## Checklist abans d'afegir un registre

- La pregunta inicial sembla una cosa que algú preguntaria sense haver vist la font?
- Queda clar de qui o de què parla cada torn?
- Cada resposta contesta la pregunta completa i s'entén si el diàleg s'acaba allí?
- Cada seguiment demana informació nova que probablement sorgeix del torn anterior?
- El diàleg sona natural llegit en veu alta?
- Les respostes separen fets, llegendes, interpretacions i incerteses?
- La procedència del mateix registre sosté totes les afirmacions i permet reutilitzar-les?
- Si la conversa no necessita seguiment, s'ha deixat en un sol intercanvi?
