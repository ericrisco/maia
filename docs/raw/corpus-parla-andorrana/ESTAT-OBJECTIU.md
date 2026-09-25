# Estat verificable de l'objectiu

Aquest document audita l'estat actual del corpus independent i conserva les
condicions que falten abans de considerar-lo acabat.

| Requisit | Evidència actual | Estat |
|---|---|---|
| Subcorpus separat de la resta del brain | `README.md` declara `linked_to_existing_corpus: false`; no hi ha enllaços semàntics fora del directori | assolit |
| Entre 50 i 100 persones | `persones-canonics.tsv`: 60 persones canòniques en 66 registres de font | assolit |
| Fonts audiovisuals públiques i procedència | 66 WAV, transcripcions, URLs, hashes i READMEs de procedència | assolit provisionalment |
| Transcripció per persona | 66 fitxers TXT/VTT/JSON i 66 informes | assolit com a ASR |
| Anàlisi de formes per persona | `evidencia-formes.tsv`: 2.014 contextos; `matriu-formes.tsv`: 2.310 cel·les | provisional; pendent d'àudio |
| Inventari complet de formes per fitxa | Les 66 fitxes incorporen les 35 formes candidates, amb recompte ASR, clip QA i estat de verificació | assolit com a inventari automàtic; pendent d'àudio |
| Consens ASR per persona | `qa-clips-consens.tsv`: 263 coincidències en dos models; `resum-consens-per-persona.tsv` i secció homònima als 66 informes | assolit com a evidència textual |
| Perfil acústic dels consensos | `analisi-acustica-consens.tsv`: 263 clips amb F0, veu, pauses i espectre; resum incorporat als 66 informes | assolit com a priorització acústica |
| Alineació tokenitzada dels consensos | `qa-consens-tokens-base.tsv`: 249/263 formes amb timestamp i probabilitat; 14 sense token localitzat | assolit com a evidència temporal |
| Priorització de revisió tokenitzada | `prioritat-consens-token.tsv`: 14 casos sense token, 120 de baixa probabilitat i 129 forts | assolit com a cua de revisió |
| Incidències tokenitzades documentades | `informe-token-missing.md`: 14 clips sense token localitzat, amb textos, JSON i acústica | assolit com a informe de revisió |
| Contraste de tokenitzadors | `qa-token-missing-comparativa.tsv`: 7 casos recuperats pel small i 7 persistents | assolit com a diagnòstic automàtic |
| Coincidència amb límit de paraula | `qa-clips-boundary.tsv`: 249 consensos estrictes i 14 falsos positius de subcadena; resum als 66 informes | assolit com a neteja textual |
| Referència de casos persistents | `referencies-institucionals-casos-persistents.md` i secció als 7 informes | assolit com a identificació contextual; llengua pendent |
| Quarantena ASR corroborada | `qa-quarantena-base.tsv` i `informe-quarantena-comparativa.md`: 9 finestres en 3 veus amb dos ASR | pendent d'escolta |
| Normalització acústica per veu | `analisi-acustica-normalitzada-consens.tsv`: 263 deltes respecte a la mediana de cada persona; resum als 66 informes | assolit com a comparació exploratòria |
| Mesures instrumentals de formants | `analisi-formants-consens.tsv`: 250 files de mesura (161 valors F0 i 249 valors per a cadascun de F1, F2 i F3); `resum-formants-consens.tsv`: 20 formes; secció als 66 informes | assolit com a mesura exploratòria; pendent d'escolta |
| Trajectòries instrumentals per token | `analisi-trajectories-formants.tsv`: 1.250 punts (cinc per token); `resum-trajectories-formants.tsv`: medianes d'inici/final per 20 formes; secció als 66 informes | assolit com a mesura exploratòria; pendent d'escolta |
| Evidència gramatical i de contacte | `evidencia-gramatica.tsv`: 10.458 contextos candidats de nou categories; `resum-evidencia-gramatica.tsv`: 66 parlants; secció als informes | assolit com a inventari textual; pendent d'audició |
| Tercera passada dels clips forts | `qa-clips-forts-greedy.tsv` i `qa-clips-forts-consens.tsv`: 109 clips; 81 amb tres decodificacions coincidents, 24 amb dues i 4 amb una | assolit com a priorització; pendent d'escolta |
| Reproductor filtrable de divergències | `auditoria-forts-triple.html`: reproductor local dels 109 clips amb filtre per categoria i persona | assolit com a eina de revisió |
| Cua manual de divergències | `registre-audicio-forts-divergencies.tsv` i `quadern-audicio-forts-divergencies.md`: 28 files amb àudio, tres textos i camps humans buits | preparada; pendent d'escolta |
| Perfil acústic de divergències | `analisi-acustica-divergencies.tsv`: 28 files amb durada, F0, F1–F3, intensitat i contrast de veu | assolit com a suport instrumental; pendent d'escolta |
| Formants de la cua QA completa | `analisi-formants-qa.tsv`: 309 tokens localitzats en una passada QA; `resum-formants-qa.tsv`: 20 formes; secció als 66 informes | assolit com a mesura exploratòria; pendent d'escolta |
| JSON i tokens de la cua completa | `qa-cua-small-json.tsv`: 656 JSON; `qa-cua-small-tokens.tsv`: 439 clips amb 451 ocurrències tokenitzades; `analisi-formants-cua-small.tsv`: 451 mesures | assolit com a cobertura automàtica ampliada; pendent d'audició |
| Graf de la tokenització small completa | `trets-small-token.tsv`: 20 formes; `arestes-parlants-small-token.tsv`: 1.140 parelles; `matriu-formes-small-token.tsv`: 1.320 cel·les; graf Mermaid separat | assolit com a semblança textual; pendent d'audició |
| Priorització per forma | `prioritat-formes-small-token.tsv` i `quadern-formes-small-token.md`: 20 formes ordenades per cobertura, ocurrències i probabilitat | assolit com a cua de revisió; pendent d'audició |
| Perfil comparatiu per parlant | `nodes-small-token.tsv`: 66 perfils; 63 amb ocurrències small; secció de cobertura als 66 informes | assolit com a resum automàtic; pendent d'audició |
| Repertori aplicat amb evidència | `repertori-evidencia.tsv`: 1.188 files amb estat explícit d'evidència i buits conservats | assolit com a mapa de cobertura; fonètica pendent |
| Anàlisi fonètica i prosòdica | descriptors acústics dels 66 WAV i 656 clips; repertori de 18 dimensions | pendent d'escolta |
| Cobertura del repertori | `grafo/informe-cobertura-repertori.md` i `proveniencia/resum-cobertura-repertori.tsv`: 18 dimensions, 123 indicadors automàtics i 1.065 buits específics | assolit com a mapa de buits; pendent d'audició |
| Relació entre formes i parlants | capes consensual, QA i forts; grafs Mermaid i TSV | provisional; no dialectològic |
| Graf canònic de les 35 formes | `grafo/*-formes-completa.*`: 60 nodes, 1.690 arestes amb almenys tres formes i 2.100 cel·les persona-forma | assolit com a semblança textual ASR; pendent d'audició |
| Graf separat dels candidats | `grafo/nodes-formes-candidats.tsv`: 100 nodes, `grafo/arestes-formes-candidats.tsv`: 36 arestes i 24 formes entre 11 expedients | assolit com a capa textual exploratòria; pendent d'audició |
| Graf acústic separat dels candidats | `grafo/nodes-acustic-candidats.tsv`: 124 nodes i `grafo/arestes-acustic-candidats.tsv`: 859 arestes entre 11 expedients | assolit com a exploració instrumental; pendent d'audició |
| Agrupació de persones repetides | `proveniencia/persones-canonics.tsv`: 66 registres → 60 persones; graf canònic small separat amb 996 arestes | assolit com a normalització nominal; pendent d'audició |
| Clip auditable per a cada interval | `clips-audicio.tsv`: 656/656 hashes vàlids | assolit |
| Cobertura operativa per persona | `proveniencia/auditoria-cobertura-sessions.tsv`: 57 dels 60 parlants coberts per les sessions actives i 3 en quarantena | assolit com a selecció; audició pendent |
| Integritat dels WAV i clips | `proveniencia/auditoria-integritat-audio.tsv`: 66 fonts + 656 clips, 722/722 encapçalaments vàlids | assolit tècnicament; audició pendent |
| Procedència completa per font | `proveniencia/auditoria-proveniencia.tsv`: 66/66 fitxes amb URL, termes d’ús, derivat, hash i ASR | assolit documentalment |
| Integritat de les transcripcions | `proveniencia/auditoria-integritat-transcripcions.tsv`: 64/66 estructuralment completes; pa-028 i pa-047 amb incidències de timestamp/ASR registrades | QA pendent en dos casos |
| Derivats QA de timestamps | `proveniencia/auditoria-remediacio-transcripcions.tsv`: VTT limitats a la durada per pa-028 i pa-047, sense tocar els originals | preparats; audició pendent |
| Índex operatiu d'audició | `proveniencia/INDEX-AUDICIO.md`: entrada única a les cues, guies, registres i importadors | preparat; audició pendent |
| Independència del subcorpus | `proveniencia/auditoria-independencia.tsv`: 253 documents, sense enllaços relatius fora del directori ni destinacions inexistents | assolit |
| Independència del graf | `proveniencia/auditoria-grafo-independent.tsv`: sis capes canòniques sense IDs fora de les 60 persones | assolit |
| QA alternatiu de quarantena | `proveniencia/qa-quarantena-20s-alt-resum.tsv`: 237 finestres, 193 localitzables, 42 amb bucle i 2 silencioses | priorització; audició pendent |
| Cua humana de quarantena contrastada | `proveniencia/auditoria-cua-quarantena-20s.tsv`: 15/15 clips localitzables i preparats, camps humans buits | preparada; audició pendent |
| Cobertura de formes candidates | `proveniencia/auditoria-cobertura-formes.tsv`: 35 formes, 10 amb cobertura escassa i prioritat alta d’audició | mapa de revisió; confirmació pendent |
| Cua de formes escasses | `proveniencia/cua-audicio-formes-escasses.tsv`: 30 clips, 3 per cadascuna de les 10 formes escasses, amb hash vàlid | preparada; audició pendent |
| Registre propi de formes escasses | `proveniencia/registre-audicio-formes-escasses.tsv`: 30 claus separades del registre general, amb camps humans | preparat; audició pendent |
| Progrés d'audició per persona | `proveniencia/resum-estat-audicio.tsv`: 60 persones amb el desglossament de 656 intervals generals i 30 clips escassos | preparat; audició pendent |
| Guia de les formes escasses | `proveniencia/guia-audicio-formes-escasses.tsv`: 10 formes, 30 clips i criteris d'escolta per forma | preparada; audició pendent |
| Perfil acústic de les formes escasses | `proveniencia/analisi-acustica-formes-escasses.tsv`: 30 clips amb descriptors instrumentals orientatius | preparat; audició pendent |
| Reproductor de formes escasses | `proveniencia/auditoria-formes-escasses.html`: reproductor local dels 30 clips amb filtres i exportació d'anotacions | preparat; audició pendent |
| Importació de formes escasses | `proveniencia/importa-auditoria-formes-escasses.py`: valida la clau persona-forma-clip abans d'escriure | preparat; sense anotacions encara |
| Integritat reproducible del paquet | `proveniencia/verifica-corpus.py` retorna `OK` i valida cobertura, fitxers, hashes, registres, recomptes i ruta d'audició de les 66 fitxes | assolit |
| Traçabilitat de mostres duplicades | pa-023 i pa-057 enllacen la sessió de la seva persona canònica sense perdre la transcripció pròpia | assolit |
| Revisió auditiva | `registre-audicio.tsv`: 656 files canòniques + `auditoria-candidats.tsv`: 124 clips candidats, tots amb camps humans pendents | pendent |
| Primera cua humana de candidats | `cua-audicio-candidats-prioritaria.tsv`: 20 clips locals que cobreixen les 11 veus candidates, amb veu, forma i notes en `pendent` | preparada; pendent d'escolta |
| Mostra equilibrada per iniciar l'audició | `proveniencia/cua-audicio-small-equilibrada.tsv`: 100 clips, 63 parlants i 20 formes; quadern Markdown associat | preparada; pendent d'escolta |
| Veus en quarantena | pa-044, pa-047 i pa-050 tenen clips de control però continuen fora del graf | pendent |

