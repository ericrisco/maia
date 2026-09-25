La cobertura de font és de 66 registres que corresponen a 60 persones canòniques; sis persones tenen dues mostres i la vista canònica evita comptar-les dues vegades.

# Informe comparatiu provisional

## Cobertura

El subcorpus conserva 66 paquets i 66 àudios locals (unes 20,2 hores); 63 mostres entren ara al graf perquè pa-044, pa-047 i pa-050 estan en quarantena ASR. Cada registro tiene transcripción ASR en catalán, VTT, JSON con
probabilidades, versión marcada por confianza, informe individual y ficha de
procedencia. Las fuentes se conservan separadas del corpus temático de Maia.

La mostra combina 12 càpsules d'Andorra Recerca i Innovació, 33 peces del
Consell General, 17 entrevistes o perfils de RTVA i quatre peces de l'Arxiu
d'Etnografia d'Andorra. Aquestes darreres declaren ús educatiu i investigador sense
difusió; les peces del Consell i RTVA es conserven com a còpies locals de recerca.

## Formas compartidas

El recuento automático compara 20 formas discursivas y léxicas. Diecinueve
aparecen en al menos tres transcripciones y se representan como candidatos en
`arestes-auto.tsv`; `ensenyança` aparece en dos y queda pendiente. Las formas
Amb més cobertura hi ha `perquè` (50 parlants), `bé` (48), `clar` (42), `doncs` (42),
`bueno` (37), `llavors` (37), `és a dir` (31) i `crec` (31).

Estos números miden cadenas producidas por Whisper, no realizaciones fonéticas.
El grafo identifica coincidencias para orientar la revisión: no afirma que una
forma sea exclusiva de Andorra ni que su frecuencia sea una propiedad
dialectal. Cada arista automática conserva la evidencia `recompte ASR; revisió
auditiva pendent`.

Cinquanta-set fitxes (pa-001—pa-043, pa-045—pa-046, pa-048—pa-049 i pa-051—pa-054) tenen lectura manual o contextual
ampliada; dotze fitxes noves, pa-055—pa-066, conserven anàlisi automàtica provisional i pa-044, pa-047 i pa-050 queden en quarantena ASR. Totes continuen marcades com a
provisionals perquè la
validació auditiva i fonètica encara no s'ha completat.

La cua `auditoria-formes.tsv` conserva fins a vuit intervals temporals per
parlant i forma, amb una prioritat alta quan el segment conté tokens de baixa
confiança. Això permet revisar el senyal sense confondre una coincidència ASR
amb una observació lingüística.
La tercera passada `proveniencia/qa-beam.tsv` comprova un clip prioritari per veu amb cerca de feixos; 63 de 63 clips actius s'han processat i els resultats continuen sent evidència ASR.

Per a les tres veus en quarantena s'han afegit nou finestres independents de 30
segons a `proveniencia/qa-quarantena.tsv`. Les finestres de pa-044 i pa-050 no
repeteixen línies en aquesta mostra curta; pa-047 presenta una finestra repetitiva
i dues netes. Aquest resultat permet reprendre la revisió per mostreig, però no
justifica treure cap veu de la quarantena sense escolta.

La quarta passada `proveniencia/qa-clips.tsv` cobreix els 656 clips de la cua i
recupera la forma candidata textualment en 452 fragments; els 204 restants són
divergències del model que s'han de revisar contra l'àudio, no errors confirmats.
La vista `trets-qa.tsv` conserva 18 formes que reapareixen en almenys tres veus
en aquesta passada i `arestes-parlants-qa.tsv` enllaça 1.222 parelles que
comparteixen almenys tres d'aquestes formes. Aquest graf és una priorització
textual independent, no una validació dialectològica.

La cua `proveniencia/prioritat-audicio.tsv` ordena els 656 intervals: 303 tenen
triple consens automàtic, 63 doble consens, 86 només una coincidència i 204
divergeixen. Aquest ordre permet començar l'escolta pels clips més robustos.

