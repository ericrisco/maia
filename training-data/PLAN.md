# Pla de Maia Training Data

## Objectiu

Preparar dos datasets independents:

- **Maia Knowledge:** respostes útils sobre Andorra, basades en `docs/temes/` i fonts reutilitzables.
- **Maia Language:** català andorrà contemporani extret de parla humana real, amb drets, consentiment i transcripció prou fiables.

La prioritat és la qualitat del diàleg i la fidelitat a les fonts. No hi ha quota mínima de registres ni d'unitats cobertes.

## El problema que corregim

Una pregunta com «Què explica aquesta secció?» només té sentit per a qui veu una fitxa. I una resposta com «Tres coses que el corpus registra per separat» no resol el dubte d'una persona. Això són consultes al document, no converses amb un assistent.

Per a cada tema, primer definim quin dubte pràctic, curiositat o confusió podria tenir una persona. Després comprovem si el corpus el pot respondre. Els títols, apartats, taules i identificadors serveixen per trobar evidència; no són el guió del diàleg.

## Procés per a cada conversa de Knowledge

1. **Escriure la intenció en privat:** quin dubte vol resoldre la persona? Si només es pot formular com «vull saber què diu la fila 4», no és encara una bona intenció.
2. **Comprovar evidència i drets:** consultar la fitxa i les fonts originals disponibles; anotar què se sap, què no se sap i si es pot reutilitzar el contingut en el dataset.
3. **Redactar el diàleg sencer:** pregunta inicial clara per si sola, resposta directa i seguiment que neix del que s'acaba de dir.
4. **Llegir-lo sense context:** amagar fitxes i notes, i llegir només els missatges en veu alta. Si sona a examen, a formulari o a recitació, reescriure'l.
5. **Revisar cada torn:** verificar les afirmacions, els períodes, les xifres, les premisses i els límits de la resposta.
6. **Registrar procedència i decisió:** conservar en la revisió les fonts i els drets; l'export d'entrenament contindrà només `messages`.

## Què fa que una pregunta soni humana

- Comença pel dubte, no per la fitxa: «La Passa és un ball?» en lloc de «Què explica la secció sobre la Passa?»
- No inventa un usuari, una biografia ni una situació personal per fer la frase més vistosa.
- No força expressions com «segons la fila», «en aquesta taula» o «què diu el document?» quan la persona no tindria el document al davant.
- Pot ser curta. La naturalitat ve de preguntar una cosa comprensible i pertinent, no d'afegir farciment.
- El seguiment és una pregunta que podria sorgir en sentir la resposta: demana un detall nou, comprova una conseqüència o aclareix una confusió. No és una segona pregunta enganxada per cobrir més dades.
- Cada resposta resol la pregunta del seu torn sense dependre de la següent.
- Si un tema no dona per a un seguiment honest, el deixem pendent. No hi afegim una pregunta artificial per complir una llargada.

## Llindar d'aprovació

Una conversa s'aprova només si totes les respostes són «sí»:

1. S'entén la primera pregunta sense haver llegit Maia ni cap font?
2. Respon a un dubte que una persona podria tenir de debò?
3. La primera resposta ja és completa si la conversa s'acaba allí?
4. El seguiment és conseqüència plausible del torn anterior i demana informació nova?
5. Queda clar a què es refereixen els pronoms i les expressions com «això»?
6. Cada afirmació és verificable i cada font es pot reutilitzar per a aquest ús?
7. Les xifres diuen què mesuren i de quin període són?
8. El diàleg sona normal llegit en veu alta?

Un sol «no» vol dir revisar, deixar pendent o descartar. La cobertura mai no compensa una pregunta artificial ni una font no autoritzada.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── review/       # converses candidates, procedència i exemples editorials
│   ├── scripts/      # eines de generació i validació, quan toqui
│   ├── work/         # inventaris regenerables
│   ├── reports/      # cobertura i qualitat
│   └── output/       # exports d'entrenament, només quan estiguin aprovats
└── language/
    ├── README.md
    ├── review/
    ├── scripts/
    ├── work/
    ├── reports/
    └── output/
```

Les carpetes buides tenen un `README.md` breu que n'explica el propòsit. No generem fitxers `train`, `validation` o `test` fins que hi hagi material revisat i un pla de partició que eviti filtracions.

## Fases

1. Fixar el criteri amb exemples de calibratge i revisar-lo amb lectura a cegues.
2. Crear converses de Knowledge una per una; comprovar fonts, drets, naturalitat i exactitud abans d'aprovar-les.
3. Recuperar registres antics només després d'avaluar-los de nou amb aquest llindar. Cap aprovació anterior no es trasllada automàticament.
4. Mesurar cobertura i duplicació sense convertir-les en quotes de redacció.
5. Fer splits agrupant converses relacionades abans de repartir-les.
6. Construir Language només amb parla humana elegible, sense fabricar respostes ni normalitzar la veu fins a esborrar-ne els trets.
7. Validar formats, drets, duplicats, cobertura i exclusions abans d'exportar.

## Maia Language

Només pot aportar senyal lingüístic una peça que compleixi els criteris del corpus (`veu: originaria`, `epoca: contemporania`, `apte_llengua: true`) i la revisió de drets aplicable. Cal escoltar o verificar directament els fragments i excloure els trams incerts. No convertir monòlegs en diàlegs inventats ni omplir el conjunt amb imitacions generades.

## Definició d'acabament

- **Knowledge:** el coneixement útil està cobert per converses correctes, naturals i traçables; els drets estan resolts; els splits i informes passen els controls.
- **Language:** s'han revisat les peces elegibles; només s'hi inclou parla fiable i autoritzada; es preserva la veu humana; els splits eviten filtracions entre fragments relacionats.
