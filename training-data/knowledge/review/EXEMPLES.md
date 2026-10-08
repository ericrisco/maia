# Guia editorial i exemples de Maia Knowledge

Aquesta guia fixa com ha de sonar una conversa abans d'afegir registres. Les converses de `conversations.jsonl` són candidates; l'estat i la procedència de cadascuna es consulten a `provenance.jsonl`.

## La prova principal

Amaga el nom de la fitxa i llegeix només els missatges. Si la pregunta sembla una consigna d'examen, si pressuposa que l'usuari té un article al davant, o si el seguiment només serveix per allargar el diàleg, no passa.

Una pregunta humana sol néixer d'una cosa que la persona ha vist, sentit o vol aclarir. Pot contenir una confusió. No cal fer veure que coneixem la vida de qui pregunta.

## Conversa útil: una confusió que surt d'un programa

```text
Usuari: He vist la Passa i la Marratxa al programa de dilluns. Són les dues danses?
Assistent: No. La Marratxa és una dansa; la Passa és una cercavila de parelles de fadrins. Les parelles que es casaran aquell any van al davant i la resta segueix per edat.
Usuari: I la Passa no té passos de ball?
Assistent: La descripció disponible la presenta com una cercavila, no com una dansa, i no descriu passos de ball. Tampoc concreta si hi ha música o moviments ritualitzats durant el recorregut.
```

La pregunta neix d'una confusió plausible entre dos actes del mateix programa. La resposta separa els actes i no inventa coreografia.

## Conversa útil: una discrepància que no s'ha de tapar

```text
Usuari: He sentit que la Marratxa commemora el Pareatge, però trobo el 7 i el 8 de setembre. Quina data és la bona?
Assistent: Les fonts recollides no coincideixen: la tradició de la Marratxa la situa el 7 de setembre de 1278, i la fitxa del Pareatge data la signatura a Lleida el 8 de setembre. La discrepància no està resolta.
Usuari: Així, tampoc no sabem segur que la dansa es ballés després de signar-lo?
Assistent: Exacte. La primera ballada forma part del relat tradicional, però la documentació consultada no la prova com a fet històric.
```

La resposta distingeix tradició i fet documentat. No tria una data per fer desaparèixer la discrepància.

## Conversa útil: una inferència que va massa lluny

```text
Usuari: M'han dit que a la Passa les parelles que es casen aquell any van al davant. I la resta com s'ordena?
Assistent: La resta va darrere, de més grans a més joves. Les parelles que es casen aquell any s'anomenen «majors fadrins» i obren la cercavila.
Usuari: Aleshores els majors fadrins organitzen la festa?
Assistent: No ho podem assegurar. La informació disponible deixa aquesta qüestió oberta i no documenta quines funcions tenen durant la festa.
```

La resposta corregeix la inferència sense presentar una hipòtesi com a fet.

## Conversa que rebutgem

```text
Usuari: Què explica la secció «Què és» de la fitxa «La Passa»?
Assistent: És una cercavila de parelles de fadrins.
Usuari: I què més?
Assistent: Van ordenats per edat.
```

Aquesta forma exigeix conèixer la fitxa, la primera resposta queda curta i el seguiment no té una curiositat concreta.

## Llista de control abans d'aprovar

- La pregunta inicial s'entén sense títol, secció ni ID de font.
- El dubte sembla una cosa que algú voldria aclarir en una conversa normal.
- La resposta contesta primer i afegeix només el context que ajuda.
- Cada seguiment neix del torn anterior i aporta alguna cosa nova.
- Cap torn no repeteix la mateixa dada amb paraules diferents.
- Les premisses falses es corregeixen amb tacte.
- Les dades, dates i límits coincideixen amb les fonts.
- Les fonts i drets permeten l'ús previst, i això consta a `provenance.jsonl`.
- Llegida sense metadades, la conversa no sembla una fitxa transformada en qüestionari.

Una conversa que no passa un punt es reescriu o es descarta. No es compensa una pregunta artificial amb una resposta correcta.
