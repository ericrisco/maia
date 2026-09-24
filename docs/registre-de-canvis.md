---
type: index
title: "Registre de canvis del cervell andorrà"
---

# Registre de canvis del cervell andorrà

Aquesta pàgina explica, commit a commit, què entra al corpus i per què. Cada
entrada correspon a un commit del repositori i en repeteix el títol: per trobar
el canvi exacte, cerqueu el títol a `git log`. Cada entrada diu quina font s'ha
incorporat o revisat, quins articles en depenen, on és el material de partida
i quin diari de treball documenta la troballa i els seus límits.

Les entrades s'afegeixen al final. No es reescriuen: si una font canvia, se'n
fa una entrada nova.

## Abans d'aquest registre

Fins al 24 de setembre de 2026 el repositori acumulava 2.733 commits locals
sense publicar. Es van publicar tots de cop, amb una sola intervenció a
l'historial: `docs/raw/estadistica-api/resta-del-cataleg/resta-cataleg-api-2026-09-18.tsv`
(102,6 MB) supera el límit de 100 MB de GitHub i es va migrar a Git LFS a tots
els commits on apareix. El contingut del fitxer no ha canviat.

La descripció d'aquells commits és al seu missatge (`git log`). Aquest registre
comença amb la tanda següent: la revisió del cervell per relació amb Andorra i
les fonts arxivístiques incorporades entre el 22 i el 25 de setembre de 2026.

## Entrades


### 1. 🧹 retira del cervell el material sense relació amb Andorra

Revisió document a document del brain: un fitxer no es considera andorrà només perquè contingui la paraula «Andorra». S'eliminen cinc blocs EWA sense relació amb el país (l'homònim de Budapest 1939–1940, la genealogia Belfort/Delvert/Carla, l'arxiu familiar de Chciuk, el dossier Stempowski i el catàleg SPP) i el capítol de David Crystal sobre l'anglès mundial, que no aportava cap dada andorrana; la dada bibliogràfica es manté a l'article de manlleus. Es conserven explícitament els dossiers de Miranda, Girona, Viadiu i Grumbach perquè alimenten Els passadors. La nota de Fontargente perd l'apèndix sense dades andorranes. El detall fitxer a fitxer (5.310 baixes) és a 2026-09-23-revisio-brain-andorra-deletes.tsv.

- Fitxa retirada: `fonts/david-crystal-english-worldwide.md`
- Material de partida: 8 fitxers a `raw/sdd/ewa/budapest-homonym/`, `raw/sdd/ewa/chciuk-celt/family-archive/`, `raw/sdd/ewa/chciuk-celt/jerzy-stempowski/`, `raw/sdd/ewa/chciuk-celt/krzysztof-tutaj/spp/`, `raw/sdd/ewa/chciuk-celt/miranda/`, `raw/sdd/ewa/eloise-fontargente/` …
- Diari de treball: `raw/worklog/2026-09-23-revisio-brain-andorra-deletes.tsv`
- Diari de treball: `raw/worklog/2026-09-23-revisio-brain-andorra.md`

### 2. 📝 incorpora ACA-2339 — Rebuts del cens anual de l’empriu de Lles, 1600

La fitxa **ACA-2339** descriu rebuts del cens anual que la parròquia d’Andorra paga a la Baronia de Lles per l’empriu a la muntanya de Lles, amb data de 24 d’agost de 1600.

- Fitxa: [ACA-2339 — Rebuts del cens anual de l’empriu de Lles, 1600](fonts/aca-2339-cens-anual-lles-1600.md)
- Article nou: [El cens anual de l’empriu de Lles, 1600](temes/historia/antic-regim/cens-anual-empriu-lles-1600.md)
- Material de partida: 4 fitxers a `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/cens-anual-lles-1600/`
- Diari de treball: `raw/worklog/2026-09-23-cens-anual-lles-1600.md`

### 3. 📝 incorpora ACA-2371 — Apoca i censos de la muntanya de la Pera, 1635–1642

La fitxa **ACA-2371** descriu una apoca feta per **Ramon Rocabruna i de Cadell** a favor de la **Universitat d’Andorra**, corresponent al pagament anyal de la muntanya de la Pera, a Arànser. La mateixa unitat incorpora un rebut dels censos dels anys 1636 a 1642.

- Fitxa: [ACA-2371 — Apoca i censos de la muntanya de la Pera, 1635–1642](fonts/aca-2371-censos-pera-1635-1642.md)
- Article nou: [Els censos de la muntanya de la Pera, 1635–1642](temes/historia/antic-regim/censos-de-la-pera-1635-1642.md)
- Material de partida: 4 fitxers a `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/censos-pera-1635-1642/`
- Diari de treball: `raw/worklog/2026-09-23-censos-pera-1635-1642.md`

### 4. 📝 incorpora ACA-282 — Venda perpètua de l’empriu de la Pera, 15 d’agost de 1475

La fitxa **ACA-282** descriu una certificació i còpia de la ratificació feta per Miquel i Joan Cadell de la venda perpètua de l’empriu de la muntanya de la Pera per Joan Cadell a Joan Ortadó i Salvador Sucarana, representants de la parròquia d’Andorra.

- Fitxa: [ACA-282 — Venda perpètua de l’empriu de la Pera, 15 d’agost de 1475](fonts/aca-282-empriu-pera-1475.md)
- Article nou: [La venda perpètua de l’empriu de la Pera, 1475](temes/historia/edat-mitjana/la-venda-perpetua-delempriu-de-la-pera-1475.md)
- Material de partida: 4 fitxers a `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/empriu-pera-venda-1475/`
- Diari de treball: `raw/worklog/2026-09-23-empriu-pera-venda-1475.md`
- Diari de treball: `raw/worklog/2026-09-23-proces-empriu-cantabra-pera-1542.md`

