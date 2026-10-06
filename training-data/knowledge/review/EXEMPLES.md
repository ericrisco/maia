# Estàndard de conversa per a Maia Knowledge

La pregunta ha de néixer d'un dubte que una persona podria tenir sense haver
llegit la font. La resposta ha de resoldre'l de manera directa, clara i fidel.
La conversa completa ha de sonar bé en veu alta.

## Patrons que sí que serveixen

No són plantilles ni categories obligatòries. Són maneres habituals de començar
una conversa:

- «M'he embolicat amb dues xifres…» — aclarir una confusió.
- «Com pot ser que…?» — entendre una contradicció aparent.
- «Si jo fes X, què passaria?» — resoldre un cas concret.
- «Aleshores això vol dir que…?» — seguir una conseqüència de la resposta.
- «És veritat que…?» — comprovar una afirmació amb una premissa.
- «Quina diferència hi ha entre…?» — comparar conceptes que la persona pot
  confondre.

Canviar les paraules no és suficient. Una pregunta només aporta valor si canvia
el dubte que es resol o el coneixement que s'aprèn.

## Patrons que rebutgem

| Rebutja | Motiu | Converteix-ho en |
|---|---|---|
| «Què explica la secció “El relat”?» | Només té sentit mirant el document. | Una pregunta sobre el relat o un detall que sorprèn. |
| «Què indica aquesta fila?» | No diu quina dada importa ni per què. | Una pregunta que identifiqui la discrepància i demani com entendre-la. |
| «I dos topònims que en surten:» | Fragment sense pregunta ni resposta completa. | Una frase que expliqui què són els llocs i per què s'esmenten. |
| «Què més?» | No té una intenció concreta. | Un seguiment sobre una conseqüència o distinció acabada d'introduir. |
| «Quan se celebra?» després de cada resposta | Seguiment en sèrie sense cap transició. | Preguntar només si la data és útil per al dubte en curs. |

## Revisió torn a torn

Per cada torn, comprova:

1. **Context:** s'entén sense conèixer el títol de la font?
2. **Intenció:** sona com una curiositat, confusió, comprovació o necessitat real?
3. **Resposta:** contesta de seguida i s'entén sense rellegir la font?
4. **Fidelitat:** separa el fet documentat, la interpretació i allò que no se sap?
5. **Seguiment:** és plausible després de la resposta i demana informació nova?
6. **Veu:** ho diria així una persona en una conversa normal?

Si falla context, intenció, resposta o fidelitat, reescriu o rebutja el registre.
Si només falla el seguiment, acaba la conversa després d'una resposta completa.
No hi ha una llargada mínima ni un nombre de torns obligatori.

## Pilot

`pilot.jsonl` conté quatre diàlegs complets per provar aquest estàndard.
`pilot-provenance.jsonl` en traça les fonts i els drets. Són mostres editorials:
no són registres aprovats i no es poden exportar a entrenament. Un d'ells depèn
de premsa amb redistribució no permesa.

Les converses acumulades a `conversations.jsonl` continuen en estat d'esborrany.
Cal revisar-les amb aquesta mateixa llista, una per una.

## Mostres del nou enfocament

`human-dialogues/conversations.jsonl` recull tres converses completes per
revisar la naturalitat i els seguiments. `human-dialogues/provenance.jsonl`
registra fonts i límits de reutilització. La mostra no és un lot aprovat: tots
els registres continuen pendents de revisió humana i de drets.
