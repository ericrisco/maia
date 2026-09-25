# Expedient de prospecció — Isidre Bartumeu Martínez

## Estat

`lead-rtva-009-isidre-bartumeu` és una font candidata fora del recompte canònic
i fora dels grafs canònics. La pàgina de RTVA presenta Isidre Bartumeu com a
notari amb trajectòria professional al país i l'entrevista és en català. La
font conté com a mínim dos torns de veu; per això els clips no s'atribueixen al
convidat fins a l'audició.

## Procedència i fitxers

- Font: [RTVA — capítol 23 d'El Camí de la Vida](https://www.rtva.ad/programes/capitol-23-isidre-bartumeu-el-cami-de-la-vida).
- Pàgina conservada: `source-page.html`; termes: `legal-page.html`.
- Flux original local: `source-original.mp4` (només recerca local).
- WAV de treball: `audio.wav`, mono, 16 kHz, 2.930,40 s.
- Hashes i metadades: `source.info.json`.

## Transcripcions

La passada principal és `asr/isidre-bartumeu-nocontext.*` (small, català,
sense context acumulat): 842 segments fins a 2929.80 s. La passada
independent `asr/isidre-bartumeu-base-nocontext.*` té 759 segments fins a
2930.04 s. La primera passada amb context (`asr/isidre-bartumeu.*`) es
conserva com a incidència: entra en repetició i produeix offsets de tokens
incoherents a partir d'una part de l'entrevista, de manera que no s'utilitza
com a text principal.

La passada small conté 2026 tokens amb probabilitat inferior a 0,55 i
18 repeticions consecutives exactes. El text i la forma s'han de
contrastar amb l'àudio.

## Inventari i anàlisi provisional

`formes.tsv` conserva les 35 formes candidates amb recompte independent small i
base. `clips/` conté 16 clips locals, un per forma localitzada;
`cua-audicio.tsv` manté veu, variant, fonètica, prosòdia i nota en `pendent`.

`analisi-acustica.tsv` conserva descriptors dels 16 clips (RMS mediana -42.0–-25.7 dB, F0 mediana 108.8–153.8 Hz, activitat de veu 0.44–0.84). Són mesures instrumentals per ordenar l'escolta, no trets fonètics confirmats.

 

Seqüències lèxiques més repetides en la passada small (no són trets dialectals):
que (331), la (231), i (224), de (221), no (190), el (180), a (155), és (136), una (94), en (94), per (74), sí (73), un (70), els (60), amb (56), va (52), ha (50), dia (43), vida (42), molt (41)

No es publica cap tret fonètic, prosòdic ni dialectal com a confirmat. La font
és una entrevista institucional i els marcadors poden pertànyer a
l'entrevistador o al convidat. Qualsevol incorporació al corpus canònic exigirà
atribució de veu, revisió dels termes d'ús i escolta clip per clip.

## Inventari lingüístic comparable

La taula [`analisi-linguistica.tsv`](analisi-linguistica.tsv) conserva, per a `small` i `base`, recompte de tokens i tipus, diversitat lèxica, marcadors discursius, formes territorials, contacte lingüístic, clítics, passat perifràstic aparent, primera persona i negació.

| model | tokens | tipus | TTR | clítics | passat aparent | primera persona | negació |
|---|---:|---:|---:|---:|---:|---:|---:|
| small | 6391 | 1681 | 0.2630 | 781 | 55 | 36 | 131 |
| base | 6391 | 1681 | 0.2630 | 781 | 55 | 36 | 131 |

Aquests recomptes provenen de l'ASR i són candidats textuals; no confirmen trets dialectals, identitat de veu ni variants fonètiques.
