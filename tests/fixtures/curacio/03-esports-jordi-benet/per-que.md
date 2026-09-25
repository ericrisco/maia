# Exemple 3 — Esports: taules, auditoria i una dada que caduca

**El cas freqüent.** 272 documents d'esports segueixen aquest patró: fitxa de
Viquipèdia, taules de carrera, nota d'auditoria i buits ja tancats.

| Què hi ha a l'entrada | Què se'n fa | Regla |
| --- | --- | --- |
| Taules (`\| Naixement \| …`, carrera, seleccions) | **Dins del chunk**, en Markdown net (sense negretes) | Les taules de dades es queden al chunk: RAFT necessita llegir-les («quants partits va jugar?» → 2). Només les taules marcades com a conjectura van a `pendent` (exemple 2). |
| `### Les seleccions, totes` | `seccio` de la taula | Els `###` es tracten com els `##`. |
| «**Tota la font és aquesta frase.**» | S'elimina **la frase**, no el paràgraf | Frases de procés amb inici fix: «Tota la font…», «El corpus…», «Aquest corpus…», «Tancat el…», «El material era al corpus…». Llista tancada i testejada. |
| «**Tancat el 2026-09-13 sense cap font nova.** El material era al corpus… [`Jordi_Benet.wiki`](raw/…)» | Paràgraf sencer `nota-treball` | Comença per «Tancat el» i enllaça a `raw/`. |
| `> **Auditat el 2026-09-13.** …` | `nota-treball`, excloure | Blockquote que comença per «Auditat el». |
| `~~Tot.~~ — no-es-buit` | Excloure | Estat `no-es-buit`: placeholder, no pregunta. |
| `~~La resta de la carrera.~~ — resolt` | Excloure | Estat `resolt`: la resposta ja és al text. Convertir-lo en «els documents no ho diuen» seria **fals**. |
| «FC Andorra.» sol en un paràgraf | Es manté | No hi ha regla determinista per treure'l sense risc. Si molesta, va a `correccions.tsv`, no s'esborra per intuïció. |
| Club `2000-` (rang obert, sense any final) | `volatilitat: 0.5` → **només `raft-context`**, no `coneixement` | Un rang obert vol dir «encara hi juga», i això caduca. El model no ha de memoritzar «juga al FC Andorra»; sí que pot llegir-ho en un context datat. |
| Data de naixement completa d'una persona viva | **No és PII a revisar** | El subjecte del document és un esportista de la selecció amb font a la Viquipèdia: entra a la llista blanca de persones públiques (títols de `temes/esports/` i `temes/persones/`). |
| Font CC BY-SA 4.0 | `llicencia` al frontmatter | L'obligació de compartir igual **viatja amb el chunk**: el dataset que el faci servir l'haurà d'heretar. |
