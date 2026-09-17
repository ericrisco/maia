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

## Un defecte d'extracció que cal saber abans de citar

**Els llibres d'actes estan impresos a dues columnes, i `pdftotext` les
intercala.** **Una frase pot continuar dotze línies més avall i, entremig,
n'hi ha una d'una altra columna que parla d'una altra cosa.**

**No fa el text inservible i sí que fa perillosa la citació curta.** **La regla
que el corpus segueix des del 17-09-2026 és aquesta**:

- **Llegir sempre el voltant**, no la línia que ha sortit al `grep`;
- **si una frase no lliga, comprovar si el que s'hi ha colat és d'una altra
  columna** —sol notar-se perquè canvia de matèria de cop;
- **i quan un mot o una xifra no es poden confirmar, dir-ho al costat de la
  citació** en comptes d'arrodonir.

**Les actes soltes i els documents precedents no tenen aquest problema**: són a
una columna.

## Què ha resultat tenir, comprovat article per article

**El 17-09-2026 aquest fons va tancar o avançar més de quaranta buits del corpus
en un sol dia.** **La llista serveix d'índex del que s'hi ha trobat, per si cal
tornar-hi:**

| Matèria | On és |
| --- | --- |
| **Els dos pergamins fundacionals del Consell, 1419**, amb la clàusula que prohibeix actuar contra el bisbe | precedents |
| **L'apel·lació del 1364** i les vuit greuges | precedents |
| **Els dos saigs del 1390**, un per copríncep, i el que es nega | precedents |
| **La ratificació de l'infant Pere del 1335** | precedents |
| **Les ordinacions del 1289 i del 1390** —quèstia, cabanes, primes per llop, ós i linx | precedents |
| **El dret de pas per l'Urgellet, 1341**: un parell de formatges l'any | precedents |
| **El jurament dels veguers**, amb dues negatives (1442, 1447) | precedents |
| **La sèrie de la quèstia comtal del segle XV**, sempre a crèdit | precedents |
| **La cluseda per contagi del 1628-1630**: soldats, guardes, certificats, campanes | Llibre I |
| **La bruixeria: el finançament del 1621 i la prima per execució del 1666** | Llibres I i II |
| **El règim de la farga** i els treballadors francesos, 1629 | Llibre I |
| **L'*afor*, 1744-1795**, i el preu del vi, el pa, les truites i les perdius | Llibres I-IV |
| **La *conducta* de metges, barber, advocats i llosador**, des del 1624 | Llibres I-IV |
| **La prohibició del tabac, 1731-1733**, i el permís de conreu del 1791 | Llibres III i IV |
| **L'acta del 23 de març de 1775** i l'edicte contra la gent vaga | Llibre IV |
| **El canvi de la moneda francesa, 1723** | Llibre III |
| **Els *manadors*** i el torn de casa | Llibres II-IV |
| **Els últims pagaments de la quèstia als dos coprínceps, 1863-1864** | Llibre IV |

## Related

- [El BOPA](./bopa.md) — la sèrie que comença on aquesta s'acaba, el 1989.
