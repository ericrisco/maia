# Revisió en curs — ajut per desocupació involuntària

- **Unitat:** `docs/temes/societat/treball/lajut-per-desocupacio-involuntaria.md`
- **Estat:** `pending`; no s'exporta fins a completar la revisió de tot l'article.
- **Prioritat:** primera unitat del mapa inicial: és una prestació social i barrejar absència de font amb absència del dret pot produir un negatiu fals.
- **Revisió humana:** no; revisió assistida per model, iniciada el 2026-09-25.

## Drets registrats

Les fonts declarades inclouen BOPA (text normatiu i condicions generals de
reutilització), Estadística (CC BY 4.0 per a informació estadística pròpia),
bolcats API amb llicència i atribució declarades, i Jurisprudència.ad
(consolidació pròpia del responsable del projecte sobre norma oficial).
La revisió del 25-09-2026 ha resolt l'elegibilitat dels resultats agregats
A052: els articles 21.2 de les lleis 13/2022 i 27/2025 disposen que els
resultats de les activitats estadístiques es difonguin sota llicència oberta
amb citació de la font, i A052 consta als dos plans. Això permet redistribuir
els resultats A052 amb atribució; no inclou registres administratius, dades
individuals, marques ni continguts de tercers. L'evidència i l'abast consten a
`docs/raw/estadistica-prestacions/elegibilitat-a052-2026-09-25.md` i a les
còpies locals de les dues lleis. La decisió de l'article continua `pending`
perquè la revisió factual i normativa integral no s'ha completat.
## Contrast parcial de les sèries d'Estadística

S'han contrastat l'A052 de 2024 i els bolcats de prestacions, mercat laboral i
indicadors europeus del 18-09-2026 per a les xifres que l'article destaca.

- L'A052, p. 2, identifica els registres del Departament d'Afers Socials com a
  font: 107 sol·licituds el 2024, 71 favorables, 36 desfavorables, 64 llars,
  139 persones i 334.704,11 €. L'import mitjà per llar és 5.229,75 €. La p. 3
  repeteix la relació 71/107; la p. 4 confirma 26 sol·licituds favorables en
  famílies unipersonals i 14 en monoparentals. Les pàgines 5 i 9, llegides i contrastades visualment, confirmen també els
  percentatges per nacionalitat i el desglossament per sexe i edat;
  agregant les dues files de sexe, 60–64 anys és el grup més gran (14/71,
  19,7%), no 50–54 anys (vuit dones, 11,3%). S'ha corregit aquesta atribució
  del borrador.
- La publicació oficial A052 de 2025 informa 62 sol·licituds: 31 favorables,
  28 desfavorables i 3 no resoltes. La captura API del 18-09-2026 informa 59 a
  la divisió 2829 i 31/28 a la divisió 2830; el total API és la suma de les
  resolucions i no inclou els tres casos no resolts de la publicació. La causa
  de la diferència no està documentada. La divisió 2834 confirma la
  distribució per nacionalitat 17/5/2/0/7, que suma 31.
  La divisió 2829 conté dades per a cadascun dels onze anys 2015–2025. El
  contrast complet ha recuperat 2017 (177 sol·licituds, 107 concedides) i 2019
  (139, 97), omesos a la taula del borrador; també s'ha afegit 2023 (120, 70).
  L'expressió «onze anys» era correcta per a l'interval, però la taula no el
  cobria completament.
- La divisió 2646 confirma les taxes d'atur 1,8 (2018), 2,2 (2019), 3,1 (2020),
  3,3 (2021), 2,1 (2022) i 1,6 (2023). Per a 2024 retorna 0 per atur i 0,8 per
  ocupació i activitat; el bolcat no explica què signifiquen les tres cel·les.
  El text revisat no les classifica com a valors vàlids ni com a placeholders:
  registra que cal consultar-ne la definició.
- La divisió 455 té 224 observacions mensuals, 2008/01–2026/08. El màxim del
  període és 2.214 el 2020/05; el mínim, 346 el 2008/08; el darrer valor és 429
  el 2026/08. El desembre de 2025 (483) és el segon valor de desembre més baix
  entre 2008 i 2025, no el segon valor de tota la sèrie mensual. En els 224 mesos
  queda quart per valor baix, després de 346, 404 i 417.
- Les divisions 456, 547, 463 i 461 confirmen per al 2025/12 els desglossaments
  citats: motiu d'inscripció 210/198/74/1; residència 70/55/67/291; nacionalitat
  224/132/82/34/11; sexe 269/214. La suma de les categories és 483. S'ha
  corregit l'extrapolació «les altres 285 tenen feina»: 284 estan etiquetades
  explícitament com ocupades i una figura en baixa mèdica superior a sis mesos.

## Queda per revisar abans de decidir

