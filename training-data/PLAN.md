# Pla editorial de Maia Training Data

## Per a què és aquest pla

Preparar dos conjunts separats, a partir de `docs/`:

- **Knowledge**: respostes correctes i útils sobre Andorra, basades en `docs/temes/`.
- **Language**: català andorrà real, extret de parla humana elegible a `docs/parla/`.

Ara només fixem el format i el llindar de qualitat amb uns quants exemples. No intentem omplir el dataset ni cobrir tot el corpus en aquesta fase. Després de validar l'estil, reprendrem els registres un a un.

## El problema que volem evitar

Una pregunta no es torna humana només perquè ja no digui «aquesta secció» o «aquesta fila». També sona artificial si busca una dada rara només perquè és a la fitxa, si enumera conceptes com un examen, o si l'assistent hi afegeix un seguiment per encabir informació que faltava.

La conversa ha de començar per un dubte recognoscible. La fitxa és la font de la resposta, no el motiu de la pregunta.

## Com escriure una conversa de Knowledge

1. **Identifica una necessitat plausible.** Què voldria aclarir una persona: una idea que ha sentit, una diferència, un dubte pràctic o el context d'un costum?
2. **Formula la pregunta com la diria aquesta persona.** Fes servir paraules corrents i el context imprescindible. No esmentis fitxes, apartats, gràfics ni «el document».
3. **Comprova que el dubte no l'has inventat només per cobrir una dada.** Si cal explicar massa perquè sembli una situació real, tria un altre angle o no facis registre.
4. **Respon primer el que s'ha preguntat.** Afegeix només el context que ajudi a entendre la resposta o eviti una interpretació errònia.
5. **Respecta el que la font sap i el que no sap.** No ampliïs una regla històrica a l'actualitat ni converteixis una interpretació en un fet.
6. **Llegeix la conversa en veu alta.** Ha de sonar bé sense títol, nota editorial ni cap explicació del procés de recerca.

## Converses de més d'un torn

El multitorn és opcional. Una pregunta ben resolta en un intercanvi és millor que una conversa allargada artificialment.

Afegeix un seguiment només quan la resposta anterior faria venir de manera natural una altra pregunta. El seguiment ha de demanar una cosa nova, no repetir la pregunta, provar l'assistent ni obrir un qüestionari.

No cal que cada conversa tingui el mateix nombre de torns. No afegim preguntes perquè «un dataset hauria de ser multitorn».

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── scripts/                 # validacions compartides
├── knowledge/
│   ├── review/
│   │   ├── EXEMPLES.md      # guia d'estil i mostres editorials
│   │   ├── conversations.jsonl
│   │   └── provenance.jsonl
│   ├── work/                # inventari i traça de cobertura
│   ├── reports/             # qualitat, cobertura i exclusions
│   ├── scripts/
│   └── output/              # només registres aprovats per a un ús concret
└── language/
    ├── review/              # fragments candidats per revisar
    ├── work/                # selecció i incerteses de transcripció
    ├── reports/
    ├── scripts/
    └── output/              # només fragments aprovats per a un ús concret
```

`review/` és provisional. `output/` és el dataset revisat per al destí indicat. `work/` i `reports/` no són missatges d'entrenament. Knowledge i Language no es barregen.

## Procedència i drets

Cada conversa candidata de Knowledge té una traça separada amb documents, fragments d'evidència, fonts originals, atribució, llicència i estat d'ús. La traça no s'inclou als missatges entrenables.

Abans que material d'una font entri a qualsevol `output/`, cal haver-ne registrat la llicència i les condicions d'ús a `docs/raw/` i `docs/fonts/`. «Accés públic» no vol dir automàticament que es pugui redistribuir o fer servir per entrenar.

Language conserva intervencions humanes. No es redacten preguntes o respostes noves per convertir un monòleg en conversa, ni es reescriu la varietat lingüística.

## Revisió de cada exemple

Abans d'acceptar una conversa, pregunta:

- Podria algú fer aquesta pregunta sense tenir la fitxa oberta?
- S'entén què vol aclarir i sona espontània en veu alta?
- La resposta resol el dubte des del començament?
- Tots els detalls i matisos són a les fonts citades?
- Si hi ha seguiment, surt de la resposta i demana informació nova?
- La procedència i els drets són traçables?

Si la pregunta sembla feta per demostrar que hem llegit la fitxa, es descarta encara que la resposta sigui certa.

## Passos següents, després de validar l'estil

1. Revisar aquestes mostres i acordar quines sonen naturals.
2. Recórrer `docs/temes/` i crear només converses que passin el filtre editorial; registrar cobertura i exclusions sense fabricar preguntes.
3. Revisar totes les peces de `docs/parla/` segons el contracte de llengua, sense inventar diàlegs.
4. Revisar contingut, duplicats, drets i procedència abans de separar `train`, `validation` i `test`.
5. Exportar i informar dels recomptes, la cobertura i les limitacions.

No s'exporta cap mostra fins que estigui revisada per al seu ús previst. No hi ha una quota que justifiqui converses artificials.
