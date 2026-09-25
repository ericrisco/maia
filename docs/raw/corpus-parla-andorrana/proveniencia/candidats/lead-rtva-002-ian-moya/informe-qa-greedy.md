# Tercera descodificació greedy — lead-rtva-002-ian-moya

La passada `greedy` usa `ggml-small.bin` amb beam 1 sobre els **15 clips** de formes. El text és una tercera evidència ASR, no una decisió auditiva ni una atribució de veu.

| categoria | clips |
|---|---:|
| A-tres-models | 2 |
| B-dos-models | 1 |
| C-un-model | 7 |
| D-cap-model | 5 |

El detall és a `qa-greedy.tsv`; els JSON i TXT de cada clip es conserven a `qa-greedy/`.
