# Criteris de les mostres

Les cinc converses de `../examples/conversations.jsonl` són material de
calibratge, no dades aprovades. Serveixen per posar a prova el mètode abans de
crear una cua nova.

## Què han de demostrar

- La primera pregunta dona context suficient, però no sona com una ordre de
  llegir el corpus.
- La resposta comença pel dubte concret i explica els termes locals quan cal.
- El seguiment apareix de manera creïble després de la resposta i continua el
  mateix fil.
- La conversa pot ser útil encara que l'usuari no conegui cap títol ni fitxa.
- Els matisos, les contradiccions i el que no se sap es mantenen visibles.

## Per què s'han triat aquestes mostres

1. **Passa i Marratxa** — una confusió versemblant entre dos actes del mateix
   programa; el seguiment pregunta per l'ordre de la cercavila.
2. **L'Última Ossa** — un dubte espontani sobre l'escena de la sang; després,
   l'usuari pregunta com continua la representació.
3. **Sant Joan de Caselles** — compara dues obres visibles al mateix lloc i
   segueix amb una pregunta sobre la conservació de la Crucifixió.
4. **La Marratxa i el Pareatge** — no oculta la diferència entre les dates del
   7 i el 8 de setembre ni converteix la tradició en certesa documental.
5. **Els estripagecs** — parteix d'una característica visible d'una finestra,
   n'explica la funció i el nom, i després n'aclareix l'abast geogràfic.

## Rebutja o reescriu

- Preguntes sobre què diu una secció, fitxa, fila o document.
- Respostes que comencen amb fragments sense subjecte o context.
- Seguiments que només serveixen per extreure una dada independent.
- Històries personals inventades per fer que una pregunta soni oral.
- Fets que la font no sosté o que amaga una discrepància documentada.

Llegeix només els missatges, en veu alta i sense procedència. Si la conversa
sembla un qüestionari o una plantilla, reescriu-la des de la necessitat humana
o descarta-la. Registra sempre les fonts i els drets a `../examples/provenance.jsonl`.
