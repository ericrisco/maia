# Protocol d'audició i anotació del corpus independent

Aquest protocol governa l'escolta dels 656 clips canònics, dels 30 clips de
formes escasses i dels 124 clips candidats. Les sortides ASR, els formants i
els descriptors de senyal només serveixen per localitzar i ordenar el
fragment; no són una decisió sobre la parla.

## Decisió mínima per clip

1. **Decisió auditiva:** `sí` si la forma candidata s'escolta sencera i en el
   context indicat; `no` si el model l'ha localitzada però l'àudio mostra una
   altra seqüència; `incerta` si el senyal, la segmentació o la veu no permeten
   decidir.
2. **Variant transcrita:** escriure el que s'entén, mantenint dubtes entre
   claudàtors (`[?]`) i separant una reformulació o una parla superposada.
3. **Nota:** explicar el motiu de la decisió i qualsevol problema del clip.

No s'ha d'escriure `sí` només perquè coincideixin dos models. La coincidència
és una prioritat de revisió.

## Què observar quan la forma és audible

- **Segmental:** vocals obertes o tancades, reducció, diftongació, hiats,
  sonorització o ensordiment, ròtica, laterals, africades, fricatives,
  consonants finals i elisió. Anotar l'IPA només quan el contrast sigui
  perceptible; si no, descriure'l amb paraules (`vocal més oberta`, `final
  debilitada`) i marcar-lo com a aproximat.
- **Prosòdia:** accent lèxic, moviment final (ascendent, descendent o suspès),
  allargament, pausa, acceleració, repetició i canvi de torn. Separar una
  impressió auditiva (`entonació ascendent`) de la mesura instrumental.
- **Morfosintaxi i discurs:** pronoms `en/hi/ho`, perífrasis, possessius,
  negació, connectors (`aleshores`, `llavors`, `o sigui`, `vull dir`),
  autocorreccions i marcadors de contacte amb el castellà. Citar el context
  local, no només la paraula aïllada.
- **Lèxic i pragmàtica:** formes locals o institucionals, diminutius,
  manlleus, tractament, intensificadors i fórmules de cortesia. No marcar com a
  andorranisme una paraula que també sigui general del català.

## Qualitat i incertesa

Registrar si hi ha música, reverberació, solapament, pregunta de
l'entrevistador, tall d'edició o soroll. Quan la variant no es pot distingir,
es conserva el buit i es tria `incerta`; no es completa amb la grafia de l'ASR.
Una observació fonètica és una observació d'aquest parlant i clip, no una
etiqueta de tot Andorra.

## Camps del registre

`registre-audicio.tsv` és el registre mestre. Les columnes humanes són
`forma_confirmada_auditivament`, `variant_transcrita`,
`trets_fonetics_observats`, `observacions_prosodiques` i `nota_audicio`.
La mostra equilibrada usa els camps equivalents i es pot projectar al mestre
amb `importa-auditoria-equilibrada-master.py`, que exigeix una coincidència
exacta de persona, forma i clip.

Les formes escasses tenen un registre propi (`registre-audicio-formes-escasses.tsv`)
i una columna `decisio_humana`; no es projecten al registre mestre fins que la
clau persona-forma-clip coincideix. Els candidats tenen les cues
`cua-audicio-candidats-prioritaria.tsv` i `auditoria-candidats.tsv`: la veu es
classifica com `persona-candidata`, `entrevistador`, `mixt`, `incerta` o
`pendent`, i la decisió de la forma es manté separada. Una confirmació candidata
no la converteix automàticament en persona canònica ni la connecta al graf
canònic; primer cal revisar veu, termes d'ús i atribució.

Per a una tanda, escoltar en aquest ordre: (1) veu i solapaments, (2) forma i
context, (3) variant literal, (4) trets segmentals, (5) prosòdia i pauses, i
(6) nota justificativa. Si falla el primer pas, la forma queda `incerta` encara
que l'ASR sigui consensual.

## Condició de tancament

El corpus analitzat només es tanca quan les 656 files canòniques i les 30 de
formes escasses tenen una decisió (`sí`, `no` o `incerta`), una nota
justificativa i, quan sigui pertinent, variant, trets fonètics i prosòdia. Els
124 clips candidats han de tenir a més una atribució de veu i termes d'ús
revisats abans de qualsevol promoció. Les files sense escolta continuen sent
pendents, encara que tinguin ASR consensual o formants disponibles.
