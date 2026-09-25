# Informe del contraste small/base de la mostra equilibrada

La mostra conté 100 clips de 63 parlants i 20 formes candidates. Es conserva una
segona descodificació independent amb `ggml-base.bin` per comprovar si el text
small es manté en el mateix fragment.

## Resultat automàtic

- 70 clips tenen coincidència textual de la forma en small i base.
- 30 clips només coincideixen textualment en small.
- Les 30 divergències afecten 26 parlants i 17 formes; no són descartes de la
  forma ni decisions sobre la pronunciació.
- `qa-equilibrada-consens.tsv` conserva els dos textos i la categoria de cada
  clip; els JSON i TXT base són a `qa-equilibrada-base/`.

## Divergències per forma

- **llavors**: 5 clips
- **bé**: 4 clips
- **o sigui**: 3 clips
- **és a dir**: 3 clips
- **a nivell**: 2 clips
- **aleshores**: 2 clips
- **bueno**: 2 clips
- **a veure**: 1 clip
- **aviam**: 1 clip
- **clar**: 1 clip
- **diguem**: 1 clip
- **doncs**: 1 clip
- **ensenyança**: 1 clip
- **perquè**: 1 clip
- **reformeta**: 1 clip
- **tirar endavant**: 1 clip

## Casos

- **pa-002 · reformeta** · [pa-002__reformeta__12.25.wav](clips/pa-002__reformeta__12.25.wav) · small: `reformeta` · base: `Però no que s'hagués fet que s'havia de reformar-te.`
- **pa-003 · ensenyança** · [pa-003__ensenyan-a__279.69.wav](clips/pa-003__ensenyan-a__279.69.wav) · small: `ensenyança` · base: `que s'integre amb una primera enseñanza de sistemes educatius estrangers.`
- **pa-005 · o sigui** · [pa-005__o-sigui__373.33.wav](clips/pa-005__o-sigui__373.33.wav) · small: `O sigui` · base: `n'ha de dir un format xar i dues fogaixes de pas, així que hi ha poques bromes.`
- **pa-012 · perquè** · [pa-012__perqu__369.25.wav](clips/pa-012__perqu__369.25.wav) · small: `perquè` · base: `per que la gent és recording d'aquesta setmana.`
- **pa-013 · bé** · [pa-013__b__196.65.wav](clips/pa-013__b__196.65.wav) · small: `bé` · base: `que em sofre i que la ve per la pell, pel sistema digestiu, i també té altres propietats.`
- **pa-013 · és a dir** · [pa-013__s-a-dir__579.17.wav](clips/pa-013__s-a-dir__579.17.wav) · small: `És a dir` · base: `és de dir, l'arquitectura de granites dona en un moment de reconversió gradual del nostre país que passa de ser`
- **pa-014 · aviam** · [pa-014__aviam__875.45.wav](clips/pa-014__aviam__875.45.wav) · small: `aviam` · base: `d'una cosa, i van dir, escolteu, ho havíem.
 Imaginau-se que les malades apareix.
 Què passa amb el contrapass?
 Estàs deixant el de ballar?`
- **pa-015 · llavors** · [pa-015__llavors__197.25.wav](clips/pa-015__llavors__197.25.wav) · small: `llavors` · base: `d'edat i abans a part de tindre a la G3`
- **pa-016 · bé** · [pa-016__b__170.05.wav](clips/pa-016__b__170.05.wav) · small: `bé` · base: `És una disolució, mentre ens encarà amb molta responsabilitat de diòstres,
 és que bon de febre, amb de...`
- **pa-019 · llavors** · [pa-019__llavors__422.25.wav](clips/pa-019__llavors__422.25.wav) · small: `llavors` · base: `perquè ens donava eines per fer més coses als que podíem fer fins allà.`
- **pa-023 · a nivell** · [pa-023__a-nivell__418.57.wav](clips/pa-023__a-nivell__418.57.wav) · small: `a nivell` · base: `i després també aniré de agricultura.`
- **pa-025 · aleshores** · [pa-025__aleshores__361.93.wav](clips/pa-025__aleshores__361.93.wav) · small: `aleshores` · base: `I a les hores ens es tornen més primirats.`
- **pa-029 · a nivell** · [pa-029__a-nivell__417.09.wav](clips/pa-029__a-nivell__417.09.wav) · small: `a nivell` · base: `i xarquatres, o que els altres volien als quadren i veig nacional,
 i l'aconseguiria.`
