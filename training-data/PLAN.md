# Pla per crear Maia Training Data

## Objectiu

Crear dos datasets separats, complets, revisables i preparats per al fine-tuning:

- **Maia Knowledge**: coneixement entrenable de `docs/temes/`.
- **Maia Language**: parla humana contemporània elegible de `docs/parla/`.

La cobertura és exhaustiva: cada fitxa, secció, taula, llista, relació, excepció i buit es revisa. Cada element acaba cobert, justificadament exclòs o pendent amb un motiu concret. No hi ha quota de registres. El contracte de `docs/CONTRACT.md` i les condicions de cada font són vinculants. Els fets canviants que el projecte reserva per a recuperació no s'ensenyen com si fossin permanents.

## Principi conversacional de Knowledge

El dataset no és un qüestionari sobre els documents. La persona no sap que hi ha fitxes, seccions, taules ni un corpus. Cada conversa representa un dubte que algú podria tenir sobre Andorra i un seguiment que apareix de manera natural després de la resposta.

Cada registre és una conversa completa i multitorn: com a mínim dues intervencions de `user`, alternades amb respostes de `assistant`. La primera pregunta obre un fil comprensible per si sol. La repregunta s'ancora en la resposta anterior i afegeix una necessitat nova: aclarir-ne una conseqüència, corregir una interpretació, contrastar alternatives o entendre què permet afirmar la informació. No es força el diàleg amb una pregunta de farciment. Si no hi ha un seguiment humà que aporti valor, el punt queda pendent de combinar amb un fil adequat; no s'inventa una repregunta.

Abans d'escriure, formula en una línia la intenció de la persona (per exemple: entendre si una tradició és realment medieval, saber què veurà en una festa o destriar dues versions d'un fet). Escriu la pregunta des d'aquesta intenció, sense mencionar la fitxa ni exposar el procés de recerca. Evita atribuir al parlant experiències inventades com «ahir ho vaig veure» només per fer la pregunta més viva.

Una resposta ha de contestar la pregunta en aquell mateix torn, amb referents clars i prou context. No amaguis la dada principal per repartir-la entre torns. No hi posis IDs, capçaleres, camps, fonts ni estats interns. Distingim fets, tradicions, interpretacions i hipòtesis. Quan el corpus no resol una qüestió o les fonts discrepen, ho expliquem directament i sense completar els buits amb conjectures.

Els criteris pràctics i les converses de calibratge viuen a [`knowledge/review/EXEMPLES.md`](knowledge/review/EXEMPLES.md) i [`knowledge/examples/`](knowledge/examples/). Els exemples són calibratge, no candidats ni exports.

## Porta de qualitat abans d'acceptar cada conversa

1. Llegeix sencera la fitxa i les fitxes enllaçades que calguin per entendre context, contradiccions i límits.
2. Identifica els fets que es volen ensenyar i comprova que una pregunta natural els pugui demanar sense deformar-los.
3. Redacta la conversa com una persona: llegeix només els missatges en veu alta. Si sona a índex, examen, formulari, encadenament de dades o plantilla, refés-la.
4. Comprova cada frase de cada resposta amb les fonts. La bona prosa no valida el fet.
5. Registra documents, afirmacions cobertes, font, llicència, atribució i estat d'ús a `knowledge/review/provenance.jsonl`.
6. Marca a `knowledge/work/coverage.csv` només allò que la conversa cobreix de debò. La resta continua pendent.
7. Valida alternança i estructura del diàleg. Un JSON correcte no compensa un exemple antinatural o incorrecte.

Les candidates amb drets `no` o `pendent` poden quedar en revisió, però no s'exporten. No inferim permís d'entrenament de l'accés públic ni d'una citació. Els drets, l'atribució i les obligacions de compartir igual es revisen per font i ús previst.

## Cobertura de Knowledge

