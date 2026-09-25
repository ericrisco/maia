# Resegmentació curta de les veus en quarantena

Aquesta passada usa finestres no solapades de 20 segons i `ggml-base.bin`, sense context acumulat. És una transcripció ASR auxiliar per reduir bucles; no és una validació humana ni entra al graf.

| veu | finestres | mitjana de línies úniques | finestres < 0,80 | transcripció combinada |
|---|---:|---:|---:|---|
| pa-044 | 81 | 0.974 | 3 | [`pa-044-combinada.txt`](qa-quarantena-20s/pa-044-combinada.txt) |
| pa-047 | 79 | 0.990 | 2 | [`pa-047-combinada.txt`](qa-quarantena-20s/pa-047-combinada.txt) |
| pa-050 | 77 | 1.000 | 0 | [`pa-050-combinada.txt`](qa-quarantena-20s/pa-050-combinada.txt) |

Els fragments amb text coherent són candidats per a escolta i revisió. Les formes, variants, fonètica i prosòdia continuen pendents d'anotació auditiva.
