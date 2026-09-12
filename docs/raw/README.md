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
- **`31a-2018-...-sumari.txt`** — no és el volum sencer sinó **el sumari
  extret**, que és el que es va poder llegir.
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
| **31a** | **2018** | **El parlamentarisme andorrà** | **sí** (sumari) |

**Deu de trenta-una.** Les vint-i-una que falten són **la feina pendent més
gran i més ben delimitada que té el corpus**, i n'hi ha que van directes a
branques buides: *L'andorranitat* (21a), *L'aigua* (24a), *La nacionalitat
andorrana* (26a), *L'energia* (22a).

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

**Tota aquesta carpeta té la procedència incompleta.** Són fonts d'arxiu
públiques i identificables, però **el corpus no pot citar-les amb rigor fins
que no en tingui l'URL i la signatura**. Cap d'aquests materials ha generat
encara fitxa de font.

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
| `sac-diades/` | **sí** — institució, llicència, handle i patró d'URL |
| `llibres/` | **no** — falta l'URL de les quatre obres |
| `academic/` | **no** — falta l'URL de les sis |
| `hemeroteca/` | **no** — falten URL i signatures |
| `web/` | **parcial** — s'identifica l'origen, no l'URL exacta |

**Aquest quadre és, ell mateix, la llista de feina.** La regla del projecte
demana **registrar la procedència i els termes d'ús de cada font abans que
entri en un conjunt d'entrenament**, i ara mateix **només `sac-diades/` hi
compleix**.
