# Incidències de tokenització en consensos ASR

Aquest informe recull els **14 clips** on `ggml-small.bin` i `ggml-base.bin` coincideixen a nivell de text del fragment, però la passada JSON base no troba una seqüència de tokens que coincideixi exactament amb la forma. No són descartes: són els primers casos per escoltar i decidir si hi ha segmentació, reducció fonètica, variant lèxica o error ASR.

Cada entrada conserva l'àudio, el JSON complet i els descriptors acústics.

## pa-002 — bé — 348.25-355.75

- Àudio: [`clips/pa-002__b__348.25.wav`](clips/pa-002__b__348.25.wav)
- JSON base: [`qa-consens-base-json/pa-002__b__348_25.json`](qa-consens-base-json/pa-002__b__348_25.json)
- Text small: que ha signat el canvi.  Ara, el que ens dividiria bé,  òbviament, era el control de govern.
- Text base: de tot canvi. Ara, el que ets llibre, el cop i a mena, era el control de cobert.
- Interval: 348.25-355.75 s · F0: 309.71 Hz · veu: 0.4733 · pausa: 0.090 s · centroid: 1231.82 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-008 — clar — 841.25-846.75

- Àudio: [`clips/pa-008__clar__841.25.wav`](clips/pa-008__clar__841.25.wav)
- JSON base: [`qa-consens-base-json/pa-008__clar__841_25.json`](qa-consens-base-json/pa-008__clar__841_25.json)
- Text small: Clar, hem de pensar que els fallares que 87 van començar a tornar a cremar l'espai públic
- Text base: Esclar, hem de pensar que els fallaïres que 87 van començar a tornar a cremar l'espai públic.
- Interval: 841.25-846.75 s · F0: 174.34 Hz · veu: 0.5328 · pausa: 0.060 s · centroid: 1280.12 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-013 — bé — 196.65-203.47

- Àudio: [`clips/pa-013__b__196.65.wav`](clips/pa-013__b__196.65.wav)
- JSON base: [`qa-consens-base-json/pa-013__b__196_65.json`](qa-consens-base-json/pa-013__b__196_65.json)
- Text small: que em sofre i que va bé per la pell, pel sistema digestiu, i també té altres propietats.
- Text base: que em sofre i que la ve per la pell, pel sistema digestiu, i també té altres propietats.
- Interval: 196.65-203.47 s · F0: 301.12 Hz · veu: 0.7029 · pausa: 0.040 s · centroid: 1061.40 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-019 — diguem — 109.25-113.75

- Àudio: [`clips/pa-019__diguem__109.25.wav`](clips/pa-019__diguem__109.25.wav)
- JSON base: [`qa-consens-base-json/pa-019__diguem__109_25.json`](qa-consens-base-json/pa-019__diguem__109_25.json)
- Text small: I va haver una certa, diguem-ne, un bon feeling, no?
- Text base: I m'ha aviat una certa, diguem-ne, un bon fillig, no?
- Interval: 109.25-113.75 s · F0: 146.29 Hz · veu: 0.5446 · pausa: 0.100 s · centroid: 1031.32 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-021 — bé — 257.61-263.59

- Àudio: [`clips/pa-021__b__257.61.wav`](clips/pa-021__b__257.61.wav)
- JSON base: [`qa-consens-base-json/pa-021__b__257_61.json`](qa-consens-base-json/pa-021__b__257_61.json)
- Text small: És ben veritat que, com es diu,
- Text base: És ben veritat que, com has diu, un error.
- Interval: 257.61-263.59 s · F0: 232.22 Hz · veu: 0.4799 · pausa: 0.120 s · centroid: 1185.54 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-022 — bé — 270.45-275.35

- Àudio: [`clips/pa-022__b__270.45.wav`](clips/pa-022__b__270.45.wav)
- JSON base: [`qa-consens-base-json/pa-022__b__270_45.json`](qa-consens-base-json/pa-022__b__270_45.json)
- Text small: A part que ja feia anys que es venia empenyent amb el canvi i també...
- Text base: que es venien en peñen amb el canvi i també.
- Interval: 270.45-275.35 s · F0: 272.82 Hz · veu: 0.6803 · pausa: 0.060 s · centroid: 1116.03 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-022 — o sigui — 42.93-48.95

- Àudio: [`clips/pa-022__o-sigui__42.93.wav`](clips/pa-022__o-sigui__42.93.wav)
- JSON base: [`qa-consens-base-json/pa-022__o-sigui__42_93.json`](qa-consens-base-json/pa-022__o-sigui__42_93.json)
- Text small: O sigui, al fondo el que es buscaveré tindrà una independència com a país.
- Text base: No res a fer, bo sigui el fondo que és buscar haver-hi tindre una independència com a país.
- Interval: 42.93-48.95 s · F0: 266.57 Hz · veu: 0.5967 · pausa: 0.060 s · centroid: 1114.90 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-031 — a veure — 4.25-9.07

