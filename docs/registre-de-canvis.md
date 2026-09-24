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

### 12. 📝 incorpora ACA-5359 — Ratificació de l’empriu de la Pera i del bestiar foraster, 1481

La fitxa **ACA-5359** d’Arxius en Línia descriu una acta de 12 de setembre de 1481 en què Joan Catell, senyor d’Arànser, reconeix i ratifica un acord sobre el bestiar foraster del domini d’Arànser i de la parròquia d’Andorra, lligat a la venda a carta de gràcia de la muntanya i empriu de la Pera a favor dels cònsols Antoni Moles i Arnau Ribot.

- Fitxa: [ACA-5359 — Ratificació de l’empriu de la Pera i del bestiar foraster, 1481](fonts/aca-5359-empriu-pera-1481.md)
- Diari de treball: `raw/worklog/2026-09-23-empriu-pera-arancer-1481.md`

### 13. 📝 incorpora ACA-5362 — Pagament del cens de l’empriu de Lles i Travesseres, 1489

La fitxa **ACA-5362** descriu l’acta del pagament del cens anual que la parròquia d’Andorra ha de pagar per l’empriu a les muntanyes de Lles i Travesseres, i el rebuig de l’àpoca per part del batlle Joan Mor, per instrucció de Pere d’Ortafà.

- Fitxa: [ACA-5362 — Pagament del cens de l’empriu de Lles i Travesseres, 1489](fonts/aca-5362-cens-lles-travesseres-1489.md)
- Article nou: [Quan el batlle de Travesseres rebutja l’àpoca del cens, 1489](temes/historia/antic-regim/cens-empriu-lles-travesseres-1489.md)
- Diari de treball: `raw/worklog/2026-09-23-cens-empriu-lles-travesseres-1489.md`

### 14. 📝 incorpora ACA-5367 — Concòrdia entre Lles i Andorra sobre els emprius, 1570

La fitxa **ACA-5367** descriu una còpia de la concòrdia signada a Lles el 22 de juny de 1570 entre representants de la baronia de Lles i els cònsols d’Andorra, dins un litigi per penyoraments i emprius de les muntanyes de Lles.

- Fitxa: [ACA-5367 — Concòrdia entre Lles i Andorra sobre els emprius, 1570](fonts/aca-5367-concordia-lles-1570.md)
- Article nou: [Abans de la sentència, Lles i Andorra signen una concòrdia pels emprius, 1570](temes/historia/antic-regim/concordia-lles-andorra-emprius-1570.md)
- Diari de treball: `raw/worklog/2026-09-23-concordia-lles-1570.md`

### 15. 📝 incorpora ACA-5368 — Sentència de la Reial Audiència sobre l’empriu de la Pera, 1572

La fitxa **ACA-5368** d’Arxius en Línia descriu una sentència de la Reial Audiència de Barcelona, datada el 18 de desembre de 1572, davant les al·legacions de la parròquia d’Andorra contra una sentència de Jaume Tora, jutge d’Arànser, en el litigi amb Miquel Cadell i el seu fill Joan pels emprius de la muntanya de la Pera.

- Fitxa: [ACA-5368 — Sentència de la Reial Audiència sobre l’empriu de la Pera, 1572](fonts/aca-5368-empriu-pera-1572.md)
- Article nou: [La Reial Audiència intervé en l’empriu de la Pera, 1572](temes/historia/antic-regim/la-reial-audiencia-i-empriu-pera-1572.md)
- Diari de treball: `raw/worklog/2026-09-23-empriu-pera-audiencia-1572.md`

### 16. 📝 revisa Actes històriques del Consell General (1289-1864)

