# `docs/raw/consell-general/dcg-1995/` — Diari Oficial del Consell General, 1995

**Els catorze diaris de sessions de l'any 1995**, baixats sencers el 2026-09-17.

| | |
| --- | --- |
| **Font** | Consell General del Principat d'Andorra |
| **Patró d'URL** | `https://www.consellgeneral.ad/ca/arxiu/diari-oficial-del-consell-general-1/any-<AAAA>/dcg-<N>-<AAAA>/at_download/pdf` |
| **Llicència** | **pendent de determinar** per a la peça concreta, com ja consta a [`consell-general-dcg-2018-7`](../../../fonts/consell-general-dcg-2018-7.md) |
| **Redistribució** | **pendent** |
| **`apte_dataset`** | **no** |
| **Data de consulta** | 2026-09-17 |

## L'arxiu arriba fins al 1995 i s'atura el 2023

Sondejant l'any a l'URL: **1995, 2000, 2008, 2014 i 2018 responen 200**; **2024 i
2026 responen 404**. **El Diari de Sessions en línia cobreix, doncs, les
legislatures antigues i no les més recents**, que són a la seu electrònica
(`seu.consellgeneral.ad`) amb una altra estructura.

## Els catorze diaris del 1995, amb data i matèria

| Núm. | Sessió | Mencions de «nacionalitat» |
| --- | --- | --- |
| 1 | extraordinària, **16-02-1995** | 0 |
| 2 | tradicional, 14-03-1995 | 0 |
| 3 | ordinària, 06-04-1995 | 2 |
| 4 | ordinària, 11-05-1995 | 2 |
| **5** | ordinària, **25-05-1995** | **79** — **debat de globalitat** de la llei |
| 6 | ordinària, 01-06-1995 | 1 |
| 7 | ordinària, 01-06-1995 | 0 |
| 8 | ordinària, 14-06-1995 | 3 |
| 9 | ordinària, 30-06-1995 | 26 |
| **10** | ordinària, **05-10-1995** | **74** — **votació article per article i aprovació** |
| 11 | ordinària, 21-11-1995 | 8 |
| 12 | ordinària, 14-12-1995 | 0 |
| 13 | ordinària, 20-12-1995 | 0 |
| 14 | tradicional, 21-12-1995 | 0 |

## Com s'ha d'extreure aquest PDF

**És a dues columnes.** `pdftotext -layout` **interleava les dues columnes** i
produeix frases que barregen dos oradors: serveix per **localitzar** i **no per
citar**. Per citar, l'extracció bona és **`pdftotext -raw`**, que respecta l'ordre
de lectura; a canvi, **la justificació del document menja espais**
(`Nomésunacosaprèvia`) i **cal restituir-los a mà** en cada cita.

Per això aquí hi ha **les dues extraccions** del núm. 10: `dcg-10-1995.txt`
(layout, per cercar) i `dcg-10-1995-raw.txt` (raw, per citar).

## El que se n'ha tret

**Les cinc xifres del debat de la nacionalitat de 1995** —30, 25, 20, 18 i 15
anys— **amb grup proposant, article i resultat de votació**, a
[`temes/institucions/nacionalitat-i-residencia/el-rellotge-dels-vint-i-cinc-anys.md`](../../../temes/institucions/nacionalitat-i-residencia/el-rellotge-dels-vint-i-cinc-anys.md).

**El DCG 5/1995, el debat de globalitat del 25 de maig, està baixat i no
llegit.**
