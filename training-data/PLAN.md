# Pla de Maia Training Data

## Objectiu complet

Preparar dos datasets exhaustius i independents a partir del corpus actual de Maia. **Knowledge** ha de cobrir tot el coneixement útil de `docs/temes/`; **Language** ha d'auditar tot el material de `docs/parla/` i conservar només parla humana elegible. Una pregunta natural comença amb una necessitat de persona, mai amb l'estructura d'una fitxa.

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

### Prova de naturalitat abans d'escriure

Redacta primer una nota interna amb aquesta forma: **«La persona vol entendre/decidir/aclarir…»**. Si només pots escriure «vol saber què diu la fitxa», encara no has trobat una consulta humana.

La conversa ha de superar aquestes proves:

- **Context autònom:** s'entén sense veure el document ni els missatges previs.
- **Motiu recognoscible:** hi ha una curiositat, confusió, comparació o conseqüència concreta darrere la pregunta.
- **Resposta completa:** el primer enunciat de l'assistent resol el dubte; no és un títol, una llista sense introducció ni un fragment de la font.
- **Seguiment conversacional:** la segona pregunta reacciona a la resposta i demana una aclaració, un límit o una conseqüència que una persona voldria saber a continuació.
- **Veu no fabricada:** no inventis una situació personal («m'ha passat…», «vull denunciar…») si no cal per formular el dubte.
- **Varietat real:** no reutilitzis una mateixa plantilla canviant-hi només el topònim, la xifra o el nom.

No obliguis tots els registres a tenir el mateix nombre de torns. La pauta habitual és de dues parelles user/assistant, però un seguiment que no sorgeix de la primera resposta és pitjor que descartar el registre. Si la conversa s'allarga, cada torn ha d'afegir una necessitat nova i respondre-la sense perdre el fil.

Abans de redactar, classifica la necessitat —per exemple, aclarir una contradicció, entendre una regla, saber què canvia entre dos casos, comprovar una premissa o entendre una conseqüència—. Fes servir aquesta classificació només per diversificar la cobertura; no converteixis les categories en motlles de pregunta.

La guia vinculant de redacció i revisió és [`knowledge/review/EXEMPLES.md`](knowledge/review/EXEMPLES.md). La línia pública de `knowledge/review/conversations.jsonl` conté només `{"messages":[...]}`; `provenance.jsonl` manté la traça interna alineada per línia, incloent-hi evidències, motiu humà de la consulta, seguiment, estat de revisió i drets.

### Regla multitorn

Una conversa de Knowledge que proposem per a revisió té almenys dues parelles de pregunta i resposta. El segon torn ha de ser un seguiment versemblant, no una variació de la primera pregunta ni una dada afegida només per arribar al mínim. Si no hi ha cap continuació honesta, no forcem la conversa: anotem la unitat a cobertura i la deixem fora dels candidats multitorn.

### Preguntes que es rebutgen

No passen la revisió preguntes com:

- «Què explica la secció “El relat”?»
- «Què indica aquesta fila?»
- «Què diu aquesta fitxa sobre X?»
- «I dos topònims que en surten?»

Depenen del document o produeixen respostes penjades. No n'hi ha prou de canviar «secció» per «text»: cal identificar què vol resoldre la persona.

També es rebutja una pregunta que només soni oral però continuï sent una ordre de lectura, com ara «M'expliques aquest gràfic?» si el diàleg no diu quin dubte vol resoldre. Igualment, una resposta pot ser fluida i continuar sent dolenta si no contesta la pregunta, deixa el referent implícit o barreja fets que la font no relaciona.

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

S'ha d'inventariar tot `docs/temes/`, incloent-hi cada fitxa, secció, paràgraf, fila de taula, element de llista, cita útil, relació i límit explícit. Cada unitat de coneixement útil acabarà amb una decisió traçable: representada per una o més converses, reservada per a retrieval (per exemple, informació volàtil) o exclosa amb un motiu concret. La cobertura és per unitat, no per document: una conversa sobre una fitxa no la marca sencera com a coberta. Els índexs i les remissions s'utilitzen per orientar la lectura, no es transformen en preguntes artificials.

Abans que una font entri en cap export, registrar-ne l'autoria, llicència i condicions d'ús. Si la reutilització o l'ús en entrenament no és clar, conservar el registre com a no exportable fins a resoldre-ho.

## Maia Language

Language conserva fragments humans autèntics. Cal auditar cada peça de `docs/parla/` i registrar si és elegible, exclosa o pendent, amb motiu. No es crea una pregunta fictícia per convertir un monòleg en diàleg, ni es reescriu la resposta perquè sembli català andorrà. Només s'extreuen parelles explícites d'entrevistador i parlant quan es poden atribuir i transcriure amb prou fiabilitat. Es revisen parlant, llengua, `apte_llengua`, incertesa de transcripció, drets i separació per peça o parlant. Es guarda el text fontal i els spans per demostrar que les respostes no s'han generat ni reescrit.

## Exports

Els fitxers de conversa d'exportació contindran només missatges `user` i `assistant`. La procedència i les decisions editorials aniran en fitxers separats. `knowledge/output/` i `language/output/` es mantenen buits fins que hi hagi converses aprovades, drets resolts, deduplicació, validació i splits sense filtració entre conjunts.

## Ordre de treball i definició d'acabament

1. Reconstituir l'inventari complet de Knowledge i l'auditoria d'elegibilitat de Language.
2. Revisar primer els exemples de calibratge amb la guia. La cua activa de `knowledge/review/` comença buida. Els registres antics conservats en còpies o en la història de Git no s'hi reincorporen automàticament: només es pot recuperar una conversa després de reescriure-la des de la necessitat humana, verificar cada afirmació i tornar a registrar-ne la procedència. No afegir registres nous fins que els exemples de calibratge passin la revisió. La cobertura tampoc no es dona per feta perquè hi hagués una pregunta antiga.
3. Treballar fitxa a fitxa i peça a peça. Cada nova conversa de Knowledge es revisa, es valida amb evidència i procedència, i rep el seu propi commit i push a `main` abans de començar la següent.
4. Mantenir registres d'exclusió i cobertura que permetin demostrar què s'ha fet amb cada unitat i cada peça.
5. Resoldre drets i deduplicar abans de fer splits. Knowledge s'agrupa per tema/font quan cal evitar filtració; Language s'agrupa com a mínim per peça i, quan es coneix, per parlant.
6. Crear `train.jsonl`, `validation.jsonl` i `test.jsonl` per separat només amb registres aprovats i fonts aptes per a l'ús. Els conjunts no comparteixen conversa, font contigua ni grup de parlant.
7. Executar els validators i publicar reports de volum, drets, cobertura, exclusions, duplicats i fuites.

El projecte només s'acaba quan totes les unitats útils de Knowledge i totes les peces de Language tenen una decisió verificable; els candidats exportats passen qualitat i drets; els splits i els reports coincideixen amb les dades reals. No s'inventa volum per arribar a una xifra. No s'entrenen als pesos fets volàtils que s'han de recuperar actualitzats.
