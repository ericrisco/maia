# Scripts de Maia Language

Des de l'arrel de `maia/`, executeu:

```sh
PYTHONPATH=src python3 -m training_data.language_text
```

El comandament inventaria `docs/parla/`, extreu les línies amb marca temporal
que no contenen incerteses explícites i agrupa línies adjacents en mostres de
text. Escriu les mostres i la procedència alineada a `review/`, crea informes
a `reports/` i genera splits locals a `output/`. Els fitxers `output/`, `work/`
i `reports/` són regenerables. Les mostres de menys de 80 caràcters queden al
registre per revisar però s'exclouen dels splits. Les transcripcions pendents
de verificació d'àudio queden marcades a la procedència.
