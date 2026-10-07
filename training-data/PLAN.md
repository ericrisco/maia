# Pla de Maia Training Data

## Objectiu

Preparar exemples de conversa que ensenyin un assistent a resoldre dubtes humans sobre Andorra i, en un conjunt separat, a conservar senyals reals del català andorrà contemporani. El corpus font és `docs/`. No es converteixen documents mecànicament en preguntes.

## Criteri editorial: començar per la intenció

Abans d'escriure cap conversa, l'editor anota en una frase: **«Què intenta aclarir la persona i per què preguntaria això?»** Intencions útils: entendre una pràctica, resoldre una aparent contradicció, comprovar si una història és documentada, saber què va canviar, o distingir dues mesures o tradicions.

Si la motivació és només «aquesta dada surt al document», no es crea el registre. Les preguntes no poden referir-se a una fitxa, secció, taula, fila, font interna o identificador. Tampoc no s'inventa una situació personal per fer veure que la consulta és real.

## Conversa multitorn

- Cada conversa comença amb una pregunta completa, comprensible sense context previ.
- La resposta contesta directament i amb prou context per entendre-la.
- El torn següent surt d'una cosa que s'ha dit o d'un dubte que la resposta deixa obert. Llegides seguides, només les preguntes de l'usuari han de formar un fil coherent.
- Normalment es busquen 2–4 torns d'usuari quan el tema dona peu a aclariments reals. No s'allarga una conversa per arribar a una quota: un intercanvi és millor que un seguiment forçat.
- No s'encadenen preguntes independents dins del mateix missatge. No es fan servir «I què més?» o «I per què?» si no queda clar a què es refereixen.

## Respostes

La primera frase resol la pregunta. La resta explica només el context útil. Cal distingir fets documentats, tradició, interpretació i hipòtesi; situar les xifres en el temps i dir què mesuren; i fer explícites les discrepàncies o els límits de la font. No es completa amb coneixement extern ni s'atribueixen causes que el corpus no demostra.

## Flux de Knowledge

1. Inventariar tots els documents i registrar elegibilitat, procedència i drets. Les fonts amb redistribució prohibida o no verificable queden fora de les cues; l’inventari les compta amb l’estat `excluded_rights` i una raó explícita. Les dades d’actualitat també necessiten una font vigent i datada abans de generar converses.
2. Revisar cada document per unitats de coneixement: afirmacions, dates, noms, relacions, taules, excepcions, desacords i incerteses.
3. Per cada unitat útil, decidir quina intenció humana podria portar-hi; crear una conversa només si la pregunta és versemblant i aporta cobertura nova.
4. Guardar els candidats amb traçabilitat de font i afirmacions sustentades, fora del format final.
5. Fer revisió factual, editorial, de drets, de duplicats i de cobertura abans d'exportar.
6. Separar train/validation/test per tema o grup de fonts relacionades per reduir filtracions entre conjunts.

## Flux de Language

1. Revisar les peces de `docs/parla/` i aplicar els criteris del corpus: veu originària, època contemporània i `apte_llengua: true`.
2. Comprovar drets i qualitat de transcripció abans d'usar fragments.
3. Convertir només intercanvis o fragments humans que admetin un context d'usuari fidel. La resposta ha de conservar el text original o una normalització mínima documentada.
4. No inventar frases «com si les digués un andorrà» ni fabricar seguiments. Si no hi ha un torn humà coherent, es descarta el fragment per a fine-tuning conversacional.
5. Separar els splits per entrevista/peça i, si és possible, parlant.

## Revisió obligatòria de cada conversa Knowledge

Puntuació editorial interna (0–2 per criteri):

- **Intenció humana:** s'entén què vol resoldre la persona?
- **Coherència:** cada seguiment reprèn el fil anterior?
- **Resposta:** contesta directament i amb la llargada necessària?
- **Suport:** cada afirmació està sustentada per una font elegible?
- **Naturalitat:** sona com una conversa real, sense parlar del document?

Un zero en intenció, coherència o suport implica reescriure o descartar. Els exemples editorials no es compten com a dades ni com a cobertura.

## Estructura

- `knowledge/review/`: guia, exemples editorials i més endavant candidats amb procedència.
- `knowledge/work/`: inventaris i estat de cobertura.
- `knowledge/scripts/`: eines de revisió, validació, deduplicació i exportació.
- `knowledge/reports/`: cobertura, drets, exclusions i qualitat.
- `knowledge/output/`: només exports revisats, deduplicats i dividits.
- `language/`: les mateixes fases, amb elegibilitat i fidelitat lingüística pròpies.

## Fites

1. **Calibratge editorial (ara):** aprovar les intencions, la guia i els exemples abans de reprendre la producció de registres.
2. **Knowledge:** inventari i drets; cobertura document a document; producció de converses; revisió i deduplicació; splits i validació.
3. **Language:** elegibilitat, drets i qualitat; selecció de fragments humans; splits sense leakage; validació.
4. **Tancament:** documentar volum, cobertura, exclusions, drets i limitacions de cada conjunt.

Cap fita de producció no es dona per acabada només perquè existeixi l'estructura o hi hagi exemples.
