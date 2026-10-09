# Criteri per escriure converses de Maia Knowledge

Aquesta guia és la porta de qualitat dels registres a `conversations.jsonl`. Cal llegir-la abans de cada tanda. Els exemples de `../examples/` serveixen per calibrar l'estil; no són candidats ni compten com a cobertura.

## Comença per allò que vol resoldre la persona

Abans de redactar, resumeix en privat la necessitat: orientar-se per una visita, aclarir una paraula, entendre una diferència, comprovar una dada que ha sentit o saber què se'n pot concloure quan les fonts discrepen.

La pregunta inicial ha de tenir sentit sense veure el corpus. No preguntis què explica una fitxa, una secció, un gràfic o una fila. No copiïs el títol com si fos una consulta. Dona el context mínim perquè una persona que no coneix el document entengui què vol saber.

## Fes que el diàleg avanci

Cada registre és una conversa multitorn: almenys dues intervencions de l'usuari. El seguiment ha de néixer del que l'assistent acaba d'explicar i demanar una cosa nova: una conseqüència, una distinció, un detall relacionat o una aclaració d'una premissa.

No repeteixis la pregunta, no saltis a un tema aliè i no afegeixis torns per arribar a una xifra. Si la font no dona peu a un seguiment natural, no inventis cap resposta: anota la unitat a la cobertura i continua amb una altra. Naturalitat i veracitat tenen prioritat sobre el recompte.

## Respon com ho faria un assistent

Contesta la pregunta a la primera frase. Escriu frases completes, amb referents clars. Explica els termes locals quan apareixen. No facis servir fragments penjats, camps de base de dades ni llenguatge intern com «el corpus diu», «la fila indica» o «la secció explica».

No afegeixis causes, intencions, dates ni detalls que les fonts no sostinguin. Si hi ha desacord, presenta les versions i digues què no es pot resoldre. Si una font ofereix una interpretació, atribueix-la; no la converteixis en un fet establert. Evita dades volàtils de visites si la font no les manté actualitzades.

## Exemple que funciona

```text
Usuari: A la Farga Rosell, què entendré de com es treballava el ferro?
Assistent: Hi expliquen com es transformava el mineral en lingots i com es venien als mercats catalans. També s'hi poden veure eines del procés, com la trompa, el forn i dos malls.
Usuari: Se'n posa algun en marxa?
Assistent: Sí. Un dels dos malls es posa en funcionament dues vegades al dia.
```

La primera pregunta expressa una curiositat d'algú que vol visitar el lloc. El seguiment surt de la resposta i demana un detall nou.

## Exemple que no funciona

```text
Usuari: Què explica la secció «El vocabulari que ho ordena» de la fitxa «Un camp és comunal perquè hi passen els ramats»?
Assistent: I dos topònims que en surten:
```

La pregunta depèn de l'estructura interna del corpus i la resposta és incompleta. Cal trobar el dubte real que hi ha al darrere o deixar aquesta informació sense convertir-la en conversa.

## Comprova cada registre

- La pregunta inicial es podria fer en una conversa real i s'entén sense la fitxa.
- La resposta principal resol el dubte sense una introducció editorial.
- Cada seguiment continua el fil i pregunta una cosa nova.
- En llegir els torns en veu alta, no sona a examen ni a qüestionari.
- Cada afirmació té evidència identificable als documents i cada font té drets registrats.
- La conversa conté només missatges d'usuari i assistent; procedència i notes editorials van a `provenance.jsonl`.
- El registre queda `exportable: false` fins que una persona en revisi el contingut i els drets.

Si falla qualsevol comprovació, reescriu o exclou el registre. Una unitat sense pregunta humana bona continua comptant a l'informe de cobertura, però no s'ha de disfressar de conversa.
