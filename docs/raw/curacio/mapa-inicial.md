# Mapa inicial de curació del corpus Maia

Recompte de base observat el 2026-09-24, abans de crear els fitxers de
`docs/raw/curacio/`. Els nombres són fitxers, no afirmacions sobre qualitat,
cobertura efectiva, exactitud ni dret de reutilització.

## Inventari per àrea

| Àrea | Fitxers | Rol inicial |
| --- | ---: | --- |
| `docs/temes/` | 1.476 | Lectures compilades per tema; 1.347 articles i 129 índexs segons el recompte de tancament anterior |
| `docs/fonts/` | 619 | Registres de font i peces de context; cal separar fitxes de font d'articles |
| `docs/parla/` | 45 | Corpus oral i audiovisual; 40 registres i 5 índexs |
| `docs/raw/` | 23.429 | Evidència primària, captures, OCR, derivats tècnics, registres i materials encara no seleccionats; exclou els fitxers administratius de `curacio/` |
| `docs/_exemples/` | 1 | Exemples de format |

`docs/raw/` ocupa 36.669.302.412 bytes de mida lògica (36,67 GB decimals; `du -sh` mostra aproximadament 34 GiB assignats). La mostra d'extensions és heterogènia: text, HTML, JSON, PDF, àudio, vídeo, subtítols, codi i imatges. Cal inventariar els fitxers, però classificar-los per rol i grup de font abans de tractar-los com a unitats de coneixement. Els índexs, captures, còpies duplicades i fitxers tècnics no són automàticament material d'entrenament.

## Dominis editorials de `temes/`

| Domini | Fitxers |
| --- | ---: |
| institucions | 350 |
| esports | 280 |
| història | 241 |
| societat | 155 |
| economia | 104 |
| cultura | 83 |
| territori | 65 |
| llengua | 56 |
| persones | 44 |
| costums | 34 |
| política | 24 |
| gastronomia | 22 |
| vida quotidiana | 18 |

Els recomptes són totals per subcarpeta principal i inclouen índexs; no són una puntuació de cobertura ni de prioritat.

## Prioritat i primera tanda

