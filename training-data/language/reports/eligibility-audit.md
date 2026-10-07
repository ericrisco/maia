# Auditoria inicial d'elegibilitat de Maia Language

**Revisió:** 2026-10-07

**Abast:** 40 peces de parla oral incloses a `work/eligibility-inventory.json`. Els índexs de `docs/parla/` no són peces de parla i queden fora del recompte.

## Estat observat

- **40 peces** inventariades.
- **38** compleixen al frontmatter `veu=originaria`, `epoca=contemporania` i `apte_llengua=true`.
- **2** tenen `apte_llengua=false` i no s'han d'incloure.
- Les 40 peces apunten a una fitxa de font amb redistribució general `pendent`.
- La llicència CC BY s'ha verificat per a **4 vídeos individuals**. Només **3** d'aquests són elegibles per veu i època (#34, #56 i #57); la peça #49 no compleix `apte_llengua`.
- **39 de 40** transcripcions porten marques de text no verificat. Els tres vídeos elegibles amb llicència individual verificada també tenen marques d'incertesa a la transcripció.
- `review/conversations.jsonl` conté **un candidat**, de la càpsula #34. El fragment no té marques d'incertesa, però encara no s'ha contrastat amb l'àudio. Continua en revisió i no s'exporta.

## Decisió de treball

No generar frases noves perquè «sonin andorranes». Cada resposta de Language ha de provenir de parla humana real i conservar-ne les paraules. Per a cada peça, cal:

1. confirmar l'elegibilitat a partir dels camps del corpus;
2. verificar els drets de la peça individual, sense estendre el permís d'un vídeo a tota la sèrie;
3. escoltar l'àudio i comparar-hi els fragments proposats;
4. excloure o marcar qualsevol fragment dubtós, llegit o mal transcrit;
5. conservar la procedència, la veu identificada i el grup de split.

Fins que no es compleixin aquests passos, una peça és pendent, no una dada aprovada. Els fragments consecutius d'una mateixa càpsula han d'anar al mateix grup abans de fer `train`, `validation` i `test`.

## Material pendent

- Verificar a l'àudio els tres candidats amb llicència individual confirmada: càpsules #34, #56 i #57.
- Comprovar si hi ha altres vídeos individuals amb permís reutilitzable; la fitxa general d'AR+I diu explícitament que no s'ha d'estendre una llicència a tota la sèrie.
- Escoltar i classificar les altres 35 peces que compleixen els camps d'elegibilitat, començant per les que tinguin drets verificables i fragments menys incerts.
- Revisar les peces excloses i deixar-ne el motiu al seguiment intern, sense barrejar-les amb Knowledge.
