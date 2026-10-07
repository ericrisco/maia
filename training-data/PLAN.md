# Pla nou per a Maia Training Data

## Decisió editorial

El problema dels primers registres no era que fossin massa curts. Les preguntes sonaven com exercicis d'extracció: demanaven què deia una secció, una fila o una fitxa. Una conversa bona comença amb una necessitat que una persona podria tenir sense haver vist el corpus.

Per això, primer calibram converses i només després tornem a produir registres. No generarem preguntes automàticament a partir dels títols, les seccions o cada dada d'una fitxa.

## Separació dels dos conjunts

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb informació documentada a `docs/temes/`.
- **Language** preserva formes de parlar de persones andorranes a partir de `docs/parla/`, seguint-ne els criteris d'elegibilitat, transcripció i drets.

No es barregen. Les converses editorials de `knowledge/review/EXEMPLES.md` serveixen per calibrar l'estil i no són registres d'entrenament ni compten com a cobertura.

## Estructura de treball

```text
training-data/
├── PLAN.md
├── README.md
├── knowledge/
│   ├── review/       # guia, exemples de calibratge, candidats i procedència
│   ├── work/         # inventari i seguiment intern de cobertura
│   ├── scripts/      # inventari, validació i exportació
│   ├── reports/      # cobertura, exclusions i qualitat
│   └── output/       # conjunts finals aprovats
└── language/
    ├── review/       # fragments i candidats lingüístics
    ├── work/         # elegibilitat i fiabilitat de transcripció
    ├── scripts/
    ├── reports/
    └── output/       # conjunts finals aprovats
```

## Com escriure una conversa Knowledge

1. Llegeix la fitxa completa i comprova les fonts abans de formular cap pregunta.
2. Identifica una cosa útil que una persona voldria entendre, decidir, explicar o contrastar.
3. Escriu una pregunta que tingui sentit per si sola. No facis referència a la fitxa, a una secció, a una fila ni al corpus.
4. Contesta la pregunta directament, amb context suficient per entendre la resposta.
5. Afegeix un seguiment només quan la resposta anterior faci néixer un dubte natural. El seguiment ha de reprendre el fil i aportar alguna cosa nova.
6. Acaba quan el dubte s'hagi resolt. Sovint seran dos o tres intercanvis; no hi ha un mínim de torns.
7. Contrasta cada afirmació amb la font i registra per separat la procedència, els drets i els límits.

Abans d'aprovar-la, llegeix la conversa en veu alta sense mirar les fonts. Si sembla un qüestionari, una ordre d'extracció o una història inventada per justificar la pregunta, reescriu-la o descarta-la.

## Exemples de necessitats humanes

- Algú veu tres actes al programa d'una festa i vol saber si tots són balls.
- Algú ha sentit dues dates i vol entendre si són dues fites diferents o una contradicció.
- Algú planifica una visita i pregunta què podria veure en un lloc i una data concrets.
- Algú vol explicar una llegenda a un infant i no recorda com acaba.
- Algú consulta un document històric i es pregunta què permet concloure i què no.

Aquests contextos són punts de partida, no plantilles. No afegim viatges, familiars, estudis o decisions fictícies si no fan més clara una necessitat real.

## Regles per a respostes fiables

- Respon primer allò que s'ha preguntat. Afegeix només el context que ajuda.
- Separa fets documentats, llegendes, interpretacions i hipòtesis.
- Si les fonts discrepen, explica què diu cadascuna i si el corpus ho pot resoldre.
- Si falta informació, digues què no se sap. No converteixis un buit en una negació.
- No presentis informació històrica com si fos necessàriament vigent avui.
- Evita llistes llargues si la persona no les necessita.
- Mantén les notes editorials i la metadata fora del text de `assistant`.

## Fases

### 1. Calibratge

Revisar la guia i els exemples d'aquest directori. Acordar què sona natural i què fa que una conversa es descarti.

### 2. Pilot petit

Crear entre cinc i vuit converses de temes diferents. Prioritzar preguntes espontànies i seguiments connectats. Revisar-les abans d'iniciar la cobertura sistemàtica.

### 3. Producció per fitxa

Llegir una fitxa sencera, registrar les unitats útils i els buits, i redactar només les converses que resolguin dubtes plausibles. Una fitxa pot donar lloc a cap conversa, una o diverses; el nombre no és una quota.

### 4. Revisió i cobertura

Comprovar exactitud, naturalitat, continuïtat, duplicats i procedència. Mesurar quines unitats de coneixement queden representades; no confondre una conversa amb cobertura completa de la fitxa.

### 5. Exportació

Només els registres aprovats passen a `output/`. Agrupar exemples relacionats abans de separar train, validation i test, per evitar que variants gairebé iguals quedin en splits diferents.

### 6. Maia Language

Treballar-lo separadament. Incloure només peces elegibles i fragments fiables, preservar la parla humana i agrupar per peça o parlant abans de fer splits. No inventar respostes per augmentar el volum.

## Format final

Una conversa per línia JSONL, amb missatges alternats i sense procedència ni notes internes:

```json
{"messages":[{"role":"user","content":"Al programa de Sant Julià hi ha la Passa i el ball del Cerdà. Són dues danses?"},{"role":"assistant","content":"El Cerdà és un ball; la Passa és una cercavila de parelles de fadrins. Les parelles que es casaran aquell any van al davant."},{"role":"user","content":"Ah, per això la Passa té un ordre concret?"},{"role":"assistant","content":"Sí. La resta de parelles segueix de més grans a més joves. La fitxa no explica com es formen les parelles."}]}
```

## Prioritats

1. Correctesa i traçabilitat.
2. Preguntes que una persona faria de debò.
3. Respostes clares i completes.
4. Seguiments que continuen el mateix fil.
5. Cobertura útil, varietat i absència de duplicats.
6. Volum.

No augmentarem el volum a costa de cap prioritat anterior.
