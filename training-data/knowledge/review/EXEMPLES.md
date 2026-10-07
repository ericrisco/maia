# Exemples de calibratge: dubtes reals, respostes completes

Aquests són exemples editorials per decidir com han de sonar les converses.
No són registres aprovats ni s'exporten automàticament. Abans d'aprovar-los com
a dades, encara cal verificar la procedència i els drets de les fonts citades.

## Dues festes de l'ossa, dos calendaris

**Usuari:** Si vull veure una festa de l'ossa, he d'anar-hi per Carnaval?

**Maia:** Depèn d'on. A Encamp, el ball de l'ossa es representa el dilluns de
Carnaval. A Ordino, l'Última ossa es fa durant la primera setmana de desembre,
a la fira de Nadal.

**Usuari:** Ah, la d'Ordino també es feia al desembre abans?

**Maia:** No. Originalment també es feia per Carnaval. El corpus explica que es
va reprendre el 2017 i que des d'aleshores se celebra al desembre, però no diu
per què es va triar aquest canvi de data.

**Per què funciona:** la pregunta inicial serveix per orientar un pla concret.
El seguiment sorgeix de la diferència de calendari i comprova si és antiga. La
resposta dona el que se sap i marca el límit sense inventar un motiu.

**Fonts per revisar:** [`les-festes-de-lossa.md`](../../../docs/temes/costums/danses/les-festes-de-lossa.md), apartats «La cronologia» i «Les dues que queden».

## Un plat que no és exclusiu d'un país

**Usuari:** El trinxat és un plat típicament andorrà?

**Maia:** També es menja a Andorra, però no és exclusivament andorrà. És un
plat pirinenc que també es troba a la Cerdanya, l'Alt Urgell i el Berguedà.

**Usuari:** I la col i la patata són la recepta tradicional d'aquí?

**Maia:** La fitxa descriu el trinxat amb col i patata bullides, aixafades i
daurades amb el greix de la cansalada. Però no concreta si hi ha una variant
pròpia d'Andorra; aquest detall no consta al corpus.

**Usuari:** Per què precisament aquests ingredients?

**Maia:** La fitxa ho relaciona amb els hiverns del Pirineu: la col podia
aguantar al camp i la patata es guardava al celler quan hi havia pocs aliments
disponibles. També situa la primera referència escrita al segle XV.

**Per què funciona:** la conversa corregeix amb tacte una atribució massa
exclusiva, no presenta una recepta general com si fos una variant andorrana i
respon la curiositat que obre l'explicació dels ingredients.

**Fonts per revisar:** [`el-trinxat.md`](../../../docs/temes/gastronomia/plats/el-trinxat.md), apartats «Com es fa», «Per què existeix» i «El que falta».

## Com convertir una pregunta de fitxa en una pregunta humana

**No:** «Què explica la secció “El relat” de la fitxa “La troballa de Meritxell”?»

**Per què no:** només té sentit per a qui coneix la fitxa i el seu índex. No
explica què vol entendre la persona.

**Millor punt de partida:** identifica quin dubte resol aquell relat. Per
exemple, si la font documenta què va passar després de trobar la imatge, es
podria preguntar «Què va passar després que la trobessin?». Abans d'escriure la
resposta, cal comprovar que el relat sosté aquesta formulació i que no s'hi
afegeixen detalls d'altres versions.

**No:** «Què indica aquesta fila?»

**Per què no:** la pregunta assenyala una fila que no existeix dins la conversa
i no diu quina comparació o conclusió necessita l'usuari.

**Millor punt de partida:** si les dades mostren dues sèries diferents, formula
el dubte que provoquen («Per què una sèrie puja si l'altra baixa?») i explica
què mesura cadascuna. No converteixis els valors en una llista sense context.

## Senyals per descartar o reescriure

- «Què explica la secció...» — pregunta sobre l'índex de la font.
- «I què més?» — no concreta cap necessitat ni reprèn un detall.
- «Tres coses que el corpus registra per separat:» — fragment, no resposta.
- «Això prova que...?» — només funciona si la resposta pot explicar què proven i què no proven les dades.
- Una llista de dates, xifres o noms sense una frase que n'expliqui la rellevància.
- Una pregunta inicial i un seguiment que podrien intercanviar-se amb qualsevol altra conversa.
- Una resposta que afegeix la causa més plausible quan la font no la documenta.

## Com ha de quedar l'exportació

Quan una conversa s'hagi revisat, aprovat i assignat a un split, l'exportació
contindrà només missatges, per exemple:

```json
{"messages":[{"role":"user","content":"El trinxat és un plat típicament andorrà?"},{"role":"assistant","content":"També es menja a Andorra, però no és exclusivament andorrà. És un plat pirinenc que també es troba a la Cerdanya, l'Alt Urgell i el Berguedà."},{"role":"user","content":"I la col i la patata són la recepta tradicional d'aquí?"},{"role":"assistant","content":"La fitxa descriu el trinxat amb col i patata bullides, aixafades i daurades amb el greix de la cansalada. Però no concreta si hi ha una variant pròpia d'Andorra; aquest detall no consta al corpus."}]}
```

Les fonts, els drets, la puntuació i l'explicació editorial es guarden fora de
`output/`.
