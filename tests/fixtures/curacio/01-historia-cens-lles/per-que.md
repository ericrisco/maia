# Exemple 1 — Article històric curt

**Cas bàsic.** Dues seccions de cos, un paràgraf de procedència editorial, Related
i tres buits oberts.

| Què hi ha a l'entrada | Què se'n fa | Regla |
| --- | --- | --- |
| Frontmatter `tema: temes/historia/antic-regim` | `tema: historia/antic-regim`, `domini: historia` | Es treu el prefix `temes/`; el domini és el primer nivell. |
| `redistribucio` en text lliure («…recerca interna; no es publica…») | `redistribucio: no` + el text original a `redistribucio_detall` | Text lliure amb «no es publica», «recerca interna» o que comença per «no» → `no`. |
| `**ACA-2339**`, `**24 d’agost de 1600**`… | Sense negretes | L'èmfasi es treu sempre. |
| `d’agost`, `l’empriu` | `d'agost`, `l'empriu` | Apòstrof tipogràfic ’ → '. Les cometes «» i els guions – — es mantenen. |
| Encapçalaments `##` | Fora del text; van a `seccio` a l'inventari | El chunk és prosa. |
| Paràgraf «La [fitxa de font](…) conserva la descripció… La imatge s'ha revisat visualment, però no s'ha transcrit.» | `nota-treball`, excloure | Paràgraf amb enllaç a `fonts/` o `raw/` **i** verb de procés del corpus (conserva, s'ha revisat, s'ha transcrit). Parla del corpus, no d'Andorra. |
| «la fitxa d'ACA-2339 parla de la muntanya de Lles…» | **Es manté** | Aquí «fitxa» és la del catàleg de l'arxiu, i no hi ha enllaç: no dispara la regla. |
| `## Related` | Excloure | Navegació. |
| Dues seccions de cos de 101 i 50 paraules | **Un sol chunk** (`#c1`, 151 paraules) | Regla de tall: vegeu el README. 101 + 50 no passa de 300 → mateix chunk. |
| Tres ítems de «Buits registrats», no ratllats | Tres unitats a `buits/` (`#g1`…`#g3`), `estat: obert` | Buit no ratllat = obert → `raft-sense-oracle`. |
| Any 1600, cap marca d'actualitat | `volatilitat: 0.0` → `coneixement` + `raft-context` | Sense senyals de volatilitat. |

**Per què importa el `#g2`:** «No s'ha pogut comprovar l'import…» es convertirà en
una pregunta RAFT sense oracle («Quant pagava la parròquia pel cens de Lles?») amb
resposta «els documents no ho diuen». **Mai** en «no pagava res».
