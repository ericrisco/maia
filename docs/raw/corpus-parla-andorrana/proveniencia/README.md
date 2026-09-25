# Proveniència del corpus independent

Les carpetes de cada `pa-*` contenen el JSON de metadades de la font, l'URL
externa, els termes de la plataforma, els registres de descàrrega i els hashes
dels àudios. La font no es considera reutilitzable només perquè es pugui veure:

- les 12 càpsules d'Andorra Recerca i Innovació declaren **Creative Commons
  Attribution (reuse allowed)**;
- els vídeos del Consell General i RTVA consultats indiquen llicència estàndard
  de YouTube o no declaren una llicència oberta.

Els fitxers d'àudio sense llicència oberta es conserven només com a derivats
locals de recerca. No es publiquen ni es redistribueixen. Cada informe separa
els fets documentats, la sortida de l'ASR i les hipòtesis fonètiques pendents de
verificació auditiva.

Els estats `analitzada-provisional-contextual` i `analitzada-provisional-automatica` descriuen la preparació documental i l'ASR; cap dels dos vol dir que el clip s'hagi validat escoltant-lo. La validació humana continua al `registre-audicio.tsv`.
`qa-exclusions.tsv` registra pa-044, pa-047 i pa-050, que conserven àudio i transcripcions però queden fora del graf per degeneracions ASR fins a la revisió auditiva i la confirmació dels segments atribuïbles.


`fonts-resum.tsv` és el registre regenerat de les 66 fonts; `analisi-metrics.tsv`
resumeix les mètriques temporals i de confiança calculades a partir dels JSON;
`analisi-audio-metrics.tsv` afegeix pauses i volum mesurats directament sobre els
WAV amb `ffmpeg`.
`analisi-prosodia.tsv` afegeix, per cada WAV, activitat de veu, energia, creuaments per
zero i una estimació espectral orientativa de F0; aquestes mesures serveixen per
prioritzar l'escolta i no substitueixen l'anotació fonètica.
`analisi-formants-consens.tsv` afegeix 250 files amb mesures instrumentals de F0, F1, F2 i F3
per als tokens consensuals amb timestamp (161 valors F0 i 249 valors per a cadascun de F1, F2 i F3); el resum per forma és a
`resum-formants-consens.tsv`. Són una capa exploratòria i requereixen confirmació
auditiva abans d'interpretar qualsevol diferència fonètica.
La regeneració usa `praat-parselmouth` per llegir els formants de Praat; les files i
els paràmetres queden documentats al script `analitza-formants-consens.py`.
`analisi-trajectories-formants.tsv` repeteix la mesura en cinc punts temporals per
cadascun dels 250 tokens (1.250 files) i conserva també la intensitat.
`evidencia-gramatica.tsv` conserva contextos ASR localitzables de nou categories; els
pronoms en/hi/ho es marquen com a candidats perquè també poden ser preposicions o
formes mal reconegudes.
`qa-clips-forts-greedy.tsv` conserva una tercera decodificació dels 109 clips forts;
`qa-clips-forts-consens.tsv` compara small, base i greedy sense convertir el consens
automàtic en una decisió d'audició.
`auditoria-forts-triple.html` ofereix un reproductor local amb filtre per persona i
categoria, i mostra al costat els tres textos per facilitar l'anotació auditiva.
`registre-audicio-forts-divergencies.tsv` i `quadern-audicio-forts-divergencies.md`
concentren les 28 divergències en una cua d'anotació que conserva buits humans.
`analisi-acustica-divergencies.tsv` conserva mesures instrumentals dels mateixos
clips; s'usen per orientar la revisió i no substitueixen l'escolta.
`analisi-formants-qa.tsv` amplia aquesta capa a 309 tokens amb timestamp en la cua
QA; no implica consens entre models.
`qa-cua-small-json.tsv` conserva el JSON de cadascun dels 656 clips; la tokenització
small recupera 451 ocurrències en 439 clips i les mesures queden a
`analisi-formants-cua-small.tsv`.
El graf corresponent queda separat a `../grafo/trets-small-token.tsv`,
`../grafo/arestes-parlants-small-token.tsv` i `../grafo/matriu-formes-small-token.tsv`.
`prioritat-formes-small-token.tsv` i `quadern-formes-small-token.md` ordenen les
formes per iniciar l'audició en els patrons més estesos.
`cua-audicio.tsv` combina el primer interval temporal de cada forma i parlant amb
el consens entre ASR i les mètriques acústiques; totes les files comencen amb
`estat_audicio=pendent` i requereixen escolta humana.
`clips-audicio.tsv` enumera 656 clips mono de 16 kHz per cobrir tota la cua: 384
corresponen a intervals on les dues passades coincideixen temporalment i 272 s'han
extret directament del WAV quan no hi havia solapament; cada clip conserva el seu
SHA-256.
`clusters-prosodia.tsv` i `resum-clusters-prosodia.md` agrupen exploratòriament les
63 veus actives per mètriques acústiques i ritme; no són etiquetes dialectals.
`candidats.tsv` conserva la taula històrica de prospecció que va donar lloc a la
selecció actual.
`cobertura.tsv`, regenerat per `verifica-cobertura.py`, comprova que les 66
persones tenen el paquet mínim abans de qualsevol revisió lingüística.