La passada independent `proveniencia/qa-clips-base.tsv`, executada amb
`ggml-base.bin`, recupera la forma candidata en 321 clips. La intersecció amb la
passada `small` queda en **263 clips** (`qa-clips-consens.tsv`); 393 clips
divergeixen entre models. Aquesta intersecció és una corroboració textual més
estricta, no una confirmació auditiva ni fonètica.

La capa `grafo/trets-base-consens.tsv` conserva 18 formes que reapareixen en
almenys tres veus dins dels 263 consensos. Les seves arestes estan separades de
les capes anteriors perquè els dos textos automàtics es puguin comparar sense
convertir el consens en un veredicte dialectal.

Per als 263 clips consensuals, `proveniencia/analisi-acustica-consens.tsv`
conserva F0 orientativa, IQR de F0, proporció de veu, pausa mediana i centroid
espectral. `resum-acustica-formes-consens.tsv` resumeix aquests descriptors per
forma; poden ordenar l'escolta i la prosòdia, però no resolen vocals, accent,
/r/ ni entonació sense anotació auditiva.

La passada base amb JSON complet conserva timestamps i probabilitats token a
`proveniencia/qa-consens-tokens-base.tsv`: 249 de 263 clips tenen la forma
localitzada i 14 no tenen coincidència tokenitzada. Hi ha 250 coincidències de
token; la mediana de probabilitat mínima és 0,5622 i 120 queden per sota de
0,55. Aquests 14 casos no es descarten; són prioritats d'escolta perquè mostren
que una coincidència textual de segment no sempre es manté al nivell de token.
La cua `proveniencia/prioritat-consens-token.tsv` separa 14 casos sense token,
120 de baixa probabilitat i 129 forts per ordenar la revisió auditiva.

La cerca inicial per subcadena contenia 14 falsos positius: formes com `bé` dins
`ben` o fragments que només apareixien en una de les dues transcripcions. La
capa `proveniencia/qa-clips-boundary.tsv` aplica límits alfanumèrics i redueix el
consens estricte a 249 clips; `grafo/trets-boundary-consens.tsv` conserva 18
formes amb almenys tres parlants. Aquesta neteja millora la precisió textual,
però encara no confirma cap pronunciació.

Els descriptors de `proveniencia/analisi-acustica-clips.tsv` permeten comparar
activitat de veu, energia, F0 orientativa, espectre i pauses en el mateix
fragment que sosté cada candidat textual; continuen sent mesures exploratòries.

Les fitxes poden obrir 2.014 contextos de les formes candidates a
`proveniencia/evidencia-formes.tsv`; aquests fragments només localitzen la
sortida ASR i encara no són exemples dialectals confirmats.
Els 303 clips de triple consens tenen també timestamps JSON a
`proveniencia/qa-clips-json.tsv`, que faciliten la localització temporal durant
l'audició.
En 309 ocurrències tokenitzades (quatre clips no tenen coincidència) es conserven
probabilitats i temps absoluts a `proveniencia/qa-formes-tokens.tsv`; una
probabilitat baixa només augmenta la prioritat d'escolta.
El filtre `proveniencia/candidats-forts.tsv` deixa 109 clips amb triple consens i
probabilitat mínima de token >= 0,80. La capa derivada del graf conté 13 trets i
59 relacions; continua sent ASR provisional.
La taula `proveniencia/evidencia-formes-vtt.tsv` alinea 3.326 ocurrències amb
segments VTT i permet obrir el context temporal corresponent.
El repertori `grafo/repertori-referencia.tsv`, documentat a
`proveniencia/referencies-linguistiques.md`, amplia la revisió a 18 dimensions
de vocalisme, morfologia, fonosintaxi, lèxic, prosòdia i variació social.
`grafo/repertori-aplicat.tsv` les desplega per als 66 registres de font i manté buida
l'observació auditiva fins que hi hagi escolta directa.
La matriu `grafo/matriu-formes.tsv` deixa preparada la comparació persona-forma
(66 × 35) sense interpretar els zeros o les divergències com a absència
dialectal.

