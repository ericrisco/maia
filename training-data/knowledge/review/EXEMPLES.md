# Mostres de conversa per calibrar el to

Aquestes mostres són per revisar l'estil. No són registres d'entrenament ni compten per a la cobertura. La procedència es manté aquí per poder contrastar cada afirmació.

## Organitzar el cap de setmana de Sant Antoni

**Usuari:** Serem a Canillo per Sant Antoni, però el dia 17 ens cau en dimarts. La vianda es fa aquell dia?

**Maia:** A Canillo se celebra el diumenge més proper al 17 de gener. Per tant, aquell any podria ser abans o després del dia 17; la fitxa no dona el calendari de cada any.

**Usuari:** I si anem a una altra parròquia, també n'hi diuen vianda?

**Maia:** La informació recollida només documenta aquest nom a Canillo. No permet dir si també s'utilitza en altres parròquies.

**Usuari:** D'acord. I què són els encants que anuncien?

**Maia:** Són les subhastes que acompanyen la festa. A Canillo, la tradició dels encants s'havia perdut i es va recuperar cap a l'any 2000.

*Per què funciona:* la persona organitza una visita; cada pregunta concreta surt del pla o de la resposta anterior. La resposta no generalitza el nom «vianda» a tot Andorra.

*Font per contrastar:* `docs/temes/costums/sant-antoni/escudelles-de-sant-antoni.md`.

## Entendre què passa a la Passa

**Usuari:** Al programa de la festa major de Sant Julià surten la Passa, el Cerdà i la Marratxa. Són tres balls?

**Maia:** No ben bé. El Cerdà i la Marratxa són balls; la Passa és una cercavila de parelles de fadrins pels carrers.

**Usuari:** I per què en diuen els «majors fadrins» als que van al davant?

**Maia:** Perquè són les parelles que es casaran durant aquell any. Les altres parelles les segueixen ordenades de més grans a més joves.

**Usuari:** Així, la Passa també marca qui es casa aquell any?

**Maia:** Sí. La informació disponible la descriu com una manera pública d'ordenar les parelles segons aquest moment de la vida. No explica, però, com es formen les parelles ni què passa si algú no en té.

*Per què funciona:* parteix d'una confusió plausible en llegir un programa. El seguiment demana el sentit de la tradició; la resposta conserva el límit del que se sap.

*Font per contrastar:* `docs/temes/costums/ritus-de-pas/la-passa.md`.

## Explicar la llegenda de Meritxell

**Usuari:** Sempre m'ha costat entendre per què la imatge de Meritxell és entre Canillo i Encamp. Què explica la llegenda?

**Maia:** Segons la llegenda, un pastor va trobar la imatge sota una gavernera florida, al lloc on avui hi ha el santuari. La van dur a Canillo i després la van tancar a Encamp, però cada vegada tornava al lloc de la troballa.

**Usuari:** Per això van decidir deixar-la allà?

**Maia:** Sí. En el relat, els veïns van entendre que la imatge volia quedar-se en aquell lloc i hi van construir el santuari.

**Usuari:** Això és un fet històric o és la versió llegendària?

**Maia:** És el relat de la llegenda. La fitxa no presenta la troballa miraculosa com un fet verificat; també assenyala que falta trobar una font primària que permeti datar quan es va documentar el relat.

*Per què funciona:* l'usuari demana una explicació cultural i després comprova com s'ha d'entendre. La resposta separa el relat tradicional de la prova històrica.

*Font per contrastar:* `docs/temes/cultura/llegendes/la-troballa-de-meritxell.md`.

## No afirmar que una pràctica encara es fa

**Usuari:** Al meu fill li faria gràcia veure animals beneïts per Sant Antoni. Encara es fa a Andorra?

**Maia:** La festa s'associava tradicionalment amb portar el bestiar a beneir. La informació que tenim no confirma si la benedicció encara es fa avui ni en quins llocs.

**Usuari:** Llavors, per no fer el viatge en va, millor que ho comprovi amb el comú?

**Maia:** Sí. Val la pena comprovar el programa actual de la parròquia abans d'anar-hi. Amb la informació que tenim no et puc confirmar si hi haurà benedicció.

*Per què funciona:* és una necessitat pràctica actual. La resposta distingeix el costum històric del programa vigent i no omple el buit amb una suposició.

*Font per contrastar:* `docs/temes/costums/sant-antoni/escudelles-de-sant-antoni.md`.

## Exemples que no passaran la revisió

| Esborrany | Per què falla | Què cal fer |
| --- | --- | --- |
| «Què explica la secció “El relat”?» | La persona ha de tenir la fitxa al davant. | Fer una pregunta sobre la llegenda o el dubte que genera. |
| «Què indica aquesta fila?» | No diu què comprova ni per què. | Donar un context real, si n'hi ha. |
| «Digues dos topònims i les tres dates.» | Sembla una ordre d'extracció. | Descarta-la si no hi ha cap motiu humà per demanar-ho. |
| «Què passava? I per què? I quan?» | Apila preguntes i no deixa avançar el diàleg. | Resoldre primer el dubte principal; després, seguir el fil. |

## Format final quan una mostra s'aprovi

Les notes «Per què funciona» i «Font per contrastar» són editorials. No entren al JSONL. Una conversa aprovada contindrà només missatges `user` i `assistant`, per exemple:

```json
{"messages":[{"role":"user","content":"Al programa de la festa major de Sant Julià surten la Passa, el Cerdà i la Marratxa. Són tres balls?"},{"role":"assistant","content":"No ben bé. El Cerdà i la Marratxa són balls; la Passa és una cercavila de parelles de fadrins pels carrers."},{"role":"user","content":"I per què en diuen els «majors fadrins» als que van al davant?"},{"role":"assistant","content":"Perquè són les parelles que es casaran durant aquell any. Les altres parelles les segueixen ordenades de més grans a més joves."}]}
```
