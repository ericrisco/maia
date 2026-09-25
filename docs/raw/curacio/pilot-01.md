# Pilot 01 — tancat

Inici: 2026-09-24. Abast previst: 20 unitats variades de les categories
història, institucions, societat, estadística, llengua i transcripcions.
Aquest registre només compta com a revisada una unitat quan hi ha decisió amb
hash d'entrada; no converteix la resta de la selecció en revisada.

## Unitat 1/20

- ID: `maia-docs/temes/societat/demografia/dues-maneres-de-comptar-la-poblacio.md`
- Estat actual: `approved`; destí: coneixement.
- Font declarada: `estadistica-ad`; data de referència: 31-07-2026.
- SHA-256 revisat: `042e56f2d4efad8e167124e1fd140f06ff516cd1b3f91349105c472ff5ca5650`.
- Exportació: `final-corpus/coneixement/societat/demografia/dues-maneres-de-comptar-la-poblacio.md`;
  SHA-256: `3f7ca122e7d004dd182e6b8fabf47099fe53d9abf0809f334928affa1d16f668`.
- Mètodes: comparació factual assistida per model, inspecció visual de PDF i
  recàlcul aritmètic. No hi ha hagut revisió humana.

### Evidència i comprovacions

- Nota NP_A001_A003_20260813, p. 1: total resident de 90.021; registre dels
  comuns de 94.596; avís sobre depuracions administratives i validació menys
  completa de la població andorrana.
- La mateixa nota, p. 7: taula de població registrada i estimada per parròquia,
  diferències absolutes i percentatges; gràfic anual amb Encamp −4,7% registrat
  i +2,2% estimat, i la Massana −1,3% i +2,2%. La pàgina s'ha inspeccionat
  visualment i els colors/etiquetes concorden amb el text.
- Nota, p. 8: diferència per nacionalitat; les persones andorranes són 38.573
  registrades i 40.128 estimades, amb desviació de −1.555.
- Nota, p. 12: publicació mensual des de desembre de 2009 i definicions de les
  poblacions registrada i estimada.
- Metodologia A001, pp. 4–6: registres creuats, detecció de possibles altes i
  baixes, i millores metodològiques descrites com a treball futur.
- Avís legal del Departament d'Estadística, §6: CC BY 4.0 per a informació
  estadística pròpia; cal atribuir el Departament i indicar tractament/data.
  La fitxa `docs/fonts/estadistica-ad.md` delimita que aquesta nota i la
  metodologia són les peces cobertes.
- Recàlcul independent de la taula: 94.596 − 90.021 = 4.575; 4.575 / 90.021
  arrodoneix a 5,1%; les set diferències parroquials sumen 4.575.
- Cerca d'identitat de cos normalitzat sobre 1.348 articles temàtics: zero
  famílies de duplicat exacte. La unitat comparteix fonts i alguns fets amb
  «Demografia» i «Qui compta com a resident»; queda agrupada a
  `family:estadistica-a001-a003-2026-07` perquè una selecció posterior pugui
  evitar ponderar tres vegades la mateixa evidència.

### Estat i feina que falta

La lectura factual de les xifres i les afirmacions principals concorda amb les
fonts. S'ha trobat i corregit un defecte a «Buits registrats»: la versió prèvia
deia que la prosa de §3.1, p. 7, comparava juliol de 2026 amb juliol de 2026;
la pàgina original diu juliol de 2025, coherent amb les columnes de la taula.
S'ha eliminat aquesta falsa discrepància. També s'han retirat la secció de
navegació `Related`, les marques de ratllat de seguiment i el comentari de
treball «Selecció de columnes del corpus». La nota sobre l'abast s'ha corregit
per precisar quines pàgines sustenten aquesta unitat, sense afirmar que les
altres pàgines no s'hagin consultat en altres lectures del corpus.

