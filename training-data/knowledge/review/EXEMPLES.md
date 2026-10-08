# Criteri de calibratge de Maia Knowledge

Aquests exemples mostren el tipus de conversa que volem: una persona pregunta una cosa que realment necessita aclarir; la resposta resol el dubte; el seguiment surt d'allò que s'acaba de dir. Són mostres de criteri, no plantilles per copiar.

## Què fa que soni humà

- La pregunta té sentit fora del corpus i sense haver llegit cap fitxa.
- El context és suficient però no teatral. No inventem qui és l'usuari, on va, què sent ni què ha llegit.
- El seguiment reprèn una idea concreta de la resposta anterior.
- Cada resposta és completa per si sola. No deixem una dada important per al torn següent.
- Quan les fonts no resolen una qüestió, la resposta ho diu amb precisió i sense convertir el buit en una certesa.

## Exemples de referència

### Distingir dues tradicions

```json
{"messages":[{"role":"user","content":"La Passa i la Marratxa són dos balls de Sant Julià?"},{"role":"assistant","content":"Només la Marratxa és un ball. La Passa és una cercavila de parelles de fadrins; totes dues formen part del dilluns de la festa major de Sant Julià de Lòria."},{"role":"user","content":"I com s'ordena la gent a la Passa?"},{"role":"assistant","content":"Al davant hi van les parelles que es casaran aquell any, conegudes com a «majors fadrins». Darrere seu, les altres parelles desfilen de més grans a més joves."}]}
```

### Aclarir què va passar amb un objecte

```json
{"messages":[{"role":"user","content":"La imatge de Meritxell que es venera avui és la talla medieval original?"},{"role":"assistant","content":"No. La talla original, del segle XII, es va perdre en l'incendi del santuari la nit del 8 al 9 de setembre de 1972. La imatge actual és una rèplica."},{"role":"user","content":"Se sap qui va fer la rèplica?"},{"role":"assistant","content":"Sí. La va fer l'escultor Sergi Mas. El santuari nou, projectat per Ricard Bofill, es va inaugurar el 1976."}]}
```

### Comparar versions sense inventar-ne una de definitiva

```json
{"messages":[{"role":"user","content":"He trobat dues explicacions diferents de l'argument de l'Ossa d'Encamp. Quina és la bona?"},{"role":"assistant","content":"Les fonts consultades descriuen versions diferents i no permeten donar-ne una com a definitiva. Joan Amades, el 1950, explica que l'ós s'acosta a un rusc de cartó i un caçador el mata. Una altra font descriu una cacera de l'ossa per les muntanyes amb contingut sexual."},{"role":"user","content":"Això vol dir que l'obra va canviar amb els anys?"},{"role":"assistant","content":"Les descripcions no coincideixen, però no permeten establir quan ni per què va canviar l'argument, ni quina versió és la més antiga. És més exacte parlar de relats diferents que no pas donar per resolta la seva evolució."}]}
```

### Separar una versió actual d'una tradició antiga

```json
{"messages":[{"role":"user","content":"La Marratxa que es balla avui conserva una coreografia antiga?"},{"role":"assistant","content":"La coreografia actual es va fixar als anys seixanta. Ricard Mas, dansaire del ball durant més de vint anys, va conservar-ne els passos i la música. El compositor Daniel Areny va recollir de la seva memòria les variacions de la tonada, i Isidre Marbà les va harmonitzar i hi va crear una coreografia. L'Esbart Laurèdia la interpreta des del 1963."},{"role":"user","content":"Aleshores sabem que la dansa va començar als anys seixanta?"},{"role":"assistant","content":"No. Aquesta data correspon a la fixació de la versió actual, no pas a l'origen de la dansa. La tradició la situa el 7 de setembre de 1278, però la fitxa del Pareatge dona el 8 de setembre; el corpus registra la discrepància i no la resol."}]}
```

### Respondre amb honestedat quan falta una dada

```json
{"messages":[{"role":"user","content":"Quina música acompanya el ball de l'Ossa d'Encamp?"},{"role":"assistant","content":"Les fonts consultades no identifiquen la música ni els instruments propis de la representació d'Encamp. La descripció general de la UNESCO esmenta música en les festes de l'ós dels Pirineus, però no concreta el repertori d'Encamp."},{"role":"user","content":"Per tant, durant la representació no hi ha música?"},{"role":"assistant","content":"Això no es pot concloure. Les fonts consultades no indiquen quina música hi sona; que no en detallin el repertori no vol dir que no n'hi hagi."}]}
```

## Exemples que no passen el criteri

- «Què explica la secció “El relat” de la fitxa de Meritxell?» — depèn de conèixer un document intern.
- «Què indica aquesta fila?» — no explica quin dubte vol resoldre i no té referent.
- «2014 — verd, 57,7 — morat, 56,4» — és una resposta fragmentària sense context ni explicació.
- «I dos topònims que en surten:» — no és una pregunta completa.
- Afegir «vaig a visitar-ho aquest cap de setmana» si la resposta no necessita ni pot resoldre aquesta situació — context inventat que no aporta res.
- Fer una segona pregunta d'un altre tema només per arribar a dos torns — conversa forçada.
- Repetir «Què és X?» per a cada fitxa — plantilla recognoscible, no diversitat real.

## Porta d'entrada

Abans d'afegir una conversa a `review/`, comprova els punts del [pla](../../PLAN.md), valida cada afirmació contra el corpus i registra les fitxes font i els drets a `work/provenance.jsonl`. Si el diàleg no se sosté tot sol, reescriu-lo o descarta'l. Aquestes mostres de calibratge tampoc no passen a `output/` automàticament.
