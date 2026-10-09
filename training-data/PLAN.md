# Pla de Maia Training Data

## Objectiu final

Preparar dos datasets separats, exhaustius i auditables a partir del corpus complet de `docs/`:

1. **Maia Knowledge:** converses en català sobre tot el coneixement útil d'Andorra a `docs/temes/`.
2. **Maia Language:** fragments o converses de parla andorrana contemporània i humana a `docs/parla/`.

No barrejar els objectius. Les respostes redactades per Knowledge no són senyal lingüístic autèntic. Language no s'infla amb respostes inventades.

## Unitat de cobertura de Knowledge

La cobertura és de coneixement, no de nombre de fitxes ni de registres. Inspeccionar tots els documents de `docs/temes/`, inclosos els índexs quan aportin context o enllaços. Per cada document, revisar títol, descripció, seccions, paràgrafs, llistes, taules i files, dates, xifres, noms, llocs, institucions, causes, conseqüències, relacions, comparacions, excepcions, correccions, divergències, buits explícits i enllaços útils.

Cada afirmació entrenable ha de quedar coberta per una conversa o marcada amb una raó verificable per no convertir-la en pregunta (duplicada, no factual, incerta sense resposta responsable, protegida o no rellevant). No comptar una fitxa com a coberta perquè només se n'ha fet una pregunta genèrica. La cobertura i les exclusions es documenten a `knowledge/work/coverage.csv` i als informes.

## Criteri de preguntes i converses

Tots els registres de Knowledge d'aquesta feina són **multitorn**: com a mínim dues intervencions d'usuari amb les respostes corresponents. Cada conversa comença amb una pregunta que una persona faria sense conèixer l'estructura del corpus. Els seguiments neixen de les respostes i demanen una cosa nova.

Variar de manera natural entre dubtes pràctics, curiositat, aclariment de paraules, premisses equivocades habituals, preguntes de lloc o temps, comparacions i relacions entre temes. No fabricar variació canviant només unes paraules ni afegir preguntes per arribar a una llargada.

Evitar «què explica la secció», «què diu aquesta fila», títols de fitxes emprats com a prompt, fragments penjats i preguntes que exigeixen veure el document intern. Vegeu `knowledge/review/EXEMPLES.md`.

Les respostes resolen el dubte directament, amb context suficient i català natural. Cada fet, matís temporal o incertesa s'ha de poder traçar a les fonts. No omplir els missatges amb IDs, estats interns, notes del pipeline o cites de procedència.

## Procedència i drets

Cada conversa té una fila de procedència amb totes les fonts que la sostenen, llicència/termes, estat de revisió i elegibilitat d'exportació. No convertir `pendent` o `no` en permís. Respectar la fitxa de font i la política de `docs/CONTRACT.md`; registrar els termes de fonts recopilades a `docs/raw/` abans d'incloure-les en un export. Les metadades internes no entren als missatges.

## Cadència de treball

1. Inventariar el corpus i crear un registre de cobertura complet.
2. Revisar fonts i drets abans d'escriure preguntes.
3. Crear una conversa multitorn per unitats de coneixement relacionades; evitar barrejar afirmacions sense fil natural.
4. Verificar cada torn i llegir la conversa sense les metadades.
5. Validar format, procedència, duplicats i correspondència amb la cobertura.
6. Fer un commit i un push a `main` per cada conversa nova, amb només els fitxers d'aquell registre i l'actualització mínima de cobertura/procedència.
7. Revisar bloc per bloc fins que tots els documents i unitats estiguin coberts o tinguin una exclusió raonada.

No continuar després d'un push fallit. No incloure canvis locals no relacionats.

## Maia Language

Aplicar exactament la regla de `docs/CONTRACT.md`: `veu == originaria` i `epoca == contemporania` (equivalent a `apte_llengua == true`). Inspeccionar totes les peces; filtrar fragments incerts amb criteri documentat. Preservar lèxic, sintaxi i ordre de paraules humans, amb normalització mínima i traçable. No inventar preguntes o respostes en veu d'un andorrà.

Agrupar les particions per peça i, si és possible, parlant. No repartir fragments veïns de la mateixa conversa entre train, validation i test.

## Exports i validació final

Crear `train.jsonl`, `validation.jsonl` i `test.jsonl` separadament per Knowledge i Language només després de revisar cobertura, qualitat, deduplicació, drets i agrupació dels splits. Els validators han de comprovar JSONL, rols i continguts no buits, duplicats, alternança, elegibilitat de fonts, drets i cobertura global. Els informes han de permetre explicar què s'ha inclòs, què s'ha exclòs i per què.

El volum mai no substitueix exactitud ni cobertura. No marcar cap dataset complet mentre hi hagi documents o afirmacions útils sense revisar.