### 5. 📝 incorpora ACA-322 — Procés pels emprius de Cantabrà i la Pera, 1542

Abast: Unitat ACA-322, 28 folis catalogats, procés judicial de 1542

- Fitxa: [ACA-322 — Procés pels emprius de Cantabrà i la Pera, 1542](fonts/aca-322-proces-emprius-1542.md)
- Article nou: [El procés dels emprius de Cantabrà i la Pera, 1542](temes/historia/edat-mitjana/el-proces-dels-emprius-de-cantabra-i-la-pera-1542.md)
- Material de partida: 4 fitxers a `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/proces-empriu-cantabra-pera-1542/`

### 6. 📝 incorpora ACA-323/324 — Original i traducció de la sentència de l’empriu de la Pera,…

Abast: ACA-323 i ACA-324, inventari 23680, data 18 de desembre de 1572; traducció castellana i original llatí de la sentència

- Fitxa: [ACA-323/324 — Original i traducció de la sentència de l’empriu de la Pera, 1572](fonts/aca-323-324-sentencia-pera-1572.md)
- Material de partida: 7 fitxers a `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/sentencia-pera-1572-original-traduccio/`

### 7. 📝 incorpora ACA-335 — Rodalia de l’empriu de la Pera, 1792

La fitxa **ACA-335** descriu la rodalia de l’empriu que la parròquia d’Andorra té amb els de Lles i Aransa, al terme o muntanya de la Pera.

- Fitxa: [ACA-335 — Rodalia de l’empriu de la Pera, 1792](fonts/aca-335-rodalia-empriu-pera-1792.md)
- Article nou: [La rodalia de l’empriu de la Pera es descriu per fites, 1792](temes/historia/antic-regim/rodalia-empriu-pera-1792.md)
- Material de partida: 4 fitxers a `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/rodalia-empriu-pera-1792/`
- Diari de treball: `raw/worklog/2026-09-23-rodalia-empriu-pera-1792.md`

### 8. 📝 incorpora Arxius en Línia — ACA-46, ACA-47 i ACA-48: declaracions sobre la sortida de…

Abast: ACA-46, ACA-47 i ACA-48, declaracions de veïns de la Cerdanya datades el 1631

- Fitxa: [Arxius en Línia — ACA-46, ACA-47 i ACA-48: declaracions sobre la sortida de blat, 1631](fonts/aca-46-48-declaracions-cerdanya-1631.md)
- Material de partida: 41 fitxers a `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/`, `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/concòrdia-lles-1570/`, `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/empriu-pera-arancer-1481/`, `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/empriu-pera-audiencia-1572/`, `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/emprius-lles-travesseres-1386/`, `raw/web/institucions/arxiu-nacional/arxiu-comunal-andorra/franquicia-cerdanya-1631-1634/` …

### 9. 📝 incorpora ACA-5344 — Execució de la sentència sobre els emprius de Lles i Travesseres…

La fitxa oficial **ACA-5344** del portal Arxius en Línia descriu l’execució, datada el 6 d’agost de 1386, d’una sentència dictada a Puigcerdà en el litigi entre la parròquia d’Andorra i Sibil·la, muller de Pere d’Aragall, pels emprius andorrans de Lles i Travesseres.

- Fitxa: [ACA-5344 — Execució de la sentència sobre els emprius de Lles i Travesseres, 1386](fonts/aca-5344-emprius-lles-1386.md)
- Article nou: [Andorra defensa els emprius de Lles i Travesseres, 1386](temes/historia/edat-mitjana/andorra-defensa-emprius-lles-travesseres-1386.md)
- Diari de treball: `raw/worklog/2026-09-23-emprius-lles-travesseres-1386.md`

### 10. 📝 incorpora ACA-5347 — Sentència sobre la lleuda de la vall de Querol, 26 de novembre d…

La fitxa oficial **ACA-5347** d’Arxius en Línia descriu la sentència de 26 de novembre de 1401 dictada per Joan de Masguillem, lloctinent del jutge del patrimoni reial, en el litigi entre Andreu Igòsol i els andorrans representats per Joan Garreta, Arnau Berenguer i Joan Babot.

- Fitxa: [ACA-5347 — Sentència sobre la lleuda de la vall de Querol, 26 de novembre de 1401](fonts/aca-5347-lleuda-querol-1401.md)
- Diari de treball: `raw/worklog/2026-09-23-lleuda-querol-1401.md`

### 11. 📝 incorpora ACA-5348 — Petició perquè l’oficial d’Urgell administri justícia, 1409

La fitxa pública de l’**ACA-5348** descriu la petició de Pere Sança i Pere Batlle, d’Andorra la Vella, en representació dels andorrans, davant de Vicenç Morató, oficial d’Urgell i vicari general, en un litigi en què la part contrària no s’havia presentat al dia assignat.

- Fitxa: [ACA-5348 — Petició perquè l’oficial d’Urgell administri justícia, 1409](fonts/aca-5348-peticio-justicia-urgell-1409.md)
- Article nou: [Dos veïns d’Andorra exigeixen que l’oficial d’Urgell faci justícia, 1409](temes/historia/edat-mitjana/peticio-justicia-urgell-1409.md)
- Diari de treball: `raw/worklog/2026-09-25-peticio-justicia-urgell-1409.md`
