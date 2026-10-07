# Pla de treball: converses que una persona iniciaria

## Objectiu

Crear dos conjunts separats a partir de `docs/`:

- **Maia Knowledge**: respostes fiables sobre Andorra, basades en `docs/temes/`.
- **Maia Language**: llengua oral andorrana autèntica, basada en peces de
  `docs/parla/` que compleixin els criteris de veu, època, aptitud i drets.

La unitat de treball és una conversa amb una intenció clara. No és un paràgraf
convertit en pregunta. No cal que cada registre tingui diversos torns.

## La prova de naturalitat

Abans d'escriure, completa aquesta frase:

> Algú preguntaria això perquè vol entendre, decidir o aclarir ______.

Si només hi cap «perquè ho diu una secció de la fitxa», descarta la pregunta.
L'usuari no ha de saber que existeix una fitxa, un gràfic o una secció, tret que
la conversa parli explícitament d'aquella font.

Una pregunta bona normalment parteix d'algun d'aquests motius:

- una xifra sembla contradictòria;
- una idea comuna pot ser errònia;
- la persona vol entendre com funciona una cosa;
- necessita distingir dues coses semblants;
- vol situar un fet en el temps o en el lloc;
- una resposta anterior li ha obert una pregunta concreta.

No inventis que la persona ha visitat un lloc, ha tastat un plat o ha llegit un
article. Una situació quotidiana pot donar context, però no ha de fingir una
experiència real de l'usuari.

## Com fer una conversa multitorn

1. Escriu la pregunta inicial com la diria algú en una conversa normal.
2. Contesta-la directament, amb una frase completa i el context necessari.
3. Afegeix un altre torn només si una persona podria tenir aquella rèplica
   després de llegir la resposta.
4. Fes que el seguiment reprengui una dada o una distinció de la resposta.
5. Acaba quan el dubte queda resolt. No allarguis el diàleg per omplir torns.

El seguiment ha d'afegir una funció: aclarir una conseqüència, provar una
interpretació, demanar una comparació o preguntar pel límit del que se sap.
«I què més?» no és una funció.

## Com redactar la resposta

- Comença pel punt principal. No comencis amb una etiqueta ni amb un fragment.
- Escriu com un assistent que coneix el tema, no com una fitxa ni un catàleg.
- Dona només els detalls que resolen el dubte i ajuden a entendre'l.
- Corregeix premisses falses amb naturalitat i sense renyar.
- Separa el fet documentat de la interpretació, la tradició o la incertesa.
- Si el corpus no permet una conclusió, digues quin límit té la informació.
- No afegeixis fets que no es puguin recolzar en les fonts de Maia.

## Prova en veu alta

Llegeix els torns seguits, sense mirar l'article. Revisa:

1. **Intenció:** s'entén què vol saber l'usuari i per què?
2. **Naturalitat:** ho diria una persona, sense conèixer l'estructura del corpus?
3. **Fil:** la resposta contesta la pregunta i el seguiment reprèn el fil?
4. **Claredat:** cada resposta s'entén sense consultar el títol de la font?
5. **Fidelitat:** cada afirmació està sostinguda per les fonts indicades?
6. **Proporció:** la resposta té prou context, sense convertir-se en un resum?

Si falla qualsevol punt, reescriu o descarta el registre. La varietat de temes
no compensa preguntes artificials.

## Cobertura sense qüestionari

Inventaria els fets rellevants de totes les fonts. Relaciona cada fet amb una
conversa aprovada o registra per què no s'ha convertit en pregunta. No forcis
una pregunta per cada paràgraf, xifra o fila. Agrupa fets quan una persona els
demanaria junts. Conserva a l'auditoria els detalls que no donen peu a una
conversa natural.

La cobertura es revisa per fet, no pel nombre de fitxes amb un exemple. Abans
d'afegir un registre, comprova també si ja hi ha una conversa que ensenya el
mateix punt amb una intenció equivalent.

## Separació dels dos datasets

### Maia Knowledge

Les preguntes poden ser redactades i les respostes poden resumir o explicar,
però els fets han de provenir de `docs/temes/`. Cada conversa necessita una
procedència revisable i drets compatibles. A l'exportació final només hi van
els missatges de conversa.

### Maia Language

La resposta ha de preservar parla humana autèntica. No inventis preguntes per
transformar un monòleg en entrevista. No demanis a un LLM que imiti com
parlaria una persona andorrana. Exclou o filtra fragments amb transcripció
dubtosa segons la política documentada. Mantén fragments de la mateixa peça o
parlant al mateix split.

## Estructura de treball

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── review/       # converses candidates, exemples i procedència
│   ├── work/         # inventari i mapa de cobertura
│   ├── output/       # només registres aprovats per entrenar
│   └── reports/      # cobertura, drets i qualitat
└── language/
    ├── review/       # fragments i decisions d'inclusió
    ├── work/         # inventari d'elegibilitat i transcripció
    ├── output/       # només fragments aprovats per entrenar
    └── reports/      # cobertura, exclusions i qualitat
```

Els scripts s'afegeixen quan hi ha una tasca repetida que automatitzar. No es
construeix un generador abans de saber quin format i quines revisions
necessitem.

## Format d'entrenament

Una línia JSONL per conversa, amb `messages` alternats entre `user` i
`assistant`. Es permet una conversa d'un intercanvi o de diversos. No s'hi
afegeixen identificadors, proves, procedència ni notes editorials.

```json
{"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

La procedència, els drets i l'estat de revisió es desen en fitxers separats de
`output/`.

## Ordre de treball

1. Fixar i revisar els criteris amb els exemples de `knowledge/review/EXEMPLES.md`.
2. Preparar un grup petit de converses candidates d'un tema cada vegada.
3. Revisar naturalitat, fil, exactitud, procedència i drets.
4. Corregir els exemples abans de generar-ne més.
5. Auditar cobertura i duplicats; deixar constància dels fets sense conversa.
6. Aprovar els registres i exportar-los als splits sense filtració entre fonts
   relacionades.
7. Aplicar un flux separat a Language, respectant autenticitat i permisos.

No s'escala el volum fins que els exemples de calibratge sonin a converses
reals i passin tots els criteris anteriors.