La font canònica ja té atribució CC BY 4.0 (titular, referència, data de
publicació/consulta i absència d'aval institucional), i la unitat queda aprovada
per a coneixement amb mètodes i limitacions explícits. `export_final_corpus.py
--write`, `export_final_corpus.py --check` i `build_final_manifest.py --check`
han passat; el manifest conté l'original, els localitzadors, els termes, la
revisió sense validació humana, les transformacions i la família de fonts.

Els PNG inspeccionats són derivats de consulta guardats a
`pilot/statistics/`; els PDFs i els fitxers de text originals no s'han alterat.

## Unitat 2/20

- ID: maia-docs/temes/societat/treball/lajut-per-la-feina-que-no-havia-comencat.md
- Estat actual: approved; destí: coneixement històric.
- Font: bopa-ad; text publicat al BOPA 150 del 17-12-2020, derogat
  expressament pel Decret 44/2021 al BOPA 24 del 18-02-2021.
- SHA-256 revisat després de neteja editorial: e0673b0f142fc263ed58afae2a741be9db679372f6eae73c8f158ff52a07a4eb.
- Exportació: final-corpus/coneixement/societat/treball/lajut-per-la-feina-que-no-havia-comencat.md.
- Mètodes: contrast del text legal primari, comprovació dels localitzadors,
  revisió dels termes BOPA i neteja editorial. Revisió assistida per model;
  no hi ha hagut revisió humana.

### Evidència i comprovacions

- Decret del 16-12-2020, art. 26 bis.1 i 3: dos supòsits de contractació
  frustrada o incorporació ajornada; requisits de temporada 2019–2020,
  residència, inscripció i períodes de cotització per edat.
- Art. 26 bis.5–7, 9.c, 10.c i 12–13: quantia, afiliació a les dues branques
  de la CASS, data d'inici, certificat d'empresa, termini màxim de deu dies
  hàbils, durada vinculada a l'obertura de temporada i definició de residència.
- Decret 44/2021, art. 3, disposició addicional i disposició derogatòria 1:
  assimilació al règim ordinari, còmput dels períodes percebuts i derogació
  expressa del decret temporal. La lectura no afirma que s'hagi comprovat
  l'execució dels expedients.
- Els termes generals del BOPA permeten copiar, adaptar i distribuir el text
  normatiu amb atribució, sentit i condicions preservats; no s'inclouen
  logotips, gràfics ni presentació institucional.
- S'han tret del text exportable les marques de ratllat i els comentaris de
  seguiment ja resolts. Es mantenen els buits sobre aplicació administrativa,
  interpretació d'ofertes i resultats individuals.
- La unitat queda agrupada amb el document jurídic post-freeze sobre els
  períodes de cotització de la mateixa família normativa, per evitar comptar
  com a evidència independent la síntesi de regles que comparteix el BOPA.
- L'exportació i el manifest es regeneren després d'actualitzar el ledger; no
  hi ha revisió humana.

## Unitat 3/20

- ID: maia-docs/temes/institucions/comuns-i-parroquies/quan-una-sentencia-confon-el-precedent.md
- Estat actual: approved; destí: coneixement.
- Font: bopa-ad; sentència constitucional 2026-25-RE publicada al BOPA 71 del
  25-06-2026.
- SHA-256 després de neteja editorial:
  f971a5c47b35b9fb69c1b22b2bd53dfbfccd1db8330b8857c0c5470017c2e78a.
- Localitzadors principals: antecedents 1.1, 1.6–1.7, pp. 1–2; fonaments
  3.2, p. 7, 3.3–3.4, pp. 7–8, 3.5, p. 9; decisió 1–3, p. 9.
- PDF BOPA, pàgines impreses 8–9, inspeccionat visualment. Els dos renders ja
  conservats a docs/raw/consell-general/ coincideixen amb l'extracció de text.
- La cerca de l'identificador 2026-25-RE i del fitxer PDF citat retorna només
  aquesta unitat sota docs/temes/; al manifest es declara duplicate_group=none.
- Revisió: contrast factual assistit per model, localitzadors visuals i termes
  BOPA; cap revisió humana. Els originals dels precedents i l'estat actual de
  la finca continuen fora de l'abast i s'indiquen al text.
- S'han retirat l'apartat de navegació wiki i anotacions de seguiment resoltes.
  S'ha conservat el límit entre el que decideix el Tribunal i el que encara no
  se sap sobre la resolució posterior.
- L'exportació resultant i el manifest s'han generat i comprovat amb tres
  unitats aprovades.

## Unitat 4/20

- ID: maia-docs/temes/historia/antic-regim/queixa-batlle-garreta-1528.md
- Estat: pending; destí possible: coneixement històric.
- Font: fitxa pública de l’Arxiu de les Set Claus, registre ASC-3494; data
  catalogràfica 06-09-1528.
- S’han contrastat les afirmacions contra els camps d’identificador,
  descripció, persones, fons, extensió i data del JSON de metadades capturat.
  No s’ha fet una transcripció paleogràfica ni s’ha inferit el desenllaç.
- L’avís oficial vigent de FotoWeb (consultat el 25-09-2026 i guardat a
  docs/raw/web/institucions/arxiu-set-claus/terms-and-conditions-2026-09-25.html,
  SHA-256 2d0ba5ac229546bc70de6321fef43a58de29b154456b9e444d8bf97aca1d03dd)
  reserva la redistribució llevat d’autorització; l’excepció d’imatges és
  limitada i no cobreix publicació o modificació. No s’ha trobat permís per a
  aquesta síntesi catalogràfica en un corpus distribuïble.
- Es manté pending i no s’exporta fins a obtenir autorització o una
  determinació clara dels termes. La fitxa de font s’ha corregit perquè
  redistribucio sigui l’enum pendent i expliqui el motiu a notes. El registre
  i la captura de termes queden exclosos com a material d’entrenament.

## Unitat 5/20

- ID: `maia-docs/temes/llengua/contacte-de-llengues/contacte-de-llengues.md`
- Estat: `pending`; destí possible: coneixement sobre sociolingüística.
- Font declarada: `iec-vocabulari-andorra`; SHA-256 revisat: `31305195e8b8ec4817bd49573c6987f1b3bd64fb3a7b077a8c647b592f2f23d9`.
- La peça IEC catalogada a les pp. 43–60 tracta de dialectalismes, diccionaris i reconeixement normatiu del vocabulari. No verifica els patrons de bilingüisme/quadrilingüisme ni el canvi de llengua afirmats a l’article.
- L’article reconeix que falten xifres d’ús i no identifica una font primària per a les generalitzacions centrals. La fitxa IEC tampoc documenta una llicència explícita de redistribució.
- No s’exporta. Cal afegir fonts sociolingüístiques adequades i resoldre els drets abans de reconsiderar-lo. Revisió assistida per model; sense validació humana.

## Unitat 6/20

- ID: `maia-docs/temes/institucions/consell-general/el-consell-general.md`
- Estat: `approved`; destí: coneixement.
- Fonts: Constitució, arts. 50, 52–53 i 57.3 (BOPA 24, p. 452), i Reglament del Consell General de 2026, arts. 14–18, 30–38, 45, 55 i 58 (BOPA 72, pp. 8–9, 12–15, 18–19). Entrada en vigor: 27-06-2026.
- Hash de l’article després de la correcció: `6e07c8ffe54d165657be1df8d0d78efa206e47d076ce7bfdd9d064a4e4a389a0`.
- Es va detectar i corregir una dada falsa: el mínim constitucional és 21 escons, no 28; el màxim és 42. La divisió 14/14 continua només com a exemple hipotètic.
- Es van retirar les afirmacions sobre el nombre i noms actuals dels consellers, que depenien d’una pàgina institucional amb redistribució no autoritzada; també es van netejar marques de seguiment i navegació.
- Nou renders de pàgina es van comprovar visualment i queden exclosos com a derivats tècnics; el text aprovat i les seves fonts són reproduïbles des del BOPA. Revisió assistida per model, sense validació humana.

## Unitat 7/20

- ID: `maia-docs/parla/oral/cal-pal-esther-jover.md`
- Estat: `pending`; destí possible: llengua; no exportada.
- SHA-256 de la fitxa revisada: `da884bc57f295fce58478b7484cb0d3dd02e0f9e1fda59d8bc2db93b62cc8064`.
- El títol del vídeo #49 atribueix la veu a Esther Jover, i UNESCO la relaciona amb Cal Pal; cap prova consultada n’estableix l’origen andorrà o la varietat lingüística.
- YouTube declara CC BY per a aquesta peça. Captura JSON amb data, eina i procedència: `docs/raw/parla/ari-capsula-49/youtube-info-2026-09-25.json`, SHA-256 `ff1dcbb286b6b557a77fbf4d0bd781759135f41e44e0e540060ef51996ae7d17`. El registre de tota la sèrie passa a `redistribucio=pendent` perquè la llicència s’ha de verificar per vídeo.
- No s’ha escoltat l’àudio i no hi ha cap fitxer d’àudio al directori local; l’extracció ASR conté 294 segments i 52 marques. La fitxa es classifica com `veu=compilada`, `apte_llengua=false` fins a verificar àudio i perfil. La metadada diu 9:48 i el material anterior 9:49.
- Grup de família: `family:cal-pal-house-history`, per mantenir juntes les peces que tracten els mateixos fets patrimonials de Cal Pal; no s’ha trobat duplicat textual exacte. Revisió assistida per model; sense revisió auditiva humana.

## Unitat 8/20

- ID: `maia-docs/temes/economia/banca-i-fiscalitat/el-superavit-que-financa-habitatge-i-hospital.md`
- Estat actual: `approved`; destí: coneixement.
- Font: Llei 10/2026, BOPA 56 del 03-06-2026. Entrada en vigor el 04-06-2026 segons la disposició final quarta; l'article 1 és aplicable als superàvits de 2025.
- SHA-256 de l'article després de netejar els buits ratllats i retirar referències derivades de memòries del Govern sense redistribució acreditada: `236e5325242c117da50940b3ccf6f74a149b359de67793efd5d69e03b6c8dd46`.
- Contrast amb `docs/raw/pressupost-2026/bopa-llei-10-2026.txt` i el PDF BOPA, arts. 1–6, pp. 3–5, exposició de motius, pp. 1–2, i final quarta, p. 5. El registre de font anota que els renders 3–5 es van inspeccionar en la lectura documental anterior; aquesta tanda ha contrastat de nou el text i els imports.
- Recàlcul Decimal: les quatre partides d'habitatge sumen 35.000.000 €; el suplement de l'Administració general suma 33.750.000 €; crèdit extraordinari més suplement fan 40.150.000 €; i el suplement receptor del SAAS (3.600.000 € + 800.000 €) correspon als 4.400.000 € transferits que ja formen part dels 40.150.000 €, no a finançament addicional.
- La llei autoritza copiar, adaptar, distribuir i transformar la informació, condicionat a preservar-ne el sentit i les metadades i a no reutilitzar elements gràfics ni maquetació. La fitxa `bopa-ad` i l'avís local `docs/raw/desocupacio/bopa-avis-legal.txt` en documenten els termes.
- Revisió editorial: s'han eliminat anotacions ratllades i afirmacions dependents de fonts del Govern que no tenen redistribució autoritzada. El text no afirma execució, adjudicacions, lliuraments, inventari actual d'habitatge ni vigència consolidada; aquests buits queden explícits. El preàmbul invoca conclusions de l'FMI, però el document original no s'ha consultat.
- Cerca de duplicats textuals normalitzats a `docs/temes/`: cap coincidència exacta. Grup: `family:bopa-law-10-2026-budget-housing-health`. Revisió assistida per model, sense revisió humana.

## Unitat 9/20

- ID: `maia-docs/temes/cultura/museus-i-arxius/res-danterior-al-1984-no-es-tria.md`
- Estat: `pending`; destí possible: coneixement; no exportat.
- SHA-256 revisat: `d9fa36e6cfdd349025dd6fc338888b3fb8df0fd457f37e67c2f2a937f2ca9242`.
- Fitxa `bopa-ad`: condicions generals permeten copiar, adaptar i distribuir text preservant-ne el sentit i metadades; no hi ha reutilització gràfica.
- Triage de la cadena primària: el Decret del 2014, art. 3.5, conté el límit d'1-1-1984 però deroga el Reglament CAD del 1998; el reglament CAAD de 2015 deroga el Decret del 2014; el Decret 455/2022 deroga el reglament del 2015, preservant explícitament les taules d'avaluació però no reprodueix la regla del 1984. No s'ha demostrat si una altra disposició la manté vigent.
- La tesi del títol es pot entendre com a dret vigent; no s'aprova sense determinar-ne l'estat jurídic actual. Tampoc no s'ha confirmat sistemàticament la cerca de «cap cas localitzat» o l'execució de la transferència de 2010. El text conserva una secció `Related` que l'exportador rebutja.
- Per reprendre: reconstruir derogacions i normes d'arxiu posteriors, comprovar les afirmacions empíriques i, si cal, reescriure com a lectura històrica amb límits explícits. Revisió assistida per model; sense revisió jurídica humana.

## Unitat 10/20

- ID: `maia-docs/temes/territori/clima-i-muntanya/el-terreny-sense-classificar-i-les-allaus.md`
- Estat: `approved`; destí: coneixement; SHA-256 revisat:
  `e330fc4f6534187268651eef78436cbe6bc4d826b88b09fed8c83817d7edb050`.
- Evidència: Decret del 26-09-2012, preàmbul, arts. 1 i 3 i disposició
  transitòria primera, BOPA 48, pp. 3938–3939; Reglament del 09-03-2016,
  arts. 1–7, 12–16, 22, disposicions derogatòria i final, BOPA 17,
  pp. 3–4, 6–8, 11 i 15, annexos fins a p. 19; Decret 335/2023,
  exposició de motius i art. 1 (redacció dels arts. 1, 7 i 35), BOPA 84,
  pp. 1–3.
- Els textos originals confirmen la distinció entre terreny no estudiat i
  absència de perill detectat, els estudis requerits, les classes R1/R2B/R7,
  l'excepció dels dominis esquiables vinculats a PIDA i les correccions de
  2023. S'han comprovat els localitzadors contra les còpies BOPA. La revisió
  no estableix vigència consolidada, cartografia actual, assignació a parcel·les
  ni contingut d'un PIDA.
- S'han retirat una comparació amb ATES/BPA basada en fonts amb drets de
  redistribució no acreditats i anotacions de treball ratllades. Els buits ara
  indiquen que no s'han consultat cartografia, Cadastre d'allaus ni PIDA, i
  conserven l'ambigüitat textual dels límits d'1 i 30 kPa. El BOPA permet
  reutilitzar el text segons els termes registrats a la fitxa `bopa-ad`.
- No hi ha duplicat textual exacte. Comparteix família normativa amb
  «Quan un bosc protegeix un edifici»; el grup queda registrat com
  `family:bopa-allaus-2012-2016-2023` per evitar tractar la mateixa base
  reglamentària com a evidència independent. Revisió assistida per model;
  sense revisió humana.

## Unitat 11/20

- ID: `maia-docs/temes/territori/clima-i-muntanya/quan-un-bosc-protegeix-un-edifici.md`
- Estat: `approved`; destí: coneixement; SHA-256 revisat:
  `01b1a90a402e2d8445c2103ff9492cc194031feeea455d8f179c45858958dfa4`.
- Evidència: Reglament del 09-03-2016, arts. 6, 7.2.h i 21.1–6, BOPA 17,
  pp. 4 i 10; art. 13, pp. 6–7; arts. 28.1–4 i 33.4, pp. 12 i 14;
  annex V, apartats 2–7, p. 19. Els localitzadors confirmen la definició de
  bosc R7, l'espai i el dret d'ús necessaris per a proteccions futures, el
  document de compromís, el desallotjament indefinit, els llindars anuals de
  risc i les obligacions en transmissions i lloguers.
- S'han netejat les marques de seguiment i retirat l'ampliació sobre els
  articles 127 i 129 de la LGOTU: no era necessària per sostenir aquesta
  lectura. Es conserva com a buit la manca de reconstrucció normativa i
  jurisprudencial i la manca d'evidència sobre compliment en casos concrets.
- No hi ha duplicat textual exacte. La unitat comparteix la família normativa
  amb «El terreny sense classificar i les allaus» i queda al grup
  `family:bopa-allaus-2012-2016-2023`; comparteixen base reglamentària, però
  tracten qüestions diferents. Revisió assistida per model, sense revisió
  humana.

## Unitat 12/20

- ID: `maia-docs/temes/societat/treball/la-flexibilitzacio-de-la-desocupacio-el-2021.md`
- Estat: `approved`; destí: coneixement històric; SHA-256 revisat:
  `9fb93b9a95391bb836e8c2ece9ff63aacf5c2d5699365d6b199368535cebcf40`.
- Evidència: Decret 44/2021, arts. 1–3 i disposicions addicional, transitòria,
  derogatòria i final (BOPA 24, 18-02-2021); Reglament del 7-10-2020,
  art. 26.4.c,d,i,j i art. 26.12 (BOPA 121, 14-10-2020); Decret del
  16-12-2020, article 26 bis (BOPA 150, 17-12-2020). Les peces confirmen
  els canvis de 6 a 12 mesos, de 45/90 a abans de sol·licitar o 30 dies,
  de 36/60 a 18/30 i de 18 a 9 mesos, i el còmput de 6 mesos treballats
  dels 24 per tornar a sol·licitar.
- També s'han verificat la data d'entrada en vigor, el màxim del 30-06-2021,
  la transició dels expedients pendents amb la norma més beneficiosa «en el
  seu conjunt», l'assimilació i còmput dels períodes cobrats amb l'article
  26 bis i la derogació expressa del Decret del 16-12-2020.
- S'han retirat notes de seguiment ratllades i una remissió a una lectura més
  àmplia que depèn de fonts addicionals. Els buits mantenen obertes la
  interpretació de la compensació per comiat, la vigència real, les resolucions
  i el nombre d'expedients; no s'han inferit resultats administratius.
- No hi ha duplicat textual exacte. Comparteix fonts amb «L'ajut per la feina
  que no havia començat» i queda a la família
  `family:ajut-desocupacio-2020-2021`. Revisió assistida per model, sense
  revisió humana.

## Unitat 13/20

- ID: `maia-docs/temes/cultura/museus-i-arxius/abans-ho-decretava-el-govern.md`
- Estat: `pending`; destí possible: coneixement; SHA-256 de l'original:
  `96faf102b07ee1ce4485e5f37a6457ba116cde29342e76f4b6b4d03d93072ce6`.
- La porta de drets està resolta: la fitxa `bopa-ad` permet reutilitzar els
  textos normatius del BOPA amb les condicions registrades. La revisió factual
  completa no s'ha fet.
- La tesi principal divideix 25 edictes entre 19 fórmules de Govern i 6 de
  CNAAD, afirma que cap edicte no barreja les fórmules i presenta recomptes de
  taules. L'evidència pròpia de la carpeta assenyala que 13 edictes de
  2021–2022 —el gruix de l'activitat CAAD— només s'han llegit per la capçalera.
  No es poden confirmar amb això els recomptes, les dates ni el contingut de les
  resolucions.
- No s'exporta fins a llegir els 13 textos i contrastar els recomptes. L'article
  també manté una secció `Related`, rebutjada pel control d'exportació. Aquesta
  és una retenció per manca de verificació factual, no per drets; no s'ha fet
  una revisió factual completa ni revisió humana.

## Unitat 14/20

- ID: `maia-docs/temes/societat/educacio/les-guarderies.md`
- Estat: `pending`; destí possible: coneixement; SHA-256 de l'article:
  `babca8170e223fc6f1699e58ca5861fff1cce44e06d54cacd29f9245bbfdfe4e`.
- La lectura d'elegibilitat ha detectat una font material no documentada a la
  fitxa de font: el llistat oficial de guarderies del Registre Nacional de
  Serveis Socials i Sociosanitaris. El llistat és allotjat al portal del Govern;
  l'avís legal vigent consultat el 25-09-2026 reserva reproducció, tractament,
  distribució i comunicació pública sense consentiment previ i escrit, i limita
  l'ús ordinari a l'àmbit privat i personal. Captura desada a
  `docs/raw/web/societat/educacio/govern-avis-legal-2026-09-25.html`, SHA-256
  `b174ae0813a365c8f2625b5c13fe501961b4f1ebf719c8a24c32d6e623bb6d5d`.
- S'ha creat la fitxa `docs/fonts/govern-llistat-guarderies.md` amb URL,
  titular, termes i evidència. La fotografia inicial no incloïa aquesta fitxa
  ni la captura dels termes; es registren com a incorporacions posteriors i no
  s'amplia per elles l'abast inicial.
- No s'ha fet la revisió factual completa dels requisits legals, les ràtios ni
  les xifres de registre. L'article no s'exporta mentre l'elegibilitat del
  llistat i l'abast de les fonts secundàries no estiguin resolts. Revisió
  assistida per model; sense revisió humana.

## Unitat 15/20

- ID: `maia-docs/temes/institucions/justicia/el-tribunal-de-comptes.md`
- Estat: `pending`; destí possible: coneixement; SHA-256 després de les
  correccions parcials: `2b936662a09f1630a4908b990ebc3cfe85c63fc5cde3bf9bd1bed49061551a0d`.
- La comparació amb el text refós BOPA del 27-09-2017, arts. 18, 22 i 23,
  ha corregit tres imprecisions: el Ple pot tenir de dos a quatre membres; els
  mandats de sis anys són renovables; i les titulacions exigides comprenen els
  àmbits econòmic, jurídic, financer i/o comptable. S'ha retirat la inferència
  no sostinguda que el Consell General pagui directament el Tribunal. La
  designació del 2021 ara consta com la més recent dins les quatre peces
  BOPA llegides, no com a composició actual.
- El text refós deixa oberta la reconstrucció de les versions legals vigents
  a cada nomenament, especialment el del 2006. La pàgina oficial d'informes
  consultada el 25-09-2026 ja llista una memòria anual del 2025 i altres
  informes; no s'han descarregat ni revisat. L'avís legal del Tribunal reserva
  els drets i limita a ús personal els fitxers descarregables. S'han guardat
  les captures a `docs/raw/web/institucions/tribunal-comptes/` i creat la fitxa
  `docs/fonts/tribunal-comptes-web.md`, marcada no redistribuïble.
- La fitxa BOPA s'ha corregit per fonamentar la redistribució en les condicions
  d'ús del BOPA, no en què els documents siguin públics. Queden pendents la
  verificació de totes les afirmacions, la revisió del règim entre 2000 i 2017
  i la resolució de la font institucional no redistribuïble. No s'exporta;
  revisió assistida per model, sense revisió humana.

## Unitat 16/20

- ID: `maia-docs/temes/cultura/museus-i-arxius/com-sentra-a-larxiu-nacional.md`
- Estat: `pending`; no exportat. SHA-256 després de corregir els límits de la
  lectura de 2016 i afegir els buits verificats:
  `a9fa9c223c3116e41a46cbe839c70a964b1ac742a1fb6241cb862e507ff2b9b0`.
- S'han contrastat els articles 18–35 i 41–43 del Decret del 06-04-2005, els
  articles 2–8 del Decret del 20-04-2016, i la disposició addicional primera de
  la Llei 33/2021. Aquesta darrera disposició estableix l'aplicació supletòria
  de la Llei general quan hi ha un règim específic; això no substitueix la
  reconstrucció de les normes concretes ni el contrast article per article.
- La pàgina oficial actual del Govern «Prepareu la vostra visita a l'arxiu»
  (apartat «Qui pot consultar…?», consultada 2026-09-25) diu que poden consultar
  documents les persones majors de 18 anys i que els menors de 16 a 18 han
  d'anar acompanyats. El Decret de 2016 regula l'accés de menors de 16 en
  supòsits concrets i l'acreditació dels usuaris. S'ha registrat la pàgina a
  `docs/fonts/govern-prepareu-visita-arxiu.md`; no s'ha identificat llicència
  oberta ni permís i la redistribució queda pendent. No es resol la discrepància
  ni s'afirma quina pràctica o regla preval.
- Una versió de treball remetia al «Decret 454/2022 del procediment d'accés».
  No s'ha identificat un text que avali aquesta denominació. No s'ha de
  confondre amb el Decret 455/2022, identificat a la normativa oficial com el
  reglament d'organització i funcionament de la CNAAD. Cal identificar i llegir
  les normes de desplegament aplicables.
- L'article conserva altres buits: capítols I–II i articles posteriors al 35 del
  Reglament, modificació del Reglament del Sistema d'Arxius, casos d'aplicació,
  i revisió completa del règim d'accés actual. La secció `Related` també impedeix
  l'exportació pel contracte actual. Revisió assistida per model; sense revisió
  legal humana ni revisió humana.
- Fitxa de font afegida després de congelar l'inventari inicial: exclosa de la
  sortida d'entrenament. La unitat temàtica sí que forma part del pilot original.

## Unitat 17/20

- ID: `maia-docs/parla/oral/qui-eren-els-constituents.md`
- Estat: `pending`; no exportat. SHA-256 després de corregir l'abast:
  `039a5a490e77c548dc94504bcf5e635cd4be389530f0c5cf4f3baca8d981a4bc`.
- La font consultada és la síntesi de 2024 de les actes del Consell General.
  La fitxa `docs/fonts/actes-historiques-consell-general.md` registra copyright
  de l'autor i del Consell General i prohibició expressa de reproducció total o
  parcial. La unitat deriva molts detalls d'aquesta síntesi, de manera que no
  s'exporta sense permís o una determinació documentada que permeti reutilitzar
  el material.
- S'ha detectat una discrepància d'abast: l'article es presentava com la llista
  dels vint-i-vuit consellers que van aprovar la Constitució, però combina
  llistes d'assistents del 22-04-1992, 05-06-1992 i 05-03-1993. La síntesi situa
  l'aprovació del text a DCG 1-1993, 02-02-1993; la llista de març no pot provar
  qui va assistir-hi ni qui va votar. La taula també inclou dues persones
  titulades secretari general. S'ha canviat el títol i delimitat què demostra
  la font; el text no atribueix cap votació individual.
- La fitxa deixa registrat que no s'ha localitzat una llista nominal de la
  sessió del 02-02-1993 en la síntesi consultada. Queden sense auditar els
  recomptes i totes les afirmacions de detall. Revisió assistida per model;
  sense revisió humana.

## Unitat 18/20

- ID: `maia-docs/parla/oral/testimoni-constituent-jordiareny.md`
- Estat: `pending`; no exportat. SHA-256 revisat:
  `28f1073511e76c164cad3aff7c59d7a0782718e62683a1e4848277f556e48066`.
- La fitxa de la sèrie registra llicència estàndard de YouTube i cap permís de
  redistribució. L'article transcriu gairebé tota l'entrevista, de manera que
  no entra al corpus d'entrenament sense una base clara de reutilització.
- L'article mateix declara 65 marques d'ASR (9,4% dels mots) no verificades
  contra l'àudio. La revisió no l'ha escoltat; ser sota el llindar intern del
  10% no constitueix una verificació. No s'afirma que les marques siguin
  correctes ni que la veu sigui apte per a llengua.
- No s'exporta fins a resoldre els drets i verificar l'àudio. Revisió assistida
  per model; sense escolta ni revisió humana.

## Unitat 19/20

- ID: `maia-docs/temes/institucions/govern/la-llei-de-transparencia.md`
- Estat: `pending`; no exportat. SHA-256 després d'actualitzar el buit sobre
  l'article 12: `db2916299fe179ece5171796a13ef6b5aa8fbaf4f7e561104656d36cb2838353`.
- El text de la Llei 33/2021 guardat des del BOPA confirma que l'article 12
  també es va consultar: regula dades especialment protegides, 25 anys des de
  la mort o, si aquesta data és desconeguda, 50 anys des de la producció del
  document, manament judicial, ponderació i dissociació. S'ha corregit el buit
  fals que deia que l'article no s'havia llegit.
- No s'han tornat a verificar totes les afirmacions materials, les cerques i
  els recomptes de codis comunals, ni la vigència consolidada actual. L'article
  conserva una secció `Related`, que el contracte d'exportació no admet. Cal
  contrast complet amb localitzadors de disposició i neteja editorial abans
  d'aprovar-lo. Revisió assistida per model; sense revisió humana.

## Unitat 20/20

- ID: `maia-docs/temes/costums/danses/el-contrapas.md`
- Estat: `pending`; no exportat. SHA-256:
  `9ffa6e989ab881d90445236442306a90884c9c7bb852ecebb47f581657c8707c`.
- La decisió de drets i traçabilitat ja és al ledger (`rights-triage-premsa-01`)
  amb aquest mateix hash. L'article cita només «premsa andorrana», sense diari,
  data, titular ni enllaç; la fitxa general no autoritza redistribució. Per tant,
  no hi ha peça concreta per verificar-ne afirmacions com les tretze parts, la
  durada o el calendari anual, i no es pot incloure en un corpus distribuïble.
- Es compta com a unitat del pilot per elegibilitat/procedència; no com a
  revisió factual. No s'afegeix una segona decisió duplicada al ledger. Cal
  trobar fonts oficials o històriques reutilitzables i tornar a revisar el text.

## Tancament del pilot

Les vint unitats del pilot tenen ara decisió traçable amb hash d'entrada: vuit
aprovades per a coneixement i dotze pendents; cap de les vint s'ha marcat com a
revisada per una persona. Les vuit aprovades ja formen part de l'exportació de
`final-corpus/`. Les pendents romanen fora d'aquesta carpeta.

Les causes principals de retenció observades són: drets no resolts o
incompatibles amb redistribució; referències massa genèriques per identificar
la peça; transcripcions sense escolta/verificació; llistes que no proven la
conclusió que el títol els atribueix; vigència o aplicació actual no establerta;
i afirmacions que encara no s'han contrastat completament. La primera tanda de
50 unitats després del pilot és una triatge de perfils d'esportistes basats en
Viquipèdia, amb una decisió pròpia per persona i correspondència amb bolcat
local; cap perfil no s'ha aprovat només per aparèixer sota una categoria
andorrana.
