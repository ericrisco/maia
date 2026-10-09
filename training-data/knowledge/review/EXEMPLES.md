# Guia per a converses de Maia Knowledge

## Comença per la persona

Escriu primer, només per a tu, què intenta resoldre la persona. Exemples: entendre si una norma canviava segons qui demandava, saber què podia fer el propietari d'una finca, o entendre per què un lloc té una història concreta.

Després redacta la pregunta com la diria algú que no ha vist el corpus. Dona el context que calgui, però no parlis de fitxes, seccions, taules, gràfics, files ni fragments. No copiïs l'encapçalament de la font com si fos una consulta.

## Mantén el fil

La primera resposta ha de contestar la pregunta. El seguiment ha de sortir d'allò que acaba de sentir la persona i demanar una cosa nova. Mantén referents clars: si el segon torn diu «això», ha de quedar clar a què es refereix.

No afegeixis torns per complir una quota. Si el corpus no permet un seguiment natural, busca un altre angle o no facis servir aquella unitat com a conversa. La naturalitat i la correcció valen més que la llargada.

## Escriu respostes completes

- Comença per la resposta, no per una introducció sobre la font.
- Fes servir frases completes i explica els termes locals.
- Afegeix només els detalls útils per entendre la resposta.
- No transformis interpretacions en fets ni completis buits amb intuïcions.
- Si les fonts discrepen, explica què sosté cada versió i què queda sense resoldre.
- Si una dada no consta, digues-ho amb claredat.

## Exemples de redacció

**En lloc de:** «Què explica la secció “La regla de competència: depèn de qui és demandat”?»

**Pregunta humana:** «Si un comú em reclamava una cosa, m'havia de jutjar el mateix tribunal que si jo el reclamava a ell?»

La primera pregunta demana una resposta sobre un dubte jurídic. La segona demana que s'extregui un fragment.

**En lloc de:** «Què indica aquesta fila del gràfic?»

**Pregunta humana, si el dubte és sobre les dades:** «Aquestes xifres semblen contradir el text. Quina dada és més fiable i què no es pot assegurar?»

Si les fonts no permeten decidir quina és correcta, la resposta ho ha de dir. No s'ha d'inventar una reconciliació.

## Reescriu els casos que semblen una cerca al corpus

No acceptis preguntes sobre una secció, una fila o un gràfic com a punt de partida. Tampoc acceptis respostes que siguin un títol, una etiqueta, un sintagma sense verb o un fragment copiat. Converteix el tema en un dubte que una persona podria tenir i redacta una resposta que el resolgui.

| Evita | Pregunta humana i resposta completa |
|---|---|
| «Què explica la secció sobre la regla de competència?» → «Apel·lació al Consell General.» | **Usuari:** «Si un particular demandava un comú, el jutjaven al mateix lloc que si el comú el demandava a ell?» **Assistent:** «No. En la regla històrica que recull Brutails, si el particular demandava el comú, el cas anava a la jurisdicció política; si el comú demandava el particular, anava als tribunals ordinaris.» **Seguiment:** «I si el conflicte era amb un quart?» **Resposta:** «El consell de parròquia el jutjava primer i la decisió es podia apel·lar al Consell General.» |
| «Què explica el vocabulari que ho ordena?» → «I dos topònims que en surten:» | **Usuari:** «Com podia ser comunal un camp que algú havia conreat durant anys?» **Assistent:** «En la sentència de 1790 que recull la fitxa, el conreu no impedia que el terreny es considerés comunal: després de la collita, hi passaven els ramats. La font vincula el caràcter comunal a aquest ús de pastura.» **Seguiment:** «Això vol dir que el camp no es podia sembrar?» **Resposta:** «No necessàriament. La mateixa fitxa recull casos en què es conreava en determinades condicions; el dret de pas i de pastura depenia de si el terreny era “de guarda” i de si era buit de conreu.» |
| «Què indica aquesta fila del gràfic?» → «2014 — verd (català), 57,7 — morat (castellà), 56,4.» | **Usuari:** «En aquesta enquesta, el text i el gràfic diuen el mateix sobre el català i el castellà?» **Assistent:** «No. Per al 2018, el text dona 56,8 al català i 57,6 al castellà, però el gràfic, segons els colors de la llegenda, assigna 57,6 al català i 56,8 al castellà. La fitxa registra la contradicció, però no permet saber quina presentació reflecteix millor les dades originals.» **Seguiment:** «I el 2014 també hi ha aquesta discrepància?» **Resposta:** «No en el gràfic descrit: el 2014 hi situa el català a 57,7 i el castellà a 56,4. La contradicció concreta que documenta la fitxa és la del 2018.» |
| «Què explica la secció “El relat”?» → un fragment que comença a mig episodi. | **Usuari:** «Per què, segons la llegenda, el santuari de Meritxell es va construir en aquell lloc?» **Assistent:** «Segons la llegenda, la imatge de la Mare de Déu tornava al peu de la gavernera on l’havien trobada, tot i que primer la duien a Canillo i després la deixaven a Encamp. Els veïns van entendre que volia quedar-s’hi i hi van construir el santuari.» **Seguiment:** «Això està documentat com un fet històric?» **Resposta:** «La font ho presenta com una llegenda i no n’estableix quan va començar a explicar-se. Com a fet institucional diferent, el Consell General va declarar la imatge patrona del Principat el 1873.» |
| «Què explica la secció “I aquí hi ha el document que ho resol”?» → «Tres coses que el corpus registra per separat:» | **Usuari:** «Per què el 1895 es parlava d’un interès del tres i terç i també del cinc per cent?» **Assistent:** «Perquè els tipus s’aplicaven a contractes diferents. El decret mantenia el tres i terç per als censals i fixava el cinc per cent per a la resta.» **Seguiment:** «Per tant, el tres i terç encara era vigent aquell any?» **Resposta:** «Sí, per als censals. El decret del 25 de novembre de 1895 el reconeixia com la taxa legal de la Vall; el cinc per cent s’aplicava als altres contractes.» |

Els exemples de la taula són calibratge editorial, no registres exportables. Abans d'incorporar-ne cap a `review/conversations.jsonl`, comprova totes les afirmacions a la font i registra la procedència al fitxer corresponent.

## Porta de qualitat

Abans d'acceptar un exemple, comprova:

- La pregunta inicial sona plausible en una conversa real i s'entén tota sola.
- La resposta comença resolent el dubte i usa frases completes. No pot ser només un fragment, una capçalera o un apunt.
- El seguiment continua el mateix fil i pregunta una cosa nova.
- La conversa no menciona seccions, taules, gràfics o files, tret que la persona pregunti explícitament per un document concret.
- El diàleg no pressuposa que la persona conegui la font.
- Cada línia és JSON complet i tancat; cap conversa acaba amb un torn d'usuari sense resposta.
- Cada fet es pot verificar en una font citada a la procedència.
- La llicència i la redistribució estan registrades. Si no permeten entrenar, l'exemple no s'exporta.
- Llegit en veu alta, sembla una conversa d'ajuda i no un examen.

Els missatges contenen només les veus `user` i `assistant`. Els IDs, les fonts, les notes editorials i els estats de revisió van a `provenance.jsonl`.
