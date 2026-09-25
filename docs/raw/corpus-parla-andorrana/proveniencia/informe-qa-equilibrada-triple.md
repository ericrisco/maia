# Comparació de tres descodificacions — mostra equilibrada

La mostra conté **100 clips**. La tercera passada és greedy del model small; cap categoria substitueix l'escolta.

| Categoria | Clips |
|---|---:|
| A-tres-models | 61 |
| B-dos-models | 34 |
| C-un-model | 5 |
| D-cap-model | 0 |

## Casos que requereixen escolta prioritària

- **pa-001 · evidentment** (B-dos-models) · [pa-001__evidentment__1067.69.wav](clips/pa-001__evidentment__1067.69.wav) · small=`evidentment` · base=`en Espanya Mècubuca, evidentment, però no...` · greedy=`i que no es pot fer una altra cosa.`
- **pa-002 · reformeta** (B-dos-models) · [pa-002__reformeta__12.25.wav](clips/pa-002__reformeta__12.25.wav) · small=`reformeta` · base=`Però no que s'hagués fet que s'havia de reformar-te.` · greedy=`per molt que s'hagués fet, el que se'n va dir reformeta,`
- **pa-002 · evidentment** (B-dos-models) · [pa-002__evidentment__205.25.wav](clips/pa-002__evidentment__205.25.wav) · small=`evidentment` · base=`Però evidentment no hi havia d'altra forma.` · greedy=`Providament no hi havia d'altra fórmula.`
- **pa-003 · ensenyança** (B-dos-models) · [pa-003__ensenyan-a__279.69.wav](clips/pa-003__ensenyan-a__279.69.wav) · small=`ensenyança` · base=`que s'integre amb una primera enseñanza de sistemes educatius estrangers.` · greedy=`que s'integre amb una primera ensenyança de sistemes educatius estrangers,  com?`
- **pa-005 · o sigui** (B-dos-models) · [pa-005__o-sigui__373.33.wav](clips/pa-005__o-sigui__373.33.wav) · small=`O sigui` · base=`n'ha de dir un format xar i dues fogaixes de pas, així que hi ha poques bromes.` · greedy=`Un formatxar i dues fogaces de pa.  O sigui que hi ha poques bromes.`
- **pa-012 · perquè** (B-dos-models) · [pa-012__perqu__369.25.wav](clips/pa-012__perqu__369.25.wav) · small=`perquè` · base=`per que la gent és recording d'aquesta setmana.` · greedy=`perquè la gent es recordi d'aquestes eines.`
- **pa-013 · bé** (B-dos-models) · [pa-013__b__196.65.wav](clips/pa-013__b__196.65.wav) · small=`bé` · base=`que em sofre i que la ve per la pell, pel sistema digestiu, i també té altres propietats.` · greedy=`que em sofre i que va bé per la pell, pel sistema digestiu i també té altres propietats.  Propietats que...`
- **pa-013 · és a dir** (B-dos-models) · [pa-013__s-a-dir__579.17.wav](clips/pa-013__s-a-dir__579.17.wav) · small=`És a dir` · base=`és de dir, l'arquitectura de granites dona en un moment de reconversió gradual del nostre país que passa de ser` · greedy=`d'urrana. És a dir, l'arquitectura de granit es dona en un moment de reconversió gradual  del nostre país, que passa de ser...`
- **pa-014 · aviam** (B-dos-models) · [pa-014__aviam__875.45.wav](clips/pa-014__aviam__875.45.wav) · small=`aviam` · base=`d'una cosa, i van dir, escolteu, ho havíem.
 Imaginau-se que les malades apareix.
 Què passa amb el contrapass?
 Estàs deixant el de ballar?` · greedy=`i es pot fer una cosa, i van dir, escuteu, aviam,  imagineu-vos que les merdes apareixen.  Què passa amb el contrapàs? Es deixarà de ballar.`
- **pa-015 · llavors** (B-dos-models) · [pa-015__llavors__197.25.wav](clips/pa-015__llavors__197.25.wav) · small=`llavors` · base=`d'edat i abans a part de tindre a la G3` · greedy=`lletat. I llavors, a part de tindre aquest sis,`
- **pa-016 · bé** (B-dos-models) · [pa-016__b__170.05.wav](clips/pa-016__b__170.05.wav) · small=`bé` · base=`És una disolució, mentre ens encarà amb molta responsabilitat de diòstres,
 és que bon de febre, amb de...` · greedy=`És una disolució, entres encara amb molta més responsabilitat de dir  "estàs bé, hem de fer bé".`
