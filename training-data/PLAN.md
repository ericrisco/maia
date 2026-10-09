# Pla de Maia Training Data

## Objectiu

Preparar dues línies separades: Maia Knowledge, per respondre preguntes sobre Andorra amb el corpus de `docs/temes/`; i Maia Language, per aprendre del català andorrà real amb fragments humans elegibles de `docs/parla/`.

## Criteri de conversa de Knowledge

1. Identificar què vol entendre una persona, sense copiar el títol de la fitxa.
2. Fer una pregunta inicial que s'entengui sense haver vist el corpus.
3. Respondre el dubte directament, amb context suficient i sense afegir fets.
4. Fer un seguiment només quan sorgeixi de manera natural del torn anterior. La continuïtat és desitjable; allargar cada conversa per quota no ho és.
5. Revisar el diàleg en veu alta, com si l'usuari no conegués cap font interna.
6. Registrar les fonts i l'estat dels drets fora de `messages`. Una mostra amb drets pendents o no redistribuïbles no s'exporta.

No es fan preguntes com «què explica aquesta secció?», «què diu aquesta fila?» ni «resumeix la fitxa». Si una pregunta depèn d'un títol, una taula o un gràfic que l'usuari no ha vist, cal donar-li el context natural que li falta o descartar-la.

## Fases

### Fase 1 — Calibratge editorial (ara)

- Mantenir Knowledge i Language separats.
- Revisar les cinc converses de `knowledge/examples/` i el seu raonament editorial a `provenance.jsonl`.
- Ajustar el criteri abans de crear registres en volum.
- No generar exports d'entrenament.

### Fase 2 — Primera tanda de Knowledge

- Triar un tema acotat del corpus.
- Extreure els fets que val la pena ensenyar i les fonts que els sostenen.
- Escriure converses agrupant fets quan una persona els preguntaria junts.
- Revisar naturalitat, correcció, continuïtat, cobertura i drets.
- Deixar els exemples pendents a `knowledge/review/` fins que passin revisió.

### Fase 3 — Revisió i cobertura

- Registrar per tema què s'ha cobert, què s'ha descartat i què continua obert.
- Detectar preguntes artificials, respostes incompletes, duplicats i fets sense font.
- No comptar els candidats com a aprovats ni exportables abans de revisar-los.

### Fase 4 — Maia Language

- Auditar origen, consentiment/permís, llicència i qualitat de transcripció de cada peça de `docs/parla/`.
- Preservar expressions i construccions humanes; no inventar preguntes i respostes perquè sonin andorranes.
- Mantenir fora les peces o fragments no elegibles o incerts.
- Revisar Language com un conjunt separat de Knowledge.

### Fase 5 — Exports

Només quan hi hagi registres aprovats, generar `train.jsonl`, `validation.jsonl` i `test.jsonl` per separat per a Knowledge i Language. L'export conté converses, no procedència interna. Validar els fitxers i evitar que una mateixa conversa o peça de parla aparegui en més d'un split.

## Estructura

- `knowledge/examples/`: mostres editorials per calibrar l'estil; no entrenables.
- `knowledge/review/`: candidats nous encara pendents de revisió.
- `knowledge/work/`: procedència i seguiment de cobertura.
- `knowledge/output/`: exports aprovats, quan n'hi hagi.
- `language/review/`: fragments o converses de parla en revisió.
- `language/work/`: selecció, drets i traçabilitat de les peces.
- `language/output/`: exports de parla aprovats, quan n'hi hagi.
- `reports/`: cobertura, qualitat, exclusions i estadístiques.

## Estat actual

L'estructura i cinc mostres de Knowledge estan preparades per revisar. Els directoris d'export són buits. Language no té mostres perquè primer cal validar les fonts i conservar parla humana autèntica.
