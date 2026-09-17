# `quotes-immigracio-1989-2011/` — la sèrie de quotes anterior a la llei del 2012

Cent un textos del BOPA baixats el **17 de setembre del 2026**: totes les quotes
d'immigració publicades entre **el juny del 1989 i el novembre del 2011**. Són
l'antecedent de la sèrie `quotes-immigracio-2012-2026/`, i juntes cobreixen tot
el que el Butlletí en publica.

| | |
| --- | --- |
| **Font** | [BOPA](https://www.bopa.ad/) · Servei del Butlletí Oficial del Principat d'Andorra |
| **Titular** | Govern d'Andorra |
| **Condicions** | [avís legal del BOPA](https://www.bopa.ad/AvisLegal) |
| **Redistribució** | **sí**, amb el sentit i les metadades de data preservades |
| **Data de consulta** | 2026-09-17 |
| **Fitxa de font del corpus** | [`bopa`](../../../../fonts/bopa.md) |
| **`apte_dataset`** | **sí** — text normatiu publicat, sense dades personals |

`manifest.json` guarda, per a cada fitxer, la data de publicació, el sumari
oficial i l'URL d'origen. Els duplicats es van eliminar per hash de contingut.

## Com se n'extreuen les xifres

Amb `02-DOCS/raw/operations/gap-audit-scripts/extreu_quotes.py`, que busca
l'ancoratge estable **«que es pot/poden lliurar en el marc d'aquesta quota és
de…»** i, per als textos dels anys noranta, **«es fixa/aprova una quota de…»**.
**Setanta-vuit dels cent un porten xifra llegible**; els altres són suspensions,
pròrrogues, redistribucions i correccions d'errata, que no en fixen cap de nova.

**Les xifres no s'escriuen a mà.** Tres files es van comprovar llegint el
document (2002-11-14 → 950, 2008-04-02 → 95, 2009-02-17 → 35) i les tres
coincideixen; una versió anterior de l'extractor donava 80 per a la primera, i
per això el mètode és aquest i no un altre.
