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

## Revisió abans d'aprovar

- Entendria la pregunta una persona que no coneix el corpus?
- La primera resposta resol el dubte encara que la conversa s'acabi aquí?
- El seguiment surt de la resposta anterior i demana informació nova?
- Els referents són clars sense haver de veure una fitxa?
- Les xifres indiquen què mesuren i de quin període són?
- Cada afirmació és sostinguda per una font reutilitzable?
- El diàleg sona natural llegit en veu alta?

Un sol «no» vol dir reescriure o deixar el registre pendent. La cobertura no justifica un seguiment artificial.