`verifica-corpus.py` és el verificador reproducible del paquet complet. Comprova
la cobertura de persones, informes i fitxers multimèdia, la correspondència entre
la cua i els clips, els SHA-256 i els recomptes dels registres, la matriu de
formes i les capes QA del graf. En l'estat actual retorna `OK` amb 66 registres i 60 persones canòniques,
656 intervals/clips, 2.310 cel·les i hashes vàlids.

`auditoria-aillament-brain.md` comprova, fora d'aquest directori, que no hi ha
enllaços semàntics cap al subcorpus; el recompte esperat és zero.

`persones-canonics.tsv` és el mapa regenerable que agrupa les sis persones amb dos registres de font; no elimina cap àudio ni transcripció.

`fonts-pendents.tsv` recull quatre testimonis encara pendents del fons de l'Arxiu d'Etnografia
d'Andorra que poden ampliar el corpus amb veus rurals i històriques. El catàleg
oficial descriu 57 enregistraments en català d'accés lliure, però restringeix la
reproducció i exigeix autorització del propietari; per això aquestes veus no es
compten encara entre les 66 mostres. Fitxa del fons:
<https://www.govern.ad/ca/l/4673848>.
La justificació documental i els termes consultats es conserven a
`autoritzacions.md`.

El mateix registre conserva també sis candidats `preanalisi-candidat` (quatre
RTVA i dos del Consell General) amb àudio i ASR provisionals però sense atribució de
veu o termes prou resolts per entrar al recompte canònic. Les quatre files
`incorporat-pa-051`—`incorporat-pa-054` són històriques del registre i ja formen
part de les 66 mostres.

La prospecció oficial més recent hi conserva una referència `pendent-recollida`
del Consell General (Roser Suñé); Pere López Agràs ja té un extracte local de
120 segons, doble ASR, dos clips i perfil acústic, però encara no entra al corpus
fins a confirmar veu i termes d’ús.

`context-persones.tsv` registra les fonts institucionals i etnogràfiques consultades per documentar el context dels 60 parlants canònics. En el cas de Carles Sasplugas, la coincidència entre el nom abreujat del vídeo i el nom complet del registre municipal queda explícitament marcada com a compatible però no verificada. Aquesta evidència territorial no prova la llengua inicial.

Per als dos registres que abans només tenien títol o metadades s'han afegit
referències contextuals públiques: el catàleg de la Biblioteca Nacional i una
notícia sobre Roser Jordana, i el registre municipal d'associacions d'Andorra
la Vella per a Carles Sasplugas. Només se'n conserven els enllaços i la lectura
documental; no s'hi incorpora ni redistribueix cap còpia dels documents externs.

analisi-acustica-densa.tsv afegeix quantils d'energia, F0, centroid espectral i intervals de veu per prioritzar fragments; no és una anotació fonètica.

analisi-linguistica.tsv resumeix patrons discursius, morfosintaxi candidata, repetició i lèxic territorial observables en l'ASR; no són variants confirmades.

pla-audicio.tsv i pla-audicio.md ordenen els 656 intervals per començar la revisió auditiva amb les coincidències ASR més fortes.

La `sessions/sessio-05.tsv` i el seu quadern `sessions/sessio-05.md` afegeixen
20 clips canònics d'alta prioritat fora de les sessions 01–02. Inclouen els dos
textos ASR i les mètriques instrumentals disponibles, però mantenen buits els
camps que només es poden completar escoltant.

