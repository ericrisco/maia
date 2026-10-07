# Guia d'exemples per a Maia Knowledge

Aquestes converses mostren el to i l'estructura esperats. Algunes ja són registres aprovats; les que duen `approved_sample` a la procedència continuen sent només material de calibratge i no entrenen el model.

## Converses que funcionen

### Entendre què és un estripagec

```text
Usuari: Què és exactament un estripagec? M'ha sortit la paraula i no m'imagino què és.
Assistent: És un barrot metàl·lic amb punxes irregulars als costats, col·locat a les finestres de bordes i cases. Les punxes servien per estripar la jaqueta d'un lladre que intentés passar el braç entre els barrots.
Usuari: Ara entenc el nom. Ve literalment de l'efecte que feia?
Assistent: Sí. «Estripagecs» ajunta «estripa» i «gecs», és a dir, jaquetes: el nom descriu què li podia passar a la roba de qui intentés entrar a robar.
Usuari: És una peça pròpia només d'Andorra?
Assistent: No. Se'n troben al Pirineu i també en altres zones, com el Ripollès, Osona i el Vallès.
```

La conversa parteix d'un terme que la persona no coneix. El seguiment pregunta pel nom i després per l'abast geogràfic, sense dependre de la fitxa ni d'una referència amagada.

### Entendre per què la imatge de Meritxell es queda al santuari

```text
Usuari: Per què la imatge de Meritxell no es va quedar ni a Canillo ni a Encamp?
Assistent: Segons la llegenda, cada vegada que la portaven a una de les dues esglésies, la imatge tornava a aparèixer al peu de la gavernera on l'havien trobada. Els habitants van interpretar que volia quedar-se allí i hi van construir el santuari.
Usuari: I quan la van declarar patrona d'Andorra?
Assistent: El Consell General la va declarar patrona i protectora del Principat el 24 d'octubre de 1873. La festa se celebra el 8 de setembre.
```

La pregunta planteja una curiositat comprensible. La resposta distingeix el relat llegendari de la dada institucional.

### No deduir més del que diu una fotografia

```text
Usuari: S'ha documentat algun estripagec en una casa concreta d'Andorra?
Assistent: Sí. Hi ha una fotografia identificada com una finestra amb estripagecs al Museu Casa Rull, a Sispony.
Usuari: Això vol dir que la peça original encara es conserva allà?
Assistent: No es pot concloure només a partir del registre de la fotografia. Aquest identifica el lloc on es va fotografiar la finestra, però no diu si la peça és original, si s'ha traslladat o si encara s'hi conserva.
```

La resposta diferencia el lloc identificat en una fotografia de l'estat actual de l'objecte.

### Entendre què feia comunal un terreny

```text
Usuari: Com podia ser comunal un camp que algú havia sembrat durant anys?
Assistent: En una sentència de 1790, el fet decisiu era que, un cop recollits els fruits, els guardians hi feien passar els ramats. Haver-lo sembrat no impedia que es considerés comunal: el pas i la pastura dels ramats comptaven per determinar-ne l'ús.
Usuari: Per tant, conrear-lo no volia dir que el propietari en pogués decidir tots els usos?
Assistent: Exacte. La font descriu terres privades gravades amb drets comunals de pas i pastura. En aquests casos, el propietari no podia canviar lliurement la rotació dels conreus sense autorització del consell parroquial.
```

La conversa explica el terme amb un cas concret i el seguiment pregunta per una conseqüència nova. La resposta manté la distinció entre propietat i drets d'ús.

### Aclarir per què apareixen dos tipus d'interès

```text
Usuari: He trobat una referència al tres i terç per cent i una altra al cinc. Es contradiuen?
Assistent: No necessàriament. Un decret del Consell General de 1895 diu que el tres i terç continuava aplicant-se als censals; per a la resta, tant el Consell com el Tribunal de Corts acceptaven el cinc per cent.
Usuari: Així, el decret episcopal de 1854 encara era vigent el 1895?
Assistent: Sí. El decret de 1895 diu que el tipus dels censals es mantenia «segons llei de la Vall», i el distingeix del tipus aplicat als altres casos.
```

Aquí la persona aporta una confusió concreta. La resposta resol la distinció sense repetir les notes internes de recerca.

### Saber quan una dada no es pot convertir en resposta

```text
Usuari: Què vol dir la fila de 2014: verd 57,7 i morat 56,4?
Assistent: Amb aquesta fila sola no es pot saber què mesura el gràfic ni què representen els colors. Cal identificar les categories, les unitats i el context abans d'explicar-la.
```

Aquest exemple només és admissible si la conversa forma part d'una situació on l'assistent pot demanar el gràfic o el seu context. Si el dataset exigeix una resposta factual autònoma, es descarta: no s'inventa què volen dir els colors.

### Planificar una festa

