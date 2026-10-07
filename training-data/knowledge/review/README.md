# Revisió de Maia Knowledge

`records.jsonl` és la font de veritat editorial. Cada línia conté una conversa i, al mateix objecte, les fonts, llicència, afirmacions sostingudes, límits, grup de divisió i unitats de cobertura. Això evita aparellar missatges i procedència per número de línia.

`conversations.jsonl` és una vista generada pel validador. Conté només els `messages` dels registres aprovats; les mostres i els esborranys no hi apareixen. No l'edites directament. Els splits d'entrenament s'escriuran més endavant a `output/`.

Els registres poden tenir aquests estats:

- `draft`: pendent de revisió.
- `approved_sample`: exemple de calibratge que no entra a l'entrenament ni compta com a cobertura.
- `approved`: revisat i elegible per a l'exportació i la cobertura.
- `rejected`: descartat.

El JSONL final d'entrenament contindrà només `{"messages":[...]}`. No hi exportem `record_id`, fonts ni dades internes. Les mostres actuals fixen el criteri editorial; no són dades entrenables.

`unit-decisions.jsonl` registra unitats no entrenables o excloses, amb el motiu i les fonts examinades. `work/` conté inventari regenerable; `reports/` conté informes de cobertura.

Abans d'aprovar una conversa, revisa-la llegint només el diàleg i passa la checklist de [`EXEMPLES.md`](EXEMPLES.md). Després comprova les afirmacions i els drets a la mateixa línia de `records.jsonl`.
