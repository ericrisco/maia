# Pla de Maia Training Data

## Objectiu

Preparar dos datasets independents a partir de `docs/`:

- **Maia Knowledge**: converses que ensenyen coneixement documentat sobre Andorra.
- **Maia Language**: fragments humans de català andorrà contemporani, preservats des de `docs/parla/`.

Les respostes redactades per Knowledge no són mostra de llengua autèntica. Language no s'amplia amb respostes inventades.

## Punt de reinici de Knowledge

Les converses de `knowledge/archive/rejected-v1/` es conserven com a historial, però queden rebutjades: no són candidates, no compten per cobertura i no poden entrar als exports. La cua nova és `knowledge/review/conversations.jsonl`, amb procedència paral·lela a `knowledge/review/provenance.jsonl`.

Els exemples de `knowledge/examples/` ensenyen l'estàndard editorial. Són mostres, no dades aprovades ni cobertura. No s'exporten.

## Com escriure una conversa

1. Tria una afirmació o un petit grup d'afirmacions que una persona voldria entendre.
2. Imagina una situació recognoscible: ha sentit un terme, prepara una visita, llegeix una notícia o intenta entendre una regla.
3. Escriu la primera pregunta amb prou context perquè s'entengui sense haver vist Maia.
4. Respon directament. Explica el terme quan calgui i marca si és una tradició, una interpretació d'una font o una regla històrica.
5. Fes seguiments només quan la resposta desperti una pregunta natural. Cada torn nou ha d'afegir una peça: quan, qui, com funciona, quina excepció o què vol dir un terme.
6. Para quan el dubte s'hagi resolt. No hi ha un nombre objectiu de torns; habitualment en basten dos a quatre.
7. Verifica cada dada contra el corpus i anota totes les evidències i fonts a la procedència.

La conversa ha de sonar bé llegida només pels missatges d'usuari i assistent. Si les preguntes semblen un qüestionari sobre un document, es reescriuen.

## Preguntes que no farem

No preguntar per «la secció», «la fitxa», «aquesta fila», «el gràfic» o «el paràgraf». No copiar títols com si l'usuari els hagués llegit. No deixar fragments penjats com «I dos topònims que en surten:». No afegir un seguiment per complir una quota de multitorn. No inventar una motivació, una causa o una conclusió que les fonts no sostinguin.

La varietat surt de la situació i de la intenció, no de substituir paraules en una plantilla. Una pregunta factual curta és bona si és el que algú preguntaria; una conversa llarga és dolenta si cada torn repeteix el mateix.

## Revisió abans d'afegir

- La pregunta inicial s'entén fora del corpus?
- Algú preguntaria això en una conversa real?
- Cada resposta resol la pregunta abans d'afegir context?
- El seguiment neix del torn anterior i demana informació nova?
- La llargada és necessària?
- Cada afirmació, data i matís té evidència?
- Les fonts discordants o els buits es presenten sense inventar una solució?
- La procedència i els drets estan registrats? `pendent` o `no` no vol dir permís.
- La conversa continua sent natural si se'n treuen les metadades?

Una resposta negativa a les primeres cinc preguntes exigeix reescriure. Una dada sense evidència exigeix corregir o retirar-la. Un dret pendent impedeix exportar, encara que l'exemple serveixi per revisar estil.

## Cobertura i ritme

Inventariar tot `docs/temes/`, també seccions, paràgrafs, llistes i files útils de taules. Cobrir afirmacions útils, no només títols de fitxes. Per cada unitat, crear una conversa, vincular-la a una existent o registrar una exclusió amb motiu. Cobertura, unitats excloses i converses rebutjades han de quedar diferenciades als reports. No declarar Knowledge complet mentre hi hagi documents o afirmacions útils pendents.

Treballar en tandes petites: primer revisar un tema, després escriure, llegir en veu alta, comprovar evidències, validar procedència i només llavors afegir registres. No perseguir un nombre fix de preguntes. No generar variacions cosmètiques per inflar volum.

## Maia Language

Incloure només material que compleixi `veu == originaria` i `epoca == contemporania` (`apte_llengua == true`). Revisar transcripcions incertes, preservar la parla humana amb normalització mínima i agrupar els splits per peça o parlant. No redactar respostes noves en veu d'un parlant andorrà.

## Exportació

No crear train/validation/test fins que les converses hagin superat revisió humana, cobertura, deduplicació, verificació de drets i control de filtracions entre splits. Els fitxers finals contenen només `messages` amb torns `user` i `assistant`; evidències i procedència queden en fitxers de revisió.

## Cadència de canvis

Per cada pas funcional: revisar el diff, validar els fitxers afectats, comprovar `git status`, afegir només els fitxers del pas, fer un commit petit i confirmar el push abans de continuar. No incloure canvis locals de `docs/` ni dades de llengua alienes al pas.
