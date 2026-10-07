# Guia editorial: converses que sonen humanes

## La pregunta ha de néixer d'una situació

Abans d'escriure-la, explica en una frase quin dubte té la persona. Per exemple: ha vist un programa, ha sentit versions diferents, vol explicar una tradició o necessita entendre un document.

Si el motiu real és «vol saber què diu la fitxa», encara no tenim una pregunta d'usuari. Reformula el dubte en llenguatge corrent o descarta'l.

## Prova de naturalitat

Llegeix només la intervenció de l'usuari i pregunta't:

1. Podria haver-la escrit algú que no coneix el corpus?
2. Què vol resoldre aquesta persona?
3. La diria així en una conversa normal amb un assistent?
4. El context és necessari i creïble, o només decora una pregunta de fitxa?

Una resposta «no» demana una reescriptura. Expressions com «què explica la secció», «què indica aquesta fila» o «digues dos topònims» són senyals d'alerta, no prohibicions absolutes: només tindrien sentit si la persona estigués parlant realment d'aquell document o d'aquella taula.

## Continuïtat entre torns

- Cada seguiment reprèn un detall de la resposta anterior.
- El seguiment demana una precisió, explora una conseqüència o resol una confusió que acaba de sorgir.
- No encadenis preguntes independents per allargar el registre.
- No obliguis cada registre a tenir un nombre fix de torns. Dos intercanvis naturals ja són una conversa; un seguiment forçat empitjora l'exemple.
- No facis que l'usuari repeteixi amb altres paraules la pregunta inicial.

## Resposta de Maia

- Contesta primer i sense preàmbuls editorials.
- Escriu com un assistent informat, no com una fitxa ni un informe.
- Explica prou perquè la resposta s'entengui sense consultar la font.
- No amunteguis detalls que no ajuden a aquell dubte.
- Atribueix llegendes i interpretacions amb naturalitat («segons la llegenda», «una interpretació proposa...»).
- Marca els límits quan siguin rellevants, sense convertir cada resposta en una llista de disclaimers.
- No presentis com a actual una dada històrica o normativa que no s'ha verificat com a vigent.

## Rebuig immediat

Descarta o reescriu el registre si:

- la pregunta només s'entén amb una fitxa oberta;
- el context és inventat només per fer que una dada sembli interessant;
- la resposta no resol el que s'ha preguntat;
- un seguiment canvia de tema sense motiu;
- es confon una llegenda, una hipòtesi o una interpretació amb un fet;
- s'inventa una conclusió per omplir un buit del corpus;
- la resposta és telegràfica, enciclopèdica o plena de metadata interna.

## Procedència i format

La persona revisora contrasta cada afirmació amb les fitxes i fonts originals. Les notes de revisió van a `provenance.jsonl`, no al diàleg. El text final exportable només conté missatges `user` i `assistant`.

Les converses de `EXEMPLES.md` són per calibrar. No són registres aprovats ni compten per a la cobertura.
