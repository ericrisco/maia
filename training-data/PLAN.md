# Pla de Maia Training Data

## Objectiu

Preparar converses útils per entrenar un model especialitzat en Andorra. Cada exemple ha de sonar com una conversa que una persona podria tenir i ensenyar una resposta correcta, completa i natural.

No convertim títols, paràgrafs, taules o files en preguntes mecàniques. Primer identifiquem una curiositat humana; després comprovem que el corpus permet respondre-la.

## Per què canviem el mètode

Les preguntes «Què explica aquesta secció?» o «Què indica aquesta fila?» pressuposen que la persona llegeix material editorial. Les respostes fragmentàries com «I dos topònims que en surten:» tampoc resolen cap dubte. Aquests exemples ensenyen a repetir l'estructura de les notes, no a conversar.

## Criteris per a cada conversa Knowledge

1. **Curiositat concreta:** què vol entendre una persona i per què ho preguntaria?
2. **Pregunta autònoma:** s'entén sense haver vist cap fitxa, títol o taula. El context necessari apareix a la pregunta o al torn anterior.
3. **Resposta directa:** la primera frase resol el dubte; després hi afegeix només el context necessari.
4. **Seguiment motivat:** cada nou torn neix de la resposta anterior, demana una aclaració, una conseqüència o posa a prova una deducció. No canviem de tema per arribar a més torns.
5. **Conversació completa:** com a mínim dos torns d'usuari. Si no surt un seguiment útil i natural, no forcem la conversa.
6. **Límits clars:** distingim fets, relats tradicionals, interpretacions i incerteses. No generalitzem més enllà de la font.
7. **Procedència separada:** les converses no porten IDs ni notes internes; un fitxer de procedència les vincula amb fonts, afirmacions i situació dels drets.
8. **Lectura en veu alta:** si sona com un examen, una consulta de base de dades o una nota de recerca, es reescriu.

## Preguntes a evitar

- «Què explica la fitxa/secció?»
- «Què indica aquesta fila/taula?»
- «Quins elements hi surten?» sense dir què vol resoldre la persona.
- «I què més?» si no hi ha un antecedent clar.
- Preguntes que ja contenen la resposta o exigeixen endevinar un context absent.
- Seguiments que repeteixen la primera pregunta amb altres paraules.

## Cicle de treball

1. **Calibrar:** revisar les mostres de `knowledge/examples/` i acordar veu, extensió i estil de seguiment.
2. **Inventariar:** recórrer tots els documents de `docs/temes/` i `docs/parla/`; marcar cada unitat com pendent, coberta o exclosa amb motiu.
3. **Crear per tema:** llegir la font completa, anotar els fets verificables i redactar converses només quan hi hagi una pregunta humana plausible.
4. **Revisar:** comprovar naturalitat, resposta completa, exactitud, seguiments i procedència. Registrar drets abans d'exportar.
5. **Ampliar:** avançar tema a tema, sense quotes artificials ni paraphrases repetides. Revisar les noves mostres abans de generar-ne més.
6. **Exportar Knowledge:** deduplicar i fer splits per tema/font per limitar filtracions. Incloure només registres aprovats i fonts elegibles.
7. **Preparar Language:** seleccionar fragments humans elegibles, verificar transcripció i drets, conservar la veu real i agrupar splits per peça o parlant.
8. **Validar i documentar:** comprovar format, contingut, cobertura, procedència, drets i separació entre train/validation/test.

## Format

Una línia JSONL per conversa, només amb `messages` i els rols `user` / `assistant`. La procedència va en un fitxer separat. Les mostres d'`examples/` no es copien a cap exportació automàticament.

## Estat i següent pas

Les quatre converses inicials són una prova de disseny, no una cobertura del corpus. El següent pas és revisar-les junts, corregir les que no sonin naturals i acordar el patró abans de produir més registres.
