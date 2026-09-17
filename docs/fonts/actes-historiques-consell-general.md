---
type: font
id: actes-historiques-consell-general
title: "Actes històriques del Consell General (1289-1864)"
titular: Consell General del Principat d'Andorra
autor: institucional
publicacio: "consellgeneral.ad/actes-historiques. Projecte de transcripcio obert, quatre llibres d'actes i vuitanta documents precedents."
url: https://www.consellgeneral.ad/actes-historiques
llicencia: "Publicacio institucional en obert, sense llicencia declarada als llibres d'actes. La sintesi de Guillamet (2024) SI que porta prohibicio expressa de reproduccio."
redistribucio: pendent
data_consulta: 2026-09-17
abast: >
  Les actes del Consell de la Terra i del Consell General transcrites: vuitanta
  documents solts del 1289 al segle XVI i quatre llibres d'actes del 1529 al
  1864. Font primaria andorrana en catala de cada epoca.
notes: >
  COM S'HI ARRIBA. El lloc es Plone i tot son PDF servits sense clau a URL sense
  extensio: cada acta i cada llibre es un PDF encara que l'adreca sembli una
  pagina. CAL MIRAR EL BOM %PDF- abans de descodificar: decodificar bytes de PDF
  com a text no llenca cap error i dona un fitxer illegible que sembla baixat.
  Es el mateix defecte que provar UTF-16 sense mirar el BOM (vegeu bopa.md).
  El text s'extreu amb `pdftotext` i es el que el corpus cita; els PDF son
  gitignorats per R014 (26 MB de binaris).
  Client: `02-DOCS/raw/operations/gap-audit-scripts/baixa_precedents.py`.
  DOS REGIMS DE DRETS, que no es poden barrejar:
  - Els LLIBRES D'ACTES i els DOCUMENTS PRECEDENTS son transcripcions de
    documents d'arxiu public de fa segles, a cura d'Ignasi J. Baiges, Mariona
    Fages i Jordi Guillamet. No hi consta cap nota de drets. El corpus els cita
    i no els republica com a recull.
  - La SINTESI de Jordi Guillamet, "Del Consell de la Terra al Consell General.
    Sindics, subsindics, consellers i consols (1133-2023)" (2024, ISBN
    978-99920-52-52-5), porta copyright de l'autor i del Consell General i la
    frase "La reproduccio total o parcial d'aquesta obra per qualsevol
    procediment [...] resten rigorosament prohibides". NOMES CITACIO.
tema: fonts
veu: compilada
epoca: medieval
apte_llengua: true
timestamp: 2026-09-18T02:00:00Z
tags: [font, historia, consell-general, arxiu, llengua, font-primaria]
---

# Les actes històriques del Consell General

## Què és, i per què importa més que la mida

**Set milions de caràcters de text andorrà primari, del 1289 al 1864**, i **la
xifra no és el que importa.** **El que importa és que està transcrit i datat
document per document**, amb **la signatura arxivística de cadascun**.

| | |
| --- | --- |
| **Documents precedents** | **80 actes soltes**, de **1289 maig 20** al segle XVI, una per fitxer |
| **Llibre I** | **1529-1639** (ASC 32) |
| **Llibre II** | **1637-1682** |
| **Llibre III** | **1682-1744** |
| **Llibre IV** | **1743-1864** (ANA, ASC núm. 5.860) |

## El document més antic, i què hi ha a dins

**L'acta del 20 de maig del 1289** —la més antiga del recull— **no és un
document sobre Andorra: és un document d'Andorra**, i **dona els noms dels
pròmens de cada parròquia**:

> «Ací comense lo **Libre de les Ordenacions dels habitans de les vals
> d'Endora**, feytas e ordenades per los pròmens he consellés del **Consel de
> les dites vals d'Endorra** ab lisènsia e voluntat del senyor en Perre, per la
> divinall providènsia **bisbe de Urgell**, e del senyor en **Royger Bernat**,
> per gràcia de Déu **comte de Foys**, a XX del mes de may, en l'an de la
> nativitat de nostre Senyor **Mo CCo LXXXo IXo**»

**Hi consten sis parròquies** —Canillo, Encamp, Ordino, la Massana, Andorra i
Lòria— **amb els seus consellers pel nom**, i **la matèria és la muntanya**:
cabanes, *apreus*, senyalar, i **la quèstia deguda als coprínceps**.

**Un any després del segon Pareatge, el Consell de la Terra ja legisla sobre
pastures amb llicència dels dos senyors.**

## Per a la llengua

**`apte_llengua: true`, i és el primer fons del corpus que ho és de debò per a
l'andorrà antic.** **No és català de Barcelona transcrit a Andorra: és la
grafia andorrana de cada segle** —*Endorra*, *pròmens*, *feytas*, *seynalar*,
*aprés*— **amb cinc-cents setanta-cinc anys de continuïtat documentada.**

## Related

- [El BOPA](./bopa.md) — la sèrie que comença on aquesta s'acaba, el 1989.
