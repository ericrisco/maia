---
type: index
title: "El cervell andorrà — índex del corpus"
---

# El cervell andorrà — índex del corpus

Aquesta carpeta és **el corpus**. S'obre directament com a vault d'Obsidian:
poseu-hi `docs/` com a carpeta base, no l'arrel del repositori.

## Com està organitzat

| Carpeta | Què hi ha | Veu |
| --- | --- | --- |
| `temes/` | Coneixement sobre Andorra, en onze dominis | `compilada` |
| `parla/` | Transcripcions literals de parla andorrana | `originaria` |
| `fonts/` | Una fitxa per font: titular, llicència, redistribució | — |
| `_exemples/` | Un cas resolt per combinació. Part del contracte |  |

## La distinció que ho ordena tot

Un text **sobre** Andorra no és un text **en** andorrà.

```yaml
veu: originaria | compilada        # qui va produir el text
epoca: contemporania | historica   # de quan és la llengua
apte_llengua                        # derivat: sí ⟺ originaria ∧ contemporania
```

Tot el que hi ha a `temes/` és `veu: compilada`: ho va escriure un agent, per
molt que estigui en català i amb lèxic andorrà. Serveix com a **coneixement** i
mai com a model de com es parla. Ni la revisió humana ho canvia, perquè el que
defineix la veu és qui va produir el text.

## Abans d'afegir res

Llegiu **[CONTRACT.md](CONTRACT.md)**. Es genera des de `schema/corpus.toml` i no
s'edita a mà: el que llegiu allà és exactament el que comprova la màquina.

```bash
uv run cervell render docs        # regenera el contracte
uv run pytest                     # la suite
```

## Els buits són part del corpus

Molts articles acaben amb un **«buit registrat»**. No és una tasca pendent que
se'ns hagi oblidat treure: és la regla del projecte. El que no es pot fonamentar
amb una font **no s'escriu**, es registra com a buit.

Un buit es veu. Un error inventat no es veu fins que algú que sap del tema ho
llegeix — o pitjor, fins que el model entrenat l'etziba amb tot l'aplom.

## Estat

**Obtenció inicial del corpus tancada el 24 de setembre de 2026.** El corpus
editorial conté 1.347 articles, 618 fitxes de font i 40 documents de parla.
Les transcripcions conserven els seus avisos de revisió pendent.

La fase següent és **curació i preparació de datasets**: determinar quin
material és elegible, corregir errors, reservar una avaluació independent i
preparar exemples verificables abans de l'entrenament pilot.

El [registre de tancament i traspàs](raw/estat-projecte/tancament-obtencio-v1.md)
detalla l'abast, els pendents i els criteris per completar la fase següent.
