# Cua de revisió de Maia Knowledge

Les converses candidates actives són a `conversations.jsonl`; la línia corresponent de `provenance.jsonl` conserva fonts, afirmacions i estat dels drets. Les línies s'alineen pel `conversation_id` de procedència. Els candidats encara no són dades aprovades ni compten com a cobertura completa.

Revisa cada conversa des del dubte humà que planteja, sense consultar mentalment els títols o les seccions de la fitxa. La resposta ha de ser completa, directa i ajustada a la certesa de les fonts. Un seguiment només s'hi queda si neix naturalment de la resposta anterior.

`exportable: true` indica que l'estat de drets registrat permet considerar el candidat per a exportació; no vol dir que la conversa ja estigui aprovada. Els candidats amb drets pendents o incompatibles continuen fora de `output/`. No copiïs els candidats antics de `archive/` sense revisar-los amb el pla actual.