- **pa-019 · llavors** (B-dos-models) · [pa-019__llavors__422.25.wav](clips/pa-019__llavors__422.25.wav) · small=`llavors` · base=`perquè ens donava eines per fer més coses als que podíem fer fins allà.` · greedy=`perquè ens donava eines per poder fer més coses  que podíem fer fins al llavors.`
- **pa-020 · aviam** (B-dos-models) · [pa-020__aviam__252.21.wav](clips/pa-020__aviam__252.21.wav) · small=`aviam` · base=`I jo m'han resultat que clar, jo sóc, aviam, puc ser va futbol.` · greedy=`I a mi em sembla que és el que em sembla.`
- **pa-023 · a nivell** (B-dos-models) · [pa-023__a-nivell__418.57.wav](clips/pa-023__a-nivell__418.57.wav) · small=`a nivell` · base=`i després també aniré de agricultura.` · greedy=`i després també a nivell d'agricultura.`
- **pa-025 · aleshores** (B-dos-models) · [pa-025__aleshores__361.93.wav](clips/pa-025__aleshores__361.93.wav) · small=`aleshores` · base=`I a les hores ens es tornen més primirats.` · greedy=`i aleshores ens tornem més primirats.`
- **pa-029 · a nivell** (B-dos-models) · [pa-029__a-nivell__417.09.wav](clips/pa-029__a-nivell__417.09.wav) · small=`a nivell` · base=`i xarquatres, o que els altres volien als quadren i veig nacional,
 i l'aconseguiria.` · greedy=`i això ha de deixar a quatre,  a algú que els valta els quatre a nivell nacional.`
- **pa-030 · vull dir** (B-dos-models) · [pa-030__vull-dir__842.69.wav](clips/pa-030__vull-dir__842.69.wav) · small=`vull dir` · base=`Bé, vull dir també perquè cal recordar-ho.` · greedy=`i que no hi hagi una altra part de l'independentisme.`
- **pa-031 · tirar endavant** (B-dos-models) · [pa-031__tirar-endavant__146.09.wav](clips/pa-031__tirar-endavant__146.09.wav) · small=`tirar endavant` · base=`de la manera que fos i que s'havia de dir en davant de la manera que fos.` · greedy=`que s'havia de tirar endavant de la manera que fos.`
- **pa-033 · diguem** (B-dos-models) · [pa-033__diguem__49.01.wav](clips/pa-033__diguem__49.01.wav) · small=`diguem` · base=`Doncs normalment es revie amb interès.` · greedy=`normalment es revia amb... amb interès, diguem.`
- **pa-035 · doncs** (B-dos-models) · [pa-035__doncs__195.49.wav](clips/pa-035__doncs__195.49.wav) · small=`doncs` · base=`i jo vaig participar d'un amic, una mica.` · greedy=`I, ara, ja he vingut a participar, doncs, una mica.`
- **pa-037 · bueno** (B-dos-models) · [pa-037__bueno__105.29.wav](clips/pa-037__bueno__105.29.wav) · small=`bueno` · base=`d'acompanyar-se, d'acompanyar-se.` · greedy=`i que s'ha constituït.  Gailbé, existim tothom.  Jo, personalment, he passat tots els altres anys que no he pogut anar.  Però, bueno, aquí està el mateix, he bainat.  I torne bé.  Bona ambient, molt bona ambient.  Molt bona ambient.  Torna a comentar coses del que ha fet passat,  però sobretot...`
- **pa-037 · bé** (B-dos-models) · [pa-037__b__105.29.wav](clips/pa-037__b__105.29.wav) · small=`bé` · base=`d'acompanyar-se, d'acompanyar-se.` · greedy=`i que s'ha constituït.  Gailbé, existim tothom.  Jo, personalment, he passat tots els altres anys que no he pogut anar.  Però, bueno, aquí està el mateix, he bainat.  I torne bé.  Bona ambient, molt bona ambient.  Molt bona ambient.  Torna a comentar coses del que ha fet passat,  però sobretot...`
- **pa-039 · bé** (B-dos-models) · [pa-039__b__27.77.wav](clips/pa-039__b__27.77.wav) · small=`bé` · base=`fins a la prostitució no hi estava.` · greedy=`fins a la prostitució no ja està bé.`
- **pa-042 · perquè** (B-dos-models) · [pa-042__perqu__29.13.wav](clips/pa-042__perqu__29.13.wav) · small=`perquè` · base=`A més que res, perquè tenia els nens petits, crec que...` · greedy=`i que no hi hagi una escola.`
- **pa-045 · clar** (B-dos-models) · [pa-045__clar__399.85.wav](clips/pa-045__clar__399.85.wav) · small=`clar` · base=`No ho he fet, no ho he fet, no ho he fet, no ho he fet, no ho he fet.` · greedy=`amb el qual estava... amb res.  Amb el qual estava bastant clar.  Semblava bastant clar.`
- **pa-046 · és a dir** (C-un-model) · [pa-046__s-a-dir__135.61.wav](clips/pa-046__s-a-dir__135.61.wav) · small=`és a dir` · base=`Som filers, doncs es veiem el dia a dia i hem espanyol.` · greedy=`i que no hi hagi una altra.`
- **pa-049 · llavors** (B-dos-models) · [pa-049__llavors__230.45.wav](clips/pa-049__llavors__230.45.wav) · small=`llavors` · base=`I aquí en Dorra va vindre llabons el delegat de prensa de la casa blanca.
 No sé si va ser arreu de la càrrecament de aquesta càrrec.` · greedy=`i aquí en Dorre va vindre llavors el delegat de premsa de la Casa Blanca.  No sé si va ser arreu realment d'aquesta carta.`