El pla proveniencia/pla-audicio.tsv ordena els 656 intervals per consens ASR i coincidència temporal, de manera que la revisió humana pot començar pels fragments amb més evidència textual.

La cua operativa `proveniencia/cua-audicio.tsv` redueix aquesta informació al
primer interval de cadascuna de les 20 formes per parlant (656 intervals, 66
parlants) i hi afegeix el consens entre ASR, la coincidència temporal entre
passades (384 intervals) i les mètriques acústiques orientatives.
Els 656 clips es conserven a `proveniencia/clips/` i es registren a
`proveniencia/clips-audicio.tsv`: 384 provenen de solapaments temporals entre ASR
i 272 s'han extret directament del WAV; encara no tenen veredicte humà.

Per a pa-004—pa-023, pa-025—pa-043, pa-045—pa-046, pa-048—pa-049, pa-053—pa-054 i pa-055—pa-066 s'ha fet una segona passada amb Whisper base. Pa-024 conserva una resegmentació base separada, però no es compta com a doble ASR perquè és la transcripció canònica actual; pa-050 queda fora per la seva quarantena ASR. `auditoria-creuada-asr.tsv` conserva les coincidències i divergències de les 20 formes; una coincidència entre dos ASR reforça la prioritat de revisió, però tampoc substitueix l'escolta humana.
La vista estricta `trets-consens.tsv` conserva 19 formes amb almenys tres parlants
coincidents en les dues passades; `ensenyança` queda pendent. Les seves arestes
continuen marcades com a consens textual provisional, no com a tret dialectal.
`arestes-parlants-consens.tsv` explicita 1.386 parelles que comparteixen almenys tres
formes consensuals; és una relació de semblança textual per orientar la comparació,
no una classificació de dialectes ni d'identitats lingüístiques.
La taula `arestes-acustica-densa.tsv` afegeix 143 veïnatges acústics entre les 63 veus actives a partir de descriptors robustos d'energia, F0, espectre i pauses; aquests veïnatges només serveixen per seleccionar clips i no són semblances dialectals.

La capa acústica agrupa exploratòriament les 63 veus actives en quatre clústers
(`proveniencia/resum-clusters-prosodia.md`); les diferències poden provenir de
microfonia, música, edició o del propi ASR i requereixen escolta abans d'interpretar-les.

La taula grafo/trets-linguistics.tsv conserva 284 trets ampliats (discursius, territorials i gramaticals) i grafo/arestes-linguistics.tsv relaciona 1.951 parelles que comparteixen almenys tres candidats; aquesta capa és textual i provisional.
Les mesures de formants `proveniencia/analisi-formants-consens.tsv` intenten descriure 250 tokens alineats: hi ha 161 valors F0 i 249 valors per a cadascun de F1, F2 i F3. Són punts de mesura sensibles a la coarticulació, el micròfon i la segmentació; serveixen per prioritzar l'audició, no per validar encara un sistema vocàlic.
La taula `proveniencia/analisi-trajectories-formants.tsv` conserva cinc punts temporals per token (1.250 files) i permet comparar la direcció instrumental entre inici i final; continua sense substituir la revisió auditiva.
La nova evidència textual `proveniencia/evidencia-gramatica.tsv` localitza 10.458 contextos candidats en nou categories, però distingeix explícitament els pronoms ambigus i les perífrasis aparents: cal escoltar-los abans de convertir-los en trets.
La matriu ampliada `grafo/matriu-formes-linguistics.tsv` desplega els 284 trets en 18.744 cel·les persona-forma; la matriu original de 2.310 cel·les es conserva per comparar amb la primera versió del repertori.
La tercera descodificació greedy dels 109 clips forts deixa 81 casos de triple coincidència, 24 de doble i 4 de coincidència única; les divergències queden a `proveniencia/informe-forts-greedy.md` per escoltar-les primer.
La tokenització small de la cua completa recupera 20 formes en 63 veus actives; la capa separada del graf suma 1.140 parelles amb almenys tres formes compartides, sempre com a semblança textual pendent d'audició.

