---
title: "Peces descartades"
---

# Peces descartades

Peces transcrites i **no admeses** al corpus de parla. Es guarden senceres amb el
motiu, perquè un descart sense proves és una opinió i perquè la següent sessió no
les torni a baixar.

## Càpsula #33, «La ramaderia a Andorra entre els segles IX i XI», Climent Miró

`ari-capsula-33-ramaderia/` · https://youtu.be/1e3bGvK7hXc · 14 min 36 s ·
CC-BY · transcrita el 2026-09-14 · **1.800 mots**

**Motiu: és un text escrit llegit en veu alta.** Dos passats simples sintètics:

> «els [?hereus] de Carlemany **impulsaren** un incipient intent de control del
> país i dels seus recursos» (00:00:42)
>
> «**aglutinaren** dominis» (00:11:41)

I **zero marcadors de parla en 1.800 mots** —0,0 per mil—, que és el registre
més baix de tot el que s'ha mesurat. Ni un *no?*, ni un *vull dir*, ni una
represa.

### Per què aquesta peça va estar a punt d'entrar

**El detector no la va veure la primera vegada.** Fins a aquesta tanda, la llista
de passats simples plurals era **una llista de formes** —`passaren`, `robaren`,
`foren`, `tingueren`...— i **`impulsaren` no hi era**. Era la segona vegada que
passava: a la tanda 19, la #58 va escapar-se perquè la llista tenia `foren` però
no `tingueren`.

La segona vegada va bastar. La llista es va substituir per **un patró
morfològic**:

```python
PLURAL_SIMPLE = re.compile(r"\b\w{3,}(?:aren|eren|iren)\b", re.I)
```

**Un inventari de formes sempre és incomplet; un patró, no.** Amb el patró,
aquesta peça cau a la primera línia i no cal haver previst el verb.

El preu del patró és un fals positiu —`preparen`, present de *preparar*, que
marcava una peça ja admesa—, i es paga amb un conjunt d'excepcions **tret de les
40 transcripcions reals**, no imaginat: en tot el corpus només hi havia **una**
forma que hi caigués.

### Què s'ha après i s'ha conservat igualment

La peça és rica en lèxic ramader medieval i **no serveix com a mostra de
llengua**. Com amb la #60, el vocabulari queda anotat com a **indici de què
buscar en parla real**, i no es cita com a parla.

## Càpsula #60, «La pedra seca», Xavier Llovera

`ari-capsula-60-pedra-seca/` · https://youtu.be/Hl3_qTjeBcM · 12 min 23 s ·
CC-BY · transcrita el 2026-09-13 · **1.675 mots**

**Motiu: és un text escrit llegit en veu alta.** La regla diu «sempre parla real,
mai text escrit per algú altre», i això és un guió.

**La prova que no admet discussió** són dos **passats simples sintètics**:

> «Els nostres avantpassats **passaren** moltes hores trastejant rocs.» (00:01:5x)
>
> «les feixes **robaren** espai fins a la roca» (00:03:58)

**En català central i pirinenc ningú no diu *passaren* ni *robaren* parlant.**
És una forma exclusiva de la llengua escrita. Dues en mil sis-cents mots no és
un tret de parla: és algú llegint.

**La prova que hi va a favor** és la densitat de marcadors: **1,2 per mil**,
contra 89 de la peça més espontània del corpus. Però aquesta sola **no bastaria**
—la càpsula #57 té la mateixa densitat i és xerrada preparada, no llegida—, i per
això el detector només dona veredicte ferm quan hi ha passat simple.

**Què s'ha après i s'ha conservat igualment:** diu «de les explicacions pràctiques
dels seus **pares i padrins**», que és **el segon parlant del corpus** que fa
servir *padrí* amb el sentit d'avi, després de la Ruth Casabella a la tanda 2.
**Un text llegit no serveix com a mostra de llengua, però sí com a indici de
què buscar.** Això queda anotat i no es cita com a parla.

## Tres testimonis descartats a la tanda 23 i **readmesos** a la tanda 24

Garrallà Rossell (16,6 %), Naudi Casal (16,2 %) i Gaspà Picart (12,9 %) es van
descartar per proporció de conjectura **sense llegir-ne dos**. En llegir-los,
**se segueixen perfectament**: les marques cauen a mots funcionals i a noms, no
al contingut.

**Són al corpus.** Veure la tanda 24 del registre i
`docs/raw/parla/cg-constituent-{garralla,naudi,gaspa}/`.

**La lliçó, que val per a qui vingui:** la proporció de marques diu **quanta
conjectura hi ha**, no **si el text es pot fer servir**. Dues peces al mateix
percentatge poden ser una llegible i l'altra inintel·ligible, segons si les
marques s'agrupen o es reparteixen. **Només ho veu qui llegeix.**

## Càpsula #65, «Una conversa sobre Boris Skóssirev», Guillamet i Lang

`ari-capsula-65-skossirev/` · https://youtu.be/4nzPEHF4xLc · 22 min 31 s ·
CC-BY · transcrita el 2026-09-14 · **2.519 mots**

**Motiu: no és en català. És en castellà.**

