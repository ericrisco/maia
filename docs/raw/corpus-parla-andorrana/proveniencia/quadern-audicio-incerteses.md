# Cua d'audició d'incerteses ASR

Mostra de **100 clips** de `registre-audicio.tsv` que contenen almenys un token ASR amb probabilitat inferior a 0,55.

La selecció cobreix primer una fila per persona i després prioritza la probabilitat més baixa. No és una mostra dialectològica: serveix per corregir transcripció i decidir quins fragments mereixen anotació fonètica o prosòdica.

- Font: `inventari-incerteses-asr.tsv` i `registre-audicio.tsv`.
- Camps humans: es mantenen buits fins a l'escolta.
- Importació: `importa-auditoria.py` pot projectar anotacions si la clau exacta coincideix.

| ordre | persona | forma | clip | segments incerts | probabilitat mínima | estat |
|---:|---|---|---|---:|---:|---|
| 1 | pa-024 | doncs | `clips/pa-024__doncs__83.01.wav` | 3 | 0.0066 | pendent |
| 2 | pa-024 | és a dir | `clips/pa-024__s-a-dir__78.49.wav` | 3 | 0.0066 | pendent |
| 3 | pa-055 | evidentment | `clips/pa-055__evidentment__1644.01.wav` | 2 | 0.0100 | pendent |
| 4 | pa-014 | aviam | `clips/pa-014__aviam__875.45.wav` | 3 | 0.0142 | pendent |
| 5 | pa-007 | evidentment | `clips/pa-007__evidentment__778.25.wav` | 3 | 0.0152 | pendent |
| 6 | pa-040 | crec | `clips/pa-040__crec__4.37.wav` | 3 | 0.0158 | pendent |
| 7 | pa-062 | vull dir | `clips/pa-062__vull-dir__316.81.wav` | 3 | 0.0174 | pendent |
| 8 | pa-024 | a nivell | `clips/pa-024__a-nivell__1547.93.wav` | 2 | 0.0196 | pendent |
| 9 | pa-056 | crec | `clips/pa-056__crec__347.05.wav` | 3 | 0.0272 | pendent |
| 10 | pa-041 | ensenyança | `clips/pa-041__ensenyan-a__523.25.wav` | 2 | 0.0299 | pendent |
| 11 | pa-041 | bueno | `clips/pa-041__bueno__165.25.wav` | 3 | 0.0314 | pendent |
| 12 | pa-006 | llavors | `clips/pa-006__llavors__214.25.wav` | 3 | 0.0317 | pendent |
| 13 | pa-022 | llavors | `clips/pa-022__llavors__57.37.wav` | 3 | 0.0320 | pendent |
| 14 | pa-037 | doncs | `clips/pa-037__doncs__20.49.wav` | 3 | 0.0323 | pendent |
| 15 | pa-017 | bé | `clips/pa-017__b__112.25.wav` | 3 | 0.0357 | pendent |
| 16 | pa-063 | perquè | `clips/pa-063__perqu__142.61.wav` | 3 | 0.0358 | pendent |
| 17 | pa-059 | bé | `clips/pa-059__b__112.41.wav` | 2 | 0.0362 | pendent |
| 18 | pa-064 | llavors | `clips/pa-064__llavors__713.33.wav` | 3 | 0.0364 | pendent |
| 19 | pa-037 | diguem | `clips/pa-037__diguem__469.77.wav` | 3 | 0.0389 | pendent |
| 20 | pa-006 | diguem | `clips/pa-006__diguem__530.25.wav` | 2 | 0.0391 | pendent |
| 21 | pa-010 | llavors | `clips/pa-010__llavors__386.25.wav` | 3 | 0.0400 | pendent |
| 22 | pa-024 | perquè | `clips/pa-024__perqu__225.53.wav` | 3 | 0.0403 | pendent |
| 23 | pa-024 | clar | `clips/pa-024__clar__648.09.wav` | 3 | 0.0409 | pendent |
| 24 | pa-034 | bueno | `clips/pa-034__bueno__33.81.wav` | 3 | 0.0452 | pendent |
| 25 | pa-034 | llavors | `clips/pa-034__llavors__29.17.wav` | 3 | 0.0452 | pendent |
| 26 | pa-061 | bé | `clips/pa-061__b__662.89.wav` | 2 | 0.0454 | pendent |
| 27 | pa-060 | aleshores | `clips/pa-060__aleshores__147.17.wav` | 2 | 0.0462 | pendent |
| 28 | pa-060 | bueno | `clips/pa-060__bueno__150.05.wav` | 3 | 0.0462 | pendent |
| 29 | pa-001 | vull dir | `clips/pa-001__vull-dir__621.37.wav` | 2 | 0.0480 | pendent |
| 30 | pa-024 | de fet | `clips/pa-024__de-fet__482.25.wav` | 2 | 0.0481 | pendent |
| 31 | pa-052 | clar | `clips/pa-052__clar__59.97.wav` | 3 | 0.0496 | pendent |
| 32 | pa-052 | llavors | `clips/pa-052__llavors__68.73.wav` | 3 | 0.0496 | pendent |
| 33 | pa-065 | a nivell | `clips/pa-065__a-nivell__529.09.wav` | 3 | 0.0537 | pendent |
| 34 | pa-001 | clar | `clips/pa-001__clar__129.77.wav` | 3 | 0.0548 | pendent |
| 35 | pa-024 | bé | `clips/pa-024__b__175.29.wav` | 3 | 0.0550 | pendent |
| 36 | pa-063 | aleshores | `clips/pa-063__aleshores__151.45.wav` | 2 | 0.0552 | pendent |
| 37 | pa-049 | diguem | `clips/pa-049__diguem__213.13.wav` | 3 | 0.0556 | pendent |
| 38 | pa-022 | bueno | `clips/pa-022__bueno__122.85.wav` | 2 | 0.0565 | pendent |
| 39 | pa-022 | doncs | `clips/pa-022__doncs__122.85.wav` | 2 | 0.0565 | pendent |
| 40 | pa-022 | reformeta | `clips/pa-022__reformeta__125.53.wav` | 2 | 0.0565 | pendent |
| 41 | pa-055 | reformeta | `clips/pa-055__reformeta__139.05.wav` | 1 | 0.0580 | pendent |
| 42 | pa-059 | perquè | `clips/pa-059__perqu__4.09.wav` | 3 | 0.0581 | pendent |
| 43 | pa-017 | perquè | `clips/pa-017__perqu__4.25.wav` | 3 | 0.0602 | pendent |
| 44 | pa-056 | bé | `clips/pa-056__b__436.49.wav` | 3 | 0.0611 | pendent |
| 45 | pa-049 | llavors | `clips/pa-049__llavors__230.45.wav` | 2 | 0.0629 | pendent |
| 46 | pa-010 | bé | `clips/pa-010__b__24.65.wav` | 2 | 0.0636 | pendent |
| 47 | pa-010 | doncs | `clips/pa-010__doncs__24.65.wav` | 2 | 0.0636 | pendent |
| 48 | pa-029 | tirar endavant | `clips/pa-029__tirar-endavant__56.73.wav` | 3 | 0.0643 | pendent |
| 49 | pa-027 | o sigui | `clips/pa-027__o-sigui__361.61.wav` | 3 | 0.0663 | pendent |
| 50 | pa-062 | és a dir | `clips/pa-062__s-a-dir__973.65.wav` | 3 | 0.0665 | pendent |
| 51 | pa-016 | doncs | `clips/pa-016__doncs__62.33.wav` | 2 | 0.0667 | pendent |
| 52 | pa-023 | crec | `clips/pa-023__crec__42.93.wav` | 2 | 0.0678 | pendent |
| 53 | pa-023 | llavors | `clips/pa-023__llavors__48.81.wav` | 3 | 0.0678 | pendent |
| 54 | pa-057 | o sigui | `clips/pa-057__o-sigui__249.45.wav` | 3 | 0.0678 | pendent |
| 55 | pa-057 | perquè | `clips/pa-057__perqu__249.45.wav` | 3 | 0.0678 | pendent |
| 56 | pa-020 | diguem | `clips/pa-020__diguem__1459.77.wav` | 2 | 0.0701 | pendent |
| 57 | pa-019 | diguem | `clips/pa-019__diguem__109.25.wav` | 1 | 0.0703 | pendent |
| 58 | pa-001 | a veure | `clips/pa-001__a-veure__341.57.wav` | 3 | 0.0725 | pendent |
| 59 | pa-028 | clar | `clips/pa-028__clar__290.33.wav` | 3 | 0.0738 | pendent |
| 60 | pa-027 | doncs | `clips/pa-027__doncs__18.01.wav` | 3 | 0.0761 | pendent |
| 61 | pa-037 | llavors | `clips/pa-037__llavors__92.53.wav` | 3 | 0.0772 | pendent |
| 62 | pa-031 | de fet | `clips/pa-031__de-fet__9.93.wav` | 1 | 0.0776 | pendent |
| 63 | pa-060 | bé | `clips/pa-060__b__415.73.wav` | 3 | 0.0793 | pendent |
| 64 | pa-037 | bueno | `clips/pa-037__bueno__105.29.wav` | 3 | 0.0796 | pendent |
| 65 | pa-037 | bé | `clips/pa-037__b__105.29.wav` | 3 | 0.0796 | pendent |
| 66 | pa-020 | clar | `clips/pa-020__clar__89.81.wav` | 3 | 0.0810 | pendent |
| 67 | pa-024 | llavors | `clips/pa-024__llavors__336.85.wav` | 3 | 0.0814 | pendent |
| 68 | pa-004 | evidentment | `clips/pa-004__evidentment__522.93.wav` | 3 | 0.0816 | pendent |
| 69 | pa-029 | a nivell | `clips/pa-029__a-nivell__417.09.wav` | 3 | 0.0819 | pendent |
| 70 | pa-049 | a veure | `clips/pa-049__a-veure__244.85.wav` | 3 | 0.0828 | pendent |
| 71 | pa-046 | diguem | `clips/pa-046__diguem__626.01.wav` | 2 | 0.0844 | pendent |
| 72 | pa-009 | llavors | `clips/pa-009__llavors__201.25.wav` | 3 | 0.0851 | pendent |
| 73 | pa-058 | a nivell | `clips/pa-058__a-nivell__188.37.wav` | 1 | 0.0856 | pendent |
| 74 | pa-021 | vull dir | `clips/pa-021__vull-dir__314.29.wav` | 2 | 0.0875 | pendent |
| 75 | pa-002 | llavors | `clips/pa-002__llavors__550.25.wav` | 3 | 0.0897 | pendent |
| 76 | pa-045 | doncs | `clips/pa-045__doncs__283.01.wav` | 2 | 0.0923 | pendent |
| 77 | pa-032 | bueno | `clips/pa-032__bueno__44.73.wav` | 1 | 0.0954 | pendent |
| 78 | pa-054 | a veure | `clips/pa-054__a-veure__77.97.wav` | 1 | 0.0959 | pendent |
| 79 | pa-048 | o sigui | `clips/pa-048__o-sigui__581.65.wav` | 1 | 0.0962 | pendent |
| 80 | pa-038 | reformeta | `clips/pa-038__reformeta__1821.69.wav` | 2 | 0.1004 | pendent |
| 81 | pa-008 | és a dir | `clips/pa-008__s-a-dir__1110.25.wav` | 2 | 0.1021 | pendent |
| 82 | pa-051 | de fet | `clips/pa-051__de-fet__200.81.wav` | 2 | 0.1121 | pendent |
| 83 | pa-030 | és a dir | `clips/pa-030__s-a-dir__193.13.wav` | 1 | 0.1172 | pendent |
| 84 | pa-035 | bé | `clips/pa-035__b__715.81.wav` | 3 | 0.1174 | pendent |
| 85 | pa-026 | bé | `clips/pa-026__b__99.97.wav` | 2 | 0.1189 | pendent |
| 86 | pa-043 | crec | `clips/pa-043__crec__102.25.wav` | 3 | 0.1230 | pendent |
| 87 | pa-053 | llavors | `clips/pa-053__llavors__40.73.wav` | 2 | 0.1278 | pendent |
| 88 | pa-036 | doncs | `clips/pa-036__doncs__367.25.wav` | 3 | 0.1332 | pendent |
| 89 | pa-018 | és a dir | `clips/pa-018__s-a-dir__74.49.wav` | 2 | 0.1423 | pendent |
| 90 | pa-013 | perquè | `clips/pa-013__perqu__433.89.wav` | 2 | 0.1428 | pendent |
| 91 | pa-011 | bé | `clips/pa-011__b__185.57.wav` | 3 | 0.1482 | pendent |
| 92 | pa-033 | tirar endavant | `clips/pa-033__tirar-endavant__135.69.wav` | 3 | 0.1485 | pendent |
| 93 | pa-025 | bueno | `clips/pa-025__bueno__909.25.wav` | 3 | 0.1490 | pendent |
| 94 | pa-039 | crec | `clips/pa-039__crec__90.85.wav` | 1 | 0.1570 | pendent |
| 95 | pa-005 | llavors | `clips/pa-005__llavors__433.29.wav` | 2 | 0.1648 | pendent |
| 96 | pa-015 | bé | `clips/pa-015__b__42.25.wav` | 1 | 0.1814 | pendent |
| 97 | pa-012 | bé | `clips/pa-012__b__160.25.wav` | 2 | 0.1898 | pendent |
| 98 | pa-042 | clar | `clips/pa-042__clar__101.97.wav` | 3 | 0.1933 | pendent |
| 99 | pa-003 | bé | `clips/pa-003__b__0.00.wav` | 2 | 0.1987 | pendent |
| 100 | pa-066 | bé | `clips/pa-066__b__10.13.wav` | 1 | 0.2454 | pendent |