La `sessions/sessio-06.tsv` afegeix 19 clips, un per cadascun dels parlants
canònics actius que encara no apareixien a les cues anteriors; les tres veus en
quarantena es mantenen en la seva cua específica.

`verifica-sessions-audicio.py` comprova els sis manifests de sessió, els 140
clips, l'existència de l'àudio local, els identificadors i l'absència de
solapament entre les sessions canòniques.

qa-beam.tsv registra una tercera passada amb cerca de feixos sobre un clip prioritari per cadascuna de les 63 veus actives; 63 clips s'han processat amb èxit.

`qa-clips.tsv` registra una quarta passada ASR independent sobre els 656 clips
de la cua completa. La columna `forma_en_qa` només indica coincidència textual
del model en el fragment curt; no confirma que la forma s'hagi pronunciat com
la grafia ni substitueix l'escolta.

`qa-clips-base.tsv` conserva una passada independent addicional amb
`ggml-base.bin` sobre els mateixos 656 clips. `qa-clips-consens.tsv` combina les
dues passades i marca **263** clips amb coincidència textual en tots dos models;
els textos de cada model es mantenen separats per fer visibles les divergències.
`resum-consens-per-persona.tsv` resumeix el recompte per veu, i
`actualitza-informes-consens.py` manté aquesta secció sincronitzada dins dels
66 informes individuals.

`analisi-acustica-consens.tsv` conserva els descriptors de veu, F0, pauses i
espectre dels 263 clips amb consens textual; `resum-acustica-formes-consens.tsv`
en calcula medianes per forma. `analitza-acustica-consens.py` també incorpora
un resum cautelós a cada informe individual: són mesures de selecció i no
etiquetes fonètiques.

`quadern-audicio-consens.md` ordena els 263 clips consensuals per persona i
forma, amb enllaç directe a l'àudio, els dos textos ASR i els camps per a la
decisió auditiva, la variant, la fonètica i la prosòdia.

`qa-consens-base-json/` conserva el JSON complet de la passada base per als 263
clips. `qa-consens-tokens-base.tsv` localitza la forma amb temps absolut i
probabilitat en **249** clips (250 coincidències tokenitzades); els 14 sense
coincidència tokenitzada es mantenen com a divergència interna que requereix
escolta. La mediana de probabilitat mínima és 0,5622 i 120 coincidències queden
per sota de 0,55.

`prioritat-consens-token.tsv` ordena aquesta cua en 14 casos
`A-token-missing`, 120 `B-token-low` i 129 `C-token-strong`, amb els temps
absoluts disponibles quan hi ha token.

`informe-token-missing.md` documenta els 14 casos sense token amb els dos textos
ASR, l'enllaç al JSON complet i els descriptors acústics perquè es puguin
revisar primer.
`qa-token-missing-comparativa.tsv` afegeix una tokenització independent small:
7 casos es recuperen amb aquest model i 7 continuen sense token en cap dels dos.

`referencies-institucionals-casos-persistents.md` reuneix fonts oficials per
identificar territorialment els set casos que continuen sense token en cap model;
les referències no s'interpreten com a prova de llengua inicial.

`qa-quarantena-base.tsv`, `qa-quarantena-comparativa.tsv` i
`informe-quarantena-comparativa.md` afegeixen la passada `base` a les nou
finestres de pa-044, pa-047 i pa-050. Les tres veus continuen en quarantena fins
a l'escolta.
`qa-quarantena-20s.tsv` i `informe-quarantena-20s.md` afegeixen 237 finestres no solapades de 20 segons amb `ggml-base.bin` i una transcripció combinada per veu; aquesta capa redueix bucles de context però continua sent ASR auxiliar i pendent d'audició.
`cua-audicio-quarantena-20s.tsv` i `auditoria-quarantena-20s.html` seleccionen cinc finestres de màxima qualitat per cadascuna de les tres veus, amb camps humans buits per anotar veu, decisió, variant, fonètica i prosòdia.
`qa-quarantena-20s-formes.tsv` compta les 35 formes candidates sobre aquestes transcripcions curtes i les manté explícitament com a candidats ASR pendents d’audició.
`qa-quarantena-20s-consens.tsv` conserva una segona descodificació small dels 15 clips i el solapament lèxic; la coincidència textual exacta no es fa servir com a decisió humana.
`analisi-acustica-quarantena-20s.tsv` calcula veu activa, energia, F0, espectre i pauses sobre els mateixos 15 WAV; són descriptors instrumentals orientatius i també queden resumits als tres informes.

