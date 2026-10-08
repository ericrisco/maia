# Criteri de revisió de converses

`conversations.jsonl` conté candidats en format final de missatges. Llegeix primer només `messages`, sense veure títol, identificador ni procedència. Les notes de fonts i drets van a `../work/`.

## Una pregunta que faria una persona

- Ha de poder sortir d'una curiositat, un pla o una necessitat recognoscible.
- No ha de parlar de seccions, fitxes, gràfics, files, corpus ni documents.
- No ha de dependre d'una dada obscura ni d'un context que només coneix qui ha llegit la font.
- Pot incloure un escenari hipotètic senzill si realment ajuda a plantejar el dubte; no inventis una vida o experiència personal per decorar-lo.

Per exemple, «Què explica la fitxa de la Passa?» no serveix. «Aniré a la festa major de Sant Julià: quin dia fan la Passa, i què és?» és una pregunta concreta que algú podria fer abans d'anar-hi.

## Conversa multitorn

- El primer parell de torns resol completament la pregunta inicial.
- El seguiment reprèn una idea concreta de la resposta i en demana una precisió nova.
- Cada torn ha de ser útil si la conversa s'acaba en aquell punt.
- Els exemples de calibratge són multitorn; això no justifica afegir seguiments artificials a altres converses. Si no n'hi ha cap de natural, busca un altre fil.

## Respostes

- Respon directament abans d'afegir context.
- Escriu prosa clara, no una fitxa telegràfica ni una llista anunciada però absent.
- No afegeixis fets perquè semblin plausibles.
- Presenta una llegenda com a llegenda; diferencia la data del relat d'una data documental; conserva desacords i buits quan siguin rellevants.
- No parlis de fonts internes ni de com s'ha trobat la informació.

## Passada final

1. Llegeix el diàleg en veu alta sense mirar la font. Si sona a examen o a consulta del repositori, reescriu-lo.
2. Comprova cada afirmació a les fonts enumerades a `../work/provenance.jsonl`.
3. Confirma que el seguiment neix del torn anterior i aporta una dada nova.
4. Confirma que no hi ha repeticions, resposta buida, incertesa amagada ni referent confús.
5. Revisa drets abans d'exportar. Els candidats actuals no són exportables automàticament.
