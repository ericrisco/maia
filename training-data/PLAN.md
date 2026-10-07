# Pla de disseny de converses de Maia Knowledge

## Objectiu

Crear converses que ensenyin Maia a entendre dubtes normals sobre Andorra,
respondre'ls amb precisió i seguir el fil. El contingut factual surt de
`docs/temes/`. La conversa ha de tenir sentit per si sola: qui la llegeix no
ha de conèixer les fitxes ni els seus títols.

`Maia Language` continua separat. Només s'hi poden posar intervencions humanes
autèntiques i autoritzades de `docs/parla/`; no s'hi inventen entrevistes.

## Què va fallar

Aquestes formes no són preguntes útils d'un usuari:

- «Què explica la secció X de la fitxa Y?» demana un resum de l'índex.
- «Què indica aquesta fila?» assenyala material que no és a la conversa.
- «I dos topònims que en surten:» no és ni una pregunta clara ni una resposta.
- Reproduir una taula amb guions trasllada dades sense explicar què volen dir.

No n'hi ha prou de canviar-ne les paraules. Cal trobar primer el dubte que una
persona voldria resoldre.

## Mètode editorial

### 1. Entendre el material abans d'escriure

Llegeix la fitxa sencera i les fitxes enllaçades que siguin necessàries. Apunta
en una targeta interna:

- què vol aclarir la conversa;
- quins fets concrets poden respondre-ho;
- quines fonts sostenen cada fet i si permeten reutilitzar-lo;
- què no se sap o quina interpretació seria excessiva.

No comencis per una fila, un encapçalament o una dada a la qual l'usuari no té
accés. La fitxa és la font de l'assistent, no el context compartit del diàleg.

### 2. Escriure la pregunta inicial des d'una intenció

Abans de redactar-la, completa per a ús editorial: «Aquesta persona vol saber
___ perquè ___». La resposta ha de poder omplir el primer buit amb una
necessitat concreta, com ara:

- entendre si dues coses són iguals o diferents;
- saber quan o on passa una cosa;
- comprovar una impressió o una premissa;
- entendre què vol dir una pràctica o una paraula;
- saber què es pot concloure d'una dada.

Després expressa aquesta intenció en català corrent. Es permet una mica de
context («Em pensava que...», «Quan hi anem...») si ajuda a entendre el dubte,
però no inventis una biografia, una experiència personal ni una conversa prèvia.
No facis servir «segons la fitxa», «en aquesta taula» o «a l'apartat».

### 3. Construir el seguiment a partir de la resposta

Escriu primer la resposta. A continuació, formula la pregunta que aquella
resposta faria venir al cap: aclarir una excepció, comprovar una conseqüència,
demanar el motiu o seguir un detall que acaba d'aparèixer. Si el seguiment no
depèn d'alguna cosa que l'assistent acaba de dir, no és un bon seguiment.

Fes normalment 2 o 3 intercanvis. No allarguis el diàleg per complir una quota.
Una sola pregunta pot ser millor que una conversa forçada; però quan la tasca
demana multitorn, cada torn ha d'afegir una necessitat real i no repetir la
resposta anterior amb altres paraules.

### 4. Respondre com en una conversa

- Contesta la pregunta concreta a la primera frase.
- Usa frases completes, amb prou context perquè s'entenguin sense la font.
- Explica què representen les dates, xifres i noms; no els deixis com una llista.
- Corregeix una premissa amb tacte i dona la versió que sí que se sosté.
- Separa el fet documentat de la inferència. Digues què no consta quan calgui.
- Afegeix context només si ajuda a resoldre el dubte o entendre'n el límit.
- Evita l'obertura buida («Bona pregunta!»), el to d'examen i la prosa de fitxa.

### 5. Revisar el diàleg sense mirar la font

Llegeix només els missatges, en veu alta. Rebutja'l si:

- no s'entén què vol saber la persona;
- sembla que l'usuari conegui la fitxa o una dada no dita abans;
- el seguiment es podria enganxar a qualsevol conversa;
- una resposta comença amb una llista o amb una frase inacabada;
- el diàleg sona com un qüestionari, un guió promocional o una entrevista
  escrita per omplir torns.

Després comprova de nou cada afirmació contra les fonts i els seus drets.

## Targeta de treball i registre

La targeta de treball és editorial i no s'exporta:

```text
Intenció de l'usuari:
Situació mínima necessària:
Fets que responen el dubte:
Límit / què no consta:
Fonts i drets:
Possible seguiment que neix de la resposta:
```

El registre revisat conserva identificador, fonts, drets, revisió i split als
fitxers interns. El JSONL d'entrenament conté només `messages`, amb rols
alternats `user` i `assistant`, sense cap metadada interna.

## Criteris de calibratge

Puntua cada aspecte de 0 a 2: intenció recognoscible, naturalitat, continuïtat
entre torns, resposta completa i fidelitat a les fonts. Cal obtenir 9/10 o més,
cap zero, i passar totes dues lectures: primer només el diàleg; després amb les
fonts obertes. La puntuació no substitueix el judici editorial.

## Estructura i ordre de treball

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── review/       # exemples, candidats i procedència
│   ├── work/         # targetes, inventari i cobertura
│   ├── output/       # converses aprovades, només missatges
│   ├── reports/      # cobertura, qualitat, drets i splits
│   ├── scripts/      # exportació i validació
│   └── archive/      # lots antics, preservats i exclosos
└── language/         # flux separat basat en parla humana autoritzada
```

Per a cada lot: tria un tema, revisa les fonts i els drets, escriu poques
converses, aplica la lectura editorial, comprova duplicats i cobertura, i només
llavors aprova i exporta. No generis una pregunta per paràgraf o per fila. Anota
els fets sense una pregunta natural a la cobertura pendent, en lloc d'inventar
una pregunta. No ampliïs el volum fins que les mostres de calibratge siguin
aprovades.

## Propera etapa

Llegir i aprovar les mostres de `knowledge/review/EXEMPLES.md`. Després crear
un lot petit, tema per tema, amb el mateix estàndard. Els registres antics
queden arxivats i no tornen a les sortides sense una revisió completa.
