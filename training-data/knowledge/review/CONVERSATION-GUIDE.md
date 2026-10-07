# Guia per escriure converses Knowledge

## Comença per la persona, no per la fitxa

Abans de redactar, acaba aquesta frase: **«Algú preguntaria això perquè vol...»**. La resposta ha de descriure una intenció recognoscible: aclarir una confusió, entendre un costum, comprovar una dada, comparar dues coses o recordar un relat.

Si l'única motivació és «aquesta informació surt al document», no hi ha encara una bona pregunta. Busca una altra manera de plantejar el dubte o deixa el contingut fora del pilot.

## Preguntes que s'han de descartar

Descarta o reescriu preguntes que:

- demanen què diu una fitxa, una secció, una taula o una fila;
- fan servir «això», «aquesta fila» o «el gràfic» sense donar context suficient;
- exigeixen conèixer una dada que només apareix en un document que l'usuari no ha esmentat;
- són fragments, com «I dos topònims que en surten»;
- semblen un encàrrec de recollir dades («digues tres coses»), sense una necessitat al darrere;
- afegeixen una família, un viatge, una feina o una experiència fictícia per teatralitzar la consulta;
- repeteixen la mateixa pregunta amb paraules diferents.

No cal que totes les consultes siguin col·loquials. Han de sonar com una persona que busca una resposta, no com algú que està anotant l'estructura d'un article.

## Conversa multitorn

- La primera pregunta estableix el tema i el dubte amb prou context per entendre-la sola.
- La primera resposta resol el dubte principal.
- El seguiment reprèn una idea que acaba d'aparèixer: en demana una precisió, comprova una conseqüència o aclareix una confusió nova.
- La resposta següent afegeix informació pertinent; no repeteix la resposta anterior amb altres paraules.
- Acaba quan la persona ja té la resposta. No hi ha un nombre obligatori de torns.

**Prova de fil:** llegeix només els missatges de l'usuari, un darrere l'altre. Si el seguiment podria anar igualment després de qualsevol conversa, és massa genèric. Si canvia de tema, separa'l en un altre registre.

## Respostes

- Respon primer la pregunta concreta.
- Escriu en llenguatge clar i conversacional. Evita etiquetes com «Segons la secció X», «el corpus afirma» o «tres coses» quan la persona no ha demanat una anàlisi documental.
- Afegeix context només si ajuda a comprendre la resposta o evita una conclusió errònia.
- Atribueix llegendes i interpretacions («segons la llegenda», «la font ho presenta com...»).
- Davant d'una contradicció, indica quina dada sosté cada font i si hi ha una font que la resol.
- Davant d'un buit, digues què no es pot concloure. No omplis el buit amb una hipòtesi.
- Marca quan una dada és històrica i quan la seva vigència actual no s'ha comprovat.

## Revisió final

Una conversa passa el filtre només si totes aquestes respostes són sí:

1. S'entén sense veure la fitxa?
2. És creïble que algú ho pregunti així?
3. La resposta resol el dubte, sense afegir detalls que no fan falta?
4. Cada seguiment neix del torn anterior?
5. Cada afirmació factual es pot rastrejar a una font registrada?
6. Els drets de les fonts estan registrats i són compatibles amb l'ús previst?
7. La conversa és prou diferent de les ja aprovades?

Un «no» implica reescriure o descartar, no rebaixar el criteri.

## Què va passar amb el pilot anterior

Els primers candidats es van escriure com si l'usuari tingués una fitxa oberta. S'han apartat de la cua activa i es conserven a `archive/initial-pilot-2026-10-07/` per consultar-ne la procedència. No compten com a registres aprovats ni com a cobertura. Els exemples nous d'`EXEMPLES.md` són només calibratge fins que el criteri s'hagi validat.

## Format

Les converses candidates són JSONL, una conversa per línia. El camp `messages` només conté missatges `user` i `assistant`. La procedència, els drets, les notes de revisió i l'estat d'aprovació van en `provenance.jsonl`, mai dins del text de conversa.
