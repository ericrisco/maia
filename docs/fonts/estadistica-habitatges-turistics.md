---
type: font
id: estadistica-habitatges-turistics
title: "Nombre d'habitatges i apartaments turístics — Departament d'Estadística"
titular: Departament d'Estadística, Govern d'Andorra
autor: institucional
publicacio: "sig.govern.ad (API SIGDDE)"
url: https://sig.govern.ad/SIGDDE.Public
llicencia: dades públiques
redistribucio: citacio
data_consulta: 2026-09-18
abast: >
  Sèries "NOMBRE D'HABITATGES I APARTAMENTS TURÍSTICS TOTAL" (divisió
  2801) i "...PER PARRÒQUIA" (divisió 2802), 2021-2024, consultades via
  l'API pública del Departament d'Estadística.
notes: >
  Consultada amb 02-DOCS/raw/operations/gap-audit-scripts/estadistica_api.py.
  La divisió 2802 té 8 grups pel dimension SCODIEXTENDED: 7 sumen
  exactament el vuitè (el total, idèntic a la divisió 2801), confirmant
  que són les set parròquies més el total — però l'API no dona la
  correspondència nom-de-parròquia per SCODIEXTENDED en aquesta consulta.
---

# Estadística — habitatges i apartaments turístics

## Què hi busca el corpus

**Quants HUT hi ha**, buit registrat a
[els pisos turístics](../temes/economia/turisme-i-neu/els-pisos-turistics.md).

## Què en treu

**Sèrie total, 2021-2024**: **44.366 / 46.276 / 46.790 / 47.221.**

`parcial`, amb un avís de conflació important: **aquesta xifra sembla
massa gran per ser el nombre d'HUT amb llicència** sota la definició
legal que l'article ja destil·la (article 5 de la llei). **47.221 és
un ordre de magnitud proper al parc d'habitatges total d'Andorra**, no
al nombre d'habitatges que es lloguen turísticament. **És versemblant
que aquest indicador d'Estadística compti una categoria estadística
diferent** —potser el parc de segones residències o d'habitatges no
principals, classificats com «turístics» a efectes cadastrals— **i no
els HUT registrats sota la llei del 2022 que l'article documenta.**
**No s'ha pogut confirmar la definició exacta de l'indicador.** `DIVERGÈNCIA
REGISTRADA, NO ARBITRADA`: cal contrastar la metodologia de la divisió
2801/2802 abans de citar aquesta xifra com el nombre d'HUT.
