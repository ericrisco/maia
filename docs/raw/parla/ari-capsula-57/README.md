# Càpsula #57 — «Un racó d'Escaldes-Engordany», per Ruth Casabella

Material de partida de la **tanda 2 de parla**. La fitxa viu a
`docs/parla/oral/un-raco-descaldes.md`.

## La peça

| | |
| --- | --- |
| Peça | Càpsula #57. Un racó d'Escaldes-Engordany, per Ruth Casabella. |
| Sèrie | Càpsules d'història d'AR+I ([fitxa de font](../../../fonts/ari-capsules.md)) |
| URL | https://youtu.be/xyJqeun7e2g |
| Publicada | 2020-06-30 |
| Durada | 1081 s (18 min 1 s) |
| Llicència declarada | **Creative Commons Attribution (reuse allowed)** |
| Consultada | 2026-09-13 |

**Compte amb el duplicat.** La mateixa càpsula existeix dues vegades al canal:
`xyJqeun7e2g` (18:01, publicada 2020-06-30, títol «Un racó d'Escaldes-Engordany»)
i `Y5s87g2IYwE` (17:56, publicada 2020-07-24, títol «Un racó d'Escaldes»). S'ha
fet servir **la primera**. No s'han comparat les dues: si són muntatges
diferents, no consta.

## L'àudio

```
font   : https://youtu.be/xyJqeun7e2g
procés : yt-dlp -f bestaudio -x --audio-format wav --postprocessor-args "-ar 16000 -ac 1"
wav    : 16 kHz, mono, 1081.469375 s
sha256 : 1d04841cf6a9ebc162d0f8eed4c1491727e5a985c769c9cfc2a5575bcaa07605
```

## Transcripció

Mateix mètode que la tanda 1, mateix script
([`marcatge-confianca.py`](../marcatge-confianca.py)), mateix
llindar 0,55:

```
whisper-cli -m ggml-large-v3-turbo-q5_0.bin -l ca \
  --vad --vad-model ggml-silero-v6.2.0.bin -ojf -ml 0 -et 2.8
```

**232 segments, 147 paraules marcades.** Proporció més alta que la tanda 1 (69
sobre 77 segments): la dicció és més ràpida i hi ha molts noms propis.

### El VAD, segona confirmació

Sense VAD, els primers 22 segons de careta musical produeixen **«Institut
Cartogràfic i Geològic de Catalunya» repetit vint-i-dues vegades**. A la tanda 1
la mateixa careta produïa «El Verde Rosanandí» tretze vegades.

**Dues tandes, dues al·lucinacions diferents sobre el mateix silenci.** Queda
documentat com a comportament esperat, no com a incident: **tota peça d'aquesta
sèrie porta careta i tota transcripció sense VAD arrencarà amb text inventat.**

### El preu del VAD

El VAD **es menja l'inici**. La transcripció arrenca a 00:00:15,200 amb una
frase ja començada —«[?i] participo en aquestes càpsules»— i **la presentació
d'ella mateixa no hi és**. A la tanda 1 el parlant deia el seu nom i es podia
verificar contra el títol; **aquí no**. El nom surt del títol i de la descripció
que hi posa la institució, no de la seva boca.

### Errors sistemàtics detectats

| Què escriu | Què és | Nota |
| --- | --- | --- |
| `en Gordany` | **Engordany** | Sistemàtic, desenes de vegades. Talla el topònim en dos. |
| `escaldes` en minúscula | **Escaldes** | Sistemàtic a mitja frase. |
| `[?quartier] general` | *quarter general* | Castellanisme o francesisme de la màquina. |
| `[?sac de jamecs]` | **sac de gemecs** | L'instrument. |
| `[?obada]` | **obaga** | Oposada a *solana*, que sí que encerta. |
| `[?mucli]` | *nucli* | |
| `[?valls]` | *balls* | «es dansaven diversos [?valls]». |

**No s'han corregit dins la transcripció.** Van aquí perquè el patró és la dada:
la màquina falla als topònims andorrans i al lèxic tradicional, i encerta el
vocabulari acadèmic.

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | Transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua. |
| `paraules-marcades.txt` | Les 147 paraules marcades amb la seva probabilitat. |
