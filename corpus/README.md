# Corpus curat de Maia

Aquest arbre és una sortida regenerable de `cervell cura tot docs --out corpus`.
No s'edita a mà. El contingut conserva identificadors de document i de chunk,
hashos de blob d'origen, font, família, llicència, redistribució i decisió de
revisió. La sortida no és un dataset ni conté Q&A.

## Ús dels chunks

- `coneixement`: fragments amb volatilitat inferior a 0,5.
- `raft-context`: fragments factuals, inclosos els volàtils que només s'han
  de consultar en context.
- `raft-sense-oracle`: buits oberts o parcials; mai no expressen una negació.
- `llengua`: parla originària sense normalització ortogràfica. Les mostres
  `pendent-escolta` són material de curació i no s'han de tractar com a
  aprovades per entrenar.

Consulteu `informe.md` per als recomptes, drets i decisions obertes. Les
columnes `estat_revisio` provenen exclusivament de `status` a
`docs/raw/curacio/decisions.jsonl`; sense decisió s'usa `unreviewed`.
Les decisions manuals per chunk s'escriuen a `curacio/decisions/overrides.tsv`;
un override ha d'apuntar a un ID existent i no pot reobrir PII ni fragments bruts.
