# Elegibilitat inicial de Maia Language

Informe generat amb `scripts/build_eligibility_inventory.py` a partir de `docs/parla/` i els registres de `docs/fonts/`.
Aquesta és una auditoria documental, no una aprovació per entrenar.

## Estat

- Fitxes `type: parla`: **40**.
- Marcades `apte_llengua: true`: **38**.
- Marcades no aptes: **2**.
- Cap fitxa `apte_llengua: true` té ara permís global confirmat al registre de font.
- A les càpsules AR+I, el registre només confirma CC BY per a peces individuals #34, #49, #56, #57, #60 i #65; cal comprovar quina fitxa correspon a cada vídeo i validar-ne la transcripció i el parlant.
- Les entrevistes del Consell General tenen llicència estàndard de YouTube; les preguntes de l'entrevistador s'han eliminat de les transcripcions.

## Candidates per font

| Font | Peces marcades aptes | Estat de redistribució del registre |
|---|---:|---|
| `ari-capsules` | 11 | `pendent` |
| `consell-general-constituent` | 27 | `pendent` |

## Decisions necessàries abans de crear registres

1. Comprovar els drets de cada peça i de cada transcripció. Un permís d'un vídeo no cobreix tota una sèrie.
2. Confirmar que cada parlant i cada text representen català andorrà contemporani, en lloc d'inferir-ho del lloc de publicació.
3. Revisar els fragments marcats amb `[?]`; aquests són propostes automàtiques de transcripció i no es poden tractar com a parla verificada.
4. Fer servir només torns humans que es conservin a la font. Les entrevistes sense preguntes ni monòlegs no es convertiran en diàlegs de xat inventats.

## Inventari per peça

