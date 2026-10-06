# Pla de conversa per al fine-tuning

## Objectiu

Crear converses en què una persona pregunta perquè vol entendre alguna cosa,
prendre una decisió o aclarir un dubte. La conversa ha de sonar natural encara
que l'usuari no hagi vist mai els documents de Maia.

El corpus és la font dels fets. No és el guió de la conversa: els títols, les
seccions, les files i el vocabulari de recerca no han de dictar la pregunta.

## Com redactar una conversa

1. Llegeix la fitxa i les fonts que sustenten la resposta. Apunta els fets,
   matisos, contradiccions i límits que cal conservar.
2. Decideix quin dubte real podria tenir algú. Per exemple: ha vist una cosa,
   ha sentit una explicació, vol saber què pot fer, o sospita que dues dades no
   encaixen.
3. Escriu la pregunta com la diria aquella persona, amb prou context perquè
   s'entengui sola. No facis referència a fitxes, seccions, gràfics o files.
4. Respon primer el dubte. Afegeix el context necessari perquè la resposta
   sigui entenedora, però no recitis la fitxa sencera.
5. Afegeix un seguiment només si és probable que la resposta provoqui aquella
   nova pregunta. El seguiment ha de reprendre una idea concreta de la resposta.
6. Llegeix el fil sense mirar la font. Si sembla un examen, un qüestionari o una
   seqüència de consultes independents, reescriu-lo.
7. Torna a contrastar cada afirmació amb el corpus i registra la procedència,
   l'atribució i les condicions de reutilització.

## Multitorn sense artificialitat

La mida habitual és de dos intercanvis (quatre missatges). Un sol intercanvi és
millor que un seguiment forçat. No hi ha cap quota de preguntes per document ni
de dades per conversa.

Un bon seguiment pot demanar què vol dir un terme que acaba d'aparèixer, si una
conseqüència també s'aplica al cas propi, o com es resol una aparent
contradicció. No ha de canviar de tema per cobrir una altra dada de la fitxa.

## Preguntes que cal descartar

- «Què explica la secció…?», «què indica aquesta fila?» i variants semblants.
- Preguntes que només tenen sentit per a qui té el document o una taula al davant.
- Paràfrasis de plantilla que només canvien el nom, la data o el lloc.
- Preguntes amb un escenari personal inventat que l'usuari no ha explicat.
- Seguiments que no depenen de la resposta anterior.

## Estil de resposta

- Comença per la resposta directa, no per una etiqueta o una llista de camps.
- Escriu en català clar i natural. No copiïs el to intern o emfàtic de les
  fitxes.
- Explica termes antics o locals quan siguin necessaris per entendre la resposta.
- Distingeix els fets de les tradicions, hipòtesis i lectures atribuïdes.
- Si el corpus conserva versions diferents, explica què discrepa i què sí que
  se sap. No triïs una versió sense base.
- No deixis mai una frase a mitges ni una resposta que depengui del títol de la
  conversa.

## Dues col·leccions separades

**Maia Knowledge** deriva els fets de `docs/temes/`. La cobertura es controla
amb l'inventari existent, però una dada no es converteix en pregunta si no hi ha
un dubte humà al darrere. Cada contingut passa revisió factual, editorial i de
drets abans d'arribar a `output/`.

**Maia Language** deriva només de parla humana elegible a `docs/parla/`. No
inventem entrevistadors ni convertim monòlegs en converses fictícies. Si la
transcripció o els drets no permeten l'ús, la peça queda fora.

## Flux de treball

1. Mantenir l'inventari complet de fonts i coneixement.
2. Escriure tandes petites de converses a `knowledge/review/` amb procedència
   separada.
3. Revisar naturalitat, dependència entre torns, exactitud, redundància i drets.
4. Actualitzar l'estat de cada exemple. Els candidats no són dades d'entrenament.
5. Exportar a `output/` només els exemples aprovats i amb reutilització
   compatible; treure'n qualsevol camp editorial o de procedència.
6. Separar train, validation i test per grup de coneixement/font, no per
   paràfrasi aleatòria.
7. Auditar Language separadament i no barrejar-lo amb Knowledge.

## Criteri per aprovar una conversa

Una persona que no coneix el corpus entén per què es pregunta i què respon
Maia. Cada resposta està sustentada. El seguiment sona espontani llegit en veu
alta. No hi ha cap dada inventada, cap fragment tallat, cap repetició de
plantilla i cap problema de drets pendent per a l'exportació.

Els exemples inicials de `knowledge/review/` serveixen per calibrar aquest
criteri; encara no són un dataset publicable ni un conjunt aprovat per entrenar.
