# `docs/raw/` — el material de partida

Aquí hi ha **els documents originals** de què surt el corpus. Fins ara vivien al
directori temporal de la sessió i **es perdien en acabar**; des d'ara tot el que
s'obre per treballar-hi baixa aquí.

**Regla:** *cap document de treball a `/tmp`. Tot a `docs/raw/`.*

## Què es versiona i què no

| Extensió | Al git? | Per què |
| --- | --- | --- |
| **`.txt`** (extractes de text) | **sí** | és **el que es llegeix i se cita**; són ~9 MB en total |
| `.pdf` | **no** | **250+ MB**, amb un fitxer de **50 MB**. GitHub avisa a partir de 50 MB i rebutja a partir de 100, i git guarda els blobs **per sempre**. Es queden al disc i es poden tornar a baixar amb els URL d'aquest registre |
| `.html`, `.json` (captures) | **no** | dumps de pàgina, voluminosos i reproduïbles des de l'URL |

**Això és una decisió tècnica, no una decisió sobre drets**, i **només afecta les
carpetes d'aquesta tanda**. En aquest repositori `docs/raw/` **es versiona** —
`sdd/ewa/carrera-modesto/` hi té els PDF comesos— i **aquell criteri no canvia**:
allà els fitxers són petits i aquí no.

> **Advertiment de drets, registrat aquí perquè quedi visible.** Totes les fitxes
> de `docs/fonts/` marquen aquestes obres amb **`redistribucio: pendent`**:
> són publicacions en **accés obert** consultables lliurement, **sense
> llicència explícita de redistribució**. Versionar-ne els extractes de text en
> un repositori públic **és un acte de redistribució**. Es fa per decisió
> expressa del responsable del projecte. **Si alguna d'aquestes institucions ho
> demana, s'ha de poder retirar**, i per això cada fitxer té aquí l'origen
> anotat.

## Com s'extreu el text

```bash
curl -sL --max-time 120 "<url>" -o fitxer.pdf
pdftotext -enc UTF-8 fitxer.pdf fitxer.txt
```

`WebFetch` **no serveix** per a aquests PDF: el Calaix i els arxius
parlamentaris els serveixen amb protecció anti-bot i tornen *Access Denied*.

---

## `sac-diades/` — Societat Andorrana de Ciències

**Font:** actes de les **Diades Andorranes a la Universitat Catalana d'Estiu**,
publicades per la **SAC** i consultables al **Calaix** de la Generalitat de
Catalunya.

- **Llicència:** publicació acadèmica en accés obert. **Redistribució: pendent.**
- **Patró d'URL:** `https://calaix.gencat.cat/bitstream/handle/10687/<handle>/x.pdf?sequence=1&isAllowed=y`
  El nom del fitxer del *bitstream* **és indiferent**: n'hi ha prou amb
  `?sequence=1`.
- **Fitxa de font del corpus:** [`societat-andorrana-ciencies`](../fonts/societat-andorrana-ciencies.md)
  i [l'article](../temes/cultura/museus-i-arxius/la-societat-andorrana-de-ciencies.md).

| Fitxer | Diada | Any | Handle Calaix |
| --- | --- | --- | --- |
| `02a-1989-els-moviments-migratoris-a-andorra` | 2a | 1989 | `427966` |
| `03a-1990-la-identitat-nacional` | 3a | 1990 | `427967` |
| `07a-1994-andorra-i-la-catalanitat` | 7a | 1994 | `427971` |
| `10a-1997-la-integracio-a-andorra` | 10a | 1997 | `427974` |
| `13a-2000-formacio-i-ensenyament-a-andorra` | 13a | 2000 | `427977` |
| `15a-2002-una-historia-dandorra-tematica` | 15a | 2002 | `427979` |
| `20a-2007-andorra-i-el-seu-capital-social` | 20a | 2007 | `427984` |
| `28a-2015-andorra-i-els-petits-estats-deuropa` | 28a | 2015 | `427986` |
| `29a-2016-el-canvi-climatic-i-andorra` | 29a | 2016 | `427988` |
| `31a-2018-el-parlamentarisme-andorra` | 31a | 2018 | **handle no verificat** |

**Els handles 1a-20a són consecutius des de `427965` (1a).** A partir d'aquí la
sèrie salta: `427985` = 27a, `427986` = 28a, `427988` = 29a, `427989` = 30a.
**Els volums 21a-26a no s'han localitzat en aquest rang.**

### Avisos per volum

- **`20a-2007`** — el PDF **no té capa de text**: està escanejat i
  `pdftotext` en treu **zero línies**. El `.txt` és buit a posta. **Necessita
  OCR.**
- **`31a-2018-el-parlamentarisme-andorra.txt`** — **reextret el 2026-09-13.**
  La primera extracció s'havia quedat a **1.192 línies** (fins a la pàgina 31
  del volum) i el corpus la va registrar com a «sumari». **No era un sumari: era
  una extracció truncada.** Refent `pdftotext` sobre el mateix PDF en surten
  **7.302 línies**, el volum sencer amb les **25 ponències**. El `.txt` s'ha
  substituït.
