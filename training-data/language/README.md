# Maia Language

Aquest conjunt és independent de Knowledge. L'objectiu és conservar trets de
català andorrà contemporani a partir de parla humana del corpus `docs/parla/`.

Només s'hi inclouen peces marcades com a veu originària, contemporànies i
elegibles per a ús lingüístic, amb una fitxa de font identificada. El pipeline
extreu literalment les línies amb marca temporal i exclou les que contenen una
marca explícita d'incertesa. Cada fragment té una fila de procedència alineada
a [`review/provenance.jsonl`](review/provenance.jsonl).

Les mostres són text de parla per a entrenament causal, no exemples de
pregunta-resposta ni diàlegs sintètics. Els splits de `output/` s'assignen per
peça per evitar que fragments d'una mateixa transcripció apareguin a més d'un
conjunt. La transcripció d'àudio continua marcada com a pendent de verificació;
consulteu [`review/README.md`](review/README.md) abans d'utilitzar les sortides.
