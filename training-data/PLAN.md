# Pla de treball: converses que sonen humanes

## Objectiu immediat

Reiniciar els exemples editorials de Knowledge i acordar un patró de conversa abans de reprendre la producció. Les mostres actuals són una calibració, no un dataset ni una promesa de cobertura. No generarem més registres fins que aquest patró estigui revisat.

## El problema que corregim

Preguntes com «Què explica aquesta secció?» o «Què indica aquesta fila?» només tenen sentit davant d'una fitxa. Una persona normal preguntaria pel fet que li ha despertat curiositat. Les respostes tallades o en forma de notes tampoc resolen el dubte. Això fa que el model aprengui a parlar del corpus en lloc de parlar del tema.

## Com ha de sonar una conversa

- La primera pregunta expressa una curiositat recognoscible i conté prou context per entendre-la sense veure la font.
- L'assistent contesta de seguida, amb català natural i una resposta completa. Després afegeix només el context que ajuda.
- La repregunta surt del que s'acaba de dir: demana aclarir un terme, entendre una conseqüència, comprovar una suposició o saber què passa després.
- L'assistent aprofita el context dels torns previs. No reinicia l'explicació ni canvia de tema sense motiu.
- Cada conversa de calibració té com a mínim dues preguntes de l'usuari. No afegirem torns només per allargar-la; si no hi ha una continuació natural, el registre no és multitorn i no s'inclou en aquesta tanda.
- La resposta distingeix fets documentats, relats tradicionals, interpretacions i allò que no se sap. No omple buits amb intuïcions.
- Els missatges no mencionen fitxes, seccions, taules, corpus, IDs ni el procés de recerca. La procedència es desa en un fitxer separat.
- Cal llegir la conversa en veu alta. Si sembla un examen, una consulta a una base de dades o una resposta escrita per resumir un document, es reescriu.

## Filtres editorials abans d'acceptar una mostra

1. **Pregunta humana:** algú podria dir-la en una conversa real, sense conèixer l'estructura de les notes?
2. **Resposta suficient:** contesta allò que s'ha preguntat i no acaba amb un fragment penjat.
3. **Seguiment lligat:** la pregunta següent depèn de la resposta anterior i hi aporta una curiositat nova.
4. **Fidelitat:** cada afirmació es pot justificar amb una font identificada; els límits també es conserven.
5. **Veu natural:** frases clares, concretes i sense to enciclopèdic automàtic.
6. **Drets i procedència:** cap font entra a cap exportació fins que se n'hagin registrat la llicència i les condicions d'ús.

Una sola fallada en els quatre primers filtres rebutja o retorna el registre per corregir. La qualitat no es decideix per volum.

## Preguntes que rebutgem

- «Què explica la fitxa/secció?»
- «Què indica aquesta fila/taula?»
- «Quins elements hi surten?» sense una curiositat concreta.
- «I què més?» sense un antecedent clar.
- Paraphrases consecutives de la mateixa pregunta.
- Preguntes que pressuposen un fet que les fonts no confirmen.
- Preguntes sobre una data o un horari actual sense indicar-ne l'any.

## Fases del projecte

1. **Calibrar la conversa.** Revisar les mostres de `knowledge/examples/` i ajustar pregunta, resposta, seguiment i llargada. No produir registres nous abans d'acabar aquesta revisió.
2. **Reconstruir l'inventari.** Processar tots els Markdown de `docs/temes/` i `docs/parla/`, mantenint els objectius separats. Preservar frontmatter, ordre, títols, paràgrafs, llistes, taules, files, enllaços, correccions, divergències i buits. Comptar errors i elements llegits.
3. **Extreure coneixement amb traça.** Per cada tema, registrar internament els fets, matisos i buits que podrien respondre una pregunta. No exposar aquesta estructura interna als missatges.
4. **Escriure converses Knowledge.** Crear converses naturals, majoritàriament multitorn, quan hi hagi una curiositat i un seguiment justificats. Incloure temes, preguntes contextuals, comparacions i límits del coneixement quan les fonts ho permetin.
5. **Revisar i cobrir.** Vincular cada conversa a la procedència; comprovar exactitud, naturalitat, cobertura, redundància i drets. Registrar també els motius d'exclusió.
6. **Preparar exports Knowledge.** Exportar només registres aprovats i fonts elegibles. Deduplicar i separar train/validation/test per tema o font perquè converses semblants no acabin en particions diferents.
7. **Construir Language per separat.** Revisar les peces de `docs/parla/`; admetre només veu originària, contemporània i marcada `apte_llengua: true`. Filtrar transcripcions incertes i registrar drets.
8. **Preservar la parla humana.** Convertir a format chat només els fragments amb estructura conversacional. Mantenir lèxic i sintaxi; no inventar respostes ni imitar una veu andorrana.
9. **Validar i documentar.** Validar JSONL, rols, buits, duplicats, procedència, cobertura i separació de particions. Informar inclusions, exclusions i límits.

Cada fase funcional es revisa i valida abans del seu commit i push, segons l'objectiu del projecte. Els exemples de calibració no s'exporten automàticament.

## Format dels missatges

Una línia JSONL per conversa, amb només `messages` i els rols `user` / `assistant`. La procedència, els drets i les notes de revisió van separats.

## Següent pas

Revisar en veu alta les quatre converses de `knowledge/examples/conversations.jsonl`. Després corregirem el patró amb aquesta evidència i només llavors reprendrem els registres.