- **pa-049 · a veure** (B-dos-models) · [pa-049__a-veure__244.85.wav](clips/pa-049__a-veure__244.85.wav) · small=`a veure` · base=`I ja no ens ho pot dir.
 Ja no ens ho pot dir.
 Però va anar a tablar a visitar-te amb el meu pare,
 amb el meu pare, els van a veure després o aixec.` · greedy=`i el meu pare es va veure després a la xarxa.`
- **pa-052 · bueno** (B-dos-models) · [pa-052__bueno__41.97.wav](clips/pa-052__bueno__41.97.wav) · small=`bueno` · base=`i heu erro de dins de germans.` · greedy=`I, bueno, tinc certs germans.`
- **pa-053 · perquè** (B-dos-models) · [pa-053__perqu__113.93.wav](clips/pa-053__perqu__113.93.wav) · small=`perquè` · base=`n'hi hagi d'aquí, n'havien guanyat una pel·la perquè volem desprotar la gent.` · greedy=`que no hi hagi una persona que no té cap problema.`
- **pa-056 · aleshores** (B-dos-models) · [pa-056__aleshores__393.13.wav](clips/pa-056__aleshores__393.13.wav) · small=`aleshores` · base=`i a desarres això està tan quadrícolat.` · greedy=`i, aleshores, això està tan quadriculat.`
- **pa-058 · és a dir** (C-un-model) · [pa-058__s-a-dir__74.41.wav](clips/pa-058__s-a-dir__74.41.wav) · small=`És a dir` · base=`que volien ser com un pare.` · greedy=`i que no hi hagi una persona que no hagi tingut un lloc.`
- **pa-061 · o sigui** (C-un-model) · [pa-061__o-sigui__161.05.wav](clips/pa-061__o-sigui__161.05.wav) · small=`O sigui` · base=`Si la primera activitat dels germans, despionés, peri...` · greedy=`i que no hi hagi una altra gent que no té cap problema.`
- **pa-061 · llavors** (B-dos-models) · [pa-061__llavors__380.77.wav](clips/pa-061__llavors__380.77.wav) · small=`llavors` · base=`-Exactament.
 -Ella abans comença a tornar a agradar-s'hi.` · greedy=`-Exacte.  -Bueno, llavors comença tot una agredació.`
- **pa-063 · o sigui** (B-dos-models) · [pa-063__o-sigui__826.09.wav](clips/pa-063__o-sigui__826.09.wav) · small=`O sigui` · base=`O sigui que vam estar a la primera paix amb comets.` · greedy=`i és modern.`
- **pa-064 · o sigui** (C-un-model) · [pa-064__o-sigui__36.73.wav](clips/pa-064__o-sigui__36.73.wav) · small=`o sigui` · base=`A més, les seves gràcies a les eleccions d'aquesta vegada.` · greedy=`i el que ha de fer és fer-ho.`
- **pa-064 · a veure** (B-dos-models) · [pa-064__a-veure__587.61.wav](clips/pa-064__a-veure__587.61.wav) · small=`a veure` · base=`-El set de nata veure amb els anys.` · greedy=`No s'ha tornat a veure amb els anys.`
- **pa-065 · bé** (B-dos-models) · [pa-065__b__138.57.wav](clips/pa-065__b__138.57.wav) · small=`bé` · base=`M'agrada molt bé, el Serre Benopardis va marxar el paradis.` · greedy=`i el que va passar és que el que va passar és que el que va passar  va ser que el que va passar és que el que va passar és que el que va passar`
- **pa-066 · llavors** (C-un-model) · [pa-066__llavors__16.21.wav](clips/pa-066__llavors__16.21.wav) · small=`llavors` · base=`que es poden fer a l'estudio de la ciutadania.` · greedy=`i que la gent no s'ha de fer.`