## Condició de tancament

El corpus només es pot tancar com a corpus analitzat quan cada fila de
`registre-audicio.tsv` tingui una decisió auditiva (`sí`, `no` o `incerta`), una
nota justificativa i, quan sigui pertinent, variant escoltada, trets fonètics i
observacions prosòdiques. Les coincidències ASR, els descriptors acústics i la
probabilitat del model no substitueixen aquesta decisió.

Fins aleshores, la captació queda tancada en 66 registres de font que representen
60 persones canòniques, però la validació del
corpus continua oberta.

## Decisió d'abast

Amb 60 persones canòniques (66 registres de font) el corpus ja és dins l'objectiu de 50–100 persones i té cobertura
de fonts suficient per comparar formes. No cal incorporar més parlants ara: el
següent guany de qualitat és completar l'audició dels 656 intervals, resoldre
les tres veus en quarantena i convertir les coincidències automàtiques en
decisions lingüístiques. `fonts-pendents.tsv` conserva quatre fonts pendents de
permís i onze candidats `preanalisi-candidat` per a una segona fase, després de
tancar aquesta validació.

La mostra equilibrada `proveniencia/cua-audicio-small-equilibrada.tsv` permet començar amb 100 clips que cobreixen tots els parlants amb token small i les 20 formes, sense substituir la revisió de les 656 files.

