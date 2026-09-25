# Graf independent del corpus de parla andorrana

Aquest graf no té enllaços cap al corpus temàtic actual. Les dades es mantindran
com a taules locals. Hi ha 66 nodes de registre i una vista canònica de 60 persones; pa-044, pa-047 i pa-050 queden en quarantena i les arestes automàtiques es calculen sobre 63 transcripcions utilitzables.

L'estat verificable i la condició de tancament són a `../ESTAT-OBJECTIU.md`.

- `nodes.tsv`: parlants, fonts i trets observats.
- `arestes.tsv`: relacions justificades entre parlants, fonts i trets.
- `graf.mmd`: vista Mermaid de les relacions que ja tenen evidència provisional.
- `trets.tsv` i `arestes-auto.tsv`: recompte regenerable dels marcadors que
  travessen almenys tres transcripcions; encara requereixen revisió auditiva.
- `trets-consens.tsv` i `arestes-consens-asr.tsv`: vista més estricta amb només
  les formes presents en les dues passades ASR; tampoc és validació fonètica.
- `arestes-parlants-consens.tsv`: relacions directes entre parelles que comparteixen
  almenys tres formes del conjunt consensual; són semblances textuals provisionals.
- `graf-parlants-consens.mmd`: vista Mermaid de les parelles amb cinc formes o més
  compartides.
- `trets-linguistics.tsv` i `arestes-linguistics.tsv`: capa ampliada de candidats discursius i lèxics; 284 trets i 1.951 arestes ASR provisionals.
- `arestes-acustica-densa.tsv`: veïnatges entre veus a partir de descriptors acústics densos; són exploratoris i no dialectals.
- `arestes-clusters-prosodia.tsv` i `graf-prosodia.mmd`: agrupacions acústiques
  exploratòries de les 63 veus actives, separades de les formes lingüístiques.
- `auditoria-formes.tsv`: ocurrències amb segons d'àudio i confiança mínima del
  segment per prioritzar l'escolta manual.
- `../proveniencia/pla-audicio.tsv` i `../proveniencia/pla-audicio.md`: cua
  ordenada dels 656 intervals per començar la revisió auditiva.
- `../proveniencia/qa-beam.tsv`: tercera passada ASR amb cerca de feixos sobre
  un clip prioritari per cadascuna de les 63 veus actives; continua sent
  evidència textual pendent d'escolta.
- `../proveniencia/qa-quarantena.tsv`: nou finestres ASR independents per a les
  tres veus en quarantena, només per comprovar si els bucles es poden acotar.
- `../proveniencia/qa-clips.tsv`: quarta passada ASR sobre els 656 clips de la
  cua completa; la coincidència textual continua pendent de validació auditiva.
- `../proveniencia/qa-clips-base.tsv`: passada independent amb `ggml-base.bin`
  sobre els mateixos 656 clips.
- `../proveniencia/qa-clips-consens.tsv`: comparació de les dues passades; 263
  clips tenen coincidència textual en tots dos models.
- `../proveniencia/resum-consens-per-persona.tsv`: recompte de consens i
  divergències per a cadascuna de les 66 fitxes; la secció també queda copiada
  als informes individuals.
- `../proveniencia/analisi-acustica-consens.tsv` i
  `../proveniencia/resum-acustica-formes-consens.tsv`: descriptors acústics dels
  263 consensos i medianes per forma; orienten l'escolta i no són trets fonètics.
- `../proveniencia/quadern-audicio-consens.md`: cua Markdown dels 263 consensos,
  amb enllaços d'àudio i camps d'anotació humana.
- `../proveniencia/qa-consens-tokens-base.tsv`: alineació temporal de la forma
  dins dels consensos; 249 clips tenen token localitzat i 14 queden sense
  coincidència tokenitzada.
- `../proveniencia/prioritat-consens-token.tsv`: ordre de revisió dels 263
  consensos en tres categories segons tokenització i probabilitat.
- `../proveniencia/informe-token-missing.md`: informe dels 14 casos sense token
  localitzat, amb els dos textos ASR i el fragment acústic.
- `../proveniencia/qa-token-missing-comparativa.tsv`: contrast entre les
  tokenitzacions base i small dels 14 casos.
- `../proveniencia/referencies-institucionals-casos-persistents.md`: fonts
  oficials d'identificació territorial per als set casos sense token en cap model.
- `../proveniencia/qa-quarantena-comparativa.tsv` i
  `../proveniencia/informe-quarantena-comparativa.md`: comparació base/small de
  les nou finestres de les tres veus en quarantena.
