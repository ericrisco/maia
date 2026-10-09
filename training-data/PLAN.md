# Pla: converses útils i naturals

## El problema que corregim

Una pregunta com «què explica aquesta secció?» només té sentit per a qui ja ha vist una fitxa. Una resposta que acaba amb un fragment, una taula o una frase incompleta tampoc ajuda una persona. Aquestes formes converteixen el dataset en un examen del corpus.

## Regla editorial

1. Troba una curiositat, una decisió pràctica o una confusió que una persona podria tenir sense conèixer el corpus.
2. Escriu la pregunta abans de mirar el títol i els subtítols de la font. No esmentis fitxes, seccions, files, gràfics ni IDs.
3. Contesta la pregunta de seguida i amb prou context perquè la resposta s'entengui per si sola.
4. Afegeix un seguiment només quan una resposta faci néixer una pregunta nova i versemblant. No hi ha quota de torns.
5. No inventis experiències personals per fer més simpàtica la pregunta. Un escenari pràctic breu és vàlid si canvia la resposta.
6. Separa el fet documentat, la interpretació i la incertesa. No omplis buits amb intuïcions.
7. Llegeix el diàleg sense la font. Si sembla un examen o sona forçat en veu alta, reescriu-lo o descarta'l.
8. Comprova cada afirmació amb la font i registra procedència i drets fora dels missatges.

## Converses multitor

Les mostres de calibratge inclouen seguiments perquè es pugui revisar la continuïtat. Això no obliga totes les dades futures a tenir diversos torns. Cada parell pregunta-resposta ha de resoldre una necessitat real; si el fil no continua de manera natural, s'acaba.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── examples/conversations.jsonl  # calibratge, no exportable
│   ├── work/                        # cobertura i procedència
│   ├── reports/                     # qualitat i progrés
│   ├── scripts/                     # validació/generació, quan calgui
│   └── output/                      # aprovades, només al final
└── language/
    ├── README.md
    ├── work/                        # fonts, elegibilitat i splits
    ├── reports/
    ├── scripts/
    └── output/                      # mostres humanes elegibles
```

## Fases

1. Revisar les mostres de `knowledge/examples/` i acordar-ne la veu.
2. Inventariar tot `docs/temes/`; crear converses en lots petits, amb procedència traçable.
3. Revisar exactitud, naturalitat, cobertura, duplicats i drets abans d'aprovar registres.
4. Treballar Language per separat. Incloure només veu humana contemporània i transcripcions fiables, amb drets revisats.
5. Crear exports i splits quan cada registre estigui aprovat i el conjunt tingui cobertura suficient.

`output/` comença buit expressament. Les mostres i els candidats no compten com a dades aprovades.
