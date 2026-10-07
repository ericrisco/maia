# Guia editorial de Maia Knowledge

Abans d'escriure, completa aquesta frase fora del diàleg: **«La persona vol aclarir…»**. Si només pots dir «vol saber què diu la fitxa», encara no hi ha una pregunta humana.

## Comprova la conversa

- La pregunta s'entén sense el document obert?
- La resposta resol el dubte a la primera frase?
- El seguiment reprèn una idea concreta que acaba d'aparèixer?
- Els torns d'usuari formen un fil continu?
- Cada afirmació factual té suport i respecta els límits de la font?
- Si el tema ja queda resolt, hem acabat?

## Evita

«Què explica la secció…?», «què indica aquesta fila?», referències a fitxes o apartats, respostes en forma de base de dades, «i què més?» sense referent, preguntes apilades i seguiments afegits per fer més llarga la conversa.

## Format final

Una línia JSONL per conversa, amb missatges alterns `user` i `assistant`. La primera intervenció és de l'usuari. La procedència es desa a part i no s'exporta al model.
