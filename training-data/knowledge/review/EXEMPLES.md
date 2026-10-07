# Exemples de calibratge per a Maia Knowledge

Aquests exemples fixen el llindar editorial. No són registres aprovats, no compten per a cobertura i no s'exporten. Les dades i els límits s'han de poder rastrejar a les fitxes indicades a [`examples-provenance.md`](examples-provenance.md).

La prova principal és llegir només les intervencions d'usuari. Han de semblar una consulta amb sentit propi, i el seguiment ha de sortir del que Maia acaba de respondre.

## 1. El nom de la Marratxa i el ball d'avui

```json
{"messages":[{"role":"user","content":"La Marratxa encara es balla amb una marratxa a la mà, o només n'ha quedat el nom?"},{"role":"assistant","content":"Només n'ha quedat el nom. La marratxa era un recipient d'aigua perfumada que els dansaires duien antigament; avui ja no es fa servir en el ball."},{"role":"user","content":"I els passos que es ballen ara són els mateixos de sempre?"},{"role":"assistant","content":"No es pot assegurar. La versió actual es va fixar als anys seixanta: Daniel Areny va recollir la tonada de la memòria del dansaire Ricard Mas, i Isidre Marbà en va harmonitzar la música i en va crear la coreografia. No hi ha prou documentació per afirmar que aquests passos siguin els del segle XIII."}]}
```

**Per què passa:** la primera pregunta surt d'una confusió natural entre el nom i l'objecte. El seguiment pregunta per la continuïtat que suggereix la paraula «encara»; la resposta distingeix la pràctica documentada de l'origen llegendari.

## 2. Més inscrits, menys gent que diu que hi va

```json
{"messages":[{"role":"user","content":"No ho acabo d'entendre: l'enquesta diu que menys gent va a les biblioteques, però els usuaris inscrits han pujat. Com pot ser?"},{"role":"assistant","content":"No necessàriament es contradiuen: mesuren coses diferents. L'enquesta pregunta si la persona hi ha anat; el registre administratiu compta inscripcions. La proporció que diu que hi va baixa del 36,4% el 2019 al 30,7% el 2024, mentre que les inscripcions passen de 25.038 a 29.364."},{"role":"user","content":"I amb més inscrits s'enduien més llibres?"},{"role":"assistant","content":"Si mirem del 2016 al 2024, sí: el total de préstecs de llibres puja de 29.945 a 37.270. Però això no vol dir que cada persona n'agafés més. En el mateix període, la mitjana de préstecs a domicili de tots els documents per persona inscrita baixa de 2,01 a 1,39. L'enquesta cobreix 2019-2024; les dades de préstecs i inscripcions, 2016-2024."}]}
```

**Per què passa:** la pregunta expressa una contradicció percebuda. El seguiment reprèn la distinció entre inscriure's i utilitzar el servei; no demana una llista de xifres de la fitxa.

## 3. Dos anys no són una tendència anual

```json
{"messages":[{"role":"user","content":"Sembla que hi va més gent al cinema el 2024 que el 2019. Podem dir que ha anat pujant cada any?"},{"role":"assistant","content":"No. La proporció que diu que va al cinema passa del 57,4% el 2019 al 66,3% el 2024, però les dades només comparen aquests dos anys. No mostren què va passar entremig ni quan es va produir l'augment."},{"role":"user","content":"Aleshores tampoc no sabem si va ser un canvi gradual o d'un sol cop?"},{"role":"assistant","content":"Exacte. Només tenim dues onades, la del 2019 i la del 2024. No es pot reconstruir l'evolució entre totes dues ni atribuir la diferència a una causa concreta."}]}
```

**Per què passa:** l'usuari pregunta per una conclusió que les dades no permeten treure. El seguiment precisa el mateix límit; no canvia de tema ni força una explicació.

## Quan un sol intercanvi és suficient

No afegeixis un seguiment perquè el format sigui «multitorn». Si la pregunta era «La Marratxa encara es balla a Sant Julià?», una resposta directa sobre el dilluns de festa major pot tancar la consulta. Un fil curt ben resolt és millor que una segona pregunta ornamental.

## Exemples de preguntes que es descarten

| Pregunta rebutjada | Motiu |
|---|---|
| «Què explica la secció “El relat” de la fitxa de Meritxell?» | Depèn que l'usuari conegui la fitxa i la seva estructura. |
| «Què indica aquesta fila?» | No diu què es compara ni quin dubte vol resoldre. |
| «I dos topònims que en surten:» | És un fragment, no una pregunta. |
| «Enumera els fets principals de la Marratxa.» | Demana una extracció, sense una motivació identificable. |
| «La Marratxa és una dansa? I quin dia es balla? I qui la va coreografiar?» | Acumula consultes independents en una sola intervenció. Cal separar-les si cada dubte té valor propi. |

Si una pregunta falla, no l'arreglis només canviant el títol per una frase més col·loquial. Reescriu el dubte des de la necessitat de qui pregunta o descarta el registre.
