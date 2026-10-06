# Pla per fer converses útils per a Maia

## Criteri de qualitat

La conversa comença amb una curiositat, una confusió o una necessitat recognoscible. L'assistent contesta directament. La persona fa un seguiment que sorgeix d'aquella resposta i demana una precisió nova. No cal allargar el diàleg si la continuació natural ja s'ha acabat.

Una bona conversa no és un qüestionari sobre un document. Qui pregunta no ha de saber que existeix una fitxa, una secció o una taula. Cada torn s'ha d'entendre amb el context que ja hi ha al diàleg.

## Flux de treball per conversa

1. **Llegir la font i els seus límits.** Verificar els fets, les atribucions, les contradiccions i allò que continua sense saber-se. Revisar també la llicència i les condicions de reutilització.
2. **Trobar el dubte humà.** Escriure en una frase què vol aclarir la persona i per què li podria sorgir aquest dubte.
3. **Escriure l'obertura.** Donar prou context perquè la pregunta sigui clara, però no explicar la resposta dins la pregunta.
4. **Respondre com a assistent.** Començar per la resposta; després afegir el context necessari. No recitar camps ni introduir fets que la font no sosté.
5. **Afegir un seguiment real.** Fer que el segon dubte depengui de la resposta i aporti una distinció, implicació o límit diferent. Evitar «i què més?» i preguntes de confirmació buides.
6. **Llegir-ho en veu alta.** Si sona a examen, a cerca dins d'un document o a resposta truncada, reescriure o descartar.
7. **Registrar la traça.** Guardar fonts, evidències i drets al fitxer de procedència corresponent. Mantenir l'exemple fora dels splits fins a revisió humana.
8. **Revisar el conjunt.** Buscar duplicats i preguntes que cobreixin el mateix fet amb una plantilla lleugerament diferent.

## Patró multitorn

No és una plantilla per omplir mecànicament. És una comprovació de coherència:

```text
Persona: dubte concret amb context natural
Assistent: resposta clara i completa
Persona: reacció plausible que neix de la resposta
Assistent: nova precisió, sense repetir el primer torn
```

Pot haver-hi més torns si la conversa ho demana. No hi ha una quota fixa de missatges ni una obligació de convertir cada fet en registre.

## Revisió abans d'acceptar

Per a cada conversa, decidir `acceptar`, `reescriure` o `descartar` i anotar el motiu:

- **Intenció:** sembla una cosa que preguntaria una persona?
- **Context:** s'entén sense consultar la font?
- **Seguiment:** és conseqüència natural del torn anterior i afegeix informació?
- **Resposta:** resol el dubte, sona fluida i no queda tallada?
- **Fidelitat:** cada afirmació és traçable i conserva els matisos i les incerteses?
- **Varietat:** aporta una intenció o coneixement que encara no està repetit?
- **Drets:** tenim permís per incloure aquest material a l'ús previst?

Una conversa pot ser un bon exemple d'estil i continuar sense ser exportable per manca de drets o de revisió.

## Exclusions editorials

Descartar enunciats com aquests:

- «Què explica la secció X?» o «Què indica aquesta fila?»
- preguntes que depenen d'un document que l'usuari no ha vist;
- frases incompletes com «I dos topònims que en surten:»;
- la mateixa pregunta reescrita diverses vegades;
- seguiments genèrics o afegits només per fer la conversa més llarga;
- fets que la font no confirma, presentats com a certs.

## Separació Knowledge i Language

**Knowledge** pot tenir preguntes i respostes redactades a partir de fonts, després de verificar drets i contingut. **Language** ha de preservar parla humana elegible; no s'inventen respostes per imitar un accent ni es converteixen fragments incerts en senyal lingüístic.

Les converses pilot de `knowledge/review/conversations.jsonl` mostren el to buscat. La seva procedència i estat són a `knowledge/review/provenance.jsonl`. No es generen splits fins que hi hagi prou registres revisats, drets clars, deduplicació i una estratègia contra la contaminació entre conjunts.

## Proper tram

1. Revisar plegats els exemples pilot i ajustar el to.
2. Acordar quins tipus de dubte i de seguiment funcionen millor.
3. Aplicar el criteri a un tema petit de Maia i revisar els registres abans d'ampliar-lo.
4. Incorporar més registres tema a tema, amb procedència i estat editorial per a cadascun.
5. Només després, automatitzar inventari, cobertura, deduplicació i exportació.
