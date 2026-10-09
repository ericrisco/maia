# Guia de qualitat per a converses de Maia Knowledge

## El problema que volem evitar

Una pregunta pot ser gramatical i correcta i, tot i així, no semblar una cosa que preguntaria una persona. Això passa quan la conversa només serveix per recitar una fitxa: «què explica aquesta secció?», «què indica aquesta fila?» o una successió de preguntes curtes que cobreixen fets independents.

No disfressis aquest patró afegint «he vist que», «m'han dit que» o «és veritat que». Aquestes expressions només funcionen quan la situació i el dubte són plausibles per si mateixos.

## Abans de redactar

Escriu una nota interna: **«Aquesta persona vol…»**. Ha de descriure una necessitat concreta, com orientar-se en una festa, aclarir una confusió o entendre què implica una dada. «Vol saber què diu el document» no serveix.

Després tanca la font i prova d'escriure el diàleg des d'aquesta necessitat. No inventis que l'usuari hi era, que va llegir una font o que té un problema personal. Dona només el context que una conversa real necessitaria.

## Com ha de sonar

- La primera pregunta pot tenir context («Al programa hi surten…») o anar al gra («La sang és de debò?»). No ha de seguir una plantilla fixa.
- L'assistent respon primer la pregunta. Després explica el terme local o el límit necessari, sense parlar de «la fitxa» ni de «la font» si no és rellevant per a l'usuari.
- El seguiment reacciona a la resposta i fa avançar el mateix tema. Pot ser breu; no ha de repetir tots els noms ni reformular la primera pregunta.
- Una conversa pot tenir dos, tres o més seguiments si sorgeixen de debò. No afegeixis torns només per assolir un recompte.
- Si el corpus no permet contestar una part, digues què se sap i què queda obert amb paraules normals. No converteixis cada seguiment en «se sap per què?».
- Varia les veus i el ritme. Una persona pot corregir-se, demanar una precisió, dubtar d'una afirmació o preguntar què pot esperar d'un acte.

## Calibratge: diàlegs que sí que volem

Aquests exemples fixen el to. No són registres aprovats ni compten com a cobertura. La procedència de cada exemple és a `../examples/provenance.jsonl`.

### Un dubte nascut d'un programa de festa

```text
user: Al programa de la festa major de Sant Julià, la Passa surt al costat de la Marratxa. Són dos balls?
assistant: La Marratxa sí que és un ball; la Passa és una cercavila de parelles de fadrins pels carrers. Totes dues es fan el dilluns de la festa major.
user: Ah, entesos. I a la Passa les parelles van barrejades?
assistant: No. Van ordenades per edat, i al davant hi van les parelles que s'han de casar aquell any.
```

Per què funciona: el dubte neix d'una confusió concreta i la resposta permet entendre què veurà la persona. El seguiment demana un detall del mateix acte.

### Una pregunta espontània sobre una escena

```text
user: Quan maten l'ossa d'Ordino, la sang que reparteixen és de veritat?
assistant: No. És aigua amb granadina. Dins la farsa, la minyona la «pua» i en comparteix la victòria amb el públic.
user: I després ja s'acaba la representació?
assistant: No, acaba amb un ball col·lectiu de cançons populars, en què també participa l'ossa.
```

Per què funciona: és una reacció plausible a una escena; la conversa continua amb què passa després, sense convertir-se en una llista de dades de la festa.

### Distingir dues peces d'una visita

```text
user: A Sant Joan de Caselles, la crucifixió i el retaule són tots dos romànics?
assistant: No. La Crucifixió és una obra romànica d'estuc del segle XII i es conserva dins l'església. El retaule és molt posterior, del 1527, amb influències del Renaixement italià i germànic.
user: La crucifixió l'han mogut d'on era originalment?
assistant: No. Es conserva in situ: no l'han arrencat ni traslladat a un museu.
```

Per què funciona: la comparació és útil per a qui visita el lloc. El seguiment demana una conseqüència concreta de la primera resposta.

## Reescriptures i descart

| No passa | Per què | Direcció útil |
|---|---|---|
| «Què explica la secció “El relat”?» | Depèn d'un document i no revela cap necessitat. | Pregunta pel dubte que el relat pot aclarir. |
| «Què indica aquesta fila?» | No s'entén sense veure la taula. | Digues quines xifres xoquen i què necessites aclarir. |
| «I dos topònims que en surten?» | És un fragment sense pregunta ni context. | Descarta'l si ningú no tindria un motiu real per demanar-los. |
| «Què és la Passa? I quan és? I qui hi participa?» | Sembla un qüestionari de cobertura. | Comença pel dubte principal i deixa que el seguiment surti de la resposta. |
| «He vist que la Marratxa té tres noies. Per què?» | Pot ser una pregunta natural, però no si l'únic objectiu és extreure una dada i el seguiment no avança. | Conserva-la només si la resposta i el torn següent formen una conversa clara i útil. |

## Revisió abans d'afegir un candidat

Llegeix només els missatges, en veu alta, sense títols ni procedència. Accepta el diàleg només si pots respondre «sí» a tot això:

1. Entenc qui pregunta i què intenta aclarir sense haver vist el corpus?
2. La pregunta inicial sortiria en una conversa real, sense explicar una història inventada?
3. L'assistent resol la pregunta a la primera frase i conserva els matisos importants?
4. El seguiment respon al que s'acaba de dir i manté el mateix fil?
5. Les respostes sonen com ajuda d'una persona informada, no com notes enganxades d'una fitxa?
6. Cada afirmació està coberta per l'evidència i té procedència i drets registrats per separat?

Si falla la naturalitat, no ho arreglis afegint un altre torn. Reescriu-ho des de la necessitat humana o descarta-ho.
