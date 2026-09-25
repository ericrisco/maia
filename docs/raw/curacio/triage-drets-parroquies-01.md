# Triage d'elegibilitat: les set parròquies

- Tanda: `triage-rights-parroquies-01`
- Unitat inicial: `docs/temes/institucions/comuns-i-parroquies/les-set-parroquies.md`
- Estat: `pending`; decisió limitada a fonts i elegibilitat, no revisió factual.

## Fonts i bloqueig

La fitxa declara `font: bopa-ad`, però el cos cita també Estadística A003 de juliol de 2026, la ponència de Ros Pascuet de 1989, el portal oficial `eleccions.ad` i els textos consolidats de la Llei 44/2022. Les fitxes BOPA, Estadística i Jurisprudència.ad permeten reutilització en els seus àmbits declarats. En canvi, les fitxes de Ros Pascuet i `eleccions.ad` registren `redistribucio: no`; el text utilitza la superfície de Ros Pascuet i dades electorals de 2023 d'eleccions.ad. La unitat sencera no es pot exportar mentre aquests fragments hi siguin sense permís.

No s'han revisat les xifres de població, superfície, densitat, escons ni afirmacions constitucionals contra totes les peces primàries. El gran nombre de seccions també conté anotacions de procés i relacions entre articles que requeriran una revisió editorial separada. No s'aprova ni s'exclou tota la peça pel fet que la seva font principal sigui BOPA.

## Correcció de metadades de font

La fitxa `docs/fonts/eleccions-ad.md` tenia `redistribucio: no` sense cometes. El parser YAML la llegia com el booleà `false`, tot i que l'esquema exigeix el valor de text `no`. S'ha canviat a `redistribucio: "no"`; no s'ha canviat l'estat dels drets. La fitxa de font continua exclosa del material d'entrenament.

## Comprovacions

L'inventari s'ha regenerat i comprovat: 25.587 unitats (1.216 no revisades, 174 pendents, una aprovada i 24.196 excloses). `curacio_corpus.py --self-test` i `build_final_manifest.py --self-test` passen. `export_final_corpus.py --check` i `build_final_manifest.py --check` passen per l'única unitat aprovada; aquesta no s'ha exportat. `cervell render --check docs` passa després de regenerar `docs/index.md`. L'enllaçador passa en 3.070 documents de `docs/` i 4 de `final-corpus/`. El parser comprova `redistribucio` com a cadena literal `no`. `git diff --check` passa.
