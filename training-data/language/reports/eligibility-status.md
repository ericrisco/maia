# Estat d'elegibilitat de Maia Language

Auditoria del `2026-10-08` de `docs/parla/`. Aquest informe és un inventari de
revisió, **no una aprovació de fragments ni un dataset d'entrenament**.

## Resum

- Hi ha **45 fitxes Markdown**: cinc índexs i **40 fitxes de peces o registres**.
- **38 fitxes de peça** tenen `veu: originaria`, `epoca: contemporania` i
  `apte_llengua: true`. Aquests camps són filtres inicials; no demostren per si
  sols que la mostra sigui adequada.
- D'aquestes 38, **27** són entrevistes del Consell Constituent i **11** són
  càpsules d'AR+I.
- Les **27 entrevistes del Consell** tenen consentiment documentat, però la
  font declara la llicència estàndard de YouTube i la redistribució continua
  pendent.
- A les **11 càpsules candidates d'AR+I**, la llicència CC BY està verificada
  peça a peça per a les #34, #56 i #57. Les altres vuit encara no tenen aquesta
  verificació individual registrada. Les transcripcions de les peces candidates
  encara no estan aprovades; la #57 també està marcada com a possiblement llegida.
- Les dues fitxes restants, *Alberg és un sinònim de casa* i *Qui apareix a les
  llistes del Consell durant el procés constituent*, són compilacions i tenen
  `apte_llengua: false`.

**Fragments aprovats per a l'export: 0.** Cap fitxa candidata no té alhora
redistribució resolta, fidelitat transcripcional revisada directament i un
fragment seleccionat sense incerteses que alterin la veu.

## Candidats i motius pendents

| Grup | Fitxes | Estat actual |
| --- | --- | --- |
| Entrevistes del Consell Constituent | 27 testimonis | Veu i període marcats com a elegibles; consentiment documentat; redistribució pendent; transcripcions marcades com a no verificades o incertes. L'entrevistador està editat fora, així que no s'han de fabricar preguntes per convertir-les en diàlegs. |
| Càpsules d'AR+I amb metadades elegibles | 11 fitxes | Verificar llicència individual, perfil del parlant, lectura de guió i cada fragment contra l'àudio. Les #34, #56 i #57 tenen CC BY registrada; això no valida la transcripció. |
| Compilacions | 2 fitxes | Excloses de Language per `apte_llengua: false`. |

La sèrie d'AR+I té exposicions preparades, no converses espontànies. Una
intervenció monologada no es transforma en intercanvi amb una pregunta
inventada. Només es podrà crear un exemple de conversa si hi ha torns humans
reals i recuperables; altrament, el material queda fora d'aquest format de
fine-tuning.

## Revisió de la càpsula #34

La transcripció marcada continua identificant paraules incertes amb `[?...]`.
El contrast de Whisper small i Whisper large-v3-turbo per al tram inicial
coincideix en part, però el registre de revisió diu explícitament
`listening_required`; dues sortides automàtiques no equivalen a una escolta.

La fitxa de la font registra aquest SHA-256 per a l'àudio:

```text
627f05924e9b2e07ac15ec7533c3267606ef2ad81f3858c0abc4d3111d122ee2
```

El fitxer local actual `docs/raw/parla/ari-capsula-34/source-audio.wav` dona:

```text
ecd635657c9434a956e7d4080e4967aa5ee1d5287b3d4193009d9a9a7033a09d
```

Els hashes no coincideixen. Cal aclarir si el fitxer local és una transcodificació
equivalent o una altra còpia i actualitzar-ne la procedència. Fins aleshores no
s'aprova cap fragment de la #34.

## Condicions per aprovar un fragment

1. Identificar la peça, la persona parlant i la llicència de reutilització
   aplicable a aquella peça concreta.
2. Escoltar l'àudio font i comprovar cada paraula del fragment; conservar les
   formes pronunciades i apartar els trams que no es puguin resoldre.
3. Excloure lectura de guió i contingut que no sigui una mostra adequada de
   parla contemporània andorrana.
4. No inventar preguntes, respostes ni torns. Si la peça no conté una conversa
   humana real, no generar-ne un diàleg artificial.
5. Registrar la procedència i les decisions de cada fragment abans d'exportar.

Quan una condició no es compleix, la peça queda pendent o exclosa amb el motiu
registrat. Els indicadors de cobertura no poden convertir material pendent en
material entrenable.
