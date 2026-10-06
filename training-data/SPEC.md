# Maia Training Data — especificació

## Objectiu

Crear dos corpus de fine-tuning separats a partir de `docs/`:

- **Knowledge**: cobrir tot el coneixement útil documentat a `docs/temes/`.
- **Language**: conservar parla humana andorrana elegible de `docs/parla/`, sense barrejar-hi prosa de Knowledge ni inventar torns atribuïts a persones.

La sortida d'entrenament és JSONL. Cada línia conté un objecte amb `messages`, una seqüència alternada de missatges `user` i `assistant`. No hi entren IDs, fonts, estats ni altres camps interns. La traçabilitat i les exclusions van en registres de revisió separats.

## Acceptació de Knowledge

1. Inventariar tots els documents de les tretze branques de `docs/temes/`.
2. Revisar cada secció, paràgraf, taula, fila, llista, cronologia, enllaç rellevant i matís epistemològic.
3. Enllaçar cada unitat útil amb una o més converses. Les unitats no entrenables han de tenir una exclusió motivada; els buits de font han de quedar pendents, no resolts per inferència.
4. Escriure preguntes que una persona faria per entendre el fet. No preguntar què diu un títol o una secció.
5. Respondre amb frases completes, context suficient i només afirmacions sostingudes pel corpus.
6. Fer converses multitorn amb seguiments que neixin de la resposta anterior. Agrupar preguntes relacionades; no afegir torns artificials per complir una xifra.
7. Mantenir dates, xifres, atribucions, divergències i incerteses quan canvien la resposta.
8. Separar train, validation i test per font i grup d'evidència per evitar fuga de contingut relacionat.

## Acceptació de Language

1. Revisar totes les peces de `docs/parla/` i aplicar-ne els criteris de veu, època, aptitud lingüística, certesa de transcripció i permisos.
2. Conservar literalment les respostes de parlants humans quan la font permet identificar el segment i el sentit.
3. No atribuir un fragment a una pregunta ni a un parlant si el material no ho justifica. Una pregunta editorial només és admissible si el fragment la respon sense alterar-ne el sentit.
4. Registrar exclusions, incerteses i procedència fora de la sortida pública.
5. Separar els splits per peça, parlant i font quan aquestes dades constin.

## Criteri de qualitat per conversa

- La pregunta s'entén sense haver llegit la fitxa del corpus.
- La primera resposta contesta directament i és completa per si sola.
- Cada seguiment té una relació clara amb el torn anterior.
- La conversa varia en forma i llargada d'acord amb el contingut.
- No hi ha fragments de capçalera, files sense explicació ni pronoms sense antecedent.
- Una revisió pot traçar cada afirmació a la font sense exposar aquesta traça al model.

## Estat de partida

El corpus de Knowledge conté 1.477 fitxes en tretze temes. La cobertura és pendent fins que l'inventari i el registre de cobertura la demostrin per a totes les fitxes. El corpus de Language conté peces de tipus diferents; no s'assumeix que totes siguin diàleg, transcripció literal ni redistribuïbles. Cap registre de mostra es considera aprovat per a entrenament fins que passi revisió factual, lingüística i de procedència.
