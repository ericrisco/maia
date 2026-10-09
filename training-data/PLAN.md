# Pla de Maia Training Data

## Objectiu d'aquesta etapa

Reiniciar la preparació de dades amb una regla clara: **cada conversa comença amb una necessitat humana, no amb l'estructura d'una fitxa**. Ara preparem l'estructura i un grup petit d'exemples de calibratge. Després revisarem el patró i afegirem registres en lots petits.

Les dades finals tindran dos conjunts independents:

- **Maia Knowledge**: coneixement documentat a `docs/temes/`.
- **Maia Language**: parla autèntica de `docs/parla/`; no s'inventen respostes per fer-la semblar conversacional.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── examples/       # Exemples de calibratge, fora dels exports
│   ├── review/         # Converses noves pendents de revisió
│   ├── work/           # Cobertura i anotacions de treball
│   ├── reports/        # Qualitat, drets i cobertura
│   ├── scripts/        # Eines que afegirem quan el flux estigui definit
│   └── output/         # Exports aprovats; buit de moment
└── language/
    ├── examples/       # Només fragments humans aprovats per calibrar
    ├── review/         # Decisions sobre peces i fragments
    ├── work/           # Elegibilitat, incertesa i procedència
    ├── reports/        # Inclusió, exclusions i drets
    └── output/         # Exports aprovats; buit de moment
```

## Procés per escriure una conversa de Knowledge

1. **Llegeix la font sencera.** Entén què afirma, què atribueix a una font i què deixa obert.
2. **Descriu la necessitat humana en una línia interna.** Exemples: «vol saber si pot reclamar un deute a una autoritat» o «vol entendre què veurà en una festa».
3. **Tanca la font i redacta la primera intervenció.** No citis títols, seccions, files, gràfics o “la fitxa”. La pregunta ha de tenir prou context per entendre's sola.
4. **Respon directament.** La primera frase resol el dubte. Després afegeix els límits o matisos que evitin una impressió falsa.
5. **Continua la conversa.** Afegeix una altra pregunta que algú faria en sentir la resposta. Ha de demanar una cosa nova i dependre del que s'acaba de dir; no cal repetir el context si el seguiment és clar.
6. **Llegeix només els missatges, en veu alta.** Si sona a examen, encàrrec escolar, visita guiada per la fitxa o qüestionari de dades, reescriu-ho.
7. **Verifica cada afirmació i registra la procedència a part.** Una pregunta natural no compensa una resposta sense suport o uns drets pendents.

### Regla multitorn

Una conversa de Knowledge que proposem per a revisió té almenys dues parelles de pregunta i resposta. El segon torn ha de ser un seguiment versemblant, no una variació de la primera pregunta ni una dada afegida només per arribar al mínim. Si no hi ha cap continuació honesta, no forcem la conversa: anotem la unitat a cobertura i la deixem fora dels candidats multitorn.

### Preguntes que es rebutgen

No passen la revisió preguntes com:

- «Què explica la secció “El relat”?»
- «Què indica aquesta fila?»
- «Què diu aquesta fitxa sobre X?»
- «I dos topònims que en surten?»

Depenen del document o produeixen respostes penjades. No n'hi ha prou de canviar «secció» per «text»: cal identificar què vol resoldre la persona.

## Porta de qualitat

Abans de posar una conversa a `knowledge/review/`, comprova:

- La primera pregunta és comprensible sense veure la font i sona plausible en boca d'una persona.
- La resposta contesta el que s'ha preguntat, amb context suficient i sense veu editorial.
- El seguiment neix de la resposta i aporta informació nova.
- Cada fet és fidel a la font; discrepàncies, incerteses i límits es mantenen explícits.
- La conversa funciona llegida sola, sense títols ni IDs.
- La procedència i els drets estan anotats per separat.

Un sol criteri fallit vol dir reescriure o descartar. No s'augmenta el volum per compensar una pregunta dolenta.

## Cobertura i drets

Quan comenci la producció, cada unitat útil de `docs/temes/` acabarà amb una decisió traçable: coberta per una conversa, reservada per a retrieval, o exclosa amb un motiu. No confondre cobertura d'un document amb cobertura de cada afirmació útil.

Abans que una font entri en cap export, registrar-ne l'autoria, llicència i condicions d'ús. Si la reutilització o l'ús en entrenament no és clar, conservar el registre com a no exportable fins a resoldre-ho.

## Maia Language

Language conserva fragments humans autèntics. No es crea una pregunta fictícia per convertir un monòleg en diàleg, ni es reescriu la resposta perquè sembli català andorrà. Es revisen parlant, llengua, qualitat de transcripció, drets i separació per peça o parlant.

## Exports

Els fitxers de conversa d'exportació contindran només missatges `user` i `assistant`. La procedència i les decisions editorials aniran en fitxers separats. `knowledge/output/` i `language/output/` es mantenen buits fins que hi hagi converses aprovades, drets resolts, deduplicació, validació i splits sense filtració entre conjunts.

## Següent pas

Revisar aquests exemples de calibratge amb el lector. Un cop acceptat el patró, treballar tema a tema, en lots petits, i no donar per bona cap conversa només perquè sigui multitorn.
