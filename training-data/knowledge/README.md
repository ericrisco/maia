# Maia Knowledge

Aquest dataset ensenyarà a respondre preguntes sobre Andorra a partir de `maia/docs/temes/`. La unitat de creació és una conversa que resol una curiositat humana. No convertim títols, apartats o files en preguntes.

- `review/conversations.jsonl`: converses revisades que poden formar part del dataset.
- `review/provenance.jsonl`: fonts, afirmacions i drets vinculats a aquestes converses.
- `review/calibration.jsonl`: cinc mostres per acordar el to i el format abans d'ampliar el conjunt.
- `review/calibration-provenance.jsonl`: procedència de les cinc mostres de calibratge.
- `review/EXEMPLES.md`: les mostres en format llegible i la llista de control editorial.
- `work/`: inventaris temporals mentre ampliem la cobertura.
- `reports/`: informes de revisió i cobertura.

Les mostres de calibratge són una referència editorial. No s'exporten automàticament. Abans d'incorporar-les, cal revisar-ne l'exactitud, la naturalitat i els drets de les fonts. La procedència continua separada dels missatges que rep el model.

`work/coverage.csv` inventaria els fitxers de `docs/temes/`. Cada fila ha de quedar coberta per converses o exclosa amb motiu abans de declarar complet el dataset. El flux i els criteris són a `../PLAN.md`.