La passada greedy completa permet una vista encara més estricta: `grafo/trets-triple-full.tsv`, `arestes-parlants-triple-full.tsv` i `matriu-formes-triple-full.tsv` conserven només els 206 clips amb coincidència en els tres models. El resultat és de 19 formes, 106 arestes amb almenys tres formes compartides i 1.140 cel·les persona-forma. Aquesta reducció serveix per ordenar la revisió; no converteix el triple ASR en evidència dialectal.

La taula proveniencia/analisi-linguistica.tsv amplia els 20 marcadors del graf amb clítics, perífrasis, repeticions i lèxic territorial per a les 66 veus; tots els recomptes continuen sent candidats ASR fins a l'audició.

L'inventari `proveniencia/inventari-incerteses-asr.tsv` reuneix 13.390 segments amb algun token per sota de p=0,55 i n'enllaça 1.283 amb clips de formes. Aquesta cua fa visibles possibles errors de transcripció i variants per comprovar, sense tractar-les com a trets dialectals.

## Lectura lingüística actual

- Hay una base común de conectores de explicación, consecuencia y reformulación
  (`perquè`, `doncs`, `clar`, `llavors`, `és a dir`, `o sigui`, `vull dir`).
- `bueno`, `a veure`, `aviam` y `diguem` forman un segundo grupo de marcadores
  conversacionales, sensible a la situación comunicativa y a la edición de las
  entrevistas.
- El material institucional sobrerrepresenta registros expositivos y políticos;
  no permite todavía comparar de forma equilibrada edad, parroquia, género,
  lengua primera o conversación espontánea.
- Les mètriques ASR situen el ritme aparent entre 91,5 i 229,5 paraules/minut
  (mediana 143,2) i la pausa estimada entre 0 i 11,4% de l'extensió. Són rangs
  de selecció per a l'escolta, no mesures fonètiques validades.
- La detecció acústica a -35 dB troba una pausa mediana de 0,52 s i una suma
  mediana de 161,3 s per mostra. Pot incloure soroll de fons, música o edició;
  es conserva com a senyal per auditar, no com a silenci conversacional definitiu.
- `proveniencia/analisi-prosodia.tsv` conserva una lectura acústica orientativa de
  les 66 mostres: proporció d'activitat, energia, creuaments per zero i F0 espectral
  estimada. Els valors s'han de contrastar amb fragments escoltats perquè poden
  recollir música, soroll, edició o harmònics.
- Las transcripciones no permiten resolver vocales, acento, /r/, palatalización,
  ritmo ni entonación. Esos rasgos requieren fragmentos auditados y anotación
  acústica manual.

## Próxima revisión

La base ya alcanza el mínimo de 50 personas, pero el corpus no se considera
cerrado como recurso lingüístico validado. La siguiente pasada debe seleccionar
fragmentos por forma, auditar las palabras de baja confianza, separar voces de
entrevistador y documentar biografía lingüística y lugar de socialización cuando
la fuente lo permita. Solo después se podrá convertir una arista provisional en
un rasgo comparado.

La fitxa `proveniencia/context-persones.tsv` documenta el context institucional o etnogràfic dels 60 parlants canònics i manté separat el que és identificació territorial del que encara no sabem sobre la seva socialització lingüística; en el cas de Carles Sasplugas, la correspondència entre el nom abreujat del vídeo i el nom complet del registre municipal queda marcada com a compatible però no verificada.

La referència de RTVA sobre l'estudi de Sílvia Rovira recorda que una comparació fonètica vàlida ha de separar edat i parròquia: descriu més de 70 entrevistes i el contrast de vocals obertes/tancades, però no aporta els àudios al nostre paquet.

## Capa completa de 35 formes

La vista `README-formes-completa.md` amplia la primera capa de 20 marcadors i
reagrupa els 66 registres en **60 persones canòniques**. La seva matriu té
**2.100 cel·les** (60 × 35) i el fitxer `arestes-parlants-formes-completa.tsv`
conserva **1.690 parelles** que comparteixen almenys tres formes segons l'ASR.
La vista Mermaid només dibuixa les connexions amb cinc formes o més per mantenir
el gràfic llegible. Aquesta capa no reemplaça les vistes de consens: inclou
recomptes ASR de totes les formes candidates i, per tant, continua pendent de
confirmació auditiva.

