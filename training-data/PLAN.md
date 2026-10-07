# Pla de Maia Training Data

## Objectiu complet

Crear dos datasets separats a partir del corpus `docs/`:

- **Maia Knowledge** cobreix de manera exhaustiva el coneixement útil de `docs/temes/` amb converses naturals, correctes i preparades per entrenar.
- **Maia Language** conserva el català andorrà contemporani produït per persones a `docs/parla/`, sense inventar llengua ni respostes.

No es barreja coneixement amb senyal lingüístic. La qualitat i la cobertura tenen prioritat sobre el volum.

## Format actiu

`knowledge/review/conversations.jsonl` conté una conversa per línia, només amb `messages` i torns alterns `user` / `assistant`. La procedència i les unitats cobertes van a `provenance.jsonl`, mai als missatges.

Cada conversa nova es revisa, valida, commiteja i puja individualment a `main`. No s'acumulen converses noves en un mateix commit.

## Com escriure converses que sonin humanes

La cobertura del corpus i la naturalitat de la conversa són controls diferents. No transformis cada unitat de cobertura en una pregunta. Agrupa el coneixement que serveix a una mateixa necessitat i comprova la cobertura a la procedència.

Abans de redactar, identifica la situació comunicativa: entendre una aparent contradicció, preparar una explicació, comprovar una afirmació, comparar opcions o saber què permet concloure una dada. Formula la pregunta tal com sorgiria en aquella situació, sense referir-te a la fitxa. Escriu seguiments només si un dubte nou apareix de manera plausible després de la resposta.

No imposis una llargada fixa. Una conversa pot acabar després d'una resposta; pot tenir més torns si cada pas aporta una distinció necessària. No repeteixis una forma de diàleg com a plantilla ni inventis una biografia per donar aparença d'autenticitat. Les respostes han de resoldre la necessitat amb les dades i els límits pertinents.

La guia amb exemples calibrats és `knowledge/review/EXEMPLES.md`. Els registres que es van aprovar abans d'aquesta guia no s'han de considerar automàticament aprovats pel criteri nou: s'han de revisar abans de publicar els exports.

## Cobertura exhaustiva de Knowledge

Processa totes les fitxes de `docs/temes/`, inclosos títols, seccions, paràgrafs, llistes, taules, files, cronologies, nombres, entitats, relacions, comparacions, correccions, divergències i buits explícits. No donis cobertura per acabada comptant converses: cada unitat útil ha d'estar representada en una resposta o tenir una exclusió justificada i auditable.

Mantén inventari regenerable, procedència, decisions de cobertura i grups de deduplicació fora dels missatges. Registra drets, atribució, límits i dades font abans d'incloure informació. No completis amb coneixement extern el que el corpus no resol.

## Maia Language

Inspecciona totes les peces de `docs/parla/`. Només inclou material que compleixi `veu == originaria`, `epoca == contemporania` i `apte_llengua == true`. Revisa drets, consentiment aplicable i fiabilitat de la transcripció. Conserva els fragments humans; no generis respostes que imitin la parla andorrana.

Separa els splits per peça o parlant per evitar que fragments consecutius de la mateixa conversa passin a train i test.

## Exports i validació

No publiquis exports fins que cobertura, drets, deduplicació i splits estiguin revisats. Cada split serà JSONL vàlid amb una conversa per línia. Informa documents inspeccionats, unitats cobertes, exclusions, converses i registres per split. Els exports no es creen buits.

## Fases de treball

1. Calibrar el criteri de conversa amb els exemples de `knowledge/review/EXEMPLES.md` i revisar els registres existents amb aquest criteri.
2. Regenerar inventari i estat de cobertura de `docs/temes/`.
3. Recórrer Knowledge tema a tema, creant converses des de necessitats humanes i auditant la cobertura a part.
4. Auditar i preparar Maia Language en un flux separat.
5. Deduplicar, revisar qualitat humana, dividir, validar i publicar els exports i informes.