- **`31a-2018-...` — handle de Calaix NO VERIFICAT.** Comprovat el 2026-09-13:
  **`427989` és la 30a Diada**, no la 31a, i `427990` retorna una pàgina d'error.
  El PDF es conserva aquí i les fitxes de font el citen **per ISBN
  (978-99920-61-49-7) i per DOI (10.2436/15.8060.16.x)**, que sí que consten a
  cada pàgina. **Buit registrat: localitzar el handle.**
- **Volums dels anys 1989-2002** — digitalitzats amb **OCR de baixa qualitat**:
  hi ha confusions sistemàtiques (`ç`→`9`, `í`→`f`, `ó`→`6`, columnes barrejades,
  taules destruïdes). **Les citacions s'han de verificar contra l'original.**
- **Volums del 2015 i el 2016** — PDF **digitals amb capa de text neta**: les
  citacions són fiables caràcter a caràcter.

### El catàleg complet de les Diades

Extret de **la contraportada del volum de la 31a Diada (2018)**. Tanca un buit
que el corpus tenia registrat a
[la fitxa de la SAC](../temes/cultura/museus-i-arxius/la-societat-andorrana-de-ciencies.md).

| # | Any | Títol | Al `raw/`? |
| --- | --- | --- | --- |
| 1a | 1988 | Andorra, estat, institucions, societat | — |
| **2a** | **1989** | **Els moviments migratoris a Andorra** | **sí** |
| **3a** | **1990** | **La identitat nacional** | **sí** |
| 4a | 1991 | El futur d'Andorra | — |
| 5a | 1992 | Tendències polítiques a Andorra | — |
| 6a | 1993 | Alternatives econòmiques per a Andorra | — |
| **7a** | **1994** | **Andorra i la catalanitat** | **sí** |
| 8a | 1995 | El finançament de l'estat andorrà | — |
| 9a | 1996 | Andorra en el món | — |
| **10a** | **1997** | **La integració a Andorra** | **sí** |
| 11a | 1998 | Andorra i l'aprofitament dels recursos naturals | — |
| 12a | 1999 | L'ordenació del territori andorrà | — |
| **13a** | **2000** | **Formació i ensenyament a Andorra** | **sí** |
| 14a | 2001 | Andorra i la integració a la Unió Europea | — |
| **15a** | **2002** | **Una història d'Andorra, temàtica** | **sí** |
| 16a | 2003 | Andorra i els seus veïns del sud | — |
| 17a | 2004 | Els llindars òptims del creixement andorrà | — |
| 18a | 2005 | Andorra i els seus veïns del nord | — |
| 19a | 2006 | Els models de fiscalitat per a Andorra | — |
| **20a** | **2007** | **Andorra i el seu capital social** | **sí** (sense text) |
| 21a | 2008 | L'andorranitat | — |
| 22a | 2009 | L'energia a Andorra | — |
| 23a | 2010 | Andorra i els seus ciutadans | — |
| 24a | 2011 | L'aigua i Andorra | — |
| 25a | 2012 | Andorra i l'obertura econòmica | — |
| 26a | 2013 | La nacionalitat andorrana | — |
| 27a | 2014 | Models de país per a Andorra | — |
| **28a** | **2015** | **Andorra i els petits estats d'Europa** | **sí** |
| **29a** | **2016** | **El canvi climàtic i Andorra** | **sí** |
| 30a | 2017 | Andorra i l'acord d'associació amb la Unió Europea | — |
| **31a** | **2018** | **El parlamentarisme andorrà** | **sí** (sencer, 25 ponències) |

**Deu de trenta-una.** Les vint-i-una que falten són **la feina pendent més
gran i més ben delimitada que té el corpus**, i n'hi ha que van directes a
branques buides: *L'andorranitat* (21a), *L'aigua* (24a), *La nacionalitat
andorrana* (26a), *L'energia* (22a).

