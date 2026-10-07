# Pla revisat de Maia Training Data

## Objectiu

Preparar dos datasets independents a partir de `docs/`:

- **Maia Knowledge**: respostes útils sobre Andorra, basades en `docs/temes/`.
- **Maia Language**: fragments de català andorrà real, basats en peces humanes elegibles de `docs/parla/`.

La prioritat és que cada conversa resolgui un dubte que una persona podria tenir. El recompte de registres ve després.

## Estructura

```text
training-data/
├── PLAN.md
├── README.md
├── knowledge/
│   ├── review/
│   │   ├── CONVERSATION-GUIDE.md
│   │   ├── EXEMPLES.md          # calibratge editorial; no s'exporta
│   ├── work/                    # cobertura i evidència interna
│   ├── scripts/
│   ├── reports/
│   └── output/                  # només exports aprovats
└── language/
    ├── review/                  # fragments humans candidats
    ├── work/                    # elegibilitat i exclusions
    ├── scripts/
    ├── reports/
    └── output/                  # exports independents de Knowledge
```

Les mostres de `EXEMPLES.md` no són registres i no compten com a cobertura. Quan el pilot s'aprovi, els registres aniran a `review/conversations.jsonl` i la procedència a `review/provenance.jsonl`. Les dades de treball i la procedència no s'exporten.

## Com escriurem Knowledge

1. Llegir la fitxa completa i les fonts que sostenen la resposta.
2. Escriure en una nota interna qui pregunta i quin dubte pràctic té.
3. Començar amb context natural. La persona no té la fitxa oberta ni parla del corpus.
4. Fer que cada seguiment surti de la resposta anterior. Res de preguntes encadenades per buidar una llista.
5. Aturar-se quan el dubte queda resolt. No afegir torns per arribar a una llargada fixa.
6. Contrastar totes les afirmacions. Mantenir atribucions, dates, contradiccions i incerteses.
7. Revisar la conversa sense mirar la font. Després revisar-la amb la font i registrar la procedència.

Una conversa pot tenir un sol intercanvi si no hi ha un seguiment honest. Quan hi ha una continuació natural, el pilot preferirà dos o tres intercanvis breus.

## Com escriurem Language

Knowledge pot tenir respostes redactades amb naturalitat a partir de fonts. Language ha de conservar veu humana real. No inventarem preguntes i respostes per convertir un monòleg en entrevista. Només inclourem fragments elegibles, amb drets i transcripció revisats. Les peces amb incertesa es filtraran fragment a fragment o s'exclouran amb motiu registrat.

## Fases

### 1. Reinici editorial

Els registres Knowledge de l'intent anterior s'han retirat. La cobertura torna a `not_started`; cap mostra d'exemple compta com a dada ni com a cobertura. No generar encara exports.

### 2. Pilot petit de Knowledge

Preparar 5–10 converses de temes diferents. Llegir-les en veu alta i revisar-les amb la persona usuària. Si una pregunta sembla un exercici sobre la fitxa, descartar-la o reescriure-la.

### 3. Acordar el criteri

Després del pilot, ajustar la guia amb els comentaris. Només llavors reprendre la producció regular, en grups petits i fàcils de revisar.

### 4. Cobrir el corpus

Recórrer totes les fitxes de `temes/`. Cobrir les unitats útils, no cada frase amb preguntes artificials. Registrar també els buits i les dades que no es poden afirmar.

### 5. Revisar Language per separat

Comprovar veu, època, `apte_llengua`, drets i fiabilitat de transcripció per peça. Incloure només fragments humans aptes. No barrejar els seus criteris amb els de Knowledge.

### 6. Validar i exportar

Deduplicar, revisar qualitat i cobertura, i fer splits agrupats per document, peça o parlant quan pertoqui. Generar `train.jsonl`, `validation.jsonl` i `test.jsonl` només quan les dades estiguin aprovades.

## Porta de qualitat per a cada conversa

- La pregunta té sentit sense veure cap document.
- Es pot explicar en una frase per què una persona ho preguntaria.
- La resposta contesta de seguida i amb el context just.
- Cada seguiment respon al fil de la conversa.
- La resposta no inventa detalls ni converteix una llegenda en fet històric.
- No demana «què diu la secció», «què indica la fila» ni «quins elements hi surten».
- No repeteix la mateixa dada amb una altra formulació.
- La conversa ensenya alguna cosa útil i no sembla un qüestionari.

Si falla un punt, no s'afegeix al conjunt aprovat.

## Pas següent

Revisar `knowledge/review/EXEMPLES.md` com a calibratge. Després fer el pilot curt i validar-ne el to abans de crear més registres.
