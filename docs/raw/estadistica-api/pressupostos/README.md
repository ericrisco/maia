# Pressupostos i finances públiques — API del Departament d'Estadística

**Baixat el 18-09-2026** amb
`02-DOCS/raw/operations/gap-audit-scripts/estadistica_api.py`, prefix de divisió
**`0202`**.

| | |
| --- | --- |
| **Fitxer** | `pressupostos-api-2026-09-18.tsv` (19 MB) |
| **Divisions** | **391** |
| **Taules** | **391** |
| **Valors** | **115.240** |
| **Divisions KO** | **0** |
| **Període** | **1990 – 2026** |

## Font i drets

- **Departament d'Estadística del Govern d'Andorra**,
  `https://sig.govern.ad/SIGDDE.Public/estadistiquesdades/api/`.
- **Llicència: CC BY 4.0.** Atribució obligatòria al Departament d'Estadística.
- **Sense clau d'accés**, sense registre, sense límit de peticions declarat.
- Fitxa de font del corpus: `docs/fonts/estadistica-ad.md`.

## Columnes

`idDivision · taula · codi · serie · periode · valor`

Els valors arriben en format europeu (`1.234,56`) i es desen normalitzats
(`1234.56`).

## Què hi ha

- **Pressupostos previstos** del Govern, dels set comuns, de la CASS, del SAAS,
  de FEDA, d'Andorra Telecom i de la resta d'entitats parapúbliques, d'ingressos
  i de despeses, **1995-2026**.
- **Liquidacions trimestrals** d'ingressos i de despeses per sectors de
  comptabilitat nacional: **S.1311A administració central**, **S.1313
  administració local**, **S.1314 fons de la seguretat social**.
- **Erogació per funcions de govern (COFOG)**, en sis agregats.
- **Pressió fiscal, impostos meritats** i **impost general indirecte**.
- **Tipus d'interès legal i moratori**, 2019-2026.

## Defectes coneguts

- **La taula `RESULTATS PRESSUPOSTARIS PREVISTOS` publica tres conceptes per al
  mateix any** —exercici, caixa i gestió— **i no els defineix.** El de
  l'exercici és volàtil (972,7 M€ el 2013, 1.220,8 M€ el 2022) perquè sembla
  incloure operacions de deute; el corpus fa servir **el de caixa**.
  Vegeu `docs/temes/institucions/govern/trenta-dos-anys-de-pressupost.md`.
- **Tot el que porta el nom «pressupost» és previsió, no liquidació.** Les
  liquidacions són a les taules trimestrals, amb un altre perímetre.
- **La taula COFOG repeteix el 2023 els valors del 2022** — defecte ja
  documentat a
  `docs/temes/economia/banca-i-fiscalitat/la-pressio-fiscal-sha-doblat.md`.
- **Els darrers anys de les sèries trimestrals poden ser parcials.** Compteu els
  trimestres abans de sumar-los per any.
