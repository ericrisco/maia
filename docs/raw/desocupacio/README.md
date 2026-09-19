# Ajut per desocupació — reglament

La tanda inicial conserva quatre textos del BOPA i un consolidat. S'hi han
afegit el decret de desembre de 2020 i material de contrast de la CASS i del
Consell General, amb condicions diferenciades a l'apartat d'ampliació.

## Procedència

| | |
| --- | --- |
| **Font** | [BOPA](https://www.bopa.ad/) · Servei del Butlletí Oficial del Principat d'Andorra |
| **Titular** | Govern d'Andorra |
| **Condicions** | [avís legal del BOPA](https://www.bopa.ad/AvisLegal), copiat sencer a `bopa-avis-legal.txt` |
| **Redistribució** | **sí**, amb el sentit i les metadades de data preservades |
| **Data de consulta** | 2026-09-13 |
| **Fitxa de font del corpus** | [`bopa-ad`](../../fonts/bopa-ad.md) |

La font es va registrar com a pendent **abans** d'obrir el BOPA. L'avís legal
es va llegir després d'obrir la primera norma i **abans de desar els textos**;
se'n guarda una còpia perquè la data de consulta sola no demostra què deien
les condicions d'ús.

**El BOPA no patrocina ni dona suport a aquest projecte.** L'avís ho prohibeix
expressament i queda dit.

## Els fitxers

| Fitxer | Què és | Procedència |
| --- | --- | --- |
| `bopa-2020-10-07-reglament.txt` | Decret del 7-10-2020, Reglament de les prestacions econòmiques dels serveis socials i sociosanitaris. **BOPA núm. 121, 14-10-2020.** L'article 26 és l'ajut per desocupació involuntària | BOPA |
| `bopa-2021-03-03-errata.txt` | Correcció d'errata del 3-3-2021 sobre la disposició derogatòria del decret anterior. **BOPA núm. 30, 03-03-2021** | BOPA |
| `bopa-2021-44-flexibilitzacio.txt` | **Decret 44/2021, del 17-2-2021**, de flexibilització parcial i temporal dels requisits de l'ajut per desocupació. **BOPA núm. 24, 18-02-2021** | BOPA |
| `bopa-avis-legal.txt` | Les condicions de reutilització, copiades el dia de la consulta | BOPA |
| `jurisprudencia-reglament-2020-consolidat-2026-09-13.txt` | El mateix Reglament en **text consolidat**, 50 articles, **10 versions**. Consulta del 2026-09-13 | [Jurisprudència.ad](../../fonts/jurisprudencia-ad.md) |

Cada fitxer comença amb `FORA_DEL_CORPUS`, l'URL, la data de consulta i —els del
BOPA— la data de publicació i l'enllaç a les condicions. **L'extracció és el text
dels paràgrafs del DOM**, amb els salts de paràgraf preservats.

**El fitxer consolidat no és del BOPA i no es regeix pel seu avís legal**: és de
Jurisprudència.ad, que hi aporta la consolidació. La seva fitxa de font recull
les condicions pròpies.

## Això no és text consolidat

`docs/raw/lleis/` conté text **consolidat**: la suma de totes les modificacions.
**Els quatre fitxers del BOPA d'aquesta carpeta, no.** Són **el que es va
publicar el dia que es va publicar**, i prou. El cinquè fitxer sí que és
consolidat, i hi és precisament per poder comparar-los.

La diferència no és menor. El mateix decret diu a l'exposició de motius que
renumera tots els apartats de l'article 26 respecte de la versió del 2019: les
lletres d'un requisit **no són estables entre versions**. I l'errata del 2021
demostra que el text del 2020 tenia un defecte que va trigar cinc mesos a
corregir-se.

> **Cap afirmació treta d'aquesta carpeta no demostra que la norma sigui vigent
> avui.** El consolidat compta **10 versions** del Reglament però **no en dona
> ni la data de publicació ni la referència BOPA** —hi consten com a «absent del
> corpus»—, de manera que **no se sap quines versions són ni quina és l'última**.
> El que la comparació sí que permet dir és una cosa més estreta: **que
> l'article 26 coincideix paraula per paraula entre el text del 2020 i el
> consolidat del 2026-09-13**.

## Related

- [El material de partida](../README.md)
- [La legislació consolidada](../lleis/README.md)

## Ampliació del 13-09-2026 — desembre de 2020 i resposta parlamentària

- [Text directe del BOPA del 16-12-2020](bopa-2020-12-16-decret.txt):
  `GD20201216_12_15_46`, BOPA 150 del 17-12-2020. Afegeix l'article 26 bis.
  Mateixes condicions del BOPA verificades; base de la nova lectura del corpus.
- [Còpia del decret allotjada a la CASS](bopa-2020-12-16-copia-cass.pdf) i
  [extracció amb pàgines](bopa-2020-12-16-copia-cass.txt): cinc pàgines llegides
  i inspeccionades amb els renders `bopa-2020-12-16-pagina-1.png` fins al 5.
  La llicència del portal CASS no és oberta; aquests fitxers romanen fora dels
  datasets. La lectura publicada cita l'exemplar directe del BOPA.
- [BCG 23/2021](bcg-2021-23.pdf) i [extracció de pàgines 33–35](bcg-2021-23-p33-35.txt):
  resposta del Govern reg. 83, signada el 09-03-2021, publicada el 10-03-2021.
  Unitat llegida i inspeccionada als renders de pàgines 33–35. La resta del
  butlletí no s'ha llegit. **Drets de la peça pendents: no datasets.**
  La continuació incorpora una
  [lectura de recerca](../../temes/institucions/consell-general/la-resposta-sobre-lajut-de-lesqui.md)
  també exclosa de datasets, distingint declaració i aplicació acreditada;
  no suposa haver resolt els drets que inicialment n'havien ajornat la lectura.

Els dos PDFs i els renders són còpies de consulta; la seva presència aquí
no constitueix una autorització per redistribuir-los. Les condicions del
BOPA no s'estenen automàticament als altres publicadors.

## Ampliació — barem patrimonial, originals contrastats

Condicions BOPA registrades abans de les consultes. Els PDF i els renders
són evidència fora del corpus; cap exportació de dataset ni reutilització
gràfica. Els nous `.txt` provenen de `pdftotext -layout`, amb capçalera i
salts de pàgina, a diferència dels extractes HTML inicials.

- [Reglament de 2020, PDF de 30 pàgines](bopa-reglament-2020-original.pdf)
  i [text](bopa-reglament-2020-original.txt): nova lectura de pàgines 2,
  11–12 i inici de 13; renders 11–12 vistos. L'article 14 s'ha llegit
  complet i el 14.1.a.i s'ha contrastat amb l'original visual.
- [Llei 6/2014, PDF BOPA allotjat al Consell](bopa-llei6-2014-original.pdf)
  i [text](bopa-llei6-2014-original.txt): 27 pàgines conservades, només
  pàgines PDF 3–4 i 15–16 llegides i renders vistos. Destil·lació limitada
  a les definicions 2.m i 2.o i al contrast del barem de l'article 32.
- [Llei 5/2018, PDF BOPA allotjat al Consell](bopa-llei5-2018-original.pdf)
  i [text](bopa-llei5-2018-original.txt): dues pàgines llegides completes i
  inspeccionades. Preàmbul i article únic destil·lats selectivament;
  finals llegides sense destil·lació. Els dos antecedents de 2017
  s'han contrastat en la continuació següent.

La [lectura del barem](../../temes/societat/treball/el-barem-patrimonial-i-els-ajuts.md)
no certifica la vigència de 2026. La còpia del Consell reprodueix el BOPA:
no és una segona font independent del text normatiu.

## Continuació — llei i decret de 2017

- [Llei 3/2017 original](bopa-llei3-2017-original.pdf) i
  [text](bopa-llei3-2017-original.txt): BOPA14,28-02-2017,82 pàgines.
  Capçalera i p.1, final cinquena p.23 i final vuitena p.30 llegides,
  amb fragments adjacents; renders1,23,30 vistos. No tota la llei llegida.
  Còpia del BOPA allotjada al Consell, mateix publicador normatiu.
- [Decret del 26-04-2017](bopa-decret-2017-04-26-original.pdf) i
  [text](bopa-decret-2017-04-26-original.txt): BOPA27,03-05-2017,
  GR20170427_11_17_25. Dues pàgines completes llegides i renders vistos.
  Localitzat al cercador públic BOPA per «prestacions econòmiques»;
  la consulta prèvia «26-4-2017» no mostrava aquesta peça entre els
  resultats examinats. No s'ha deduït absència de norma.

Les redaccions separades de febrer i cumulativa d'abril es preserven.
També es registra la data19febrer impresa al preàmbul2018 enfront del
9febrer de l'original2017. La lectura actualitza el buit antic, sense
resoldre'n l'aplicació administrativa ni certificar la vigència2026.

## Continuació — antecedents i errata de 2016

Condicions BOPA registrades abans de consulta. PDF oberts des dels botons
de les fitxes públiques i conservats amb extractes i renders fora del corpus.

- [Llei 2/2016](bopa-llei2-2016-original.pdf) i
  [text](bopa-llei2-2016-original.txt): BOPA20,31-03-2016,88 pàgines.
  Final7 p.30–31 i final9 p.31 llegides, amb renders30–31 vistos.
  El canvi literal de superar100 a igualar100 queda documentat; no es
  deriva una interpretació sobre els patrimonis de més de100 punts.
- [Reglament18-05-2016](bopa-reglament-2016-original.pdf) i
  [text](bopa-reglament-2016-original.txt): BOPA32,25-05-2016,19 pàgines.
  Text p.3–4 llegit; article5.2.a.iii complet i render4 contrastats.
  Informes immobiliaris ja exigits; el segon guió encara diu vehicles.
  No tot l'article5 ni tot el reglament llegits.
- [Errata31-08-2016](bopa-errata-2016-08-31.pdf) i
  [text](bopa-errata-2016-08-31.txt): BOPA50,07-09-2016,una pàgina
  completa i render vistos. Afecta15.2.a.ii; context íntegre15 no llegit.

La lectura del barem tanca aquests buits de lectura, però manté oberts
els d'aplicació, eventuals correccions i versions posteriors.

## Continuació — debat parlamentari de 2018

[DCG7/2018,PDF](dcg-2018-7.pdf) i [text](dcg-2018-7.txt):60 pàgines
conservades; punt3 complet llegit des de l'obertura p.27 fins a
l'aprovació p.36. Renders28,30,33,35,36 vistos; altres punts del diari
no llegits íntegrament. Parts veïnes dels punts2 i4 fora de la unitat.

[Fitxa pròpia](../../fonts/consell-general-dcg-2018-7.md), amb drets
pendents: originals, renders i lectura compilada exclosos de datasets.
No s'estenen les condicions BOPA al Diari del Consell. La
[lectura del debat](../../temes/institucions/consell-general/el-debat-sobre-el-calcul-patrimonial-de-2018.md)
atribueix posicions i votació; no valida amb elles els expedients ni
les xifres de resultats esmentades pels oradors.

## Continuació — informes de ponència i comissió de 2018

[BCG 21/2018, PDF](bcg-2018-21.pdf) i [text](bcg-2018-21.txt):
vuit pàgines, text complet llegit. Informes p. 2–6; renders 3–6 vistos.
L'extracció de l'esmena 4 conserva ratllades com si fossin text corrent:
la imatge de p. 4 permet separar proposta i supressions.

[Fitxa de drets pendents](../../fonts/consell-general-bcg-2018-21.md).
Originals, renders i lectura exclosos de datasets. La lectura del debat
ara contrasta les tres esmenes liberals no aprovades i la de Bonet
retirada. Actes de reunions, casos d'embargament i objecció atribuïda
a Sindicatura continuen sense documents originals contrastats.

## Continuació — recompte i cost de pensions APAP 2016–2017

[Memòria 2017, PDF](govern-apap-2017.pdf) i [text](govern-apap-2017.txt):
26 pàgines; portada22-05-2018. Llegits els apartats complets p.16–17
(discapacitat) i24–25(gent gran), amb renders respectius vistos. Portada,
p.2 i veïnes15,18,23,26 llegides en text; resta pendent. El gràfic25
no s'extreu amb pdftotext: valors754 i798 comprovats visualment.

[Notícia sobre la memòria2016, text](govern-apap-2016-noticia.txt) i
[HTML](govern-apap-2016-noticia.html): cos complet llegit, publicació
24-04-2017. Enllaç original a la capçalera del text. Cerques al Govern
per «2016 APAP memòria», «2016 754 solidaritat» i memòria PDF van trobar
la notícia i la memòria2017, sense localitzar la memòria2016 entre els
resultats examinats. L'enllaç /documents/ de la notícia és la imatge
og:image; no s'ha descarregat com si fos una memòria.

[Fitxa pròpia](../../fonts/govern-apap-2017.md), drets pendents
d'autorització específica: evidència i lectura exclosos de datasets.
Els dos apartats2017 i els paràgrafs de pensions de la notícia2016
alimenten el contrast del debat. No es deriven baixes individuals de
40 concessions davant un augment de30, ni s'arbitra el redactat ambigu
dels102expedients de gent gran:62favorables,30desfavorables i10pendents
esmentats després dins una frase sobre favorables. Liquidacions i
metodologia de recompte continuen pendents.


## Continuació — cotitzar sense cobrar l’ajut, article 224 bis

[CASS, HTML](cass-regims-especials-20260913.html) i
[text](cass-regims-especials-20260913.txt): secció «Persones inscrites al
Servei d’Ocupació» completa i peu de caràcter informatiu llegits.
[Inici](cass-inici-20260913.html), [navegació](cass-normativa-20260913.html)
i [normativa](cass-normativa-interpretacio-20260913.html) com a pistes
per localitzar les normes; no totes les seccions ni normes consultades.
Drets CASS pendents, cap dataset. Formulari0110 només identificat.

[Text refós2018, PDF](bopa-seguretat-social-refos-2018.pdf) i
[text](bopa-seguretat-social-refos-2018.txt):77pàgines. Decret introductori
p.1 complet llegit,article224bis complet p.60–61, renders
[60](seguretat-social-2018-pagina-60.png) i
[61](seguretat-social-2018-pagina-61.png) vistos. Altresfragments no
registrats com a unitats completes. BOPA25,02-05-2018;GL20180426_11_16_18.
Títol «involuntària» i apartat1 «voluntària» confirmats visualment,
sense correcció conjectural.

[Decret135/2024, PDF](bopa-decret135-2024-afiliacio.pdf) i
[text](bopa-decret135-2024-afiliacio.txt):13pàgines,BOPA41,03-04-2024,
GD_2024_03_28_10_51_35. Llegits preàmbul/articleúnicp.1,articles21p.6
i35p.9 complets,derogatòria/finalp.13. [Render9](afiliacio-2024-pagina-09.png)
vist. Altresfragments llegits, no totalitat dels53articles.

[Lectura compilada](../../temes/societat/treball/cotitzar-sense-cobrar-lajut-de-desocupacio.md):
10%sobre salari mínim, branca general, reembossament i còmput específic
per reversió. Declaració de no activitat al reglament2024. Referència
anterior al consolidat substituïda a l’article de l’ajut; vigència completa,
original d’introducció224bis,correccióliteral i pràctica pendents.
CitesBOPA, dretsCASSseparats. No commit ni dataset.


## Continuació — norma introductora del 224 bis

[Llei25/2011,PDF](bopa-llei25-2011.pdf), [text layout](bopa-llei25-2011.txt)
i [ordre de lectura](bopa-llei25-2011-lectura.txt). BOPA3,18-01-2012,
p.337–341, document74632, botó públicPDFobservat. Capçalera i exposició
completes llegides; article13 complet p.340; transitòries1–3,derogatòria,
final i signaturesp.341 llegides. Renders[340](llei25-2011-pagina-4.png) i
[341](llei25-2011-pagina-5.png) vistos. Resta només fragments, no tota la
llei. Textlayoutentrellaça columnes; extracció d’ordre de lectura i render
per verificar article13. Peces veïnes excloses. Anomalia noms/càrrecs a
signatures341conservada, no usada per atribuir càrrecs; no originalpaper
consultat ni autenticitatdigitalcertificada.

[Llei9/2013,PDF](bopa-llei9-2013.pdf), [text layout](bopa-llei9-2013.txt) i
[ordre de lectura](bopa-llei9-2013-lectura.txt): BOPA28,19-06-2013,
p.2833–2835,7F53E. Exposició,articles1–6,transitòria/final i signatures
complets llegits; render[2835](llei9-2013-pagina-3.png) vist. Peça10/2013
veïna exclosa. Modifica19/98.4/99,suprimeixaddicional14,introdueix223ter,
modificaaddicional15; no nova redacció224bis. No s’infereix de la lectura
que cap altra norma l’hagi modificat.

[Article ampliat](../../temes/societat/treball/cotitzar-sense-cobrar-lajut-de-desocupacio.md):
origenart13,publicació2012,transitòriasegona i discrepàncialiteral ja a
l’inici. Tanca el buit anterior de norma introductora. Cadena posterior,
correccióoficial i expedients continuen oberts. CitesBOPA, no dataset/commit.


## Continuació — vot a la CASS i correcció del model de pagament

[Llei18/2014, PDF](bopa-llei18-2014.pdf), [layout](bopa-llei18-2014.txt) i
[ordre de lectura](bopa-llei18-2014-lectura.txt):29pàgines3575–3603,
BOPA51,27-08-2014,lo26051007. Articles14–18 complets,p.3580–3581,
transitòries1–7 i finals1–3,p.3602–3603,llegits; altresfragments.
[Render3580](llei18-2014-pagina-06.png)vist.No107articlesllegits.
Refós2018 ampliat:39–41p.10;48–50p.12–13;67–69p.16–17;
132–142inclòs139bis,p.34–39,llegits complets. Renders
[16](seguretat-social-2018-pagina-16.png),[35](seguretat-social-2018-pagina-35.png),
[36](seguretat-social-2018-pagina-36.png),[37](seguretat-social-2018-pagina-37.png),
[38](seguretat-social-2018-pagina-38.png) vistos. Altresarticlesnomésfragments.
[Article224bis](../../temes/societat/treball/cotitzar-sense-cobrar-lajut-de-desocupacio.md)
ampliat amb vot67/68 senseconfondreelectoratambafiliació; candidats69nomésllegits.

[Articlegeneral de sanitat revisat](../../temes/societat/sanitat/la-cass-i-la-sanitat.md):
missióCASS40,tarifa134/135,tercerpagador141 i participació139/139bis,
remissió137estranger. Font substituïda perBOPA. Supressiódelpagamentprevi
universal i taula75/90senseversió. Hospital192habitacions,unicitat,dates,
comparacióEspanya i causalitatPortugal retirats com a fets sense peça.
[Instantània interna](la-cass-i-la-sanitat-abans-20260913.txt) conserva
l’estatanterior íntegre, no és una font de fets. Buit«CASSnooberta» tancat
parcialment; normes actuals,SAAS,capacitat i convenispendents.No datasets/commit.


## Continuació — via preferent i dos calendaris

[Llei 6/2019 PDF](bopa-llei6-2019.pdf) i [text](bopa-llei6-2019.txt):
BOPA 17, 20-02-2019, onze pàgines. Exposició, articles 1–23, finals 1–2
llegits complets en text; primera sortida truncada completada amb p. 4–8.
Renders [7](llei6-2019-pagina-07.png), [8](llei6-2019-pagina-08.png) i
[9](llei6-2019-pagina-09.png) vistos. Resta sense inspecció visual completa.
[Llei 20/2019 PDF](bopa-llei20-2019.pdf) i [text](bopa-llei20-2019.txt):
BOPA 85, 09-10-2019, dues pàgines. Exposició, article únic, final i
signatures llegits; renders [1](llei20-2019-pagina-1.png) i
[2](llei20-2019-pagina-2.png) vistos.

[Article general CASS](../../temes/societat/sanitat/la-cass-i-la-sanitat.md)
ampliat: condició de via preferent per 139.5–6; reembossament sense conveni
139.2 distingit de participació fora de via 139 bis; metge referent facturat
electrònicament i exclusió de prestacions equivalents al tercer pagador.
Calendari: final segona original 17-09-2019; nova redacció per Llei 20/2019
ajorna només 13–15 a 01-01-2020. Publicació 09-10-2019 preservada; cap
interpretació d’expedients durant la transició ni règim 2026 inferits.
Reglament d’accés, nomenclatura i cadena posterior pendents.

La Llei 9/2019 s’ha identificat i se n’ha llegit l’exposició al portal;
no s’ha baixat el PDF ni llegit el cos complet. No entrada al registre.
Evidència FORA_DEL_CORPUS, condicions textuals BOPA, cap dataset ni commit.


## Continuació — reglament d’accés sanitari de 2026

[Decret 305/2026 PDF](bopa-decret305-2026-acces-sanitari.pdf) i
[text](bopa-decret305-2026-acces-sanitari.txt): BOPA89,05-08-2026,
GR_2026_07_30_17_10_00,13 pàgines. Text complet llegit: exposició,
article únic, articles1–20, derogatòria i signatura. Renders
[1](acces-sanitari-2026-pagina-01.png),[6](acces-sanitari-2026-pagina-06.png),
[7](acces-sanitari-2026-pagina-07.png),[11](acces-sanitari-2026-pagina-11.png),
[12](acces-sanitari-2026-pagina-12.png),[13](acces-sanitari-2026-pagina-13.png)
vistos. Altres pàgines sense inspecció visual.

[Lectura de les portes d’entrada](../../temes/societat/sanitat/les-portes-dentrada-a-la-via-preferent.md):
consulta preferent/via preferent, accés directe8, confirmació10, derivació15,
calendari article únic/12/15 i tercer pagador19 destil·lats. Article general
CASS actualitzat: buit de reglament d’accés tancat; aplicació i desplegaments
específics oberts. Remissió a transitòria segona15.2.b sense disposició al
PDF registrada, sense arbitratge. Original2018 i modificacions identificats
al cercador, no llegits. Derogatòria2026 enumera la cadena anterior, no
s’infereix que es conegui el contingut de cada versió.

Augment a18 mesos ajornat a01-10-2026: no anticipat. Article19.3 combina
paper signat i factura electrònica; cap comprovació operativa o de factura.
Cosvai16–18 i sancions20 només llegits, no destil·lats. DretsBOPA textuals,
FORA_DEL_CORPUS per evidència, cap dataset ni commit.


## Continuació — les transitòries de 2018 i 2019

[Original2018 PDF](bopa-acces-sanitari-2018.pdf) i
[text](bopa-acces-sanitari-2018.txt): BOPA47,08-08-2018,
GD20180803_14_35_11,15pàgines. Exposicióp.1–3; article únic,transitòries1–2
i finals1–2,p.3; articles14–20,p.12–14, llegits complets. Resta només
fragments. Renders[3](acces-sanitari-2018-pagina-03.png),
[12](acces-sanitari-2018-pagina-12.png),[13](acces-sanitari-2018-pagina-13.png)
vistos; no inspecció visual de totes les pàgines.
[Modificació2019 PDF](bopa-acces-sanitari-2019.pdf) i
[text](bopa-acces-sanitari-2019.txt): BOPA79,25-09-2019,
GD20190923_10_19_10,2pàgines completes llegides, renders
[1](acces-sanitari-2019-pagina-01.png) i[2](acces-sanitari-2019-pagina-02.png)
vistos. La sortida de lectura repetia les dues pàgines, no el fitxer original.

[Lectura de via preferent ampliada](../../temes/societat/sanitat/les-portes-dentrada-a-la-via-preferent.md):
transitòria segona2018 sobre seguimentsestranger i canvi de remissió de
primera2018 a segona2019. Transitòries pròpies del decret2019 distingides
de les que modifica: accés directe senseMR fins30-06-2020, prescripcions
anteriors31-12-2019 fins31-12-2020 i controls previsdinsAndorra fins30-06-2020.
Buit d’original anterior tancat parcialment; efecte després de derogació2026,
intermedis2020–2025 i expedients continuen oberts. Sense reconciliació
presentada com a fet, cap dataset/commit.


## Continuació — sis, dotze i divuit mesos

[Decret2020 PDF](bopa-acces-sanitari-2020.pdf) i
[text](bopa-acces-sanitari-2020.txt): BOPA91,15-07-2020,
GR20200709_10_28_50,dues pàgines completes llegides. Renders
[1](acces-sanitari-2020-pagina-01.png),[2](acces-sanitari-2020-pagina-02.png)
vistos. Dos articles únics diferenciats, el del decret i el del reglament
modificador; transitòria primera completa.
[Decret87/2021 PDF](bopa-acces-sanitari-2021.pdf) i
[text](bopa-acces-sanitari-2021.txt): BOPA36,24-03-2021,
GD20210319_11_49_54,dues pàgines completes llegides, renders
[1](acces-sanitari-2021-pagina-01.png),[2](acces-sanitari-2021-pagina-02.png)
vistos. Article únic i final complets.
Original2018 ampliat: articles11–13,p.10–12,complets; renders
[10](acces-sanitari-2018-pagina-10.png) i
[11](acces-sanitari-2018-pagina-11.png) vistos,12ja vist.

[Lectura ampliada](../../temes/societat/sanitat/les-portes-dentrada-a-la-via-preferent.md):
12.2passa de6mesos/6visites2018 a12/12el2021;2020estableix12/12al15.2.a
extern. Regla2026de18mesos amb entrada01-10-2026 diferenciada, sense cadena
2022–2025 inferida. Transitòria2020 fixa30-06-2021 per prescripcionsabans
01-01-2020 i les d’01-01-2020aabans30-06-2020ambMRassignat; dates i
condicions diferenciades. Cap renovació actual de l’exempció inferida.
Buit2020/2021tancat; intermedis2022–2025,expedients i efecte2026pendents.
FORA_DEL_CORPUS per evidència,capdataset/commit.


## Continuació — tercer pagador de 2022 i errata limitada

[Decret349/2022 PDF](bopa-decret349-2022-acces-sanitari.pdf) i
[text](bopa-decret349-2022-acces-sanitari.txt): dues pàgines completes
llegides; renders [1](decret349-2022-pagina-1.png) i
[2](decret349-2022-pagina-2.png) vistos. BOPA104,07-09-2022.
[Errata PDF](bopa-decret349-2022-errata.pdf),
[text](bopa-decret349-2022-errata.txt) i
[render1](decret349-2022-errata-pagina-1.png) llegits i vistos complets.
[Fitxa web capturada](bopa-decret349-2022-errata-portal.json) diu BOPA106
10-09-2022; capçaleraPDF09-09-2022. Discrepància preservada.

[Lectura de via preferent](../../temes/societat/sanitat/les-portes-dentrada-a-la-via-preferent.md)
ampliada amb19.2, taula, addicional farmacèutica i entrada01-10-2022.
65anys inclosos al19.2, addicional diu«majors»; cap expedient interpretat.
Errata només data de sessió31-08-2022, no règim de prestacions. No es
converteixen motius del preàmbul en efectes observats. Buit349/2022tancat;
393/2022,542/2022,336/2023 i80/2025 encara no llegits. AcordConsell30-06-2022
i informeCASS26-07-2022 només esmentats pel decret, no originals consultats.
Evidència FORA_DEL_CORPUS, cap dataset ni commit.


## Continuació — odontologia, discapacitat i farmàcia2022–2025

[Decret393-2022 PDF](bopa-decret393-2022-acces-sanitari.pdf) i [text](bopa-decret393-2022-acces-sanitari.txt): 2pàgines completes llegides; renders [1](decret393-2022-pagina-1.png), [2](decret393-2022-pagina-2.png) vistos.
[Decret542-2022 PDF](bopa-decret542-2022-acces-sanitari.pdf) i [text](bopa-decret542-2022-acces-sanitari.txt): 3pàgines completes llegides; renders [1](decret542-2022-pagina-1.png), [2](decret542-2022-pagina-2.png), [3](decret542-2022-pagina-3.png) vistos.
[Decret336-2023 PDF](bopa-decret336-2023-acces-sanitari.pdf) i [text](bopa-decret336-2023-acces-sanitari.txt): 3pàgines completes llegides; renders [1](decret336-2023-pagina-1.png), [2](decret336-2023-pagina-2.png), [3](decret336-2023-pagina-3.png) vistos.
[Decret80-2025 PDF](bopa-decret80-2025-acces-sanitari.pdf) i [text](bopa-decret80-2025-acces-sanitari.txt): 3pàgines completes llegides; renders [1](decret80-2025-pagina-1.png), [2](decret80-2025-pagina-2.png), [3](decret80-2025-pagina-3.png) vistos.
Exposicions,articlesmodificadors,taules19.2,apartatsrestants19,finals i signatures.
BOPA117: [fitxa](bopa-decret393-2022-portal.json)04-10-2022/PDF03-10-2022.
BOPA149: [fitxa](bopa-decret542-2022-portal.json)23-12-2022/PDF22-12-2022.
BOPA84,05-07-2023 i BOPA30,13-03-2025 coincidents fitxa/PDF.

[Lectura via preferent](../../temes/societat/sanitat/les-portes-dentrada-a-la-via-preferent.md):
393/2022ajornaodontologia02-01-2023,542/2022incorporaConava33%aigualdata;
336/2023farmàciadates18-09/20-11-2023 i tiquetsmensuals, diferència65igual/majors
preservada.80/2025afegeixRD i mantétiquets,entrada17-03-2025. Comparació2026:
exposicióanunciasupressióc,19.3senseobligaciótiquets,19.2sensetaula. No cobertura
universal deduïda, ni afirmació de preàmbul convertida en resultat independent.
Buit de les quatre modificacions enumerades tancat; original2018restapendent,
esmenesnoenumerades,Conava2004,informesCASS i execució pendents. No dataset/commit.


## Continuació — memòria CASS2025: canal de pagament i imports

[PDF](cass-memoria-2025.pdf) i [text](cass-memoria-2025.txt),331pàgines.
[Portada](cass-memoria-2025-pagina-001.png) vista; sumari p.2/4 i pàgines127–129,
253 llegides completes; renders [128](cass-memoria-2025-pagina-128.png),
[129](cass-memoria-2025-pagina-129.png),[253](cass-memoria-2025-pagina-253.png)
vistos. No lectura íntegra del volum ni verificacióvisual127. Altrespassatges
29/77–79nomésidentificatspercerca, no llegits.

[Qui rep el pagament](../../temes/societat/sanitat/quan-canvia-qui-rep-el-pagament.md):
p129nota32diferenciadacanal/cost; imports2023–2025,capçalera2025/23amb11%preservada.
Càlculpropi11,04%2025/24,97,67%2025/23,noesmena. P253corrent i tancats diferenciats;
9.141,74del2024pressuposttancat no sumat implícitament a sèrie129.
Context127–128HNSMnomésllegit, no convenioriginalniresultatsassistencials inferits.
Buitaplicació de via preferent tancatparcialmentambmemòriagestor, nofactures.
DretsCASSreservats i autoritzaciópendent;FORA_DEL_CORPUS,capdataset/commit.


## Continuació — mitjanes, màxims i períodes de tramitació

Memòria2025p77–79completes llegides; renders
[77](cass-memoria-2025-pagina-077.png),[78](cass-memoria-2025-pagina-078.png),
[79](cass-memoria-2025-pagina-079.png) vistos. Les taules78/79sónimatgesque
pdftotextomet: [transcripcióderivada](cass-memoria-2025-taules-78-79-transcripcio.md)
parcial78 i completa79. No substitueixPDF,noesmena.

[DeudiesaCASS](../../temes/societat/sanitat/que-mesuren-els-deu-dies-de-la-cass.md):
quadre2025mitjana30,77/3.770demandes vsene-269,90/376;mitjanesARTICLE7
17,24 iARTICLE7IPATOLOGIA20,08enene-26,compatibilitatambmàxim10p77pendent.
Textp78tramita desprésderesoluciómèdica, nofases/fórmulaassumides.
[Qui rep el pagament](../../temes/societat/sanitat/quan-canvia-qui-rep-el-pagament.md)
ampliatambrelatCASSClínic/Teknonjuliol2025,abonamentcost/copagamentusuari.
No convenisofactures llegits. Adjudicaciórespiratòria i fullsgrocs79nomésllegits;
objectiu40%noresultat,consten87.986el2025vs82.019el2024,percentatgesimatgeno
recalculatscomasèrieanualautomàtica. No dataset, dretsCASSreservats/pendents.


## Continuació — condicions publicades dels hospitals de Catalunya

[CASS, pàgina original](https://www.cass.ad/hospitals-centres-i-metges-catalunya-convencionats),
[HTML](cass-hospitals-catalunya-20260913.html) i
[text derivat](cass-hospitals-catalunya-20260913.txt), capturats13-09-2026.
Cos complet i avís al peu llegits. Destil·lació selectiva a
[pagament](../../temes/societat/sanitat/quan-canvia-qui-rep-el-pagament.md):
Clínic14h i Teknon serveis/acord mèdic; contrast del cobrament amb Germans
Trias. A [via preferent](../../temes/societat/sanitat/les-portes-dentrada-a-la-via-preferent.md),
criteri informatiu de seguiment anterior al29-07-2026. No resolució jurídica.
La data d’enviament13-05-2024 no data tot el cos. Resta del directori llegida,
no destil·lada. Formularis CASS0112/0230 identificats però no llegits.

[Convenis, original](https://www.cass.ad/convenis-prestadors),
[HTML](cass-convenis-prestadors-20260913.html) i
[text](cass-convenis-prestadors-20260913.txt): llistat i peu llegits, nou grups
professionals. No PDF enllaçat o conveni hospitalari llegit en aquesta unitat.
Drets reservats CASS; reutilització pendent, FORA_DEL_CORPUS, cap dataset.


## Continuació — avançaments CASS-SAAS de2017 i seguiment2018

[2017 PDF](cass-estats-financers-2017.pdf) i [text](cass-estats-financers-2017.txt),
[original](https://www.cass.ad/sites/default/files/tramits/Estats%20Financers%202017.pdf).
Portada i21–23,34–36 llegides; renders[22](cass-estats-financers-2017-pagina-022.png),
[34](cass-estats-financers-2017-pagina-034.png),[35](cass-estats-financers-2017-pagina-035.png) vistos.
[2018 PDF](cass-estats-financers-2018.pdf) i [text](cass-estats-financers-2018.txt),
[original](https://www.cass.ad/sites/default/files/tramits/DOC%20Estats%20Financers%202018.pdf).
Portada,37–38,nota18 p188–190,195–197 i sumari5 llegits; renders
[37](cass-estats-financers-2018-pagina-037.png),[38](cass-estats-financers-2018-pagina-038.png),
[196](cass-estats-financers-2018-pagina-196.png) vistos.
No180/203pàgines completes. Altres resultats de cerca textual només fragments.

[Pagament](../../temes/societat/sanitat/quan-canvia-qui-rep-el-pagament.md):
avançaments2017/reintegrables, dates juliol2017 vs juny al relat2025,
liquidació declarada2018 i saldo de desembre, liquidació versus prestació,
discrepància xifra HNSM2017 entre exemplars. No conveni original, instruccions
Intervenció o comprovants consultats. Nota18 sense filaSAAS separada
identificada, conciliació pendent. P35 també imprimeix13,147 i13,148milions
al relat consecutiu: preservats, sense importar-los com un import únic.

Navegació SAAS i drets (provinença separada, no lectura temàtica):
[condicions HTML](saas-condicions-dus-20260913.html),[text](saas-condicions-dus-20260913.txt);
[contractació HTML](saas-contractacio-20260913.html),[text](saas-contractacio-20260913.txt).
Portal de transparència remet a contractacióGovern/BOPA; no conveni obtingut.
Drets reservats CASS/SAAS, reutilització pendent, FORA_DEL_CORPUS, cap dataset.


## Continuació — la instrucció d’Intervenció ja obtinguda

[Instrucció15-11-2017](govern-instruccio-cass-saas-2017.pdf),
[extracció buida advertida](govern-instruccio-cass-saas-2017.txt),
[OCRcat](govern-instruccio-cass-saas-2017-ocr.txt). Quatre pàgines íntegres
llegides visualment: renders[1](govern-instruccio-cass-saas-2017-pagina-1.png),
[2](govern-instruccio-cass-saas-2017-pagina-2.png),
[3](govern-instruccio-cass-saas-2017-pagina-3.png),
[4](govern-instruccio-cass-saas-2017-pagina-4.png).
OCR omet títol a portada i té errors prop dels segells; fets contrastats alPDF.
OriginalURL a provinença/OCR i fitxaGovern; prefix01_2026 no data la instrucció.

[Circular1/2026](govern-circular-pressupost-2026.pdf),
[text](govern-circular-pressupost-2026.txt), set pàgines completes llegides;
renders[1](govern-circular-pressupost-2026-pagina-1.png) i
[7](govern-circular-pressupost-2026-pagina-7.png) vistos. IVrelaciona instrucció2017
entre aplicables; títol18-03-2026/tancament18-02-2026 discrepants.
[Article de pagament](../../temes/societat/sanitat/quan-canvia-qui-rep-el-pagament.md)
actualitzat amb addenda01-06→entrada01-07-2017 i circuitSAAS/CASS/Govern.
Buit de la instrucció tancat; convenis/addendes originals, execució i conciliació
pendents. La instrucció aporta antecedents2014, inclosa pròrroga verbal,
annexos i26.294.893euros, només llegits; no lectura dels annexos originals.
Resta de circular1/2026 sobre gestió pressupostària només llegida.

[Navegació control pressupostari](govern-control-pressupostari-20260913.html)
i [portada contractació](govern-contractacio-inici-20260913.html) capturades.
No registre de contractes explorat; no absència del conveni inferida.
DretsGovernreservats, reutilització pendent, FORA_DEL_CORPUS, capdataset.
