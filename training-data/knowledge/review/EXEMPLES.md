# Criteri i exemples de Maia Knowledge

Aquest fitxer governa les converses candidates a `conversations.jsonl`. Una bona conversa resol un dubte que una persona podria tenir sense haver llegit el corpus.

## Regles

1. Cada conversa té com a mínim dos torns de `user` i dos d'`assistant`.
2. La primera pregunta és concreta i autònoma. No esmenta fitxes, seccions, files, gràfics ni IDs.
3. La resposta comença pel que l'usuari vol saber; després hi afegeix només el context necessari.
4. El seguiment és una pregunta nova que sorgeix de la resposta anterior. No canvia de tema per omplir torns ni repeteix la primera pregunta.
5. Cada afirmació factual es pot rastrejar fins a un document del corpus. La procedència i els drets s'anoten fora de `messages`.
6. Si el corpus no resol una qüestió, la resposta ho diu amb naturalitat i no inventa una explicació.
7. La resposta ha de ser completa encara que la conversa s'acabi després de qualsevol torn d'assistent.
8. Llegeix el diàleg sense la font. Si no sona com una conversa útil, reescriu-lo o descarta'l.

## Exemples acceptables

### Dubte i aclariment

```json
{"messages":[{"role":"user","content":"La Passa de Sant Julià és un ball?"},{"role":"assistant","content":"No. És una cercavila de parelles de fadrins pels carrers principals, i es considera un ritu de pas."},{"role":"user","content":"Qui hi va al davant?"},{"role":"assistant","content":"Les parelles que es casaran aquell any, anomenades «majors fadrins». La resta desfila darrere seu, de més grans a més joves."}]}
```

### Confusió corregida i conseqüència

```json
{"messages":[{"role":"user","content":"La Passa i la Marratxa són dos balls de la festa major?"},{"role":"assistant","content":"No ben bé: la Marratxa és un ball, però la Passa és una cercavila de parelles de fadrins. Totes dues es fan el dilluns de la festa major de Sant Julià."},{"role":"user","content":"Aleshores, la Passa també té una coreografia?"},{"role":"assistant","content":"El corpus no ho documenta com una dansa ni descriu cap coreografia. El que sí que explica és l'ordre de la cercavila: al davant hi van les parelles que es casaran aquell any."}]}
```

### Pregunta pràctica amb límit explícit

```json
{"messages":[{"role":"user","content":"Els estripagecs dels cims d'Ordino són antics o els van instal·lar fa poc?"},{"role":"assistant","content":"Les peces dels cims són modernes: sis rèpliques d'1,4 metres es van instal·lar el juny del 2017. A Sorteny ja hi havia cinc tòtems de vuit metres des de la tardor del 2015."},{"role":"user","content":"Es poden veure tots en una sola excursió?"},{"role":"assistant","content":"El conjunt es presenta com un repte d'excursionisme, però el corpus no especifica si tots els punts es fan en una sola ruta ni quant dura."}]}
```

## Exemples que cal rebutjar

- «Què explica la secció “El relat” de la fitxa de Meritxell?» — pressuposa que l'usuari coneix una fitxa interna.
- «Què indica aquesta fila?» — no diu quin dubte vol resoldre.
- «I dos topònims que en surten:» — no és una pregunta completa i no té resposta.
- «Què és X?» repetit per cada document — és una plantilla, no una conversa.
- Resposta que enganxa una llista del document sense explicar què vol dir.
- Seguiment que salta a una altra fitxa només per fer la conversa més llarga.

## Abans d'afegir una conversa

Comprova-la contra quatre coses: naturalitat, fil entre torns, exactitud factual i procedència. Anota també a `work/coverage.csv` quins fets o parts del document queden coberts. No marquis un document complet si hi ha una secció, taula, llista, excepció o incertesa encara no revisada.
