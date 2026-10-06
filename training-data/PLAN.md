# Pla complet dels datasets de Maia

## Objectiu i abast

Preparar dos datasets separats a partir de tot el material pertinent de `docs/`:

- **Knowledge**: ensenyar a respondre conversacionalment sobre tot el coneixement d'Andorra documentat a `docs/temes/`.
- **Language**: preservar català andorrà contemporani produït per persones a `docs/parla/`.

La cobertura ha de ser exhaustiva i auditable. Això no vol dir convertir cada títol, capçalera, enllaç o fragment mecànicament en una pregunta. Cada unitat de contingut s'ha de representar amb una conversa útil, o quedar registrada com a exclosa amb un motiu verificable. Mai sacrificar correctesa o naturalitat per fer pujar el recompte.

## Regles de conversa Knowledge

1. Llegir el document complet i seguir els enllaços necessaris per entendre'n les afirmacions, les fonts, les correccions, les discrepàncies i els límits.
2. Identificar el dubte humà: una decisió pràctica, una confusió, una comparació, una conseqüència o una curiositat concreta.
3. Formular l'obertura sense esmentar la fitxa, l'apartat, la taula ni una dada que només veu qui consulta el document.
4. Respondre primer el dubte, en català natural. Desenvolupar prou el context i els matisos perquè la resposta s'entengui sola.
5. Afegir seguiments quan una persona realment els faria. Cada seguiment ha de néixer del torn anterior i avançar a una distinció, implicació o límit nou. La conversa pot acabar després de qualsevol resposta completa.
6. Si hi ha una premissa falsa, corregir-la amb tacte. Si les fonts discrepen o no ho saben, dir-ho sense inventar una conciliació.
7. Llegir el diàleg sencer en veu alta. Reescriure o descartar qualsevol registre que soni com un examen, una plantilla o una resposta tallada.
8. Registrar fonts, evidència, llicència, termes de reutilització i estat de revisió fora de `messages`.

Els exemples normatius són a `knowledge/review/EXEMPLES.md`. Cap exemple pilot no s'exporta automàticament.

## Cobertura i registre d'exclusions

Inventariar tots els documents de `docs/temes/` i descompondre'n el contingut en unitats auditables: afirmacions, paràgrafs, files de taules, llistes, dates, noms, relacions, correccions i incerteses. Els enllaços s'han de registrar per poder crear síntesis entre temes.

Per a cada unitat útil, fer una o més converses només si aporten intents o coneixement diferents. Si no es pot fer una conversa natural, registrar l'exclusió i el motiu (per exemple: estructura, duplicat, enllaç de navegació sense contingut, fragment il·legible o afirmació sense suport suficient). No amagar mancances de cobertura amb una xifra global.

## Flux incremental obligatori

Treballar a `main`, com ha autoritzat l'usuari. Cada conversa nova es revisa, es valida, es commiteja i es puja a `origin/main` abans de crear la següent. Commits descriptius i petits; mai agrupar diverses converses noves en un commit.

Per cada conversa:

```text
verificar font i drets
→ redactar i revisar diàleg
→ afegir una línia a conversations.jsonl i la traça corresponent
→ validar JSONL, alternança de rols, fidelitat, naturalitat i duplicats
→ git diff --check i revisar git status/diff
→ commit individual
→ push a origin main
→ confirmar working tree net abans de seguir
```

La generació automàtica pot proposar preguntes i respostes, però no pot afegir fets. El conjunt final només inclou material amb drets compatibles i revisió humana aprovada.

## Maia Knowledge

Font principal: `docs/temes/`. Recórrer tots els temes i tots els documents; no limitar-se a un pilot ni a les pàgines amb més enllaços. Cobrir fets, explicacions, cronologies, comparacions, relacions, definicions, excepcions, desacords i buits explícits quan siguin útils per respondre una persona.

Passos:

1. Construir parser Markdown/frontmatter i inventari de documents, seccions, taules, files, enllaços i unitats d'evidència.
2. Crear converses en llenguatge natural tema a tema i pregunta a pregunta. Incloure síntesis entre fitxes quan les relacions estiguin documentades.
3. Revisar tots els registres amb `EXEMPLES.md`, anotar acceptació/reescriptura/rebuig i raó.
4. Cobrir, deduplicar i auditar exclusions per tema, font i tipus d'evidència.
5. Revisar els drets de cada font. Les fonts amb redistribució denegada o pendent no entren als outputs d'entrenament.
6. Fer splits `train`, `validation` i `test` agrupats per tema/font i pregunta base per evitar que reformulacions o contingut gairebé igual es filtrin entre conjunts.

## Maia Language

Font principal: `docs/parla/`. Només utilitzar material amb `veu == originaria`, `epoca == contemporania` i `apte_llengua == true`, segons el contracte vigent del corpus. Revisar manualment cada transcripció i els seus avisos.

- Conservar el text humà literal o amb normalització mínima documentada.
- Si hi ha torns identificables, preservar la conversa original; no inventar preguntes o respostes.
- Excloure fragments incerts o peces inadequades i comptar-los a l'informe amb el motiu.
- Revisar llicència i permisos abans de qualsevol exportació.
- Fer splits agrupats per peça, entrevista i parlant quan es pugui, per evitar leakage.

## Estructura i lliurables

```text
training-data/
├── README.md
├── PLAN.md
├── scripts/
├── knowledge/
│   ├── README.md
│   ├── work/       # inventari, evidència, relacions i exclusions auditables
│   ├── review/     # converses, exemples, rúbrica i procedència
│   ├── output/     # train.jsonl, validation.jsonl, test.jsonl
│   └── reports/    # cobertura, qualitat, drets i exclusions
└── language/
    ├── README.md
    ├── work/       # elegibilitat i selecció de fragments
    ├── review/     # candidats literals i procedència
    ├── output/     # train.jsonl, validation.jsonl, test.jsonl
    └── reports/    # peces incloses/excloses, incerteses i cobertura
```

Els JSONL d'entrenament tenen una conversa per línia i només contenen `messages` amb rols `user` i `assistant`. La procedència, les notes, els IDs i els estats interns no hi entren.

## Definition of Done

**Knowledge** no està acabat fins que tots els documents i unitats útils de `temes/` estiguin coberts o tinguin exclusió justificada; les relacions rellevants estiguin representades; els registres estiguin revisats, deduplicats i amb drets clars; i els tres splits validin sense leakage conegut.

**Language** no està acabat fins que totes les peces elegibles de `parla/` s'hagin inspeccionat; el material incert i els drets estiguin resolts; els fragments preservin parla humana; i els tres splits validin sense leakage conegut.

El report final ha d'indicar recomptes per split, cobertura, exclusió, drets pendents i limitacions. Fins aleshores, l'estat és en curs.
