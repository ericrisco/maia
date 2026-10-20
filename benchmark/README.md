# Benchmark de l'andorranitat

Mesura si un model **sap d'Andorra** i si **parla andorrà**, per comparar Gemma 4 base amb maia.

Models comparats: Gemma 4 **E4B** i Gemma 4 **31B**, base i fine-tune.

## Parts

| Part | Què mesura | Correcció |
|---|---|---|
| Coneixement | Fets d'Andorra (test, resposta oberta, trampes) | Automàtica + jutge LLM |
| Llengua | Perplexitat sobre parla real, elecció dialectal, prova cega amb andorrans | Automàtica + vots humans |
| Control | Català general (CatalanBench) | Automàtica |

## Reserva: el que no s'entrena mai

- `reserva/fitxes.txt` — 41 fitxes de `docs/temes/`. Mostra estratificada per domini (articles de 600 a 3.000
  paraules, llavor `20261020`). Cap registre de `training-data/datasets/` que en citi alguna a `documents` no
  pot entrar a l'entrenament (avui: 798 de 19.421).
- `reserva/parla.txt` — 6 peces de `docs/parla/oral/` (~21.800 paraules, ~15% de Parla), de parlants, parròquies
  i tipus diferents, amb ≤ 5% de paraules dubtoses. No poden entrar a l'entrenament.

L'exportador de datasets llegeix aquests dos fitxers i exclou el que hi surt.

## Regles

1. El benchmark porta versió. Un cop congelat (`v1`), no es toca: una correcció és una `v2`.
2. Cap pregunta del benchmark pot tenir un duplicat proper als datasets d'entrenament.
3. Mateixes condicions per a tots els models: mateix prompt, temperatura 0.
4. Sense fets que caduquen (lleis vigents, preus, càrrecs actuals, horaris).