La primera tanda és l'auditoria de [`l'ajut per desocupació involuntària`](../../temes/societat/treball/lajut-per-desocupacio-involuntaria.md) i les fonts que sostenen les seves afirmacions. És un tema de drets i prestacions en què confondre una font absent amb una prestació inexistent pot produir un negatiu fals. El text existent ja separa versions temporals i acaba amb `Buits registrats`; la feina inicial és comprovar aquests registres, no reescriure'l des de zero.

### Fonts i límits

- Els textos normatius directes del BOPA tenen una fitxa pròpia amb les condicions generals documentades; no s'ha d'estendre aquesta autorització a allotjadors ni a fonts citades diferents.
- El Portal jurídic permet consulta gratuïta de textos consolidats, però el seu avís legal reserva els drets i limita l'ús a l'àmbit personal; no s'hi ha trobat permís de redistribució. La seva fitxa queda `pendent` d'autorització.
- Les còpies locals sota `docs/raw/desocupacio/` són evidència fora del corpus. Un derivat només pot entrar a `final-corpus/` si totes les fonts que l'han originat tenen condicions compatibles i la unitat supera la revisió factual.
- L'article actual conserva buits sobre pràctica administrativa i judicial, tractats de frontera, casos individuals i algun càlcul geogràfic o aritmètic. No s'han de convertir en afirmacions positives o negatives sense nova font.

## Resultat de l'inventari inicial

La fotografia immutable de l'inventari inicial conté 25.584 fitxers o enllaços
simbòlics. La classificació provisional v1 els comptava com a 20.592 pendents i
4.992 exclosos perquè encara no distingia les unitats no revisades. La
classificació actual manté per a les 25.584 unitats inicials 883 no
revisades, catorze aprovades, 498 pendents i 24.189 excloses. La vista viva
suma 22 unitats posteriors: una unitat de contingut pendent i 21 fitxes,
captures o registres tècnics exclosos per rol. El recompte viu és
883 no revisades, catorze aprovades, 499 pendents i 24.210 excloses. De les 498
pendents inicials, 160 són
articles que declaren les actes històriques
del Consell com a font: la seva elegibilitat de redistribució no està resolta i
no se n'ha fet encara la revisió factual. Una unitat posterior és pendent per
revisió de drets i contingut, no només per canvi d'hash. Un article sobre les
parròquies queda pendent perquè integra fonts no redistribuïbles. Deu fitxes
de prospecció oral `pa-041.md`–`pa-050.md` tenen
frontmatter mal format i queden pendents; no s'han reescrit perquè pertanyen a
una tanda preexistent. La vista viva detecta fitxers modificats després de congelar l'abast; els canvis
d'hash no aproven contingut automàticament.

La cinquena unitat del pilot, «Contacte de llengües», queda pendent: la font IEC citada tracta de lexicografia, no acredita les afirmacions sobre usos lingüístics, i les dades i la llicència de redistribució continuen sense verificar.

La setena unitat del pilot, la transcripció de la càpsula #49 amb Esther Jover, queda pendent: no hi ha àudio local escoltat i no s'ha acreditat la varietat andorrana de la ponent. La metadada de YouTube confirma CC BY per a aquest vídeo, però no resol la fidelitat de la transcripció; la durada registrada (9:48) discrepa del material de partida (9:49).

La vuitena unitat del pilot, «El superàvit que finança habitatge i hospital»,
s'ha aprovat després de contrastar els articles 1–6 i la disposició final
quarta de la Llei 10/2026 amb el text BOPA i recalcular els imports. S'han
netejat els buits antics ratllats i retirat referències derivades de materials
del Govern amb redistribució no acreditada. L'exportació es limita al text
normatiu del BOPA, reutilitzable amb les condicions documentades. No afirma
execució ni lliuraments, i registra com a buits la liquidació, les
redistribucions, l'inventari d'habitatge i la vigència consolidada no
verificats.

Una tanda de drets classifica vint articles declarats sota `premsa-andorrana`
com a pendents: la fitxa registra drets reservats i no autoritza redistribució;
dinou articles no identifiquen el mitjà i cap dels vint dona data, titular ni
enllaç a la peça. No s'ha revisat factualment cap dels vint. El registre és a
`rights-premsa-01.md`.

La tanda `nationality-skiers-01` afegeix 26 biografies d'esquiadors a `pending`: la categoria de Viquipèdia i el codi FIS `AND` no acrediten ciutadania civil. No s'ha revisat la resta de les biografies ni s'han incorporat dades de FIS, que declara tots els drets reservats. Informe: `revisio-ciutadania-esquiadors-01.md`.

La revisió `law-strike-01` ha aprovat una síntesi dels articles 2, 7–13 i 21 de la Llei 33/2018 i 3, 11 i 12 de la Llei 32/2018, contrastada amb els originals del BOPA i les instantànies consolidades del 12-09-2026. S’hi ha afegit la clàusula per a altres activitats públiques indispensables i inajornables i retirat l’extrapolació que gairebé tota l’economia queda coberta. La fila corresponent de la cronologia de protestes estava datada erròniament el 2022; s’ha retirat de la cronologia i l’article sencer continua pendent. Informe: `revisio-dret-vaga-01.md`.

Una tanda de drets afegeix nou articles històrics a pendents perquè declaren
un relat terciari d'historia.ad amb drets reservats i sense llicència oberta.
No s'han revisat factualment; el resum és a `rights-historia-ad-01.md`.

Les tandes `rights-brutails-01` a `rights-brutails-04` han posat 161 articles
atribuïts a *La Coutume d'Andorre* en pendents per l'elegibilitat de la còpia
OCR i els termes de reutilització. No són aprovacions ni revisions factuals;
els informes individuals documenten hashes i localitzadors. La revisió del
registre d'entitats religioses ha corregit tres articles amb la Llei 2/2025 i
la Constitució com a fonts: el llindar de vint persones és per constituir una
entitat religiosa sense ànim de lucre, no per a l'existència d'una religió; el
registre és públic amb el procediment d'accés previst a la llei. Les tres
unitats segueixen pendents de revisió completa i elegibilitat de totes les
fonts. Informe: `revisio-registre-entitats-01.md`.

La novena unitat, «Res d'anterior al 1984 no es tria», queda pendent. La cadena
BOPA mostra que el decret que contenia la regla va ser derogat i que les normes
successores no la reprodueixen explícitament; falta determinar si la regla
continua vigent per una altra disposició. També cal verificar dues afirmacions
que depenen de cerques no sistemàtiques i retirar la navegació `Related` abans
d'una exportació.

La desena unitat, «El terreny sense classificar i les allaus», s'ha aprovat
per a coneixement després de contrastar els decrets BOPA de 2012, 2016 i 2023.
S'han retirat comparacions derivades de fonts sense redistribució acreditada i
notes ratllades. El text explica les regles publicades però no declara vigència
consolidada ni classifica parcel·les; cartografia, Cadastre d'allaus i PIDA
continuen sense consultar-se.

L'onzena unitat, «Quan un bosc protegeix un edifici», s'ha aprovat després de
contrastar els articles 6, 7, 13, 21, 28 i 33 i l'annex V del Reglament
d'allaus de 2016. S'han retirat marques de treball i una ampliació normativa
no necessària; el text no afirma compliment de les obligacions en casos concrets
ni vigència consolidada.

La dotzena unitat, «La flexibilització de la desocupació el 2021», s'ha
aprovat com a coneixement històric després de contrastar tres textos del BOPA.
La comparació registra canvis de terminis i cotitzacions, la transició dels
expedients pendents i el còmput de períodes del règim d'esquí derogat. S'han
retirat notes ratllades i una remissió a una lectura més àmplia; l'aplicació
real i els expedients continuen sense verificar-se.

La tretzena unitat, «Abans ho decretava el Govern», queda pendent de revisió
factual: tretze edictes de 2021–2022, que formen el gruix de la sèrie analitzada,
només s'han llegit per la capçalera. Això no sosté els recomptes de fórmules,
taules ni dates que presenta l'article. Els termes BOPA permeten redistribució;
el bloqueig és de verificació del contingut. L'article també conserva una
secció `Related` que s'ha de retirar abans d'una eventual exportació.

La catorzena unitat, «Les guarderies», queda pendent abans de revisió factual
completa: una part de les afirmacions de cobertura actual depèn del llistat de
guarderies del Registre Nacional de Serveis Socials i Sociosanitaris. El llistat
no tenia fitxa de procedència ni llicència oberta identificada; l'avís legal del
Govern reserva reproducció, tractament i distribució sense consentiment previ i
escrit. S'han guardat l'avís i una fitxa de font; l'article no s'exporta mentre
no es resolgui l'elegibilitat d'aquesta font. No s'han donat per contrastats els
requisits legals, les ràtios ni les xifres de l'article.

La quinzena unitat, «El Tribunal de Comptes», queda pendent de revisió factual
completa. La comparació amb el text refós de 2017 ha corregit l'interval legal
de membres i la renovabilitat dels mandats; també s'ha tret una inferència no
sostinguda sobre qui finança el Tribunal. La pàgina oficial d'informes mostra
una memòria del 2025, però els informes no s'han revisat i l'avís legal limita
l'ús a l'àmbit personal i reserva els drets. La designació del 2021 es presenta
com a històrica; la composició actual no s'infereix dels edictes antics.

El pilot 01 s'ha tancat amb vint unitats classificades: vuit aprovades i dotze
pendents, sense revisió humana. La setzena unitat, sobre l'accés a l'Arxiu
Nacional, queda pendent per una discrepància entre el Decret de 2016 i la pàgina
actual del Govern, i per la compatibilitat jurídica i els termes de reutilització
encara no resolts. La dissetena, sobre les llistes de consellers del període
constituent, s'ha corregit perquè no es presenti com la nòmina de qui va aprovar
la Constitució: les sessions llistades són d'altres dates i la síntesi té drets
reservats. La divuitena, una transcripció d'entrevista, queda pendent per drets
i àudio sense verificar. La dinovena, sobre la Llei de transparència, tenia un
buit fals que s'ha corregit: el text BOPA de l'article 12 era disponible, però
la resta de les afirmacions encara requereix contrast complet i vigència actual.
La vintena, sobre el contrapàs, ja era pendent en la tanda de drets de premsa;
la referència no identifica cap peça periodística concreta.

La tanda `rights-rios-urruti-01` afegeix 13 articles a `pending`: la fitxa de la
font no declara llicència ni estat de drets de l’ítem digital. No se n’ha fet
revisió factual ni editorial. Informe i hashes: `rights-rios-urruti-01.md`.

La tanda `rights-constituent-youtube-01` afegeix 26 unitats a `pending`: el
canal del Consell General registra llicència estàndard de YouTube i no declara
llicència oberta. No s’han revisat factualment ni s’han escoltat les entrevistes
completes. Informe i hashes: `rights-constituent-youtube-01.md`.

La primera tanda posterior al pilot cobreix cinquanta perfils d'esportistes que
declaren la fitxa de Viquipèdia en anglès. S'ha aparellat cada article amb el
bolcat local corresponent i registrat una decisió pendent per unitat; no s'han
verificat els fets amb fonts federatives o olímpiques. La categoria d'Andorran
sportspeople no prova per si sola nacionalitat andorrana, com il·lustra el perfil
de Cyril Despres, que el bolcat descriu com a francès i competidor per França.
La llicència CC BY-SA 4.0 permet redistribució sota condicions, però no acredita
els fets ni l'etiqueta nacional.

La tanda `demografia-44-pobles-01` ha aprovat la revisió de les 44 sèries
d'Andorra de la captura API del 18-09-2026. S'ha corregit el rànquing de
multiplicadors, explicitat el llindar de població inicial i separat el canvi
observat de les seves possibles causes. La fitxa de font ara inclou l'API i
enllaça la procedència i les condicions de la captura. Informe i hashes:
`demografia-44-pobles-01.md`.

L'inventari és un punt de partida, no un conjunt aprovat per entrenar. Onze
unitats s'han aprovat per a coneixement i exportat des de `docs/temes/`: dues
lectures estadístiques sobre població, una lectura històrica de l'ajut d'esquí
de 2020, una lectura de la flexibilització de la desocupació de 2021, una
síntesi de la sentència constitucional 2026-25-RE, una lectura de
l'estructura del Consell General, una lectura de la Llei 10/2026 sobre
habitatge i sistema sociosanitari, dues lectures dels decrets d'allaus, una
lectura històrica del barem patrimonial dels ajuts i una síntesi de les lleis
de 2018 sobre vaga i acció sindical. El manifest registra hashes, fonts,
termes i abast de revisió; no hi ha hagut revisió humana. El borrador jurídic
separat sobre l'article 26.4.i–j del BOPA de 2020 continua pendent perquè cita
una presentació no redistribuïble. El document més ampli sobre la prestació
també roman pendent perquè integra fonts i buits de més d'una mena. La quarta
unitat del pilot, la síntesi de la queixa ASC-3494 de 1528, queda pendent:
les metadades estan contrastades, però l'autorització per redistribuir la
síntesi en un corpus d'entrenament no està determinada.

L'error YAML cau al camp de frontmatter 2: fitxers `pa-041`–`pa-043`, columna
27; `pa-044`–`pa-050`, columna 23. Aquestes són ubicacions de validació del
frontmatter, no cites a l'evidència de coneixement.

## Seqüència de curació

1. Auditar una unitat editorial completa i els seus enllaços a fitxers primaris.
2. Confirmar per font titular, data, peça exacta, termes i redistribució.
3. Verificar que cada afirmació material té una cita a article, disposició, pàgina o altra peça exacta; separar declaracions de fets observats.
4. Conservar els buits i les contradiccions al final de l'article.
5. Seleccionar només les unitats netes i autoritzades a `final-corpus/`, amb manifest que registra la versió i el hash de cada peça.
6. Repetir per tandes de tema/família de fonts. No estimar la qualitat del corpus pel nombre d'arxius incorporats.

La tanda `demografia-serie-padro-01` ha revisat la població registrada (1947–2025), els recomptes de naixements i defuncions i el saldo migratori publicat (2016–2025). S'han corregit els períodes de les baixades, retirat causes especulatives i substituït un saldo migratori calculat que no concordava sempre amb el publicat. Informe: `revisio-serie-padro-01.md`.

La revisió `demografia-edat-nacionalitat-review-01` ha aprovat l’article d’edat, sexe i nacionalitat després de verificar les divisions 1100, 1098 i 1099. S’han retirat causalitats no mesurades i corregit el límit d’edat: la sèrie anual acaba en `99 anys o més`. Informes: `demografia-edat-nacionalitat-pending-01.md` i `revisio-edat-nacionalitat-01.md`.

La tanda `tabac-serie-01` aprova una lectura de la producció anual de tabac
(1973–2025) després de contrastar totes les files de les divisions 2404 i
2405 i les pàgines 1, 3–5 de la nota A107. Es registren set diferències entre
sumes parroquials i totals, una errada al text de la nota i la divergència de
dos kg del gràfic. Se n'han retirat afirmacions dependents d'una font
governamental amb redistribució no acreditada. Informe i renders: `revisio-produccio-tabac-01.md` i `a107-review/`.

S'ha reprès la prioritat inicial, l'ajut per desocupació involuntària. La
captura API conté els onze anys 2015–2025; la taula s'ha completat. S'han
corregit el rànquing mensual de desembre, la lectura del desglossament per edat
de l'A052 i el recompte de persones explícitament ocupades. La revisió inicial
de la cadena jurídica ha trobat que el Decret 44/2021 sí que va flexibilitzar
temporalment parts de l'article 26. Els resultats agregats A052 es poden
redistribuir amb atribució segons l'article 21.2 de les lleis 13/2022 i
27/2025; això no inclou els registres administratius subjacents. La publicació
oficial de 2025 compta 62 sol·licituds, tres de les quals no resoltes; la
captura API en compta 59, que corresponen a les 31 favorables i 28
desfavorables. La causa de la discrepància no està documentada. La unitat
continua pendent per la confrontació integral de les afirmacions jurídiques i
estadístiques. Informe:
`revisio-ajut-desocupacio-en-curs-01.md`.
