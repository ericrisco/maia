# Inventari de Maia Language

Aquest inventari aplica els tres filtres del corpus, però no converteix una peça en candidata d’entrenament automàticament. Els drets s’han de comprovar per peça i les transcripcions s’han de verificar contra l’àudio. Les transcripcions automàtiques marcades com a incertes no entren al dataset.

- Fitxers Markdown inspeccionats: **45**.
- Peces que passen `veu: originaria`, `epoca: contemporania` i `apte_llengua: true`: **38**.
- Peces que passen filtres de transcripció i tenen una font que permet redistribució a nivell de sèrie (encara pendents de revisió per peça): **0**.
- Converses Language generades: **0**. No s’ha inventat cap torn ni s’ha tractat una transcripció no verificada com a parla validada.

## Estats dels drets i transcripcions

| Drets | Peces |
|---|---:|
| `pending_or_restricted` | 40 |

| Transcripció | Peces |
|---|---:|
| `not_marked_uncertain_but_not_verified` | 1 |
| `uncertain_and_unverified` | 8 |
| `unverified` | 31 |

## Acció necessària

Revisar els drets de cada peça i escoltar l’àudio per verificar la transcripció. Després cal determinar si hi ha torns humans suficients per a un diàleg fidel. Si no n’hi ha, la peça no es força dins d’un format `user`/`assistant`.
