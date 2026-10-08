# Maia Training Data

Aquest espai prepara dos datasets separats a partir del corpus de Maia:

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb informació de `maia/docs/temes/`.
- **Language** conserva usos lingüístics humans de `maia/docs/parla/`; no s'hi inventen veus ni respostes.

## Estat actual

La carpeta `knowledge/examples/` conté quatre mostres per revisar el to i el disseny de converses. **No són exports d'entrenament.** Encara no hi ha datasets finals ni particions train/validation/test. La procedència i els drets es mantenen separats dels missatges.

## Estructura

- `PLAN.md`: criteris i passos de treball.
- `knowledge/examples/`: mostres editorials i procedència.
- `knowledge/work/`: inventari de cobertura i feina pendent.
- `knowledge/output/`: reservat per a exports aprovats.
- `language/work/`: inventari i revisió de peces de parla.
- `language/output/`: reservat per a fragments elegibles i splits.

Knowledge i Language no es barregen. Vegeu els README de cada àrea abans d'afegir registres.
