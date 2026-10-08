# Exemples per revisar Maia Knowledge

La guia positiva és [`conversations.jsonl`](../examples/conversations.jsonl). Les converses d'allà mostren quatre seguiments que neixen de la resposta anterior i una resposta d'un sol torn. Són exemples d'estil; la seva procedència i el seu estat d'export consten a [`provenance.jsonl`](../examples/provenance.jsonl).

## Reescriu la necessitat, no el títol

| Pregunta que cal rebutjar | Per què falla | Criteri de reescriptura |
| --- | --- | --- |
| «Què explica la secció “El relat” de la fitxa de Meritxell?» | L'usuari ha de conèixer l'estructura interna de la font. | Pregunta pel dubte que hi ha al darrere, per exemple què explica la llegenda sobre el retorn de la imatge. |
| «Què indica aquesta fila?» | No diu quina dada, període, grup o unitat vol entendre la persona. | Dona el context de la comparació només si la font permet identificar-la amb certesa. Si no, descarta el candidat. |
| «I dos topònims que en surten:» | És un fragment de resposta, no una resposta completa. | Contesta amb una frase que identifiqui els llocs i expliqui per què importen per al dubte. |

## Multitorn sense quota

Un seguiment és bo quan la resposta anterior el fa probable. «Això està documentat com un fet o és una llegenda?» pot seguir una explicació d'una llegenda. «I què va passar aquell any amb el cinema?» no és un seguiment si el torn anterior parlava d'una tradició sense relació.

No afegeixis un torn només perquè el registre «ha de ser multitorn». Una pregunta ben resolta en un torn també és una conversa útil. El conjunt ha de contenir les dues formes.

## Llenguatge de les respostes

- Comença per la resposta concreta i després dona el context imprescindible.
- No facis que l'assistent parli de fitxes, seccions, files, corpus o del procés de recerca.
- No completis una frase amb un nom o una dada que només es pot recuperar mirant la font.
- Marca amb naturalitat la diferència entre fet, relat tradicional, interpretació i incertesa.
- No inventis una visita, una experiència personal ni una veu dialectal per fer més «humana» la conversa.

## Validació ràpida

Llegeix el diàleg en veu alta sense la font. Si la pregunta no sona com una cosa que algú voldria saber, si la resposta queda curta o si el seguiment canvia de tema, reescriu-lo o descarta'l. Comprova els fets i la procedència per separat; naturalitat no substitueix exactitud ni drets.