`analisi-acustica-normalitzada-consens.tsv` compara els 263 clips consensuals
amb la mediana acústica de la veu completa de cada persona; el resum per forma
és `resum-acustica-normalitzada-formes.tsv`. Els deltes redueixen l'efecte de
parlant i microfonia, però continuen sent descriptors exploratoris.

`repertori-evidencia.tsv` desplega les 18 dimensions del repertori sobre les 66
persones i separa 61 files amb marcadors textuals consensuals, 62 amb descriptors
prosòdics normalitzats i 1.065 que encara no tenen evidència específica.

`qa-clips-boundary.tsv` recalcula totes les coincidències amb límits de paraula
alfanumèrics: conserva **249** consensos estrictes i identifica 14 falsos
positius de la cerca per subcadena. `resum-boundary-per-persona.tsv` i la secció
homònima dels 66 informes en deixen constància; el graf corresponent és una capa
separada i continua pendent d'escolta.

`prioritat-audicio.tsv` combina el consens de les dues passades llargues, el
solapament temporal i la quarta passada per ordenar la revisió: 303 intervals
queden en categoria A (triple consens), 63 en B (doble ASR), 86 en C (una
passada) i 204 en D (divergent).

`analisi-acustica-clips.tsv` afegeix els descriptors de senyal dels 656 clips
(proporció de veu, energia, ZCR, F0 orientativa, centroid espectral i pauses)
perquè la revisió de prosòdia parteixi del mateix fragment que es transcriu.
Són mesures de priorització i no etiquetes fonètiques.

`cua-audicio-small-equilibrada.tsv` i `quadern-audicio-small-equilibrada.md` formen una cua curta de 100 clips, equilibrada per cobrir els 63 parlants tokenitzats i les 20 formes small. Inclou mesures formàntiques instrumentals quan existeixen, però deixa buits els camps humans perquè la decisió només es faci escoltant.

`actualitza-informes-cua-equilibrada.py` copia aquesta cua a les 66 fitxes individuals, amb l'enllaç al clip i l'estat de revisió pendent, perquè cada informe mantingui visible el següent pas.

`genera-auditoria-small-equilibrada.py` regenera `auditoria-small-equilibrada.html`, un reproductor filtrable que exporta les anotacions locals de la mostra abans d'incorporar-les al TSV.

`importa-auditoria-small-equilibrada.py` valida aquest TSV i, amb `--write`, incorpora les decisions a la cua equilibrada; la cua mestra de 656 files es manté separada.

`qa-equilibrada-base.tsv` conserva una segona descodificació base dels 100 clips; `qa-equilibrada-consens.tsv` en resumeix **70** amb coincidència textual small/base i **30** divergents. Les divergències continuen sent candidats d'audició, no errors resolts.

`informe-qa-equilibrada.md` enumera les 30 divergències amb els dos textos i els enllaços d'àudio; cap text automàtic es tracta com a transcripció definitiva.

La coincidència base localitza 70 tokens amb timestamp a `qa-equilibrada-base-token-occurrences.tsv`; `analisi-formants-base-equilibrada.tsv` en mesura 70 (F0 disponible en 46 i F1–F3 en 69) com a suport instrumental independent.

`prioritat-audicio-equilibrada.tsv` i `quadern-audicio-equilibrada-prioritzat.md` ordenen els 100 clips en 52 casos A (doble ASR i confiança alta), 18 B (doble ASR amb confiança baixa) i 30 C (divergents).

`analisi-trajectories-base-equilibrada.tsv` conserva 350 punts (cinc per cadascun dels 70 tokens base coincidents) i `resum-trajectories-base-equilibrada.tsv` en dona medianes per a 19 formes.

`qa-equilibrada-triple.tsv` compara una tercera passada greedy: 61 clips coincideixen en els tres models, 34 en dos i 5 en un. `informe-qa-equilibrada-triple.md` enumera els casos que mereixen escolta prioritària.

La tercera passada s'ha estès als **656 clips**: `qa-clips-triple-full.tsv` en classifica 206 com a triples, 201 dobles, 113 d'un sol model i 136 sense coincidència textual. `informe-qa-triple-complet.md` conserva els textos paral·lels.

`prioritat-audicio-triple.tsv` reordena la cua completa en 80 casos A (triple i token fort), 126 B (triple amb token baix), 201 C (dos models), 113 D (un model) i 136 E (cap model).

