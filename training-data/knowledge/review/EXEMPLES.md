# Exemples de calibratge

Aquests exemples mostren converses multitorn que parteixen d'un dubte i mantenen el fil. No són candidats, no compten per a cobertura i no s'exporten. Les fonts i l'abast de cada resposta són a [`examples-provenance.md`](examples-provenance.md).

## 1. La Marratxa i el recipient del nom

```json
{"messages":[{"role":"user","content":"La Marratxa encara es balla amb el recipient de perfum, o només n'ha quedat el nom?"},{"role":"assistant","content":"Només n'ha quedat el nom. La marratxa era un recipient d'aigua perfumada que els dansaires duien antigament, però avui l'objecte ja no forma part del ball."},{"role":"user","content":"I que es ballés per primer cop el 1278 ho sabem del cert?"},{"role":"assistant","content":"No. La tradició situa el primer ball el 7 de setembre de 1278, però el corpus no ho verifica amb una font primària. A més, el Pareatge se situa el 8 de setembre. La relació amb el 1278 s'ha d'explicar com una tradició, no com una data demostrada."}]}
```

**Per què funciona:** la primera pregunta surt d'una confusió plausible entre el nom i l'objecte. El seguiment pregunta si l'origen que suggereix el ball és un fet comprovat.

## 2. Més gent al cinema: augment continu o dues fotografies?

```json
{"messages":[{"role":"user","content":"Sembla que el 2024 hi havia més gent que anava al cinema que el 2019. Vol dir que l'assistència ha anat pujant cada any?"},{"role":"assistant","content":"No ho podem saber amb aquestes dades. L'enquesta indica que hi va el 57,4% el 2019 i el 66,3% el 2024, però només compara aquests dos anys."},{"role":"user","content":"Aleshores no sabem quan va créixer ni si va baixar mentrestant?"},{"role":"assistant","content":"Exacte. Sense observacions dels anys intermedis, no es pot reconstruir el recorregut ni dir si l'augment va ser gradual, sobtat o amb alts i baixos."}]}
```

**Per què funciona:** la primera pregunta comprova una conclusió que sovint es treu d'una comparació. El seguiment concreta què falta per saber, sense canviar de tema.

## 3. Menys visites a biblioteques, més persones inscrites?

```json
{"messages":[{"role":"user","content":"No acabo d'entendre les dades de biblioteques: l'enquesta diu que hi va menys gent, però les inscripcions han pujat. Com poden ser certes totes dues coses?"},{"role":"assistant","content":"Perquè compten coses diferents. L'enquesta pregunta a les persones si hi han anat; el registre compta quanta gent està inscrita. Entre 2019 i 2024, la primera proporció baixa del 36,4% al 30,7%, mentre les inscripcions passen de 25.038 a 29.364."},{"role":"user","content":"I els inscrits també s'enduien més llibres?"},{"role":"assistant","content":"En total, sí: els préstecs de llibres passen de 29.945 el 2016 a 37.270 el 2024. Però no podem dir que cada persona n'agafés més: la mitjana disponible per persona inscrita agrupa tots els documents, no només els llibres, i baixa de 2,01 a 1,39. A més, aquesta mitjana i el total de préstecs cobreixen 2016–2024; l'enquesta només compara 2019 i 2024."}]}
```

**Per què funciona:** l'usuari assenyala una contradicció concreta. La resposta distingeix dues mesures; el seguiment pregunta per una conseqüència relacionada i la resposta separa volum total de mitjana per persona.

## Quan no afegir un seguiment

No allarguis una conversa només perquè volem entrenar diàleg. Si la resposta tanca el dubte i no desperta una pregunta concreta, deixa el fil en un intercanvi. Naturalitat abans que longitud.

## Exemples que es descarten

| Pregunta | Motiu |
|---|---|
| «Què explica la secció “El relat” de la fitxa de Meritxell?» | Demana navegar l'estructura interna d'un document. |
| «Què indica aquesta fila?» | No identifica ni el dubte ni què es compara. |
| «I dos topònims que en surten:» | És un fragment, no una pregunta. |
| «Digues tres dades sobre la Marratxa.» | Demana extreure informació sense una intenció clara. |
| «La Marratxa és una dansa? Quin dia es balla? Qui la va coreografiar?» | Ajunta dubtes independents sense construir una conversa. |
