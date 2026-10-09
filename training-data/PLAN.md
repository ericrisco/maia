# Pla de Maia Training Data

## Objectiu

Crear converses que ensenyin Maia a ajudar una persona amb dubtes reals sobre Andorra. Les preguntes han de sonar com una cosa que algú preguntaria en una conversa, no com una instrucció per inspeccionar el corpus.

## Regles editorials

1. **Comença per la necessitat de la persona.** Una pregunta ha de tenir sentit sense haver llegit una fitxa. Pot expressar curiositat, confusió o una comparació.
2. **Respon el dubte abans d'afegir context.** Cada resposta ha de ser clara i completa per si sola.
3. **Fes seguiments amb una funció.** El torn següent ha de néixer de la resposta i demanar una cosa nova. No afegeixis torns només per fer el diàleg més llarg.
4. **Conserva el context.** No facis repetir a l'usuari dades que ja ha donat ni introdueixis referències ambigües com «això» si no queda clar a què es refereixen.
5. **No inventis.** Cada dada ha de sortir del corpus. Separa què afirma una font, què no resol i què és una interpretació.
6. **Escriu com una conversa.** Evita respostes de base de dades, fragments penjats, llistes de camps i fórmules repetides.
7. **No parlis del corpus.** No preguntis què diu una secció, una fitxa, una fila o un gràfic, tret que la persona pregunti explícitament per una font o document que ha vist.
8. **No cal que tots els registres siguin multitorn.** En aquesta mostra, tots ho són per calibrar la continuïtat. Més endavant, el diàleg pot acabar després d'un sol parell si el dubte queda resolt.
9. **Mantén separats Knowledge i Language.** Les respostes de Knowledge es redacten a partir de `docs/temes/`; Language només pot utilitzar material humà elegible de `docs/parla/`.

## Flux de creació

1. Tria una necessitat que una persona podria tenir sense conèixer l'estructura interna de Maia.
2. Llegeix el document complet i els seus enllaços rellevants.
3. Escriu la conversa i comprova cada afirmació contra la font.
4. Llegeix només els missatges, en veu alta. Si sona a examen, si depèn de la fitxa o si el seguiment és forçat, reescriu-la o descarta-la.
5. Registra la procedència i l'estat dels drets fora dels missatges.
6. Mantén les mostres a `examples/`; no les tractis com a sortida entrenable.
7. Amplia la cobertura per blocs temàtics només després que el criteri editorial quedi validat amb aquestes mostres.

## Estructura

- `knowledge/examples/`: mostres per calibrar preguntes, respostes i continuïtat.
- `knowledge/review/`: candidats nous que encara necessiten revisió.
- `knowledge/work/`: cobertura i dades internes de producció.
- `knowledge/reports/`: resum de cobertura, qualitat i exclusions.
- `knowledge/output/`: exports aprovats; buit en aquesta fase.
- `language/`: flux separat per a parla humana contemporània.

## Fases

1. Revisar les cinc mostres i acordar el criteri.
2. Crear nous registres de Knowledge per blocs temàtics.
3. Revisar exactitud, naturalitat, seguiments, duplicats, cobertura i drets.
4. Revisar Language de manera separada, segons `docs/CONTRACT.md`.
5. Preparar exports i particions només quan hi hagi volum i aprovació suficients.
