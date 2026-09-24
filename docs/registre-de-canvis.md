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

### 18. 📝 incorpora Introducció als llibres d’actes del Consell General

- Fitxa: [Introducció als llibres d’actes del Consell General](fonts/actes-historiques-introduccio-llibres.md)

### 19. 📝 incorpora Llibre IV de les Actes del Consell General (1743–1864)

- Fitxa: [Llibre IV de les Actes del Consell General (1743–1864)](fonts/actes-llibre-iv-1743-1864.md)
- Article nou: [Els carlins arriben a les actes del Consell, 1838–1839](temes/historia/segle-xix/els-carlins-i-el-consell-1838-1839.md)
- Article nou: [El Consell encarrega un «còdigo de lleys», 1860](temes/institucions/justicia/el-consell-encarrega-un-codi-de-lleis-1860.md)

### 20. 📝 incorpora ADPO 1723-W-3 i l’edició impresa de la Reforma de 1866

Abast: Entrada bibliogràfica 659 del catàleg oficial i descripció secundària del legat ADPO 1723-W-3

- Fitxa: [ADPO 1723-W-3 i l’edició impresa de la Reforma de 1866](fonts/adpo-1723-w3-reforma-1866.md)
- Material de partida: 5 fitxers a `raw/web/institucions/arxius-departamentals-pirineus-orientals/reforma-1866/`

### 21. 📝 incorpora Arxiu Diocesà d’Urgell — fitxa del cercador Arxius de Catalunya

- Fitxa: [Arxiu Diocesà d’Urgell — fitxa del cercador Arxius de Catalunya](fonts/adu-fitxa-arxius-catalunya.md)

### 22. 📝 incorpora Mémoires et Documents / Andorre, 1652–1882 — inventari diplomàtic francès

Abast: Inventari de 411 unitats del fons 6MD/1; per a la Reforma, entrada 48 (31 de maig de 1866) i entrades 67, 69, 77 i 81 sobre el conflicte posterior, inclòs el casino de 1868.

- Fitxa: [Mémoires et Documents / Andorre, 1652–1882 — inventari diplomàtic francès](fonts/archives-diplomatiques-andorra-1652-1882.md)
- Article nou: [La frontera espanyola i la Solana entren en un expedient francès (1850)](temes/historia/segle-xix/solana-frontera-1850.md)
- Material de partida: 5 fitxers a `raw/web/institucions/archives-diplomatiques/andorre-1652-1882/`

### 23. 🔒 deixa fora de git els originals sense dret de redistribució

El repositori és públic. Des d'aquesta entrada, un original (PDF, imatge, captura
HTML, extracte de text) només es publica si la seva fitxa diu `redistribucio: sí`, o
si la carpeta ja versionava fitxers del mateix tipus per una decisió anterior del
projecte (com el text de les actes històriques del Consell General). La resta es
conserva en local per verificar i citar, i queda llistada a `.gitignore`.

- Originals retirats de l'arbre: 42 fitxers pujats a les entrades 2–22 (Archives
  diplomatiques, Arxiu Comunal d'Andorra, Arxiu de les Set Claus, ADPO, Urgell).
  Continuen a l'historial de git; retirar-los'n demanaria reescriure'l.
- Originals que no es pugen en les entrades següents: 458 fitxers.
- Es publiquen igualment les fitxes, els README amb procedència i URL, les metadades
  JSON, els articles i els diaris de treball.

### 24. 📝 incorpora Expedient diplomàtic francès sobre el conflicte del casino d’Andorra (1868)…

Abast: Folis manuscrits 77–82 del visor (medis 79–84), entrades 77 i 81 de l’inventari 6MD/1: projecte de casa de joc, conflicte amb el Consell i intervenció francesa.

- Fitxa: [Expedient diplomàtic francès sobre el conflicte del casino d’Andorra (1868) — 6MD/1, entrades 77 i 81; imatges 79–84](fonts/archives-diplomatiques-casino-1868.md)
- Material de partida: 1 fitxers a `raw/web/institucions/archives-diplomatiques/casino-1868/`
- Originals conservats només en local (sense dret de redistribució): 7 fitxers

### 25. 📝 incorpora Expedient diplomàtic francès de la Reforma d’Andorra (1866) — 6MD/1, foli 4…

Abast: Imatges primàries dels medis 50–52 del visor, corresponents a l’expedient descrit com a foli 48 de 6MD/1: projecte de declaració i decret imperial d’aprovació de la Reforma.

- Fitxa: [Expedient diplomàtic francès de la Reforma d’Andorra (1866) — 6MD/1, foli 48; imatges 50–52](fonts/archives-diplomatiques-reforma-1866.md)
- Material de partida: 1 fitxers a `raw/web/institucions/archives-diplomatiques/reforma-1866/`
- Originals conservats només en local (sense dret de redistribució): 4 fitxers

### 26. 📝 incorpora Nota diplomàtica francesa sobre la Nova Constitució d’Andorra (abril de 186…

Abast: Folis manuscrits 69–70 del visor (medis 71–72), entrada 69 de l’inventari 6MD/1: nota sobre la nova constitució i la seva promulgació pel bisbe d’Urgell.

- Fitxa: [Nota diplomàtica francesa sobre la Nova Constitució d’Andorra (abril de 1867) — 6MD/1, entrada 69; imatges 71–72](fonts/archives-diplomatiques-reforma-1867.md)
- Material de partida: 1 fitxers a `raw/web/institucions/archives-diplomatiques/reforma-1867/`
- Originals conservats només en local (sense dret de redistribució): 5 fitxers

### 27. 📝 incorpora Aiguats del 1982 — Andorra Recerca i Innovació i ICGC

- Fitxa: [Aiguats del 1982 — Andorra Recerca i Innovació i ICGC](fonts/ari-aiguats-1982-2022.md)
- Article nou: [L’aiguat de 1982: meteorologia, danys i resposta](temes/historia/historia-recent/l-aiguat-de-1982-meteorologia-danys-i-resposta.md)

