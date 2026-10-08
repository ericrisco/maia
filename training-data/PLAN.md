# Pla de treball: dades de Maia

## Objectiu

Crear exemples que ensenyin a Maia a mantenir converses útils i naturals sobre
Andorra. La persona pregunta perquè vol entendre, comprovar o relacionar alguna
cosa; no perquè conegui el nom d'una fitxa o vulgui que el model reciti un
fragment del corpus.

Knowledge i Language són conjunts separats. `knowledge/review/EXEMPLES.md`
serveix per acordar el criteri editorial; no és dada d'entrenament ni compta
per a la cobertura.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── scripts/                   # instruccions del pipeline
│   ├── review/
│   │   ├── EXEMPLES.md            # mostres editorials, mai exportades
│   │   ├── conversations.jsonl    # registres candidats
│   │   └── provenance.jsonl       # fonts i revisions
│   ├── work/                      # inventaris i candidats regenerables
│   ├── reports/                   # informes d'auditoria
│   └── output/                    # exportació només després de l'aprovació
└── language/
    ├── README.md
    ├── scripts/
    ├── review/                    # fragments i procedència
    ├── work/
    ├── reports/
    └── output/
```

El pipeline compartit viu a `src/training_data/`. `review/` conté els registres
que una persona encara ha de revisar. Cada línia de `conversations.jsonl` és una
conversa completa; la línia corresponent de `provenance.jsonl` documenta fonts,
afirmacions i decisions editorials. No poseu metadades als missatges. Els
artefactes regenerables de `work/`, els informes locals i els conjunts exportats
es regeixen pels `.gitignore` de cada carpeta.

## Mètode per escriure Knowledge

1. **Trobar una necessitat, no una secció.** Abans d'obrir el text, anoteu en
   privat què voldria aclarir una persona: una confusió, una comparació, una
   conseqüència, una contradicció aparent o el context d'una història. Aquesta
   nota no entra als missatges.
2. **Redactar la pregunta amb paraules pròpies.** La persona no ha de saber que
   existeix una fitxa, una taula ni cap apartat. Eviteu «què explica la
   secció…», «què indica aquesta fila?» i «resumeix aquest document».
3. **Contestar el dubte de debò.** La resposta inicial ha de ser entenedora per
   si sola, donar el context imprescindible i distingir fets, llegenda i
   interpretació. No amagueu la resposta darrere d'una frase introductòria ni
   la talleu per fabricar més torns.
4. **Continuar només quan hi ha una raó natural.** El seguiment ha de néixer del
   que s'acaba de dir: una conseqüència, una excepció o una comparació que la
   persona probablement voldria aclarir. No hi ha un mínim de torns. Una bona
   conversa pot acabar després d'una resposta; una conversa més llarga ha de
   conservar el context i no repetir preguntes ja resoltes.
5. **Respectar els límits de la font.** Si la informació no hi consta, digueu-ho
   amb claredat. No convertiu una hipòtesi en fet ni completeu buits amb
   coneixement extern sense verificar-lo i registrar-ne la font.
6. **Fer la prova de lectura cega.** Llegiu només `messages`, sense títols,
   notes ni metadades. Pregunteu-vos: «Això ho podria preguntar algú parlant
   amb una persona que en sap? La resposta sona completa i espontània? El
   seguiment surt de la conversa?» Si alguna resposta és no, reescriviu o
   descarteu el registre.

No s'ha de perseguir la varietat canviant paraules d'una mateixa plantilla.
Busqueu dubtes diferents i deixeu que la llargada i el to s'adaptin a cada fil.
No inventeu una situació personal només per fer que la pregunta sembli humana.

## Criteris per acceptar un registre

- La pregunta inicial té sentit sense veure el corpus i no apunta a una peça
  editorial concreta.
- La resposta cobreix el que s'ha preguntat, sense fragments penjats ni
  informació ornamental.
- Cada afirmació factual és traçable a una font i a evidència concreta.
- Els seguiments afegeixen una curiositat real; no són obligatoris.
- El diàleg sona natural llegit en veu alta i no sembla una fitxa d'examen.
- No hi ha dades volàtils congelades com si fossin coneixement permanent.
- La procedència registra llicència, termes i estat de redistribució de totes
  les fonts, abans d'incloure'n material al conjunt.

## Fases

1. **Acordar l'estil.** Llegir `knowledge/review/EXEMPLES.md` i ajustar-lo
   abans de reprendre la producció.
2. **Revisar fonts i drets.** Inventariar `docs/temes/`, comprovar les fonts
   originals i marcar fets estables, contingut volàtil, buits i restriccions.
3. **Produir converses candidates.** Crear una conversa per registre a
   `knowledge/review/conversations.jsonl` i la seva procedència a
   `knowledge/review/provenance.jsonl`.
4. **Revisar i cobrir.** Revisar to, evidència, drets, duplicats i quines
   afirmacions rellevants encara no tenen cap conversa útil.
5. **Tractar Language a part.** Seleccionar només parla humana contemporània
   elegible de `docs/parla/`; no inventar diàlegs ni respostes per imitar una
   varietat lingüística.
6. **Exportar després de l'aprovació.** Separar train, validation i test per
   font o tema per evitar que la mateixa informació aparegui als dos costats
   de l'avaluació.
7. **Auditar l'exportació.** Validar esquema, duplicats, procedència, drets,
   cobertura i criteris de qualitat abans de donar-la per bona.

## Regla de pas

Les mostres són el calibratge, no una autorització automàtica per generar lots.
Un cop acordat l'estil, es reprèn el treball amb registres petits i revisables.
Cap mostra editorial no passa a `review/` o `output/` sense una revisió nova de
contingut i procedència.