Les 66 fitxes individuals incorporen ara aquesta selecció amb enllaços directes als WAV i mantenen explícit que variant, fonètica i prosòdia continuen pendents.

`proveniencia/auditoria-small-equilibrada.html` ofereix un reproductor filtrable per anotar aquests 100 clips i exportar un TSV local; la mostra continua sense decisions fins que s'escolti.

Els 100 clips tenen també una segona descodificació `base`: `qa-equilibrada-consens.tsv` conserva 70 coincidències textuals i 30 divergències; cap d'aquestes etiquetes substitueix l'audició.

`informe-qa-equilibrada.md` documenta aquestes divergències per forma i per parlant i conserva el buit d'audició com a condició de tancament.

Dels 70 consensos textuals, la passada base permet mesurar 70 tokens: F0 és vàlida en 46 i F1, F2 i F3 en 69 cadascun. Aquestes mesures no substitueixen l'escolta.

La cua prioritzada `proveniencia/prioritat-audicio-equilibrada.tsv` separa 52 casos A, 18 B i 30 C per començar l'audició en ordre de confiança.

Les trajectòries base mesuren cinc punts temporals per als 70 tokens amb doble coincidència i queden com a descriptors instrumentals pendents d'audició.

La tercera passada greedy dels 100 clips dona 61 triples, 34 dobles i 5 coincidències d'un sol model; continua sent una priorització, no una decisió auditiva.