### 28. 📝 incorpora Carlemany i Andorra — Història de la Carta Pobla

- **Font consultada:** pàgina de projecte d’Andorra Recerca + Innovació i PDF de l’estudi d’Oliver Vergés Pons, *Carlemany i Andorra: Història de la Carta Pobla, el document que va originar una llegenda* (IEA, 2018). - **Proveniència:** còpia del PDF oficial descarregada de `iea.ad`; text extret amb `pdftotext -layout`; hashes al README de `docs/raw/academic/ari/carta-pobla-2018/`. - **Resultat:** nova font `ari-carta-pobla-2018` i nova fitxa sobre el fals diplomàtic, la hipòtesi de datació als segles XI–XII i els usos historiogràfics del document. - **Límit registrat:** la fitxa no tracta el fals com a prova de la fundació carolíngia i deixa oberta la consulta del pergamí original i la identificació del falsificador.

- Fitxa: [Carlemany i Andorra — Història de la Carta Pobla](fonts/ari-carta-pobla-2018.md)
- Article nou: [La Carta Pobla: el fals que va donar forma al mite de Carlemany](temes/historia/origens/carta-pobla-fals-carlemany.md)
- Diari de treball: `raw/worklog/2026-09-23-carta-pobla-fals-carlemany.md`

### 29. 📝 incorpora Arxiu en línia — expedient TC-6238 del Tribunal de Corts

Abast: Expedient manuscrit de disset pàgines, datat en una anotació interior el 16 de juny de 1621 i catalogat al registre com a causa de bruixeria.

- Fitxa: [Arxiu en línia — expedient TC-6238 del Tribunal de Corts](fonts/arxiu-en-linia-tc-6238.md)

### 30. 📝 incorpora Arxiu en línia — quatre expedients de bruixeria (1621)

Abast: Quatre expedients TC de 1621: TC-6237 (18 pàgines), TC-6242 (8), TC-6243 (5) i TC-6249 (7).

- Fitxa: [Arxiu en línia — quatre expedients de bruixeria (1621)](fonts/arxiu-en-linia-tc-bruixeria-1621.md)
- Material de partida: 42 fitxers a `raw/academic/arxiu-nacional/tribunal-corts/tc-6237/`, `raw/academic/arxiu-nacional/tribunal-corts/tc-6242/`, `raw/academic/arxiu-nacional/tribunal-corts/tc-6243/`, `raw/academic/arxiu-nacional/tribunal-corts/tc-6249/`
- Originals conservats només en local (sense dret de redistribució): 46 fitxers

### 31. 📝 incorpora ASC-16 — Llibre d’actes i comptes del Consell de les Valls d’Andorra, 1586–…

Abast: Unitat digital ASC-16, 280 folis, novembre de 1586–maig de 1723, signatura Ll-11

- Fitxa: [ASC-16 — Llibre d’actes i comptes del Consell de les Valls d’Andorra, 1586–1723](fonts/asc-00016-llibre-actes-1586-1723.md)
- Material de partida: 1 fitxers a `raw/web/institucions/arxiu-set-claus/llibre-actes-1586-1723/`
- Originals conservats només en local (sense dret de redistribució): 3 fitxers

### 32. 📝 incorpora El Consell paga el lloguer i el salari de l’apotecari, 1820 — ASC-00637 i A…

- **Fonts consultades:** registres oficials d’Arxius en Línia, ASC-00637 i ASC-00639. - **Proveniència:** pàgines `.pdf.info`, HTML de metadades i previsualitzacions públiques; hashes als JSON dels actius. - **Resultat:** nova font `asc-00637-00639-pagaments-apotecari-1820` i fitxa sobre salari i lloguer com a despesa sanitària institucional. - **Límit registrat:** els rebuts no permeten saber imports, obligacions ni medicines; la lectura queda al nivell de despesa documentada.

- Fitxa: [El Consell paga el lloguer i el salari de l’apotecari, 1820 — ASC-00637 i ASC-00639](fonts/asc-00637-00639-pagaments-apotecari-1820.md)
- Article nou: [El Consell paga el lloguer i el salari de l’apotecari, 1820](temes/societat/sanitat/pagaments-apotecari-consell-1820.md)
- Diari de treball: `raw/worklog/2026-09-23-pagaments-apotecari-consell-1820.md`

### 33. 📝 incorpora El Consell paga el nunci i l’advocat, 1820 — ASC-00638, 00640 i 00641

- Fitxa: [El Consell paga el nunci i l’advocat, 1820 — ASC-00638, 00640 i 00641](fonts/asc-00638-00640-00641-pagaments-oficis-1820.md)
- Article nou: [El Consell paga el nunci i l’advocat, 1820](temes/institucions/consell-general/salaris-nunci-advocat-1820.md)

### 34. 📝 incorpora ASC-00685 — Rebut del cirurgià Alonso Argullós pel lloguer de casa i hort,…

La fitxa pública de l’**ASC-00685** descriu un rebut del cirurgià Alonso Argullós pel pagament del lloguer de casa seva i de l’hort, datat el 31 de març de 1828.

