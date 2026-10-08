# Guia per escriure converses de Knowledge

Aquests exemples fixen el criteri editorial. Són mostres de calibratge: no compten com a cobertura i no s'exporten a l'entrenament.

## Com sona una conversa útil

Comença pel dubte que la persona voldria resoldre. No facis referència a fitxes, seccions, taules ni al procés de recerca. La resposta ha de contestar de seguida i donar el context mínim perquè s'entengui.

El seguiment ha de néixer del que s'acaba de dir i demanar una cosa nova. No el posis només per arribar a dos torns. Si la conversa no té un seguiment natural, busca una pregunta inicial més àmplia o deixa el contingut pendent.

### 1. Aclarir una classificació

```text
Usuari: La vall del Madriu és patrimoni natural o cultural?
Assistent: La UNESCO la va inscriure el 2004 com a paisatge cultural. El reconeixement destaca la relació històrica entre les comunitats de muntanya i l'aprofitament dels recursos de l'alta muntanya.
Usuari: I quines traces d'aquesta relació encara es poden veure a la vall?
Assistent: La descripció de la UNESCO esmenta cabanes d'estiu, camps en terrasses, camins de pedra i vestigis de fosa del ferro.
```

El seguiment demana exemples concrets de la idea que acaba d'aparèixer. No depèn d'haver llegit una fitxa.

### 2. Posar una dada en perspectiva

```text
Usuari: Andorra importa més béns d'Espanya o de França?
Assistent: Pel valor de les importacions de béns el 2025, d'Espanya: representava el 58% i França, el 9,9%.
Usuari: Aquesta diferència ja era tan gran als noranta?
Assistent: No. El 1997, Espanya representava el 40% del valor i França, el 29,9%; les proporcions eren força més properes.
Usuari: Aquests percentatges compten el nombre de productes?
Assistent: No: comparen el valor de les importacions, no el nombre ni el volum físic dels productes.
```

Cada resposta resol una pregunta nova. La darrera també evita que la persona interpreti malament què mesuren els percentatges.

### 3. Seguir una comparació que interessa

```text
Usuari: Quin sistema escolar té més alumnes a Andorra?
Assistent: El sistema andorrà. El curs 2023-24 tenia 4.700 alumnes, el 41,3% del total.
Usuari: I el sistema anglès, ha crescut gaire?
Assistent: Sí. Va passar de 85 alumnes el curs 2019-20 a 252 el 2023-24, tot i que encara representava un 2,2% de la matrícula.
```

La segona pregunta continua la comparació i demana una evolució, no una altra fila de la mateixa taula.

## Exemple que rebutgem

```text
Usuari: Què explica la secció «El gràfic que contradiu el text de la seva pròpia pàgina»?
Assistent: La fila del 2014 diu 57,7 per al català i 56,4 per al castellà.
```

La pregunta només té sentit per a qui té la fitxa al davant. La resposta tampoc diu què mesuren els valors. No n'hi ha prou de canviar «secció» per «gràfic»: cal descobrir quin dubte real resol la informació i comprovar que el corpus el pot respondre.

## Reescriptures de preguntes que sonen a consulta de fitxa

La informació pot ser bona i, tot i així, la pregunta no ser una cosa que preguntaria ningú. En aquests casos, no cal retocar només les paraules: cal trobar el dubte que hi ha al darrere.

### La competència per jutjar un cònsol

```text
Usuari: Si un cònsol devia diners a algú per un assumpte seu, també calia demanar permís per portar-lo davant la justícia?
Assistent: Abans de la Reforma de 1866, sí: calia autorització prèvia fins i tot pels deutes personals. Després, el permís només era necessari si el deute s’havia contret exercint el càrrec.
Usuari: I qui podia donar aquest permís?
Assistent: Per demandar un cònsol, es demanava al Síndic. Si el deute ja havia vençut i el crèdit era exigible, no podia refusar l’autorització.
```

La primera pregunta planteja un cas comprensible sense conèixer cap títol ni apartat. El seguiment demana qui intervenia, cosa que surt de la resposta anterior.

### El vocabulari dels camps comunals

```text
Usuari: Quan s’acabava la collita, els veïns podien fer pasturar els ramats als camps?
Assistent: En el vocabulari que recull Brutails el 1904, sí: els comunals eren terres d’ús comú un cop collit el blat. En aquell passatge també apareix el nom culties.
Usuari: Això vol dir que qualsevol camp es podia aprofitar així?
Assistent: No. El passatge distingeix els comunals dels camps «en defens»: en aquests, cultia era el que creixia durant el guaret i que el propietari feia menjar al seu ramat.
```

La conversa parteix d’un dubte pràctic i el seguiment aclareix el límit de la resposta. Els termes històrics s’expliquen perquè siguin comprensibles, no es converteixen en la pregunta.

### La llegenda de Meritxell

```text
Usuari: Per què la Mare de Déu de Meritxell és a Meritxell si primer la van portar a Canillo?
Assistent: Segons la llegenda, la imatge va desaparèixer de l’altar de Canillo i va tornar a aparèixer al peu de la gavernera florida on l’havien trobada.
Usuari: Ho van tornar a provar en un altre lloc?
Assistent: Sí. També la van dur a Encamp, però la imatge va tornar al lloc de la troballa. Els veïns van interpretar que volia quedar-s’hi i hi van construir una capella.
```

La pregunta s’entén per si sola i la resposta marca explícitament que es tracta d’una llegenda. El seguiment continua la seqüència del relat sense demanar que es reciti una secció.

### Un gràfic sobre llengües

```text
Usuari: A les enquestes sociolingüístiques, el català va quedar per davant del castellà totes les vegades?
Assistent: No. En la sèrie de 1995 a 2018, el català només va quedar per davant el 1995 i el 2014. El 2014 els valors eren 57,7 per al català i 56,4 per al castellà.
Usuari: Quan va quedar més enrere?
Assistent: El 2004: el valor del castellà superava el del català per 12,3 punts.
```

La pregunta inicial demana una comparació que una persona podria tenir en llegir notícies sobre l’ús de les llengües. El seguiment aprofundeix en la mateixa comparació. Abans d’aprovar-la, cal deixar clar al registre de procedència quin indicador concret representen aquests valors.

## Estructura de cada registre nou

Un registre de revisió inclou, en aquest ordre lògic:

1. **Intenció**: quin dubte real resol, en una frase interna i no visible a l’entrenament.
2. **Conversa completa**: missatges alternats `user` i `assistant`; cada resposta funciona també si el lector no veu cap font.
3. **Evidència i límits**: documents i passatges que sostenen les respostes, amb les cauteles necessàries.
4. **Drets i atribució**: llicència i procedència de cada font abans d’incloure’n contingut.
5. **Revisió**: estat i motiu; no s’aprova per defecte una conversa antiga ni una conversa que només arriba a dos torns.

El JSONL de revisió pot contenir camps editorials i de procedència. L’export d’entrenament conserva només `messages`. Una conversa té com a mínim dos intercanvis complets, però es descarta si el seguiment no és natural; la llargada no és una quota.

## Revisió abans d'aprovar

- Entendria la pregunta una persona que no coneix el corpus?
- La primera resposta resol el dubte encara que la conversa s'acabi aquí?
- El seguiment surt de la resposta anterior i demana informació nova?
- Els referents són clars sense haver de veure una fitxa?
- Les xifres indiquen què mesuren i de quin període són?
- Cada afirmació és sostinguda per una font reutilitzable?
- El diàleg sona natural llegit en veu alta?

Un sol «no» vol dir reescriure o deixar el registre pendent. La cobertura no justifica un seguiment artificial.
