# Maia Training Data

Aquesta carpeta prepara dues línies de dades separades a partir del corpus de
`docs/`:

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb fets documentats
  a `docs/temes/`.
- **Language** conserva mostres de llengua autèntica de `docs/parla/`; no es
  creen respostes per imitar una manera de parlar.

Ara mateix només hi ha cinc exemples interns de calibratge per a Knowledge.
No són registres aprovats, no compten com a cobertura i no s'han d'entrenar.
Les converses són a `knowledge/examples/conversations.jsonl`; les fonts i la
revisió de drets corresponents són a `knowledge/examples/provenance.jsonl`.

La cua antiga de candidats no forma part d'aquesta estructura. S'ha conservat
sense canvis a `../training-data-reset-backup-2026-10-09/` per poder-la
consultar, però no és una font de nous exemples. Els fitxers d'export continuen
buts fins que s'hagin acordat els criteris i aprovat dades amb drets compatibles.

Vegeu [`PLAN.md`](PLAN.md) per al mètode de treball i els passos següents.