- Fitxa: [Actes històriques del Consell General (1289-1864)](fonts/actes-historiques-consell-general.md)
- Article nou: [El Consell arbitra un conflicte de ramats entre valls, 1592](temes/historia/antic-regim/el-consell-arbitra-un-conflicte-de-ramats-entre-valls-1592.md)
- Article nou: [Abans del Consell: síndics, costums i comunals (1331-1364)](temes/historia/edat-mitjana/abans-del-consell-sindics-costums-i-comunals-1331-1364.md)
- Article nou: [De la citació comtal a la franquesa comercial (1381-1391)](temes/historia/edat-mitjana/de-la-citacio-comtal-a-la-franquesa-comercial-1381-1391.md)
- Article nou: [Del plet dels emprius al tribunal reial (1510-1556)](temes/historia/edat-mitjana/del-plet-dels-emprius-al-tribunal-reial-1510-1556.md)
- Article nou: [El comú no es privatitza i el Consell tria el jutge, 1480–1482](temes/historia/edat-mitjana/el-comu-no-es-privatitza-i-el-consell-tria-el-jutge-1480-1482.md)
- Article nou: [El Consell paga per matar llops, óssos i llops cervers (1390)](temes/historia/edat-mitjana/el-consell-paga-per-matar-llops-ossos-i-llops-cervers-1390.md)
- Article nou: [El jurament que feia funcionar el càrrec (1442-1456)](temes/historia/edat-mitjana/el-jurament-que-feia-funcionar-el-carrec-1442-1447.md)
- Article nou: [Els jurats contra els dos saigs (1390)](temes/historia/edat-mitjana/els-jurats-contra-els-dos-saigs-1390.md)
- Article nou: [La franquesa de la lleuda, de Querol a Cerdanya (1401–1465)](temes/historia/edat-mitjana/la-franquesa-de-la-lleuda-i-del-maestrat-de-ports-1401-1403.md)
- Article nou: [La quèstia es paga amb crèdit i fiances, 1446–1456](temes/historia/edat-mitjana/la-questa-es-paga-amb-credit-i-fiances-1446-1456.md)
- Article nou: [Quan Andorra feia valer els seus privilegis (1394-1398)](temes/historia/edat-mitjana/quan-andorra-feia-valer-els-seus-privilegis-1394-1398.md)
- Article nou: [Quan el Consell General ja paga, ven i recorre (1448-1498)](temes/historia/edat-mitjana/quan-el-consell-ja-paga-ven-i-recorre-1448-1498.md)
- Article nou: [Quan els pastors obliguen la Vall a fer pau amb Vernet, 1552](temes/historia/edat-mitjana/quan-els-pastors-obliguen-la-vall-a-fer-pau-amb-vernet-1552.md)
- Article nou: [El Consell recorre el manament d’homes armats, 1463](temes/historia/guerres-i-neutralitat/el-consell-recorre-el-manament-dhomes-armats-1463.md)
- Article nou: [El robatori de les mitges de seda i el sometent de Querol, 1712](temes/historia/guerres-i-neutralitat/el-robatori-de-les-mitges-de-seda-i-el-sometent-de-querol-1712.md)
- Article nou: [El veguer avisa de gent armada francesa, 1445](temes/historia/guerres-i-neutralitat/el-veguer-avisa-de-gent-armada-francesa-1445.md)
- Article nou: [La Vall arma els ports i demana salvaguarda, 1689](temes/historia/guerres-i-neutralitat/la-vall-arma-els-ports-i-demana-salvaguarda-1689.md)
- Article nou: [La Vall defensa l’entrada de Catalunya en temps de guerra, 1637](temes/historia/guerres-i-neutralitat/la-vall-defensa-lentrada-de-catalunya-en-temps-de-guerra-1637.md)
- Article nou: [La Vall posa espies i sometent als ports, 1686](temes/historia/guerres-i-neutralitat/la-vall-posa-espies-i-sometent-als-ports-1686.md)
- Article nou: [La Vall prohibeix amagar soldats i desertors, 1737](temes/historia/guerres-i-neutralitat/la-vall-prohibeix-amagar-soldats-i-desertors-1737.md)
- Article nou: [Quan els soldats d'Anserall molesten la Vall, 1699–1700](temes/historia/guerres-i-neutralitat/quan-els-soldats-danserall-molesten-la-vall-1699-1700.md)
- Article nou: [Quan la guerra entra per la frontera: Andorra el 1691](temes/historia/guerres-i-neutralitat/quan-la-guerra-entra-per-la-frontera-1691.md)
- Article nou: [Quan Mèrens tanca els pasturatges a Encamp i Canillo, 1726](temes/historia/guerres-i-neutralitat/quan-merens-tanca-els-pasturatges-a-encamp-i-canillo-1726.md)
- Article nou: [Quan pugen soldats, la Vall prepara pa de munició, 1652](temes/historia/guerres-i-neutralitat/quan-pugen-soldats-la-vall-prepara-pa-de-municio-1652.md)
- Article nou: [Tres-cents o quatre-cents homes armats amenacen la Vall des de l’Hospitalet, 1790](temes/historia/guerres-i-neutralitat/quatre-cents-homes-armats-a-lhospitalet-1790.md)
- Article nou: [Quatre soldats per parròquia davant els moviments de tropes, 1644](temes/historia/guerres-i-neutralitat/quatre-soldats-per-parroquia-davant-els-moviments-de-tropes-1644.md)
- Article nou: [Vint-i-tres soldats s'allotgen a Sant Julià, 1659](temes/historia/guerres-i-neutralitat/vint-i-tres-soldats-sallotgen-a-sant-julia-1659.md)
- Article nou: [Afiliat o masover: qui podia pasturar a Sant Julià, 1727](temes/institucions/comuns-i-parroquies/afiliat-o-masover-qui-podia-pasturar-a-sant-julia-1727.md)
- Article nou: [El bestiar foraster i les herbes d’Encamp, 1761](temes/institucions/comuns-i-parroquies/el-bestiar-foraster-i-les-herbes-dencamp-1761.md)
- Article nou: [El comú de Sant Julià i els arbres del prat, 1750](temes/institucions/comuns-i-parroquies/el-comu-de-sant-julia-i-els-arbres-del-prat-1750.md)
- Article nou: [El conlloc simulat i el cot de les herbes d’Ordino, 1743](temes/institucions/comuns-i-parroquies/el-conlloc-simulat-i-el-cot-de-les-herbes-dordino-1743.md)
- Article nou: [El Consell prohibeix joc i tabola als hostals, 1785](temes/institucions/comuns-i-parroquies/el-consell-prohibeix-joc-i-tabola-als-hostals-1785.md)
- Article nou: [El pas de Rull per la coma de Sant Joan, 1719–1725](temes/institucions/comuns-i-parroquies/el-pas-de-rull-per-la-coma-de-sant-joan-1723.md)
- Article nou: [El prat de Forest, l'aigua i la sentència dels veadors, 1703](temes/institucions/comuns-i-parroquies/el-prat-de-forest-laigua-i-la-sentencia-dels-veadors-1703.md)
- Article nou: [Els fullats del solà del Vesset: una ordenança amb ratllats (1734–1735)](temes/institucions/comuns-i-parroquies/els-fullats-del-sola-del-vesset-1734-1735.md)
- Article nou: [La bohiga d’Anyós i el Quart de la Massana, 1738](temes/institucions/comuns-i-parroquies/la-bohiga-danyos-i-el-quart-de-la-massana-1738.md)
- Article nou: [La casa d'hostal de Canillo i la vesura de la Pasamanera, 1704](temes/institucions/comuns-i-parroquies/la-casa-dhostal-de-canillo-i-la-vesura-de-la-pasamanera-1704.md)
- Article nou: [La cessió de Canalill i el prat de l’Aiguera (1735)](temes/institucions/comuns-i-parroquies/la-cessio-de-canalill-i-el-prat-de-laiguera-1735.md)
- Article nou: [La concòrdia de Canillo es jura davant del Consell, 1699](temes/institucions/comuns-i-parroquies/la-concordia-de-canillo-es-jura-davant-del-consell-1699.md)
- Article nou: [La fadiga de les herbes: revocació i retorn, 1764–1765](temes/institucions/comuns-i-parroquies/la-fadiga-de-les-herbes-revocacio-i-retorn-1764-1765.md)
- Article nou: [La preferència dels naturals en les herbes comunals, 1746](temes/institucions/comuns-i-parroquies/la-preferencia-dels-naturals-en-les-herbes-comunals-1746.md)
- Article nou: [Quan la sentència de la Gunarda era confusa, 1729](temes/institucions/comuns-i-parroquies/la-sentencia-de-la-gunarda-era-confusa-1729.md)
- Article nou: [Les universitats venen una casa de Bixessarri, 1464](temes/institucions/comuns-i-parroquies/les-universitats-venen-una-casa-de-bixessarri-1464.md)
- Article nou: [Quan allotjar forasters porta un cot a Sant Julià, 1736](temes/institucions/comuns-i-parroquies/quan-allotjar-forasters-porta-un-cot-1736.md)
- Article nou: [Quan el Consell envia veadors per tres termes, 1742](temes/institucions/comuns-i-parroquies/quan-el-consell-envia-veadors-per-dos-termes-1742.md)
- Article nou: [Quan el Consell fixa el pas de la fusta a Incles, 1743](temes/institucions/comuns-i-parroquies/quan-el-consell-fixa-el-pas-de-la-fusta-a-incles-1743.md)
- Article nou: [Quan el prat de l'Aiguera perd l'aigua, 1729](temes/institucions/comuns-i-parroquies/quan-el-prat-de-laiguera-perd-laigua-1729.md)
- Article nou: [Quan la Massana discuteix les pinyores d’Enclar, 1743](temes/institucions/comuns-i-parroquies/quan-la-massana-discuteix-les-pinyores-denclar-1743.md)
- Article nou: [Quan la Vall obliga a treure bohiga, 1741](temes/institucions/comuns-i-parroquies/quan-la-vall-obliga-a-treure-bohiga-1741.md)
- Article nou: [Quan les avingudes canvien els termes, 1773](temes/institucions/comuns-i-parroquies/quan-les-avingudes-canvien-els-termes-1773.md)
- Article nou: [Quan Ordino defensa els Solans i la tala, 1708](temes/institucions/comuns-i-parroquies/quan-ordino-defensa-els-solans-i-la-tala-1708.md)
- Article nou: [Qui podia pescar fora del seu terme, 1733](temes/institucions/comuns-i-parroquies/qui-podia-pescar-fora-del-seu-terme-1733.md)
- Article nou: [Un any passa Encamp, l'altre Canillo: pastures i pas, 1702](temes/institucions/comuns-i-parroquies/un-any-passa-encamp-laltre-canillo-pastures-i-pas-1702.md)
- Article nou: [El blat de les rendes es reserva als pobres, 1643](temes/institucions/consell-general/el-blat-de-les-rendes-es-reserva-als-pobres-1643.md)
- Article nou: [El blat fiat i el crèdit per abastir la Vall, 1757–1761](temes/institucions/consell-general/el-blat-fiat-i-el-credit-per-abastir-la-vall-1757-1761.md)
- Article nou: [El Consell defensa els privilegis a Montsó, 1537](temes/institucions/consell-general/el-consell-defensa-els-privilegis-a-montso-1537.md)
- Article nou: [El Consell jura batlles i mira camins, 1619](temes/institucions/consell-general/el-consell-jura-batlles-i-mira-camins-1619.md)
- Article nou: [El desterrament dels Nyerros per contraban de tabac, 1748](temes/institucions/consell-general/el-desterrament-dels-nyerros-per-contraban-de-tabac-1748.md)
- Article nou: [El desterrament perpetu contra el contraban, 1742–1743](temes/institucions/consell-general/el-desterrament-perpetu-contra-el-contraban-1742.md)
- Article nou: [El Dret de Guerra torna a aparèixer el 1688](temes/institucions/consell-general/el-dret-de-guerra-torna-a-apareixer-1688.md)
- Article nou: [El pleit d’Organyà pel passatge dels Tres Pons, 1683](temes/institucions/consell-general/el-pleit-dorganya-pel-pasatge-dels-tres-pons-1683.md)
- Article nou: [El preu de la sal de revena i les fargues, 1764](temes/institucions/consell-general/el-preu-de-la-sal-de-revena-i-les-fargues-1764.md)
- Article nou: [Els albarans governen la frontera: Andorra, 1637–1638](temes/institucions/consell-general/els-albarans-governen-la-frontera-1637-1638.md)
- Article nou: [Els darrers pagaments de la quèstia i els passos tancats, 1863–1864](temes/institucions/consell-general/els-darrers-pagaments-de-la-questia-1863-1864.md)
- Article nou: [Els forasters només poden estar tres dies, 1641](temes/institucions/consell-general/els-forasters-nomes-poden-estar-tres-dies-1641.md)
- Article nou: [Homes armats i forasters sota vigilància, 1768](temes/institucions/consell-general/homes-armats-i-forasters-sota-vigilancia-1768.md)
- Article nou: [L’exili de cinc anys per contravenir les ordenances del tabac, 1757](temes/institucions/consell-general/l-exili-de-cinc-anys-per-contravenir-les-ordenances-del-tabac-1757.md)
- Article nou: [La cerca de Lliran i Carbonell per tabac de contraban (1738)](temes/institucions/consell-general/la-cerca-de-lliran-i-carbonell-per-tabac-de-contraban-1738.md)
- Article nou: [El mal contagiós de França tanca la frontera, 1640](temes/institucions/consell-general/la-contagion-francesa-tanca-la-frontera-1640.md)
- Article nou: [Quan la contribució es paga amb ovelles: Andorra, 1657–1658](temes/institucions/consell-general/la-contribucio-es-paga-amb-ovelles-1657-1658.md)
- Article nou: [La frontera era un expedient: blat, sal i lleuda (1631–1633)](temes/institucions/consell-general/la-frontera-era-un-expedient-1631-1633.md)
- Article nou: [La guarda del morbo i la llana forastera, 1650–1651](temes/institucions/consell-general/la-guarda-del-morbo-i-la-llana-forastera-1651.md)
- Article nou: [La guia de la sal i les hores de la duana, 1744](temes/institucions/consell-general/la-guia-de-la-sal-i-les-hores-de-la-duana-1744.md)
- Article nou: [La plaça de la Vall al col·legi de Foix, 1632](temes/institucions/consell-general/la-placa-de-la-vall-al-collegi-de-foix-1632.md)
- Article nou: [La plaça del col·legi de Foix costa 25 lliures, 1636](temes/institucions/consell-general/la-placa-del-collegi-de-foix-costa-25-lliures-1636.md)
- Article nou: [La plaça del col·legi de Foix es renova, 1739](temes/institucions/consell-general/la-placa-del-collegi-de-foix-es-renova-1739.md)
- Article nou: [La Vall defensa el comerç amb Catalunya amb xifres, 1692](temes/institucions/consell-general/la-vall-defensa-el-comerc-amb-catalunya-amb-xifres-1692.md)
- Article nou: [La Vall defensa el metge cònsol Domènech, 1640](temes/institucions/consell-general/la-vall-defensa-el-metge-consol-domenech-1640.md)
- Article nou: [La Vall defensa l’entrada de moneda davant un edicte reial, 1784](temes/institucions/consell-general/la-vall-defensa-lentrada-de-moneda-1784.md)
- Article nou: [La Vall envia privilegis a París per la forana, 1635–1636](temes/institucions/consell-general/la-vall-envia-privilegis-a-paris-per-la-forana-1635-1636.md)
- Article nou: [La Vall obliga a acceptar moneda francesa i espanyola, 1693](temes/institucions/consell-general/la-vall-obliga-a-acceptar-moneda-francesa-i-espanyola-1693.md)
- Article nou: [La Vall reserva una plaça mèdica i renova els metges conduïts, 1738–1741](temes/institucions/consell-general/la-vall-renova-la-conduccio-dels-metges-1738-1741.md)
- Article nou: [La Vall reserva el blat i prepara l’ermada, 1644](temes/institucions/consell-general/la-vall-reserva-el-blat-i-prepara-lermada-1644.md)
- Article nou: [L’edicte del tabac es llegeix porta per porta, 1767](temes/institucions/consell-general/ledicte-del-tabac-es-llegeix-porta-per-porta-1767.md)
- Article nou: [L'encabesament de sal i la lluita contra el frau, 1743](temes/institucions/consell-general/lencabesament-de-sal-i-la-lluita-contra-el-frau-1743.md)
- Article nou: [El blat s’ha de netejar i vendre amb control públic, 1789](temes/institucions/consell-general/llei-del-blat-netejat-i-magatzem-public-1789.md)
- Article nou: [Preus, pesca i certificats: el mercat sota el Consell (1619–1622)](temes/institucions/consell-general/preus-pesca-i-certificats-1619-1622.md)
- Article nou: [Quan el Bisbe reforça les ordres contra el tabac, 1765](temes/institucions/consell-general/quan-el-bisbe-reforca-les-ordres-contra-el-tabac-1765.md)
- Article nou: [Quan el blat fiat puja a sis lliures, 1742](temes/institucions/consell-general/quan-el-blat-fiat-puja-a-sis-lliures-1742.md)
- Article nou: [Quan el blat tanca la frontera: 1694–1695](temes/institucions/consell-general/quan-el-blat-tanca-la-frontera-1694-1695.md)
- Article nou: [Quan el Consell mobilitza la Vall contra el tabac (1735)](temes/institucions/consell-general/quan-el-consell-mobilitza-la-vall-contra-el-tabac-1735.md)
- Article nou: [Quan el Consell restitueix l'honor d'un conceller, 1740](temes/institucions/consell-general/quan-el-consell-restitueix-lhonor-dun-conceller-1740.md)
- Article nou: [Quan el Consell troba tabac de Bayona a les cases, 1737](temes/institucions/consell-general/quan-el-consell-troba-tabac-de-bayona-a-les-cases-1737.md)
- Article nou: [Quan el ferro paga el Dret de Guerra, 1702](temes/institucions/consell-general/quan-el-ferro-paga-el-dret-de-guerra-1702.md)
- Article nou: [Quan el privilegi de Roger Bernat torna a la frontera: la lleuda de 1693](temes/institucions/consell-general/quan-el-privilegi-de-roger-bernat-torna-a-la-frontera-1693.md)
- Article nou: [Quan els habitants fan de capa als forasters, 1661](temes/institucions/consell-general/quan-els-habitants-fan-de-capa-als-forasters-1661.md)
- Article nou: [Quan la falta de blat tanca la sortida de la Vall, 1738](temes/institucions/consell-general/quan-la-falta-de-blat-tanca-la-sortida-de-la-vall-1738.md)
- Article nou: [Quan la frontera demana un albarà de guerra: 1663–1666](temes/institucions/consell-general/quan-la-frontera-demana-un-albara-de-guerra-1663-1666.md)
- Article nou: [Quan la llana queda retinguda a Sant Julià, 1690](temes/institucions/consell-general/quan-la-llana-queda-retinguda-a-sant-julia-1690.md)
- Article nou: [Quan la mala collita fa mirar blat foraster, 1741](temes/institucions/consell-general/quan-la-mala-collita-fa-mirar-blat-foraster-1741.md)
- Article nou: [Quan la Vall compra blat a Arcavell i el fia, 1743](temes/institucions/consell-general/quan-la-vall-compra-blat-a-arcavell-i-el-fia-1743.md)
- Article nou: [Quan la Vall compra blat a la Seu i el reparteix, 1742](temes/institucions/consell-general/quan-la-vall-compra-blat-a-la-seu-i-el-reparteix-1742.md)
- Article nou: [Quan la Vall demana de nou la confirmació dels privilegis, 1735](temes/institucions/consell-general/quan-la-vall-demana-confirmar-els-privilegis-1735.md)
- Article nou: [Quan la Vall es queda sense apotecari i en contracta un altre, 1737–1738](temes/institucions/consell-general/quan-la-vall-es-queda-sense-apotecari-1737-1738.md)
- Article nou: [Quan la Vall exigeix guia per la sal, 1741](temes/institucions/consell-general/quan-la-vall-exigeix-guia-per-la-sal-1741.md)
- Article nou: [Quan l'albarà torna a la frontera i l'ús propi conserva el privilegi, 1728](temes/institucions/consell-general/quan-lalbara-torna-a-la-frontera-i-lus-propi-conserva-el-privilegi-1728.md)
- Article nou: [Quan l'apotecari conduït no paga talls, 1713](temes/institucions/consell-general/quan-lapotecari-conduit-no-paga-talls-1713.md)
- Article nou: [Quan mor Heredero i la Vall condueix Fresca, 1739](temes/institucions/consell-general/quan-mor-heredero-i-la-vall-condueix-fresca-1739.md)
- Article nou: [Tres dies de presó per un frau de mocadors de seda, 1736](temes/institucions/consell-general/tres-dies-de-preso-per-un-frau-de-mocadors-de-seda-1736.md)
- Article nou: [Un any de govern escrit: el Consell General el 1617](temes/institucions/consell-general/un-any-de-govern-escrit-1617.md)
- Article nou: [Vint-i-quatre hores i trenta dies de presó per plantar tabac, 1783](temes/institucions/consell-general/vint-i-quatre-hores-i-trenta-dies-de-preso-per-tabac-1783.md)
- Article nou: [El batlle comtal ha de jurar els usos de la Vall, 1538](temes/institucions/coprincipat/el-batlle-comtal-ha-de-jurar-els-usos-de-la-vall-1538.md)
- Article nou: [El comissari del rei de França visita la Vall, 1620](temes/institucions/coprincipat/el-comissari-del-rei-de-franca-visita-la-vall-1620.md)
- Article nou: [El Consell suspèn el substitut del veguer i endureix el control del tabac, 1771](temes/institucions/coprincipat/el-consell-suspen-el-substitut-del-veguer-1771.md)
- Article nou: [El nou veguer francès i les dues sisenes de batlle, 1788](temes/institucions/coprincipat/el-nou-veguer-frances-i-les-dues-sisenes-1788.md)
- Article nou: [El veguer episcopal juramenta a la Casa del Consell, 1681](temes/institucions/coprincipat/el-veguer-episcopal-juramenta-a-la-casa-del-consell-1681.md)
- Article nou: [La festa de Sant Ermengol i el calendari del Consell, 1762](temes/institucions/coprincipat/la-festa-de-sant-ermengol-i-el-calendari-del-consell-1762.md)
- Article nou: [La nominació del batlle episcopal passa per la sisena, 1644](temes/institucions/coprincipat/la-nominacio-del-batlle-episcopal-passa-per-la-sisena-1644.md)
- Article nou: [La possessió del veguer que va posar a prova les regalies, 1758–1759](temes/institucions/coprincipat/la-possessio-del-veguer-que-va-posar-a-prova-les-regalies-1758-1759.md)
- Article nou: [La Seu vacant i les rendes episcopals, 1656](temes/institucions/coprincipat/la-seu-vacant-i-les-rendes-episcopals-1656.md)
- Article nou: [La sisena del batlle episcopal quan el Bisbe és lluny, 1640](temes/institucions/coprincipat/la-sisena-del-batlle-episcopal-quan-el-bisbe-es-lluny-1640.md)
- Article nou: [La sisena del batlle francès, 1740](temes/institucions/coprincipat/la-sisena-del-batlle-frances-1740.md)
- Article nou: [La sisena del batlle francès, 1743](temes/institucions/coprincipat/la-sisena-del-batlle-frances-1743.md)
- Article nou: [La sisena per al batlle del veguer francès, 1641](temes/institucions/coprincipat/la-sisena-per-al-batlle-del-veguer-frances-1641.md)
- Article nou: [La sisena per triar el batlle episcopal, 1704](temes/institucions/coprincipat/la-sisena-per-triar-el-batlle-episcopal-1704.md)
- Article nou: [La Vall arrenda les rendes episcopals a Beuregart, 1642–1643](temes/institucions/coprincipat/la-vall-arrenda-les-rendes-episcopals-a-beuregart-1642-1643.md)
- Article nou: [Quan el Bisbe canvia el batlle i la Vall nomena un interí, 1786](temes/institucions/coprincipat/quan-el-bisbe-canvia-el-batlle-i-la-vall-nomena-un-interi-1786.md)
- Article nou: [Quan el bisbe Curado entra a Andorra, 1740](temes/institucions/coprincipat/quan-el-bisbe-curado-entra-a-andorra-1740.md)
- Article nou: [Quan el jutge episcopal posa en joc la seva jurisdicció, 1724–1725](temes/institucions/coprincipat/quan-el-jutge-episcopal-posa-en-joc-la-seva-jurisdiccio-1724-1725.md)
- Article nou: [Quan el veguer retira un ordre sobre els danys del bestiar, 1770](temes/institucions/coprincipat/quan-el-veguer-retira-un-ordre-sobre-els-danys-del-bestiar-1770.md)
- Article nou: [Quan França nomena veguer i Andorra li pren jurament, 1703](temes/institucions/coprincipat/quan-franca-nomena-veguer-i-andorra-li-pren-jurament-1703.md)
- Article nou: [Quan la Vall paga la quèstia episcopal, 1742](temes/institucions/coprincipat/quan-la-vall-paga-la-questia-episcopal-1742.md)
- Article nou: [Quan les Corts no es poden obrir dues vegades: 1704](temes/institucions/coprincipat/quan-les-corts-no-es-poden-obrir-dues-vegades-1704.md)
- Article nou: [Quan mor el Bisbe i la Vall reorganitza els càrrecs, 1737–1738](temes/institucions/coprincipat/quan-mor-el-bisbe-i-la-vall-reorganitza-els-carrecs-1737-1738.md)
- Article nou: [Qui exerceix la jurisdicció d’Andorra? La resposta del Consell, 1775](temes/institucions/coprincipat/qui-exerceix-la-jurisdiccio-dandorra-1775.md)
- Article nou: [El Consell defensa les Valls davant un clam de pau i treva, 1460](temes/institucions/justicia/el-consell-defensa-les-valls-davant-un-clam-de-pau-i-treva-1460.md)
- Article nou: [El dret comú per damunt de les lleis veïnes, 1753](temes/institucions/justicia/el-dret-comu-per-damunt-de-les-lleis-veines-1753.md)
- Article nou: [El robatori de Fontargent i la recerca dels malfactors, 1680](temes/institucions/justicia/el-robatori-de-fontargent-i-la-recerca-dels-malfactors-1680.md)
- Article nou: [La cacera de bruixes entra al govern del Consell (1621)](temes/institucions/justicia/la-cacera-de-bruixes-entra-al-govern-del-consell-1621.md)
- Article nou: [La sentència de galera contra Guillem Castellà, 1739](temes/institucions/justicia/la-sentencia-de-galera-contra-guillem-castella-1739.md)
- Article nou: [La sentència que deixa passar el bestiar per Sant Julià, 1703](temes/institucions/justicia/la-sentencia-que-deixa-passar-el-bestiar-per-sant-julia-1703.md)
- Article nou: [La trencada de la presó i la Vall en demana una, 1635](temes/institucions/justicia/la-trencada-de-la-preso-i-la-vall-en-demana-una-1635.md)
- Article nou: [La Vall envia quatre homes per un pres de la Val de Videsós, 1644](temes/institucions/justicia/la-vall-envia-quatre-homes-per-un-pres-de-la-val-de-videsos-1644.md)
- Article nou: [La Vall negocia la guarda dels presos, 1621](temes/institucions/justicia/la-vall-negocia-la-guarda-dels-presos-1621.md)
- Article nou: [Les Corts del veguer francès i el jutge de Foix, 1618](temes/institucions/justicia/les-corts-del-veger-frances-i-el-jutge-de-foix-1618.md)
- Article nou: [Presos trets de la Vall: reclamacions a la Seu, al Bisbe i a Perpinyà, 1686–1687](temes/institucions/justicia/presos-que-surten-de-la-vall-i-no-tornen-1686-1687.md)
- Article nou: [Quan dos veguers obren Corts i la Vall nomena arraonadors, 1681](temes/institucions/justicia/quan-dos-veguers-obren-corts-i-la-vall-nomena-raonadors-1681.md)
- Article nou: [Quan el Consell defensa els usos davant un procés, 1776](temes/institucions/justicia/quan-el-consell-defensa-els-usos-davant-un-proces-1776.md)
- Article nou: [Quan el veguer obre Corts per quatre presos, 1684](temes/institucions/justicia/quan-el-veguer-obre-corts-per-quatre-presos-1684.md)
- Article nou: [Quan els presos obliguen a parlar amb els dos veguers, 1703](temes/institucions/justicia/quan-els-presos-obliguen-a-parlar-amb-els-dos-veguers-1703.md)
- Article nou: [Quan Fiter obre Corts i la Vall nomena rahonadors, 1738](temes/institucions/justicia/quan-fiter-obre-corts-i-la-vall-nomena-raonadors-1738.md)
- Article nou: [Quan la neu obliga a delegar la justícia, 1742](temes/institucions/justicia/quan-la-neu-obliga-a-delegar-la-justicia-1742.md)
- Article nou: [Quan les Corts deixen un deute a la Vall, 1742](temes/institucions/justicia/quan-les-corts-deixen-un-deute-a-la-vall-1742.md)
- Article nou: [Quan les Corts s’obren fora de temps, 1754](temes/institucions/justicia/quan-les-corts-sobren-fora-de-temps-1754.md)
- Article nou: [Quan un pres antic es fa càrrega de la Vall, 1739](temes/institucions/justicia/quan-un-pres-antic-es-fa-carrega-de-la-vall-1739.md)
- Article nou: [Quan una excomunió no podia entrar a Andorra: el mas de Tolse, 1695](temes/institucions/justicia/quan-una-excomunio-no-podia-entrar-a-andorra-1695.md)
- Article nou: [Quan violenten la caixa de la Casa de la Vall, 1778](temes/institucions/justicia/quan-violenten-la-caixa-de-la-casa-de-la-vall-1778.md)
- Article nou: [Quatre presos cap a Barcelona, amb sis homes armats, 1788](temes/institucions/justicia/quatre-presos-capita-general-barcelona-1788.md)
- Article nou: [Un pres de la baronia d'Allés i el preu de la justícia, 1698–1699](temes/institucions/justicia/un-pres-de-la-baronia-dalles-i-el-preu-de-la-justicia-1698-1699.md)
- Article nou: [Una dona presa a Encamp i el Consell que no avança els costos, 1701](temes/institucions/justicia/una-dona-presa-a-encamp-i-el-consell-que-no-avanca-els-costos-1701.md)
- Material de partida: 2 fitxers a `raw/consell-general/actes-historiques/`, `raw/consell-general/actes-historiques/text/`

### 17. 📝 incorpora Jordi Guillamet — Estudi preliminar de les actes històriques

- Fitxa: [Jordi Guillamet — Estudi preliminar de les actes històriques](fonts/actes-historiques-estudi-preliminar.md)
