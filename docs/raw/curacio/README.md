# Curació del corpus

Aquest directori guarda l'estat regenerable de la revisió inicial. No és
material per entrenar el model.

## Fitxers

- `mapa-inicial.md`: recompte observat, dominis i prioritat de la primera tanda.
- `pilot-01.md`: registre incremental del pilot, evidència examinada i
  comprovacions de les unitats revisades.
- `triage-drets-actes-01.md`: bloqueig d'elegibilitat aplicat als 160 articles
  que depenen de les actes històriques del Consell; no és una revisió factual.
- `pilot-02-desocupacio.md`: contrast del text BOPA de 2020 amb la presentació
  institucional de 2021, discrepància d'edat i bloqueig de drets de la font
  secundària.
- `triage-drets-parroquies-01.md`: fonts amb drets diferents dins l'article de
  les parròquies i correcció d'un valor YAML a la fitxa electoral.
- `decisions.jsonl`: una decisió traçable per unitat; registra mètode i
  responsable de revisió quan consten, i no s'esborra en regenerar l'inventari.
- `initial-inventory.jsonl`: fotografia immutable dels hashes i unitats que
  defineixen l'abast inicial de la curació.
- `inventory.jsonl`: registre generat, una fila per fitxer o enllaç simbòlic
  del corpus sota `docs/`, amb SHA-256, mida, domini, font, estat, fotografia
  base, deriva i metadades de revisió. El mateix
  directori `raw/curacio/` queda fora de l'inventari per evitar que el registre
  s'inventariï a si mateix.
- `registre-progres.md`: resum regenerable de les fonts citades, els articles
  que en depenen i els buits que aquests declaren; es genera amb
  `python scripts/registre_progres.py docs --output docs/raw/curacio/registre-progres.md`.

## Regenerar i comprovar

Des de l'arrel del repositori Maia:

```sh
python scripts/curacio_corpus.py --write
python scripts/curacio_corpus.py --check
python scripts/curacio_corpus.py --self-test
```

`--write` recalcula els hashes i escriu el registre. `--check` falla si el
registre falta o s'ha desviat del contingut actual. `--self-test` comprova que
una decisió vàlida s'accepta i que estats invàlids, camps obligatoris buits,
evidència mal formada, exportacions fora del directori permès, hashes absents
en aprovacions i identificadors duplicats es rebutgen.

## Decisions

Afegiu una línia JSON per unitat a `decisions.jsonl`:

```json
{"unit_id":"maia-docs/temes/societat/exemple.md","status":"pending","rationale":"falta contrastar la versió vigent","evidence":["docs/raw/.../fitxer.pdf#article 4"]}
```

`status` és `unreviewed`, `in_review`, `approved`, `pending` o `excluded`;
`destination` és `knowledge`, `language` o `none`; `rationale` és obligatori i
`evidence` conté peces exactes, no números de línia. Les unitats candidates
encara no revisades queden `unreviewed`; els errors de metadades i les decisions
amb bloquejos queden `pending`. Els índexs i els fitxers de configuració/tècnics
queden exclosos automàticament amb el motiu registrat. Una aprovació només classifica
la unitat; la seva inclusió al corpus final també requereix drets de
redistribució documentats i cites revisades.
