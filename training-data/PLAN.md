# Pla complet de Maia Training Data

## Objectiu

Preparar dos datasets separats i exhaustius a partir del corpus de Maia:

- **Knowledge:** respondre preguntes humanes sobre tot el coneixement útil de
  `docs/temes/`.
- **Language:** preservar la manera real de parlar en català andorrà
  contemporani a partir de `docs/parla/` elegible i verificable.

La cobertura no es dona per acabada perquè hi hagi moltes converses. Es dona
per acabada quan cada unitat de coneixement i cada peça elegible s'ha revisat,
i els buits i les exclusions queden explicats.

## Estructura de treball

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── review/
│   │   ├── CONVERSATION-GUIDE.md  # criteris i exemples editorials
│   │   ├── EXEMPLES.md            # accés als exemples aprovats
│   │   ├── conversations.jsonl    # una conversa per línia
│   │   └── provenance.jsonl       # fonts, drets i estat editorial
│   ├── work/                      # inventari i estat per document/unitat
│   ├── output/                    # train, validation i test
│   └── reports/                   # cobertura i exportació
└── language/
    ├── work/                      # inventari, drets i verificació
    ├── output/                    # només material apte i aprovat
    └── reports/                   # inclusions, exclusions i cobertura
```

`knowledge/starter/` és el pilot editorial. Els seus exemples orienten el to,
però no substitueixen `review/conversations.jsonl` ni l'inventari exhaustiu.
Les dades ja revisades continuen sent part del treball i no es descarten pel
reinici editorial.

## Cobertura de Knowledge

Revisar **tots els documents d'article** de `docs/temes/`, tema per tema. Per
cada article, inspeccionar títol, descripció, seccions, paràgrafs, llistes,
taules, cronologies, xifres, noms, llocs, relacions, discrepàncies, correccions
i buits explícits. Una unitat pot quedar coberta per una conversa, per diverses
converses si resol dubtes diferents, o marcada com a no apta per generar una
pregunta natural.

No convertir automàticament cada fila en una pregunta. La cobertura es registra
a `work/document-status.json` i `work/document-inventory.json`; no s'infereix
del nombre de registres.

## Converses de Knowledge

- Cada conversa comença amb un dubte que una persona podria plantejar sense
  veure cap fitxa.
- Els seguiments són multitorn quan el fil ho demana. Cada torn reprèn una
  explicació anterior; no s'allarga per extreure una llista.
- Les respostes resolen primer el dubte, amb prosa clara i context suficient.
- Es conserven atribució, període històric, incertesa, desacord entre fonts i
  límits de la documentació.
- No es pregunta per seccions, files o títols del corpus. No s'inventa cap
  situació personal per fer sonar humana la conversa.
- Aplicar la llista de control de `knowledge/review/CONVERSATION-GUIDE.md` i
  els exemples de `knowledge/review/EXEMPLES.md` abans d'aprovar.
- Registrar cada conversa i la seva procedència. Una conversa sense procedència
  completa no és exportable.

## Treball incremental i Git

Treballar a `main`, segons l'autorització de l'usuari. Fer un commit i push per
cada conversa, no agrupar preguntes diferents. Per a cada registre:

1. llegir la fitxa sencera i les fonts que sostenen la resposta;
2. redactar i revisar una conversa;
3. afegir-la a `review/conversations.jsonl` i registrar-ne la procedència;
4. actualitzar l'inventari i l'estat de cobertura;
5. exportar només els registres aprovats i comprovar l'estat de Git;
6. fer commit i push abans d'obrir la pregunta següent.

Els fitxers locals que ja estiguin modificats i no pertanyin a la conversa es
preserven i no s'inclouen al commit.

## Maia Language

Revisar totes les peces `apte_llengua: true`. Verificar la veu, la data, la
transcripció, els fragments incerts i els drets peça per peça. L'assistent no
pot atribuir-se com a parla andorrana una resposta inventada. Només es creen
converses quan la font conserva intercanvis humans reals; si és un monòleg,
no se li afegeixen preguntes artificials. Registrar també les exclusions i el
motiu. Els estats pendents es mantenen visibles i no es presenten com a permisos.

## Criteri final

Knowledge: tots els articles inspeccionats, cobertura de les unitats útils
justificada, converses naturals i fidels, drets/procedència registrats,
duplicats revisats i splits sense fuga entre contingut relacionat.

Language: totes les peces elegibles inspeccionades, material humà autèntic i
prou verificat, drets registrats, fragments incerts exclosos o corregits amb
font, i splits agrupats per peça/parlant quan es pugui.

En tots dos datasets, el JSONL final conté una línia per conversa i només el
camp `messages` amb rols `user` i `assistant`. La metadata editorial queda als
fitxers de revisió, no al missatge d'entrenament.