La mateixa passada greedy cobreix ara els 656 clips mestres: 206 triples, 201 dobles, 113 d'un sol model i 136 sense coincidència. Aquest recompte continua pendent d'escolta.

La cua operativa `proveniencia/prioritat-audicio-triple.tsv` posa davant 80 clips amb triple coincidència i probabilitat alta, però manté tots els camps humans pendents.

L'inventari `proveniencia/inventari-incerteses-asr.tsv` afegeix 13.390 segments amb tokens per sota de p=0,55 i enllaça 1.283 amb clips de formes; serveix per revisar errors de transcripció abans d'interpretar cap tret.

La mostra `proveniencia/cua-audicio-incerteses.tsv` redueix aquesta cua a 100 clips de 63 persones i té reproductor local a `proveniencia/auditoria-incerteses.html`; continua amb camps humans buits.
`proveniencia/auditoria-global.html` unifica ara els 656 clips canònics i els 124 clips dels onze candidats (780 en total), amb filtres d'origen i exportació TSV dels camps humans. La cua continua sense decisions fins que s'escoltin els fragments.
`proveniencia/importa-auditoria-global.py` valida aquesta exportació amb coincidència exacta de clip, detecta conflictes i només projecta les files canòniques a `registre-audicio.tsv`; les anotacions de candidats queden en un fitxer separat.
La primera sessió operativa `proveniencia/sessions/sessio-01.tsv` selecciona 65 clips: 20 triples amb probabilitat alta, 10 triples amb probabilitat baixa i els 35 clips dels tres candidats RTVA. El quadern `sessio-01.md` conserva l'ordre i la justificació de cada fragment.
La sessió `proveniencia/sessions/sessio-02.tsv` afegeix 20 clips canònics, un per cadascun dels 20 marcadors del repertori, i evita repetir els clips de la primera sessió.
La sessió `proveniencia/sessions/sessio-03.tsv` afegeix 12 clips de Joan Micó, mantinguts fora del registre canònic fins a confirmar veu, forma i termes d'ús.
La sessió `proveniencia/sessions/sessio-04.tsv` afegeix 4 clips de l'extracte de Xavier Espot, mantinguts fora del registre canònic fins a confirmar atribució, forma i termes d'ús.
Les sessions 03 i 04 incorporen ara `text_small`, `text_base`, rol provisional i mesures F0/formants/pauses per facilitar l'escolta; aquests camps són suport automàtic i no omplen `registre-audicio.tsv`.
La sessió 01 incorpora els mateixos camps automàtics a les 35 files candidates RTVA; les 30 files canòniques es mantenen sense alterar.
La sessió 01 i la sessió 02 incorporen ara també el text de la passada small, el context base i les mesures acústiques/formàntiques disponibles per a les files canòniques; són suport de revisió i no omplen cap decisió humana.
`proveniencia/auditoria-sessions-canoniques.html` ofereix un reproductor filtrable per revisar aquests 89 clips canònics de les sessions 01–02, 05 i 06 i exportar les anotacions; les files continuen pendents fins que s'escoltin.

