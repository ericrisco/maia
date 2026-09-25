# Tercera descodificació greedy — lead-rtva-003-dj-neura

La passada `greedy` usa `ggml-small.bin` amb beam 1 sobre els **10 clips** de formes. El text és una tercera evidència ASR, no una decisió auditiva ni una atribució de veu.

| categoria | clips |
|---|---:|
| A-tres-models | 0 |
| B-dos-models | 3 |
| C-un-model | 2 |
| D-cap-model | 5 |

El detall és a `qa-greedy.tsv`; els JSON i TXT de cada clip es conserven a `qa-greedy/`.
