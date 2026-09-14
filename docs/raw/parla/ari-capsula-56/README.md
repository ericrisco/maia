# Càpsula #56 — «La vida a pagès», per Albert Rossa Naudí

Material de partida de la **tanda 1 de parla**. Aquesta carpeta guarda la
transcripció crua; la fitxa de parla viu a
`docs/parla/oral/la-vida-a-pages.md`.

## La peça

| | |
| --- | --- |
| Peça | Càpsula #56. La vida a pagès, per Albert Rossa. |
| Sèrie | Càpsules d'història d'Andorra Recerca + Innovació (AR+I) |
| URL | https://youtu.be/lC14HCz82_Y |
| Publicada | 2020-06-29 |
| Durada | 742 s (12 min 22 s) |
| Llicència declarada | **Creative Commons Attribution (reuse allowed)**, camp de llicència de YouTube |
| Consultada | 2026-09-13 |

## El consentiment, primer

La regla diu que sense consentiment no es transcriu. Aquí **consta**, i consta
per tres vies independents:

1. **El parlant és viu i és l'autor de la peça.** No és una gravació d'arxiu
   d'algú mort de qui s'hagi d'anar a mirar què deia el dipòsit: Albert Rossa
   Naudí grava una xerrada per a una sèrie pública i s'hi presenta pel seu nom
   («Em dic Albert Rossa Naudí»).
2. **La institució que la publica és pública.** Andorra Recerca + Innovació la
   penja al seu canal oficial, amb el nom del ponent al títol.
3. **La llicència és CC-BY**, que és una cessió explícita de redistribució feta
   pel titular. Una CC-BY no és el mateix que el consentiment de la persona,
   però aquí titular i parlant fan sèrie: la peça és la seva xerrada.

El parlant **no és un particular anònim**: és autor publicat que parla en
qualitat d'autor. Per això la fitxa el nomena, cosa que no es faria amb un
informant privat.

## L'àudio

**L'àudio no es versiona.** És binari (R014 del contracte prohibeix binaris sota
`docs/`) i és reproduïble des de l'URL. Per poder comprovar la transcripció
contra exactament el mateix àudio, aquí queda l'empremta:

```
font   : https://youtu.be/lC14HCz82_Y   (format 251, opus)
procés : yt-dlp -f bestaudio -x --audio-format wav --postprocessor-args "-ar 16000 -ac 1"
wav    : 16 kHz, mono, 742.421313 s
sha256 : e03cb51349fea420ef1e2d25ebe8d8c8e24afa01cd8fea0d65fdcf6ccf199ce0
```

## Com s'ha transcrit, i què vol dir això

**Això és transcripció de màquina, no transcripció verbatim humana.** Ho diu
aquí i ho diu la fitxa, perquè la diferència és tot el valor de la branca.

```
whisper-cli -m ggml-large-v3-turbo-q5_0.bin -l ca \
  --vad --vad-model ggml-silero-v6.2.0.bin -ojf -ml 0 -et 2.8
```

El VAD hi és per una raó concreta: sense ell, els 13 segons de careta musical
del principi **generaven text al·lucinat** («El Verde Rosanandí», repetit tretze
vegades). Amb VAD, desapareixen. Queda documentat perquè és l'error que qualsevol
altra tanda es tornarà a trobar.

### Les tres coses que una ASR fa i que la regla prohibeix

1. **Normalitza.** Treu titubeigs, repeticions i falses arrencades — exactament
   el que la regla mana conservar. El que hi ha aquí és ja text endreçat per la
   màquina, i no es pot desfer sense tornar a l'àudio.
2. **No calla mai.** Allà on una persona escriuria `[inaudible 00:04:28]`, la
   màquina escriu la seva millor conjectura amb la mateixa cara que la resta.
3. **Falla justament on interessa.** Vegeu-ho a sota: és sistemàtic, no atzarós.

### El marcatge `[?...]`

Com que no es pot escoltar l'àudio, s'ha fet servir **la confiança del propi
model** com a substitut de l'orella, que és el més honest que hi ha a mà:
`marcatge-confianca.py` agrupa els tokens en paraules i marca `[?paraula]` tota
paraula amb probabilitat mínima **< 0,55**.

**`[?x]` no vol dir «diu x». Vol dir «la màquina proposa x i ningú no ho ha
comprovat».** És el més a prop que es pot arribar de la regla «marca el que no
sents, no el que et sembla que deia» sense sentir-hi.

Resultat: **69 paraules marcades sobre 77 segments**.

### El resultat que importa

**Gairebé tot el lèxic andorrà interessant cau per sota del llindar.** No és
casualitat: un model entrenat en català general dubta precisament davant la
forma pirinenca que el corpus busca.

| Paraula proposada | p | Per què importa |
| --- | --- | --- |
| `rets` | 0,21 | 00:04:28. Parla de conduir l'aigua als camps: quasi segur **recs**. |
| `l'equa` | 0,21 | 00:09:30. Qui estira el carro: quasi segur **l'euga**. |
| `armats` | 0,21 | 00:02:32. Al costat d'**esquelles**: probablement **ramats**. |
| `tallalles` | 0,21 | 00:06:38. Al costat de **dalla**: probablement **dallaires**. |
| `Madreta` | 0,21 | 00:01:09. Dit de la mà, sense lectura clara. |
| `bun` | 0,19 | 00:08:04. Un ??? d'herba enrotllat amb cordes. |
| `d'erba` | 0,27 | 00:07:45. Pot ser caiguda de la **h**, pot ser res. |
| `tromfes` | 0,38 | 00:11:03. La patata. El corpus l'escriu **trumfa**. |
| `àrguens` | 0,47 | 00:05:34. Ho escriu **àrguens** i deu segons després **àrgens**. |
| `bacanyà` | 0,44 | 00:02:53. Al costat d'oli i arengades: **bacallà**. |
| `faça` | 0,48 | 00:01:56. «Abans dels treballs de ???». Sense lectura. |
| `ar` | 0,31 | 00:07:28 i 00:08:20. «era gairebé un ar» → **art**, amb -t caiguda? |

Cap d'aquestes no s'ha corregit. **Corregir-les seria inventar-se-les**, i a més
la meitat són el tret andorrà que es buscava: un corrector que «arregli» *equa*
en *euga* i *tromfes* en *trumfes* haurà esborrat la dada.

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | La transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua de whisper.cpp, sense marcatge. |
| `marcatge-confianca.py` | El script que passa de JSON de tokens a text marcat. |
