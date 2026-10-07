# Pla de Maia Training Data

## Propòsit

Preparar dos datasets separats a partir de `docs/`:

- **Maia Knowledge** ensenya a respondre preguntes sobre Andorra amb el coneixement de `docs/temes/`.
- **Maia Language** conserva català andorrà contemporani produït per persones, a partir de les peces elegibles de `docs/parla/`.

Aquest document defineix el flux de treball. Els exemples de `knowledge/review/EXEMPLES.md` són mostres de calibratge, no registres per entrenar.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── review/
│   │   ├── README.md
│   │   ├── CONVERSATION-GUIDE.md
│   │   ├── EXEMPLES.md             # mostra editorial, no s'exporta
│   │   ├── conversations.jsonl    # candidats; no exportar abans d'auditar-los
│   │   └── provenance.jsonl       # font i drets, fora del text d'entrenament
│   ├── work/                       # inventari, cobertura i notes d'evidència
│   ├── scripts/
│   ├── reports/
│   └── output/                     # exports només després de validar
└── language/
    ├── README.md
    ├── review/                     # selecció i revisió de fragments humans
    ├── work/                       # elegibilitat i exclusions justificades
    ├── scripts/
    ├── reports/
    └── output/                     # exports separats dels de Knowledge
```

No es posa cap dada de Language a Knowledge ni a l'inrevés. La procedència i les anotacions internes no entren als JSONL finals.

## Per què els registres anteriors no són un bon patró

Algunes preguntes tracten la fitxa com si l'usuari la tingués oberta: «Què explica aquesta secció?», «Què indica aquesta fila?» o «I dos topònims que en surten?». D'altres apilen peticions independents per extreure dades. Una resposta pot ser certa i continuar sent una mala mostra si ningú no faria aquella pregunta en una conversa real.

Per això no n'hi ha prou amb una llista de formes de pregunta. Cada conversa ha de començar amb una situació o un dubte recognoscible; cada seguiment ha de néixer de la resposta anterior.

## Flux per crear Maia Knowledge

1. **Tria una unitat de coneixement** de la font i llegeix el document sencer, incloses les taules, els enllaços i els avisos d'incertesa que afectin el fet.
2. **Imagina qui ho preguntaria i per què.** Escriu una nota interna breu com «vol organitzar una visita», «ha sentit dues versions» o «vol saber si és una dansa». Si no hi ha cap motiu humà plausible, no forcis una pregunta.
3. **Escriu el primer torn** amb el context mínim perquè s'entengui sense conèixer Maia ni tenir un document al davant.
4. **Construeix el diàleg torn a torn.** Maia respon primer el dubte. Després, l'usuari pregunta una cosa que una persona podria voler aclarir arran d'aquella resposta. La conversa sol tenir més d'un intercanvi, però no s'afegeixen torns només per complir una quota.
5. **Contrasta cada afirmació** amb la font. Si hi ha versions diferents, límits o dades absents, la resposta ho explica sense inventar una resolució.
6. **Passa la porta editorial** de `knowledge/review/CONVERSATION-GUIDE.md`. Rebutja o reescriu qualsevol conversa que soni a interrogatori de la fitxa.
7. **Registra la procedència** per separat. Després d'aprovar, actualitza la cobertura de la font i valida el format abans d'afegir el registre.

### Patró de conversa

```text
Persona: situació o dubte real
Maia: resposta directa, amb el context just
Persona: aclariment que surt d'aquesta resposta
Maia: resposta al seguiment, sense reobrir tota la fitxa
```

El patró orienta; no és una plantilla literal. Les preguntes han de sonar variades perquè les situacions són variades, no perquè s'hagin parafrasejat plantilles.

## Porta de qualitat

Una conversa només s'accepta si compleix tots aquests punts:

- S'entén sense cap referència a seccions, files, documents o al corpus.
- La pregunta inicial té una intenció humana que es pot resumir en una frase.
- Els seguiments reprenen el fil i no demanen dades inconnexes.
- Maia contesta el que li han preguntat des de la primera frase.
- Cada afirmació factual està sostinguda per una font identificable.
- Les reserves, contradiccions i absències de la font es conserven amb naturalitat.
- El diàleg ensenya una cosa útil i no duplica un registre existent.
- L'extensió és la necessària per contestar, sense llistes de farciment.

**Prova de lectura:** llegir només els missatges, sense obrir la font. Si la persona sembla estar fent una auditoria, dictant una cerca o donant ordres a una base de dades, el registre no passa.

## Cobertura i estat

La cobertura es mesura per coneixement útil revisat i representat, no pel nombre de preguntes. Cada document ha de deixar constància de les unitats tractades, les converses que les cobreixen i els buits que no es poden entrenar. No s'inventa contingut per arribar a una xifra.

Els registres de `conversations.jsonl` només contenen `messages` amb torns `user` i `assistant`. La font, els drets i l'estat de revisió van a `provenance.jsonl`. Els drets s'han de transcriure segons `docs/CONTRACT.md`.

## Maia Language

Language segueix un procés separat. Només s'utilitza material de veu humana que compleixi les condicions del corpus: veu originària, època contemporània i `apte_llengua: true`. Les respostes provenen de fragments reals, amb canvis mínims i documentats. No s'inventen respostes perquè un monòleg sembli un diàleg. Les exclusions i les transcripcions incertes queden justificades.

## Etapes del projecte

1. Calibrar aquest pla amb els exemples i aprovar el criteri editorial.
2. Auditar els registres antics. Classificar-los com a bons, recuperables o descartats; no donar-los per vàlids només perquè són al JSONL. Fins que la revisió acabi, el fitxer és una cua de candidats, no un dataset aprovat.
3. Fixar el format mínim de procedència i la cobertura de Knowledge.
4. Produir registres nous per tema, revisar-los amb la porta de qualitat i actualitzar l'inventari després de cada grup petit.
5. Quan el criteri estigui estable, revisar el corpus Knowledge complet i cobrir les unitats útils pendents.
6. Revisar per separat les peces Language i aplicar-ne els criteris d'autenticitat.
7. Deduplicar, crear splits sense leakage i generar exports només quan la cobertura i la qualitat siguin auditables.
8. Validar i documentar els dos datasets.

No es genera volum per si mateix. Prioritats: correctesa, cobertura, naturalitat, varietat d'intencions i absència d'al·lucinacions.
