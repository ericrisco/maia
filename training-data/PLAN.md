# Pla de Maia Training Data

## Objectiu

Preparar dos datasets independents a partir del corpus de `docs/`:

- **Maia Knowledge** ensenya a respondre preguntes sobre Andorra amb fets documentats a `docs/temes/`.
- **Maia Language** conserva usos reals del català andorrà contemporani a partir de `docs/parla/`.

El resultat ha de ser útil per entrenar un model conversacional. No es tracta de convertir cada fitxa en una pregunta ni de fabricar volum. Cada conversa ha de resoldre un dubte que una persona podria tenir de debò.

## Regla editorial principal

**Escriu primer la situació o el dubte; després formula la pregunta.** No comencis pel títol d'una fitxa, una secció, una fila o una dada que el redactor vol incloure.

Abans de conservar un candidat, completa aquesta frase:

> Una persona preguntaria això perquè vol aclarir / entendre / comprovar / recordar…

Si no es pot acabar amb una motivació concreta, no hi ha conversa: deixa la informació a la cobertura interna i no inventis una pregunta.

### Prova de lectura en fred

Llegeix només els missatges `user`, en ordre, sense mirar la fitxa font:

1. La primera pregunta s'entén sense conèixer el corpus?
2. Sona com una consulta real, no com una ordre d'extracció?
3. El seguiment reprèn una cosa que Maia acaba de dir?
4. Cada nou torn resol una curiositat que ha sorgit de la resposta anterior?
5. El fil s'acaba quan la persona ja té el que volia saber?

Un «no» implica reescriure o descartar. No s'allarga una conversa per assolir una quota de torns. Un intercanvi únic és correcte quan no hi ha cap seguiment natural.

## Què no s'ha de generar

- «Què explica la secció…?», «Què indica aquesta fila?» o «Resumeix aquesta fitxa».
- Fragments que no són preguntes completes: «I dos topònims que en surten:».
- Llistes encobertes: «Digues tres coses sobre X», si no hi ha una necessitat que les motivi.
- Preguntes amb títols, seccions, identificadors interns o referències a «la fitxa» que la persona no coneix.
- Converses teatrals amb una família, una feina, un viatge o una experiència inventats.
- Reformulacions de la mateixa pregunta per inflar el recompte.
- Seguiments universals —«I per què?», «I què més?»— que podrien anar després de qualsevol resposta.
- Preguntes que atribueixen una causa quan les dades només mostren una coincidència o una diferència.

## Criteri de resposta

- Respon la pregunta concreta a la primera frase.
- Dona el context mínim perquè la resposta s'entengui i sigui precisa.
- Escriu com un assistent que explica una cosa, no com una fila d'una base de dades.
- No enumeris totes les dades d'una fitxa si no calen per resoldre el dubte.
- Distingeix fets, interpretacions, llegendes i hipòtesis.
- Si les fonts discrepen, explica què diu cadascuna i si la diferència es pot resoldre.
- Si la font no permet respondre una part, digues-ho clarament. No completis el buit.
- Marca el període quan una dada històrica podria semblar vigent.
- No inventis una veu local per a Maia Knowledge. La naturalitat no és imitar una persona ni afegir falques col·loquials.

## Unitat de treball: una conversa amb una intenció

Una línia de `conversations.jsonl` és una conversa sencera: un intercanvi o un fil amb seguiments. Cada línia nova es revisa, valida, commiteja i puja abans d'obrir la següent. Si té diversos torns, tots formen part del mateix canvi i del mateix registre.

Per tema:

1. Recorre les fitxes i identifica què pot voler saber algú, no quantes preguntes es poden extreure.
2. Revisa el document complet i les fonts que sostenen les afirmacions.
3. Comprova els drets abans que cap contingut entri al dataset.
4. Redacta una conversa candidata amb una motivació concreta.
5. Fes la prova de lectura en fred i comprova cada afirmació contra la font.
6. Guarda procedència i afirmacions sustentades en un fitxer separat.
7. Valida el JSONL, revisa el diff i fes un commit i un push d'aquesta conversa.
8. Actualitza la cobertura només amb el treball que s'ha revisat realment.

Una fitxa pot generar zero, una o diverses converses. No es marca completa perquè tingui una conversa: cal haver revisat totes les unitats rellevants i indicar quines queden cobertes o obertes. Una fitxa sense pregunta humana plausible es registra com a revisada sense conversa, amb una explicació breu.

## Maia Language

Maia Language és un conjunt diferent. Només s'utilitza material elegible de `docs/parla/` amb `veu: originaria`, `epoca: contemporania` i `apte_llengua: true`.

- La resposta ha de provenir de parla humana real.
- No s'inventen diàlegs ni es generen exemples de «com parlaria un andorrà».
- Es preserven lèxic, ordre i construccions del parlant. Només s'apliquen normalitzacions documentades.
- Les transcripcions incertes s'inspeccionen; els fragments no fiables s'exclouen.
- La procedència, el consentiment o base d'ús, els drets i la fiabilitat queden registrats abans de l'exportació.

