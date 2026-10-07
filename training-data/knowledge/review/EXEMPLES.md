# Exemples de calibratge: preguntes que podrien arribar al xat

Aquests dos exemples serveixen per calibrar intenció, continuïtat i to. Són
mostres editorials, encara no aprovades ni exportables. Les preguntes parteixen
d'un dubte pràctic; no demanen informació d'una fitxa. Cada seguiment reprèn
una cosa que Maia acaba de dir.

## Fer trinxat

**Usuari:** Per fer trinxat, la col i la patata es bullen juntes o per separat?

**Maia:** Es bullen juntes fins que gairebé es desfan. Després es trinxen, es
barregen amb el greix de la cansalada fregida i es dauren a la paella fins que
fan crosta.

**Usuari:** I la cansalada també es barreja amb la col i la patata?

**Maia:** Se'n barreja el greix amb les verdures; la cansalada fregida es posa
per sobre quan se serveix.

**Per què funciona:** és una pregunta de cuina concreta. El seguiment demana
aclarir un pas que apareix a la resposta. Maia explica el procés sense convertir
la resposta en una llista telegràfica.

**Fonts i drets per verificar:** [`El trinxat`](../../../docs/temes/gastronomia/plats/el-trinxat.md) i
[`Viquipèdia en català`](../../../docs/fonts/viquipedia-ca.md), llicència
CC BY-SA 4.0. En exportar, conservar atribució i compartir igual.

## Veure una festa de l'ossa

**Usuari:** Quan es fan les festes de l'ossa que encara es conserven a Andorra?

**Maia:** A Encamp, el ball de l'ossa es representa el dilluns de Carnaval. A
Ordino, l'Última ossa té lloc durant la primera setmana de desembre, coincidint
amb la fira de Nadal.

**Usuari:** La d'Ordino sempre s'ha fet al desembre?

**Maia:** No. Originàriament també es feia per Carnaval. Ordino la va recuperar
el 2017 i, des d'aleshores, se celebra al desembre. La documentació disponible
no explica per què es va fixar aquesta nova data.

**Per què funciona:** la primera pregunta ajuda a entendre quan es poden veure
les dues celebracions vigents. El seguiment sorgeix de la diferència de
calendari entre Ordino i Encamp; la resposta n'explica el canvi conegut i no
atribueix un motiu que no està documentat.

**Fonts i drets per verificar:** [`Les festes de l'ossa`](../../../docs/temes/costums/danses/les-festes-de-lossa.md) i
[`Viquipèdia en català`](../../../docs/fonts/wikipedia-llegendes-andorra.md),
llicència CC BY-SA 4.0. En exportar, conservar atribució i compartir igual.

## Rebuig de patrons

No són preguntes d'entrenament útils:

- «Què explica la secció X de la fitxa Y?» — l'usuari no ha dit que tingui la
  fitxa davant ni quin dubte vol resoldre.
- «Què indica aquesta fila?» — depèn d'una taula absent del xat.
- «Què explica el corpus sobre X?» — demana metadades del nostre procés, no una
  resposta sobre Andorra.
- Una pregunta de quiz com «Quin any es va recuperar?» si no hi ha un motiu
  conversacional per demanar una data aïllada.
- Dos o tres torns que només repeteixen la mateixa dada amb altres paraules.

## Vista de format final

Quan un exemple hagi passat revisió factual, editorial i de drets, el format
d'exportació serà una sola línia JSONL amb els missatges del diàleg. Per exemple:

```json
{"messages":[{"role":"user","content":"Per fer trinxat, la col i la patata es bullen juntes o per separat?"},{"role":"assistant","content":"Es bullen juntes fins que gairebé es desfan. Després es trinxen, es barregen amb el greix de la cansalada fregida i es dauren a la paella fins que fan crosta."},{"role":"user","content":"I la cansalada també es barreja amb la col i la patata?"},{"role":"assistant","content":"Se'n barreja el greix amb les verdures; la cansalada fregida es posa per sobre quan se serveix."}]}
```

L'exportació real només inclou mostres aprovades. Fonts, drets, identificadors i
notes editorials es queden als registres interns.
