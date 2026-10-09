# Maia Training Data

Aquesta carpeta prepara dues línies de dades separades a partir del corpus de
`docs/`:

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb fets documentats
  a `docs/temes/`.
- **Language** conserva mostres de llengua autèntica de `docs/parla/`; no es
  creen respostes per imitar una manera de parlar.

Ara mateix hi ha cinc exemples interns de calibratge i un candidat de Knowledge
pendent de revisió. Els exemples no compten com a cobertura; el candidat encara
no és exportable. Les converses i la seva procedència es mantenen en fitxers
JSONL separats dins de `knowledge/`.

La cua antiga de candidats no forma part d'aquesta estructura. S'ha conservat
sense canvis a `../training-data-reset-backup-2026-10-09/` per poder-la
consultar, però no és una font de nous exemples. Els fitxers d'export continuen
buts fins que s'hagin acordat els criteris i aprovat dades amb drets compatibles.

Vegeu [`PLAN.md`](PLAN.md) per al mètode de treball i els passos següents.