| Peça | Apta segons corpus | Font | Vídeo AR+I | Segments temporitzats | Marques `[?]` | Drets per peça confirmats al registre |
|---|---|---|---:|---:|---:|---|
| `docs/parla/oral/cal-pal-esther-jover.md` | no | `ari-capsules` | 49 | 294 | 58 | sí, cal verificar peça |
| `docs/parla/oral/el-contrapas-teo-armengol.md` | sí | `ari-capsules` | 66 | 207 | 209 | no / pendent |
| `docs/parla/oral/els-hostals-comunals-lacueva.md` | sí | `ari-capsules` | 13 | 318 | 130 | no / pendent |
| `docs/parla/oral/els-molins-daigua.md` | sí | `ari-capsules` | 20 | 436 | 131 | no / pendent |
| `docs/parla/oral/els-noms-dels-carrers.md` | sí | `ari-capsules` | 27 | 232 | 99 | no / pendent |
| `docs/parla/oral/la-nissaga-dels-marti.md` | sí | `ari-capsules` | 70 | 112 | 53 | no / pendent |
| `docs/parla/oral/la-vida-a-pages.md` | sí | `ari-capsules` | 56 | 77 | 86 | sí, cal verificar peça |
| `docs/parla/oral/les-campanes-robert-lizarte.md` | sí | `ari-capsules` | 40 | 436 | 144 | no / pendent |
| `docs/parla/oral/les-falles-albert-roig.md` | sí | `ari-capsules` | 34 | 867 | 137 | sí, cal verificar peça |
| `docs/parla/oral/les-moles-de-farina.md` | sí | `ari-capsules` | 11 | 145 | 82 | no / pendent |
| `docs/parla/oral/qui-eren-els-constituents.md` | no | `actes-historiques-consell-general` | — | 0 | 0 | no / pendent |
| `docs/parla/oral/testimoni-constituent-adellach.md` | sí | `consell-general-constituent` | — | 114 | 185 | no / pendent |
| `docs/parla/oral/testimoni-constituent-aleix.md` | sí | `consell-general-constituent` | — | 244 | 116 | no / pendent |
| `docs/parla/oral/testimoni-constituent-aleixareny.md` | sí | `consell-general-constituent` | — | 1851 | 431 | no / pendent |
| `docs/parla/oral/testimoni-constituent-altimir.md` | sí | `consell-general-constituent` | — | 221 | 215 | no / pendent |
| `docs/parla/oral/testimoni-constituent-areny.md` | sí | `consell-general-constituent` | — | 368 | 375 | no / pendent |
| `docs/parla/oral/testimoni-constituent-arenyfite.md` | sí | `consell-general-constituent` | — | 156 | 208 | no / pendent |
| `docs/parla/oral/testimoni-constituent-armengol.md` | sí | `consell-general-constituent` | — | 150 | 154 | no / pendent |
| `docs/parla/oral/testimoni-constituent-armengolvila.md` | sí | `consell-general-constituent` | — | 151 | 97 | no / pendent |
| `docs/parla/oral/testimoni-constituent-baro.md` | sí | `consell-general-constituent` | — | 522 | 652 | no / pendent |
| `docs/parla/oral/testimoni-constituent-bartumeu.md` | sí | `consell-general-constituent` | — | 1339 | 323 | no / pendent |
| `docs/parla/oral/testimoni-constituent-canut.md` | sí | `consell-general-constituent` | — | 1125 | 402 | no / pendent |
| `docs/parla/oral/testimoni-constituent-casadevall.md` | sí | `consell-general-constituent` | — | 513 | 205 | no / pendent |
| `docs/parla/oral/testimoni-constituent-cassanyvila.md` | sí | `consell-general-constituent` | — | 46 | 107 | no / pendent |
| `docs/parla/oral/testimoni-constituent-dalleres.md` | sí | `consell-general-constituent` | — | 201 | 411 | no / pendent |
| `docs/parla/oral/testimoni-constituent-dolsa.md` | sí | `consell-general-constituent` | — | 677 | 263 | no / pendent |
| `docs/parla/oral/testimoni-constituent-farras.md` | sí | `consell-general-constituent` | — | 546 | 817 | no / pendent |
| `docs/parla/oral/testimoni-constituent-garralla.md` | sí | `consell-general-constituent` | — | 121 | 259 | no / pendent |
| `docs/parla/oral/testimoni-constituent-gaspa.md` | sí | `consell-general-constituent` | — | 77 | 131 | no / pendent |
| `docs/parla/oral/testimoni-constituent-gelabert.md` | sí | `consell-general-constituent` | — | 844 | 246 | no / pendent |
| `docs/parla/oral/testimoni-constituent-jordiareny.md` | sí | `consell-general-constituent` | — | 42 | 65 | no / pendent |
| `docs/parla/oral/testimoni-constituent-mandico.md` | sí | `consell-general-constituent` | — | 454 | 250 | no / pendent |
| `docs/parla/oral/testimoni-constituent-marsal.md` | sí | `consell-general-constituent` | — | 458 | 174 | no / pendent |
| `docs/parla/oral/testimoni-constituent-mastorres.md` | sí | `consell-general-constituent` | — | 314 | 131 | no / pendent |
| `docs/parla/oral/testimoni-constituent-naudi.md` | sí | `consell-general-constituent` | — | 133 | 188 | no / pendent |
| `docs/parla/oral/testimoni-constituent-reig.md` | sí | `consell-general-constituent` | — | 1357 | 383 | no / pendent |
| `docs/parla/oral/testimoni-constituent-santamaria.md` | sí | `consell-general-constituent` | — | 384 | 98 | no / pendent |
| `docs/parla/oral/testimoni-constituent-torresalis.md` | sí | `consell-general-constituent` | — | 51 | 42 | no / pendent |
| `docs/parla/oral/toponimia-preromana-xavier-planas.md` | sí | `ari-capsules` | 45 | 148 | 243 | no / pendent |
| `docs/parla/oral/un-raco-descaldes.md` | sí | `ari-capsules` | 57 | 232 | 151 | sí, cal verificar peça |

El manifest detallat queda a `work/eligibility-inventory.json` (ignorat per Git).
