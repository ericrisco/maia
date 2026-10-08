# Pla de Maia Training Data

## Objectiu

Crear dos conjunts separats a partir de `docs/`:

- **Knowledge** ensenya a respondre preguntes naturals sobre Andorra amb fets comprovables de `docs/temes/`.
- **Language** conserva el català andorrà contemporani de parlants reals de `docs/parla/`. No s'hi inventen respostes per imitar una veu local.

Aquest és un pla editorial i de curació. Les mostres de `knowledge/examples/` ensenyen el nivell esperat; no són registres aprovats per entrenar.

## El problema que corregim

Una conversa com «Què explica aquesta secció?» depèn que l'usuari conegui una fitxa. Una resposta com «I dos topònims que en surten:» és un fragment. Cap de les dues coses ensenya a mantenir una conversa útil.

La pregunta ha de néixer d'una curiositat que algú podria tenir sense haver vist el corpus. La resposta ha de resoldre-la amb context suficient. Les repreguntes han de continuar el mateix fil i aprofitar el que ja s'ha dit.

## Com construir una conversa

1. **Troba un dubte humà.** Busca una sorpresa, una aparent contradicció, una conseqüència pràctica, una comparació que ajudi a entendre el tema o una afirmació que algú voldria comprovar.
2. **Dona el context dins la conversa.** Si el tema és històric, situa l'època. Si una pregunta breu depèn d'un torn anterior, fes-la breu; la primera pregunta s'ha d'entendre tota sola.
3. **Contesta primer.** La primera frase ha de respondre el dubte. Després afegeix només el context que ajudi a entendre-ho.
4. **Continua el fil.** Una repregunta pot demanar una conseqüència, aclarir una paraula, comprovar si una dada és actual o preguntar què se sap d'un límit. No canviïs de tema per encabir una dada pendent.
5. **Fes servir català natural.** Escriu com un assistent atent. Són naturals «Ah, d'acord», «Però llavors…» o «I això encara es fa?», quan el diàleg hi porta. Evita que totes les converses comencin igual.
6. **Acaba quan s'ha resolt el dubte.** Les converses finals són multitorn: normalment tenen dues o tres intervencions de l'usuari. No afegeixis una repregunta buida només per assolir una llargada.
7. **No amaguis la incertesa.** Separa fets, interpretacions, llegendes, fonts que discrepen i dades que el corpus no pot confirmar. No converteixis una dada històrica en una afirmació sobre el present.
8. **Mantén les respostes completes.** Cada torn de l'assistent ha de tenir sentit amb el diàleg i no pot començar amb un fragment penjat. Les llistes només són útils quan responen millor que la prosa.
9. **Deixa la traçabilitat fora del diàleg.** No mencionis fitxes, apartats, files, IDs, estats ni el procés intern. Desa fonts, afirmacions i drets al fitxer de procedència.

## Formes útils de conversa

No són plantilles per copiar. Són angles possibles quan la font els permet:

- «Jo pensava que X era Y. Ho és?» — corregir una premissa amb tacte.
- «Com pot ser que X i Y passin alhora?» — explicar una aparent contradicció.
- «Això vol dir que…?» — aclarir una conseqüència sense anar més enllà de la font.
- «Quina diferència hi ha entre X i Y?» — comparar conceptes propers.
- «Això se sap del cert o és una llegenda/interpretació?» — distingir tipus d'evidència.
- «I avui encara funciona així?» — separar passat i present; dir quan el corpus no ho pot confirmar.
- «Quina de les dues versions és correcta?» — exposar la discrepància sense inventar una resolució.

No facis una pregunta per cada paràgraf, taula o fila. Combina fets quan una persona els preguntaria junts i deixa fora els detalls que no ajudin a respondre.

## Revisió abans d'afegir un registre

### Lectura sense fonts

- La primera pregunta és clara i versemblant per a algú que no coneix el corpus?
- La resposta resol la pregunta de seguida i sona natural en veu alta?
- Cada repregunta depèn del torn anterior i aporta un pas nou?
- La conversa manté el fil i acaba quan ja ha resolt el dubte?
- Cap resposta és un fragment, una nota de base de dades o una llista descontextualitzada?

### Comprovació de fonts

- Es pot rastrejar cada afirmació fins a una font concreta?
- La resposta conserva el període, els matisos i els desacords de les fonts?
- No presenta inferències com si fossin fets ni afirma actualitat sense verificar-la?
- Els drets i les condicions d'ús permeten l'ús previst?

Si falla una pregunta de lectura cega, reescriu-la o descarta-la. Si falla la comprovació de fonts o drets, no l'exportis.

## Estructura i estats

- `knowledge/examples/`: converses de calibratge amb procedència separada.
- `knowledge/review/`: només converses candidates que ja passen la lectura cega; cada conversa sencera ocupa una línia JSONL.
- `knowledge/work/coverage.csv`: inventari de continguts, converses que els cobreixen i feina pendent. En reiniciar una conversa, no es marca com a coberta.
- `knowledge/output/`: exports aprovats. No s'hi posen fitxers buits o provisionals.
- `language/`: inventari i fragments humans elegibles, separat de Knowledge.

Les mostres d'exemple no compten com a cobertura, no són train/validation/test i no s'exporten automàticament. Cada candidata necessita procedència i revisió de drets.

## Seqüència de treball

1. Llegir les fonts completes i escollir un dubte que s'hi pugui respondre.
2. Redactar la conversa amb preguntes humanes i seguiments coherents.
3. Fer la lectura cega; reescriure qualsevol torn rígid o mecànic.
4. Verificar cada afirmació, els límits de la font i els drets.
5. Afegir la conversa i la procedència; actualitzar només la cobertura que realment resol.
6. Validar JSONL, alternança de torns, fonts i cobertura abans de publicar el registre.
7. Més endavant, deduplicar, aprovar els drets, agrupar converses relacionades i crear splits sense leakage.

No començar per assolir una xifra de registres. Primer cal tenir preguntes creïbles, respostes correctes i una cobertura que es pugui auditar.