Recorre `docs/temes/` tema per tema i deixa una decisió per cada fitxer. Inspecciona títols, cos, subseccions, paràgrafs, taules i totes les files, llistes, dates, xifres, noms, relacions, cronologies, causes, conseqüències, excepcions, correccions, divergències i buits explícits. No converteixis cada frase en una pregunta. Agrupa informació només quan una persona la voldria entendre dins del mateix fil.

Una unitat de contingut compta com a coberta quan una resposta ensenya la informació amb prou context i sense exagerar-la. Una pregunta superficialment semblant no és cobertura. Les exclusions han d'explicar per què el contingut no és entrenable (p. ex. índex sense fets, dada dinàmica, duplicat, drets no aclarits); els dubtes queden com a pendents, no com a exclusions silencioses.

## Maia Language

Audita totes les peces de `docs/parla/`. `veu: originaria`, `epoca: contemporania` i `apte_llengua: true` només són prefiltre. Confirma per peça que hi ha un parlant humà, que la seva procedència lingüística andorrana contemporània està documentada, que la transcripció concorda amb l'àudio i que els drets permeten l'ús previst. No dedueixis l'accent o l'origen perquè el tema o el canal siguin andorrans.

Preserva les formes orals, el lèxic, l'ordre de paraules i els trets del parlant. No reescriguis la resposta com a català estàndard ni generis una pregunta fictícia si l'original no documenta una interacció. Quan no és conversa, conserva el material en el format que reflecteix qui va dir què. Registra fragments dubtosos descartats, drets, transcripció i motiu d'inclusió o exclusió.

## Estructura i registres

- `knowledge/examples/`: petit conjunt de converses de calibratge i procedència; mai s'exporta automàticament.
- `knowledge/review/conversations.jsonl`: una conversa candidata completa per línia.
- `knowledge/review/provenance.jsonl`: una entrada per candidata, amb fonts, drets i punts coberts.
- `knowledge/work/coverage.csv`: una fila per document de `docs/temes/`, amb estat, contingut cobert i pendents/exclusions explicats.
- `knowledge/output/`: splits aprovats `train.jsonl`, `validation.jsonl`, `test.jsonl`.
- `knowledge/reports/`: cobertura, qualitat, drets, exclusions, deduplicació i splits.
- `language/review/`: material humà verificat i procedència.
- `language/work/coverage.csv`: una decisió per peça de `docs/parla/`.
- `language/output/`: splits finals només quan hi hagi prou material apte i autoritzat.
- `language/reports/`: inclusions, exclusions, verificació, drets i splits.

## Ordre de treball

1. Calibrar el criteri amb `knowledge/examples/`; separar exemples bons, anti-exemples i motius de rebuig.
2. Auditar i reescriure les candidates existents: cap registre es considera bo per inèrcia.
3. Recórrer `docs/temes/` de manera exhaustiva i registrar cobertura o motiu de pendent/exclusió.
4. Afegir una conversa Knowledge revisada per commit. Cada conversa, procedència i actualització de cobertura van juntes. Treballar a `main`, revisar el diff, validar i fer push a `origin` abans de preparar la següent.
5. Auditar totes les peces de `docs/parla/`, escoltar l'àudio, contrastar transcripcions, procedència i drets.
6. Deduplicar i crear splits agrupats per document, tema, peça o parlant per evitar filtracions entre train, validation i test.
7. Validar JSONL, estructura, alternança, registres duplicats, cobertura, drets i exclusions; generar informes.
8. Documentar els totals i totes les limitacions reals. No declarar complet un dataset si queda contingut sense decisió o si els exports no són vàlids i autoritzats.

## Finalització

Knowledge només és complet quan cada fitxer i cada contingut entrenable de `docs/temes/` està cobert per converses revisades o té una exclusió justificada; el conjunt està deduplicat, dividit sense filtracions, validat i acompanyat d'un informe de cobertura.

Language només és complet quan cada peça de `docs/parla/` té una decisió registrada, el material inclòs és humà, lingüísticament verificat i legalment reutilitzable, i els splits són vàlids i agrupats sense filtracions.
