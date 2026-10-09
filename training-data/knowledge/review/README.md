# Cua de revisió de Maia Knowledge

Aquí s'acumulen les converses candidates de Maia Knowledge. La guia de [`../examples/EXEMPLES.md`](../examples/EXEMPLES.md) serveix per calibrar l'estil; les mostres de `../examples/` no compten com a candidats ni com a cobertura. Les converses antigues que van motivar el reinici ja no formen part de la cua.

Quan comencem una tanda nova, afegeix només converses que hagin passat la guia de [`../examples/EXEMPLES.md`](../examples/EXEMPLES.md). El diàleg i la procedència han d'ocupar línies paral·leles a `conversations.jsonl` i `provenance.jsonl`.

Abans d'afegir un registre:

1. Llegeix només el diàleg. La pregunta inicial ha de tenir sentit per a algú que no ha llegit el corpus.
2. Comprova que expressa un dubte concret que una persona podria tenir, no una petició per resumir una secció, una fila o una fitxa.
3. La resposta ha de resoldre el dubte directament. Cada seguiment ha de néixer del torn anterior i preguntar una cosa nova.
4. Verifica cada fet al corpus i registra evidències, fonts, llicències i permisos a la procedència.
5. Si la conversa sona a examen, és incompleta sense la fitxa o força un seguiment per allargar-la, reescriu-la o descarta-la.
6. Marca les converses pendents de revisió humana com a no exportables.

Cada conversa nova té com a mínim dues preguntes d'usuari. El segon seguiment ha de ser curt i natural; si no és possible sense inventar contingut, no forcis el registre i explica l'exclusió a la cobertura.
