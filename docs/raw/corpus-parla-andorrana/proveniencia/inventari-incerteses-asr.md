# Inventari d'incerteses ASR

La taula `inventari-incerteses-asr.tsv` conserva **13390 segments** amb almenys un token de probabilitat inferior a **0.55**. Cada fila apunta al segment JSON, al text ASR i als clips de la cua que el contenen.

Aquesta és una cua d'audició i correcció de transcripció. Les formes i tokens són hipòtesis del model; no són variants dialectals ni observacions fonètiques.

- Persones amb almenys un segment: **66** de 66.
- Segments associats a algun clip de forma: **1283**.

## Formes amb més segments incerts

- `perquè`: 128 segments.
- `clar`: 122 segments.
- `bueno`: 122 segments.
- `bé`: 116 segments.
- `doncs`: 114 segments.
- `llavors`: 108 segments.
- `és a dir`: 90 segments.
- `a veure`: 78 segments.
- `vull dir`: 78 segments.
- `evidentment`: 78 segments.
- `crec`: 76 segments.
- `o sigui`: 73 segments.
- `a nivell`: 58 segments.
- `diguem`: 54 segments.
- `de fet`: 50 segments.
- `aleshores`: 43 segments.
- `tirar endavant`: 24 segments.
- `reformeta`: 15 segments.
- `aviam`: 12 segments.
- `ensenyança`: 5 segments.

Per tancar una fila cal escoltar l'interval i registrar la decisió, la variant escoltada i les observacions pertinents a `registre-audicio.tsv`.
