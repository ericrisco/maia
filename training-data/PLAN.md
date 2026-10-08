# Pla de treball: converses que una persona faria

## Per què refem els exemples

Preguntes com «què explica aquesta secció?» comproven si el model ha llegit un document, no si sap ajudar una persona. També són dolentes les preguntes amb context inventat, les dades obscures sense motiu i els seguiments que només allarguen el diàleg.

## Criteri de conversa

1. **Comença per una intenció humana concreta.** Per exemple: entendre què veurà algú en una festa, aclarir una tradició, situar un fet en el temps o distingir dues versions.
2. **Redacta la pregunta sense mirar el títol ni l'estructura de la fitxa.** Ha de tenir sentit per a algú que no sap com està organitzat Maia.
3. **Dona la resposta principal al primer torn.** Explica prou perquè sigui útil encara que la conversa s'acabi aquí.
4. **Fes un seguiment només quan una resposta desperti una pregunta versemblant.** El seguiment ha de demanar una cosa nova. No repeteixis la mateixa dada amb altres paraules.
5. **No inventis una biografia ni una situació personal** per fer que la pregunta sembli natural. Un pla hipotètic simple —com triar quin dia assistir a una festa— és acceptable si la informació realment l'ajuda.
6. **Separa fets, relats i incerteses.** Una llegenda es presenta com a llegenda. Una font que no resol una qüestió no autoritza a completar-la per intuïció.
7. **Revisa només el diàleg, sense veure la font.** Si sembla un examen, una ordre per resumir o una consulta sobre el repositori, reescriu-lo o descarta'l.
8. **Comprova cada afirmació amb les fonts** i desa la procedència i els drets en fitxers de treball separats.

## Multitorn sense farciment

Els exemples de calibratge tenen almenys dos parells de torns per mostrar continuïtat. Això no obliga a allargar totes les converses futures: si no hi ha un seguiment natural, es canvia de tema o es descarta el fil. Cada parell de torns ha de ser útil per si sol.

## Prova ràpida de qualitat

- La pregunta inicial és una cosa que algú preguntaria sense haver vist la font?
- Queda clar què vol saber i a què es refereix?
- La primera resposta contesta directament i amb prou context?
- El seguiment neix de la resposta anterior i aporta informació nova?
- La conversa continua sonant natural llegida en veu alta?
- Les afirmacions són fidels a fonts consultades i no amaguen incerteses?

Un «no» vol dir revisar o descartar. La cobertura del corpus no justifica una pregunta artificial.

## Estructura i fases

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── examples/       # Pocs exemples per acordar el criteri
│   ├── work/           # Inventari, cobertura i procedència
│   ├── reports/        # Cobertura, qualitat i exclusions
│   ├── scripts/        # Eines de validació o generació, quan calguin
│   └── output/         # Només converses aprovades i amb drets revisats
└── language/
    ├── README.md
    ├── work/
    ├── reports/
    ├── scripts/
    └── output/
```

1. Acordar l'estil amb els exemples petits de Knowledge.
2. Ajustar el criteri si encara sonen a preguntes d'examen.
3. Recuperar o reconstruir l'inventari i la procedència; no convertir cada fitxa en una pregunta automàtica.
4. Crear converses en lots petits, amb revisió humana de naturalitat i exactitud.
5. Treballar Language a part: només veu humana contemporània elegible i transcripció prou fiable; no inventar respostes per imitar parlants.
6. Exportar i fer splits només quan contingut, drets, cobertura i duplicats estiguin revisats.

`output/` comença buit expressament. Els exemples no són encara dades aprovades per entrenar.