## Estructura i estat

```text
training-data/
├── PLAN.md
├── README.md
├── knowledge/
│   ├── review/       # guia, exemples editorials, candidats i procedència
│   ├── work/         # inventari i estat de revisió per document
│   ├── scripts/      # inventari, validació i exportació
│   ├── reports/      # cobertura, qualitat i exclusions
│   └── output/       # només exports aprovats
└── language/
    ├── review/       # fragments candidats i procedència
    ├── work/         # elegibilitat i fiabilitat de transcripcions
    ├── scripts/
    ├── reports/
    └── output/       # només exports aprovats
```

`review/EXEMPLES.md` és una guia editorial, no és un dataset. Els registres rebutjats o substituïts van a `review/archive/` i no entren a l'inventari actiu. `output/` només es crea o s'actualitza quan els registres han passat revisió editorial, factual i de drets.

## Format i exports

Una conversa per línia JSONL. El format públic només conté `messages`, amb rols `user` i `assistant`. Procedència, drets, afirmacions i estat editorial es guarden a `provenance.jsonl`.

No es barregen exemples editorials amb candidats. No es publiquen exports mentre la revisió de drets, la deduplicació i l'agrupació per tema o font no estiguin acabades. Els conjunts `train`, `validation` i `test` s'agrupen abans de dividir per evitar filtracions entre converses semblants.

## Revisió de qualitat abans de cada conversa

- **Humana:** algú ho preguntaria sense tenir la fitxa oberta?
- **Clara:** la pregunta inicial diu prou per entendre què vol saber?
- **Connectada:** cada seguiment depèn del torn anterior?
- **Útil:** la resposta resol el dubte sense convertir-se en una llista de dades?
- **Fidel:** cada afirmació és traçable a una font revisada?
- **Prudent:** la resposta respecta els límits, dates i discrepàncies de la font?
- **Reutilitzable:** els drets permeten l'ús previst i consten a la procedència?
- **Diferent:** no duplica una conversa aprovada amb sinònims?

Si alguna resposta és no, es reescriu o es descarta. No hi ha una puntuació mitjana que compensi una pregunta artificial o una afirmació sense suport.

## Fases fins als datasets preparats

1. **Calibratge editorial:** mantenir exemples petits i traçables a `knowledge/review/EXEMPLES.md`. No compten com a registres.
2. **Knowledge, tema a tema:** revisar tots els articles de `docs/temes/`, una fitxa sencera cada vegada. Registrar cobertura i drets abans de donar una conversa per revisada. Cada nova conversa es valida i es puja en el seu propi commit.
3. **Revisió global de Knowledge:** buscar duplicats i fils artificials, comprovar la cobertura de tots els temes, revisar drets i resoldre o marcar fonts pendents. Cap registre arxivat no s'incorpora automàticament.
4. **Language, peça a peça:** auditar cada peça de `docs/parla/`, elegibilitat, consentiment o base d'ús, drets, parlant i fiabilitat de transcripció. Conservar només fragments humans que es puguin verificar.
5. **Splits i exportació:** agrupar converses semblants per font, tema i fil abans de dividir. Crear `train.jsonl`, `validation.jsonl` i `test.jsonl`; cap conversa ni variant propera no pot travessar els splits.
6. **Validació i informes:** validar JSONL, rols, contingut no buit, duplicats, elegibilitat, procedència, exclusions i cobertura. Publicar recomptes i limitacions sense presentar candidats com a registres aprovats.

Els passos 2 i 4 són feina exhaustiva. No es declaren acabats per haver produït un pilot, per tenir un inventari o per haver generat moltes preguntes.

## Prioritats

1. Correctesa, atribució i drets d'ús.
2. Pregunta que una persona faria de debò.
3. Resposta clara i completa per al dubte concret.
4. Seguiments que neixen del fil.
5. Cobertura exhaustiva i varietat sense duplicats.
6. Volum.

La cobertura és exhaustiva en la revisió del corpus, no en el nombre de preguntes. El dataset pot ometre una dada si cap conversa humana la necessita; la cobertura interna ha de mostrar que s'ha revisat.

## Definition of done

**Maia Knowledge** està preparat quan tots els documents de `docs/temes/` s'han revisat, totes les unitats rellevants tenen estat i procedència, les converses actives passen els filtres, els drets estan registrats, els duplicats s'han tractat, i els exports i informes són vàlids.

**Maia Language** està preparat quan totes les peces elegibles de `docs/parla/` s'han inspeccionat, s'han filtrat transcripcions incertes, els fragments humans i la seva procedència són verificables, els splits eviten filtracions i els informes descriuen inclusions i exclusions.
