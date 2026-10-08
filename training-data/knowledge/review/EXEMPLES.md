# Calibratge de converses Knowledge

Aquest document fixa com ha de sonar una conversa, no com s'ha de transformar cada paràgraf en una pregunta. Els exemples aprovats de calibratge són a [`../examples/conversations.jsonl`](../examples/conversations.jsonl); la seva traçabilitat i l'estat dels drets són a [`../examples/provenance.jsonl`](../examples/provenance.jsonl). No s'exporten.

## La prova decisiva: quin dubte resol aquest diàleg?

Abans de redactar, resumeix la intenció de l'usuari sense esmentar el corpus. Si només pots descriure la intenció com «saber què diu la secció/fila/fitxa», encara no tens una pregunta humana.

Una bona conversa té un fil: una curiositat plausible, una resposta que la resol, i una repregunta que surt d'aquella resposta i permet entendre una altra cosa. La persona no ha de conèixer la font ni parlar com si estigués fent un examen. Evita fórmules com «Què explica…», «Què indica aquesta fila?», «Quins elements s'hi esmenten?» i «El document diu…» quan el dubte real es pot formular directament.

La resposta inicial no ha de retenir fets per fer que la repregunta sembli necessària. El seguiment no demana simplement una altra dada adjacent per omplir un mínim de torns: posa a prova una inferència, aclareix una conseqüència, compara amb sentit o pregunta per un límit que la primera resposta ha fet rellevant. Si no hi ha aquesta repregunta, la conversa encara no està llesta com a exemple multitorn.

## Exemples de calibratge

Els exemples complets i basats en fonts es mantenen en JSONL a `../examples/conversations.jsonl`. A continuació, s'explica què fa bé un tipus de diàleg i què s'ha de rebutjar.

### Exemple de bon fil: tradició antiga i dansa actual

**Intenció:** destriar l'origen tradicional atribuït a la Marratxa de la història documentada de la coreografia actual.

**User:** «La Marratxa que es balla avui és la mateixa que es ballava quan es va signar el Pareatge?»

**Assistant:** «No es pot assegurar. La tradició relaciona la dansa amb el Pareatge de 1278, però les fonts no demostren que la coreografia actual vingui d'aquell moment. La versió que es balla avui es va fixar als anys seixanta a partir de la memòria d'un dansaire.»

**User:** «Aleshores el 1278 és una data que explica la tradició, no una prova de com era el ball?»

**Assistant:** «Exacte. És la data que li atribueix la tradició. A més, la data del ball —7 de setembre— no coincideix amb la del Pareatge que dona una altra font —8 de setembre—. La discrepància continua oberta.»

El primer torn no afirma continuïtat que no està documentada; el seguiment comprova què significa la distinció. Les dades i els drets d'aquest exemple continuen subjectes a la fitxa de procedència.

### Exemple de bon fil: un nom que sobreviu a l'objecte

**Intenció:** entendre una paraula poc coneguda i esbrinar què se'n pot dir més.

**User:** «Què és una marratxa? És d'aquí que ve el nom del ball?»

**Assistant:** «Sí. La marratxa —també anomenada morratxa o almorratxa— és un recipient amb aigua perfumada que, segons la descripció de la dansa, els balladors duien a les mans. El ball n'ha conservat el nom, tot i que avui ja no s'hi fa servir el recipient.»

**User:** «Se sap quin perfum hi posaven?»

**Assistant:** «La informació disponible explica que l'aigua era perfumada, però no identifica cap perfum concret.»

La repregunta surt d'una part concreta de la resposta i permet mostrar un límit real sense omplir-lo amb una suposició.

### Exemple de bon fil: una simbologia que no quadra a primera vista

**Intenció:** entendre qui participa en la Marratxa i no atribuir una correspondència inventada.

**User:** «Què representen els dansaires de la Marratxa?»

**Assistant:** «La descripció atribueix als dos homes la representació dels coprínceps i diu que les tres noies simbolitzen les sis parròquies antigues.»

**User:** «I se sap quines parròquies representa cadascuna?»

**Assistant:** «No. La descripció no explica com es reparteix aquesta representació entre les tres noies.»

El seguiment detecta una pregunta natural provocada per la resposta. No s'inventa una explicació només perquè la simbologia sembli incompleta.

## Anti-exemples que s'han de rebutjar

| Pregunta o resposta rebutjada | Per què falla | Com corregir el plantejament |
| --- | --- | --- |
| «Què explica la secció “La regla de competència”?» | La persona coneix l'organització interna d'una fitxa. | Identifica el dubte sobre qui podia jutjar o recórrer i formula'l directament. |
| «Què indica aquesta fila?» | No té context fora de la taula i no diu què vol saber. | Pregunta per la comparació o el canvi que la dada ajuda a entendre; anomena any i sèries si cal. |
| «Què va passar al relat?» | Converteix un encapçalament en pregunta, sense cap intenció humana. | Pregunta per una acció o conseqüència que algú voldria entendre; mantén els referents explícits. |
| «Tres coses que el corpus registra per separat:» | No és una resposta i parla del procés intern. | Respon directament el dubte real amb una frase completa. |
| «Quan i on es balla?» → «A la una, a la plaça Major.» | Pot servir com una dada puntual, però aïllada no forma un diàleg humà ni situa la tradició. | Parteix d'una curiositat contextual i continua només amb una repregunta que n'aclareixi el sentit o un detall rellevant. |
| «I què més?» / «Quins altres detalls hi ha?» | El seguiment no té objectiu i demana una llista indefinida. | Pregunta per la implicació específica de la resposta anterior. |
| «Ahir ho vaig veure a la plaça. Per què…?» quan la font no ho diu | Inventa una experiència personal per fer més vistosa la pregunta. | Elimina l'anècdota fictícia; formula la curiositat directament. |
| Resposta: «Apel·lació al Consell General.» | Fragment sense actor, relació ni context. | Explica qui podia apel·lar i en quines circumstàncies, només fins on arribi la font. |

## Llengua i contingut de les respostes

- Contesta primer la pregunta actual; no comencis per «segons la fitxa» ni «el corpus diu».
- Escriu català natural i oral, sense exagerar col·loquialismes ni fingir una veu personal.
- Dona el context que evita una resposta telegràfica, però no descarreguis tota la font en cada torn.
- Escriu noms, dates, llocs, xifres i referents de manera inequívoca.
- Presenta com a tradició el que la font presenta com a tradició; no ho converteixis en fet provat.
- Quan una dada no consta, digues exactament què manca. No transformis l'absència de prova en prova que una cosa no va passar.
- Corregeix amb tacte una premissa falsa i respon la pregunta que la persona probablement volia fer.

## Revisió abans d'acceptar

Llegeix només la conversa, sense obrir les fonts, i comprova:

1. La persona podria tenir aquest dubte sense haver vist la fitxa?
2. La conversa té un sol fil recognoscible, sense salts de tema ni preguntes de qüestionari?
3. La primera resposta resol el dubte completament?
4. El seguiment surt de la resposta i aporta una comprensió nova?
5. Tots els torns s'entenen per si sols en el context del diàleg?
6. La resposta distingeix el que se sap, el que s'atribueix i el que queda obert?

Després contrasta cada afirmació amb les fonts i comprova la procedència i els drets. Si falla qualsevol punt, reescriu la conversa sencera o deixa-la pendent. Una pregunta més bonica no corregeix una afirmació sense base.