- **pa-031 · tirar endavant** · [pa-031__tirar-endavant__146.09.wav](clips/pa-031__tirar-endavant__146.09.wav) · small: `tirar endavant` · base: `de la manera que fos i que s'havia de dir en davant de la manera que fos.`
- **pa-033 · diguem** · [pa-033__diguem__49.01.wav](clips/pa-033__diguem__49.01.wav) · small: `diguem` · base: `Doncs normalment es revie amb interès.`
- **pa-035 · doncs** · [pa-035__doncs__195.49.wav](clips/pa-035__doncs__195.49.wav) · small: `doncs` · base: `i jo vaig participar d'un amic, una mica.`
- **pa-037 · bueno** · [pa-037__bueno__105.29.wav](clips/pa-037__bueno__105.29.wav) · small: `bueno` · base: `d'acompanyar-se, d'acompanyar-se.`
- **pa-037 · bé** · [pa-037__b__105.29.wav](clips/pa-037__b__105.29.wav) · small: `bé` · base: `d'acompanyar-se, d'acompanyar-se.`
- **pa-039 · bé** · [pa-039__b__27.77.wav](clips/pa-039__b__27.77.wav) · small: `bé` · base: `fins a la prostitució no hi estava.`
- **pa-045 · clar** · [pa-045__clar__399.85.wav](clips/pa-045__clar__399.85.wav) · small: `clar` · base: `No ho he fet, no ho he fet, no ho he fet, no ho he fet, no ho he fet.`
- **pa-046 · és a dir** · [pa-046__s-a-dir__135.61.wav](clips/pa-046__s-a-dir__135.61.wav) · small: `és a dir` · base: `Som filers, doncs es veiem el dia a dia i hem espanyol.`
- **pa-049 · llavors** · [pa-049__llavors__230.45.wav](clips/pa-049__llavors__230.45.wav) · small: `llavors` · base: `I aquí en Dorra va vindre llabons el delegat de prensa de la casa blanca.
 No sé si va ser arreu de la càrrecament de aquesta càrrec.`
- **pa-052 · bueno** · [pa-052__bueno__41.97.wav](clips/pa-052__bueno__41.97.wav) · small: `bueno` · base: `i heu erro de dins de germans.`
- **pa-056 · aleshores** · [pa-056__aleshores__393.13.wav](clips/pa-056__aleshores__393.13.wav) · small: `aleshores` · base: `i a desarres això està tan quadrícolat.`
- **pa-058 · és a dir** · [pa-058__s-a-dir__74.41.wav](clips/pa-058__s-a-dir__74.41.wav) · small: `És a dir` · base: `que volien ser com un pare.`
- **pa-061 · o sigui** · [pa-061__o-sigui__161.05.wav](clips/pa-061__o-sigui__161.05.wav) · small: `O sigui` · base: `Si la primera activitat dels germans, despionés, peri...`
- **pa-061 · llavors** · [pa-061__llavors__380.77.wav](clips/pa-061__llavors__380.77.wav) · small: `llavors` · base: `-Exactament.
 -Ella abans comença a tornar a agradar-s'hi.`
- **pa-064 · o sigui** · [pa-064__o-sigui__36.73.wav](clips/pa-064__o-sigui__36.73.wav) · small: `o sigui` · base: `A més, les seves gràcies a les eleccions d'aquesta vegada.`
- **pa-064 · a veure** · [pa-064__a-veure__587.61.wav](clips/pa-064__a-veure__587.61.wav) · small: `a veure` · base: `-El set de nata veure amb els anys.`
- **pa-066 · llavors** · [pa-066__llavors__16.21.wav](clips/pa-066__llavors__16.21.wav) · small: `llavors` · base: `que es poden fer a l'estudio de la ciutadania.`

## Buit registrat

La coincidència textual entre dos models no confirma que la forma es pronunciï amb una realització andorrana. Cal escoltar cada clip i consignar una decisió, la variant real i els trets fonètics o prosòdics observats.
