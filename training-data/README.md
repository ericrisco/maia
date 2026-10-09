# Maia Training Data

Àrea de treball per preparar dades de fine-tuning a partir del corpus de Maia.

Hi ha dos objectius separats:

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb fets documentats a `docs/temes/`.
- **Language** conserva català andorrà contemporani produït per persones, a partir de `docs/parla/`.

No es barregen fonts, exemples ni criteris entre els dos conjunts. Les converses llegibles no porten IDs ni notes de procedència; aquestes es guarden en fitxers separats. Cap exemple d'aquesta etapa no és exportable. `output/` queda buit fins que hi hagi revisió de qualitat, drets i splits.

Comença per [PLAN.md](PLAN.md). Les guies de cada conjunt són a [knowledge/](knowledge/README.md) i [language/](language/README.md).
