# Pla de Maia Training Data

## Objectiu

Preparar dos conjunts separats a partir de `docs/`:

- **Maia Knowledge**: converses útils i correctes sobre Andorra, basades en `docs/temes/`.
- **Maia Language**: català andorrà contemporani extret de parla humana elegible a `docs/parla/`.

Knowledge ensenya a resoldre preguntes reals amb coneixement del corpus. Language conserva senyals lingüístics humans. No es barregen.

## Per què reiniciem les converses

Les preguntes enganxades a seccions, files o títols de fitxes semblen exercicis de lectura, no preguntes d'una persona. Algunes respostes començaven a mitja idea. Altres converses repetien la mateixa dada amb un seguiment afegit per rutina.

Per això, les converses anteriors ja no són candidates actives. L'inventari del corpus, els drets de les fonts i les eines de cobertura es conserven. Les converses inicials van servir per calibrar el to; cada una es pot aprovar com a dada només després de revisar naturalitat, contingut i drets. Les que mantenen `approved_sample` no compten com a dades d'entrenament ni com a cobertura.

## Com crear una conversa

1. **Troba una necessitat humana abans d'escriure la pregunta.** Per exemple: entendre una història que algú ha sentit, planificar una visita, aclarir una confusió, comprovar un rumor o comparar dues tradicions.
2. **Escriu la pregunta com si la persona no hagués llegit la fitxa.** No parlis de seccions, files, documents ni unitats. No inventis records, familiars, plans o experiències personals de l'usuari només per fer la pregunta més conversacional. Un dubte concret i directe ja pot sonar humà.
3. **Contesta el dubte directament.** La primera frase ha de resoldre la pregunta. Afegeix només el context necessari i mantén separats el fet, la llegenda, la hipòtesi i allò que no se sap.
4. **Fes seguiment del fil, no del format.** Afegeix un torn quan la resposta desperti una pregunta probable o quedi una decisió pràctica per resoldre. No allarguis una conversa per arribar a un nombre fix de torns.
5. **Llegeix el diàleg sense la font.** Si la pregunta no sona espontània o la resposta no s'entén tota sola, reescriu-la.
6. **Comprova cada afirmació i els drets.** La procedència ha d'indicar fonts, atribució, llicència, límits i grup de divisió. No incorporis una font amb redistribució pendent o prohibida.

### Prova de qualitat

Abans d'aprovar una conversa, comprova aquests quatre punts:

1. **Intenció:** la pregunta demana una explicació, una distinció, una conseqüència o una dada útil. No demana que l'assistent llegeixi en veu alta una part de la fitxa.
2. **Autonomia:** sense veure la font, s'entenen la pregunta i la resposta? Si hi ha «això», «aquesta fila» o un nom sense context, afegeix el referent o descarta el cas.
3. **Resposta completa:** la primera resposta resol la pregunta en prosa clara. No comença a mitja frase ni deixa la dada clau per a un seguiment previsible.
4. **Necessitat del seguiment:** cada torn posterior introdueix una qüestió nova que és probable que sorgeixi de la resposta. Si només confirma o reparteix una resposta que podia anar sencera al primer torn, elimina'l.

Si no es pot formular una pregunta autònoma sense inventar context, o la font només dona un fragment sense explicar què significa, el coneixement es manté a l'inventari i no es força cap registre conversacional. La cobertura no és una quota de preguntes.

## Senyals que una pregunta sona humana

- La persona explica què vol fer, què ha sentit o què li causa dubte.
- La pregunta demana una explicació o una decisió útil, no que es buidi una secció.
- El context és concret i natural, però no pressuposa informació que l'assistent no té.
- El seguiment neix de la resposta anterior i demana una cosa nova.
- La conversa pot acabar després de qualsevol resposta sense que sembli tallada.

## Rebutja o reescriu si

- La pregunta comença amb «què explica la secció», «què indica aquesta fila» o «segons la fitxa».
- Només funciona si es veu un «això» o «aquesta» que no té antecedent al diàleg.
- La resposta és un fragment, una etiqueta o una llista sense context.
- El seguiment repeteix, confirma sense necessitat o canvia de tema bruscament.
- La pregunta és una plantilla aplicada a una dada només per sumar registres.
- La resposta converteix una llegenda, una hipòtesi o una absència de dades en un fet segur.

## Estructura i estat

- `knowledge/review/conversations.jsonl`: només missatges visibles, una conversa per línia.
- `knowledge/review/provenance.jsonl`: una línia paral·lela per conversa, amb drets, afirmacions, límits i estat.
- `knowledge/review/EXEMPLES.md`: exemples bons, dolents i checklist de revisió.
- `knowledge/review/unit-decisions.jsonl`: decisions justificades sobre unitats no entrenables o duplicades.
- `knowledge/work/`: inventari i estat de cobertura regenerables.
- `knowledge/reports/`: informes generats per les eines.
- `knowledge/output/`: splits finals; romanen buits fins que la revisió i la cobertura ho justifiquin.
- `language/`: procés independent per a parla humana elegible.

Les mostres de calibratge tenen `review_status: approved_sample` i `unit_ids: []`. La seva presència no les converteix en dades d'entrenament.

## Seqüència de treball

1. Revisar les mostres de calibratge com a diàlegs independents de les fonts.
2. Ajustar els criteris si una mostra no sona natural o no queda ben fonamentada.
3. Reprendre Knowledge per tema. Primer revisar els drets; després pensar quina necessitat humana resol cada dada útil.
4. Crear una conversa només si el conjunt de fets permet una resposta completa i natural. Agrupar fets relacionats; no exigir una pregunta per unitat.
5. Revisar contingut i procedència. Corregir o rebutjar les converses que fallin qualsevol criteri.
6. Mesurar cobertura sense convertir la cobertura en una quota de preguntes. Marcar explícitament drets irresolts i contingut no factual.
7. Deduplicar per intenció i coneixement, i dividir per grup de contingut per evitar filtracions.
8. Tractar Language només amb material humà que compleixi origen, consentiment, contemporaneïtat, drets i qualitat de transcripció.
9. Generar exports quan hi hagi prou registres revisats. Validar estructura, drets, duplicats, cobertura i separació dels conjunts.

## Criteri d'acabament

Knowledge estarà llest quan el corpus útil estigui cobert sense preguntes artificials, les respostes siguin correctes i naturals, les fonts permetin l'ús, no hi hagi duplicats inútils i els splits i informes siguin vàlids.

Language estarà llest quan totes les peces candidates s'hagin revisat, només s'hi inclogui material elegible, es preservi parla humana real, els splits evitin filtracions i existeixi un informe d'inclusions i exclusions.
