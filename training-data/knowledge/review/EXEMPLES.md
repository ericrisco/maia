# Exemples i criteri de revisió

Les mostres editorials viuen a [`../examples/conversations.jsonl`](../examples/conversations.jsonl). Són una referència de to, continuïtat i exactitud; no compten encara com a cobertura temàtica.

## Abans d'aprovar una conversa

- La pregunta inicial s'entén sense haver llegit Maia ni conèixer cap títol intern.
- La resposta resol directament el dubte i es pot entendre sense completar-la amb la font.
- Cada seguiment demana informació nova que una persona podria voler després de la resposta anterior.
- Les respostes no converteixen la informació en camps telegràfics ni afegeixen context només per allargar el diàleg.
- Cada dada i cada matís d'incertesa estan sostinguts per les fonts indicades a `provenance.jsonl`.
- El registre és una conversa completa en català natural. No parla de «la fitxa», «la secció», «aquesta fila» ni d'IDs interns.
- La pregunta no introdueix una premissa que la resposta no pugui sostenir.

Els exemples són multitorn per calibrar el fil. Els registres futurs també poden ser d'un sol torn si aquesta és la forma més natural de resoldre la necessitat.

## Format del registre

Una conversa per línia JSONL:

```json
{"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

Els registres actius s'afegeixen a `conversations.jsonl`. La procedència, les llicències i les notes de revisió van en un fitxer separat i mai dins dels missatges.