- Completar la confrontació frase per frase dels articles 2, 14 i 26, incloses
  les causes d’extinció, documentació, suspensió i el text consolidat. La
  comparació inicial ja ha localitzat l’esmena substancial del relat de
  versions: el Decret 44/2021 sí que va flexibilitzar temporalment parts de
  l’article 26.
- Verificar l’univers de la comparació entre demandants i població per
  nacionalitat; les divisions 1099 i 797 confirmen els recomptes publicats.
  Revisar totes les dades mensuals i anuals derivades, no només els extrems.
- Comprovar si els recomptes API de sol·licituds dels anys anteriors inclouen
  casos no resolts amb el mateix criteri que l'A052 de 2025; la discrepància
  del 2025 està registrada, però la font no n'explica la causa.
- Reconciliar les deu versions anunciades per Jurisprudència.ad amb les peces
  que retorna la cerca BOPA, i comprovar els butlletins posteriors al 13-09-2026
  abans de fer cap afirmació sobre el règim actual.
## Contrast inicial de la cadena normativa

La comparació dels textos locals mostra que la secció anterior del borrador
contenia una afirmació errònia: deia que cap modificació posterior afectava
l’article 26, però el Decret 44/2021 en va flexibilitzar temporalment els
apartats 4.c, 4.d, 4.i i 4.j i el requisit de nova sol·licitud de l’apartat
12. El mateix decret va derogar el Decret del 16-12-2020, que havia afegit
l’article 26 bis per a treballadors de temporada d’esquí. La flexibilització
del 2021 tenia data límit màxima del 30-06-2021, llevat que el Govern la deixés
sense efecte abans. L’article revisat ara distingeix aquesta excepció de la
redacció general del 2020.

La nota del 2020 diu expressament que el reglament nou substitueix el del 2019
i que reenumera l’article 26. La correcció d’errata del 03-03-2021 es refereix
a la disposició derogatòria, no a l’article 26. S’han localitzat també les
peces posteriors 191/2022, 476/2022, 531/2022, 585/2023, 486/2024 i 471/2025;
els textos descarregats tracten altres articles. La cerca no constitueix una
reconciliació completa de les deu versions que anuncia Jurisprudència.ad ni
una comprovació de butlletins posteriors al 13-09-2026.

La correcció parcial no canvia la decisió `pending`. Aquest informe i els
bolcats datats permeten reprendre la revisió sense donar per aprovat el
contingut jurídic ni l'article complet.

## Contrast normatiu addicional — 2026-09-25

S'han confrontat amb el text del BOPA de 2020 les afirmacions de l'article que
remeten als articles 2, 14 i 26. La remissió de l'article 2 als articles 4 i 5
de la Llei 6/2014 és correcta. L'article 14.1 exigeix majoria d'edat o
emancipació i els requisits generals de recursos; l'apartat 1.b eximeix de
prescripció tècnica l'ajut de l'article 26 quan se'n compleixen els requisits
específics. Els resums de l'article sobre la finalitat, caràcter no contributiu,
causes de pèrdua involuntària de feina, cotitzacions, oferta adequada,
formació, import, durada, suspensió, compatibilitat, extinció, nova sol·licitud,
gestió i documentació coincideixen amb les peces citades de l'article 26.1–14.
El text de 2020 conté les expressions «es trobar sense feina» i «90 naturals»;
la lectura les reprodueix i no presenta la seva interpretació com una regla
corregida pel corpus.

Per als exemples sobre la compensació per comiat, s'ha contrastat directament
l'article 84.1 de la Llei 31/2018, que fixa 25 dies de salari per any treballat
amb un màxim de 365, i l'article 3 de la Llei 3/2026, que modifica l'apartat 4
de l'article 84, no l'apartat 1. La conversió d'anys en dies és aritmètica
pròpia; continua oberta la interpretació administrativa del topall de 120 dies
i de les fraccions que es registren a «Buits registrats».

S'ha tornat a llegir la cadena local de modificacions 2022–2025: el Decret
191/2022 afegeix l'article 17 bis; el 476/2022 afegeix el 19 bis; el 531/2022
i el 585/2023 modifiquen el 17 bis; i els decrets 486/2024 i 471/2025
modifiquen l'article 17. No s'hi ha trobat cap canvi a l'article 26. El Decret
471/2025 és l'última modificació examinada; el seu article únic modifica
l'article 17, no el 26. Això limita la discrepància amb les deu versions de
Jurisprudència.ad, però no explica com es compten les versions consolidades ni
demostra que la cadena documental sigui exhaustiva.

La passada és parcial: s'han revisat les afirmacions jurídiques reproduïdes a
l'article, no tots els efectes de la Llei 6/2014, la interpretació
jurisprudencial ni l'aplicació administrativa. La unitat es manté `pending`
fins a completar la verificació dels universos estadístics i la cadena de
versions.
