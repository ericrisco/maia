# Cua de revisió de Maia Knowledge

La cua és buida mentre calibrem el criteri amb les cinc mostres de [`../examples/`](../examples/). Les converses antigues que van motivar aquest reinici ja no compten com a candidats ni com a cobertura.

Quan comencem una tanda nova, afegeix només converses que hagin passat la guia de [`../EXEMPLES.md`](../EXEMPLES.md). El diàleg i la procedència han d'ocupar línies paral·leles a `conversations.jsonl` i `provenance.jsonl`.

Abans d'afegir un registre:

1. Llegeix només el diàleg. La pregunta inicial ha de tenir sentit per a algú que no ha llegit el corpus.
2. Comprova que expressa un dubte concret que una persona podria tenir, no una petició per resumir una secció, una fila o una fitxa.
3. La resposta ha de resoldre el dubte directament. Cada seguiment ha de néixer del torn anterior i preguntar una cosa nova.
4. Verifica cada fet al corpus i registra evidències, fonts, llicències i permisos a la procedència.
5. Si la conversa sona a examen, és incompleta sense la fitxa o força un seguiment per allargar-la, reescriu-la o descarta-la.
6. Marca les converses pendents de revisió humana com a no exportables.

No hi ha quota de torns: una conversa pot tenir un torn o diversos. No afegeixis un seguiment si la resposta ja resol la necessitat.
