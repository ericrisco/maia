# Pla de Maia Training Data

## Per a què serveix

Preparar dos conjunts separats a partir del corpus de Maia:

- **Maia Knowledge**: ajuda a respondre preguntes sobre Andorra amb informació de `docs/temes/`.
- **Maia Language**: preserva català andorrà contemporani produït per persones, només a partir de material elegible de `docs/parla/`.

Les mostres de Knowledge d'aquesta carpeta són exemples de disseny. No són dades aprovades ni exportables. La cua antiga s'ha preservat als directoris `training-data-reset-backup*` fora d'aquesta carpeta; no es reutilitza automàticament.

## Com escriure converses que sonin humanes

1. **Comença per una necessitat concreta.** Pregunta't què vol aclarir algú, no quin tros del document es pot convertir en pregunta.
2. **Dona el context mínim que necessita la pregunta.** La persona no ha de conèixer el títol d'una fitxa, una secció, una fila o un identificador.
3. **Contesta de seguida.** La primera frase ha de resoldre el dubte; després hi pots afegir el context que ajuda a entendre la resposta.
4. **Segueix el fil.** Afegeix un altre torn quan la resposta faci sorgir una pregunta relacionada. El seguiment ha de demanar informació nova, no extreure una dada aïllada per allargar la conversa.
5. **No inventis una vida per a l'usuari.** No afegeixis «el meu avi m'ho explicava», «hi vaig anar l'altre dia» ni altres experiències que no calen per fer natural la pregunta.
6. **Marca què és tradició, què és document i què no se sap.** No presentis una llegenda com un fet ni resolguis discrepàncies sense suport.
7. **Llegeix només els missatges en veu alta.** Si semblen un examen, una plantilla o una consulta a una fitxa, reescriu-los o descarta'ls.

No hi ha un nombre obligatori de torns. Les mostres inicials són multitorn per revisar la continuïtat. En el conjunt futur, una resposta d'un sol torn és millor que un seguiment forçat.

## Fase zero: calibrar abans de produir registres

No convertir seccions ni unitats d'evidència directament en preguntes. Per a cada mostra:

1. **Identifica el dubte humà** que resol el fet: què voldria aclarir algú, amb quines paraules ho demanaria i quin context mínim necessita.
2. **Escriu la pregunta sense mirar el títol de la fitxa.** Si cal dir «la secció», «la fila» o «el gràfic», comprova si es pot expressar el dubte real en lloc de preguntar pel document.
3. **Redacta una resposta completa i autònoma.** Evita respostes com «apel·lació al Consell General» o «tres coses que el corpus registra»: inclou qui fa què i en quines circumstàncies.
4. **Afegeix seguiments només si tenen una motivació conversacional.** Cada torn ha d'obtenir una informació nova i respondre al fil anterior; no hi ha una quota de torns.
5. **Llegeix només la conversa.** Rebutja-la si sembla un examen, una ordre de lectura, una consulta de base de dades o una seqüència de preguntes enganxades.
6. **Verifica afirmació per afirmació** contra la font i desa la procedència separadament. Indica quan parles d'una llegenda, una interpretació, una contradicció o un buit documental.

Les cinc converses de `knowledge/examples/` són mostres de calibratge, no registres del dataset. Després de revisar-les, es pot ampliar el paquet d'exemples abans de reprendre la producció per temes. Cap mostra passa a `output/` automàticament.

### Abans i després

**No:** «Què explica la secció “El relat” de la fitxa “La troballa de Meritxell”?»

**Sí:** «Per què la imatge de Meritxell torna a aparèixer al mateix lloc?»

**No:** «Què indica aquesta fila del gràfic?»

**Sí:** «Quina llengua tenia més parlants segons les dades del 2014?» — només si el gràfic i les unitats estan explicats prou bé per respondre sense endevinar.

**No:** «Què explica la secció “I aquí hi ha el document que ho resol”?» — la pregunta depèn de l'estructura interna de la fitxa.

**Sí:** «Per què les fonts donaven dos tipus d'interès diferents?» — la resposta ha de distingir els censals de la resta de contractes i explicar què diu el decret de 1895.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── examples/       # Mostres de conversa i procedència; no exportables
│   ├── review/         # Candidats nous després de revisar el criteri
│   ├── work/           # Evidència, inventari, cobertura i exclusions
│   ├── reports/        # Informes de cobertura i qualitat
│   ├── scripts/        # Eines de construcció i validació
│   └── output/         # Exports aprovats, encara buit
└── language/
    ├── examples/
    ├── review/
    ├── work/
    ├── reports/
    ├── scripts/
    └── output/         # Exports aprovats, encara buit
```

Les converses i la procedència van en fitxers separats. Una línia dels fitxers de conversa conté només `{"messages": [...]}`. La procedència interna apunta a les fonts, les afirmacions comprovades i l'estat dels drets; mai no s'afegeix a l'export de fine-tuning.

## Flux per a Knowledge

1. Tria un fet, una relació o un dubte real que es pugui respondre amb el corpus.
2. Redacta la conversa completa i la procedència en paral·lel.
3. Comprova cada afirmació i cada seguiment contra les fonts.
4. Revisa naturalitat, context, matisos, drets i duplicació.
5. Mantén el candidat a `review/` fins que passi les revisions de contingut i de drets.
6. Mesura cobertura per coneixement representat, no pel nombre de preguntes.
7. Deduplica i crea els splits només quan hi hagi prou dades aprovades.

## Flux per a Language

Utilitza només fragments humans que compleixin els criteris d'origen i d'elegibilitat del corpus. No generis oralitat sintètica per inflar el conjunt. Registra els fragments descartats i el motiu, filtra incerteses de transcripció i separa els splits per peça o parlant per evitar filtracions entre train i test.

## Què queda per fer

- Revisar i ajustar aquestes mostres i el criteri editorial.
- Després d'acordar el criteri, afegir nous registres per temes amb procedència i drets.
- Revisar el corpus de Language peça a peça i decidir què és reutilitzable.
- Construir les validacions, la cobertura, la deduplicació i els splits quan hi hagi dades aprovades.

No es creen exports buits ni es compten les mostres com a cobertura. No s'afegeixen registres per assolir una quota de volum.
