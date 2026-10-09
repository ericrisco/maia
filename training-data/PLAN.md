# Pla de Maia Training Data

## Objectiu

Crear dos datasets separats a partir del corpus Maia. **Knowledge** cobreix fets sobre Andorra. **Language** conserva llengua contemporània produïda per persones andorranes. No barregem els objectius ni les seves fonts.

## Criteri per a Maia Knowledge

1. Comença per un dubte que una persona podria tenir sense haver llegit Maia.
2. Dona el context mínim perquè la pregunta inicial s’entengui sola.
3. Respon directament i amb prou context perquè el torn quedi resolt.
4. Afegeix seguiments només quan neixen de la resposta i demanen informació nova.
5. Mantén el fil: no facis repetir el tema ni afegeixis preguntes per complir una quota.
6. Marca si el corpus descriu una llegenda, una interpretació d’autor, una incertesa o una contradicció. No les converteixis en fets segurs.
7. Comprova cada afirmació a `docs/temes/` i registra fonts, drets i evidència fora dels missatges.
8. No exportis una font amb redistribució `no` o `pendent`.

No escriguis preguntes com «què explica aquesta secció?» o «què indica aquesta fila?». No facis servir títols de fitxa, IDs, noms de secció ni frases tallades com a prompt. Si cal veure el document intern per entendre la pregunta, reescriu-la.

Les cinc mostres de `knowledge/examples/` calibren preguntes quotidianes, seguiments contextuals, correcció de premisses i tractament de llegendes i matisos històrics. Són exemples editorials no exportables.

## Estructura

- `knowledge/examples/`: mostres de referència, amb procedència separada.
- `knowledge/review/`: converses noves pendents de revisió.
- `knowledge/work/`: inventari, evidència, drets i cobertura.
- `knowledge/reports/`: cobertura i qualitat.
- `knowledge/output/`: només exports aprovats.
- `language/work/`: selecció de fragments de parla humana elegibles.
- `language/review/`: fragments pendents de revisió.
- `language/output/`: només exports aprovats.

## Seqüència de treball

1. Revisar i aprovar el criteri amb les mostres.
2. Inventariar `docs/temes/` i revisar drets de cada font.
3. Crear converses per blocs de coneixement relacionats.
4. Llegir cada conversa sense procedència ni fitxa al davant; corregir preguntes artificials i respostes incompletes.
5. Verificar fets, drets, duplicats i cobertura abans d’aprovar.
6. Només llavors generar exports i particions train, validation i test.
7. Tractar `docs/parla/` per separat. Incloure només fragments humans elegibles i prou fiables; no inventar la veu de l’entrevistat.

La prioritat és exactitud, cobertura, naturalitat, diversitat útil i drets. El volum ve després.
