# Guia per a converses Knowledge

Aquest fitxer defineix el criteri per a `conversations.jsonl`. Cada línia és una conversa completa en format `messages`; la procedència corresponent va a `provenance.jsonl`. Els identificadors, les fonts i les notes editorials no s'inclouen als missatges.

## Comprova si la pregunta és humana

Abans de redactar, resumeix el dubte en una frase privada: què vol entendre, comparar o decidir la persona? Si la intenció és només «vol que li resumeixin la fitxa», descarta la pregunta.

La primera pregunta ha de funcionar sense cap document obert. Ha d'anomenar el tema i el dubte concret. Pot preguntar per una diferència, un mot, una data, una causa que cal verificar, una afirmació que sembla contradictòria o una decisió pràctica.

No facis servir preguntes com:

- «Què explica la secció “El relat”?»
- «Què diu el vocabulari que ho ordena?»
- «Què indica aquesta fila?»
- «Resumeix la fitxa “La troballa de Meritxell”.»

Aquestes preguntes parlen de l'estructura d'un document, no de la necessitat d'una persona. Tampoc comencis amb «això», «aquesta dada» o «aquesta fila» si no hi ha un referent clar dins la conversa.

## Escriu el fil

1. Escriu la primera pregunta d'usuari.
2. Contesta-la directament i amb els matisos necessaris.
3. Escriu el seguiment que algú podria fer després d'aquella resposta.
4. Contesta'l sense tornar a començar el tema.
5. Repeteix només mentre aparegui un dubte nou. Cada conversa ha de tenir entre **2 i 4 intercanvis**. No allarguis el fil per arribar al màxim.
6. Llegeix només les preguntes, en ordre. Han de sonar com una conversa, no com un examen ni un índex.

Els seguiments poden aclarir un terme, comprovar una conseqüència, demanar una comparació o posar a prova una inferència. No cal que siguin fórmules com «i per què?» o «i què més?» si no aporten un dubte concret.

No inventis una biografia, una feina, una opinió o una experiència personal de l'usuari. La naturalitat ha de venir de la pregunta, no d'un escenari fabricat.

## Escriu la resposta

- Comença per contestar la pregunta.
- Usa llenguatge corrent i frases completes.
- No responguis amb un títol, un fragment o una llista de camps.
- No afegeixis fets només perquè apareixen a la mateixa fitxa.
- Separa les dades dels relats tradicionals, les interpretacions i les hipòtesis.
- Si la font no permet resoldre el dubte, digues què se sap i què queda sense saber.
- No presentis una coincidència temporal com a causa.
- Mantén les xifres amb la unitat correcta: recompte, percentatge o punts percentuals.

## Exemples de calibratge

Els tres fils de `../examples/conversations.jsonl` mostren preguntes sobre un canvi, una lectura de conjunt i dues mesures que es poden confondre. Serveixen per calibrar l'estil; no es copien a la cua ni compten com a registres entrenables.

## Revisió obligatòria

Abans d'afegir una línia a `conversations.jsonl`, comprova:

- La pregunta inicial s'entén sense consultar una fitxa?
- La preguntaria una persona que vol resoldre aquest dubte?
- Cada seguiment neix de la resposta anterior i afegeix un pas nou?
- El fil té entre dos i quatre intercanvis i s'atura quan el dubte queda resolt?
- Cada resposta contesta directament, sona natural i és completa?
- Les afirmacions tenen suport en fonts reutilitzables i traçables?
- La resposta conserva els límits i les incerteses de les fonts?
- El fil continua tenint sentit si se n'esborren títols, IDs i procedència?
- No és una paràfrasi gairebé duplicada d'un registre existent?

Un «no» vol dir que cal reescriure, deixar pendent o excloure la conversa.