`inventari-incerteses-asr.tsv` conserva 13.390 segments amb algun token de probabilitat inferior a 0,55; 1.283 se solapen amb clips de la cua. És una cua de correcció de transcripció i no una llista de variants dialectals.

`cua-audicio-incerteses.tsv` selecciona 100 clips d'aquesta inventariació, cobreix 63 persones i prioritza la probabilitat més baixa; `auditoria-incerteses.html` permet escoltar-los i exportar les anotacions.

`qa-beam.tsv` conserva una quarta descodificació amb feixos per a 63 persones actives; és contrast automàtic addicional i continua pendent d'audició.

El candidat extern `candidats/lead-rtva-001` conserva l'àudio, ASR i informe de Joan Verdú com a expedient separat; no entra encara al recompte canònic perquè cal separar entrevistador i entrevistat.
La seva separació acústica provisional (`segments-clusters.tsv`) només orienta l'obertura dels fragments i no assigna identitats.
El candidat també té una passada base independent (`candidats/lead-rtva-001/asr/joan-verdu-base.*`) i un contrast de formes, sempre pendent d'audició.
La segmentació textual provisional de Joan (`segments-speaker-provisional.tsv`) només ordena els torns que cal escoltar.
L'anotador `candidats/lead-rtva-001/auditoria.html` manté la revisió del candidat separada del registre mestre.
La comprovació estèreo del candidat dona correlació L/R 0,993388; els canals són una mescla i no resolen la diarització.
Els 10 clips del candidat tenen també mesures exploratòries de F0/F1/F2/F3 a `candidats/lead-rtva-001/formants.tsv`; no són trets dialectals.

`../grafo/*-triple-full.*` és la vista canònica estricta dels 206 clips amb triple coincidència: 19 formes, 106 arestes entre parlants amb almenys tres formes compartides i 1.140 cel·les persona-forma; continua sent evidència textual pendent d'audició.

`actualitza-informes-prioritat-equilibrada.py` copia aquest ordre a les fitxes individuals perquè cada persona tingui visible el seu següent clip.

`importa-auditoria-equilibrada-master.py` comprova la clau exacta `(persona, forma, clip)` i pot projectar una anotació de la mostra al `registre-audicio.tsv`; per defecte només simula i rebutja conflictes.

`protocol-audicio-anotacio.md` fixa les decisions, els camps i els criteris per observar fonètica, prosòdia, morfosintaxi, lèxic i contacte sense convertir l'ASR en veredicte.

`resum-estat-audicio.tsv` i `resum-estat-audicio.md` es regeneren amb `resumeix-estat-audicio.py`: ara sumen els 656 intervals generals i els 30 clips de formes escasses, desglossats per les 60 persones canòniques i separats per cua.

`registre-audicio.tsv` és el full únic de treball: conserva les evidències
automàtiques ordenades i deixa buits els camps `forma_confirmada_auditivament`,
`variant_transcrita`, `trets_fonetics_observats`, `observacions_prosodiques` i
`nota_audicio`, que només es poden completar escoltant el clip.

`evidencia-formes.tsv` conserva 2.014 fragments de context extrets de les 66
transcripcions per localitzar cada forma candidata al WAV. El context és ASR i
queda marcat com a pendent d'audició.

`qa-clips-json.tsv` conserva timestamps JSON per als 303 clips de categoria A;
permet obrir el segment exacte de la quarta passada abans d'escoltar-lo.

`qa-formes-tokens.tsv` avalua els 313 clips A: localitza 309 coincidències de
tokens i deixa quatre clips sense coincidència tokenitzada, amb probabilitat
mínima i mitjana i temps absolut; els valors baixos continuen sent candidats
per revisar, no descartes automàtics.

`candidats-forts.tsv` filtra 109 clips A amb totes les coincidències tokenitzades
a probabilitat mínima igual o superior a 0,80. És una cua de primera escolta,
no una confirmació lingüística.

`quadern-audicio-forts.md` presenta aquests 109 clips agrupats per 52 persones,
amb enllaços al WAV i al text QA i amb els camps humans per completar la variant,
la fonètica i la prosòdia.

`auditoria-forts.html` ofereix el mateix bloc amb reproductor, filtres per
persona i estat, camps d'anotació i exportació TSV local; les notes es guarden
només al navegador fins que es descarreguen.

