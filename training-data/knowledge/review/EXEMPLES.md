# Exemples de conversa

Aquest fitxer fixa el criteri d'estil. Els exemples complets en JSONL són a [`examples.jsonl`](examples.jsonl) i no s'exporten com a dades d'entrenament.

## Conversa bona

La pregunta neix d'una interpretació plausible d'una dada; la resposta corregeix la part imprecisa i explica què permet afirmar la font.

```text
Usuari: El 2025, la majoria de famílies ateses per protecció infantil eren separades? Vol dir que separar-se és un motiu habitual d'intervenció?
Assistent: Eren el grup més nombrós, però no la majoria: 97 de les 233 famílies, un 41,6%. I la taula descriu com eren les famílies ateses; no explica per què van arribar al servei.
Usuari: Es pot comparar amb el tipus de família més habitual al país?
Assistent: No amb aquestes dades. La font no publica el repartiment de totes les famílies d'Andorra amb les mateixes categories, així que no permet fer aquesta comparació.
```

## Conversa que rebutgem

```text
Usuari: Què explica la secció «Quines famílies» de la fitxa «Tres-centes catorze criatures»?
Assistent: Separada 97, nuclear 47, monoparental 46.
Usuari: I què més?
Assistent: Altres tipus.
```

Aquesta versió demana que l'usuari conegui una fitxa, converteix una taula en una llista sense explicar-ne el sentit i deixa el seguiment sense resposta útil. Cal preguntar pel dubte real i contestar-lo en context.

## Comprovació ràpida

- La primera pregunta s'entén sense cap fitxa al davant.
- Cada torn següent respon a una curiositat que surt de la resposta anterior.
- La resposta no confon correlació, descripció i causa.
- Les xifres, els períodes i els denominadors coincideixen amb la font.
- Llegida seguida, la conversa sona a intercanvi útil i no a interrogatori.
