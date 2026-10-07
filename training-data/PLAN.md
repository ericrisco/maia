# Pla de Maia Training Data

## Objectiu complet

Crear dos datasets separats a partir del corpus `docs/`:

- **Maia Knowledge** cobreix de manera exhaustiva el coneixement útil de `docs/temes/` amb converses naturals, correctes i preparades per entrenar.
- **Maia Language** conserva el català andorrà contemporani produït per persones a `docs/parla/`, sense inventar llengua ni respostes.

No es barreja coneixement amb senyal lingüístic. La qualitat i la cobertura tenen prioritat sobre el volum.

## Format actiu

`knowledge/review/conversations.jsonl` conté una conversa per línia, només amb `messages` i torns alterns `user` / `assistant`. La procedència i les unitats cobertes van a `provenance.jsonl`, mai als missatges.

Cada conversa nova es revisa, valida, commiteja i puja individualment a `main`. No s'acumulen converses noves en un mateix commit.

## Com escriure preguntes humanes

1. Decideix quin dubte real vol resoldre una persona; no parteixis del títol o de l'estructura d'una fitxa.
2. Formula una pregunta inicial que s'entengui sense obrir el corpus.
3. Respon-la directament i amb el context necessari.
4. Afegeix un seguiment només quan aparegui un dubte plausible a partir de la resposta anterior.
5. Mantén el fil multitorn quan ajudi a entendre. No allarguis una conversa per complir una quota.
6. Llegeix només les preguntes, en veu alta. Si semblen preguntes d'examen o d'índex, reescriu-les.
7. No inventis una història personal, una opinió ni una experiència de l'usuari.

No preguntis «què diu la secció», «què indica aquesta fila» ni «resumeix la fitxa». Evita «això» si no té un referent clar dins del diàleg. Les respostes no poden ser fragments, títols ni llistes de camps.

Consulta `knowledge/review/EXEMPLES.md` abans de redactar cada registre.

## Cobertura exhaustiva de Knowledge

Processa totes les fitxes de `docs/temes/`, inclosos títols, seccions, paràgrafs, llistes, taules, files, cronologies, nombres, entitats, relacions, comparacions, correccions, divergències i buits explícits. No donis cobertura per acabada comptant converses: cada unitat útil ha d'estar representada en una resposta o tenir una exclusió justificada i auditable.

Mantén inventari regenerable, procedència, decisions de cobertura i grups de deduplicació fora dels missatges. Registra drets, atribució, límits i dades font abans d'incloure informació. No completis amb coneixement extern el que el corpus no resol.

## Maia Language

Inspecciona totes les peces de `docs/parla/`. Només inclou material que compleixi `veu == originaria`, `epoca == contemporania` i `apte_llengua == true`. Revisa drets, consentiment aplicable i fiabilitat de la transcripció. Conserva els fragments humans; no generis respostes que imitin la parla andorrana.

Separa els splits per peça o parlant per evitar que fragments consecutius de la mateixa conversa passin a train i test.

## Exports i validació

No publiquis exports fins que cobertura, drets, deduplicació i splits estiguin revisats. Cada split serà JSONL vàlid amb una conversa per línia. Informa documents inspeccionats, unitats cobertes, exclusions, converses i registres per split. Els exports no es creen buits.

## Fases de treball

1. Calibrar el criteri amb les mostres i la guia actuals.
2. Regenerar inventari i estat de cobertura de `docs/temes/`.
3. Recórrer Knowledge tema a tema, afegint una conversa per commit i push.
4. Auditar i preparar Maia Language en un flux separat.
5. Deduplicar, dividir, validar i publicar els exports i informes.
