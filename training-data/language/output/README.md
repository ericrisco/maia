# Sortida de Maia Language

El generador crea `train.jsonl`, `validation.jsonl` i `test.jsonl` amb l'esquema
de text causal `{"text": "…"}`. Cada línia uneix spans literals elegibles amb
espais, sense canviar-ne les paraules. Els fitxers es divideixen per peça font
i no contenen metadades als exemples. No són converses de xat. Les mostres de
menys de 80 caràcters es conserven a `review/` però no s'exporten.

Les sortides actuals són provisionals: 2.781 mostres de 38 peces, de les quals
les que tenen menys de 80 caràcters queden fora dels splits. Les transcripcions
no s'han verificat línia per línia contra l'àudio. La procedència alineada és a
`../review/provenance.jsonl`; la distribució per peça és a
`../work/text-split-manifest.json`. No utilitzeu aquests splits com a conjunt
final fins a revisar les condicions de font i el nivell de verificació necessari.