## Candidats fora del recompte canònic

`proveniencia/candidats/lead-rtva-001/` conserva Joan Verdú amb dues passades
ASR, 10 clips i un graf provisional de 11 formes, 54 connexions i 61 nodes.
`proveniencia/candidats/lead-rtva-002-ian-moya/` conserva Ian Moya amb MP3 i WAV
locals, 470 segments small, 494 base, 35 formes candidates, 15 clips i un graf
provisional de 14 formes, 60 connexions i 61 nodes. En tots dos casos les
connexions són textuals; la mescla amb l'entrevistador impedeix incorporar-los
encara a `persones.tsv`.

`proveniencia/candidats/lead-rtva-003-dj-neura/` conserva una entrevista d'àudio
RTVA amb 142 segments small, 189 base, 35 formes candidates, 10 clips i un graf
provisional de 8 formes, 60 connexions i 61 nodes. La seva segmentació textual
separa 36 segments `dj-neura-probable`, 21 de l'entrevistador i 85
indeterminats; també queda fora del recompte fins a l'audició.

La tercera passada greedy dona 3 dobles, 2 d'un sol model i 5 sense coincidència
en els 10 clips de DJ Neura; és una priorització ASR conservada a `qa-greedy.tsv`.

La segmentació provisional d'Ian separa 89 segments `ian-probable`, 92 de
l'entrevistador, un segment mixt i 288 indeterminats. És una cua per escoltar,
no una diarització.

La tercera passada greedy dels 15 clips d'Ian dona 2 triples, 1 doble, 7 d'un
sol model i 5 sense coincidència; també continua pendent d'audició.

La prospecció ha localitzat vuit veus de l'Arxiu d'Etnografia d'Andorra amb
trajectòries rurals o històriques especialment valuoses. Josep Casal, Rosa Vidal,
Pere Torres i Trini Mandicó Baró, i les sis veus del Consell Constituent pa-055—pa-060 i sis veus de RTVA pa-061—pa-066, s'han incorporat com pa-051—pa-066; quatre
peces individuals o mixtes es conserven a `fonts-pendents.tsv` perquè els
termes del fons permeten recerca però restringeixen la reproducció.


## Decisió de fase

Amb 66 veus individuals i quatre peces de l'Arxiu d'Etnografia, la captura inicial ja compleix l'objectiu de 50–100 persones i es pot tancar com a fase de recol·lecció. No es tanca encara el recurs lingüístic: la fase següent és l'auditoria auditiva i fonètica dels intervals prioritzats.


## Quart candidat RTVA: Joan Micó

`proveniencia/candidats/lead-rtva-004-joan-mico/` conserva una entrevista a Joan Micó amb àudio local, dues passades ASR, informe per formes, 12 clips i graf provisional separat (12 formes consensuals, 60 connexions i 61 nodes). La segmentació textual proposa 49 segments de Joan, 66 de l'entrevistador i 222 indeterminats o mixtos; aquestes etiquetes són només una cua d'audició.

La tercera passada greedy classifica els 12 clips en 1 triple, 1 doble, 6 d'un sol model i 4 sense coincidència. El candidat queda fora del recompte canònic i de qualsevol afirmació dialectal fins a confirmar veu, transcripció i termes d'ús.


## Cinquè candidat: Xavier Espot (Consell General)

`proveniencia/candidats/lead-cg-001-xavier-espot/` conserva un extracte inicial de 120 segons del discurs-programa del Consell General, dues passades ASR, 4 clips i un graf provisional de 3 formes, 37 connexions i 61 nodes. La font completa dura aproximadament 81 minuts; l'extracte es manté separat per no atribuir automàticament tota la sessió a una sola veu.

La tercera passada greedy dona 2 triples, 1 doble i 1 d'un sol model. El candidat queda fora del recompte canònic fins a confirmar l'atribució auditiva i els termes d'ús.
