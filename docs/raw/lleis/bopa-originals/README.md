# Originals de les lleis que el corpus tenia consolidades

Seixanta-dos textos baixats del BOPA el **17 de setembre del 2026**. Són
l'**original publicat** de lleis de les quals `docs/raw/lleis/` ja tenia una
instantània consolidada.

## Per què existeixen

**La instantània consolidada no porta les disposicions.** De les 104
instantànies del corpus, **71 no tenen cap disposició final, derogatòria,
transitòria ni addicional**: el consolidat en dona l'articulat i prou. I les
disposicions són exactament on viu el que decideix si una llei és viva: **què
deroga**, **quan entra en vigor**, **què encomana al Govern** i **quines altres
lleis modifica de passada**.

Que això no és teòric es va veure el mateix dia: una fitxa es va escriure amb el
règim del contenciós administratiu **derogat des del 2022**, perquè la
consolidació del règim anterior no ho deia enlloc.

## Procedència

| | |
| --- | --- |
| **Font** | [BOPA](https://www.bopa.ad/) · Servei del Butlletí Oficial del Principat d'Andorra |
| **Titular** | Govern d'Andorra |
| **Condicions** | [avís legal del BOPA](https://www.bopa.ad/AvisLegal) |
| **Redistribució** | **sí**, amb el sentit i les metadades de data preservades |
| **Data de consulta** | 2026-09-17 |
| **Fitxa de font del corpus** | [`bopa`](../../../fonts/bopa.md) |
| **`apte_dataset`** | **sí** — text normatiu publicat, sense dades personals |

## Com s'han baixat

Amb `02-DOCS/raw/operations/gap-audit-scripts/baixa_originals.py` del repositori
de treball: llegeix la capçalera de cada instantània, en treu la referència
`Llei N/AAAA`, cerca al BOPA el document el sumari del qual comença per aquella
referència i el desa com a `original-N-AAAA.txt`.

**Nou instantànies no en tenen**: set perquè la capçalera no porta cap
referència numerada —el Codi Penal, el de Procediment Penal, la Llei de
relacions laborals, la de taxes judicials, la transitòria de procediments
judicials, la del Tribunal Constitucional i la de la persona i la família, totes
anteriors a la numeració moderna— i dues perquè la cerca no va trobar el document
(`18/2024` de caça i `18/2023` del saig).

## Què s'hi ha comprovat

Es van llegir les disposicions derogatòries dels seixanta-dos i es van creuar amb
les 93 instantànies que porten referència numerada. **Les setze coincidències són
totes derogacions parcials** —un article, una lletra, una disposició final
concreta—: **cap llei del corpus no ha estat derogada sencera** per cap d'aquests
seixanta-dos textos.
