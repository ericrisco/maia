# `llengua-usos-linguistics/` — fons documental de llengua del Servei de Política Lingüística

Material de partida de les tandes de l'àmbit **llengua**. Tot ve de la pàgina
**«La llengua a Andorra»** del portal del Govern, llegida i desada el
**13-09-2026**:
`https://www.govern.ad/ca/tematiques/cultura-i-esports/llengua/parla-catala/la-llengua-a-andorra`

**Res d'aquesta carpeta no es versiona.** No és una decisió de mida: és una
decisió de **drets**. El portal del Govern reserva els drets i exigeix
autorització escrita per reproduir i distribuir; el DIEC2 prohibeix
expressament l'extracció i la reutilització del contingut de la seva base de
dades. Desar-ne els extractes complets en un repositori públic seria
redistribuir-los. Els fitxers es queden al disc i es tornen a baixar amb els
URL i els hash d'aquesta taula.

Fitxes de drets al harness, a `02-DOCS/raw/sources/`: `govern-ad.md`,
`spl-estudis-llengua.md`, `diec2-iec.md`.

## Peces baixades el 13-09-2026

Totes pengen de `https://www.govern.ad/documents/d/guest/<nom>?download=true`.

| Fitxer | Peça, tal com la titula el portal | SHA-256 |
| --- | --- | --- |
| `dialectalismes_nousdiec2.pdf` | Variants dialectals incorporades al DIEC2 | `4868a737…83b91` |
| `parlardandorra.pdf` | 2007, El parlar d'Andorra dels segles XVII i XVIII, Xavier Rull Muruzàbal | `f1971ba8…127b2` |
| `cu_22_web-indicador_dusos_linguistics_compressed-1-.pdf` | Coneixements i usos lingüístics de la població d'Andorra. Situació actual i evolució (1995-2022) | `3c781819…f95cf` |
| `coneixements_i_usos_llengua_2018.pdf` | …(1995-2018) | `c6ddee73…b7c54` |
| `coneixements_i_usos_llengua_2014.pdf` | …(1995-2014) | `c5f2f895…d77b6` |
| `coneixements2011.pdf` | …(1995-2009) | `a2e94e2f…b7f7c` |
| `2013_analisi_toponims_and.pdf` | 2013, Anàlisi fisiogràfica de topònims andorrans d'arrel preromana | `8f044cb3…80871` |
| `annexos_toponims_andorrans.pdf` | Annexos del mateix estudi. **És un ZIP, no un PDF**, tot i l'extensió amb què s'ha desat | `1f4209a7…e5f128` |
| `escenari_sociolinguistic.pdf` | 2010, L'escenari sociolingüístic de la població escolar d'Andorra, Estel Margarit i Viñals | `8202df7b…d3d8a1` |
| `jovesillengua.pdf` | 2006, Joves i llengües d'Andorra, Alexandra Monné Bellmunt | `546644f4…a6efe` |
| `model_us_catala.pdf` | 2008, Model sistèmic de l'evolució de l'ús del català a Andorra | `0f6dc140…a24d8` |
| `2017_us_terminologia_cat_andorra.pdf` | 2017, Ús de la terminologia catalana a Andorra: els esports d'hivern | `0aaa33a0…9abf92` |
| `andorra_llengues_identitats-pdf.pdf` | 2021, Andorra: llengües i identitats, Jordi Serra i Massansalvador | `3855a483…68f1a2` |
| `presentacio_indicador2022_10-11-2022_compressed-1-.pdf` | Presentació Indicadors | `a7dfa4ab…e39e68` |

`pagina-llengua-2026-09-13.html` i `.txt` són la captura de la pàgina d'origen,
i acrediten com el portal titula i data cada peça.

## Evidència de la consulta al DIEC2 (13-09-2026)

Generada amb `02-DOCS/raw/operations/lexic-diec2/consulta_diec2.py` (al
harness), que consulta el diccionari **mot a mot**, només amb els mots d'una llista donada.

| Fitxer | Què conté |
| --- | --- |
| `mots-llista-2007.txt` | Els 35 mots de la llista oficial del 2007, tal com s'han consultat |
| `diec2-verificacio-2026-09-13.json` | Resposta del diccionari per a cadascun |
| `diec2-subentrades-2026-09-13.json` | Consulta dels mots capçalera de les locucions (`casa`, `foc`, `raonador`, `tabac`, `botir`, `cap`) |
| `diec2-textos-2026-09-13.txt` | Les 51 accepcions llegides, en text pla |
| `diec2-abreviatures-completes.json` | Les 431 abreviatures del diccionari, recollides de les pàgines A–Z |
| `diec2-infolegal-2026-09-13.html` / `.txt` | L'avís legal, tal com es va llegir |

`diec2-textos-2026-09-13.txt` **és el fitxer que no pot sortir d'aquest disc**:
són accepcions senceres del diccionari. Als articles només hi passen **fets**
—si un mot hi és, amb quines marques— i **citacions curtes atribuïdes**.

## Estat de lectura

**Llegit i destil·lat:** `dialectalismes_nousdiec2.pdf` (3 pàgines, completes) i
la consulta al DIEC2 de la seva llista. `parlardandorra.pdf`, parcialment:
introducció (p. 7-12), lèxic (p. 101-110) i conclusions (p. 111-115).
`cu_22_web-indicador_dusos_linguistics_compressed-1-.pdf`, parcialment: p. 7,
10-12, 16, 38, 39-40, 41-42 i 44-45.

`2013_analisi_toponims_and.pdf`, parcialment: resum, prefaci, p. 91-95 i
p. 269-278. `andorra_llengues_identitats-pdf.pdf`, parcialment: p. 17-30,
102-103 i 389-395. `escenari_sociolinguistic.pdf`, parcialment: p. 19-20 i
63-84. `2017_us_terminologia_cat_andorra.pdf`, parcialment: p. 43-56, 65-72,
77-78 i 79-89. `model_us_catala.pdf`, parcialment: p. 116-125 i 137-144.

**Llegit i no destil·lat:** `coneixements_i_usos_llengua_2018.pdf`, només la
pàgina impresa 32.

**Avís:** `annexos_toponims_andorrans.pdf` **no és un PDF**. El portal el
serveix amb aquesta extensió i és un **ZIP** de 29 MB. Conté els annexos de
l'estudi de toponímia —les llistes dels 414 i els 174 topònims i les 81 fitxes
fisiogràfiques—, i **no s'ha obert**.

**Gràfics verificats sobre render a 300 ppp** (`cu22-*.png`), perquè de
l'extracció de text **es perd quina sèrie és quina**: llengua inicial (PDF p. 12),
indicador de coneixement (PDF p. 18) i indicador lingüístic (PDF p. 40).

**Baixat, no llegit:** la resta. Que un fitxer sigui en aquesta carpeta no
acredita cap lectura.

## Avís: el text extret de `parlardandorra.pdf` no és citable

`parlardandorra.txt` surt de `pdftotext -layout` i té **la lligadura «ti»
corrompuda**: el mateix parell de lletres hi apareix com a `-`, `4`, `5`, `7`,
`.`, `*` o `+` segons el context (*Fonè-ca* = Fonètica, *u4litzava* = utilitzava,
*Par.cules* = Partícules, *jus+cia* = justícia). **Serveix per localitzar
passatges, no per citar-los.** Les citacions del corpus s'han verificat sobre
`pag-*.png`, renderitzats a 150 ppp amb `pdftoppm`: pàgines PDF 11, 102, 105,
108 i 112 (impreses 10, 101, 104, 107 i 111).
