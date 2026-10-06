# Pla refet de Maia Training Data

## Objectiu

Preparar dos datasets separats a partir de `docs/`:

- **Knowledge** ensenya a respondre preguntes humanes sobre Andorra amb fets del corpus.
- **Language** conserva el català andorrà contemporani produït per persones.

La cobertura continua sent exhaustiva. No vol dir convertir cada fragment en una
pregunta. Cada fet útil ha d'estar cobert per una conversa que algú podria dir en
veu alta, o quedar exclòs amb un motiu verificable.

## Prioritat nova: naturalitat abans de volum

El pilot anterior va confondre cobertura amb convertir títols, seccions, files i
fragments en preguntes. Aquesta via queda tancada. Els registres que ja hi ha a
`knowledge/review/conversations.jsonl` són esborranys: no es consideren aprovats
ni exportables fins que passin la rúbrica de `knowledge/review/EXEMPLES.md`.

Per a cada conversa nova:

1. Llegir la font completa i confirmar el fet, el seu context i els límits.
2. Escriure en una frase quin dubte real resol la conversa.
3. Formular la pregunta com una persona que vol entendre, comprovar o decidir
   alguna cosa. No mencionar fitxes, seccions, taules, files ni el corpus.
4. Respondre primer la pregunta, amb llenguatge corrent i prou context perquè
   la resposta s'entengui sola.
5. Afegir un seguiment només si és plausible després de la resposta i demana
   informació nova. No forçar una conversa llarga: un sol intercanvi també pot
   ser complet.
6. Llegir el diàleg en veu alta. Reescriure'l si sembla un examen, una consulta
   a un document o una plantilla.
7. Guardar fonts, evidència, drets i decisions de revisió fora de `messages`.

Intencions útils: aclarir una confusió, comprovar una afirmació, entendre una
conseqüència, orientar-se davant d'un cas, distingir dues coses o demanar què va
passar després. No cal repartir-les en quotes ni fer-les servir com a plantilles.

## Estructura de treball

```text
training-data/
├── README.md
├── PLAN.md
├── scripts/
├── knowledge/
│   ├── work/       # inventari, evidència, relacions i exclusions
│   ├── review/     # esborranys, procedència, rúbrica i exemples pilot
│   ├── output/     # splits publicables, només després de revisió i drets
│   └── reports/    # cobertura, qualitat, drets i exclusions
└── language/
    ├── work/       # elegibilitat i selecció de fragments
    ├── review/     # candidats literals i procedència
    ├── output/     # splits publicables
    └── reports/    # peces incloses/excloses i cobertura
```

No esborrarem els esborranys existents per fer veure que el problema no hi és.
Els mantindrem en revisió i els aprovarem, reescriurem o rebutjarem amb motiu.
El pilot editorial és separat dels registres acumulats.

## Flux incremental per conversa

Treballar a `main`, tal com ha autoritzat l'usuari. Afegir una conversa nova a
la vegada. Abans de començar la següent:

1. Confirmar-ne les afirmacions i els drets a les fonts.
2. Revisar el diàleg sencer amb la rúbrica editorial i validar JSONL, evidència,
   traça i cobertura.
3. Revisar `git status` i `git diff`; fer un commit que contingui només aquesta
   conversa i la seva procedència, més els reports que regeneri.
4. Fer push a `origin main` i comprovar que la branca queda neta i sincronitzada.

No agrupar converses diferents en un mateix commit ni continuar si el push de
l'anterior no ha funcionat.

## Passos

### 1. Fixar l'estàndard i provar-lo

Revisar la rúbrica i els exemples pilot amb una persona. Acceptar només els
patrons que sonin naturals i responguin amb fidelitat a les fonts. Revisar també
quins tipus de pregunta falten. Cap exemple del pilot passa automàticament a
entrenament.

### 2. Auditar els esborranys existents

Llegir cada conversa sencera, no només les preguntes. Marcar-la `accepta`,
`reescriu` o `descarta`, amb motiu i enllaç a l'evidència. Detectar preguntes
dependents del document, respostes tallades, inferències no marcades, redundància
i seguiments artificials. Treballar tema a tema.

### 3. Completar Knowledge amb el mateix estàndard

Recórrer tots els documents de `docs/temes/`. Representar cada unitat útil amb
una conversa o justificar-ne l'exclusió. Crear síntesis entre fitxes quan una
persona obtindria una resposta millor connectant-les. Cobertura primer, volum
després.

### 4. Resoldre procedència i drets

Cada conversa conserva una traça interna fins a les fonts i unitats d'evidència.
Registrar llicència i termes de reutilització abans d'incloure contingut en un
output. Drets pendents o redistribució no permesa vol dir que no es publica ni
entra als splits.

### 5. Deduplicar, dividir i validar Knowledge

Agrupar reformulacions pel mateix coneixement abans de fer els splits. Crear
`train.jsonl`, `validation.jsonl` i `test.jsonl` sense fuites entre grups.
Validar JSONL, estructura de missatges, alternança de rols, camps interns,
duplicats, cobertura, qualitat i estat dels drets.

### 6. Completar Language per separat

Usar només material admès per `docs/CONTRACT.md`: `veu == originaria`,
`epoca == contemporania` i `apte_llengua == true`. Preservar torns autèntics,
filtrar incerteses i no inventar preguntes o respostes. Agrupar els splits per
peça, entrevista i parlant quan es pugui.

### 7. Documentar i exportar

Documentar regeneració, validacions, cobertura, exclusions i límits. Només els
registres aprovats per contingut, revisió humana i drets poden arribar a
`output/`.

## Format dels outputs

Una conversa per línia JSONL. `messages` només conté missatges `user` i
`assistant`, en ordre i amb contingut no buit. IDs, proves, notes editorials,
estats i procedència es queden als fitxers interns.

## Definition of Done

**Knowledge** acaba quan tots els documents i continguts útils estan coberts o
exclosos amb motiu; les converses són naturals, fidels, revisades i deduplicades;
els drets estan clars; i els tres splits validen sense fuites conegudes.

**Language** acaba quan totes les peces elegibles estan inspeccionades, les
incerteses i els drets estan resolts, es preserva parla humana i els tres splits
validen sense fuites conegudes.

Fins llavors, tots dos conjunts són en curs. El recompte no és criteri
d'acceptació.
