# Pla de redacció de converses Knowledge

## Objectiu

Crear exemples que ensenyin l'assistent a respondre converses reals sobre Andorra. La persona no ha d'haver vist cap fitxa ni saber com està organitzat el corpus. Les dades factuals surten de `docs/temes/`; les preguntes i les respostes es redacten de nou.

Maia Knowledge i Maia Language són projectes separats. Aquest pla només governa Knowledge. Language conserva fragments de parla humana i no s'ha d'omplir amb diàlegs inventats.

## Què va fallar

Preguntes com «Què explica aquesta secció?» o «Què indica aquesta fila?» parlen del document i no del tema. Les respostes que comencen amb «I dos topònims...» o que només donen una xifra són fragments, no respostes útils. Aquest patró ensenya a completar notes, no a conversar.

## Com escriure una conversa

1. **Parteix d'un dubte humà.** Pot ser una sorpresa, una contradicció aparent, una conseqüència pràctica o una afirmació que la persona vol comprovar. No facis que la persona demani un resum d'una fitxa.
2. **Situa el tema sense fer un preàmbul artificial.** Inclou el lloc, l'època o el fet necessari perquè la conversa s'entengui sola.
3. **Respon primer i explica després.** La primera frase ha de resoldre el dubte. Afegeix el context necessari per entendre la resposta, no totes les dades del document.
4. **Fes que cada repregunta escolti la resposta anterior.** Pot aclarir un terme, comprovar una conseqüència o preguntar què se sap i què no. No canviïs de tema per cobrir una dada pendent.
5. **Escriu com parla una persona.** Admet «Ah, d'acord», «Però llavors...» o una pregunta breu quan el context ja és al diàleg. Evita fórmules repetides i el to d'examen.
6. **No forcis la llargada.** Una mostra té dos o més torns d'usuari quan hi ha un seguiment natural. Si no n'hi ha, busca un altre angle; no inventis una repregunta buida.
7. **Completa les respostes.** Cap resposta pot quedar com un títol, una enumeració sense explicació o una frase dependent d'un torn que no existeix.
8. **Respecta el que la font permet dir.** Separa fets, interpretacions, llegendes i incerteses. Si el corpus no dona un motiu o no resol una discrepància, digues-ho clarament.
9. **No exposis la cuina interna.** No mencionis fitxes, apartats, files, IDs ni estats de revisió. Desa la procedència en un fitxer separat.

## Com revisar

Fes dues passades:

### Lectura cega

Llegeix només els missatges. Aprova la conversa si:

- la primera pregunta s'entén sense veure el corpus;
- sembla una curiositat que algú podria tenir de debò;
- la resposta resol la pregunta amb naturalitat;
- les repreguntes depenen del diàleg i hi afegeixen una curiositat nova;
- cada resposta és completa i no repeteix innecessàriament el que ja s'ha dit.

### Comprovació de fonts

Comprova cada afirmació i registra la procedència, els límits de la font i els drets. Una conversa candidata no s'exporta fins que passi també la revisió de drets. No dedueixis que una dada és actual només perquè apareix escrita en present en una font històrica.

## Estructura i registres

- `knowledge/examples/conversations.jsonl`: exemples de calibratge, no entrenables per defecte.
- `knowledge/examples/provenance.jsonl`: fonts, afirmacions, límits i estat dels drets dels exemples.
- `knowledge/review/conversations.jsonl`: registres candidats pendents de revisió.
- `knowledge/review/provenance.jsonl`: procedència dels candidats.
- `knowledge/work/coverage.csv`: inventari de fitxes i aspectes encara pendents.
- `knowledge/output/`: exports només quan hi hagi registres aprovats i drets compatibles.
- `language/`: procés independent basat en fragments humans elegibles de `docs/parla/`.

El JSONL de converses conté només missatges `user` i `assistant`. Una línia és una conversa sencera. Els exemples inicials fixen el to; no són una quota ni un motlle per copiar.

## Seqüència de treball

1. Acordar el to amb els exemples de calibratge.
2. Per a cada fitxa, llegir-ne el contingut i registrar què queda cobert i què falta.
3. Escriure una conversa candidata que cobreixi un dubte coherent; afegir-ne la procedència.
4. Revisar-la amb la lectura cega i la comprovació de fonts.
5. Validar JSONL, fonts i cobertura. Pujar cada conversa candidata en el seu propi commit a `main` abans de passar a la següent.
6. Més endavant, deduplicar, aprovar drets i preparar els splits. No crear cap export buit o provisional com si fos un dataset acabat.

La cobertura és exhaustiva, però no s'aconsegueix fent una pregunta mecànica per cada paràgraf. Es poden combinar fets relacionats en una conversa útil; es mantenen pendents els detalls que encara no s'han explicat.