- Fitxa: [ASC-00685 — Rebut del cirurgià Alonso Argullós pel lloguer de casa i hort, 1828](fonts/asc-00685-rebut-lloguer-cirurgia-1828.md)
- Article nou: [Un cirurgià paga el lloguer de casa i hort (1828)](temes/societat/treball/rebut-lloguer-cirurgia-1828.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/rebut-lloguer-cirurgia-1828/`
- Diari de treball: `raw/worklog/2026-09-23-rebut-lloguer-cirurgia-1828.md`
- Originals conservats només en local (sense dret de redistribució): 1 fitxers

### 35. 📝 incorpora ASC-02775 — Contribució industrial i de comerç, 1849

La fitxa pública de l’**ASC-02775** descriu una carta de Josep López al síndic general, del 8 de juliol de 1849, que tramet una disposició de la Direcció General de Contribucions Directes sobre la no-exempció dels habitants d’Andorra en la contribució industrial i de comerç.

- Fitxa: [ASC-02775 — Contribució industrial i de comerç, 1849](fonts/asc-02775-contribucio-industrial-1849.md)
- Article nou: [La contribució industrial i de comerç arriba al síndic (1849)](temes/economia/banca-i-fiscalitat/contribucio-industrial-comerc-1849.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/contribucio-industrial-1849/`
- Diari de treball: `raw/worklog/2026-09-23-contribucio-industrial-1849.md`
- Originals conservats només en local (sense dret de redistribució): 5 fitxers

### 36. 📝 incorpora Acta notarial de cartes de la reina de Navarra, 1512 — ASC-2886

- **Font consultada:** registre oficial d’Arxius en Línia, ASC-2886. - **Proveniència:** pàgina `ASC_02886.pdf.info`, HTML de metadades i previsualitzacions públiques de 800 i 200 px; hashes al JSON de l’actiu. - **Resultat:** nova font `asc-02886-cartes-reina-navarra-1512` i fitxa sobre la sindicatura andorrana, el notariat extern i la comunicació reial de 1512. - **Límit registrat:** només es pot afirmar l’acta i els intervinents; el contingut de les cartes i la resposta política queden oberts.

- Fitxa: [Acta notarial de cartes de la reina de Navarra, 1512 — ASC-2886](fonts/asc-02886-cartes-reina-navarra-1512.md)
- Article nou: [Un síndic d’Andorra fa aixecar acta de cartes de la reina de Navarra, 1512](temes/historia/edat-mitjana/cartes-reina-navarra-1512.md)
- Diari de treball: `raw/worklog/2026-09-23-cartes-reina-navarra-1512.md`

### 37. 📝 incorpora El nunci Pau Serra demana una rebaixa de salari, 1840 — ASC-03466

- **Font consultada:** registre oficial d’Arxius en Línia, ASC-03466. - **Proveniència:** pàgina `ASC_03466.pdf.info`, HTML de metadades i previsualització pública; hash al JSON de l’actiu. - **Resultat:** nova font `asc-03466-suplica-salari-nunci-1840` i fitxa sobre negociació de salaris davant el Consell. - **Límit registrat:** no consten l’import, els motius ni la resolució de la petició.

- Fitxa: [El nunci Pau Serra demana una rebaixa de salari, 1840 — ASC-03466](fonts/asc-03466-suplica-salari-nunci-1840.md)
- Article nou: [El nunci Pau Serra demana una rebaixa de salari, 1840](temes/institucions/consell-general/suplica-rebaixa-salari-nunci-1840.md)
- Diari de treball: `raw/worklog/2026-09-23-suplica-rebaixa-salari-nunci-1840.md`

### 38. 📝 incorpora ASC-3494 — Queixa de Martí Garreta contra una decisió del batlle, 1528

La fitxa pública de l’**ASC-3494** descriu una queixa de Martí Garreta, de les Bons, davant el Consell General contra una decisió del batlle Guillem Ramon Colat, datada el 6 de setembre de 1528.

- Fitxa: [ASC-3494 — Queixa de Martí Garreta contra una decisió del batlle, 1528](fonts/asc-03494-queixa-batlle-garreta-1528.md)
- Article nou: [Una queixa contra el batlle arriba al Consell, 1528](temes/historia/antic-regim/queixa-batlle-garreta-1528.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/queixa-batlle-garreta-1528/`
- Diari de treball: `raw/worklog/2026-09-23-queixa-batlle-garreta-1528.md`
- Originals conservats només en local (sense dret de redistribució): 2 fitxers

### 39. 📝 incorpora ASC-03545 — Ordinacions sobre pastures i pas del bestiar andorrà, 1340

La fitxa pública de l’**ASC-3545** descriu un trasllat autoritzat per Pere Sicard, notari públic de Castellbò, d’unes ordinacions de Roger Bernat de Castellbò sobre les pastures i el pas del bestiar andorrà per l’Urgell. El catàleg les data entre el 26 de gener i l’1 d’abril de 1340.

- Fitxa: [ASC-03545 — Ordinacions sobre pastures i pas del bestiar andorrà, 1340](fonts/asc-03545-ordinacions-pastures-1340.md)
- Article nou: [Unes ordinacions protegeixen el pas dels ramats andorrans, 1340](temes/historia/edat-mitjana/ordinacions-pastures-1340.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/ordinacions-pastures-1340/`
- Diari de treball: `raw/worklog/2026-09-23-ordinacions-pastures-1340.md`
- Originals conservats només en local (sense dret de redistribució): 2 fitxers

### 40. 📝 incorpora ASC-03572 — Ordinacions de la Cort contra quadrilles i rodamons, 1580

La fitxa pública de l’**ASC-03572** descriu unes ordinacions de la Cort de les valls d’Andorra, signades pel jutge Bernat Coromines i el veguer Amany de Queralt, datades aproximadament el 1580. El catàleg resumeix prohibicions de quadrilles armades, obligacions d’armes i avisos, presència simultània dels dos batlles i límits a l’estada de rodamons.

- Fitxa: [ASC-03572 — Ordinacions de la Cort contra quadrilles i rodamons, 1580](fonts/asc-03572-ordinacions-cort-1580.md)
- Article nou: [La Cort ordena armes, batlles presents i rodamons controlats (1580)](temes/historia/antic-regim/ordinacions-cort-quadrilles-rodamons-1580.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/ordinacions-cort-1580/`
- Diari de treball: `raw/worklog/2026-09-23-ordinacions-cort-quadrilles-1580.md`
- Originals conservats només en local (sense dret de redistribució): 3 fitxers

### 41. 📝 incorpora Manaments de Foix sobre presos i immunitat a Andorra, 1595 — còpies de 1512…

- **Fonts consultades:** registres oficials d’Arxius en Línia, ASC-3583 i ASC-3584. - **Proveniència:** pàgines `ASC_03583.pdf.info` i `ASC_03584.pdf.info`, HTML de metadades i previsualitzacions públiques; hashes als JSON dels actius. - **Resultat:** nova font combinada `asc-03583-03584-immunitat-1595-1512` i fitxa sobre presos, immunitats i circulació entre Foix, Urgell, Catalunya i Andorra. - **Límit registrat:** el catàleg dona 1595 com a data de la unitat però descriu una còpia de 1512; la discrepància queda oberta fins a la lectura dels folis.

- Fitxa: [Manaments de Foix sobre presos i immunitat a Andorra, 1595 — còpies de 1512 — ASC-3583/3584](fonts/asc-03583-03584-immunitat-1595-1512.md)
- Article nou: [Foix ordena alliberar presos i manté immunitats dins Andorra, 1595](temes/historia/edat-mitjana/mandaments-immunitat-presos-1595.md)
- Diari de treball: `raw/worklog/2026-09-23-immunitat-presos-1595-1512.md`

### 42. 📝 incorpora ASC-3593, ASC-3716 i ASC-3594 — Rendes episcopals per als pobres, 1645–1647

Les fitxes ASC-3593, ASC-3716 i ASC-3594 documenten una ordre de repartiment de 1645, una carta de 1646 sobre 240 lliures i una nova ordre de 1647 sobre les rendes episcopals destinades als pobres d’Andorra i de la Seu.

- Fitxa: [ASC-3593, ASC-3716 i ASC-3594 — Rendes episcopals per als pobres, 1645–1647](fonts/asc-03593-03716-03594-rendes-pobres-1645-1647.md)
- Material de partida: 4 fitxers a `raw/web/institucions/arxiu-set-claus/rendes-episcopals-pobres-1645-1647/`
- Diari de treball: `raw/worklog/2026-09-23-rendes-episcopals-pobres-1645-1647.md`
- Originals conservats només en local (sense dret de redistribució): 9 fitxers

### 43. 📝 incorpora ASC-3615 — Cavalcadures per portar malalts a l’hospital, 1691

La fitxa pública de l’**ASC-3615** descriu una carta del 6 d’agost de 1691 que ordena als batlles i consellers d’Andorra proporcionar cavalcadures amb albardes i bastons per transportar malalts a l’hospital de la Seu d’Urgell.

- Fitxa: [ASC-3615 — Cavalcadures per portar malalts a l’hospital, 1691](fonts/asc-03615-ordre-hospital-seu-1691.md)
- Article nou: [Una ordre de 1691 organitza el transport de malalts](temes/societat/sanitat/ordre-hospital-seu-1691.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/ordre-hospital-seu-1691/`
- Diari de treball: `raw/worklog/2026-09-23-ordre-hospital-seu-1691.md`
- Originals conservats només en local (sense dret de redistribució): 2 fitxers

### 44. 📝 incorpora El governador de Lleida respon sobre els passaports andorrans, 1840 — ASC-0…

- **Font consultada:** registre oficial d’Arxius en Línia, ASC-03658. - **Proveniència:** pàgina `ASC_03658.pdf.info`, HTML de metadades i previsualització pública; hash al JSON de l’actiu. - **Resultat:** nova font `asc-03658-passaports-seu-1840` i fitxa sobre el conflicte administratiu entre la sindicatura, la Seu d’Urgell i el governador de Lleida. - **Límit registrat:** el catàleg no publica la resposta ni permet reconstruir la norma aplicada als passaports.

- Fitxa: [El governador de Lleida respon sobre els passaports andorrans, 1840 — ASC-03658](fonts/asc-03658-passaports-seu-1840.md)
- Article nou: [El governador de Lleida intervé pels passaports dels andorrans, 1840](temes/institucions/nacionalitat-i-residencia/passaports-andorrans-seu-1840.md)
- Diari de treball: `raw/worklog/2026-09-23-passaports-andorrans-seu-1840.md`

### 45. 📝 incorpora ASC-03660 — Trasllat de la concòrdia sobre el batlle d’Andorra, 1176–1379

## Objectiu

- Fitxa: [ASC-03660 — Trasllat de la concòrdia sobre el batlle d’Andorra, 1176–1379](fonts/asc-03660-concordia-batlle-1176-1379.md)
- Article nou: [Una concòrdia de 1176 arriba en un trasllat de 1379](temes/historia/edat-mitjana/concordia-batlle-1176-1379.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/concòrdia-batlle-1176-1379/`
- Diari de treball: `raw/worklog/2026-09-23-concordia-batlle-1176-1379.md`
- Diari de treball: `raw/worklog/2026-09-24-concordia-batlle-1176-1379.md`
- Originals conservats només en local (sense dret de redistribució): 2 fitxers

### 46. 📝 incorpora Trasllat de la potestat per defensar muntanyes i emprius, 1513 — ASC-3663

- **Font consultada:** registre oficial d’Arxius en Línia, ASC-3663. - **Proveniència:** pàgina `ASC_03663.pdf.info`, HTML de metadades i previsualitzacions públiques; hashes al JSON de l’actiu. - **Resultat:** nova font `asc-03663-potestat-defensa-muntanyes-1513` i fitxa sobre la transmissió documental d’un dret de defensa dels emprius. - **Límit registrat:** la cronologia separa 1332 i 1513, però encara no sabem si el foli és còpia, trasllat intermedi o resum de l’acte original.

- Fitxa: [Trasllat de la potestat per defensar muntanyes i emprius, 1513 — ASC-3663](fonts/asc-03663-potestat-defensa-muntanyes-1513.md)
- Article nou: [Un trasllat de 1513 protegeix la defensa de muntanyes i emprius](temes/historia/edat-mitjana/potestat-defensa-muntanyes-1513.md)
- Diari de treball: `raw/worklog/2026-09-23-potestat-defensa-muntanyes-1513.md`

### 47. 📝 incorpora ASC-3670 — Concòrdia sobre passatge i pasturatge a Santa Cecília, 1543

La fitxa pública de l’**ASC-3670** descriu una concòrdia del 14 de gener de 1543 entre el Capítol de Santa Maria de Castellbò i els representants andorrans Gervasi Moles i Bernat Rossell sobre el passatge i el pasturatge a Santa Cecília.

- Fitxa: [ASC-3670 — Concòrdia sobre passatge i pasturatge a Santa Cecília, 1543](fonts/asc-03670-concordia-castellbo-pasturatge-1543.md)
- Article nou: [Una concòrdia regula el pas dels ramats a Santa Cecília, 1543](temes/historia/edat-mitjana/concordia-pasturatge-castellbo-1543.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/concordia-castellbo-pastures-1543/`
- Diari de treball: `raw/worklog/2026-09-23-concordia-castellbo-pasturatge-1543.md`
- Originals conservats només en local (sense dret de redistribució): 2 fitxers

### 48. 📝 incorpora ASC-3781 — Apel·lació contra el cobrament de lleuda a Cerdanya, 1465

La fitxa pública de l’**ASC-3781** descriu l’apel·lació de Guillem Aldosa, en nom dels cònsols i prohoms d’Andorra, contra un manament que exigia provar documentalment la franquícia de lleuda a Cerdanya. El catàleg conserva també el rebuig processal del 2 de novembre de 1465.

- Fitxa: [ASC-3781 — Apel·lació contra el cobrament de lleuda a Cerdanya, 1465](fonts/asc-03781-apelacio-lleuda-cerdanya-1465.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/apelacio-lleuda-cerdanya-1465/`
- Diari de treball: `raw/worklog/2026-09-23-apelacio-lleuda-cerdanya-1465.md`
- Originals conservats només en local (sense dret de redistribució): 2 fitxers

### 49. 📝 incorpora ASC-03783 i ASC-03785 — Sentència i execució de la franquícia de lleuda d’A…

Les fitxes **ASC-03783** i **ASC-03785** documenten una seqüència: la sentència arbitral del 30 de juny de 1493 reconeix la franquesa de lleuda dels andorrans a Agramunt, i l’actuació de 1494–1503 en fa complir l’execució després d’una provisió de Ferran II.

- Fitxa: [ASC-03783 i ASC-03785 — Sentència i execució de la franquícia de lleuda d’Agramunt, 1493–1503](fonts/asc-03783-03785-lleuda-agramunt-1493-1503.md)
- Article nou: [Agramunt ha de respectar la franquesa de lleuda dels andorrans, 1493–1503](temes/historia/edat-mitjana/lleuda-agramunt-1493-1503.md)
- Material de partida: 4 fitxers a `raw/web/institucions/arxiu-set-claus/execucio-lleuda-agramunt-1494-1503/`, `raw/web/institucions/arxiu-set-claus/sentencia-lleuda-agramunt-1493/`
- Diari de treball: `raw/worklog/2026-09-25-lleuda-agramunt-1493-1503.md`
- Originals conservats només en local (sense dret de redistribució): 4 fitxers

### 50. 📝 incorpora ASC-3800 — Sentència de Felip II sobre la treta de blat i aliments, 1593

La fitxa pública de l’**ASC-3800** descriu una sentència de Felip II del 22 de novembre de 1593 en la causa entre les Valls d’Andorra i el vescomtat de Castellbò sobre la treta de blat, vi, oli i altres aliments per al manteniment de la Vall.

- Fitxa: [ASC-3800 — Sentència de Felip II sobre la treta de blat i aliments, 1593](fonts/asc-03800-sentencia-treta-blat-1593.md)
- Article nou: [Una sentència reial protegeix l’abastiment de les Valls, 1593](temes/institucions/consell-general/sentencia-treta-blat-1593.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/sentencia-treta-blat-1593/`
- Diari de treball: `raw/worklog/2026-09-23-sentencia-treta-blat-1593.md`
- Originals conservats només en local (sense dret de redistribució): 2 fitxers

### 51. 📝 incorpora ASC-03801 — Sentència sobre el pont del Grau, 1595

La fitxa pública de l’**ASC-03801** descriu una sentència del 8 de març de 1595 pel litigi entre les valls d’Andorra i els cònsols de la Seu d’Urgell sobre el pont del Grau, davant el Quer de Santa Llúcia, en el camí de la Seu a Andorra.

- Fitxa: [ASC-03801 — Sentència sobre el pont del Grau, 1595](fonts/asc-03801-sentencia-pont-grau-1595.md)
- Article nou: [El pont del Grau i el camí de la Seu a Andorra (1595)](temes/economia/transport/pont-grau-seu-andorra-1595.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/pont-grau-1595/`
- Diari de treball: `raw/worklog/2026-09-23-pont-grau-1595.md`
- Originals conservats només en local (sense dret de redistribució): 5 fitxers

### 52. 📝 incorpora Súplica del síndic per treure sal de Cardona, 1520 — ASC-3913

- **Font consultada:** registre oficial d’Arxius en Línia, ASC-3913. - **Proveniència:** pàgina `ASC_03913.pdf.info`, HTML de metadades i previsualitzacions públiques; hashes al JSON de l’actiu. - **Resultat:** nova font `asc-03913-suplica-sal-cardona-1520` i fitxa sobre abastament, contractes i interrupció bèl·lica. - **Límit registrat:** només es pot afirmar el contingut del descriptor de catàleg; el contracte, la guerra i la resolució requereixen el text complet.

- Fitxa: [Súplica del síndic per treure sal de Cardona, 1520 — ASC-3913](fonts/asc-03913-suplica-sal-cardona-1520.md)
- Article nou: [El síndic demana dos mesos per treure sal de Cardona, 1520](temes/economia/comerc/suplica-sal-cardona-1520.md)
- Diari de treball: `raw/worklog/2026-09-23-suplica-sal-cardona-1520.md`

### 53. 📝 incorpora ASC-03958 — Relació del blat portat de Cerdanya i repartit entre els veïns…

## Objectiu

- Fitxa: [ASC-03958 — Relació del blat portat de Cerdanya i repartit entre els veïns de la parròquia d’Encamp.](fonts/asc-03958-blat-encamp-1904.md)
- Article nou: [El blat de Cerdanya es reparteix entre els veïns (1904)](temes/economia/comerc/blat-cerdanya-parroquies-1904.md)
- Material de partida: 8 fitxers a `raw/web/institucions/arxiu-set-claus/blat-andorra-1904/`, `raw/web/institucions/arxiu-set-claus/blat-encamp-1904/`, `raw/web/institucions/arxiu-set-claus/blat-massana-1904/`, `raw/web/institucions/arxiu-set-claus/blat-ordino-1904/`
- Diari de treball: `raw/worklog/2026-09-23-blat-cerdanya-parroquies-1904.md`
- Originals conservats només en local (sense dret de redistribució): 12 fitxers

### 54. 📝 incorpora ASC-03961 — Relació del blat portat de Cerdanya i repartit entre els veïns…

Abast: Unitat documental ASC-03961, 14 d’octubre de 1904; 2 folis i 3 pàgines digitalitzades

- Fitxa: [ASC-03961 — Relació del blat portat de Cerdanya i repartit entre els veïns de la parròquia d’Andorra (les Caldes i Andorra).](fonts/asc-03961-blat-andorra-1904.md)

### 55. 📝 incorpora ASC-03962 — Relació del blat portat de Cerdanya i repartit entre els veïns…

Abast: Unitat documental ASC-03962, 14 d’octubre de 1904; 2 folis i 3 pàgines digitalitzades

- Fitxa: [ASC-03962 — Relació del blat portat de Cerdanya i repartit entre els veïns de la parròquia de la Massana.](fonts/asc-03962-blat-massana-1904.md)

### 56. 📝 incorpora ASC-03963 — Memorial del blat portat de Cerdanya i repartit entre els veïns…

Abast: Unitat documental ASC-03963, 14 d’octubre de 1904; 2 folis i 3 pàgines digitalitzades

- Fitxa: [ASC-03963 — Memorial del blat portat de Cerdanya i repartit entre els veïns de la parròquia d’Ordino.](fonts/asc-03963-blat-ordino-1904.md)

### 57. 📝 incorpora ASC-4505 i ASC-4506 — Joan Francesc Sucarà i el Col·legi de Foix, 1672

Les fitxes de l’**ASC-4505** i l’**ASC-4506** documenten un nomenament de Lluís XIV per a Joan Francesc Sucarà: primer per cobrir una vacant (20 de març de 1672) i després per atorgar-li una plaça com a col·legiat (8 de setembre).

- Fitxa: [ASC-4505 i ASC-4506 — Joan Francesc Sucarà i el Col·legi de Foix, 1672](fonts/asc-04505-04506-collegi-foix-sucara-1672.md)
- Article nou: [Un nomenament educatiu del copríncep francès, 1672](temes/societat/educacio/collegi-foix-sucara-1672.md)
- Material de partida: 3 fitxers a `raw/web/institucions/arxiu-set-claus/collegi-foix-sucara-1672/`
- Diari de treball: `raw/worklog/2026-09-23-collegi-foix-sucara-1672.md`
- Originals conservats només en local (sense dret de redistribució): 4 fitxers

### 58. 📝 incorpora ASC-04538 — Ordre de no admetre emigrats francesos a Andorra, 1904

La fitxa pública de l’**ASC-04538** descriu una carta del 28 de novembre de 1904 sobre l’ordre de no admetre a les valls d’Andorra emigrats francesos, eclesiàstics i seglars.

- Fitxa: [ASC-04538 — Ordre de no admetre emigrats francesos a Andorra, 1904](fonts/asc-04538-restriccio-emigrats-francesos-1904.md)
- Article nou: [Andorra restringeix l’entrada d’emigrats francesos (1904)](temes/institucions/nacionalitat-i-residencia/restriccio-emigrats-francesos-1904.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/restriccio-emigrats-francesos-1904/`
- Diari de treball: `raw/worklog/2026-09-23-restriccio-emigrats-francesos-1904.md`
- Originals conservats només en local (sense dret de redistribució): 2 fitxers

### 59. 📝 incorpora ASC-04549 — Pactes amb l’apotecari Francesc Balmes, 1737

La fitxa pública de l’**ASC-04549** descriu els pactes entre el Consell General i Francesc Balmes d’Igualada pel seu servei com a apotecari a les valls d’Andorra, datats 1737 post.

- Fitxa: [ASC-04549 — Pactes amb l’apotecari Francesc Balmes, 1737](fonts/asc-04549-conveni-apotecari-balmes-1737.md)
- Article nou: [El Consell contracta un apotecari d’Igualada (1737)](temes/societat/sanitat/conveni-apotecari-balmes-1737.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/conveni-apotecari-balmes-1737/`
- Diari de treball: `raw/worklog/2026-09-23-conveni-apotecari-balmes-1737.md`
- Originals conservats només en local (sense dret de redistribució): 3 fitxers

### 60. 📝 incorpora ASC-4695 — Sentència sobre taxes notarials i canvi de saig a batlle, 1456

La fitxa pública de l’**ASC-4695** descriu una sentència del 7 de juny de 1456 que resol un litigi sobre taxes notarials i ordena als saigs denominar-se batlles i exercir l’ofici anterior.

- Fitxa: [ASC-4695 — Sentència sobre taxes notarials i canvi de saig a batlle, 1456](fonts/asc-04695-sentencia-taxes-saigs-1456.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/sentencia-taxes-saigs-1456/`
- Diari de treball: `raw/worklog/2026-09-23-sentencia-taxes-saigs-1456.md`
- Originals conservats només en local (sense dret de redistribució): 3 fitxers

### 61. 📝 incorpora ASC-04696 — Sentència arbitral sobre el robatori de moltons, 1468

La fitxa pública de l’**ASC-04696** descriu una sentència arbitral del 18 de juny de 1468, dictada pels veguers Menaud de Lobie i Pere Paüls, en un litigi entre les universitats d’Andorra i homes de Gascunya pel robatori de moltons de Ramon Vernet, veí de Puigcerdà.

- Fitxa: [ASC-04696 — Sentència arbitral sobre el robatori de moltons, 1468](fonts/asc-04696-sentencia-ramats-gascunya-1468.md)
- Article nou: [Els veguers arbitren un robatori de moltons, 1468](temes/historia/edat-mitjana/sentencia-ramats-gascunya-1468.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/sentencia-ramats-gascunya-1468/`
- Diari de treball: `raw/worklog/2026-09-24-sentencia-ramats-gascunya-1468.md`
- Originals conservats només en local (sense dret de redistribució): 2 fitxers

### 62. 📝 incorpora ASC-05249 — Conveni del Banc Agrícol i la Caixa de Pensions, 1934

## Objectiu

- Fitxa: [ASC-05249 — Conveni del Banc Agrícol i la Caixa de Pensions, 1934](fonts/asc-05249-conveni-banc-agricol-caixa-pensions-1934.md)
- Article nou: [El Banc Agrícol signa un conveni amb la Caixa de Pensions (1934)](temes/economia/banca-i-fiscalitat/conveni-banc-agricol-caixa-pensions-1934.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/conveni-banc-agricol-caixa-pensions-1934/`
- Diari de treball: `raw/worklog/2026-09-23-conveni-banc-agricol-caixa-pensions-1934.md`
- Originals conservats només en local (sense dret de redistribució): 1 fitxers

### 63. 📝 incorpora Sis fitxes sobre el telègraf entre França, Andorra i la Seu, 1882–1897

- **Font consultada:** sis registres oficials d'Arxius en Línia, ASC-05521, ASC-05541, ASC-05549, ASC-05561, ASC-05571 i ASC-05573. - **Proveniència:** fitxes públiques, HTML de metadades i previsualitzacions; els JSON locals conserven descriptors, URL, permisos i hashes. - **Resultat:** nova fitxa de font i article que documenten la protesta de 1882, la destrucció de la línia anterior, l'aprovació francesa de 1892, la línia Seu–Andorra, l'extensió a Ordino i la Massana i les franquícies de 1897. - **Buit actualitzat:** ja no és correcte dir que el corpus no té cap peça primària sobre la instal·lació del telègraf. Encara falten les transcripcions, els expedients tècnics i la comprovació de l'entrada en servei de cada tram.

- Fitxa: [Sis fitxes sobre el telègraf entre França, Andorra i la Seu, 1882–1897](fonts/asc-05521-05573-telegraf-1882-1897.md)
- Article nou: [El telègraf torna a Andorra: França, la Mitra i la Seu (1882–1897)](temes/economia/energia-i-serveis/telegraf-franca-espanya-1882-1897.md)
- Material de partida: 7 fitxers a `raw/web/institucions/arxiu-set-claus/telegraf-franca-espanya-1881-1892/`
- Diari de treball: `raw/worklog/2026-09-23-telegraf-franca-espanya-1882-1897.md`
- Originals conservats només en local (sense dret de redistribució): 18 fitxers

### 64. 📝 incorpora ASC-05593 — Pase de Pere Dalleres para circular por Francia, 1868

La fitxa pública de l’**ASC-05593** descriu un acta del 26 de novembre de 1868 que concedeix a Pere Dalleres, veí d’Andorra la Vella, un passe de trasllat dins de França, atorgat pel batlle Anton Armengol i els síndics Nicolau Duedra i Anton Picart.

- Fitxa: [ASC-05593 — Pase de Pere Dalleres para circular por Francia, 1868](fonts/asc-05593-pas-franca-dalleres-1868.md)
- Article nou: [Pere Dalleres obté un passe per circular per França (1868)](temes/institucions/nacionalitat-i-residencia/pas-franca-dalleres-1868.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/pas-franca-dalleres-1868/`
- Diari de treball: `raw/worklog/2026-09-23-pas-franca-dalleres-1868.md`
- Originals conservats només en local (sense dret de redistribució): 3 fitxers

### 65. 📝 incorpora ASC-05604 — Registre de residència de Josep Isidre Gil Vigatà, 1893

La fitxa pública de l’**ASC-05604** descriu l’acta d’inscripció de Josep Isidre Gil Vigatà, d’Encamp, al registre de residència de Puègserguièr, datada el 12 d’octubre de 1893.

- Fitxa: [ASC-05604 — Registre de residència de Josep Isidre Gil Vigatà, 1893](fonts/asc-05604-registre-residencia-gil-1893.md)
- Article nou: [Un veí d’Encamp s’inscriu a França (1893)](temes/institucions/nacionalitat-i-residencia/registre-residencia-andorra-franca-1893.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/registre-residencia-gil-1893/`
- Diari de treball: `raw/worklog/2026-09-23-registre-residencia-gil-1893.md`
- Originals conservats només en local (sense dret de redistribució): 2 fitxers

### 66. 📝 incorpora ASC-05606 — Proposta de cens general de la població andorrana, 1896

Les fitxes públiques de l’**ASC-05606** i l’**ASC-05607** documenten una seqüència de correspondència d’Ardison: el 21 d’agost de 1896 proposa un cens general de la població per repartir les imposicions d’una carretera i el 18 de desembre en reclama els resultats.

- Fitxa: [ASC-05606 — Proposta de cens general de la població andorrana, 1896](fonts/asc-05606-proposta-cens-poblacio-1896.md)
- Article nou: [Un cens de població per pagar la carretera (1896)](temes/societat/demografia/cens-poblacio-carretera-1896.md)
- Material de partida: 4 fitxers a `raw/web/institucions/arxiu-set-claus/proposta-cens-poblacio-1896/`, `raw/web/institucions/arxiu-set-claus/seguiment-cens-poblacio-1896/`
- Diari de treball: `raw/worklog/2026-09-23-cens-poblacio-carretera-1896.md`
- Originals conservats només en local (sense dret de redistribució): 6 fitxers

### 67. 📝 incorpora ASC-05626 — Passaport andorrà de Filomena Albós Cerqueda, 1941

La fitxa pública de l’**ASC-05626** descriu el passaport andorrà número 263, expedit pel síndic general Francesc Cairat Freixes a favor de Filomena Albós Cerqueda, veïna d’Escaldes, el 21 de febrer de 1941.

- Fitxa: [ASC-05626 — Passaport andorrà de Filomena Albós Cerqueda, 1941](fonts/asc-05626-passaport-filomena-albos-1941.md)
- Article nou: [Filomena Albós rep el passaport andorrà número 263 (1941)](temes/institucions/nacionalitat-i-residencia/passaport-filomena-albos-1941.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/passaport-filomena-albos-1941/`
- Diari de treball: `raw/worklog/2026-09-23-passaport-filomena-albos-1941.md`
- Originals conservats només en local (sense dret de redistribució): 7 fitxers

### 68. 📝 incorpora ASC-05638 — Adrià Benezet demana el passaport andorrà des de Besiers, 1946

La fitxa pública de l’**ASC-05638** descriu una carta d’Adrià Benezet al síndic general, datada a Besiers el 16 de març de 1946, per demanar el passaport andorrà.

- Fitxa: [ASC-05638 — Adrià Benezet demana el passaport andorrà des de Besiers, 1946](fonts/asc-05638-demanda-passaport-benezet-1946.md)
- Article nou: [Adrià Benezet demana el passaport andorrà des de Besiers (1946)](temes/institucions/nacionalitat-i-residencia/demanda-passaport-benezet-1946.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/demanda-passaport-adrià-benezet-1946/`
- Diari de treball: `raw/worklog/2026-09-23-demanda-passaport-benezet-1946.md`
- Originals conservats només en local (sense dret de redistribució): 1 fitxers

### 69. 📝 incorpora ASC-05645 — Certificat de residència de Maria Josepa Quesada a Grenoble, 1948

La fitxa pública de l’**ASC-05645** descriu un certificat de residència expedit per la policia de Grenoble el 16 de novembre de 1948 a favor de Maria Josepa Quesada, nascuda a Bacares i resident a Grenoble des del 10 de maig de 1947.

- Fitxa: [ASC-05645 — Certificat de residència de Maria Josepa Quesada a Grenoble, 1948](fonts/asc-05645-certificat-residencia-quesada-1948.md)
- Article nou: [Maria Josepa Quesada acredita la residència a Grenoble (1948)](temes/institucions/nacionalitat-i-residencia/certificat-residencia-quesada-1948.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/certificat-residencia-quesada-1948/`
- Diari de treball: `raw/worklog/2026-09-23-certificat-residencia-quesada-1948.md`
- Originals conservats només en local (sense dret de redistribució): 1 fitxers

### 70. 📝 incorpora ASC-05660 — Autorització d’entrada i residència per a Francesc Pasto Badena…

La fitxa pública de l’**ASC-05660** descriu una súplica de Pere Font Riba, veí d’Encamp, per autoritzar l’entrada i residència de Francesc Pasto Badena, paleta nascut a Onda, durant unes obres. La data és el 27 de juny de 1950.

- Fitxa: [ASC-05660 — Autorització d’entrada i residència per a Francesc Pasto Badena, 1950](fonts/asc-05660-autoritzacio-residencia-pasto-1950.md)
- Article nou: [Un paleta d’Onda demana residència per treballar a Encamp (1950)](temes/institucions/nacionalitat-i-residencia/autoritzacio-residencia-pasto-1950.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/autoritzacio-residencia-francesc-pasto-1950/`
- Diari de treball: `raw/worklog/2026-09-23-autoritzacio-residencia-pasto-1950.md`
- Originals conservats només en local (sense dret de redistribució): 1 fitxers

### 71. 📝 incorpora ASC-05685 — Certificat de residència i nacionalitat d’Antònia Rispal Guitar…

La fitxa pública de l’**ASC-05685** descriu un certificat expedit pel cònsol major d’Andorra Escaldes a favor d’Antònia Rispal Guitart, amb nacionalitat andorrana, residència a la parròquia i passaport número 3.699.

- Fitxa: [ASC-05685 — Certificat de residència i nacionalitat d’Antònia Rispal Guitart, 1956](fonts/asc-05685-certificat-residencia-rispal-1956.md)
- Article nou: [Escaldes certifica la residència i nacionalitat d’Antònia Rispal (1956)](temes/institucions/nacionalitat-i-residencia/certificat-residencia-rispal-1956.md)
- Material de partida: 2 fitxers a `raw/web/institucions/arxiu-set-claus/certificat-residencia-rispal-1956/`
- Diari de treball: `raw/worklog/2026-09-23-certificat-residencia-rispal-1956.md`
- Originals conservats només en local (sense dret de redistribució): 1 fitxers
