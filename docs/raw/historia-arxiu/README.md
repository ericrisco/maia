# Evidència — història i arxiu (BOPA)

Peces del **Butlletí Oficial del Principat d'Andorra** descarregades el
**2026-09-13** per a l'àmbit *història i arxiu*. Drets registrats **abans** de
llegir res, a [`02-DOCS/raw/sources/bopa-ad.md`](../../../../02-DOCS/raw/sources/bopa-ad.md)
i a la fitxa de corpus [`bopa-ad`](../../fonts/bopa-ad.md): les condicions
generals d'utilització de la seu electrònica permeten còpia, extracció i
distribució conservant el sentit i les metadades. **Redistribució: sí.** No es
reutilitzen logotips, elements gràfics ni la presentació del portal, i res d'això
no implica suport del Servei del BOPA al projecte.

## Com s'ha obtingut

El portal és una aplicació de JavaScript; el cercador crida
`POST https://bopaazurefunctions.azurewebsites.net/api/GetPaginatedDocuments2Indexes`
amb el cos `{textSearch, temaFilter, dateFilter, organismeFilter, butlletiFilter,
anyFilter, size, skip, orderBy, searchMode}`, i `searchMode: 2` és la cerca
exacta. El resultat dona, per a cada document, l'URL de l'HTML al magatzem
`bopadocuments.blob.core.windows.net`. **Cap credencial, cap sessió, cap
endpoint privat.** L'script de consulta és a
`02-DOCS/raw/operations/bopa/` i fa una crida per cerca.

**Avís d'evidència: la codificació no és uniforme.** Una part dels fitxers són
**UTF-16 amb BOM** i la resta UTF-8. Llegir-los tots com a UTF-8 produeix
mojibake silenciós —no un error—, i és així com una primera extracció va donar
text il·legible per a dos documents. Els `.txt` d'aquesta carpeta s'han generat
detectant el BOM.

## Peces

