# Criteri de conversa per a Maia Knowledge

Aquest document calibra la redacció de converses. Els missatges són el producte visible; les fonts, els drets i les unitats cobertes es registren a `provenance.jsonl`.

## Per què els exemples anteriors no bastaven

Dir «sona humà» no dona prou instruccions. Molts registres acabaven amb el mateix patró: pregunta factual, resposta plena de xifres, «i això vol dir...?», aclariment. La pregunta podia ser plausible, però el diàleg semblava un qüestionari creat per recórrer una taula.

La cobertura del corpus és una feina interna. No s'ha de notar com una llista de comprovació dins la conversa. Primer es tria una necessitat comunicativa; després s'hi incorpora el coneixement que realment ajuda a resoldre-la.

## Com construir un diàleg

Abans d'escriure'l, anota per a tu mateix:

1. **La situació comunicativa:** què intenta entendre, explicar, decidir o comprovar la persona?
2. **La pregunta espontània:** com ho preguntaria sense haver vist la fitxa?
3. **El fil de seguiment:** quin dubte nou podria sorgir de la resposta, sense que l'autor l'hagi de suggerir artificialment?
4. **El límit de la font:** quina conclusió no es pot treure?

Després escriu el diàleg. No incloguis aquestes notes als missatges.

### Regles de redacció

- Obre amb la necessitat o el dubte, no amb el nom de la secció, la fitxa o una fila.
- Fes que cada torn aporti una cosa nova: una distinció, una conseqüència, una excepció o una decisió pràctica.
- Accepta converses curtes quan el dubte queda resolt. No calen sempre dos seguiments.
- No facis servir «I això vol dir que...?» si la resposta no ha creat aquesta confusió de manera plausible.
- Varia la forma de les preguntes i les respostes. No comencis cada registre amb «Si...» o «Aleshores...».
- No inventis una biografia, una experiència personal ni una falsa urgència per fer la pregunta més viva.
- No converteixis cada fila, xifra o unitat de cobertura en una conversa independent. Agrupa dades quan serveixen per respondre una mateixa necessitat.
- No forcis tota la cobertura dins de converses llargues. Una conversa natural pot cobrir una part; la cobertura es comprova per separat.

## Exemples de calibratge

Els diàlegs següents parteixen de dades presents als registres revisats. Són exemples de forma i de progressió, no plantilles per copiar literalment.

### 0. Resoldre el dubte en una resposta

```json
{"messages":[{"role":"user","content":"Les bruixes d’Engolasters són una llegenda andorrana documentada?"},{"role":"assistant","content":"El corpus no ho pot confirmar. Joan Amades en va publicar una descripció detallada, però Pere Canturri explica que el 1994 no havia trobat cap andorrà que la confirmés. Això deixa la llegenda sense corroboració local en les fonts consultades; no demostra que no n’existeixi cap altra versió."}]}
```

**Per què funciona:** és una pregunta directa i la resposta resol el dubte amb el límit necessari. Afegir una pregunta de seguiment només per allargar-la no hi aportaria res.

### 1. Preparar una explicació breu

```json
{"messages":[{"role":"user","content":"He de resumir què ha passat amb el cinema entre el 2019 i el 2024. Puc dir que el públic jove és qui més hi ha tornat?"},{"role":"assistant","content":"No exactament. La proporció que anava al cinema va augmentar en tots els trams d’edat, però l’increment més gran va ser entre les persones de 45 a 64 anys: 12,8 punts. Entre les de 15 a 29 anys va pujar 3,4 punts."},{"role":"user","content":"Llavors, quina frase evitaria confondre l’augment amb qui hi va més?"},{"role":"assistant","content":"Pots dir que l’assistència declarada al cinema va créixer en tots els grups d’edat, amb l’augment més fort entre els 45 i els 64 anys. El 2024, però, la proporció més alta continuava sent la dels joves de 15 a 29 anys: 78,8%, davant del 68,6% entre els 45 i els 64."}]}
```

**Per què funciona:** la persona té una tasca concreta; el seguiment demana una formulació útil i neix de la distinció de la primera resposta. No demana llegir una taula en veu alta.

### 2. Comprovar si dues dades es contradiuen

```json
{"messages":[{"role":"user","content":"He vist que hi ha més persones inscrites a les biblioteques, però l’enquesta diu que hi va menys gent. Quina de les dues dades és correcta?"},{"role":"assistant","content":"Poden ser correctes totes dues perquè mesuren coses diferents. Les inscripcions van passar de 19.580 el 2016 a 29.364 el 2024. L’enquesta estima la proporció de persones que deien haver visitat una biblioteca: va baixar del 36,4% el 2019 al 30,7% el 2024."},{"role":"user","content":"Per tant, amb les inscripcions no puc afirmar que les visites hagin augmentat?"},{"role":"assistant","content":"Exacte. Una inscripció compta persones registrades; no compta ni les visites ni la freqüència d’ús. Per parlar de visites cal una sèrie de visites, que aquestes xifres no aporten."}]}
```

**Per què funciona:** parteix d’una aparent contradicció i resol la diferència entre mesures sense insinuar que cap dada sigui errònia.

### 3. Demanar una conclusió que les dades no permeten

```json
{"messages":[{"role":"user","content":"Els recomptes dels museus han baixat. Això vol dir que hi han anat menys residents?"},{"role":"assistant","content":"El recompte total de visitants va baixar de 149.679 el 2019 a 92.583 el 2024, però aquesta sèrie no separa residents i turistes. Per tant, no permet saber quin grup explica la baixada."},{"role":"user","content":"I l’enquesta pot aclarir-ho?"},{"role":"assistant","content":"L’enquesta també mostra una baixada en la proporció de persones que deien haver visitat un museu, del 63,8% al 54,5%. Però aquestes xifres tampoc no identifiquen si els visitants eren residents o turistes."}]}
```

**Per què funciona:** respon a la inferència que la persona vol fer i explica quin límit comparteixen les dues fonts.

## Exemples que cal rebutjar

```text
Què explica la secció «El relat» de la fitxa «La troballa de Meritxell»?
Què indica aquesta fila?
Quin és el percentatge de 2014?
La baixada afecta igual totes les edats? I els joves? I les persones grans?
```

Les tres primeres depenen de l'estructura de la font o semblen un examen. L'última encadena preguntes de cobertura sense una conversa que les motivi.

## Revisió abans d'incorporar un registre

- La pregunta inicial té sentit fora de Maia i no delata la fitxa d'origen.
- La necessitat és concreta i plausible, sense ficció biogràfica.
- Cada seguiment respon a alguna cosa dita abans i canvia o aprofundeix el dubte.
- Si traiem un torn, el diàleg perd una distinció o un pas útil; si no, traiem-lo.
- Les respostes comencen pel que la persona necessita saber i no reciten dades sense explicar-les.
- Les xifres tenen període, unitat i comparació clars. Una variació de percentatge no es confon amb punts percentuals.
- La font sosté les afirmacions i els límits. Cap correlació no es presenta com a causa.
- No hi ha una pregunta gairebé duplicada ni una seqüència mecànica repetida en els registres propers.
- Les unitats cobertes consten a la procedència, no s'utilitzen per justificar una pregunta artificial.

Si un registre no passa aquests punts, es reescriu o queda fora de la revisió activa.
