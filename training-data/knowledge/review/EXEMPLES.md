# Guia per redactar candidats

Les mostres de calibratge són a [`../examples/conversations.jsonl`](../examples/conversations.jsonl). Les candidates actives s'escriuen a `conversations.jsonl`, amb procedència separada.

## Reescriu la necessitat, no el títol

| Rebutja | Motiu | Pregunta més humana, si el corpus la pot respondre |
| --- | --- | --- |
| «Què explica la secció “El relat” de la fitxa de Meritxell?» | Depèn de conèixer una fitxa i una secció. | «Per què el santuari de Meritxell es va construir just en aquell indret?» |
| «Què indica aquesta fila?» | No identifica què es vol entendre. | Afegeix el tema i el dubte concret, o descarta-la si no hi ha context fiable. |
| «I dos topònims que en surten:» | No és ni pregunta ni resposta completa. | Formula el dubte real sobre els llocs, si n'hi ha; altrament, no facis un registre. |
| «Què és X?» repetida per cada document | Fa que tot el dataset sembli un formulari. | Parteix de confusió, decisió, comparació, causa o conseqüència que algú voldria entendre. |

## Multitorn natural

Un seguiment ha de poder venir de la resposta anterior. Després d'explicar que la Passa és una cercavila, és natural preguntar qui hi va al davant. No és natural saltar a una dada d'un altre article només per afegir un torn.

No cal que cada conversa sigui multitorn. El conjunt ha de mostrar ambdues formes, sense quota per registre.

## Respostes

- Contesta primer el dubte amb una frase que s'entengui sola.
- Afegeix el context necessari, no una llista de tot el que diu la font.
- Distingeix fets, llegendes i interpretacions amb paraules clares.
- No inventis experiències personals, errors, argot o accent.
- Deixa explícita la incertesa quan la font no resol una discrepància.

## Validació ràpida

Llegeix el diàleg en veu alta sense la font. Si no sona com una conversa útil, si necessita que l'usuari conegui l'estructura de l'article o si la resposta no resol el dubte, reescriu-lo o descarta'l. Comprova després els fets i drets per separat.
