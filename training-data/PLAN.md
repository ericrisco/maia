# Pla de Maia Training Data

## Objectiu

Crear dos conjunts separats a partir de `docs/`:

- **Knowledge** respon dubtes reals sobre Andorra amb informació que el corpus sosté.
- **Language** conserva llengua andorrana contemporània produïda per persones i verificada.

La qualitat de cada conversa va abans que el volum. Un registre que només serveix per cobrir una fila no s'afegeix.

## Criteri de conversa

Cada conversa ha de semblar una interacció útil entre una persona i un assistent. La font serveix per verificar els fets; no és el context que ha de tenir l'usuari.

### Preguntes que sí serveixen

- Dubte pràctic o de significat: «Si hi ha més persones inscrites a la biblioteca, vol dir que també hi va més gent?»
- Contrast: «Va créixer l'assistència al cinema o només ho sembla per les xifres?»
- Conseqüència: «Això permet dir que la pandèmia va fer caure els préstecs?»
- Aclariment: «Quan dius 9 punts, vols dir un 9%?»
- Síntesi: «En general, quins hàbits culturals van pujar i quins van baixar?»

### Preguntes que no serveixen

No preguntar què diu una fitxa, secció, taula, fila, gràfic o paràgraf. No usar «aquesta dada» sense explicar quina dada és. No fer preguntes d'examen ni repetir la mateixa plantilla amb altres noms.

### Fer que el fil avanci

1. Escriu primer la necessitat humana en una frase privada.
2. Formula una primera pregunta que s'entengui sense obrir cap document.
3. Respon directament i amb prou context per evitar una lectura errònia.
4. Afegeix seguiments que neixin de la resposta anterior: una conseqüència, una comparació, una possible confusió o un límit.
5. Atura el fil quan el dubte queda resolt. El patró habitual és de 2–4 intercanvis; no és una quota.
6. Llegeix només les preguntes d'usuari. Si semblen un qüestionari, reescriu-les.

No inventis una biografia, una feina, una opinió ni una experiència de l'usuari per fer sonar el diàleg més humà. La naturalitat surt del dubte i del seguiment, no d'afegir escenari fictici.

## Respostes

- Comença per la resposta, no per una etiqueta ni una llista de camps.
- Fes servir llenguatge corrent i explica els termes necessaris.
- Separa recompte, percentatge, punts percentuals, estimació i percepció.
- No dedueixis causes de dues xifres que només coincideixen en el temps.
- Quan la font no resolgui una pregunta, digues què permet afirmar i què no.
- No copiïs un paràgraf sencer si una resposta més curta resol el dubte.

## Fonts, drets i cobertura

Abans d'escriure, comprova que les fonts sostenen cada afirmació i permeten l'ús previst. Registra títol o identificador de font, ubicació, llicència, atribució, limitacions i les unitats de contingut cobertes. Mantén aquesta informació fora de `messages`.

Una conversa pot cobrir més d'una unitat o fitxa si la relació entre elles és documentada. Exclou contingut amb drets pendents. Marca com a incert el que el corpus no resol; no completis buits amb coneixement extern.

## Revisió abans d'acceptar

Totes les respostes han de ser «sí»:

- La pregunta inicial és una cosa que una persona podria preguntar sense veure la font?
- El seguiment és una reacció plausible a la resposta immediatament anterior?
- Cada resposta contesta primer la pregunta i sona bé en veu alta?
- Les afirmacions i els matisos estan sostinguts per fonts reutilitzables?
- El fil distingeix fet, interpretació, tradició i incertesa?
- El diàleg ensenya un comportament útil i no és duplicat d'un altre?
- La conversa continua tenint sentit sense procedència ni identificadors interns?

Si alguna resposta és «no», reescriu, deixa pendent o exclou.

## Fases

1. Aplicar la guia `knowledge/review/EXEMPLES.md` i calibrar l’estil amb `knowledge/examples/`.
2. Inventariar el coneixement i els drets de les fonts de `docs/temes/`; conservar el mapa de cobertura regenerable.
3. Crear converses multitorn a `knowledge/review/conversations.jsonl`, amb procedència i unitats cobertes a fitxers separats.
4. Revisar naturalitat, correcció, drets, duplicats i separació dels conjunts; no donar per coberta cap unitat sense evidència.
5. Generar els exports i informes només quan hi hagi registres aprovats.
6. Tractar Language en el seu propi flux. Incloure només parla humana elegible i verificada; no generar respostes lingüístiques inventades.

## Definició de fet

Knowledge no està acabat fins que les fitxes elegibles s'han inspeccionat, el coneixement útil està cobert, les converses són naturals i correctes, els drets són clars i els conjunts passen validació.

Language no està acabat fins que les peces elegibles s'han inspeccionat, la parla i els drets s'han verificat, les transcripcions incertes s'han filtrat i no hi ha filtracions entre train, validation i test.
