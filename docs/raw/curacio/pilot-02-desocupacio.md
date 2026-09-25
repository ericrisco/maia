# Pilot 02: requisit de cotització per desocupació (post-freeze)

- Data de revisió: 2026-09-25, Europe/Madrid.
- Unitat: `maia-docs/temes/societat/treball/mesos-cotitzats-ajut-desocupacio-2020.md` (afegida després de congelar l'inventari inicial).
- Estat: `pending`; revisió factual feta per l'abast citat, però no exportable per drets d'una font secundària incorporada per registrar una discrepància.

## Contrast i correcció de lectura

El text HTML oficial del BOPA i el PDF del Decret del 7-10-2020 coincideixen en els apartats 26.4.i–j: «a partir de 26 anys» requereix 36 mesos al llarg dels darrers 60 mesos; «fins a 25 anys» requereix 18 mesos. El PDF BOPA núm. 121, publicat el 14-10-2020, ho situa a la pàgina impresa 19/30. Es va renderitzar i revisar visualment la pàgina 19; el número de pàgina, la data i els dos trams es llegeixen amb claredat.

La presentació del Govern del 18-02-2021, pàgina 9, compara aquesta regla amb la flexibilització i representa els grups com `> 26` i `< 25`. El render de la taula confirma les desigualtats estrictes; no s'infereix què es va aplicar a les edats 25 o 26 ni si la taula és una abreviació. La discrepància queda atribuïda a cada peça a l'article. L'article continua limitat al text promulgat el 2020 i adverteix que no certifica el règim vigent posterior.

El primer resultat de cerca del Govern acabat en `_1.pdf` va retornar una presentació diferent sobre ajuts a propietaris; s'ha eliminat el PDF equivocat, no s'ha citat i no s'ha reutilitzat. La segona URL identificada en el resultat oficial retorna la presentació pertinent; se'n conserva la còpia a `docs/raw/desocupacio/govern-flexibilitzacio-ajuts-desocupacio-2021.pdf` i el render de la pàgina 9 a `docs/raw/curacio/pilot/desocupacio/`.

## Procedència i decisió

La fitxa `docs/fonts/bopa-ad.md` registra que el BOPA permet copiar, difondre, adaptar i distribuir els textos normatius sota condicions de sentit, metadades, no-patrocini i no-reutilització de la identitat gràfica. El text de la norma es cita amb data, número, article i pàgina; no s'atribueix cap llicència Creative Commons.

La presentació és contingut del Govern amb copyright © 2021. La fitxa específica `docs/fonts/govern-flexibilitzacio-ajuts-desocupacio-2021.md`, basada en l'avís general `govern-andorra-web`, registra `redistribucio: no`. Com que l'article ara documenta una discrepància amb aquesta presentació, roman `pending` i no entra a `final-corpus/` fins que l'ús d'aquesta font es pugui autoritzar o la seva aportació es pugui retirar sense ocultar la incidència.

La decisió del ledger conserva els hashes dels articles i les fonts, els localitzadors BOPA p. 19 i presentació p. 9, els termes per font, els mètodes de revisió i l'abast de la revisió. No hi ha hagut revisió humana.

## Comprovacions

- `python scripts/curacio_corpus.py --write` i `--check`: passen; 25.587 unitats, 1.217 sense revisar, 173 pendents, una aprovada i 24.196 excloses.
- `python scripts/curacio_corpus.py --self-test` i `python scripts/build_final_manifest.py --self-test`: passen; casos vàlids acceptats i invàlids rebutjats.
- `python scripts/export_final_corpus.py --check` i `python scripts/build_final_manifest.py --check`: passen per l'única unitat aprovada; la nota legal pendent no s'exporta.
- `uv run cervell render --check docs`: passa; contracte i índex generats al dia.
- `python scripts/check_links.py docs` i `python scripts/check_links.py final-corpus`: passen, amb 3.069 i 4 documents respectivament.
- `git diff --check`: passa.
