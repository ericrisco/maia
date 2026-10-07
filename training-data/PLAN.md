# Pla editorial per a converses de Maia

## Objectiu

Crear diàlegs útils sobre Andorra a partir del corpus de `docs/`. Les preguntes
han de semblar missatges que una persona enviaria a un assistent perquè vol
entendre, aclarir o resoldre alguna cosa. Les respostes han de ser correctes,
directes i naturals.

No es mesura la cobertura pel nombre de preguntes. Es mesura pels temes i fets
revisats, inclosos els que no donen lloc a cap pregunta natural.

## Com es construeix un diàleg

1. **Entén el tema abans d'escriure.** Llegeix la peça sencera i les fonts que
   calguin. Apunta en una nota interna els fets, els límits, les discrepàncies i
   els drets de cada font.
2. **Tria una necessitat humana concreta.** Per exemple: entendre una norma,
   aclarir una paraula, saber per què una pràctica era diferent o comprovar una
   idea que pot ser errònia. No triïs una dada només perquè encara no té
   pregunta.
3. **Escriu el primer missatge com un xat.** Dona només el context que la persona
   diria de debò. La pregunta ha de tenir sentit sense veure cap fitxa, taula o
   document.
4. **Redacta la resposta abans del seguiment.** Contesta directament. Afegeix
   prou context perquè s'entengui, sense descarregar-hi tots els detalls de la
   font.
5. **Continua el fil.** El següent missatge ha de sorgir d'una cosa que Maia
   acaba d'explicar. Pot demanar un aclariment, una conseqüència, una diferència
   o un límit. Si és una pregunta nova sense relació, comença un altre diàleg.
6. **Atura't quan el dubte s'ha resolt.** Sovint n'hi haurà prou amb dos o tres
   intercanvis. No s'afegeix un torn només per allargar la mostra.
7. **Revisa el diàleg sense consultar la font.** Pregunta't si sona com una
   conversa possible, si cada torn segueix l'anterior i si l'usuari sembla saber
   coses que encara no li han explicat.
8. **Contrasta després cada afirmació amb les fonts.** Si hi ha incertesa,
   discrepància o un buit, conserva'l en la resposta sense inventar una
   explicació.

## Preguntes que volem

- Parteixen d'un dubte concret: «Quan parlem de terres comunals, vol dir que
  pertanyien al comú?»
- Poden demanar ajuda pràctica, sempre dins d'allò que les fonts permeten
  afirmar: «Si hi vaig per Carnaval, a quina parròquia puc veure el ball de
  l'ossa?»
- Poden expressar una confusió real: «Aleshores, si el terreny era privat,
  per què en diuen comunal?»
- Poden comprovar una premissa: «La imatge de Meritxell es va quedar a
  Canillo?»
- Poden ser breus i col·loquials, però han de continuar sent clares i
  respectuoses.

## Preguntes que descartem

- «Què explica la secció X de la fitxa Y?»
- «Què indica aquesta fila?» o «Què diu el gràfic?» sense descriure què vol
  entendre la persona.
- «Quin any va passar X?» quan l'any és una dada aïllada sense cap motiu
  conversacional.
- Una seqüència de preguntes independents, com si l'usuari passés un qüestionari.
- Una història personal inventada («hi vaig anar l'altre dia», «el meu avi em
  va dir…») usada només per fer més viva la pregunta.
- Una premissa falsa que l'assistent no corregeix.
- Sinònims d'una pregunta ja inclosa, si no canvien la intenció ni la resposta.

## Respostes

- Comença per la resposta, no per una referència al document.
- Usa frases completes i vocabulari planer. Defineix els termes històrics quan
  són necessaris per seguir el fil.
- Separa el fet documentat de la interpretació. No presentis una inferència com
  si fos una dada de la font.
- En preguntes sobre el passat, situa el període perquè no es confonguin amb una
  norma vigent.
- No donis consell legal, mèdic o financer actual a partir d'una font històrica.
- Si la font no permet respondre, explica què se sap i què queda obert.

## Criteris d'aprovació: tots han de passar

1. **Intenció:** s'entén què vol saber la persona i per què ho preguntaria.
2. **Naturalitat:** el missatge podria aparèixer en un xat real; no depèn d'una
   fitxa ni sembla una pregunta d'examen.
3. **Continuïtat:** cada seguiment reprèn la resposta anterior i no repeteix el
   mateix dubte.
4. **Utilitat:** la resposta resol la pregunta sense ser telegràfica ni
   enciclopèdica.
5. **Fidelitat:** cada afirmació és sostinguda per una font revisada i respecta
   els seus límits.
6. **Drets:** la procedència i les condicions de reutilització estan anotades.
7. **Originalitat:** la conversa no duplica una altra mostra amb els noms
   canviats.

Si un criteri falla, es reescriu o es descarta. Una puntuació numèrica no
substitueix aquesta revisió.

L'estat de drets es registra tal com consta a la font. Un estat «no» o
«pendent» no s'ha de presentar com a permís. La decisió d'incloure material a
la preparació del model correspon al propietari del projecte; l'exportació
conserva l'atribució i les limitacions, i no declara una llicència global.

## Cobertura i exportació

Es revisa el corpus tema a tema. L'inventari intern marca què s'ha llegit,
quines afirmacions tenen mostra aprovada i quines encara no tenen una pregunta
natural. Les relacions entre temes només s'utilitzen quan ajuden a respondre una
necessitat concreta.

Els exemples de `knowledge/review/EXEMPLES.md` fixen el criteri editorial. Les
converses de producció van a `knowledge/review/conversations.jsonl`, una
conversa completa per línia; la procedència va en una línia corresponent a
`provenance.jsonl`. Només les converses aprovades passen a `knowledge/output/`.
Cada conversa és un pas de treball independent: revisar-la, validar-la,
actualitzar cobertura, fer un commit i push a `main` abans de començar la
següent. Els splits s'agrupen per tema o fet relacionat per evitar variants
gairebé iguals a banda i banda.

## Maia Language

És un flux separat. Només s'hi inclou parla contemporània autèntica amb drets
anotats i transcripció prou fiable. Es conserva la formulació humana. No
s'inventen preguntes ni es reescriu una resposta per imitar el català
andorrà.

## Fases

1. Aplicar els exemples editorials a cada tema i revisar tot el corpus, sense
   saltar documents perquè siguin difícils o poc coneguts.
2. Redactar i verificar converses una a una. Un registre ha de respondre una
   necessitat real; diversos fets poden quedar coberts pel mateix diàleg si
   aquest els necessita de debò.
3. Afegir la procedència i les condicions reals de cada font. Marcar els drets
   pendents o negatius; no convertir-los en una afirmació de permís.
4. Mantenir inventari de documents i cobertura perquè es vegi què falta i per
   què algun fet no té una pregunta natural.
5. Deduplicar i agrupar els registres relacionats abans de crear els splits.
6. Exportar, validar i informar la cobertura dels dos datasets.

El treball continua tema a tema fins a cobrir el corpus. No es considera acabat
per haver arribat a una xifra de registres.
