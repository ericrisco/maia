# Pla editorial de Maia Training Data

## Objectiu

Preparar dos datasets separats i útils per entrenar un assistent:

- **Knowledge**: respondre preguntes sobre Andorra amb el coneixement de
  `docs/temes/`.
- **Language**: aprendre de parla andorrana contemporània autèntica i autoritzada
  a `docs/parla/`; no inventar converses ni barrejar-la amb Knowledge.

La cobertura ha de ser exhaustiva. La generació de dades, però, no consisteix a
convertir cada títol, paràgraf o fila en una pregunta. Es cobreixen els fets amb
preguntes que una persona faria; quan no n'hi ha cap de natural, el fet queda
registrat com a pendent, no es força una conversa.

## Per què es refà el criteri

Una pregunta com «Què explica la secció X de la fitxa Y?» pressuposa que
l'usuari té una fitxa al davant. «Què indica aquesta fila?» depèn d'una taula
que no forma part del xat. I una resposta com «La fitxa no ho concreta» parla
del sistema de documentació, no ajuda l'usuari.

També són febles les preguntes que només existeixen per activar una dada, les
converses on cada usuari pregunta una cosa nova sense escoltar la resposta, i
els diàlegs amb el mateix inici fictici repetit («em pensava que...», «he vist
que...»). Canviar aquestes frases per sinònims no resol el problema.

## Escriure una conversa de Knowledge

### 1. Comença pel motiu de consulta

Llegeix la fitxa sencera i les fonts relacionades que calguin. Abans de redactar,
anota en una targeta interna:

```text
Què necessita resoldre l'usuari?
Quina resposta concreta li servirà?
Quins fets i quines fonts ho sostenen?
Quin límit o dubte no es pot donar per resolt?
Quina pregunta podria sorgir després de la resposta?
```

La intenció pot ser pràctica (què cal saber per anar-hi o fer-ho), explicativa
(què vol dir o com funciona), de verificació (és cert això?), de comparació (en
què es diferencien?) o de context (com s'hi ha arribat?). No facis servir el
títol de la fitxa com a motiu de consulta.

### 2. Formula la pregunta com un missatge de xat

La pregunta ha de ser comprensible sense cap document extern. Escriu-la com la
diria algú que vol resoldre aquell dubte, amb la quantitat de context que
realment aportaria al xat. Combina preguntes directes, peticions pràctiques,
dubtes de significat, comprovacions i comparacions. No repeteixis una plantilla
amb els noms canviats.

No inventis una biografia, una experiència, una observació o una conversa
prèvia per fer la pregunta més viva. «On i quan puc veure una festa de l'ossa?»
ja té una intenció clara; no cal atribuir a l'usuari un viatge que no ha explicat.
No parlis de «la fitxa», «el corpus», «aquesta secció» ni «la fila».

### 3. Fes que cada seguiment continuï el fil

Primer escriu la resposta inicial. Després pregunta't què voldria aclarir algú
que acaba de llegir-la: una diferència, una conseqüència, un terme, una data o
un límit. El seguiment ha de reprendre una dada o una idea de la resposta
anterior; si es podria enganxar igualment a qualsevol conversa, no serveix.

No exigeixis un nombre fix de torns. Una conversa pot tenir un seguiment o més
d'un si el fil ho demana. No hi afegeixis preguntes només per arribar a tres
intercanvis. No tornis a preguntar el mateix amb altres paraules.

### 4. Respon de manera directa i útil

- Comença contestant el que s'ha preguntat.
- Escriu frases completes i autònomes, amb context suficient per entendre-les.
- Explica què vol dir una data, una xifra, una institució o un nom quan calgui.
- Corregeix una premissa amb naturalitat i ofereix la informació que sí que
  consta.
- Si hi ha discrepàncies, explica-les sense triar arbitràriament una versió.
- Si la font no permet concloure una cosa, digues-ho sense fer veure que ho sap.
- No diguis «la fitxa», «el corpus» o «el document diu» en lloc de contestar.
- No afegeixis context només per omplir la resposta.

### 5. Llegeix només el diàleg i fes la revisió factual

Fes dues revisions separades:

1. **Lectura de persona usuària:** només amb els missatges, s'entén per què
   pregunta i què vol resoldre? El fil sona com un xat que podria passar de
   debò? Hi ha alguna dada que l'usuari sembla saber sense que ningú l'hagi
   introduïda?
2. **Lectura de font:** cada afirmació de l'assistent està sostinguda? La
   resposta distingeix els fets, les interpretacions i les coses que no
   consten? Els drets permeten reutilitzar-la?

Descarta o reescriu qualsevol conversa que soni a examen, interrogatori, índex,
formulari o demostració d'una plantilla. Com a comprovació addicional, puntua
de 0 a 2 la intenció recognoscible, la naturalitat, la continuïtat, la resposta
i la fidelitat. Cal 9/10 o més i cap zero; una puntuació alta no substitueix les
dues revisions.

## Cobertura sense preguntes artificials

Treballa tema a tema. Registra quins documents, seccions, taules, noms, dates,
relacions i buits s'han revisat. Connecta fitxes quan una resposta necessita
més d'una font. Marca explícitament els fets sense una pregunta natural, els
buits i les discrepàncies. Això permet auditar cobertura sense inflar el
dataset amb preguntes inútils.

## Language: flux separat

Inclou només material de `docs/parla/` que compleixi els criteris de veu,
època, aptitud lingüística, drets i fiabilitat de transcripció. Quan hi hagi
intercanvis reals, conserva'ls amb retocs mínims. No fabriquis preguntes per
convertir monòlegs en diàlegs i no reescriguis les respostes com si fossin una
imitació del parlar andorrà.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── review/       # candidats, procedència i exemples de calibratge
│   ├── work/         # inventari, targetes i cobertura
│   ├── output/       # converses aprovades, només missatges
│   ├── reports/      # cobertura, qualitat, drets i splits
│   ├── scripts/      # exportació i validació
│   └── archive/      # lots retirats, preservats i exclosos
└── language/         # flux separat de parla humana autoritzada
```

Els lots antics romanen a `knowledge/archive/`; no entren a l'exportació. Cada
conversa recuperada s'ha de tornar a redactar i revisar. `output/` només inclou
registres aprovats; cada línia final conté únicament `messages` i no exposa
identificadors, notes editorials ni metadades internes.

## Seqüència de treball

Per cada conversa: revisa el tema i la font, redacta el fil, comprova la
naturalitat llegint-lo sense les fonts, verifica els fets i els drets, revisa
duplicats i split, exporta i actualitza cobertura. Fes un commit i un push per
conversa, a `main`, després de validar els canvis. No passis al registre
següent si el push ha fallat.

No ampliïs el volum fins que els exemples de calibratge sonin creïbles llegits
en veu alta. Un nombre més alt de registres no compensa preguntes que ningú no
faria.