### `33a-2021-andorra-i-la-multiculturalitat/` — via nova d'accés

**Trenta ponències, una per fitxer.** Baixades el **2026-09-13** per un camí
diferent del Calaix, i **aquest camí canvia el que el corpus pot fer**:

```bash
curl -sL "https://doi.org/10.2436/15.8060.<volum>.<article>" -o article.pdf
```

**Els DOI de la SAC resolen directament al repositori de l'Institut d'Estudis
Catalans**, `publicacions.iec.cat/repository/pdf/<col·lecció>/<ítem>.pdf`,
**que no té la protecció anti-bot del Calaix**. Comprovat: la pàgina HTML del
Calaix retorna *«Making sure you're not a bot!»*; el DOI, el PDF.

**Volums localitzats per aquesta via** (prefix `10.2436/15.8060.`):

| Segment | Publicació |
| --- | --- |
| **10** | 13es Trobades Culturals Pirinenques — *Art i història al Pirineu* (2017) |
| **11** | Recull de conferències 2015 / Debats de recerca 9 |
| **12** | **30a Diada** — *Andorra i el tractat d'associació amb la UE* (2017) |
| **13** | 14es Trobades — *L'economia muntanyenca al Pirineu* (2018) |
| **15** | Recull de conferències 2016 / Debats de recerca 10 |
| **16** | **31a Diada** — *El parlamentarisme andorrà* (2019) |
| **17** | 15es Trobades — *Els usos del patrimoni al Pirineu* (2019) |
| **18** | Recull de conferències 2017 / Debats de recerca 11 |
| **19** | **32a Diada** — *L'economia circular i Andorra* (2020) |
| **20** | 16es Trobades — *Els Pirineus marítims* (2020) |
| **21** | Recull de conferències 2018 / Debats de recerca 12 |
| **22** | **33a Diada** — *Andorra i la multiculturalitat* (2021) |
| **23** | 17es Trobades — *Aliances territorials pirinenques* (2021) |
| **24-26** | Recull de conferències 2019-2020 / Debats de recerca 13 |
| **27** | **34a Diada** — *Els boscos andorrans* (2022) |
| **28** | 18es Trobades — *Accions dinamitzadores al Pirineu* (2022) |
| **30** | Recull de conferències 2021 / Debats de recerca 14 |
| **32** | **35a Diada** — *L'àrea funcional Andorra-Pirineus* (2023) |
| **34** | 20es Trobades — *La protecció del territori pirinenc* (2024) |
| **35** | 39è Cicle de conferències 2023 |
| **36** | *Aigua: desafiaments i oportunitats* — Debats de recerca 16 (2025) |
| **37** | **37a Diada** — *La globalització i Andorra* (2025) |
| **38** | 21es Trobades — *Conflictes bèl·lics al Pirineu* (2025) |

**Això vol dir que el corpus té accés a les Diades 30a-37a i a nou volums de
Trobades Culturals Pirinenques** que no eren al Calaix ni estaven localitzats.
**El segment 16 confirma, a més, el DOI del volum del parlamentarisme**, el
handle Calaix del qual segueix sense verificar.

**Buit registrat:** els segments **1-9**, **14**, **29**, **31**, **33** i
**39+** no s'han resolt o no s'han identificat. **Les Diades 1a-29a segueixen
sense via per aquest camí.**

---

## `lleis/` — la legislació andorrana vigent

