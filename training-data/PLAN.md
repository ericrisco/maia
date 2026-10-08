# Pla per crear converses que faria una persona

## Què va fallar

Les mostres rebutjades parlaven de les fitxes, no del tema. «Què explica aquesta secció?» i «Què indica aquesta fila?» són ordres de lectura per a qui ja té un document al davant. Una persona curiosa preguntaria pel fet: qui podia demandar un cònsol, com funcionava un dret de pastura o per què dues xifres no coincideixen.

Algunes respostes també començaven a mig pensament —«I dos topònims que en surten»— o deixaven el context clau fora. El seguiment ha de néixer del que acaba de dir l'assistent, i la resposta ha de resoldre el dubte sencer.

## Regla de redacció

Escriu una conversa que pugui començar sense que ningú hagi llegit el corpus.

1. **Comença per una curiositat concreta.** Pot partir d'una sorpresa, un rumor, una contradicció o una cosa que la persona ha vist. No facis servir el títol, els apartats o les taules com a motiu de la pregunta.
2. **Dona prou context al primer missatge.** Ha de quedar clar de quin lloc, període o fet es parla.
3. **Contesta de seguida.** La primera frase resol la pregunta. Després afegeix només el context que l'ajuda a entendre-la.
4. **Fes seguiments que surtin del diàleg.** La persona pot aclarir una paraula, comprovar què ha entès, preguntar per una conseqüència o demanar què se sap d'un límit.
5. **Mantén el fil.** No tornis a començar l'explicació sencera ni canviïs de tema perquè queda una dada per cobrir.
6. **No inventis el torn que falta.** Si la font no dona un motiu, una data o una resposta, digues-ho amb claredat.
7. **Distingeix el tipus d'afirmació.** Una llegenda és un relat; una interpretació s'atribueix; una dada actual porta any; una incertesa no es converteix en certesa.
8. **Deixa fora la cuina interna.** Als missatges no hi entren fitxes, seccions, files, IDs, estats de revisió ni instruccions del pipeline. La procedència va separada.

## Què vol dir multitorn

Cada mostra de calibratge té almenys dues intervencions de l'usuari. El seguiment ha de ser plausible i aportar un dubte nou. No allarguis una conversa només per complir el nombre de torns. Si un tema no dona peu a un seguiment natural, busca un altre angle o no el facis servir en aquesta tanda.

## Prova de lectura cega

Llegeix només els missatges, sense obrir la fitxa. La mostra falla si passa qualsevol d'aquestes coses:

- la primera pregunta no s'entén fora d'un document;
- sona com un examen o una consulta a una base de dades;
- l'assistent tarda a respondre el que li han preguntat;
- una resposta queda en forma de nota, títol o fragment;
- una repregunta podria haver-se escrit sense llegir la resposta anterior;
- la conversa fa passar una llegenda, hipòtesi o dada discutida per un fet segur.

Després de la lectura cega, comprova cada afirmació amb les fonts. Registra també què no permet concloure la font.

## Separació dels dos datasets

**Knowledge** parteix de `docs/temes/`. Les converses són redacció nova, però els fets només poden venir del corpus. Només es podran exportar quan passin la revisió de qualitat i drets.

**Language** parteix de `docs/parla/`. Les respostes han de provenir de persones reals i elegibles. No s'inventen converses perquè “sonin andorranes” ni s'utilitzen mostres Knowledge com a senyal lingüístic.

## Ritme de producció

Cada conversa candidata és un pas independent. Després de redactar una conversa, afegeix la seva procedència, actualitza la cobertura del document, valida els missatges i les fonts, i fes un commit i un push a `main`. No passis a la pregunta següent fins que el push s'hagi confirmat. Un commit no ha d'incloure altres converses.

La cobertura és exhaustiva: un document pot necessitar diverses converses. Mantén anotats els fets i apartats que encara falten; una conversa no marca tota una fitxa com a coberta si només n'explica una part.

## Fases

1. Acordar el to amb `knowledge/examples/conversations.jsonl`.
2. Ajustar la guia segons les observacions sobre aquestes mostres.
3. Afegir converses en lots petits; revisar-les abans d'ampliar el volum.
4. Vincular cada conversa a fonts i drets a `knowledge/examples/provenance.jsonl` o al registre de procedència de revisió.
5. Registrar cobertura, duplicats i exclusions a `knowledge/work/`.
6. Exportar només registres aprovats; separar train, validation i test per tema o font.
7. Tractar Language en una fase independent, amb els controls d'origen i transcripció.

## Format de calibratge

Una línia JSONL per conversa. El contingut inclou només els missatges `user` i `assistant`. La procedència és un fitxer separat. Les mostres són referències editorials i no passen automàticament a cap export.
