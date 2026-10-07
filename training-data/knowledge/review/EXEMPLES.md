# Calibratge de converses de Maia Knowledge

Aquestes tres mostres fixen el punt de partida per a la revisió humana. Una
mostra no queda aprovada només perquè sigui correcta o passi el validador.
Cal llegir-la com un diàleg i comprovar que la pregunta sona espontània.

## Llegenda de la Dama Blanca

```text
Usuari: A la llegenda de la Dama Blanca també hi surt un llop. Quin paper hi té?
Assistent: Després que desaparegui el bisbe d'Urgell, un llop negre comença a sembrar la mort i el terror. Un síndic el caça, però més endavant té malsons i embogeix. La llegenda diu que el llop duia l'ànima negra del bisbe.
Usuari: I què li passa, al síndic?
Assistent: La Dama Blanca no el pot guarir i ell acaba morint. Després, el llop i el bisbe deixen de manifestar-se. És el desenllaç de la llegenda, no un fet històric documentat.
```

La pregunta parteix de la història, no del nom d'una secció. El seguiment demana
el desenllaç d'un personatge que acaba d'aparèixer.

## Visita a Barcelona

```text
Usuari: Passaré unes hores per Barcelona. On puc veure escultures de Josep Viladomat?
Assistent: En pots veure, per exemple, a la plaça de Catalunya (*Dona amb nen i flabiol*), a la Casa de la Ciutat (*Maternitat*) i als jardins de Joan Maragall (*Dos Tritons*).
```

La resposta resol una petició pràctica en un torn. No cal afegir una pregunta
només per convertir-la en multitorn.

## Ficció i història

```text
Usuari: He començat «Andorra, entre el torb i la Gestapo». La història va passar tal com la veiem?
Assistent: La minisèrie és una ficció basada en fets reals i en el llibre autobiogràfic de Francesc Viadiu. Dramatitza una xarxa d'evasió que ajudava per Andorra aviadors britànics ferits i perseguits per la Gestapo. Això no confirma que cada escena passés tal com es mostra.
Usuari: Què se sap de la xarxa, doncs?
Assistent: La trama parla d'una xarxa d'evasió que ajudava aviadors britànics ferits i perseguits per la Gestapo a través d'Andorra. La informació disponible no confirma quines escenes concretes van passar.
```

El seguiment pregunta per un límit pràctic que neix de la primera resposta.

## Rebutja aquests patrons

- «Què explica la secció X de la fitxa Y?»
- «Què indica aquesta fila?»
- Respostes que comencen a mitja idea o només deixen una dada sense context.
- Un seguiment de confirmació que repeteix la resposta anterior.
- Afegir torns perquè totes les converses tinguin la mateixa llargada.

## Revisió ràpida

1. Amaga la font i llegeix només els missatges.
2. Comprova que la primera pregunta podria aparèixer en una conversa real.
3. Comprova que la resposta contesta abans d'afegir context.
4. Suprimeix cada seguiment que no aporta una nova necessitat.
5. Comprova les afirmacions i els drets a `provenance.jsonl`.

Les mostres apareixen a `conversations.jsonl` amb estat `approved_sample` a la
procedència. Són material de calibratge; no són exemples aprovats per entrenar.
