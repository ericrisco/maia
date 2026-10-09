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

1. **Llegeix la font sencera**, incloses les notes sobre què és incert i què no s'ha comprovat.
2. **Busca una situació de conversa recognoscible** que el corpus ajudi a resoldre: una confusió habitual, una decisió pràctica, una comparació que algú ja està fent o una afirmació que li han dit. No inventis una biografia per fer-la sonar humana.
3. **Escriu la pregunta sense mirar el títol de la fitxa.** Ha d'explicar el context imprescindible amb paraules quotidianes. No cal que sigui una pregunta completa si una persona diria «Ah, i això quan passa?» com a seguiment.
4. **Respon com un assistent**, no com un catàleg. Contesta primer, explica els termes locals i afegeix només el context necessari. No copiïs frases editorials com «la fitxa diu» ni comencis amb fragments penjats.
5. **Escolta què obre la resposta.** El torn següent ha de sortir d'aquell punt: aclarir una conseqüència, resoldre una confusió o preguntar per un detall que ara té sentit. Si no n'hi ha, canvia d'angle o descarta la conversa; no afegeixis una segona targeta de preguntes.
6. **Llegeix només el diàleg en veu alta.** Si cada torn sona com una pregunta d'examen, una entrevista al document o una seqüència dissenyada per exhibir cobertura, reescriu-lo.
7. **Comprova naturalitat i fets per separat.** Un diàleg fluid pot contenir errors; una resposta correcta pot continuar sonant artificial. Verifica les afirmacions i registra la procedència i els drets a part.

### Prova de naturalitat abans d'escriure

Redacta primer una nota interna amb aquesta forma: **«La persona vol entendre/decidir/aclarir…»**. Si només pots escriure «vol saber què diu la fitxa», encara no has trobat una consulta humana.

La conversa ha de superar aquestes proves:

- **Context autònom:** s'entén sense veure el document ni els missatges previs.
- **Motiu recognoscible:** s'entén per què algú ho pregunta ara; no n'hi ha prou que la pregunta es pugui formular sobre aquella fitxa.
- **Resposta completa:** el primer enunciat de l'assistent resol el dubte; no és un títol, una llista sense introducció ni un fragment de la font.
- **Seguiment conversacional:** la segona pregunta reacciona a la resposta i demana una aclaració, un límit o una conseqüència que una persona voldria saber a continuació.
- **Veu no fabricada:** no inventis una situació personal («m'ha passat…», «vull denunciar…») si no cal per formular el dubte.
- **Veu oral variada:** alterna preguntes directes, dubtes, reaccions, peticions pràctiques i correccions de premissa. No omplis cada registre de «He vist que…», «És veritat que…», «Aleshores…» o «Se sap per què…».
- **Fil de conversa:** no facis que cada diàleg tingui la mateixa arquitectura de dos torns pregunta-resposta ni que cada seguiment sigui una pregunta sobre allò que la font no explica.
- **Varietat real:** no reutilitzis una mateixa plantilla canviant-hi el topònim, la xifra o el nom.

No obliguis tots els registres a tenir el mateix nombre de torns. La pauta habitual és de dues parelles user/assistant, però un seguiment que no sorgeix de la primera resposta és pitjor que descartar el registre. Si la conversa s'allarga, cada torn ha d'afegir una necessitat nova i respondre-la sense perdre el fil.

Abans de redactar, classifica la necessitat —per exemple, aclarir una contradicció, entendre una regla, saber què canvia entre dos casos, comprovar una premissa o entendre una conseqüència—. Fes servir aquesta classificació només per diversificar la cobertura; no converteixis les categories en motlles de pregunta.

La guia vinculant de redacció i revisió és [`knowledge/review/EXEMPLES.md`](knowledge/review/EXEMPLES.md). Els diàlegs de `knowledge/examples/` serveixen només per calibrar el to i no compten com a dades ni com a cobertura. La línia de `knowledge/review/conversations.jsonl` conté només `{"messages":[...]}`; `provenance.jsonl` manté la traça interna alineada per línia, incloent-hi evidències, motiu humà de la consulta, seguiment, estat de revisió i drets.

### Regla multitorn

Una conversa de Knowledge que proposem per a revisió és multitorn: normalment té dues o tres parelles de pregunta i resposta. No hi ha una quota fixa de torns. Cada intervenció ha de reaccionar a l'anterior i fer avançar el mateix fil. Si la continuació només serveix per afegir una dada independent, no és una conversa multitorn útil: busca un altre angle o deixa aquella unitat fora dels candidats.

### Preguntes que es rebutgen

No passen la revisió preguntes com:

- «Què explica la secció “El relat”?»
- «Què indica aquesta fila?»
- «Què diu aquesta fitxa sobre X?»
- «I dos topònims que en surten?»

Depenen del document o produeixen respostes penjades. No n'hi ha prou de canviar «secció» per «text»: cal identificar què vol resoldre la persona.

També es rebutja una pregunta que només soni oral però continuï sent una ordre de lectura, com ara «M'expliques aquest gràfic?» si el diàleg no diu quin dubte vol resoldre. Igualment, una resposta pot ser fluida i continuar sent dolenta si no contesta la pregunta, deixa el referent implícit o barreja fets que la font no relaciona. Expressions com «He vist que…» o «M'han dit que…» no fan humana una pregunta per si soles: només s'usen quan creen un context versemblant i no una excusa per empaquetar un fet.

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
2. Revisar primer els exemples de calibratge amb la guia. La cua actual de `knowledge/review/` conté registres anteriors a aquesta guia: no es consideren aprovats ni una base per crear més registres. Abans de reprendre la producció, cal retirar-los de la cua activa o revisar-los un per un des de la necessitat humana. No afegir registres nous fins que els exemples de calibratge passin la revisió. La cobertura tampoc no es dona per feta perquè hi hagués una pregunta antiga.
3. Treballar fitxa a fitxa i peça a peça. Cada nova conversa de Knowledge es revisa, es valida amb evidència i procedència, i rep el seu propi commit i push a `main` abans de començar la següent.
4. Mantenir registres d'exclusió i cobertura que permetin demostrar què s'ha fet amb cada unitat i cada peça.
5. Resoldre drets i deduplicar abans de fer splits. Knowledge s'agrupa per tema/font quan cal evitar filtració; Language s'agrupa com a mínim per peça i, quan es coneix, per parlant.
6. Crear `train.jsonl`, `validation.jsonl` i `test.jsonl` per separat només amb registres aprovats i fonts aptes per a l'ús. Els conjunts no comparteixen conversa, font contigua ni grup de parlant.
7. Executar els validators i publicar reports de volum, drets, cobertura, exclusions, duplicats i fuites.

El projecte només s'acaba quan totes les unitats útils de Knowledge i totes les peces de Language tenen una decisió verificable; els candidats exportats passen qualitat i drets; els splits i els reports coincideixen amb les dades reals. No s'inventa volum per arribar a una xifra. No s'entrenen als pesos fets volàtils que s'han de recuperar actualitzats.