**Cent quatre normes en text consolidat**, baixades el **2026-09-12** de
**[Jurisprudència.ad](https://jurisprudencia.ad/lleis-andorra)**. De la
**Constitució de 1993** a la **Llei 2/2026**.

- **Fitxa de font del corpus:** [`jurisprudencia-ad`](../fonts/jurisprudencia-ad.md).
- **Redistribució: sí**, i és l'única carpeta d'aquest `raw/` que ho té clar. El
  text normatiu és **norma oficial andorrana**, pública per naturalesa; el que hi
  afegeix la font és **la consolidació**, i aquesta feina és del responsable del
  projecte.
- **Capçalera de cada fitxer:** títol, URL d'origen, nombre d'articles, nombre de
  versions consolidades i **data i hora de la instantània**.

| | |
| --- | --- |
| Fitxers | **104** |
| Articles declarats | **8.956** |
| Lleis qualificades | **17** |
| Instantània | **2026-09-12** |

### L'avís que ha d'anar amb aquesta carpeta

**Una instantània no és la llei.** La llei canvia i la foto no. Cap afirmació
sobre dret vigent es resol contra aquests fitxers: es resol **contra la font**.
El corpus cita **l'article i la data de la foto**.

### El defecte de l'extracció, i com es va tancar

**La primera baixada va sortir un terç buida i no ho semblava.** 2.966 dels
8.956 articles van quedar amb el cos substituït per un marcador de la forma
`$1e`, `$20`, `$28`: capçalera de l'article intacta, text desaparegut. Només
**dos fitxers dels 104** en sortien nets. Els més afectats eren
`codi-procediment-civil` (137 articles), `organitzacio-entitats-financeres`
(105) i `seguretat-social` (97); la **Constitució** en tenia **cinc** —els
articles **45, 46, 56, 68 i 80**, l'últim el que delimita els Comuns.

**La causa era de la baixada, no de la font.** El lector llegia les
continuacions de text de la pàgina buscant-les després d'un salt de línia, i la
font no sempre n'hi posa: quan una continuació anava enganxada al final de
l'anterior, se la saltava.

**Reextret el 2026-09-12** amb el lector corregit:

| | Primera passada | Ara |
| --- | --- | --- |
| Normes | 104 | **104** |
| Articles amb cos | 5.990 | **8.956** |
| Marcadors sense resoldre | 2.966 | **0** |
| Mida | 3,9 MB | **11 MB** |

**Buit tancat.** Queda escrit perquè és un error que no crida l'atenció: un
corpus amb un terç dels articles buits té la mida, els títols i la numeració
correctes, i s'indexa com un corpus sencer.

L'**índex complet de les 104 normes**, amb el repartiment per branques i els
articles i versions de cadascuna, és a
**[`lleis/README.md`](lleis/README.md)**.

---

## `llibres/` — obres impreses

| Fitxer | Què és | Estat de la procedència |
| --- | --- | --- |
| `vilar-andorre-1904` | Obra sobre Andorra, **1904** | **URL no registrada.** Cal reconstruir-la |
| `andre-vilar-andorre` | Variant de la mateixa obra | **URL no registrada** |
| `brutails-coutume` | **J.-A. Brutails**, sobre el costum andorrà | **URL no registrada** |
| `la-cuestion-de-andorra-1894` | *La cuestión de Andorra*, **1894** | **URL no registrada** |

**Aquests fitxers venen de sessions anteriors i l'URL exacte no consta.** El
corpus **no se l'inventa**: queda com a **buit de procedència a tancar** abans
que cap d'aquests textos entri en un conjunt d'entrenament.

---

## `academic/` — tesis i articles

| Fitxer | Què és | Estat de la procedència |
| --- | --- | --- |
| `becat-these-l2` | Tesi de **Joan Becat** | **URL no registrada** |
| `becat-transhum` | Becat, sobre transhumància | **URL no registrada** |
| `herencia-andorra` | Sobre l'herència a Andorra | **URL no registrada** |
| `madriu-neolithic` | Neolític a la vall del **Madriu** | **URL no registrada** |
| `neolithic-pastoralism-pyrenees` | Pastoralisme neolític al Pirineu | **URL no registrada** |
| `transhumance-andorra-fcm` | Transhumància a Andorra | **URL no registrada** |

Mateixa nota: **procedència a reconstruir**. Els metadades d'OpenAlex i
Crossref que es van descarregar són a `web/` i **poden servir per tancar-ho**
(`openalex-madriu.json`, `openalex-transhum.json`, `crossref-transhum.json`).

---

## `hemeroteca/` — premsa i diaris de sessions

Material sobre **la crisi andorrana de 1894-1895** i el debat parlamentari
espanyol que va provocar.

| Grup | Què és | Origen |
| --- | --- | --- |
| `congreso-*` | **Diari de sessions del Congreso de los Diputados**, juny de 1895, amb apèndixs | Arxiu històric del Congreso (**URL exacta no registrada**) |
| `senado-1895-*` | **Diari de sessions del Senado**, juny de 1895 | Arxiu del Senado (**URL exacta no registrada**) |
| `boletin-leon-1894-09-17` | Butlletí provincial, 17.09.1894 | **URL no registrada** |
| `heraldo-1895-06-27-p2`, `correspondencia-1895-06-27` | Premsa espanyola del **27 de juny de 1895** | Hemeroteca Digital de la **BNE** (**URL no registrada**) |
| `bpt-*` | *Bulletin* francès, 1878-1893 | **Gallica / BnF** (**URL no registrada**) |
| `12052025` | Document del **12.05.2025** | **URL no registrada** |

**La procedència d'aquesta carpeta és parcial, i el 2026-09-12 ho és menys.**
Els diaris de sessions **s'identifiquen sols**: porten capçalera, número de
diari, data de sessió i pàgina, i això és **signatura suficient per citar-los**
encara que falti l'URL de descàrrega.

| Fitxer | Identificació verificada |
| --- | --- |
| `congreso-1895-06-17` | Congrés, **núm. 148**, sessió de **dilluns 17 de juny de 1895** |
| `congreso-157` | Congrés, **núm. 157**, sessió de **dissabte 29 de juny de 1895** |
| `congreso-1895-06-30` | Congrés, **núm. 158**, sessió de **diumenge 30 de juny de 1895** |
| `congreso-1895-ap40` | **Apèndix 40 al núm. 89** — l'addició signada el **27 de març de 1895** |
| `congreso-153-ap2`, `congreso-157-ap2` | Apèndixs **2n** als núm. **153** i **157** |
| `boletin-leon-1894-09-17` | **Boletín Oficial de la provincia de León**, núm. 34, **17 de setembre de 1894** |
| `12052025` | **No és premsa.** És l'acta d'una **Junta de Govern comunal** del **12-5-2025**, exp. 2025/2714. **Està mal classificat en aquesta carpeta** |

**Ja tenen fitxa de font:** els diaris de sessions del Congrés, a
[`diario-sesiones-corts-1895`](../fonts/diario-sesiones-corts-1895.md).

**Dos fitxers `.txt` són buits** —`senado-1895-06-29` i
`correspondencia-1895-06-27`—: els PDF no tenen capa de text i **necessiten
OCR**. El del Senat és, precisament, **on hauria de constar el desenllaç** de la
qüestió duanera.

**Avís de lectura:** aquests diaris van **a dues columnes**, i el text pla que en
surt les barreja línia a línia. Llegits seguits **fabriquen frases que ningú no
va dir**. S'han de reconstruir columna a columna abans de citar-ne res.

---

## `web/` — captures i extractes

Dumps de pàgines i respostes d'API. **Cap d'aquests fitxers és citable tal
com està**: són material de cerca, no fonts.

| Grup | Què és |
| --- | --- |
| `ram-*.html`, `ramaderia-*` | Fitxes i vídeos sobre **ramaderia i transhumància** andorranes |
| `elperiodic-*`, `bondia-*` | Premsa andorrana en línia |
| `andorra_nomenclator.html`, `andorra_ide_wms_urls.txt`, `andorra_toponym_*` | **Nomenclàtor** i serveis cartogràfics d'Andorra |
| `andorra_stats_*.json` | **Departament d'Estadística d'Andorra** |
| `andorra_opac_index.html`, `andorra_openlibrary_candidates.json` | Catàlegs bibliogràfics |
| `openalex-*.json`, `crossref-*.json` | Metadades bibliogràfiques |
| `grazing-andorra.html`, `pastorclim.html`, `transhum-unesco.html`, `camins.html` | Pastura, clima i **Madriu-Perafita-Claror** (Unesco) |
| `pujal-rtva.html` | **RTVA** |
| `andosins.txt`, `fhasa.txt`, `jueus.txt`, `lluita.txt`, `voc.txt` | Extractes de treball de sessions anteriors |

---

## Estat del registre

| Carpeta | Procedència completa? |
| --- | --- |
| `lleis/` | **sí** — font, URL, llicència, redistribució i instantània datada; contingut complet i verificat |
| `sac-diades/` | **sí** — institució, llicència, handle i patró d'URL |
| `llibres/` | **no** — falta l'URL de les quatre obres |
| `academic/` | **no** — falta l'URL de les sis |
| `hemeroteca/` | **parcial** — els diaris de sessions s'identifiquen per número, data i pàgina i ja tenen fitxa; falta l'URL, i la premsa i els `bpt-*` segueixen sense signatura |
| `web/` | **parcial** — s'identifica l'origen, no l'URL exacta |

**Aquest quadre és, ell mateix, la llista de feina.** La regla del projecte
demana **registrar la procedència i els termes d'ús de cada font abans que
entri en un conjunt d'entrenament**, i ara mateix **només `lleis/` i
`sac-diades/` hi compleixen**.