- Àudio: [`clips/pa-031__a-veure__4.25.wav`](clips/pa-031__a-veure__4.25.wav)
- JSON base: [`qa-consens-base-json/pa-031__a-veure__4_25.json`](qa-consens-base-json/pa-031__a-veure__4_25.json)
- Text small: I es va decidir que a veure quin sindic podien portar i tothom podria portar.
- Text base: I jo ho deixi dir que va veure quin síndic pugui un proportat i tot el temps pugui ser.
- Interval: 4.25-9.07 s · F0: 143.96 Hz · veu: 0.5208 · pausa: 0.060 s · centroid: 1202.91 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-037 — diguem — 469.77-482.03

- Àudio: [`clips/pa-037__diguem__469.77.wav`](clips/pa-037__diguem__469.77.wav)
- JSON base: [`qa-consens-base-json/pa-037__diguem__469_77.json`](qa-consens-base-json/pa-037__diguem__469_77.json)
- Text small: Bé, marxar. Una cosa que em va satisfir molt va ser que vaig fer desíndic, diguem-ho així,  durant una hora o més.
- Text base: una cosa que em va ser desfem molt, molt,  va ser que vaig fer desindic, diguem-ho, xis,  durant misora o una hora.
- Interval: 469.77-482.03 s · F0: 242.06 Hz · veu: 0.4395 · pausa: 0.100 s · centroid: 1334.90 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-051 — clar — 161.85-167.07

- Àudio: [`clips/pa-051__clar__161.85.wav`](clips/pa-051__clar__161.85.wav)
- JSON base: [`qa-consens-base-json/pa-051__clar__161_85.json`](qa-consens-base-json/pa-051__clar__161_85.json)
- Text small: entor, tronassorda i joclar això l'he rendat als remats.
- Text base: en tor, per a una sort de joclar i això l'he rendat al remat.
- Interval: 161.85-167.07 s · F0: 197.87 Hz · veu: 0.6269 · pausa: 0.080 s · centroid: 1380.87 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-056 — bé — 436.49-441.47

- Àudio: [`clips/pa-056__b__436.49.wav`](clips/pa-056__b__436.49.wav)
- JSON base: [`qa-consens-base-json/pa-056__b__436_49.json`](qa-consens-base-json/pa-056__b__436_49.json)
- Text small: "Pasabe" o "pero sentimen" o "pero nonimidad".
- Text base: o pasabeu, però sentim-me, però no limitad.
- Interval: 436.49-441.47 s · F0: 159.29 Hz · veu: 0.3387 · pausa: 0.040 s · centroid: 1709.65 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-057 — diguem — 929.81-935.31

- Àudio: [`clips/pa-057__diguem__929.81.wav`](clips/pa-057__diguem__929.81.wav)
- JSON base: [`qa-consens-base-json/pa-057__diguem__929_81.json`](qa-consens-base-json/pa-057__diguem__929_81.json)
- Text small: però que no siguis un club, diguem-ho així.
- Text base: Però que no sigui és un club, diguem-ho així.
- Interval: 929.81-935.31 s · F0: 226.75 Hz · veu: 0.4380 · pausa: 0.100 s · centroid: 1962.97 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-064 — a veure — 587.61-591.67

- Àudio: [`clips/pa-064__a-veure__587.61.wav`](clips/pa-064__a-veure__587.61.wav)
- JSON base: [`qa-consens-base-json/pa-064__a-veure__587_61.json`](qa-consens-base-json/pa-064__a-veure__587_61.json)
- Text small: No s'ha tornat a veure amb els anys.
- Text base: -El set de nata veure amb els anys.
- Interval: 587.61-591.67 s · F0: 223.51 Hz · veu: 0.4406 · pausa: 0.110 s · centroid: 1469.24 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## pa-065 — a nivell — 529.09-536.75

- Àudio: [`clips/pa-065__a-nivell__529.09.wav`](clips/pa-065__a-nivell__529.09.wav)
- JSON base: [`qa-consens-base-json/pa-065__a-nivell__529_09.json`](qa-consens-base-json/pa-065__a-nivell__529_09.json)
- Text small: i el que podreu donar.  Nosaltres venim als santuaris,  trobades a nivell català i a nivell espanyol.
- Text base: que no podreu d'una.  Nosaltres tenim els santuaris.  Trobades, amb teta l'unió,  amb teta nivell d'esquerra.
- Interval: 529.09-536.75 s · F0: 145.24 Hz · veu: 0.3691 · pausa: 0.100 s · centroid: 893.80 Hz
- Hipòtesi de treball: coincidència de segment, però tokenització base no exacta; cal escoltar.
- Decisió auditiva: `pendent`
- Variant escoltada:
- Trets fonètics:
- Prosòdia / pauses:
- Nota:

## Contraste tokenitzat independent

Una segunda tokenització amb `ggml-small.bin` localitza **7** de les 14 formes que `ggml-base.bin` no havia alineat; **7** continuen sense token en cap dels dos JSON. Això separa una possible diferència de tokenitzador d'una incidència persistent, però no resol la pronúncia sense escolta.

Casos recuperats pel small: pa-002 bé; pa-008 clar; pa-013 bé; pa-022 o sigui; pa-031 a veure; pa-064 a veure; pa-065 a nivell.

Casos sense token en tots dos: pa-019 diguem; pa-021 bé; pa-022 bé; pa-037 diguem; pa-051 clar; pa-056 bé; pa-057 diguem.

La taula completa és `qa-token-missing-comparativa.tsv`.
