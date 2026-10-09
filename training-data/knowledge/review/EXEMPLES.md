# Guia de conversa per a Maia Knowledge

## Què falla als exemples rebutjats

Les preguntes «Què explica la secció…?» i «Què indica aquesta fila…?» només
funcionen si l'usuari té la fitxa davant. No són preguntes que una persona faria
per entendre Andorra: descriuen l'estructura del document. Les respostes
«I dos topònims que en surten:» i «Tres coses que el corpus registra per
separat:» són fragments d'una explicació editorial, no respostes completes.
La dada del gràfic, sense una pregunta sobre què es vol comparar o resoldre,
queda descontextualitzada.

No es corregeix això esborrant «la secció» i mantenint la mateixa pregunta.
Primer cal imaginar el dubte d'algú; després, redactar la conversa; al final,
verificar-la amb la font.

## Quatre converses de calibratge

Els exemples complets són a
[`calibration/conversations.jsonl`](../calibration/conversations.jsonl), amb la
procedència a
[`calibration/provenance.jsonl`](../calibration/provenance.jsonl). Són una
mostra d'estil, **no dades aprovades per exportar**.

### 1. Una pregunta històrica concreta

**En lloc de:** «Què explica la secció “La regla de competència: depèn de qui és demandat”?»

**Pregunta humana:** «A l’Andorra del segle XIX, si un cònsol et devia diners, podies reclamar-li com a qualsevol altra persona?»

La resposta situa la regla en el temps. El seguiment pregunta per una diferència
que sorprèn —les causes criminals— i la resposta també deixa clar què no
explica la font.

### 2. Un dubte pràctic sobre una paraula local

**Pregunta humana:** «Un terreny podia ser d’una família i, alhora, deixar que hi pasturessin els ramats dels veïns?»

La resposta introdueix i explica *peixena* després d'haver contestat el dubte.
El seguiment pregunta per la conseqüència per al propietari; no demana una altra
definició.

### 3. Una història que respon el “per què”

**Pregunta humana:** «La festa major de Sant Julià té una dansa que es diu Marratxa. D’on surt aquest nom?»

La resposta explica el recipient que donava nom al ball. El seguiment pregunta
per la versió actual de la dansa. Cal mantenir aquest exemple en calibratge fins
que els drets de la font s'hagin revisat.

### 4. Dues xifres que semblen discrepar

**En lloc de:** «Què explica la secció “I aquí hi ha el document que ho resol”?»

**Pregunta humana:** «En un document andorrà de 1895 he vist un interès del 3,33% per als censals i del 5% per a la resta. Són dues versions incompatibles?»

La resposta resol la contradicció aparent explicant que els tipus s'aplicaven a
casos diferents. El seguiment comprova una conseqüència directa: si el 3,33%
encara era vigent aquell any.

## Porta de revisió

Llegeix només els missatges, sense el títol de la fitxa. Pregunta't:

- La primera intervenció sona com un dubte que algú podria tenir fora del corpus?
- La resposta contesta la pregunta a la primera frase, amb prou context per
  entendre-la?
- El seguiment neix del que s'acaba de dir i aporta una pregunta nova?
- Es pot entendre cada torn sense veure un títol, una fila o una secció?
- Cada fet està comprovat i la font permet el tractament proposat?

Si alguna resposta és no, reescriu o descarta la conversa. Dos torns no
converteixen una mala pregunta en una bona dada.
