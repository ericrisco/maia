# Pla de producció dels datasets de Maia

Aquest pla governa el treball tema a tema a `training-data/knowledge/` i peça a peça a `training-data/language/`. La font factual és el corpus actual de Maia. El format públic és el definit a [SPEC.md](SPEC.md).

## Seqüència

### 1. Recuperar una base revisable

- Mantenir els dos datasets separats.
- Crear fitxers de revisió humans i conservar els outputs finals en `output/`.
- Tractar qualsevol generador antic com a eina d'inventari, no com a autoritat editorial ni com a generador final sense superar els exemples i criteris de `knowledge/review/EXEMPLES.md`.
- Registrar inventari, procedència, unitats d'evidència, relacions, exclusions i errors de parseig en fitxers interns.

### 2. Inventariar tot el corpus

- Enumerar els 1.477 documents de `docs/temes/` i classificar-los dins de les tretze branques.
- Extreure unitats semàntiques respectant seccions, llistes, taules i relacions internes.
- Inspeccionar els 45 documents Markdown de `docs/parla/`; separar fitxes de contingut, índexs i material no elegible.
- Verificar font, atribució, llicència, termes de redistribució i estat de transcripció abans d'exportar material.
- Produir un report de cobertura inicial amb quantitats i motius de pendència o exclusió.

### 3. Escriure i revisar converses de Knowledge

- Treballar una branca temàtica cada vegada, seguint l'ordre definit a `knowledge/TEMES.md`.
- Llegir la fitxa sencera abans de redactar preguntes; després tractar cada unitat útil una per una.
- Convertir conceptes relacionats en converses naturals de dos o més intercanvis, amb seguiments reals.
- Incloure les preguntes factuals, explicatives, comparatives i contextuals que el corpus pugui respondre. No generar variants mecàniques.
- Escriure respostes completes en català natural. Preservar qualificadors, atribucions, desacords i desconeixement.
- Enregistrar la cobertura interna de cada afirmació i rebutjar respostes fragmentàries, genèriques o no sustentades.
- Tancar una branca només quan totes les seves fitxes i unitats útils tinguin conversa o exclusió justificada.

### 4. Curar Language sense falsejar la font

- Revisar cada peça elegible i cada interval incert.
- Fer servir només fragments humans que siguin prou fiables i redistribuïbles segons la font.
- Crear un prompt contextual només quan el fragment és una resposta semànticament vàlida. Conservar literalment el text del parlant i registrar que el prompt és editorial.
- Si la peça és monòleg, transcripció incerta, veu no acreditada o sense permís suficient, registrar-la com a pendent/exclosa; no fabricar una conversa real ni atribuir torns.
- Dividir train/validation/test per font, peça i parlant quan sigui possible.

### 5. Validar i exportar

- Validar JSONL, alternança de rols, contingut no buit, duplicats, frases completes, traçabilitat i absència de metadades internes.
- Auditar manualment tots els casos dubtosos i una mostra de cada branca i font.
- Comprovar que cap grup d'evidència o peça de parla apareix en més d'un split.
- Exportar els tres splits només des de registres aprovats.
- Generar reports de cobertura, exclusions, permisos, splits i validació.

## Regla d'avanç

Cada conversa de Knowledge s'incorpora després d'una revisió de la pregunta, de tots els torns, de la resposta i de la traça. Es valida i es publica en un commit propi abans de passar a la pregunta següent, tal com ha demanat Eric. Els commits no substitueixen la revisió de cobertura del tema complet.

## Definition of done

Knowledge no és complet fins que les tretze branques i totes les seves unitats útils estiguin conciliades amb converses o exclusions motivades, i els tres splits passin les validacions.

Language no és complet fins que totes les peces s'hagin revisat, totes les inclusions siguin traçables i compatibles amb la font, els splits no tinguin fuga i els permisos siguin coneguts o les peces pendents quedin fora de l'exportació.

El projecte complet no s'ha de marcar com acabat mentre un tema, una peça, una exclusió o una condició de procedència resti sense estat justificat.
