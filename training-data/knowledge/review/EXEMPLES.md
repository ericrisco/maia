# Exemples de calibratge: Maia Knowledge

Aquestes mostres ensenyen el criteri de redacció. **No són dades d'entrenament, no compten com a cobertura i no s'han d'afegir automàticament a cap export.** Les notes de font són internes.

## 1. Una tradició que es confon amb un ball

```text
Usuari: La Passa és un ball?
Assistent: No. La Passa de Sant Julià de Lòria és una cercavila de parelles de fadrins. Les parelles que es casaran aquell any van al davant i la resta s'ordena de més grans a més joves.
Usuari: I quan es fa?
Assistent: Al migdia del dilluns de la festa major de Sant Julià.
```

**Per què funciona:** la pregunta s'entén sense conèixer cap fitxa; el seguiment és la curiositat immediata sobre una celebració que acaba de sortir a la conversa.

**Font i drets:** [`la-passa.md`](../../../docs/temes/costums/ritus-de-pas/la-passa.md) cita premsa i el portal del Govern; les fitxes generals d'aquestes fonts no autoritzen la redistribució. Mostra només de calibratge; no elegible per a l'export fins que hi hagi evidència i drets resolts.

## 2. Una llegenda explicada com a llegenda

```text
Usuari: Per què es va construir el santuari de Meritxell just en aquell lloc?
Assistent: Segons la llegenda, un pastor va trobar-hi una imatge de la Mare de Déu sota una gavernera florida en ple hivern. La van dur a Canillo, però l'endemà havia tornat al lloc de la troballa; després va passar el mateix quan la van deixar a Encamp. Els veïns van entendre que la imatge volia quedar-s'hi i hi van construir el santuari.
Usuari: Això és un fet històric o forma part del relat llegendari?
Assistent: La història de la imatge que torna és una llegenda. La fitxa encara no n'ha identificat la font primària ni quan es va documentar per primer cop.
```

**Per què funciona:** la resposta no presenta la llegenda com un fet comprovat; el seguiment aclareix l'estatus de la història.

**Font i drets:** [`la-troballa-de-meritxell.md`](../../../docs/temes/cultura/llegendes/la-troballa-de-meritxell.md) cita premsa andorrana, amb redistribució no autoritzada. Mostra de calibratge; no elegible per a l'export fins que es resolgui la font.

## 3. Un plat compartit amb altres comarques

```text
Usuari: El trinxat és un plat propi d'Andorra?
Assistent: També és típic d'Andorra, però no és exclusiu del país: es fa en diverses zones del Pirineu, com la Cerdanya, l'Alt Urgell i el Berguedà.
Usuari: Què porta, a banda de la col i la patata?
Assistent: Es trinxen la col i la patata bullides, s'hi barreja el greix de la cansalada i es daura tot a la paella. Sovint també s'hi posa cansalada per sobre.
```

**Per què funciona:** corregeix una possible idea d'exclusivitat amb tacte i el seguiment demana un detall pràctic sobre el plat.

**Font i drets:** [`el-trinxat.md`](../../../docs/temes/gastronomia/plats/el-trinxat.md) cita Viquipèdia en català, CC BY-SA 4.0. Si aquesta mostra s'incorporés mai a un dataset, caldria conservar l'atribució i complir la condició de compartir igual; aquest exemple no és una aprovació de reutilització.

## 4. Llegir una comparació sense exagerar què demostra

```text
Usuari: Entre el 2019 i el 2024 va anar més gent al cinema o als museus?
Assistent: Al cinema: la proporció de persones que hi havien anat va passar del 57,4% al 66,3%. Als museus va baixar del 63,8% al 54,5%.
Usuari: Amb aquestes dues dades podem dir que és una tendència que continua?
Assistent: No. Són dues onades de l'enquesta, del 2019 i del 2024, no una sèrie contínua; permeten comparar aquests dos anys, però no afirmar què ha passat cada any entremig ni què passarà després.
```

**Per què funciona:** respon la comparació directament i el seguiment posa a prova una conclusió temptadora que les dades no sostenen.

**Font i drets:** [`cinc-anys-i-el-cinema-es-lunica-cosa-que-puja.md`](../../../docs/temes/cultura/cinc-anys-i-el-cinema-es-lunica-cosa-que-puja.md), basat en les onades 2019 i 2024 de l'enquesta d'hàbits culturals i esportius del Departament d'Estadística. El corpus declara CC BY 4.0 per a les dades estadístiques pròpies; cal conservar l'atribució i revisar l'abast concret abans d'exportar.

## Exemple que rebutgem

```text
Usuari: Què explica la secció «El relat» de la fitxa «La troballa de Meritxell»?
Assistent: Se la va endur a Canillo i la va posar sobre l'altar major. L'endemà, en obrir la porta de l'església, ja no hi era.
Usuari: I què més diu la fitxa?
Assistent: També parla d'Encamp.
```

La pregunta pressuposa que l'usuari té una fitxa oberta. La resposta és fragmentària i el seguiment només demana més text. Cal tornar al dubte real: què vol entendre aquesta persona sobre la llegenda?

## Revisió ràpida

- La pregunta inicial funciona sense cap document al davant?
- La primera resposta resol el dubte per si sola?
- El seguiment sorgeix de la conversa i afegeix una pregunta real?
- La resposta respecta què és cert, què és llegenda i què no sabem?
- Cada dada té període, unitat i context quan cal?
- Els drets de la font permeten aquest ús concret?