La quarta descodificació `proveniencia/qa-beam.tsv` cobreix 63 veus actives amb una cerca de feixos; reforça la priorització textual però no substitueix l'escolta.

Joan Verdú queda documentat com a candidat separat a `proveniencia/candidats/lead-rtva-001/`: l'àudio i l'ASR ja són locals, però no s'afegeix als 60 parlants canònics fins a separar veus i completar l'audició.
 Té una segona descodificació base i una taula de formes consensuals, però la similitud textual baixa mostra que cal escolta directa abans d'interpretar-la.
El candidat té també un graf provisional separat a `proveniencia/candidats/lead-rtva-001/graf/`: 11 formes consensuals entre small i base, 54 connexions textuals amb el graf canònic i 61 nodes. Aquest resultat només orienta la revisió i no modifica el recompte de 60 persones.
Ian Moya queda documentat com a segon candidat separat a `proveniencia/candidats/lead-rtva-002-ian-moya/`: l'entrevista RTVA té WAV local, dues passades ASR, 35 formes candidates i 15 clips. La font combina la seva veu amb la de l'entrevistador i no declara una llicència oberta; per això no modifica el recompte canònic.
El candidat té també un graf provisional separat amb 14 formes consensuals, 60 connexions textuals i 61 nodes; la vista només orienta l'audició i no és una atribució dialectal.
Els 15 clips d'Ian tenen una tercera descodificació greedy: 2 coincideixen en els tres models, 1 en dos, 7 en un i 5 en cap; la taula continua sent priorització ASR.
DJ Neura queda documentat com a tercer candidat separat a `proveniencia/candidats/lead-rtva-003-dj-neura/`: té MP3 i WAV locals, dues passades ASR, 35 formes, 10 clips i un graf provisional de 8 formes, 60 connexions i 61 nodes. La segmentació textual deixa 36 segments `dj-neura-probable`, 21 de l'entrevistador i 85 indeterminats; cap d'aquestes etiquetes és una diarització.
Els 10 clips de DJ Neura tenen una tercera descodificació greedy: 3 coincideixen en dos models, 2 en un i 5 en cap; també queda pendent d'audició.
Joan Micó queda documentat com a quart candidat separat a `proveniencia/candidats/lead-rtva-004-joan-mico/`: té MP3 i WAV locals, 337 segments small, 457 base, 35 formes, 12 clips i un graf provisional de 12 formes, 60 connexions i 61 nodes. La segmentació textual deixa 49 segments `joan-mico-probable`, 66 de l'entrevistador i 222 indeterminats o mixtos; cap d'aquestes etiquetes és una diarització.
Els 12 clips de Joan Micó tenen una tercera descodificació greedy: 1 coincideix en tres models, 1 en dos, 6 en un i 4 en cap; també queda pendent d'audició.
El perfil `proveniencia/candidats/lead-rtva-004-joan-mico/analisi-acustica.tsv` afegeix descriptors instrumentals als 12 clips (F0, energia, centroid i pauses), però continua pendent d'audició.
La taula `formants.tsv` de Joan Micó i Xavier Espot conserva F0/F1/F2/F3 als 12 i 4 clips; són mesures instrumentals i no substitueixen l'audició.
El graf acústic `grafo/graf-acustic-candidats.mmd` relaciona provisionalment els 124 clips mesurats dels onze candidats amb 859 arestes instrumentals; no és una atribució dialectal.
Xavier Espot queda documentat com a cinquè candidat separat a `proveniencia/candidats/lead-cg-001-xavier-espot/`: conserva la URL del vídeo del Consell General i un extracte WAV inicial de 120 segons, amb 32 segments small, 36 base, 35 formes candidates, 4 clips i un graf provisional de 3 formes, 37 connexions i 61 nodes. L'extracte no modifica el recompte canònic i cal confirmar-ne l'atribució auditiva.
La tercera passada greedy dels 4 clips de Xavier Espot dona 2 triples, 1 doble i 1 d'un sol model; també queda pendent d'audició.
El perfil `proveniencia/candidats/lead-cg-001-xavier-espot/analisi-acustica.tsv` afegeix descriptors instrumentals als 4 clips (F0, energia, centroid i pauses), però continua pendent d'audició.

