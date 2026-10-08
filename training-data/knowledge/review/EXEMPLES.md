# Exemples i criteris de revisió de Maia Knowledge

Els registres de `conversations.jsonl` han de sonar com una conversa entre una persona i un assistent. La persona no sap com està organitzat el corpus.

## Abans d'aprovar una conversa

1. **Pregunta humana:** parteix d'una curiositat, sorpresa, confusió o necessitat real. No demana explicar una fitxa, secció, taula, fila o fragment.
2. **Resposta completa:** resol la pregunta en el primer torn. No guarda informació imprescindible per al següent.
3. **Seguiment amb fil:** la pregunta següent sorgeix de la resposta i explora una cosa nova. No repeteix el mateix ni canvia de tema per recollir una dada pendent.
4. **Llengua oral i clara:** la pregunta podria dir-se en veu alta. Evita llistes telegràfiques i expressions internes com «el corpus registra».
5. **Fets amb límits:** les afirmacions, dates i matisos concorden amb les fonts. Una tradició no es presenta com a prova.
6. **Diàleg autònom:** una persona que no ha vist les fonts entén tots els torns i els pronoms tenen referents clars.
7. **Traçabilitat:** cada fet es pot vincular a una font i a les seves condicions d'ús.

Cada registre té almenys dues preguntes d'usuari. Pot tenir-ne més si el fil ho demana. No s'allarga una conversa per complir una mida fixa.

## Reescriptures

**No:** «Què explica la secció “Els personatges”?»

**Sí:** «A la farsa de l'ossa d'Encamp, per què els dallaires tenen tant de protagonisme?»

La segona pregunta neix del tema i es pot fer sense veure la fitxa.

**No:** «I dos topònims que en surten:»

**Sí:** «Quins dos llocs hi apareixen, i què se sap de la relació entre ells?»

La resposta ha de donar els noms i explicar què permet afirmar la font. Si la font no explica la relació, ho ha de dir directament.

**No:** «Tres coses que el corpus registra per separat:»

**Sí:** «Per què el Consell General avançava diners per celebrar les Corts?»

La resposta explica la regla i el motiu documentat, sense parlar del procés de treball.

## Prova de lectura en veu alta

Llegeix només els missatges, sense obrir les fonts. Pregunta't:

- La primera pregunta la faria una persona que no coneix el corpus?
- La resposta resol el dubte i s'entén en aquest torn?
- El seguiment neix de la resposta i obre un pas nou?
- La conversa té un ritme natural, sense semblar un qüestionari?
- Cada resposta distingeix què sabem i què no podem afirmar?

Si un punt falla, reescriu el diàleg. No afegeixis una repregunta per amagar una resposta incompleta.

## Proveniència i exportació

Els missatges finals només contenen rols i contingut. Els IDs, les fonts i els drets van a `provenance.jsonl`. Una candidata amb drets pendents pot quedar en revisió, però no s'exporta fins que l'ús per entrenar estigui justificat.
