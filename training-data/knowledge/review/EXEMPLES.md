# Revisió de preguntes i converses

Aquest fitxer fixa el criteri editorial per a `conversations.jsonl`. Cada línia és una conversa candidata completa. La procedència i els drets s'anoten a `../work/provenance.jsonl`; cap candidat no és exportable automàticament.

## Què canviem

Una pregunta no ha de demanar que l'assistent resumeixi una peça del repositori. Ha de plantejar el dubte que aquella informació pot resoldre. Per exemple:

| Evita | Pregunta que sí pot fer una persona |
|---|---|
| «Què explica la secció sobre la regla de competència?» | «Si un cònsol devia diners a un veí, el veí podia reclamar-los als tribunals com a qualsevol altra persona?» |
| «Què explica la secció sobre el vocabulari?» | «Si el bestiar dels veïns podia pasturar en un camp, volia dir que el camp era del comú?» |
| «Què indica aquesta fila del gràfic?» | «El gràfic i el text d'aquest informe donen valors diferents per al 2018. Quins valors puc citar?» |
| «Què explica el relat de la troballa?» | «A la llegenda de Meritxell, per què van construir el santuari on el pastor havia trobat la imatge?» |
| «Què resol el document del cinc per cent?» | «El tres i terç i el cinc per cent s'aplicaven al mateix tipus de préstec?» |

La columna dreta encara s'ha de jutjar com a conversa, no aprovar només perquè evita dir «secció» o «fitxa». Si una pregunta depèn d'una situació inventada, una dada obscura o una referència que l'usuari no té, es reescriu.

## Conversa multitorn

- Cada conversa té com a mínim dues parelles `user` → `assistant`.
- El primer torn dona una resposta completa. No deixa una frase penjada ni anuncia una llista que no presenta.
- El seguiment reprèn una idea concreta que acaba d'aparèixer i demana una precisió o conseqüència nova.
- Si no surt un seguiment creïble, no s'allarga el diàleg per força: es busca un altre fil.
- Les respostes són útils per si soles i no inclouen metadades internes, IDs ni comentaris sobre el repositori.

## Revisió abans d'acceptar

Llegeix només `messages`, sense títol, ID ni font. Comprova que la pregunta inicial sigui entenedora per a algú que no coneix Maia, que cada resposta contesti el torn, que el seguiment neixi de la resposta anterior i que cada afirmació sigui fidel a les fonts. Distingeix explícitament llegenda, interpretació, discrepància i incertesa.

Qualsevol candidat que no passi un d'aquests punts s'ha de reescriure o descartar. Els exemples actuals són candidats de calibratge, no sortida d'entrenament: els drets de les seves fonts continuen pendents.
