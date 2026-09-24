---
type: worklog
date: 2026-09-23
unitat: revisio-document-a-document-brain-andorra
---

# Revisió de documents del brain per relació amb Andorra

## Criteri

S'ha revisat el contingut i l'ús documental dels candidats abans d'eliminar-los.
Un fitxer no es considera andorrà només perquè contingui una coincidència textual
amb «Andorra»: les coincidències accidentals de topònims o metadades no substitueixen
una relació amb el país. Es conserven els dossiers que alimenten articles del corpus
o que documenten directament Andorra, les seves rutes, persones o institucions.

## Eliminacions

S'han eliminat els blocs següents després de comprovar-ne els fitxers i cercar-ne
referències a `docs/temes/` i `docs/fonts/`:


- `docs/raw/sdd/ewa/budapest-homonym` — 12 fitxers, 32552569 bytes. EWA Budapest 1939–1940; recerca hongaresa sense Andorra.
- `docs/raw/sdd/ewa/eloise-fontargente/dreyfus-schmidt` — 5258 fitxers, 4210069970 bytes. Genealogia Belfort/Delvert/Carla; cap document forma part del corpus andorrà ni té un ús documentat en un article andorrà.
- `docs/raw/sdd/ewa/chciuk-celt/family-archive` — 3 fitxers, 3317830 bytes. Genealogia familiar de Chciuk; no documenta Andorra i no té cap enllaç al corpus.
- `docs/raw/sdd/ewa/chciuk-celt/jerzy-stempowski` — 25 fitxers, 77987289 bytes. Dossier de Jerzy Stempowski; cap document tracta Andorra i no té cap enllaç al corpus.
- `docs/raw/sdd/ewa/chciuk-celt/krzysztof-tutaj/spp` — 11 fitxers, 3754446 bytes. Catàleg i còpies del fons SPP; cap document tracta Andorra i no té cap enllaç al corpus.

## Conservació explícita

- `chciuk-celt/miranda/tadeusz-chciuk-sota-l-alies-james-hughes-a-miranda-de-ebro.md`
  es conserva: `docs/temes/historia/guerres-i-neutralitat/els-passadors.md` el cita
  com a prova del dossier Girona–Miranda i del recorregut relacionat amb Andorra.
- `chciuk-celt/girona/` i `chciuk-celt/topography/` es conserven pel mateix article:
  aporten els expedients de frontera i la comparació de la ruta Ax–Andorra–Cerdanya.
- `eloise-fontargente/francesc-viadiu-fons/` i el seu subdossier `grumbach/` es
  conserven perquè documenten les xarxes d'evasió, els passadors i els itineraris
  andorrans; els documents sense la paraula «Andorra» són peces de prova d'aquests
  casos, no recerques independents.

També s'ha retallat la nota `eloise-i-els-dos-canadencs-fontargente-1944.md`: conserva la recerca sobre Fontargente, Viadiu, Grumbach i els testimonis de la travessa; s'ha eliminat l'apèndix sobre la trajectòria esportiva de Belfort, la genealogia independent i la perfumeria Carla, que no aportava dades d'Andorra.

El detall fitxer a fitxer es conserva a `2026-09-23-revisio-brain-andorra-deletes.tsv`.
El registre suma **5.310 fitxers eliminats**: els cinc blocs EWA i el PDF de Crystal revisat a la tercera passada.

## Segona passada fora d'EWA

S'ha contrastat també el brain compilat i els blocs de fonts/raw fora de `sdd/ewa`.
En el recompte actual, els 88 fitxers de `docs/temes/` sense la cadena literal
«Andorra» són índexs o fitxes locals identificables pel tema, la ruta i les fonts
(parròquies, Consell, CASS, patrimoni i expedients de frontera); no se n'ha
eliminat cap. Les 18 fitxes de `docs/fonts/` sense la cadena literal són fonts d'esportistes, institucions,
patrimoni o persones andorranes identificades al títol o al context. Els únics
blocs raw completament sense OCR de «Andorra» són dos PDFs que el camí i la
fitxa identifiquen explícitament com a fonts andorranes: `historiografia/
brutails-coutume-andorre-1904.pdf` i `microestats/28a-diada-andorrana-2015-petits-estats.pdf`.
Aquesta passada no ha produït cap candidat segur per eliminar.

## Tercera passada: web i PDFs

S'han passat també els PDFs de `docs/raw/web/` per OCR i revisió contextual. Els
casos sense la cadena literal «Andorra» són fonts locals o expedients de frontera
identificables pel camí i la fitxa; no s'han eliminat per una coincidència textual
negativa. L'excepció segura és `llengua/david-crystal-english-worldwide.pdf`: és un
capítol general sobre l'anglès mundial, la fitxa de la ponència de manlleus admet
que no aporta cap dada andorrana i només servia per identificar la bibliografia que
Costa cita. S'han eliminat el PDF i la fitxa corresponent, s'ha mantingut la dada
bibliogràfica a l'article i s'ha eliminat l'entrada de l'índex.

La resta de candidats web revisats —fonts de llengua, història, institucions, esports, cultura, educació i economia— tenen un ús local documentat, una persona andorrana, un expedient de frontera o una font institucional del país; no hi ha cap altre fitxer segur per eliminar en aquesta passada.

## Revisió final dels dossiers EWA conservats

S'han tornat a revisar els 1.305 fitxers EWA que resten després de les
eliminacions. Els 236 de `chciuk-celt` documenten testimonis, àudios, catàlegs i
cartografia de les rutes Girona–Andorra–Cerdanya i de les xarxes d'evasió; els 14
de `claude-benet-rtva-2013` són una entrevista sobre aquestes xarxes; i els 1.055
de `eloise-fontargente` contenen les fonts de Viadiu, Fontargente i Grumbach.

Dins del subdossier Grumbach, les actes de Belfort, el full militar 494, la taula
de defuncions 1955–1964 i l'acta parisenca 1066 identifiquen André Dreyfus i
connecten el seu germà Pierre amb la travessa de 1942. Els lots de 1925, 1951,
1961, 1966 i 1975 són controls negatius necessaris per descartar lectures de la
menció marginal i no recerques independents; es conserven perquè formen part de
la cadena probatòria. No queda cap branca EWA revisada que sigui aliena a
Andorra sense una relació documental amb una ruta, una persona o una font del
corpus.

## Títols de les fitxes README

Perquè el contingut es pugui identificar des del navegador de fitxers, s'han
precisat tres encapçalaments que eren massa genèrics: el decret imperial de 1806,
la còpia del decret presentada com a peça del mes (2016) i la fitxa toponímica de
Segudet.

## Decisió d'abast

Amb aquesta revisió no cal afegir bibliografia general: el corpus ja cobreix les
fonts institucionals, la història de frontera i els dossiers de les rutes
d'evasió. Els buits que resten són preguntes documentals concretes, no absència
de material de context: recuperar les pàgines 320–341 de *Raport z Podziemia
1942*, consultar el recte i el revers de l'expedient de Miranda per confirmar
James Hughes, i obtenir el sumari Cabrero o les memòries completes de Pierre
Dreyfus-Schmidt. Es deixen com a següents passos de recerca; afegir ara fonts
generals duplicaria el corpus sense tancar cap d'aquests buits.
