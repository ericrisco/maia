# Criteri i exemples de Maia Knowledge

Les mostres completes són a [`../examples/conversations.jsonl`](../examples/conversations.jsonl). La procedència i l'estat dels drets són a `../examples/provenance.jsonl`. Són exemples editorials, no cobertura del corpus ni exports entrenables.

## Abans d'escriure

Imagina la persona, què vol saber i per què ho pregunta. Pot tenir un dubte de viatge, haver sentit una paraula, confondre dues tradicions o voler entendre una decisió històrica. La conversa no ha de dependre de conèixer títols, seccions o files internes de Maia.

**Prova de lectura:** ensenya només les intervencions d'usuari a algú que no ha vist el corpus. Si sonen a exercici de comprensió lectora, reescriu-les.

## Patró de conversa

- Comença amb una pregunta completa i natural.
- Respon el dubte sense preàmbuls de base de dades.
- Fes almenys un seguiment que s'entengui a partir del fil i aporti una pregunta nova.
- Mantén el context sense fer repetir informació.
- Atura't quan la persona ja té resposta. No cal que tots els registres tinguin el mateix nombre de torns.

## Evita

- «Què explica la secció “El relat”?»
- «Què indica aquesta fila del gràfic?»
- preguntes que copien un títol de fitxa sense una situació humana;
- respostes truncades, com una llista de topònims sense dir què signifiquen;
- atribuir al corpus una conclusió que les fonts deixen oberta;
- seguiments posats només per fer el registre més llarg.

## Exemple del to buscat

```text
Usuari: La Passa de Sant Julià és una dansa?
Assistent: No: és una cercavila de parelles de fadrins pels carrers principals de Sant Julià de Lòria, no un ball.
Usuari: I qui hi va al davant?
Assistent: Les parelles que es casaran aquell any. Reben el nom de «majors fadrins» i encapçalen la cercavila.
Usuari: La fan durant la festa major?
Assistent: Sí. Se celebra al migdia del dilluns de la festa major.
```

La conversa parteix d'un dubte que algú podria tenir i els seguiments aprofundeixen en el mateix tema. Les afirmacions es comproven a `docs/temes/costums/ritus-de-pas/la-passa.md`; l'exemple no és exportable mentre els drets de les fonts siguin pendents.

## Revisió de cada conversa

1. La primera pregunta s'entén sense haver obert Maia.
2. Hi ha almenys dues intervencions d'usuari i cada resposta resol el torn corresponent.
3. El fil és natural; cap seguiment no és una pregunta de plantilla.
4. Totes les afirmacions estan documentades i les incerteses es conserven.
5. La conversa no porta IDs ni metadades internes.
6. Totes les fonts i els drets són a la fila corresponent de procedència.