`genera-auditoria-cua.py` regenera `auditoria-cua.html` per als 656 clips de la
cua completa, amb filtres per persona, categoria i estat. El TSV descarregat es
pot revisar i incorporar al registre amb `importa-auditoria.py`; per defecte
l'importador només simula i exigeix `--write` per modificar el fitxer mestre.

`evidencia-formes-vtt.tsv` alinea 3.326 ocurrències candidates amb els segments
temporals VTT de les 66 transcripcions (fins a vuit exemples per forma i veu).

`referencies-linguistiques.md` i `../grafo/repertori-referencia.tsv` documenten
el repertori acadèmic que guia l'escolta (vocalisme, fonosintaxi, morfologia,
lèxic, prosòdia i variació social); són una guia, no etiquetes aplicades.

`qa-quarantena.tsv` conserva nou finestres independents de 30 segons (tres per
cadascuna de les veus en quarantena), amb hash SHA-256, una tercera transcripció
ASR i una mesura de repetició per finestra. És evidència de recuperabilitat parcial, no
un veredicte: pa-044 i pa-050 tenen finestres sense bucles, mentre pa-047 encara
en conserva una amb repetició; les tres continuen pendents d'escolta humana.

`genera-auditoria-sessions-canoniques.py` regenera
`auditoria-sessions-canoniques.html`, un reproductor filtrable per als 89
clips canònics de les sessions 01, 02, 05 i 06. Les mesures automàtiques es mostren al costat
de cada clip, però només les anotacions escoltades es poden projectar després
al registre mestre.

`auditoria-cobertura-persones.tsv` és la comprovació regenerable de les 66 fitxes canòniques: verifica títol, inventari de formes, perfil lingüístic, àudio, transcripció i procedència, i separa les tres veus en quarantena.

`genera-auditoria-cobertura-sessions.py` regenera `auditoria-cobertura-sessions.tsv`, una fila per a cadascuna de les 60 persones canòniques: 57 queden cobertes per almenys un clip de les sessions 01, 02, 05 o 06 i pa-044, pa-047 i pa-050 queden identificades com a quarantena.

`genera-auditoria-integritat-audio.py` regenera `auditoria-integritat-audio.tsv` i comprova els encapçalaments dels 66 WAV font i dels 656 clips escoltables: durada positiva, freqüència de mostreig i canals vàlids. La passada actual dona 722/722 fitxers `ok`; això prova recuperabilitat tècnica, no substitueix l'audició lingüística.

`genera-auditoria-proveniencia.py` regenera `auditoria-proveniencia.tsv` i comprova els camps mínims de les 66 fitxes: font, canal, URL, llicència o termes d'ús, consulta, derivat local amb hash i ordre ASR. La passada actual les troba completes; això documenta la traça de la font, no converteix una llicència estàndard en llicència oberta.

`genera-auditoria-integritat-transcripcions.py` regenera `auditoria-integritat-transcripcions.tsv`: 64 transcripcions passen la comprovació estructural; pa-028 conserva un petit desfasament final de timestamp i pa-047 conserva timestamps fora de durada associats a la incidència de repetició ASR. Totes dues queden explícites com a QA pendent.

`genera-remediacio-transcripcions.py` crea VTT de QA limitats a la durada real per a pa-028 i pa-047 a `pa-028/qa-corrected/` i `pa-047/qa-corrected/`; manté intactes els originals i deixa la repetició de pa-047 com a incidència pendent d'audició.

`genera-index-audicio.py` regenera `INDEX-AUDICIO.md`, la porta d'entrada única a les cues per persona, formes escasses, quarantena i cua completa, amb els registres i importadors corresponents.

El candidat Pere López té un expedient separat a `candidats/lead-cg-002-pere-lopez/` amb extracte WAV, doble ASR, 35 formes i 2 clips; el seu estat continua pendent de veu i termes, i no entra al graf canònic.

`genera-auditoria-independencia.py` regenera `auditoria-independencia.tsv` i comprova 226 documents del subcorpus: no hi ha enllaços relatius fora de `corpus-parla-andorrana` ni fitxers destinació inexistents. Les mencions descriptives a “brain” es conserven com a context de separació i no compten com a dependència.

`genera-auditoria-grafo-independent.py` regenera `auditoria-grafo-independent.tsv` i comprova les sis capes canòniques del graf: nodes, arestes i matriu lingüístiques, nodes i arestes acústiques i repertori aplicat. Totes les capes només contenen IDs del mapa de 60 persones canòniques.

