# Maia Training Data

Aquest directori prepara dades per entrenar i avaluar models Maia. Manté dos objectius separats:

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb el coneixement documentat a `docs/temes/`.
- **Language** conserva mostres de llengua andorrana contemporània produïdes per persones, a partir de `docs/parla/`.

No es barregen fonts ni objectius. `examples/` serveix per calibrar l'estil; `output/` només contindrà registres aprovats per entrenar. Els outputs són buits mentre les converses, la cobertura i els drets no estiguin revisats.

Comença per [PLAN.md](PLAN.md). Les preguntes i respostes s'han de poder entendre sense haver llegit els documents interns de Maia.