Pere López Agràs queda documentat com a sisè candidat separat a `proveniencia/candidats/lead-cg-002-pere-lopez/`: la pàgina del Consell General exposa un MP4, del qual es conserva un extracte WAV de 120 segons amb doble ASR, 35 formes candidates, 2 clips i perfil acústic. L'expedient no modifica el recompte canònic fins a confirmar veu i termes d'ús.

Roser Suñé queda documentada com a setena candidata separada a `proveniencia/candidats/lead-cg-003-roser-sune/`: la sessió tradicional de la Constitució conserva un WAV local de 955,24 segons i un extracte inicial de 120 segons, dues passades ASR, inventari de 35 formes, 3 clips i perfil acústic. La sessió conté diversos torns; cap fragment s'atribueix a Roser Suñé ni entra al recompte canònic fins a completar l'audició i confirmar els termes d'ús.

Carine Montaner queda documentada com a vuitena candidata separada a `proveniencia/candidats/lead-rtva-005-carine-montaner/`: RTVA exposa un MP3 de 51,68 minuts, del qual es conserven MP3 i WAV locals, dues passades ASR, 35 formes, 22 clips i perfil acústic. L'entrevista té torns alterns; el dossier no modifica el recompte canònic fins a separar la veu i confirmar els termes d'ús.

Jaume Tomàs queda documentat com a novè candidat separat a `proveniencia/candidats/lead-rtva-006-jaume-tomas/`: RTVA exposa un MP3 de 24,34 minuts, del qual es conserven MP3 i WAV locals, dues passades ASR, 35 formes, 14 clips i perfil acústic. L'entrevista té torns alterns; el dossier no modifica el recompte canònic fins a separar la veu i confirmar els termes d'ús.

Robert Guirao queda documentat com a desè candidat separat a `proveniencia/candidats/lead-rtva-007-robert-guirao/`: RTVA exposa un MP3 de 18,31 minuts, del qual es conserven MP3 i WAV locals, dues passades ASR, 35 formes, 13 clips i perfil acústic. L'entrevista té torns alterns; el dossier no modifica el recompte canònic fins a separar la veu i confirmar els termes d'ús.

Mireia Pedescoll queda documentada com a onzena candidata separada a `proveniencia/candidats/lead-rtva-008-mireia-pedescoll/`: RTVA exposa un MP3 de 23,01 minuts, del qual es conserven MP3 i WAV locals, dues passades ASR, 35 formes, 19 clips i perfil acústic. L'entrevista té torns alterns; el dossier no modifica el recompte canònic fins a separar la veu i confirmar els termes d'ús.
La revisió conjunta dels candidats queda disponible a `proveniencia/auditoria-candidats-completa.html`: 124 clips locals dels 11 expedients, inclosos els 10 clips històrics de Joan Verdú. Exporta anotacions humanes en un TSV separat i no projecta cap decisió al registre canònic.

