# `web/esport/` — captures sobre esport andorrà

**Captures de la Viquipèdia en anglès**, baixades el **2026-09-13**, per obrir la
branca d'esports, que era la més buida del corpus.

| Fitxer | URL |
| --- | --- |
| `andorra_at_the_olympics.html` | `https://en.wikipedia.org/wiki/Andorra_at_the_Olympics` |
| `2025_games_of_the_small_states_of_europe.html` | `https://en.wikipedia.org/wiki/2025_Games_of_the_Small_States_of_Europe` |
| `joan_verdu_alpine_skier.html` | `https://en.wikipedia.org/wiki/Joan_Verdú_(alpine_skier)` |
| `irineu_esteve_altimiras.html` | `https://en.wikipedia.org/wiki/Irineu_Esteve_Altimiras` |
| `monica_doria.html` | `https://en.wikipedia.org/wiki/Mònica_Dòria` |
| `nahuel_carabana.html` | `https://en.wikipedia.org/wiki/Nahuel_Carabaña` |

## Avisos

- **`Andorra at the Summer Olympics` i `Andorra at the Winter Olympics`
  redirigeixen tots dos a `Andorra at the Olympics`.** S'havien baixat per
  separat i s'han esborrat perquè eren el mateix fitxer.
- **Llicència CC BY-SA 4.0**, redistribuïble amb atribució i amb clàusula de
  compartir igual.
- **Font secundària.** Vegeu la fitxa
  [`wikipedia-esport-andorra`](../../../fonts/wikipedia-esport-andorra.md) per al
  criteri amb què s'usa: **serveix per a l'estructura i les xifres, i totes
  s'han de substituir per la font primària** (Comitè Olímpic Andorrà, FIS,
  World Athletics, ICF).

## Captures del 12 de setembre del 2026 — les altres competicions

**Els `.html` són al `.gitignore`; els `.txt` són l'extracció i és el que es
versiona.**

| Fitxer | D'on surt | Llicència |
| --- | --- | --- |
| `paralimpics` | https://en.wikipedia.org/wiki/Andorra_at_the_Paralympics | CC BY-SA 4.0 |
| `mediterranis` | https://en.wikipedia.org/wiki/Andorra_at_the_Mediterranean_Games | CC BY-SA 4.0 |
| `jocs-europeus` | https://en.wikipedia.org/wiki/Andorra_at_the_European_Games | CC BY-SA 4.0 |
| `p2002` … `p2022` | `Andorra_at_the_<any>_Winter_Paralympics` | CC BY-SA 4.0 |
| `p2012s` | `Andorra_at_the_2012_Summer_Paralympics` | CC BY-SA 4.0 |
| `hivern/w1980` … `hivern/w2014` | `Andorra_at_the_<any>_Winter_Olympics` (1980, 84, 88, 92, 94, 98, 2002, 06, 14) | CC BY-SA 4.0 |
| `llovera`, `llovera-en` | Albert Llovera, ca i en | CC BY-SA 4.0 |
| `linan-ana`, `reconeixement-doria-linan` | https://www.anaesports.ad/ | **drets reservats — citació breu** |
| `linan-diariandorra` | https://www.diariandorra.ad/ | **drets reservats — citació breu** |

## Una URL que no existeix, registrada

`en.wikipedia.org/wiki/Andorra_at_the_Youth_Olympic_Games` **no existeix**,
tot i que la pròpia plantilla d'equips nacionals d'Andorra hi enllaça. **Andorra
va als Jocs de la Joventut i no hi ha article.**

## Les correccions que aquestes captures han obligat a fer

1. **El biatló andorrà existeix**: **Laure Soulié**, Sotxi 2014. El corpus el
   tenia registrat com a buit sense nom.
2. **L'esquí de fons entra a Torí 2006**, no el 2010 ni el 2018. **És la segona
   correcció del corpus sobre la mateixa dada**: la primera també anava curta.
3. **Sotxi 2014 van ser tres esports**, no un.
4. **Una afirmació rebutjada**: que Albert Llovera fos «the youngest ever
   athlete to compete in the Winter Olympics». **És fals com a absolut** i la
   versió catalana no ho diu. **El corpus reté que hi va anar amb 17 anys i res
   més.**

## `alpins/` — les 28 entrades d'esquiadors, 13 de setembre del 2026

Wikitext cru descarregat per l'**API de MediaWiki** (`action=query&prop=revisions&rvslots=main`)
de les categories **«Andorran male alpine skiers»** i **«Andorran female alpine
skiers»** d'`en.wikipedia.org`. **CC BY-SA 4.0, redistribuïbles.**

**Es guarda el wikitext i no l'HTML** perquè és **deu vegades més petit** i
**conserva les infotaules senceres** —nom complet amb els dos cognoms, data i
lloc de naixement, club, alçada, parentius— que és exactament el que el corpus
necessitava i el que el text renderitzat perd.

**Vint-i-una de les vint-i-vuit entrades són esborranys d'una línia.** Les
riques són Llovera, Verdú, Gutiérrez, Oliveras, Esteve i Vidosa.

**El que han tancat:** la quarta esportista de Calgary 1988 (**Sandra Grau i
Muxella**), si els dos Font eren germans (**sí**) i qui va ser **la primera dona
andorrana als Jocs** (**Claudina Rossel i Badia**, 1988).

**El que han obligat a corregir:** **Cande Moreno** no constava a la delegació
de Pequín 2022 del corpus i hi va fer **12a a la combinada**, el segon millor
resultat olímpic d'hivern d'Andorra; i **Marc Oliveras** no constava a la de
PyeongChang 2018, on va fer **29è**.

**Una errata de la font, registrada:** l'entrada de Marc Oliveras diu que
Schladming és a **Itàlia**. És a **Àustria**.
