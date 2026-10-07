# Exemples de calibratge de Maia Knowledge

Aquests exemples mostren el nivell de naturalitat que volem. Parteixen d'un
dubte recognoscible i tenen seguiments que neixen de la resposta anterior.
Són exemples editorials, no registres aprovats ni part de l'output.

## Una contradicció aparent que no permet deduir-ne la causa

**Usuari:** He vist que Encamp baixa un 4,7% en una estadística de població,
però puja un 2,2% en una altra. Quina de les dues és la bona?

**Maia:** Totes dues poden ser correctes: mesuren coses diferents. La població
registrada compta les persones inscrites als censos comunals; l'estimada
combina aquests censos amb altres registres per calcular quanta gent resideix
al país. Les dades són del juliol del 2026 comparat amb el juliol del 2025.

**Usuari:** Aleshores, podem dir que la gent ha marxat d'Encamp?

**Maia:** No només amb aquestes xifres. El Departament diu que els canvis del
registre també poden reflectir depuracions administratives, però no quantifica
quina part de la baixada d'Encamp ve d'això. La sèrie estimada, a més, puja.

**Per què funciona:** l'usuari intenta resoldre una discrepància i després
comprova una interpretació possible. La segona resposta marca el límit de les
dades, en lloc d'inventar una causa.

**Fonts per revisar:**
[`dues-maneres-de-comptar-la-poblacio.md`](../../../docs/temes/societat/demografia/dues-maneres-de-comptar-la-poblacio.md)
— resum i apartat «Què permet dir una baixada».

## Una tradició que canvia de data

**Usuari:** Em pensava que les festes de l'ossa eren de Carnaval. Per què la
d'Ordino es fa al desembre?

**Maia:** Abans es feia per Carnaval, com en altres parròquies. L'Última ossa
d'Ordino es representa ara durant la primera setmana de desembre, a la fira de
Nadal.

**Usuari:** Des de quan la fan en aquella data?

**Maia:** El corpus situa la represa del 2017 al desembre, però no explica amb
més detall per què es va triar aquest canvi de calendari.

**Per què funciona:** la primera resposta resol la confusió entre la data
històrica i l'actual. El seguiment demana un detall concret; la resposta no
atribueix al canvi un motiu que la font no dona.

**Fonts per revisar:**
[`les-festes-de-lossa.md`](../../../docs/temes/costums/danses/les-festes-de-lossa.md)
— «La cronologia» i «Les dues que queden».

## Una atribució nacional que necessita matís

**Usuari:** El trinxat és un plat andorrà?

**Maia:** També es menja a Andorra, però no és exclusivament andorrà. És un plat
pirinenc, propi també de la Cerdanya, l'Alt Urgell i el Berguedà.

**Usuari:** I per què es feia tant a l'hivern?

**Maia:** La fitxa ho relaciona amb els aliments que es conservaven durant
l'hivern: col, que podia aguantar al camp, i patata guardada al celler. Es
bullien, es trinxaven i es dauraven a la paella amb el greix de la cansalada.

**Per què funciona:** la pregunta posa a prova una idea habitual —que tot plat
associat amb un país n'és exclusiu— i el seguiment surt naturalment de
l'explicació sobre l'origen del plat.

**Fonts per revisar:**
[`el-trinxat.md`](../../../docs/temes/gastronomia/plats/el-trinxat.md)
— «Per què existeix» i «On es menja».

## Exemples que cal rebutjar

- «Què explica la secció “La cronologia”?» — depèn de l'estructura editorial.
- «I què més?» — no concreta què vol saber ni reprèn cap punt.
- «Quines són totes les dates de la fitxa?» — és una ordre d'extracció, no un
  dubte conversacional.
- «Llavors ja sé per què la festa es va passar al desembre: per atreure turistes.»
  — introdueix una causa que la font no documenta.

## Format de sortida

Quan els exemples hagin passat la revisió, la conversa es desa en una sola
línia JSONL i només conserva els missatges. Les explicacions editorials i les
fonts d'aquí serveixen per revisar; no s'exporten a l'entrenament.
