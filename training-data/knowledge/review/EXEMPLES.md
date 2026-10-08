# Criteri per a les converses de Maia Knowledge

Aquesta guia governa les candidates de `conversations.jsonl`. Els exemples de `../examples/conversations.jsonl` només calibren l'estil; no es copien a l'entrenament sense revisió.

## La pregunta ha de sonar humana

La persona pregunta pel tema que vol entendre, no per l'estructura del corpus. Pot arribar-hi amb una confusió, una comparació, una dada sorprenent o una qüestió pràctica. No ha de conèixer títols, seccions, files, fitxes o camps interns.

- No: «Què explica la secció “La regla de competència”?»
- Sí: «Si un comú et demanda, ho veu el mateix tribunal que si el demandes tu?»
- No: «Què indica aquesta fila?»
- Sí: «El gràfic i el text coincideixen sobre quin idioma tenia el valor més alt?»

La primera pregunta ha d'incloure el context mínim perquè s'entengui. Les preguntes de seguiment poden ser més curtes si el diàleg ja ha presentat el referent.

## La conversa ha de tenir continuïtat

Cada resposta resol la pregunta que acaba de rebre. El seguiment surt d'una distinció, un terme o un límit que acaba d'aparèixer. No s'afegeix un torn només per fer que el registre sigui multitorn.

- Un seguiment útil aclareix què implica una regla, què vol dir un terme, si una dada és segura o com es compara amb el cas que s'acaba d'explicar.
- Un seguiment buit és «I què més?» o una pregunta sobre un fet nou sense relació amb el fil.
- Si el tema no dona peu a una repregunta natural, és millor una conversa d'un sol torn que una conversa artificial.

## Respostes

- Comença amb la resposta directa i explica només el context necessari.
- Escriu frases completes, no notes, etiquetes ni fragments de la fitxa.
- Mantén clars els referents quan el diàleg fa servir «això», «ell», «llavors» o el·lipsis.
- Separa fets documentats de tradicions, interpretacions, estimacions i hipòtesis.
- Acota dates, llocs i conclusions al cas que la font permet afirmar.
- Si no se sap o les fonts discrepen, explica-ho sense inventar una resolució.
- No esmentis el corpus, IDs, estats, procedència ni pipeline dins dels missatges.

## Revisió obligatòria

Abans d'afegir una conversa, llegeix només els missatges i comprova:

1. La pregunta inicial podria fer-la algú que no ha vist la fitxa?
2. La resposta contesta la pregunta de seguida?
3. El seguiment neix del torn anterior i afegeix comprensió?
4. El diàleg sona natural llegit en veu alta, sense repeticions de plantilla?
5. Cada dada, nom, data i matís està verificat a les fonts?
6. La conversa evita conclusions més fortes que les fonts?

Registra procedència i drets a `provenance.jsonl`. Una candidate amb drets pendents es pot mantenir en revisió, però no passa a `output/`.
