# Exemples de calibratge

Aquests diàlegs mostren el to i la forma de seguiment que busquem. **No són candidats, no entrenen el model i no compten per a cobertura.** Les fonts i límits consten a [`procedencia-exemples.md`](procedencia-exemples.md).

## 1. El nom de la Marratxa

```json
{"messages":[{"role":"user","content":"La Marratxa encara es balla amb el recipient de perfum, o només n'ha quedat el nom?"},{"role":"assistant","content":"Només n'ha quedat el nom. La marratxa era un recipient d'aigua perfumada que els dansaires duien antigament, però avui l'objecte ja no forma part del ball."},{"role":"user","content":"I la data del 1278, també és segura?"},{"role":"assistant","content":"No es pot donar per demostrada. La tradició situa el primer ball el 7 de setembre de 1278, mentre que el Pareatge es data el 8 de setembre. Cal presentar el 1278 com una tradició sobre l'origen, no com una data verificada del primer ball."}]}
```

La primera pregunta neix d'una confusió plausible entre el nom i l'objecte. El seguiment comprova si una història d'origen és un fet documentat.

## 2. Dues dades no fan una tendència

```json
{"messages":[{"role":"user","content":"L'enquesta diu que el 2024 més gent anava al cinema que el 2019. Vol dir que hi ha anat pujant cada any?"},{"role":"assistant","content":"No ho podem saber amb aquestes dues observacions. La proporció passa del 57,4% el 2019 al 66,3% el 2024, però no tenim aquí les dades dels anys intermedis."},{"role":"user","content":"Així doncs, podria haver baixat alguns anys pel mig?"},{"role":"assistant","content":"Sí. Amb només la comparació entre 2019 i 2024 no es veu el recorregut: l'assistència podria haver pujat de manera gradual o haver tingut alts i baixos."}]}
```

La pregunta posa a prova una conclusió humana habitual. El seguiment concreta què es pot inferir i què no.

## Quan acabar

No afegeixis un torn només per fer el diàleg més llarg. Si el dubte queda resolt, acaba aquí.
