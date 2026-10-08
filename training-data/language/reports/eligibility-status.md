# Estat d’elegibilitat de Maia Language

Data de l’auditoria: 2026-10-08. Àmbit: els 45 Markdown inventariats a `docs/parla/`.

## Resultat

Hi ha **45 fitxers**: 40 peces o registres de parla i 5 índexs. Ara mateix hi ha **0 converses elegibles** per a l’export de xat. Els exports continuen buits.

El motiu principal no és la manca de material humà. És que les transcripcions disponibles no contenen parelles de torns humà-user/humà-assistant que es puguin convertir sense inventar preguntes. Les càpsules d’AR+I són exposicions preparades. A les entrevistes del Consell Constituent, les preguntes de l’entrevistador s’han editat fora del vídeo i del text transcrit.

## Decisions per grup

| Grup | Peces | Resultat | Raó |
|---|---:|---|---|
| Índexs | 5 | Exclosos | No són mostra de parla. |
| Entrevistes del Consell Constituent | 27 | En espera | Totes tenen transcripció no verificada; 8 també estan marcades `transcripcio-incerta`. La llicència de YouTube no documenta redistribució. Les preguntes humanes no apareixen als talls editats. |
| Càpsules AR+I, veu originària, CC BY confirmada (#34, #56, #57) | 3 | Excloses del xat actual | Llicència verificada, però són exposicions preparades; transcripció i varietat del parlant encara no verificades. No hi ha torns humans de pregunta-resposta. |
| Càpsules AR+I amb llicència individual pendent | 7 | Excloses del xat actual | Xerrades preparades; llicència, transcripció i varietat del parlant pendents. Una, #45, està marcada `contingut-no-citable`. |
| Càpsula AR+I compilada #49 | 1 | Exclosa | `veu=compilada`, `apte_llengua=false`; també hi ha indicis de lectura i la transcripció no està verificada. |
| Resum d’actes del Consell | 1 | Exclòs | Metadades compilades, no parla. |

Les decisions peça per peça, l’estat de transcripció, el perfil del parlant i les notes de drets són a [`../work/coverage.csv`](../work/coverage.csv).

## Criteri per reprendre el treball

- No crear cap missatge d’usuari per a un monòleg ni per a una resposta a la qual s’ha tallat la pregunta.
- Una transcripció només passa a `verified` després de contrastar-la amb l’àudio i marcar els trams incerts.
- Una llicència oberta de vídeo no verifica la transcripció ni la varietat dialectal.
- Les entrevistes del Consell necessiten autorització compatible amb l’ús previst i preguntes humanes recuperables d’una font publicada.
- Les peces AR+I necessiten una conversa real o preguntes-respostes audibles per entrar en el JSONL de xat.

Fins que no es compleixin aquests punts, no hi ha base per exportar registres de Maia Language sense fabricar estructura conversacional.
