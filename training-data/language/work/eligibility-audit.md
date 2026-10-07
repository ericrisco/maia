# Auditoria d'elegibilitat de Maia Language

Data de tall: 2026-10-07. Criteris: `veu: originaria`, `epoca: contemporania` i `apte_llengua: true`, amb drets compatibles i transcripció verificada, segons [`PLAN.md`](../../PLAN.md).

## Resultat

- Peces candidates pels metadades: **38** (11 càpsules d'AR+I i 27 testimonis del Consell Constituent).
- Transcripcions verificades contra l'àudio: **0 de 38**. Totes les fitxes candidates tenen `transcripcio-no-verificada`; vuit també marquen incertesa de transcripció.
- Peces que ara mateix compleixen tots els requisits per entrar al dataset: **0**.

## Drets de les peces candidates

- **Càpsules d'AR+I:** la fitxa de la sèrie diu que la llicència s'ha de verificar peça per peça. D'entre les onze candidates, les peces **34, 56 i 57** tenen atribució CC BY declarada/verificada. Les altres vuit no tenen una verificació individual registrada.
- **Testimonis del Consell Constituent:** la font declara la llicència estàndard de YouTube i la redistribució pendent; no s'inclouen sense permís o una llicència compatible.

Una llicència oberta no substitueix la verificació de la transcripció. Cap fragment passa la porta d'entrada mentre la parla no s'hagi cotejat amb la font.

## Primer candidat per verificar

La càpsula **34**, d'Albert Roig, té llicència CC BY individual confirmada. En aquest checkout hi ha fitxers locals d'àudio i vídeo, però són fora de Git i no formen part d'aquest informe com a contingut entrenable. La fitxa registra 121 marques d'incertesa en 867 segments; cap fragment no està verificat escoltant l'àudio.

Per començar l'exportació Language cal cotejar fragments concrets amb l'àudio, documentar les correccions i tornar a calcular l'elegibilitat. Fins aleshores, `output/` continua buit.

## Fragment candidat en revisió

S'ha preparat el fragment `ari34-falles-intro-001` (00:41.940–00:47.360). El text coincideix amb la transcripció del corpus i amb dues sortides Whisper independents. És una comprovació automàtica creuada, **no** una escolta humana; el registre continua en esborrany i no és elegible per a l'exportació.
