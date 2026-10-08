# Pla de treball: Maia Training Data

## Objectiu

Crear Maia Knowledge i Maia Language amb cobertura exhaustiva del corpus, converses naturals multitorn i procedència verificable. Avançar tema a tema i registre a registre; una pregunta o conversa completada és un pas revisable, validat i pujat abans de continuar.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── review/
│   │   ├── EXEMPLES.md
│   │   ├── conversations.jsonl  # converses revisades i mostres editorials diferenciades
│   │   └── provenance.jsonl     # fonts, drets i estat de cada mostra
│   ├── output/                  # buit fins que hi hagi prou dades revisades
│   └── reports/                 # cobertura i qualitat, més endavant
└── language/
    ├── README.md
    ├── review/                  # corpus humà elegible, pendent de revisió
    ├── output/                  # separat de Knowledge
    └── reports/
```

Knowledge ensenya a respondre preguntes documentades sobre Andorra. Language conserva trets de parla humana andorrana contemporània. No es barregen.

## Estàndard d'una conversa

Una conversa parteix d'un dubte que algú podria tenir sense haver obert una fitxa. Pot ser una confusió, una dada que no quadra, una decisió pràctica o una curiositat que surt del torn anterior.

- La primera pregunta s'entén sola. No diu «què explica la secció», «segons la fitxa» ni «què indica aquesta fila».
- No cal inventar una biografia per fer-la versemblant. Es poden fer preguntes directes: «Quina diferència hi ha entre la Passa i la Marratxa? Sempre les confonc.»
- Cada conversa segueix un fil. La persona rep una resposta i pregunta una cosa que realment se'n desprèn.
- No s'afegeixen torns per arribar a una llargada fixa. Si no hi ha un seguiment útil, la conversa s'acaba.
- La resposta comença pel que resol el dubte. Després afegeix el context necessari, amb llenguatge normal i precís.
- Si la font no ho resol, es diu què se sap i què queda obert. No s'omple el buit amb una explicació plausible.
- Les fonts, drets, afirmacions i notes de revisió van a `provenance.jsonl`, mai als missatges d'entrenament.

### Pregunta de control

Llegida sense metadades, la conversa sembla una persona aclarint un dubte real? Si sembla un examen, una consulta a una base de dades o un resum de document, es reescriu o es descarta.

## Fases

1. **Calibratge.** Llegir les mostres editorials sense metadades i aplicar-ne el criteri de naturalitat; no copiar una sola plantilla de conversa.
2. **Preparació de fonts.** Per cada conversa, comprovar el document original, les afirmacions que sosté i les condicions de reutilització. Registrar la procedència i els límits.
3. **Redacció i revisió.** Crear una conversa per necessitat humana i per commit. Comprovar continuïtat, exactitud, límits, naturalitat i duplicats; validar el JSONL, fer commit i push abans del següent registre.
4. **Cobertura exhaustiva.** Fer servir `knowledge/reports/coverage.jsonl` com a inventari de totes les fitxes i índexs de `docs/temes/`; regenerar-lo després d'afegir registres. Revisar seccions, paràgrafs, llistes, files de taula i relacions, i registrar exclusions amb motiu. `partial` vol dir que hi ha alguna conversa vinculada, no que la fitxa estigui completa. Avançar tema a tema fins que no quedi cap coneixement entrenable sense tractar.
5. **Maia Language.** Revisar separadament totes les peces de `docs/parla/`. Incloure només parla humana contemporània elegible, amb drets, consentiment, àudio i transcripció revisats; no inventar respostes per imitar un dialecte.
6. **Exportació i auditoria.** Quan cobertura i drets estiguin revisats, deduplicar i preparar train/validation/test per grup de font o tema. Verificar els fitxers finals i publicar informes de cobertura i exclusions.

## Criteri per passar del calibratge a la producció

- Les mostres passen la pregunta de control.
- Les primeres preguntes no depenen del títol ni del contingut d'una pàgina.
- Els seguiments continuen el fil i no repeteixen dades.
- Les respostes corregeixen errors amb tacte i no sonen telegràfiques.
- Cada afirmació factual té font i condicions d'ús registrades.
- Els dubtes i desacords de les fonts es representen sense resoldre'ls artificialment.

Les mostres editorials continuen marcades com a tals i no s'exporten. Els registres revisats amb drets aptes poden formar part de l'exportació quan el split i la cobertura estiguin verificats. `output/` queda buit fins aleshores.
