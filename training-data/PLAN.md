# Pla de Maia Training Data

## Objectiu

Construir dos datasets útils per a un assistent, amb preguntes que una persona
plantejaria en una conversa normal. No cal convertir cada paràgraf, taula o
detall en una pregunta. La cobertura ha de representar el coneixement rellevant
sense fabricar diàlegs ni repetir la mateixa dada amb sinònims.

## Abans d'escriure un exemple

1. Llegeix la font i identifica una cosa que algú podria voler entendre,
   resoldre o aclarir.
2. Escriu la resposta factual a partir de la font, incloent-hi el període i els
   matisos que calguin.
3. Formula la pregunta des d'aquell dubte, sense demanar què diu una fitxa,
   secció, fila, gràfic o «corpus».
4. Llegeix la pregunta sola. Si no s'entén sense veure la font, reescriu-la.
5. Afegeix un seguiment només si una persona, després de llegir la resposta,
   tindria una raó natural per preguntar una cosa més.

Les converses poden tenir un torn o diversos. No s'han d'allargar per complir
una quota. Un seguiment no és una pregunta d'examen ni una segona dada
independent: reprèn una distinció, una conseqüència o un dubte que acaba de
sortir.

## Criteri de qualitat

- La primera pregunta té una intenció clara i prou context.
- La resposta resol el dubte a la primera frase i sona com una explicació oral.
- La resposta no copia l'estructura d'una taula ni enumera camps.
- Les preguntes no depenen d'un títol, d'un «això» sense antecedent o de veure
  una pàgina.
- Els casos hipotètics només serveixen per entendre una regla que la font
  acredita; no s'inventen persones, experiències ni fets.
- Llegendes, interpretacions, discrepàncies i buits s'expressen com a tals.
- Si una pregunta només demana recuperar una dada sense cap propòsit clar, es
  descarta. No s'omple el dataset per volum.
- La metadata de procedència i revisió queda fora de la conversa exportada.

## Maia Knowledge

Font: `docs/temes/`. Revisar els temes de manera sistemàtica, però prioritzar
converses que ensenyin una distinció, expliquin una causa, resolguin una
confusió, relacionin conceptes o responguin una curiositat plausible.

Per a cada conversa aprovada, conservar internament la font exacta, els fets que
la resposta utilitza, els drets i la decisió editorial. El fitxer d'entrenament
conté únicament `{"messages": [...]}`. No posar-hi IDs, estats, cites internes
ni comentaris del pipeline.

No fer un registre per cada unitat detectada. Una conversa pot cobrir diversos
fets si formen una explicació coherent; un fet pot quedar sense conversa si no
admet una pregunta natural. El report ha de mostrar tant la cobertura útil com
els continguts descartats i el motiu.

## Maia Language

Font: `docs/parla/`. És un objectiu separat: aprendre formes reals de parlar,
no coneixement sobre Andorra. Incloure només material contemporani elegible,
amb veu humana i drets verificats. No inventar una pregunta per a una resposta
que prové d'un monòleg. No fer que un model imiti una veu andorrana inventant
respostes.

Quan la transcripció sigui incerta, excloure el fragment afectat o justificar
clarament la decisió. Agrupar els splits per entrevista o parlant quan es pugui.

## Fases

1. Aplicar les mostres i la guia editorial a cada conversa.
2. Revisar, corregir i registrar les converses una per una.
3. Revisar tots els articles i temes de Knowledge amb procedència i cobertura
   auditables.
4. Auditar totes les peces de Language, incloses i excloses, sense fabricar
   converses.
5. Deduplicar, assignar train/validation/test sense fuga i validar els JSONL.
6. Publicar els reports i documentar com regenerar els exports.

Cada conversa JSONL nova o corregida és un pas independent: revisar-la,
validar-la, fer-ne un commit a `main` i pujar-lo abans de passar a la següent.
La procedència registra sempre la llicència i el valor real de
`redistribucio`. Segons `docs/CONTRACT.md`, els valors `no` i `pendent` són
avisos R005 i no bloquegen per si sols la inclusió; l'autorització final la
sosté el propietari del projecte. Els informes han de mantenir visibles aquests
avisos i permetre separar els registres per font.

Els fitxers de revisió actius són `knowledge/review/EXEMPLES.md`,
`knowledge/review/conversations.jsonl` i `knowledge/review/provenance.jsonl`.
El JSONL de converses és també la font de regeneració dels exports: una línia,
un objecte `messages`, sense metadata editorial.