> «Gerard Lang, **eres investigador, vives en España, eres alemán de origen y te
> dedicas a Andorra**.» (00:00:0x)

Un dels dos interlocutors és investigador alemany i la conversa es fa en
castellà de cap a peus. Del recompte de mots funcionals exclusius: **216
castellans contra 7 catalans, un 3 % de català**.

### Aquesta peça portava divuit tandes registrada com «la més valuosa»

Des de la tanda 2, el registre la citava com **«l'única conversa de dues veus
trobada amb drets nets»** i **«el candidat més valuós de tota la sèrie per a la
branca `espontani`»**. Es va repetir a la fitxa de font, al registre i a tres
tandes.

**Ningú no n'havia llegit ni una frase.** Venia d'una font andorrana, amb títol
en català i descripció en català, i **d'això se'n va deduir la llengua del
contingut**. La deducció era falsa.

**La correcció:** ara hi ha
[`comprovacio-llengua.py`](../comprovacio-llengua.py), i **s'ha passat a les
divuit peces admeses**. Totes surten entre el **99 % i el 100 % de català**.
Cap altra no tenia el problema, però això no es podia saber sense mirar-ho.

## Càpsula #58, «Història de l'esquí i dels esports de neu», Daniel Areny

`ari-capsula-58-esqui/` · https://youtu.be/zTETigZzhH0 · 12 min 34 s · CC-BY ·
transcrita el 2026-09-14 · **1.585 mots**

**Motiu: text escrit llegit en veu alta.** Tres formes de passat simple
sintètic, totes en narració seva:

> «Aquestes **foren** activitats residuals, que no **tingueren** molta
> repercussió ni un seguit en el temps.» (00:01:20)

I l'estructura del guió és transparent: «Hola, bon dia. Em dic Daniel Areny…
**i avui vinc a exposar-vos**», «**En primer lloc**, m'agradaria donar les
gràcies», «**En aquest vídeo intentaré exposar-vos breument**».

### Aquesta peça va servir per arreglar el detector

**El detector no la va condemnar a la primera.** La seva llista de passats
simples tenia `foren` però **no tenia `tingueren` ni `tingué`**, de manera que
només en va veure un i la va deixar en «sospitós».

La llista s'ha ampliat de 24 a **51 formes** —3a persona del singular i del
plural de les conjugacions regulars i dels verbs irregulars freqüents— i
**s'ha tornat a passar a totes les peces**:

- la #58 surt **TEXT LLEGIT** amb tres formes;
- la #60, que ja estava descartada, ara en mostra **tres** en lloc de dues;
- **cap de les setze peces admeses no ha caigut.**

**Un detector que no s'ha provat contra un cas que hauria d'agafar no està
provat.** Aquest el va agafar de rebot, perquè algú va llegir la transcripció.

## Concurs «Tesi en 4 minuts», Universitat d'Andorra

`uda-tesi-en-4-minuts/` · https://youtu.be/ixvzpBBa9AE · 45 min 39 s · **CC-BY** ·
transcrita el 2026-09-14 · **6.191 mots**

**Motiu: qualitat d'àudio.** **El 16,3 % dels mots surten marcats com a
conjectura**, contra un rang de **3,5 % a 9,7 %** a les quinze peces admeses.
És gairebé el doble del pitjor cas del corpus.

La causa és al mateix vídeo: era un seminari del juliol del 2020 amb **«sis en
directe i quatre enregistrats en vídeo»**, és a dir mig híbrid i en confinament.
Per blocs de cinc minuts, la degradació és desigual —del 7 % als primers deu
minuts fins al **37 % del minut 40**—, cosa que confirma que és l'àudio i no
la llengua.

**El que s'ha après i val la pena conservar:**

1. **Els torns s'anuncien en veu alta**: «Moltes gràcies, Anna. La següent
   doctoranda, Blanca Carrera». Això vol dir que **una peça multiparlant
   d'aquest format es podria partir per parlant sense diarització**, retallant
   per les marques de temps dels anuncis. **No s'ha fet**, però la via queda
   oberta i serveix per a la càpsula #65 d'AR+I i per als programes «El camí cap
   a la Constitució», que fins ara estaven bloquejats per això.
2. **Els doctorands no són necessàriament andorrans**, i això s'ha de comprovar
   un per un abans de transcriure.

## Com es comprova

[`detector-text-llegit.py`](../detector-text-llegit.py) passa el mateix examen a
qualsevol transcripció. Les sis peces admeses hi passen netes.

## Peces no baixades, i per què

| Peça | Motiu |
| --- | --- |
| AR+I #65, conversa Guillamet–Lang | **Dues veus i una no és andorrana.** Sense diarització no es poden atribuir els torns. Espera eina. |
| «El camí cap a la Constitució», 10 programes del Consell General | **Muntatge de talls de diversos testimonis.** Mateix problema de diarització. |
| Sessions del Consell General (plens, DOP) | **Text escrit llegit**, en bona part. I la calibració contra el Diari de Sessions no es pot fer: els arxius no se solapen. |
| RINS (AR+I), 4 podcasts de natura | **Locutats amb guió.** |
| «Temps d'escudelles» 1991 | Titularitat i consentiment sense resoldre. |
