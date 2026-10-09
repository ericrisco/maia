# Maia Training Data

Aquesta carpeta prepara dos conjunts independents a partir del corpus Maia:

- **Maia Knowledge** ensenya a respondre preguntes sobre Andorra amb fets documentats a `docs/temes/`.
- **Maia Language** preserva llengua contemporània autèntica de `docs/parla/`; no s'hi barreja coneixement enciclopèdic ni oralitat inventada.

`knowledge/examples/` conté cinc mostres internes per fixar el criteri de conversa natural i multitorn. La cua activa de revisió és buida i els fitxers d'export no contenen dades aprovades. Les mostres no s'han d'entrenar ni comptar com a cobertura.

Els registres rebutjats de Knowledge s'han preservat fora d'aquesta carpeta als directoris `training-data-reset-backup*`; no es reutilitzen sense reescriure'ls. Consulteu [`PLAN.md`](PLAN.md) per al mètode, l'estructura i les etapes següents.