- `../proveniencia/analisi-acustica-normalitzada-consens.tsv` i
  `../proveniencia/resum-acustica-normalitzada-formes.tsv`: deltes acústics dels
  263 consensos respecte a la veu completa de cada persona.
- `../proveniencia/analisi-formants-consens.tsv` i
  `../proveniencia/resum-formants-consens.tsv`: 250 files de mesures instrumentals de F0, F1, F2 i F3 en tokens localitzats
  (161 valors F0 i 249 valors per a cadascun de F1, F2 i F3); són exploratòries i no dialectals.
- `../proveniencia/analisi-trajectories-formants.tsv` i
  `../proveniencia/resum-trajectories-formants.tsv`: cinc punts temporals per als
  250 tokens alineats (1.250 files) i medianes d'inici/final; són exploratoris.
- `../proveniencia/evidencia-gramatica.tsv` i
  `../proveniencia/resum-evidencia-gramatica.tsv`: 10.458 contextos ASR de nou
  categories gramaticals i de contacte, amb l'estat de revisió pendent.
- `../proveniencia/qa-clips-forts-consens.tsv` i
  `../proveniencia/informe-forts-greedy.md`: tercera descodificació dels 109 clips
  forts; separa 81 triples, 24 dobles i 4 casos d'un sol model.
- `../proveniencia/analisi-formants-qa.tsv` i
  `../proveniencia/resum-formants-qa.tsv`: formants de 309 tokens localitzats en
  una passada QA, diferenciats del consens de dos models.
- `../proveniencia/qa-cua-small-tokens.tsv`, `../proveniencia/qa-cua-small-token-occurrences.tsv` i
  `../proveniencia/analisi-formants-cua-small.tsv`: 439 clips i 451 ocurrències
  tokenitzades en la cua completa small, sense consens entre models.
- `trets-small-token.tsv`, `arestes-parlants-small-token.tsv`,
  `graf-parlants-small-token.mmd` i `matriu-formes-small-token.tsv`: capa separada
  de 20 formes, 1.140 parelles i 1.320 cel·les basada en tokenització small.
- `../proveniencia/prioritat-formes-small-token.tsv` i
  `../proveniencia/quadern-formes-small-token.md`: ordre de revisió per cobertura,
  ocurrències i probabilitat de token.
- `nodes-small-token.tsv`: perfil dels 66 registres de font amb formes, ocurrències i
  probabilitat mediana de la tokenització small.
- `../proveniencia/persones-canonics.tsv` i `*-small-token-canonics.tsv`: vista agrupada dels 60 parlants únics (66 registres), amb 20 formes, 996 arestes i 1.200 cel·les.
- `../proveniencia/cua-audicio-small-equilibrada.tsv` i `../proveniencia/quadern-audicio-small-equilibrada.md`: mostra de 100 clips equilibrada entre els 63 parlants amb tokens i les 20 formes, per iniciar l'audició.
- `../proveniencia/qa-equilibrada-consens.tsv`: contrast small/base dels 100 clips de la mostra (70 coincidències, 30 divergències), separat del graf fins a l'audició.
- `../proveniencia/repertori-evidencia.tsv`: mapa de cobertura de les 18
  dimensions per persona, amb evidència textual o acústica separada dels buits.
- `../proveniencia/qa-clips-boundary.tsv` i
  `../proveniencia/resum-boundary-per-persona.tsv`: coincidències recalculades
  amb límits de paraula; eviten falsos positius per subcadena.
- `trets-boundary-consens.tsv`, `arestes-parlants-boundary-consens.tsv` i
  `graf-parlants-boundary-consens.mmd`: graf estricte de paraula completa,
  separat de les capes anteriors.
- `../proveniencia/prioritat-audicio.tsv`: ordre de revisió que combina les
  quatre evidències automàtiques i separa 303 casos A, 63 B, 86 C i 204 D.
- `../proveniencia/analisi-acustica-clips.tsv`: descriptors de senyal dels 656
  clips per orientar l'anotació de prosòdia; no són trets dialectals.
- `../proveniencia/registre-audicio.tsv`: full únic per completar la confirmació
  auditiva, la variant escoltada i els trets fonètics o prosòdics.
- `../proveniencia/evidencia-formes.tsv`: 2.014 contextos ASR localitzables per
  forma i persona; serveixen per obrir el fragment corresponent.
- `../proveniencia/qa-clips-json.tsv`: timestamps de la quarta passada per als
  303 clips A de triple consens.
- `../proveniencia/qa-formes-tokens.tsv`: 309 coincidències de tokens i quatre
  clips sense coincidència, amb temps absolut i probabilitat.
