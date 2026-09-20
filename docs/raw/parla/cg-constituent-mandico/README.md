---
title: "Testimoni del Consell Constituent — Rosa Maria Mandicó Alcobé"
---

# Testimoni del Consell Constituent — Rosa Maria Mandicó Alcobé

Material de partida de la **tanda 3 de parla**. La fitxa viu a
`docs/parla/oral/testimoni-constituent-mandico.md`.

## La peça

| | |
| --- | --- |
| Peça | #ConsellConstituent - Rosa Maria Mandicó Alcobé |
| Sèrie | [Testimonis del Consell Constituent](../../../fonts/consell-general-constituent.md) |
| URL | https://youtu.be/vOucfx_sd4M |
| Publicada | 2024-12-18 |
| Durada | 1267 s (21 min 8 s) |
| Llicència declarada | **Cap.** Llicència estàndard de YouTube. |
| Consultada | 2026-09-13 |

## El consentiment

**Consta.** Entrevista donada a la institució, publicada per la institució amb
el nom de la persona al títol i a la descripció, i la persona és **càrrec públic
electe** parlant de la seva actuació pública. Parlant viva.

**Els drets són una altra cosa i no van bé:** sense llicència oberta, la
redistribució queda `pendent`.

## L'àudio

```
font   : https://youtu.be/vOucfx_sd4M
procés : yt-dlp -f bestaudio -x --audio-format wav --postprocessor-args "-ar 16000 -ac 1"
wav    : 16 kHz, mono, 1267.52 s
sha256 : 83e8df17cf6288fb0a2f9a8ca65b0fb5e21a9bb49213c352acd299a47fd65492
```

## Transcripció

Mateix mètode i mateix llindar que les tandes 1 i 2
([`marcatge-confianca.py`](../marcatge-confianca.py)):

```
whisper-cli -m ggml-large-v3-turbo-q5_0.bin -l ca \
  --vad --vad-model ggml-silero-v6.2.0.bin -ojf -ml 0 -et 2.8
```

**454 segments, 243 paraules marcades, ~3.768 mots.**

### Aquesta peça trenca el patró de les dues anteriors

A les tandes 1 i 2, la careta musical produïa al·lucinacions i calia VAD. **Aquí
no hi ha careta**: l'entrevista arrenca a 00:00:05,090 amb la primera frase
sencera. El VAD no s'ha menjat res.

I el més important: **whisper ha conservat els titubeigs**. A les xerrades
preparades no n'hi havia per conservar; aquí sí, i hi són. Frases a mitges
(«Vull dir, eren, doncs...»), repeticions («anem amb un canvi, anem amb un
canvi»), rectificacions. **Això és el material que la regla demanava i que les
dues primeres tandes no podien donar.**

### L'entrevistador

**Editat fora.** Se sent una sola veu. Es nota que hi havia preguntes perquè les
respostes arrenquen a mitja idea —«Doncs normalment es rebia amb interès»— i
perquè una vegada s'adreça a algú: «com tu m'estàs explicant, no?» (00:08:08).

**No hi ha problema de diarització**, i per això aquesta sèrie s'ha pogut fer
abans que la càpsula #65 d'AR+I.

## Densitat de marcadors

Comptat sobre el cos sense marques de temps, **3.768 mots**:

| Marcador | Ocurrències | % dels mots |
| --- | --- | --- |
| `vull dir` | **167** | 4,4 % (×2 mots) |
| `no?` (interrogació de represa) | **149** | 4,0 % |
| `clar` | 65 | 1,7 % |
| `bueno` | 54 | 1,4 % |
| `doncs` | 44 | 1,2 % |

**Al voltant del 11 % del text són marcadors discursius.** Cap dels tres primers
no surt ni una vegada a `docs/temes/`, que són 700 documents de veu compilada.
**És la diferència entre parla i prosa, mesurada.**

## Fitxers

| Fitxer | Què és |
| --- | --- |
| `transcripcio-asr-marcada.txt` | Transcripció amb marca de temps i `[?...]`. **És la que se cita.** |
| `transcripcio-asr.vtt` | Sortida VTT crua. |
| `paraules-marcades.txt` | Les 243 paraules marcades amb la seva probabilitat. |