| Fitxer | Què és | BOPA | SHA-256 |
| --- | --- | --- | --- |
| `CGL20171117_10_06_59` | **Llei 20/2017**, del 27 d'octubre, de drets i deures dels usuaris i dels professionals del sistema sanitari i sobre la història clínica | 75/2017, 21-11-2017 | `f9b3e40dd73bbce3f8f4c4683eb039471591544c0eecb2d107cf941b36e9880b` |
| `CGL20211222_11_55_16` | **Llei 33/2021**, del 2 de desembre, de transparència, accés a la informació pública i govern obert | 141/2021, 28-12-2021 | `4f8b6076d342f37a67f660ed83f089a2fa3c4a897de8807862b2fec3104a3d53` |
| `CGL20220210_13_54_38` | **Llei 4/2022**, del 31 de gener, del pressupost per al 2022 (disposició final desena) | 21/2022, 14-02-2022 | `ec19f2a303789890852bd71630a50b641032a19a9ef57ca025572286336d9221` |
| `GV20220927_13_36_39` | Avís del 26-9-2022, **dissolució de la CAAD** | 115/2022, 27-09-2022 | `02e0eb415bd00a2593fb3cfaa2089f61d509aff08b551888b13d6fb0b303c663` |
| `GN20220927_13_35_20` | Edicte del 26-9-2022, **nomenament dels membres de la CNAAD** | 116/2022, 28-09-2022 | `36a69ab70c1a5b3c0f37edfcc4c1af73952902aeaa170bd437d00fde62c1374f` |
| `GD20221110_09_11_32` | **Decret 455/2022**, reglament d'organització i funcionament de la CNAAD | 135/2022, 15-11-2022 | `2dd385537cc366c66dfe405d60f576d6bdeb104f17b473f6cf5b65a4f3b6bb2e` |
| `GR20221115_14_25_44` | **Decret 454/2022**, reglament del procediment d'accés a la informació pública | 135/2022, 15-11-2022 | `1967919c68fad148a009fd61f850648e783a4162d045c0e278b345af46d6f6d0` |
| `GV20230320_11_03_31` | **Edicte 17-3-2023** · resolucions CNAAD · TNAAD 01–06/2023 | 39/2023, 20-03-2023 | `82a1de216f779a124c0e6f0982ce87e9b5aeb7ea29106355a6c8045cbb791ef3` |
| `GD20230316_12_13_37` | **Decret 121/2023**, política de gestió de l'expedient i el document electrònics | 40/2023, 21-03-2023 | `55eee9ac5008902c352a6e7e490c6eaa320018f8f38d8a7e9e0243bbd1f117fb` |
| `GV_2023_06_30_12_25_47` | **Edicte 29-6-2023** · TNAAD 06(→11), 07–10/2023 | 84/2023, 04-07-2023 | `ddf177f9908511f87f66108eaefea6b9d8987b264f2632168eff2f7443a06a8c` |
| `GV_2023_10_16_12_24_05` | **Correcció d'errata 11-10-2023**: TNAAD 06/2023 duplicat → 11/2023 | 125/2023, 17-10-2023 | `e37edd2be7f50e2b24c7a0391934b81663e45cc1dc8e64e11b9d71bca7d7db00` |
| `GD_2023_11_15_13_54_39` | Codi de conducta dels membres del Govern i alts càrrecs | 143/2023, 16-11-2023 | `88a210be70293b186d366935c36bcc87779d06da58829003014c1b43be6d644c` |
| `GV_2024_07_08_08_45_26` | **Edicte 8-7-2024** · TNAAD 001–006/24 | 79/2024, 09-07-2024 | `0e7e2895ccd79a87599f713aeb82539da35ba97699343acd7596271d751756a6` |
| `GV_2024_11_22_14_58_50` | **Edicte 22-11-2024** · TNAAD 007–017/24 | 132/2024, 26-11-2024 | `c9c63c3704b085f0c31ba01eb8cc39d2ead1d477fe11af49cefcac1399bb93da` |
| `GV_2025_04_17_08_36_50` | **Edicte 16-4-2025** · TNAAD 001/25 | 47/2025, 22-04-2025 | `7906d7d24216422fcc20002150fd1354764d061918726a398c30f832ddb233de` |
| `GV_2025_11_18_09_50_20` | **Edicte 18-11-2025** · TNAAD 002–004/25 | 139/2025, 18-11-2025 | `4697aa3145b72e2c22279eeac5691df5752d61c244f1f7da9fa0d1b4434b7757` |
| `3C6BA` | **Decret del 6-4-2005**, Reglament de l'Arxiu Nacional d'Andorra | 2005, 12-04-2005 | `ee5f42588f3fe2151819a5a0757600f9877b9ccd52f4a9d067f080bcfde027c0` |
| `3C67A` | **Decret del 6-4-2005**, Reglament del Sistema d'Arxius i de l'Àrea d'Arxius del Govern | 2005, 12-04-2005 | `0ca9e2689cdf4014b2a6222e3b3540e589ad3fe374d2b36f737dfa7446534440` |
| `GD20230223_11_26_40` | **Decret 90/2023**, del 22-2-2023, d'arxiu qualificat | 2023, 28-02-2023 | `7ab842248bd7af9cd14a352f6894399ab50fa9b044515debb12ef05ffefb4ad4` |
| `30396` | Decret del 17-9-2003, Reglament de l'Arxiu Comunal **d'Encamp** | 2003, 23-09-2003 | `7cc69565f0d791a0603981dbb65ee425839cd93b626847c7e363fdc6b73f26cb` |
| `7DD7E` | Reglament del 21-3-2013, Servei d'Arxiu del Comú de **Canillo** | 2013, 02-04-2013 | `155a3b05daed5721bca3df6ea5a17b32caa2235d9af9a441948b3ffe150dab78` |
| `826C2` | Reglament del 31-10-2013, Arxiu Comunal d'**Ordino** | 2013, 12-11-2013 | `8ca729ff4fc85a2a53fd4ed620d3f983d13ff32a524b68f2a4b9294de28adcbc` |
| `QXO20190617_11_13_04` | Reglament del 14-6-2019, Servei d'Arxiu del Comú d'**Escaldes-Engordany** | 2019, 18-06-2019 | `637cbf7030df71ec14bcdbad2e17535b522ea9f68827a6a28f0cae3dcd57d852` |
| `QAD20230525_12_19_52` | Reglament de l'1-6-2023, Arxiu Comunal d'**Andorra la Vella** | 74/2023, 06-06-2023 | `d826b29b35fffaa97638a52282e15c524eedb9187d2f29b29a0f025cff14d0f0` |
| `QOO_2024_05_30_09_25_40` | Reglament del 30-5-2024, Servei d'Arxiu Comunal d'**Ordino** | 2024, 05-06-2024 | `6b3fa3a515d029a79acf559865f4670efa4bbc3c03f07495c038892186b5593d` |
| `QCO_2024_09_19_15_40_33` | Reglament del 17-9-2024, Arxiu Comunal de **Canillo** | 2024, 24-09-2024 | `12c0d752f597c2364be11cd08bd9a2f73054431e5b86e7762a2c4803c0f4b450` |
| `QOV_2023_09_14_11_00_54` | Plec de clàusules del Comú d'**Ordino** que remet l'avaluació documental a la CNAAD | 111/2023, 19-09-2023 | `1fbbc35418a961b52e28a82fdaef4dcc03665c7b2d8e12f8381713e598630c82` |
| `GD20160422_09_32_37` | **Decret del 20-4-2016**, modificació parcial del Reglament de l'Arxiu Nacional (arts. 7.o, 19.2, 19.3, 26, 31, 41, 42 i 43) | 2016, 26-04-2016 | `3f071985ad571ad8a8bec29ae06346eda09b607eaacadf79c0bf7005f18770ab` |
| `67AAA` | **Decret del 15-9-2010**, Reglament de transferències de documents del Govern d'Andorra | 2010, 21-09-2010 | `c663074ad3370345f2fb368aa1ed898ea0f705fba1bc180f0413a747142a88c4` |
| `1655A` | **Reglament organitzatiu de la CAD**, del 8-7-1998 (article 3.3: res anterior a l'1-1-1984 no s'avalua) | 1998, 28-07-1998 | `52ab6c839530ddeee7c3eaabeb23cb68a6176325fe77eb6e1f9be2951f259038` |
| `ga26036024` | **Decret de l'11-6-2014**, refà sencer el Reglament de la CAD i el deroga (article 3.5 manté la data del 1984; 114 sèries avaluades) | 2014, 17-06-2014 | `8ca1a7dc0ada3b1c97c4bdd7f04bf0d4842c9fc25e719093d894e698e43ce70d` |
| `ga26057026` | Decret del 24-9-2014 pel qual es publica el Decret de l'11-6-2014 | 2014, 30-09-2014 | `7b24909c0a52fe909fb173c6d683bea0564da092c1aea21cdfe4c42d7ccd462c` |
| `86A1E` | Edicte del 29-5-2014, formació de la Comissió permanent d'avaluació de la documentació | 2014, 10-06-2014 | `db72bc24a845d01c0b54834dab676b8479aeabe97976f02739b478dcfee89558` |
| `GV20150626_09_17_13` | **Edicte del 25-6-2015**, taules d'avaluació de la CAD | 2015, 30-06-2015 | `a47878b1ee34bedb91865f7da76108e94fcb57740aded674f3cdd05128049531` |
| `GV20160603_12_31_51` | **Edicte de l'1-6-2016**, taules d'avaluació de la CAD | 2016, 07-06-2016 | `0184ab687a5b8fe5b5ea7089a675014937aff82ab1f7366408e7e20b22923527` |
| `GV20170209_11_51_41` | **Edicte del 8-2-2016**, taules d'avaluació de la CAD | 2017, 14-02-2017 | `77bbac5c4d1f74a8891cc477550abb2fa301f904dbbe19fea6f10348ba293010` |
| `GF20150910_13_18_12` | Avís del 9-9-2015, nomenament dels membres de la **CAAD** | 2015, 15-09-2015 | `7230bc3704e576a7cf9f1955a97dd1343ac608e124c347879a8148daec3d9c9b` |
| `GD20151105_16_39_43` | **Decret del 4-11-2015**, Pla director de preservació dels objectes digitals del Govern | 2015, 10-11-2015 | `7c8e2f6fac4253e3a8c3a8abd9ef11c6068de618f97501dc5bcf8e83d7a33f97` |
| `GV20201214_14_24_47` | Edicte del 9-12-2020 pel qual es publiquen les taules d’avaluació documental. | — | `11cd5e7b7d0e5cc37e30ca71e02c33cc13c458cb37526759c4900295b444e143` |
| `GV20210121_12_38_27` | Edicte del 20-1-2021 pel qual es publiquen les taules d’avaluació documental. | — | `cb736c0982a69945cc896c6282d3115c7c8b36309fafd21099d627d1e71f5cdc` |
| `GV20210305_10_39_20` | Edicte del 3-3-2021 pel qual es publiquen les taules d’avaluació documental. | — | `be6ba474480266aa302085cd889940721d0834f515230a8964bb20845b79808c` |
| `GV20210426_11_18_59` | Edicte del 21-4-2021 pel qual es publiquen les taules d’avaluació documental. | — | `6c594cf4809dcae9a6ae654455dd0cfe79ff347fa0dd7f32def57398cc2bb1ee` |
| `GV20210528_09_46_51` | Edicte del 26-5-2021 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació d | — | `d747b991e3b42389b2ec2045fc921d916a891c1f1c17755ce62601e1e8f882f1` |
| `GV20210618_11_58_09` | Edicte del 16-6-2021 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació d | — | `cdf22af5b2ba13a9ec63e2a685f44aea48d2e4fcb85a2113112d5d3e44f8ab4e` |
| `GV20210722_10_32_33` | Edicte del 21-7-2021 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació d | — | `fa9fad092289ce7482e25fddd0eed20f881912be1c2ecc3b5a47fe8745222c85` |
| `GV20210819_11_03_19` | Edicte del 18-8-2021 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació d | — | `11d2fc54deeae9b051b3ba04b9254e545778ae7b1b607827fc8cbbf13c40c949` |
| `GV20211022_10_04_25` | Edicte del 20-10-2021 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació  | — | `d53bf42db825e07a257b13b1a4d63c3cf688347d035c937c27cf3b6318a3b155` |
| `GV20211202_14_36_17` | Edicte de l’1-12-2021 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació  | — | `f9eefeb7ca38984219b1446d04b0cbc715f56137ecb06e9e8e71a5094b58c905` |
| `GV20220107_10_39_52` | Edicte del 5-1-2022 pel qual s’aproven les taules d’avaluació documental. | — | `87266decf119bc56129adb9b5e88eb234d83f96517a423d07eb1ad1bcfdc2bdc` |
| `GV20220304_09_26_16` | Edicte del 2-3-2022 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació de | — | `3ad12f1015e749d2edd93a52787719d0d5a481b05cb92020a3831ff361d180ac` |
| `GV20220331_16_54_19` | Edicte del 30-3-2022 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació d | — | `6fcce8e04cd31157e4f3bda717a70608cec93870b7db2b94374dad93006f5a54` |
| `GV20220428_15_43_07` | Edicte del 27-4-2022 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació d | — | `37449f38791634ce152d4ae5ad4f7bbb19759dba0cae9a4ba17f0bd7c7f04cd2` |
| `GV20220527_09_21_27` | Edicte del 25-5-2022 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació d | — | `bcf29813b3473cdcded829bdf19e6f15221df1a64e40ab3c599d7c30cfa6b6cf` |
| `GV20220714_12_06_16` | Edicte del 13-7-2022 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació d | — | `af560c816a9d17a2a39c05285718aa2fbfaeff62ce72b5fe6f1ac01fd1060e84` |
| `GV20221010_11_38_08` | Edicte del 5-10-2022 pel qual es publiquen les resolucions de la Comissió d’Accés i Avaluació d | — | `08064ccd83dcc1305f08b46efee8b9edb42115a8c7fc77cdb6de89e743b94fbf` |
| `QCD20160303_09_17_21` | Edicte de 29-2-2016 de publicació de les taules d’avaluació establertes per la Unitat d’Avaluac | — | `ae3fcf65838da56450d4363ea5485b02be70e7f5f363e9e928bc2ffac58c5a76` |
| `cnaad-cerca-bopa.json` | Resultat cru de la cerca «Comissió Nacional d'Accés i Avaluació de la Documentació» (`totalCount` 21) | — | — |
| `taules-avaluacio.json` | Les **32 taules d'avaluació documental** extretes dels sis edictes | — | — |

