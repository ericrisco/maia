# Tercera descodificació greedy — lead-rtva-004-joan-mico

La passada `greedy` usa `ggml-small.bin` amb beam 1 sobre els **12 clips** de formes. El text és una tercera evidència ASR, no una decisió auditiva ni una atribució de veu.

| categoria | clips |
|---|---:|
| A-tres-models | 1 |
| B-dos-models | 1 |
| C-un-model | 6 |
| D-cap-model | 4 |

El detall és a `qa-greedy.tsv`; els JSON i TXT de cada clip es conserven a `qa-greedy/`.
