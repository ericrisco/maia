# Criteri per escriure converses de Maia Knowledge

Els registres rebutjats de la primera tanda són a `../archive/rejected-v1/`. Les mostres editorials actuals són a [`../examples/conversations.jsonl`](../examples/conversations.jsonl), amb procedència a [`../examples/provenance.jsonl`](../examples/provenance.jsonl). No són exportables: algunes fonts tenen redistribució denegada o pendent.

## Comprovació principal

Llegeix només les preguntes, com si no haguessis vist cap document. Si sonen com una pregunta d'examen sobre una secció, una fila o un títol, la conversa no serveix. Si una persona podria fer la pregunta en aquella situació i cada resposta li dona peu a un seguiment real, el fil funciona.

## Mostra bona: dubte d'una persona que hi va

```text
Usuari: Vaig a la festa major de Sant Julià i m'han dit que hi ha la Passa. Què és exactament?
Assistent: És una cercavila de parelles de fadrins pels carrers principals de Sant Julià de Lòria. No és un ball.
Usuari: I per què tothom parla dels majors fadrins?
Assistent: Perquè les parelles que es casaran aquell any encapçalen la cercavila i reben aquest nom. Darrere seu, les altres parelles van de més grans a més joves.
Usuari: La podré veure qualsevol dia de la festa?
Assistent: La Passa es fa al migdia del dilluns de la festa major.
```

El primer torn desfà una confusió plausible. Els seguiments demanen ordre i horari perquè la persona vol entendre què veurà.

## Mostra bona: paraula trobada en una font

```text
Usuari: Estic llegint un text antic i hi surt la paraula «peixena». Vol dir que els ramats podien passar per qualsevol camp?
Assistent: No per qualsevol camp. La peixena era el dret de pas i de pastura dels habitants sobre terres que no eren «de guarda». S'exercia després de la collita, quan el camp quedava buit.
Usuari: Aleshores, si la terra era meva, podia canviar què hi plantava?
Assistent: No necessàriament. La font diu que el propietari no podia canviar la rotació de conreus ni plantar-hi farratge sense autorització del consell de parròquia. El dret de pastura també condicionava l'ús privat de la terra.
```

El seguiment explora la conseqüència pràctica del terme; no demana que es reciti la secció d'un article.

## Mostra bona: entendre una regla històrica

```text
Usuari: En un plet antic entre un veí i un comú, el cas anava sempre als tribunals ordinaris?
Assistent: No: segons la regla que descriu la font, depenia de qui presentava la demanda. Si el particular demandava el comú o un quart, l'afer anava a la jurisdicció política. Si el comú o el quart demandava un particular, anava als tribunals ordinaris.
Usuari: I si el conflicte era amb un quart, qui el resolia primer?
Assistent: Primer el consell de parròquia; després es podia apel·lar al Consell General. Si la part interessada era una parròquia sencera, l'afer anava directament al Consell General.
```

La primera resposta contesta la comparació i explica el criteri. El seguiment concreta una branca de la regla.

## No fer això

```text
Usuari: Què explica la secció «El vocabulari que ho ordena» de la fitxa «Un camp és comunal perquè hi passen els ramats»?
Assistent: I dos topònims que en surten:
```

Aquesta pregunta pressuposa que l'usuari té la fitxa oberta; la resposta no resol el dubte ni és una frase completa. Cal començar pel terme o la situació que interessa a una persona.

## Regles de mida i to

- Comença per la pregunta humana, no per la taxonomia del corpus.
- Respon abans d'afegir context; defineix termes locals sense convertir la resposta en glossari.
- Fes servir seguiments que aprofundeixin o concretin. «I això quan passa?» només funciona si el torn anterior dona un referent clar.
- No forcis una tercera pregunta. Dos torns d'usuari ben connectats són millors que quatre de plantilla.
- No presentis com a fet una interpretació d'una font ni completis un buit amb intuïcions.
- Llegeix en veu alta les preguntes. Si un parlant les trobaria artificials, reescriu-les.
