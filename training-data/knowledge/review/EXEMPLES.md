# Exemples per calibrar converses

Aquestes mostres fixen el to i el tipus de seguiment que busquem. Són exemples
editorials, no registres aprovats ni exportables. Abans d'incorporar-los al
dataset, cal comprovar-ne la procedència i els drets al registre corresponent.

## Una festa de l'ossa que no és per Carnaval

**Usuari:** Em pensava que les festes de l'ossa eren totes per Carnaval. N'hi ha
alguna que es faci en una altra època?

**Maia:** Sí. A Ordino, l'Última ossa es representa durant la primera setmana de
desembre, coincidint amb la fira de Nadal. A Encamp, en canvi, el ball de
l'ossa es fa el dilluns de Carnaval.

**Usuari:** Ah, la d'Ordino ja es feia al desembre de sempre?

**Maia:** No. Abans també es feia per Carnaval. Es va recuperar el 2017 i des
d'aleshores se celebra al desembre; la documentació no explica per què es va
canviar la data.

**Per què funciona:** comença per una impressió que algú podria tenir i la
comprova. El seguiment reprèn la diferència de calendari i pregunta per la seva
història. La resposta no inventa el motiu del canvi.

**Fonts per revisar:** [`les-festes-de-lossa.md`](../../../docs/temes/costums/danses/les-festes-de-lossa.md).

## El trinxat és andorrà o pirinenc?

**Usuari:** El trinxat és un plat d'Andorra o es menja també a fora?

**Maia:** També es menja a fora. És un plat pirinenc que es troba, entre altres
llocs, a Andorra, la Cerdanya, l'Alt Urgell i el Berguedà.

**Usuari:** I què porta, més o menys?

**Maia:** Es fa amb col i patata bullides i aixafades, que es barregen amb el
greix de la cansalada i es dauren a la paella. La fitxa no concreta si a
Andorra hi ha una variant pròpia.

**Usuari:** Doncs si demano trinxat aquí, puc esperar que sigui diferent del de
la Cerdanya?

**Maia:** No ho podem donar per fet. El corpus descriu la preparació general,
però no documenta cap diferència entre una versió andorrana i una de cerdana.

**Per què funciona:** la conversa va de l'origen del plat a què hi porta i
després a una conseqüència pràctica. Maia no inventa una «variant andorrana»
perquè la pregunta la suggereixi.

**Fonts per revisar:** [`el-trinxat.md`](../../../docs/temes/gastronomia/plats/el-trinxat.md).

## Com pot baixar i pujar alhora la població d'Encamp?

**Usuari:** He vist que Encamp perd població en una estadística i en guanya en
una altra. Com pot ser?

**Maia:** Perquè no compten exactament el mateix. El juliol del 2026, la
població registrada d'Encamp havia baixat un 4,7% respecte d'un any abans,
mentre que l'estimada havia pujat un 2,2%. La primera surt del cens comunal;
la segona calcula la població resident encreuant-lo amb altres registres.

**Usuari:** Llavors la baixada del cens no vol dir que tanta gent hagi marxat?

**Maia:** No ho podem saber només amb aquesta dada. Estadística adverteix que
les variacions del registre també poden reflectir depuracions administratives,
però no quantifica quina part de la baixada d'Encamp ve d'això.

**Per què funciona:** la pregunta surt d'una contradicció aparent entre dues
dades concretes. El seguiment prova una interpretació possible; la resposta
marca el límit que la font dona per a Encamp.

**Fonts per revisar:** [`dues-maneres-de-comptar-la-poblacio.md`](../../../docs/temes/societat/demografia/dues-maneres-de-comptar-la-poblacio.md) i [`estadistica-ad.md`](../../../docs/fonts/estadistica-ad.md).

## Contramodel: pregunta i resposta que descartem

**No:** «Què explica la secció “El relat” de la fitxa “La troballa de
Meritxell”?»

**Per què no:** depèn d'un document que l'usuari no ha esmentat. No diu quin
dubte vol resoldre.

**Tampoc:** «Tres coses que el corpus registra per separat:»

**Per què no:** és un fragment sense resposta directa. Una bona resposta ha de
dir què són aquestes coses i per què contesten la pregunta.

## Format d'entrenament quan s'aprovi una mostra

```json
{"messages":[{"role":"user","content":"Em pensava que les festes de l'ossa eren totes per Carnaval. N'hi ha alguna que es faci en una altra època?"},{"role":"assistant","content":"Sí. A Ordino, l'Última ossa es representa durant la primera setmana de desembre, coincidint amb la fira de Nadal. A Encamp, en canvi, el ball de l'ossa es fa el dilluns de Carnaval."},{"role":"user","content":"Ah, la d'Ordino ja es feia al desembre de sempre?"},{"role":"assistant","content":"No. Abans també es feia per Carnaval. Es va recuperar el 2017 i des d'aleshores se celebra al desembre; la documentació no explica per què es va canviar la data."}]}
```

El JSONL final només conté `messages`. Identificadors, fonts, drets i decisions
editorials queden als fitxers interns de revisió.
