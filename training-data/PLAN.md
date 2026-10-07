# Pla de Maia Training Data

## Objectiu

Crear converses que ajudin una persona a entendre Andorra. La pregunta neix d'una necessitat humana; la resposta es fonamenta en el corpus. No convertim seccions, taules o paràgrafs directament en preguntes.

Knowledge i Language tenen fluxos, fonts i revisions separats. Cap exemple de calibratge s'incorpora automàticament al dataset.

## Mètode per escriure una conversa Knowledge

1. **Tria què vol aclarir la persona.** Pot voler entendre una aparent contradicció, saber què implica una norma, veure què ha canviat, relacionar dues coses o saber què permet concloure una dada.
2. **Redacta la pregunta sense mirar el títol de la fitxa.** Ha de tenir sentit per a algú que no ha llegit el corpus.
3. **Contesta primer el dubte.** Després afegeix el context mínim que evita una lectura equivocada.
4. **Construeix els seguiments a partir de la resposta.** Cada pregunta nova reprèn una idea concreta del torn anterior. Si el tema queda resolt, acaba.
5. **Comprova cada afirmació contra fonts elegibles.** Guarda documents, llicència, afirmacions sustentades i límits a la procedència, fora del diàleg.
6. **Llegeix només els torns d'usuari.** Han de sonar com una conversa contínua, no com una llista d'exercicis.

## Forma i to

- Normalment, dos o tres intercanvis. Un de sol és correcte si no hi ha cap seguiment natural.
- La primera pregunta és completa i concreta. No parla de fitxes, seccions, files ni del procés de recerca.
- El seguiment demana una precisió o comprova una conseqüència. No repeteix la mateixa pregunta amb altres paraules.
- La resposta comença pel punt principal. No amaga la dada essencial fins a un seguiment forçat.
- El diàleg no revela noms de fitxer, notes editorials ni traçabilitat interna.
- No inventa experiències personals per fer la pregunta més versemblant.
- Distingim obligació legal de resultat garantit, tradició d'història provada i diferència entre dos anys d'una tendència contínua.

## Rebuig immediat

Descarta o reescriu la conversa si la pregunta només funciona perquè el lector ha vist una fitxa; si la resposta no resol el dubte; si un seguiment canvia de tema sense pont; si la pregunta demana dades per omplir una llista; o si una resposta afegeix causes i certeses que la font no sosté.

## Revisió abans d'acceptar

Cada conversa necessita una intenció humana anotada internament, suport per a cada afirmació, drets i atribució verificats, seguiments coherents, revisió de naturalitat i control de duplicats. La procedència queda en un fitxer separat. Les dades es divideixen per tema i fonts relacionades per reduir leakage entre train, validation i test.

## Flux de Language

Només s'avalua material de `docs/parla/` que compleixi `veu: originaria`, `epoca: contemporania` i `apte_llengua: true`. També cal revisar drets i qualitat de transcripció. Les respostes han de conservar parla humana; no s'inventen frases ni seguiments per simular català andorrà.

## Fites

1. Revisar el criteri amb els exemples de `knowledge/review/`.
2. Aprovar el mètode abans de generar més registres.
3. Inventariar fonts, drets i cobertura tema per tema.
4. Produir i revisar candidats amb procedència separada.
5. Deduplicar, dividir per grups relacionats i validar els exports.
6. Desenvolupar Language sense barrejar-lo amb Knowledge.

No es dona per acabat cap conjunt per volum de registres. Primer van correctesa, naturalitat, drets i cobertura.