`genera-resum-qa-quarantena-20s-alt.py` resumeix una passada independent amb `ggml-base.bin` sobre les 237 finestres curtes: 193 tenen text localitzable, 42 mostren bucle ASR i 2 són silenci. És una priorització tècnica per a l’audició, no una promoció de cap veu al graf.

`genera-auditoria-cua-quarantena.py` contrasta la cua humana de 15 clips amb aquesta passada alternativa: els 15 clips seleccionats són localitzables i continuen amb la decisió humana en blanc.

`genera-auditoria-cobertura-formes.py` resumeix les 35 formes candidates: 10 tenen cobertura escassa (<10 parlants canònics) i queden prioritzades per a l’audició; la classificació és una cua de revisió, no una etiqueta dialectal.

`genera-cua-formes-escasses.py` extreu 3 clips locals per cadascuna d’aquestes 10 formes (30 clips, 18 parlants) a `cua-audicio-formes-escasses.tsv`; tots tenen hash i decisió humana pendent.

`genera-registre-audicio-formes-escasses.py` materialitza aquestes 30 claus en un registre d’audició propi (`registre-audicio-formes-escasses.tsv`), separat del registre general de 656 intervals perquè cobreix formes addicionals; conserva les anotacions humanes quan es regenera.

`genera-guia-formes-escasses.py` regenera `guia-audicio-formes-escasses.tsv`: fixa per a cadascuna de les 10 formes què cal escoltar i quins camps humans s’han d’omplir, sense convertir cap pauta automàtica en tret dialectal.

`analitza-acustica-formes-escasses.py` regenera `analisi-acustica-formes-escasses.tsv` amb veu activa, energia, F0 orientativa, espectre i pauses dels 30 WAV; són descriptors instrumentals per ordenar l’escolta, no anotacions fonètiques.

`genera-auditoria-formes-escasses.py` regenera `auditoria-formes-escasses.html`, un reproductor local amb filtres, text ASR i camps per decisió, variant, trets fonètics, prosòdia i observacions. Les anotacions s’exporten a un TSV local i no entren al registre canònic fins que es revisen.

`importa-auditoria-formes-escasses.py` valida aquesta exportació contra la clau exacta `(persona, forma, clip)` i, per defecte, només simula; `--write` és necessari per projectar les anotacions al `registre-audicio-formes-escasses.tsv`.

`importa-auditoria-sessions-canoniques.py` valida l'exportació de les sessions amb coincidència exacta i nota justificativa; per defecte simula i només modifica el registre mestre amb `--write`.
Les simulacions amb `sessions/sessio-05.tsv` i `sessions/sessio-06.tsv`
validen les 39 claus noves sense escriure cap decisió mentre continuen
pendents d'audició.

`guia-audicio-sessions-canoniques.tsv` acompanya els 89 clips prioritzats amb una guia de què cal escoltar per forma i amb les mesures automàtiques disponibles.

`actualitza-informes-sessions-canoniques.py` manté visibles dins de les 61 fitxes implicades els 89 clips de les sessions 01–02, 05 i 06, els dos textos ASR i els enllaços als WAV.

`resum-cobertura-fonts.tsv` agrupa els 66 registres per canal, compta URLs de YouTube i separa les llicències Creative Commons dels derivats locals sense llicència oberta declarada.

`actualitza-informes-repertori.py` copia el mapa de 18 dimensions de `repertori-evidencia.tsv` a les 66 fitxes i conserva explícits els buits que només es poden resoldre escoltant.

`genera-quadern-sessions-canoniques.py` regenera `quadern-sessions-canoniques.md`, la versió Markdown dels 89 clips de les sessions 01–02, 05 i 06.

`genera-auditoria-objectiu.py` regenera `auditoria-objectiu.tsv`, la matriu de requisits, evidència i buits del corpus.

`genera-auditoria-informes.py` regenera `auditoria-informes.tsv`, que comprova les seccions mínimes, els enllaços de transcripció, les mètriques i una ruta d'audició (sessions canòniques o quarantena) de les 66 fitxes individuals.
Les mostres duplicades pa-023 i pa-057 indiquen explícitament la mostra de sessió de la seva persona canònica (pa-060 i pa-029) sense perdre la seva transcripció pròpia.

`genera-auditoria-identitat-linguistica.py` regenera `auditoria-identitat-linguistica.tsv`, que separa font andorrana, context territorial i confirmació de llengua inicial; les files basades només en títol o metadades no compten com a context documentat.