- `trets-forts.tsv`, `arestes-parlants-forts.tsv` i `graf-parlants-forts.mmd`:
  capa de 109 clips A amb probabilitat mínima de token >= 0,80; 13 trets i 59
  relacions de parelles, sempre pendents d'audició.
- `../proveniencia/quadern-audicio-forts.md`: quadern de revisió dels 109 clips
  amb enllaços al WAV i camps humans d'anotació.
- `../proveniencia/auditoria-forts.html`: reproductor local amb filtres i
  exportació TSV per anotar aquests clips.
- `../proveniencia/evidencia-formes-vtt.tsv`: 3.326 ocurrències candidates
  alineades amb intervals temporals VTT.
- `repertori-referencia.tsv`: 18 dimensions de revisió extretes de referències
  dialectològiques i sociolingüístiques; cap és un veredicte del corpus.
- `repertori-aplicat.tsv`: 1.188 files (66 × 18) que separen indicadors ASR o
  acústics legítims dels candidats que requereixen escolta.
- `repertori-aplicat-canonic.tsv`: vista reagrupada dels mateixos indicadors
  per als 60 parlants canònics (1.080 files, 60 × 18); conserva els registres
  de font i continua sent exploratòria fins a l'audició humana.
- `genera-repertori-aplicat-canonic.py`: regenerador de la vista canònica a
  partir de `repertori-aplicat.tsv` i `../proveniencia/persones-canonics.tsv`.
- `informe-cobertura-repertori.md` i `../proveniencia/resum-cobertura-repertori.tsv`:
  resum de les 18 dimensions, amb 123 indicadors automàtics i 1.065 buits
  específics que no es poden inferir de la grafia ASR.
- `matriu-formes.tsv`: 2.310 cel·les persona-forma (66 × 35), amb recompte ASR,
  clip QA disponible i coincidència textual separats.
- `README-formes-completa.md`, `nodes-formes-completa.tsv`,
  `trets-formes-completa.tsv`, `arestes-parlants-formes-completa.tsv`,
  `matriu-formes-completa.tsv` i `graf-parlants-formes-completa.mmd`: vista
  canònica que reagrupa les 35 formes de la matriu en 60 persones, amb 1.690
  parelles que comparteixen almenys tres formes. Continua sent una semblança
  textual ASR pendent d'audició.
- `trets-qa.tsv`, `arestes-parlants-qa.tsv` i `graf-parlants-qa.mmd`: vista
  restringida als 18 trets que reapareixen en almenys tres veus en la quarta
  passada (1.222 relacions de parelles); continua sent textual i provisional.
- `trets-triple-full.tsv`, `arestes-parlants-triple-full.tsv`, `graf-parlants-triple-full.mmd`, `nodes-triple-full.tsv` i `matriu-formes-triple-full.tsv`: vista estricta dels 206 clips amb triple coincidència greedy; 19 formes, 106 arestes amb almenys tres formes compartides i 1.140 cel·les persona-forma, encara pendents d'audició.
- `trets-base-consens.tsv`, `arestes-parlants-base-consens.tsv` i
  `graf-parlants-base-consens.mmd`: capa estricta de les 18 formes que tenen
  coincidència en les dues passades ASR i reapareixen en almenys tres veus.
- `../proveniencia/analisi-prosodia.tsv`: activitat, energia, creuaments per zero
  i F0 espectral orientativa per prioritzar fragments comparables.
- `informe-comparatiu.md`: lectura global de la cobertura, els patrons i els
  límits de la primera passada.

- ../proveniencia/analisi-acustica-densa.tsv: descriptors acústics densos per seleccionar intervals comparables.

- ../proveniencia/analisi-linguistica.tsv: repertori ampliat de candidats discursius i lèxics per parlant.

La capa `README-acustic-candidats.md`, amb `nodes-acustic-candidats.tsv`, `arestes-acustic-candidats.tsv` i `graf-acustic-candidats.mmd`, relaciona provisionalment els 124 clips mesurats dels onze candidats per F0, formants, pauses, proporció de veu i centroid espectral. Les arestes són instrumentals i pendents d’audició.

La capa `README-acustic-canonic.md`, amb `nodes-acustic-canonic.tsv`, `arestes-acustic-canonic.tsv` i `graf-acustic-canonic.mmd`, resumeix els 60 parlants canònics amb 1.036 arestes de semblança instrumental; 57 nodes tenen mesures i 3 queden sense mesures per estar en quarantena. No és una classificació dialectal.
