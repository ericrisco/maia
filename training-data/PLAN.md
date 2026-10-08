# Pla editorial de Maia Training Data

## Objectiu

Preparar dos datasets de fine-tuning amb usos diferents: coneixement verificable sobre Andorra i llengua andorrana real. La prioritat és que cada conversa sigui correcta, entenedora i versemblant en una conversa normal.

## Com trobar una bona pregunta

Abans de redactar, resumeix el fet en una frase i pregunta't: «En quina situació algú voldria saber això?» Si només es pot formular dient «aquesta fitxa», «aquesta secció», «aquesta fila» o «aquest gràfic», encara no hi ha una pregunta d'usuari.

Punts d'entrada possibles, sempre que el corpus els sostingui: una confusió concreta, un perquè, una situació pràctica, una comparació útil, una creença que algú vol comprovar o una pregunta de continuació. La variació surt de les necessitats reals, no de complir plantilles. No inventis experiències personals, argot ornamental ni premisses falses sense motiu.

## Escriure la conversa

1. **Pregunta:** concreta i autònoma. Si diu «això», el referent ha de ser clar dins del diàleg.
2. **Resposta:** comença per la resposta; afegeix només el context necessari. Separa fets, llegendes, opinions i incerteses.
3. **Seguiment opcional:** demana una aclaració o conseqüència que es desprèn de la resposta. No canviïs de tema ni repeteixis la primera pregunta.
4. **Tancament:** acaba quan la necessitat queda resolta. Una bona resposta d'un torn és preferible a un xat allargat artificialment.

## Prova de conversa humana

Llegeix-la en veu alta sense mirar la font. Reescriu-la o descarta-la si la pregunta no sona com una cosa que algú voldria saber; si depèn de conèixer l'estructura de la font; si la resposta queda incompleta o sembla una fitxa; si un seguiment no surt del torn anterior; si el diàleg exhibeix dades en lloc d'ajudar; o si alguna afirmació va més enllà de la font.

Una conversa només passa si és plausible, s'entén sola, és correcta i cada torn aporta alguna cosa.

## Estructura i estats

- `knowledge/examples/`: calibratge intern, no exportable.
- `knowledge/review/conversations.jsonl`: fitxer actiu de converses candidates, una conversa per línia. La procedència es desa a `knowledge/work/provenance.jsonl`.
- `knowledge/work/`: cobertura i anotacions internes, mai dins del missatge final.
- `knowledge/output/`: només converses aprovades, una per línia i només amb `messages`.
- `knowledge/reports/`: cobertura, exclusions i resultats de revisió.
- `language/`: flux separat basat en fragments humans elegibles de `docs/parla/`.

Els registres existents continuen a la tanda; es revisen amb aquest criteri i es corregeixen quan calgui. Cap registre és exportable fins que s'hagin revisat exactitud, duplicació, procedència i drets de totes les fonts.

## Maia Language

Només incloure material que compleixi els criteris del corpus (`veu: originaria`, `epoca: contemporania`, `apte_llengua: true`), amb qualitat de transcripció i drets comprovats. Preservar el text humà. No generar respostes que «sonin andorranes» si no provenen de parla real.

## Avanç

1. Acordar el criteri amb les mostres de `knowledge/examples/`.
2. Afegir pocs candidats nous i llegir-los en veu alta.
3. Verificar respostes, procedència i drets.
4. Rebutjar duplicats, preguntes artificials i fets sense pregunta humana clara; registrar-los a cobertura si convé.
5. Revisar per blocs `docs/temes/` i `docs/parla/` sense convertir cada paràgraf en una pregunta.
6. Fer splits només quan hi hagi prou registres i es puguin agrupar per tema, font o peça per evitar filtracions.

## Format

Una línia JSONL és una conversa completa. Els rols alternen `user` i `assistant`; cada `content` és text pla. Vegeu [`knowledge/examples/conversations.jsonl`](knowledge/examples/conversations.jsonl).
