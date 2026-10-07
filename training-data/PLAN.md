# Pla de Maia Training Data

## Objectiu

Crear dos datasets independents a partir de `docs/`:

1. **Knowledge** respon preguntes reals sobre Andorra amb fets que el corpus pot sostenir.
2. **Language** conserva la manera real de parlar en català andorrà contemporani a partir de material humà admissible.

La prioritat és correcció, cobertura útil i qualitat de conversa. El volum no és un objectiu per si sol.

## El problema que corregim

Preguntes com «Què explica la secció X?» obliguen l'usuari a tenir una fitxa oberta. Preguntes com «Què indica aquesta fila?» no diuen quina dada interessa. Respostes com «I dos topònims que en surten» són fragments, no respostes. Aquests formats entrenen a parlar del document, no a ajudar una persona.

Per tant, cada conversa parteix d'una necessitat que es reconeix en la vida normal: entendre una dada, comprovar una afirmació, aclarir una diferència, prendre una decisió o saber què es pot concloure. La font s'usa per verificar; no es converteix en l'escenari de la conversa.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── examples/
│   │   ├── conversations.jsonl   # calibratge editorial, no entrenament
│   │   └── provenance.jsonl      # fonts i notes de revisió dels exemples
│   ├── review/                   # converses candidates i procedència per revisar
│   ├── work/                     # inventaris i cobertura per construir
│   ├── reports/                  # qualitat, exclusions i cobertura
│   ├── scripts/                  # eines de lectura, validació i exportació
│   └── output/                   # exports revisats, quan n'hi hagi
└── language/
    ├── README.md
    ├── examples/                 # només exemples de format, mai parla inventada
    ├── review/                   # fragments humans candidats i procedència
    ├── work/                     # elegibilitat i verificació de transcripcions
    ├── reports/
    ├── scripts/
    └── output/
```

## Com escriure converses Knowledge

1. **Defineix què vol resoldre la persona** en una frase concreta. Exemples: «vol saber si la comparació demostra una tendència» o «vol distingir persones inscrites de visites». Si la intenció no es pot explicar així, no escriguis encara la pregunta.
2. **Verifica els fets i els drets** a les fonts del corpus. No facis servir com a entrenable una font amb drets pendents. Anota cada font i llicència a `provenance.jsonl`, fora dels missatges.
3. **Escriu primer el fil de preguntes de l'usuari.** La primera pregunta s'entén sense cap document obert. Cada seguiment neix d'una resposta anterior i demana el pas següent que una persona podria voler aclarir.
4. **Redacta respostes que ajudin.** Comença contestant. Després dona el context imprescindible i, si escau, explica què no permet concloure la informació.
5. **Llegeix el diàleg només des del costat de l'usuari.** Si sembla un qüestionari, un índex o una visita guiada per una fitxa, reescriu-lo.
6. **Revisa cada afirmació contra les fonts.** No omplis buits amb coneixement extern ni facis passar una hipòtesi, una tradició o una correlació per fet comprovat.

### Forma de les converses

- Objectiu habitual: **2–4 intercanvis** (una pregunta i una resposta), amb seguiments genuïns. No afegeixis torns per complir una quota.
- Un exemple d'un sol intercanvi només s'accepta quan el dubte queda resolt del tot i un seguiment sonaria artificial.
- Els seguiments poden dir «i això?», «però...» o «llavors...», si el referent és clar per la conversa.
- No cal que tots els fils comencin amb «Què és...?» ni que cada resposta repeteixi el títol del tema.
- No inventis vivències, opinions o identitats de l'usuari per fer el diàleg més col·loquial.
- No escriguis cites, IDs interns, títols de secció ni notes de procedència dins la conversa, tret que la persona pregunti explícitament per la font.

### Porta de qualitat

Un exemple només es pot aprovar si totes les respostes són «sí»:

- La pregunta inicial expressa una necessitat humana i s'entén per si sola?
- Els seguiments són reaccions plausibles a la resposta anterior?
- Cada resposta contesta primer el que s'ha preguntat?
- La resposta és natural en veu alta i prou completa per ser útil?
- Tots els fets, xifres i matisos estan sostinguts per fonts elegibles?
- La resposta distingeix dades, interpretacions, tradició i incertesa?
- L'exemple aporta un patró útil i no és gairebé duplicat d'un altre?
- La procedència i els drets estan registrats i són compatibles amb l'ús previst?

Un sol «no» implica reescriure, deixar pendent o excloure.

## Construcció de Maia Knowledge

- Inspeccionar totes les fitxes elegibles de `docs/temes/`, amb seccions, llistes, taules, cronologies, relacions i incerteses.
- Convertir les unitats rellevants en converses motivades per preguntes reals; una conversa pot connectar fitxes si cada relació està documentada.
- Mantenir evidència i cobertura a `work/` i `reports/`; no carregar aquestes metadades a `messages`.
- Deduplicar i separar train, validation i test per tema/font o grup relacionat. No repartir paràfrasis d'una mateixa resposta entre conjunts.
- Crear exports només amb registres aprovats editorialment, factualment i quant als drets.

## Construcció de Maia Language

- Inspeccionar `docs/parla/` i incloure només material que compleixi els criteris del corpus: `veu: originaria`, `epoca: contemporania` i `apte_llengua: true`, amb drets compatibles i transcripció verificada.
- Preservar les paraules humanes i fer només normalitzacions mínimes documentades. No inventar respostes «com si fossin andorranes».
- Mantenir junts els fragments d'una mateixa peça, conversa o parlant en separar train, validation i test.
- No començar exports si no hi ha prou material verificat. Un conjunt buit és millor que parla fabricada.

## Etapes

1. Aprovar la guia i calibrar l'estil amb els exemples d'aquesta carpeta.
2. Crear i validar el lector estructural de `docs/temes/` i l'inventari de cobertura.
3. Definir el registre intern de procedència i la validació del format.
4. Inventariar Knowledge i Language separadament, registrant drets i buits.
5. Escriure i revisar converses Knowledge per necessitat, amb cobertura traçable.
6. Verificar transcripcions i extreure fragments Language humans elegibles.
7. Revisar, deduplicar, agrupar i separar els conjunts.
8. Generar exports i informes; comprovar-los abans de considerar cap dataset acabat.

## Definició de fet

**Knowledge** no està acabat fins que totes les fitxes elegibles s'han inspeccionat, el coneixement útil està cobert, els exemples són naturals i correctes, els drets són clars, i els exports i informes passen validació.

**Language** no està acabat fins que totes les peces elegibles s'han inspeccionat, la parla i els drets s'han verificat, no hi ha fragments incerts utilitzats com a model, els conjunts eviten filtracions i els exports passen validació.
