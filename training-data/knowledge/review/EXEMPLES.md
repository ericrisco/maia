# Exemples de calibratge

`examples.jsonl` conté dues converses de mostra. Són multitorn perquè el segon dubte apareix de manera natural després de la resposta; cada resposta també s'entén per si sola. Serveixen per revisar l'estil, no compten com a cobertura ni formen part d'un export automàtic.

Les dues mostres es basen en [`el-trinxat.md`](../../../docs/temes/gastronomia/plats/el-trinxat.md) i [`madriu-perafita-claror.md`](../../../docs/temes/territori/patrimoni-natural/madriu-perafita-claror.md). El corpus identifica Viquipèdia en català com a font CC BY-SA 4.0 i redistribuïble. Si aquestes mostres o adaptacions seves s'incorporen a un dataset, cal conservar l'atribució i complir la condició de compartir igual. Aquesta nota no resol per si sola les obligacions legals de l'export.

## Què cal observar

- La pregunta inicial parla del tema i no d'una secció d'una fitxa.
- La primera resposta resol la pregunta sense esperar el seguiment.
- El seguiment demana un detall nou que sorgeix del tema acabat d'explicar.
- Les respostes eviten afirmacions més àmplies que les dades de la fitxa.

## Exemple que rebutgem

```text
Usuari: Què diu la secció «El nom» de la fitxa del trinxat?
Assistent: El nom.
Usuari: I què més diu?
Assistent: Col i patata.
```

No és una conversa natural: depèn d'un document absent, no respon completament i el seguiment només demana que es copiï més text.
