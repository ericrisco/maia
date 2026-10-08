# Pla per crear Maia Training Data

## Objectiu i cobertura

Preparar dos datasets separats i traçables per especialitzar Maia:

- **Maia Knowledge**: respostes sobre tot el coneixement entrenable de `docs/temes/`.
- **Maia Language**: català andorrà contemporani extret de parla humana elegible a `docs/parla/`.

La feina cobreix cada fitxa, secció, taula i llista del corpus. Els índexs i les fitxes sense contingut entrenable també es revisen i es marquen amb el motiu d'exclusió. No fixem una quota de registres. No deixem cap branca sense una decisió de cobertura.

El contracte del corpus de `docs/CONTRACT.md` és vinculant. Els fets dinàmics que el projecte reserva per a recuperació no s'han d'ensenyar com si fossin permanents.

## Maia Knowledge: escriure converses útils

Cada registre de `knowledge/review/conversations.jsonl` és una conversa completa, amb missatges `user` i `assistant` alternats. Té com a mínim dues preguntes d'usuari. Cada pregunta podria sorgir en una conversa real, sense que l'usuari conegui les fitxes.

La primera pregunta planteja una curiositat clara. La resposta la resol directament i dona el context necessari. La pregunta següent parteix del que s'acaba de dir i avança el mateix fil: pot aclarir una conseqüència, distingir dues coses, demanar l'abast d'una dada o explorar què no se sap. No repetim la resposta en forma de pregunta ni afegim seguiments per omplir una quota.

Les converses poden tenir més de dos torns d'usuari quan el diàleg ho demani. No fem una pregunta per cada frase de la font. Agrupem fets relacionats en converses que una persona voldria tenir i cobrim punts diferents amb registres diferents.

La resposta ha de:

- respondre primer, en català natural i amb context suficient;
- distingir fet documentat, tradició, interpretació i hipòtesi;
- situar dates i afirmacions en el període corresponent;
- exposar desacords entre fonts sense inventar-ne la conciliació;
- reconèixer què no es pot saber amb les fonts disponibles;
- corregir premisses equivocades amb naturalitat;
- ometre IDs, noms de seccions, estats interns i procedència editorial.

Els criteris i els exemples bons i dolents són a [`knowledge/review/EXEMPLES.md`](knowledge/review/EXEMPLES.md).

## Revisió, procedència i drets

Abans d'afegir una conversa candidata:

1. Llegeix la fitxa sencera, els enllaços pertinents i les fitxes de font.
2. Escriu preguntes que s'entenguin fora del corpus i que no pressuposen fets que la font no dona.
3. Llegeix el diàleg en veu alta sense consultar la fitxa. Reescriu qualsevol torn que soni a formulari, resum o extracció.
4. Verifica cada afirmació i cada límit contra les fonts.
5. Registra a `knowledge/review/provenance.jsonl` els documents, les fonts, les afirmacions cobertes, la llicència, l'atribució i l'estat de reutilització.
6. Actualitza `knowledge/work/coverage.csv` només amb els punts que realment cobreix la conversa.

Les converses amb drets `no` o `pendent` es poden conservar com a candidates de revisió amb l'estat real dels drets. No passen a l'export fins que hi hagi una base documentada per a l'ús previst. Els drets no es dedueixen de l'accés públic ni del fet que una font sigui citada.

Una conversa amb errors factuals o estil mecànic es reescriu sencera. No es promou perquè tingui el format JSON correcte.

## Maia Language: preservar parla real

Audita totes les peces de `docs/parla/`. Només el text amb `veu: originaria`, `epoca: contemporania` i `apte_llengua: true` pot aportar senyal lingüístic. El contingut de `temes/` no es reutilitza per simular una veu andorrana.

La resposta lingüística ha de provenir del parlant. Es conserva el lèxic, l'ordre de paraules i les formes orals; no es reescriu com a català estàndard. Una transcripció dubtosa s'escolta i es contrasta amb l'àudio. S'exclouen els fragments no verificables i es registren les exclusions, la font, els drets i la verificació a `language/work/coverage.csv` i als informes.

Quan el material original no és una conversa, no s'inventa una pregunta com si el parlant l'hagués sentit. Només es creen parells de missatges si l'àudio o la transcripció documenten una interacció real. La resta del senyal lingüístic es manté en un format que no canviï qui ha dit què.

## Cobertura i estructura

- `knowledge/work/coverage.csv`: una fila per cada fitxer de `docs/temes/`; estat, converses, seccions i taules cobertes, o motiu explícit d'exclusió.
- `knowledge/review/conversations.jsonl`: candidates Knowledge, una conversa completa per línia.
- `knowledge/review/provenance.jsonl`: fonts, fets coberts i condicions d'ús per conversa.
- `knowledge/examples/`: calibratge separat, mai barrejat automàticament amb candidates o exports.
- `knowledge/output/`: `train.jsonl`, `validation.jsonl` i `test.jsonl` aprovats.
- `knowledge/reports/`: cobertura, qualitat, exclusions, drets i volum.
- `language/work/coverage.csv`: decisió per cadascuna de les peces de `docs/parla/`.
- `language/review/`: fragments humans revisats i registres de procedència.
- `language/output/`: splits finals de Language quan hi hagi material suficient i autoritzat.
- `language/reports/`: peces incloses i excloses, transcripció, drets i splits.

Una fitxa Knowledge no queda coberta per una sola conversa si té més contingut entrenable. Les files de taules, les llistes, les excepcions i els límits de les fonts també es revisen.

## Git i ordre de treball

Treballa a `main`, tal com ha autoritzat l'usuari. Afegeix una conversa cada vegada. Cada conversa i la seva procedència i cobertura corresponents van en un commit propi, que s'ha de pujar a `origin/main` abans de preparar la següent.

Ordre:

1. Deixar consistents l'inventari i els exemples.
2. Recórrer `docs/temes/` per temes, inclosos tots els continguts entrenables i les exclusions justificades.
3. Crear i revisar converses una per una; actualitzar procedència i cobertura en el mateix commit.
4. Auditar totes les peces de `docs/parla/`, escoltar el material elegible i preparar-ne els fragments humans.
5. Deduplicar i separar els conjunts agrupant per tema, font, peça o parlant per evitar filtracions.
6. Validar JSONL, alternança de missatges, duplicats, procedència, drets i cobertura abans de generar cada export.
7. Documentar el resum final i les limitacions que no es puguin resoldre amb el corpus actual.

## Definició de finalització

Knowledge és complet quan cada document i contingut entrenable de `docs/temes/` està cobert per converses revisades o té una exclusió justificada. Language és complet quan totes les peces de `docs/parla/` tenen una decisió registrada i els splits contenen només parla elegible, prou verificada i reutilitzable. Els dos conjunts tenen exports JSONL vàlids, deduplicats, separats i amb informes de cobertura i limitacions.
