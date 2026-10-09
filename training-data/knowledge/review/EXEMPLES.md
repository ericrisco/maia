# Mostres de conversa per a Maia Knowledge

Les converses de `../examples/conversations.jsonl` marquen el to desitjat. Són mostres editorials amb procedència a part. No s'han de copiar al dataset ni comptar com a cobertura.

## Abans d'afegir un registre

Llegeix la conversa sense obrir les fitxes. La primera pregunta ha de tenir sentit per si sola. El seguiment ha de sortir del que acaba de dir l'assistent i demanar una cosa que encara no s'ha respost. La resposta ha de contestar primer i explicar després, només si cal.

Pregunta't: «Ho preguntaria així a algú que en sap?». Si el dubte només existeix perquè algú està llegint una secció o una taula, busca la pregunta humana que hi ha al darrere. Si no n'hi ha cap, no en facis un exemple.

## Exemple de visita

```text
Usuari: Dilluns de festa major seré a Sant Julià i m'han dit que hi ha la Passa. És un ball?
Assistent: No ben bé: la Passa és una cercavila de parelles de fadrins pels carrers principals de Sant Julià de Lòria. Es fa el mateix dia que alguns balls, però no és una dansa.
Usuari: I qui encapçala la cercavila?
Assistent: Les parelles que es casaran aquell any, que s'anomenen els majors fadrins. Després van les altres parelles, ordenades de més grans a més joves.
Usuari: A quina hora hauria d'hi ser?
Assistent: Al migdia de dilluns. És quan se celebra la Passa durant la festa major.
```

## Exemple per entendre una regla antiga

```text
Usuari: En una sentència antiga, els pastors passen amb els ramats per un camp després de la collita. Això vol dir que el terreny era comunal?
Assistent: En la sentència de 1790 que recull el corpus, aquest pas dels ramats després de retirar els fruits és justament l'argument per considerar comunal el terreny, encara que s'hi hagués sembrat durant anys.
Usuari: I el propietari podia plantar-hi el que volgués?
Assistent: No. La peixena donava als habitants dret de pas i de pastura, i el propietari no podia canviar la rotació de conreus ni plantar-hi farratge sense autorització del consell de parròquia.
```

## Exemple de dubte sobre una norma

```text
Usuari: Al segle XIX, si un cònsol et devia diners, el podies portar directament davant d'un jutge?
Assistent: No sempre. La regla que descriu la font exigia autorització prèvia per iniciar una reclamació civil contra una autoritat. Després de la Reforma de 1866, aquesta exigència es va limitar als deutes contrets en virtut del càrrec.
Usuari: I si l'acusaves d'un delicte, també calia demanar permís?
Assistent: No segons aquesta mateixa font: l'autorització prèvia s'exigia per a les accions civils, però no per a les persecucions criminals. La font no explica per què es feia aquesta distinció.
```

## Exemple que resol una aparent contradicció

```text
Usuari: Si ara no hi ha lliga femenina de futbol a Andorra, on juga l'ENFAF?
Assistent: La font situa l'ENFAF a la lliga catalana: el primer equip juga a la Primera Divisió Femenina de Catalunya i el filial, a la Segona.
Usuari: I no hi ha hagut mai una competició femenina al país?
Assistent: Sí que n'hi va haver una durant la temporada 2010–11. El corpus no en concreta el format ni els equips, ni explica per què no va continuar.
```

## Exemple sobre una pèrdua històrica

```text
Usuari: La imatge de Meritxell que es venera avui és la talla medieval original?
Assistent: No. La talla romànica del segle XII es va perdre quan el santuari antic es va incendiar la nit del 8 al 9 de setembre de 1972. La imatge actual és una rèplica.
Usuari: Qui va fer la rèplica i quan es va obrir el santuari nou?
Assistent: La rèplica és obra de l'escultor Sergi Mas. El santuari nou, projectat per Ricard Bofill, es va inaugurar el 1976.
```

## No fer això

```text
Usuari: Què explica la secció «El vocabulari que ho ordena» d'una fitxa sobre camps i ramats?
Assistent: I dos topònims que en surten:
```

La pregunta depèn d'una fitxa que l'usuari no ha esmentat i la resposta no contesta res. Cal identificar quin terme o dubte podria interessar-li a una persona i començar per aquí. No afegir seguiments per obligar el registre a ser multitorn.
