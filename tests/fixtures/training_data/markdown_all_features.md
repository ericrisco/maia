---
type: article
title: Fitxa de prova del parser
description: Un exemple sense dades reals.
tema: proves/parser
veu: compilada
epoca: contemporania
apte_llengua: false
font: font-de-prova
timestamp: '2026-10-04T09:00:00Z'
tags: [prova, estructura]
---

# Títol principal

Un paràgraf amb [un enllaç intern](../fitxa.md) i
[un enllaç extern](https://example.invalid/font).

## Llista i taula

- primer element
- segon element amb [[fitxa-relacionada|un wikilink]]
  - subelement

| Camp | Valor |
| --- | --- |
| estat | corregit i resolt |

> La font A i la font B discrepen; no es resol aquí.

La part corregida s'ha marcat com a resolta. El que falta continua com a buit registrat.

```markdown
# Aquest títol és dins d'un bloc de codi.
[no és un enllaç](codi.md)
```

    ## Aquest títol és dins d'un bloc de codi indentat.
