# Exemples de conversa per a Maia Knowledge

Els tres primers exemples són registres aprovats de [`records.jsonl`](records.jsonl) i apareixen a l'export `conversations.jsonl`. La guia també inclou exemples rebutjats per aclarir què no s'ha d'afegir.

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
