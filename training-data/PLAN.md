# Pla de Maia Training Data

## Objectiu

Preparar dos conjunts independents a partir de `docs/`:

- **Maia Knowledge** ensenya a respondre preguntes sobre Andorra amb informació de `docs/temes/` i fonts reutilitzables.
- **Maia Language** preserva el català andorrà contemporani de parlants reals a `docs/parla/`.

No es creen diàlegs de Knowledge per imitar la parla de Language. No es generen mostres de Language a partir de preguntes o respostes inventades.

## El problema que corregim

Els exemples anteriors de vegades tractaven la fitxa com si l'usuari la tingués al davant: «què explica aquesta secció?» o «què indica aquesta fila?». Això produeix preguntes que una persona no faria i respostes incompletes que depenen del document.

El nou punt de partida és el dubte de la persona. Primer definim què voldria entendre. Després consultem el corpus per redactar una resposta exacta. El títol, la secció i la fila només serveixen per trobar evidència; no passen a la conversa.

## Procés per crear una conversa de Knowledge

1. **Descriure la necessitat en llenguatge planer.** Una frase interna, com «vol entendre per què la vall és patrimoni cultural» o «vol comparar l'origen de les importacions». No és un missatge del dataset.
2. **Comprovar que el corpus ho pot respondre.** Llegir les fonts, revisar-ne els drets i anotar els fets, els límits i les incerteses que importen.
3. **Escriure el diàleg sencer com una conversa.** La pregunta inicial ha de funcionar sense conèixer la fitxa. La resposta ha de resoldre-la. Cada seguiment ha de sorgir del que s'acaba de dir i obrir un dubte nou.
4. **Fer la prova de lectura a cegues.** Llegir només el diàleg, sense fitxa ni notes. Si sembla un examen, una cerca de camp o una excusa per cobrir una fila, reescriure'l o descartar-lo.
5. **Verificar cada afirmació i cada torn.** Cap motivació personal, causa, detall o conseqüència no documentats no s'afegeixen per fer més viva la conversa.
6. **Registrar procedència i decisió al mateix registre.** El fitxer de revisió guarda fonts, drets, afirmacions i missatges junts. L'export final conté només `messages`.

## Regles de redacció

- Preguntes breus i directes són benvingudes. No cal disfressar cada dubte amb una història personal.
- El context de l'usuari només s'hi posa si és necessari i no s'inventa. No atribuïm records, plans, família ni experiències a una persona fictícia.
- Variem les intencions: entendre una paraula, aclarir una confusió, comparar dues opcions, saber què es conserva avui, entendre una conseqüència o situar un fet en el temps.
- No repetim la mateixa plantilla canviant topònims o xifres. Una frase com «i què més?» tampoc no és un bon seguiment si no queda clar què demana.
- Les respostes comencen per la resposta concreta. Després donen només el context necessari per entendre-la.
- Una premissa errònia es corregeix amb respecte. Llegendes, interpretacions i incerteses es marquen com a tals.
- No s'inventa una causa perquè les dades mostrin una tendència. «El corpus no ho indica» és una resposta vàlida quan s'explica què sí que sabem.
- El multitorn és obligatori per als registres de Knowledge, però no justifica preguntes artificials. Si no apareix un seguiment creïble, s'ha de buscar un dubte inicial més ampli i relacionat. Si no n'hi ha, el contingut queda pendent; no s'infla.
- Cada torn ha d'afegir informació útil. No es reparteix una resposta breu en diverses preguntes.

## Llindar d'aprovació

Una conversa passa a `approved` només si compleix tots aquests punts:

1. Una persona que no hagi llegit el corpus entendria què pregunta el primer torn.
2. La primera resposta és completa per al dubte inicial, encara que la conversa s'acabi allí.
3. El seguiment és conseqüència plausible del torn anterior, no una segona pregunta enganxada per quota.
4. El seguiment demana informació nova i deixa clars els referents.
5. Totes les afirmacions són al corpus i cada font permet la reutilització prevista.
6. El diàleg sona normal en llegir-lo en veu alta.

Un sol «no» implica reescriure o descartar. No s'aprova una conversa perquè cobreixi moltes unitats.

## Estructura de treball

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── review/
│   │   ├── records.jsonl       # conversa, procedència i estat de revisió
│   │   ├── conversations.jsonl # vista generada; només approved
│   │   ├── EXEMPLES.md         # guia editorial i exemples de calibratge
│   │   └── unit-decisions.jsonl
│   ├── scripts/                # inventari i validació
│   ├── work/                   # inventaris regenerables
│   ├── reports/                # cobertura i decisions de qualitat
│   └── output/                 # exports preparats per entrenar
└── language/                   # flux separat per a parla humana autèntica
```

Els exemples de `EXEMPLES.md` i els registres `approved_sample` serveixen per calibrar el criteri. No són dades d'entrenament i no compten com a cobertura. Només els registres `approved` poden arribar a `conversations.jsonl`.

## Fases

1. Calibrar la veu i el llindar amb els exemples d'aquesta fase.
2. Revisar candidats de Knowledge d'un en un: drets, intenció humana, diàleg, evidència, naturalitat.
3. Revisar els registres antics amb el nou llindar abans de recuperar-ne cap. No hereten l'aprovació anterior.
4. Mesurar cobertura i qualitat sense convertir el nombre de registres en una quota.
5. Preparar splits només quan hi hagi prou converses revisades i sense separar converses o fonts relacionades.
6. Avançar Maia Language sota les seves regles d'autenticitat, consentiment, drets i fidelitat de transcripció.

## Acabament

**Knowledge** queda llest quan el coneixement útil del corpus està cobert amb converses correctes, naturals, traçables i sense seguiments artificials, i els splits i informes passen els controls.

**Language** queda llest quan s'han revisat les fonts elegibles, només s'hi inclou parla humana prou fiable, es preserva la veu de les persones i els splits eviten filtracions entre fragments relacionats.
