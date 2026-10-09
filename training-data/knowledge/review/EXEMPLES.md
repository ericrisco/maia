# Guia per a converses de Maia Knowledge

## Comença per la persona

Escriu primer, només per a tu, què intenta resoldre la persona. Exemples: entendre si una norma canviava segons qui demandava, saber què podia fer el propietari d'una finca, o entendre per què un lloc té una història concreta.

Després redacta la pregunta com la diria algú que no ha vist el corpus. Dona el context que calgui, però no parlis de fitxes, seccions, taules, gràfics, files ni fragments. No copiïs l'encapçalament de la font com si fos una consulta.

## Mantén el fil

La primera resposta ha de contestar la pregunta. El seguiment ha de sortir d'allò que acaba de sentir la persona i demanar una cosa nova. Mantén referents clars: si el segon torn diu «això», ha de quedar clar a què es refereix.

No afegeixis torns per complir una quota. Si el corpus no permet un seguiment natural, busca un altre angle o no facis servir aquella unitat com a conversa. La naturalitat i la correcció valen més que la llargada.

## Escriu respostes completes

- Comença per la resposta, no per una introducció sobre la font.
- Fes servir frases completes i explica els termes locals.
- Afegeix només els detalls útils per entendre la resposta.
- No transformis interpretacions en fets ni completis buits amb intuïcions.
- Si les fonts discrepen, explica què sosté cada versió i què queda sense resoldre.
- Si una dada no consta, digues-ho amb claredat.

## Exemples de redacció

**En lloc de:** «Què explica la secció “La regla de competència: depèn de qui és demandat”?»

**Pregunta humana:** «Si un comú em reclamava una cosa, m'havia de jutjar el mateix tribunal que si jo el reclamava a ell?»

La primera pregunta demana una resposta sobre un dubte jurídic. La segona demana que s'extregui un fragment.

**En lloc de:** «Què indica aquesta fila del gràfic?»

**Pregunta humana, si el dubte és sobre les dades:** «Aquestes xifres semblen contradir el text. Quina dada és més fiable i què no es pot assegurar?»

Si les fonts no permeten decidir quina és correcta, la resposta ho ha de dir. No s'ha d'inventar una reconciliació.

## Converses de calibratge

Aquests diàlegs mostren el nivell esperat. Són exemples editorials, no registres nous ni aprovats per exportar. Les fonts i els estats de drets continuen a la procedència interna.

### Dubte sobre una regla històrica

**Consulta que es rebutja:** «Què explica la secció “La regla de competència: depèn de qui és demandat”?»

**Necessitat humana:** entendre si un cònsol tenia una protecció especial davant dels tribunals i si depenia del tipus de causa.

```text
user: A l’Andorra del segle XIX, es podia portar un cònsol als tribunals per un deute privat com a qualsevol altre veí?
assistant: Depenia del moment i de si el deute era personal o l’havia contret en exercici del càrrec. Abans de la Reforma de 1866 calia autorització prèvia per a qualsevol causa civil contra un cònsol; després, l’autorització només es mantenia per als deutes del càrrec.
user: I si el problema era que havia comès un delicte?
assistant: Per a una causa criminal no calia aquella autorització. La font marca aquesta diferència entre reclamacions civils i persecució criminal, però no n’explica el motiu.
```

El seguiment és natural perquè demana si la regla que acaba de sentir també s'aplicava a un altre tipus de causa. La resposta separa civil i criminal i no inventa el motiu de la diferència.

### Contradicció entre xifres

**Consulta que es rebutja:** «Què indica aquesta fila?»

**Necessitat humana:** aclarir quin balanç es pot afirmar quan la mateixa font dona recomptes diferents.

```text
user: A les inundacions del 1982 a Andorra, quanta gent va morir? He vist xifres diferents.
assistant: Per a Andorra, la font dona set morts i dotze desapareguts. Però no permet tancar el recompte: en altres punts del mateix article el total de morts passa de catorze a dotze, i també s’hi diu que inicialment s’havia parlat d’una cinquantena de víctimes a Andorra. Sense una font andorrana de contrast, no es pot triar una xifra definitiva.
user: I dels desapareguts, se’n va saber mai res?
assistant: La font no diu què se’n va acabar sabent ni n’identifica els noms. Per resoldre-ho caldria consultar els registres andorrans.
```

La resposta manté la discrepància visible. El seguiment pregunta per una conseqüència que la primera resposta deixa oberta, i l'assistent admet què no consta.

### Entendre com funciona una institució

**Consulta que es rebutja:** «Què explica la secció sobre els dos cosenyors?»

**Necessitat humana:** saber què passava si els dos cosenyors no coincidien i quin paper tenia el Consell General.

```text
user: Si els dos cosenyors no es posaven d’acord sobre una llei, qui ho desencallava? El país quedava aturat?
assistant: Segons André Vilar, el 1904 el poble podia desempatar-los amb un referèndum; la manca d’acord no obligava a mantenir l’statu quo. Ara bé, Vilar no cita cap norma ni cap precedent que confirmi com s’havia aplicat aquesta regla.
user: I el Consell General podia fer lleis pel seu compte?
assistant: Formalment, no, en la lectura de Vilar: la llei depenia de l’acord dels dos cosenyors. A la pràctica, però, el Consell sovint proposava disposicions i l’acord tàcit dels cosenyors les convertia en lleis. Vilar també diu que moltes lleis consagraven costums que els andorrans ja s’havien donat.
```

La resposta distingeix entre la regla formal i la pràctica descrita per l'autor, sense presentar aquesta interpretació com una certesa jurídica independent.

### Quan el seguiment no és prou bo

```text
user: A les eleccions andorranes, la votació parroquial també reparteix els escons proporcionalment als vots?
assistant: No. A cada parròquia, les dues candidatures més votades obtenen un escó cadascuna.
user: I quants habitants té Canillo?
```

Encara que les dues preguntes siguin humanes per separat, el seguiment no sorgeix de la resposta i canvia de tema sense motiu. Cal triar un altre seguiment que aclareixi el sistema electoral o descartar aquesta parella.

## Porta de qualitat

Abans d'acceptar un exemple, comprova:

- La pregunta inicial sona plausible en una conversa real i s'entén tota sola.
- La resposta resol el dubte a la primera frase.
- El seguiment continua el mateix fil i pregunta una cosa nova.
- El diàleg no pressuposa que la persona conegui la font.
- Cada fet es pot verificar en una font citada a la procedència.
- La llicència i la redistribució estan registrades. Si no permeten entrenar, l'exemple no s'exporta.
- Llegit en veu alta, sembla una conversa d'ajuda i no un examen.
- El seguiment sorgeix de la resposta anterior; no és una segona targeta de preguntes enganxada al mateix registre.
- La resposta no queda interrompuda ni depèn d'un missatge que no hi és.

Els missatges contenen només les veus `user` i `assistant`. Els IDs, les fonts, les notes editorials i els estats de revisió van a `provenance.jsonl`.