Cada peça té el `.html` original i el `.txt` extret. **El `.txt` és derivat: la
citació es resol contra l'HTML**, i l'HTML contra el BOPA.

## Lectures que en surten

- [La llei que deia que es conservava tot](../../temes/cultura/museus-i-arxius/la-llei-que-deia-que-es-conservava-tot.md)
- [Sèries senceres, no](../../temes/cultura/museus-i-arxius/series-senceres-no.md)
- [Res d'anterior al 1984 no es tria](../../temes/cultura/museus-i-arxius/res-danterior-al-1984-no-es-tria.md)
- [Abans ho decretava el Govern](../../temes/cultura/museus-i-arxius/abans-ho-decretava-el-govern.md)

## Buits d'aquesta carpeta

- **La cerca del BOPA no és un cens.** `totalCount` 21 per a la cadena exacta
  «Comissió Nacional d'Accés i Avaluació de la Documentació» i disset documents
  retornats amb `size` 50. **No s'ha establert per què el recompte i els
  retornats no coincideixen**, i per tant **no es diu que aquests siguin tots
  els documents que existeixen**.
- **Cap PDF oficial descarregat.** L'evidència és l'HTML del magatzem del BOPA;
  la paginació de la publicació en paper no consta per a la majoria de peces.
- **La vigència s'ha de cercar, no llegir.** El Decret del 6-4-2005 no anuncia la
  seva pròpia modificació del 2016; només apareix cercant el BOPA pel títol del
  reglament. **Una primera lectura feta sobre el text original era errònia en
  cinc punts.** Per a qualsevol altre decret d'aquesta carpeta, la comprovació
  de modificacions **encara no s'ha fet**.
- **Memòries anuals de la CNAAD**: l'article 26.8 de la Llei 33/2021 i
  l'article 5.6 del Decret 455/2022 les fan obligatòries. **Cap no s'ha
  localitzat al BOPA.**
