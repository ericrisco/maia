# Criteris per revisar converses Knowledge

Les converses de [`../examples/conversations.jsonl`](../examples/conversations.jsonl) són mostres de calibratge, no candidats automàtics. Els registres que poden arribar a l'entrenament viuen a `conversations.jsonl`, una conversa per línia. La procedència i els drets corresponents van a `provenance.jsonl`.

## Abans d'aprovar una conversa

1. **La pregunta inicial surt d'una curiositat humana.** Ha de tenir sentit sense conèixer el corpus. No preguntis què diu una secció, una taula, una fitxa o una fila.
2. **La resposta resol el dubte.** Comença amb la idea principal i dona prou context perquè s'entengui; no copiïs una frase aïllada ni enumeris camps.
3. **El seguiment neix del que s'acaba de dir.** Afegeix un pas nou i creïble. No canviïs de tema per encabir una dada pendent ni preguntis el mateix amb altres paraules.
4. **Conserva el matís.** Distingeix tradició, interpretació, fet documentat i allò que encara no se sap. Situa les afirmacions en el seu període.
5. **Llegeix-la sense les fonts.** La conversa ha de fluir en veu alta i cada resposta ha de ser útil en el seu torn.
6. **Comprova cada afirmació a les fonts.** Desa'n el camí, la llicència, el permís, les condicions d'atribució i els límits a `provenance.jsonl`.
7. **Actualitza la cobertura concreta.** Marca només els fets i parts del document que la conversa realment tracta.

Cada registre ha de ser multitorn i contenir com a mínim dues preguntes de l'usuari. La segona pregunta ha de sortir de la primera resposta i demanar una cosa nova. Si el tema no permet una repregunta natural, no s'afegeix un «i això?» de farciment: es busca una altra conversa que sí que sostingui el format.

## Prova de lectura sense la fitxa

Llegeix només els missatges i pregunta't:

- La primera pregunta la faria algú que no sap com està organitzat el corpus?
- La primera resposta ja resol el dubte, sense obligar a esperar el torn següent?
- El seguiment s'entén pel que s'acaba de dir i aporta una resposta nova?
- Es distingeix què és documentat, què és una tradició i què no se sap?
- La conversa sona natural dita en veu alta, sense frases de fitxa ni llistes penjades?

Si falla una resposta, reescriu el torn sencer. No tapis una resposta incompleta amb una repregunta.

## Dos patrons de reescriptura

**No passa:** «Què explica la secció “Els personatges”?» La persona hauria de veure la fitxa per entendre la pregunta.

**Millor:** «A la farsa de l'ossa, per què els dallaires tenen tant de protagonisme?» El dubte es pot fer sense saber com està organitzat el document.

**No passa:** «I dos topònims que en surten:» És un fragment que no respon una pregunta.

**Millor:** explicar quins topònims són i per què importen, o dir clarament que les fonts no expliquen la relació.

**No passa:** «Tres coses que el corpus registra per separat:» Anuncia una llista, parla del procés intern i no respon el dubte de la persona.

**Millor:** dir directament què resol el decret, distingir els dos tipus d'interès i explicar què continua sense saber-se.

## Dades i drets

Cada línia JSONL és una conversa completa amb `messages` alternats entre `user` i `assistant`. No hi van IDs, explicacions del pipeline ni procedència. Una candidata no s'exporta fins que la conversa, els fets, els drets i la cobertura estan revisats.
