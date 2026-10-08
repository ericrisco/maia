# Mostres de conversa

Aquestes mostres ensenyen el to i el ritme esperats. Són exemples editorials: no compten com a registres, cobertura ni aprovació per a l'entrenament. El JSONL corresponent és `examples.jsonl`.

## Comprovació ràpida

Abans d'aprovar un candidat, llegim-lo com si fos una conversa que sentim al costat. Ha de complir tot això:

- La primera pregunta s'entén sense haver vist una fitxa.
- La persona pregunta una cosa concreta que li podria interessar de debò.
- La resposta resol la pregunta abans d'afegir context.
- Cada seguiment surt del que s'acaba de dir i demana una cosa nova.
- L'assistent corregeix amb calma les premisses equivocades i separa els fets de les interpretacions.
- Cada dada es pot verificar a la font indicada al registre de revisió.
- No hi ha frases truncades, referències opaques, repeticions ni preguntes afegides només per allargar el diàleg.

No cal que totes les converses tinguin la mateixa llargada. Una conversa de dos torns és millor que una de quatre amb farciment.

## Mostres acceptables

Les preguntes no demanen «què diu» una fitxa. Neixen d'una confusió comprensible, i el seguiment comprova una conseqüència de la resposta.

### El trinxat és andorrà?

```text
Usuari: El trinxat és un plat andorrà?
Assistent: Es menja a Andorra, però no és exclusiu del país: és un plat pirinenc que també es troba a la Cerdanya, l'Alt Urgell i el Berguedà.
Usuari: I se sap si aquí es fa d'una manera pròpia?
Assistent: Amb la informació recollida no es pot descriure una variant andorrana concreta. S'hi explica la preparació general, però aquesta diferència local queda sense documentar.
```

### Per què «paisatge cultural»?

```text
Usuari: La vall del Madriu és patrimoni mundial pels paisatges de muntanya?
Assistent: La UNESCO la va inscriure el 2004 com a paisatge cultural. El reconeixement inclou la relació entre les persones i la muntanya al llarg del temps, no només el valor natural de la vall.
Usuari: Què hi ha a la vall que expliqui aquesta relació?
Assistent: Hi ha elements vinculats a la vida de muntanya, com bordes i cortals, camins ramaders i pastures gestionades comunalment. En conjunt, mostren com s'hi ha treballat i viscut.
Usuari: Això vol dir que encara s'hi fa transhumància com abans?
Assistent: No es pot concloure això amb la informació disponible. S'hi descriu la transhumància com una activitat que va sostenir l'economia durant segles i que avui forma part del patrimoni; no s'hi detalla fins a quin punt continua.
```

Les dues mostres es basen en [`el-trinxat.md`](../../../docs/temes/gastronomia/plats/el-trinxat.md) i [`madriu-perafita-claror.md`](../../../docs/temes/territori/patrimoni-natural/madriu-perafita-claror.md). Les fitxes declaren la Viquipèdia en català com a font; la fitxa de la font declara CC BY-SA 4.0. Si aquestes mostres s'incorporessin a un export, caldria conservar atribució i compartir igual.

## Mostra que rebutgem

```text
Usuari: Què explica la secció «El relat» de la fitxa «La troballa de Meritxell»?
Assistent: Se la va endur a Canillo i la va posar sobre l'altar major.
Usuari: I què més?
Assistent: L'endemà ja no hi era.
```

Depèn d'un document absent, no deixa clar a qui es refereix «se», i les respostes són fragments que no expliquen el relat. Caldria començar pel dubte real —per exemple, com explica la tradició la troballa— i donar una resposta completa, fidel a la font.