La primera tanda humana `proveniencia/cua-audicio-candidats-prioritaria.tsv` selecciona 20 clips: cobreix una ocurrència de cadascuna de les 11 veus candidates i completa la cua amb casos de consens ASR alt. Els camps humans comencen en `pendent` i la tanda no altera `persones.tsv` ni el graf canònic.

La vista estricta `grafo/*-triple-full.*` restringeix el graf als 206 clips amb triple coincidència: 19 formes, 106 arestes entre parlants i 1.140 cel·les persona-forma. És una síntesi textual per orientar l'audició, no un tancament lingüístic.

Quan hi hagi anotacions, `proveniencia/importa-auditoria-equilibrada-master.py` les podrà projectar al registre mestre només si la coincidència de clip és exacta i no hi ha conflicte.

El protocol de tancament i els camps d'anotació estan fixats a `proveniencia/protocol-audicio-anotacio.md`; les decisions automàtiques no compten com a escolta.

El resum regenerable `proveniencia/resum-estat-audicio.tsv` confirma l'estat actual: 656 pendents al registre mestre, 100 pendents a la mostra i cap decisió humana incorporada.

Per facilitar la revisió, `proveniencia/auditoria-forts.html` reprodueix els 109
clips forts i `proveniencia/auditoria-cua.html` cobreix els 656 clips. Tots dos
permeten exportar anotacions locals; `proveniencia/importa-auditoria.py` les
valida i les incorpora al registre mestre només quan s'executa amb `--write`.
`proveniencia/quadern-audicio-consens.md` ofereix una cua Markdown més curta amb
els 263 clips on coincideixen els dos models.

Abans de qualsevol ampliació o tancament, es pot repetir:

```sh
python proveniencia/verifica-corpus.py
```

`proveniencia/auditoria-cobertura-persones.tsv` comprova les 66 fitxes: títol, inventari de 35 formes, perfil lingüístic, àudio, transcripció i procedència; marca explícitament les tres veus en quarantena.

`proveniencia/importa-auditoria-sessions-canoniques.py` valida l'exportació de la vista amb la clau exacta `(persona, forma, clip)`, exigeix una nota per a cada decisió i només escriu amb `--write`.

`proveniencia/guia-audicio-sessions-canoniques.tsv` desglossa els 89 clips de les sessions 01–02, 05 i 06 per forma i categoria, i fixa qué cal revisar en lèxic, morfosintaxi, fonètica i prosòdia abans de decidir.

`actualitza-informes-sessions-canoniques.py` manté els 89 clips de les sessions 01–02, 05 i 06 dins de les 61 fitxes canòniques implicades, amb els dos textos ASR i els clips directes; tots continuen marcats com a pendents d’audició.

El graf `grafo/graf-acustic-canonic.mmd` resumeix els 60 parlants canònics amb 1.036 arestes instrumentals; 57 nodes tenen mesures i les tres veus en quarantena es conserven sense inventar valors. La capa no és una atribució dialectal i continua pendent d'audició.

`proveniencia/resum-cobertura-fonts.tsv` verifica la diversitat de fonts: 33 registres del Consell General, 17 de RTVA, 12 d'Andorra Recerca i Innovació i 4 de l'Arxiu d'Etnografia, amb els termes d'ús separats.

`actualitza-informes-repertori.py` incorpora a les 66 fitxes les 18 dimensions del repertori, amb evidència automàtica i buits d'audició separats; no converteix cap indicador en tret dialectal confirmat.

`proveniencia/quadern-sessions-canoniques.md` ofereix la mateixa cua de 89 clips en Markdown, amb enllaços directes a l'àudio i camps d'anotació encara pendents.

`proveniencia/auditoria-objectiu.tsv` és la matriu regenerable de **23 requisits i evidències**; manté explícit que la revisió auditiva dels 656 clips canònics, els 30 de formes escasses i els 124 candidats encara està pendent.

`proveniencia/auditoria-identitat-linguistica.tsv` audita la qualificació dels 60 parlants: tots 60 tenen ara una font contextual, encara que en el cas de Carles Sasplugas la coincidència amb el nom complet del registre municipal continua marcada com a compatible i no verificada; la biografia lingüística continua explícitament pendent per a totes.
La prospecció manté també una referència nova del Consell General en estat
`pendent-recollida`; no altera el recompte de 60 persones fins que hi hagi
àudio local, veu atribuïble i termes d’ús documentats.