```text
Usuari: Estem pensant a venir a Andorra aquest hivern per veure la festa de l'ossa. L'Última Ossa d'Ordino i la d'Encamp se celebren per les mateixes dates?
Assistent: No. L'Última Ossa d'Ordino se celebra la primera setmana de desembre, durant la fira de Nadal. El ball d'Encamp es fa el dilluns de Carnaval.
Usuari: Ah, jo em pensava que les dues eren de Carnaval. Ordino sempre s'havia fet al desembre?
Assistent: No. A Ordino es representava per Carnaval; més endavant es va traslladar a Sant Esteve, als jardins d'Areny-Plandolit. Des de la recuperació del 2017 se celebra al desembre. La informació recollida no n'explica el motiu del canvi.
```

La pregunta conté una decisió real. El seguiment la resol amb la diferència de calendari.

### Aclarir dues versions d'una llegenda

```text
Usuari: A casa sempre m'havien dit que els minairons sortien d'una herba. Després he llegit que els tenien dins d'un canó. Com quadren les dues versions?
Assistent: Les dues imatges formen part de les llegendes. Alguns relats fan néixer els minairons de l'herba menaironera; després, l'amo els guarda en un canó. La tradició no acaba de resoldre si neixen de la llavor o si el minairó mateix n'és la llavor.
Usuari: I quin perill hi ha, si algú destapa el canó?
Assistent: En poden sortir milers de cop i demanar feina. Segons la llegenda, si l'amo no els en mana, el maten.
```

La primera pregunta compara dues idees que la persona ja ha sentit. La resposta conserva la incertesa de la font.

### Distingir una broma antiga d'una activitat actual

```text
Usuari: Els itineraris per trobar el Tamarro són una continuació de la cacera que feien abans?
Assistent: Comparteixen el personatge, però el plantejament és diferent. La cacera tradicional era una broma pesada: feien anar algú a buscar una bèstia imaginària. Avui el Tamarro també és una mascota i el protagonista d'itineraris familiars per la natura.
Usuari: O sigui que no és un animal que es pugui veure de veritat?
Assistent: Exacte. El Tamarro és una criatura del folklore, no un animal real. Els itineraris són una activitat turística, no una cerca d'una espècie que visqui als boscos.
```

El seguiment surt d'una ambigüitat concreta: si la criatura és real o forma part del joc.

## Patrons que no funcionen

```text
Usuari: Què explica la secció «El relat» de la fitxa «La troballa de Meritxell»?
Assistent: Se la va endur a Canillo i la va posar sobre l'altar major.
```

Això demana extreure una secció i la resposta comença a mitja història. Cal reformular-ho des del dubte d'una persona i donar el context necessari.

```text
Usuari: Què explica la secció «El vocabulari que ho ordena» de la fitxa «Un camp és comunal perquè hi passen els ramats»?
Assistent: I dos topònims que en surten:
```

També és una mala mostra: la pregunta exposa l'estructura de la fitxa i la resposta és un fragment editorial, no una explicació. Si no podem identificar una curiositat humana i respondre-la amb context, no la convertim en conversa.

```text
Usuari: Què explica la secció «I aquí hi ha el document que ho resol»?
Assistent: Tres coses que el corpus registra per separat:
```

És incomprensible sense la fitxa i la resposta no contesta res. No cal rescatar cada secció del corpus com a registre independent. En aquest cas sí que hi ha una pregunta possible sobre la diferència entre el tipus dels censals i el cinc per cent; s'ha de respondre amb la distinció i el decret, no amb l'encapçalament intern.

```text
Usuari: Què indica aquesta fila?
Assistent: 2014 — verd, 57,7 — morat, 56,4.
```

Sense context, no se sap quin gràfic es mira ni què vol dir la resposta. Si la dada és útil, cal explicar-la en una pregunta real amb els valors i les categories identificats.

```text
Usuari: Els minairons surten d'una herba?
Assistent: Sí.
Usuari: I de quina herba?
Assistent: De l'herba menaironera.
```

El segon torn no amplia gaire la resposta. És millor contestar l'origen amb el context rellevant en un sol torn, tret que la persona pregunti després per un aspecte nou.

## Checklist abans d'aprovar

- La pregunta inicial podria aparèixer en una conversa normal?
- La pregunta expressa una intenció real sense inventar biografia, records o plans de l'usuari?
- S'entén sense veure la fitxa, el títol d'una secció ni un gràfic ocult?
- La resposta contesta directament i dona context suficient?
- Cada torn següent neix de la resposta anterior i demana una cosa nova?
- La conversa continuaria tenint sentit si llegíssim només els missatges, sense conèixer el document d'origen?
- S'ha respectat la diferència entre fet, tradició oral, interpretació i incertesa?
- Les afirmacions tenen suport en les fonts declarades i els drets permeten redistribuir-les?
- Si elimino un seguiment, la conversa empitjora? Si no, l'elimino.

Qualsevol resposta «no» obliga a corregir o rebutjar el registre. No s'accepta una pregunta només per cobrir una unitat del corpus.
