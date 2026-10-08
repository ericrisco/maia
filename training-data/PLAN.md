# Pla de treball: Maia Training Data

## Objectiu

Preparar dades de fine-tuning que ensenyin a Maia a contestar com un assistent
útil, no com un cercador de títols o un lector de fitxes. Cada conversa ha de
néixer d'un dubte que una persona podria tenir sense haver vist el corpus.

Knowledge i Language continuen separats. Les mostres de calibratge serveixen
per acordar l'estil; no compten com a dades d'entrenament ni com a cobertura.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── examples/EXEMPLES.md       # mostres editorials, mai exportades
│   ├── review/                    # converses reals revisades i procedència
│   ├── work/                      # inventari i cobertura, quan es regenerin
│   ├── reports/                   # informes d'auditoria
│   └── output/                    # train/validation/test, al final
└── language/
    ├── README.md
    ├── review/                    # fragments humans elegibles i procedència
    ├── reports/
    └── output/                    # train/validation/test, al final
```

## Com s'escriu una conversa de Knowledge

1. **Partir d'una intenció humana.** Abans de redactar, escriure en una frase
   què vol resoldre la persona: una confusió, una decisió, una comparació, una
   dada que no li quadra o una conseqüència que vol entendre.
2. **Redactar sense mirar els títols de secció.** La pregunta inicial ha de
   tenir sentit per si sola. No pot demanar què diu una fitxa, una secció, una
   fila o un document.
3. **Respondre el dubte complet.** La primera resposta ha de poder-se llegir
   sola i contenir el context necessari. No s'ha de repartir una resposta en
   torns artificials.
4. **Afegir seguiments només si neixen de la resposta.** Cada nou torn de la
   persona ha d'aportar una curiositat o una conseqüència genuïna. No hi ha una
   llargada obligatòria; si el fil s'ha acabat, la conversa s'acaba.
5. **Respectar el que la font no resol.** Corregir una premissa amb tacte.
   Separar els fets de les interpretacions i dir clarament quan el corpus no
   permet respondre.
6. **Revisar-la sense metadades.** Llegir només els missatges. Si sona a examen,
   a consulta a una base de dades o a resum d'article, reescriure-la o descartar-la.

No s'ha d'aplicar una plantilla fixa de tipus de pregunta. La varietat ha de
sortir de necessitats diferents, no de canviar «què és» per «quan passa».
Tampoc no s'han d'inventar situacions personals per fer més simpàtica una
pregunta.

## Registre i control

- Una conversa per registre revisable; una conversa completada per commit i push.
- `messages` conté només torns `user` i `assistant`. Font, drets, afirmacions i
  notes de revisió van en un fitxer de procedència separat.
- Cada resposta factual s'ha de contrastar amb la font original. Cap dada nova
  no pot venir d'una suposició de qui redacta.
- Cobertura vol dir que les afirmacions rellevants de cada font estan
  representades; tenir una conversa que en cita el document no és cobertura
  completa.
- Els fets que canvien amb el temps —composició actual d'institucions, horaris
  o preus— es tracten segons la constitució del projecte: són candidats a
  recuperació de documents, no coneixement per congelar al fine-tuning.
- Les mostres d'`examples/` són només editorials. No s'afegeixen a `review/` ni
  a `output/` sense una revisió independent de font i drets.

## Fases

1. **Calibratge d'estil.** Revisar les mostres d'`knowledge/examples/EXEMPLES.md`.
   No ampliar el corpus fins que les preguntes i respostes tinguin el to desitjat.
2. **Inventari de fonts.** Recórrer `docs/temes/`, registrar drets i identificar
   fets entrenables, informació volàtil, incerteses i relacions entre fitxes.
3. **Producció de Knowledge.** Crear converses a partir d'intencions humanes,
   revisar-les contra les fonts i desar cada conversa amb la seva procedència.
4. **Cobertura i deduplicació.** Comparar afirmacions i unitats de cada fitxa
   amb els registres. Completar buits i descartar repeticions sense valor.
5. **Producció de Language.** Inspeccionar `docs/parla/` separadament. Utilitzar
   només parla humana contemporània marcada com a elegible i filtrar fragments
   incerts; no inventar respostes per imitar un dialecte.
6. **Exportació.** Crear `train.jsonl`, `validation.jsonl` i `test.jsonl` només
   després de revisar qualitat i drets. Agrupar pel tema o la font abans de fer
   el split per reduir filtracions entre conjunts.
7. **Auditoria final.** Validar format, duplicats, cobertura, procedència i
   elegibilitat lingüística; deixar els informes a `reports/`.

## Regla de pas

Primer cal acordar l'estil amb les mostres. Després es reprèn la producció, una
conversa per vegada, amb revisió, validació, commit i push abans de continuar.
