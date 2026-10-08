# Pla de treball: Maia Training Data

## Objectiu d'aquesta etapa

Reiniciar l'edició de Knowledge amb un estàndard de conversa clar. Ara només hi ha d'haver una estructura mínima i unes poques mostres per calibrar el to. Les mostres no són dades d'entrenament. No reprendre la producció en volum fins que l'estil de les preguntes i les respostes estigui validat.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── review/
│   │   ├── EXEMPLES.md
│   │   ├── conversations.jsonl  # només mostres de calibratge, de moment
│   │   └── provenance.jsonl     # fonts, drets i estat de cada mostra
│   ├── output/                  # buit fins que hi hagi prou dades revisades
│   └── reports/                 # cobertura i qualitat, més endavant
└── language/
    ├── README.md
    ├── review/                  # corpus humà elegible, pendent de revisió
    ├── output/                  # separat de Knowledge
    └── reports/
```

Knowledge ensenya a respondre preguntes documentades sobre Andorra. Language conserva trets de parla humana andorrana contemporània. No es barregen.

## Estàndard d'una conversa

Una conversa parteix d'un dubte que algú podria tenir sense haver obert una fitxa. Pot ser una confusió, una dada que no quadra, una decisió pràctica o una curiositat que surt del torn anterior.

- La primera pregunta s'entén sola. No diu «què explica la secció», «segons la fitxa» ni «què indica aquesta fila».
- No cal inventar una biografia per fer-la versemblant. Es poden fer preguntes directes: «Quina diferència hi ha entre la Passa i la Marratxa? Sempre les confonc.»
- Cada conversa segueix un fil. La persona rep una resposta i pregunta una cosa que realment se'n desprèn.
- No s'afegeixen torns per arribar a una llargada fixa. Si no hi ha un seguiment útil, la conversa s'acaba.
- La resposta comença pel que resol el dubte. Després afegeix el context necessari, amb llenguatge normal i precís.
- Si la font no ho resol, es diu què se sap i què queda obert. No s'omple el buit amb una explicació plausible.
- Les fonts, drets, afirmacions i notes de revisió van a `provenance.jsonl`, mai als missatges d'entrenament.

### Pregunta de control

Llegida sense metadades, la conversa sembla una persona aclarint un dubte real? Si sembla un examen, una consulta a una base de dades o un resum de document, es reescriu o es descarta.

## Fases

1. **Calibratge.** Mantenir unes poques mostres curtes i variades a `knowledge/review/conversations.jsonl`. Revisar-les llegint només els missatges.
2. **Aprovació de l'estil.** Ajustar les mostres fins que preguntes, seguiments i respostes sonin naturals i siguin exactes. Encara no crear lots.
3. **Preparació de fonts.** Per cada conversa nova, comprovar el document original, les afirmacions que sosté i les condicions de reutilització. Registrar-ho abans d'afegir-la.
4. **Redacció i revisió.** Escriure una conversa per necessitat humana; comprovar continuïtat, exactitud, límits, naturalitat i duplicats.
5. **Cobertura.** Quan l'estil estigui fixat, avançar pel corpus de manera sistemàtica i registrar què s'ha cobert i què s'exclou.
6. **Exportació.** Només després de revisar cobertura, drets i duplicats, preparar train/validation/test. Separar per font o tema abans de fer variants per evitar contaminació entre splits.
7. **Maia Language.** Tractar-la després i per separat. Incloure només parla humana contemporània elegible, amb drets i transcripció revisats; no inventar respostes per imitar un dialecte.

## Criteri per passar del calibratge a la producció

- Les mostres passen la pregunta de control.
- Les primeres preguntes no depenen del títol ni del contingut d'una pàgina.
- Els seguiments continuen el fil i no repeteixen dades.
- Les respostes corregeixen errors amb tacte i no sonen telegràfiques.
- Cada afirmació factual té font i condicions d'ús registrades.
- Els dubtes i desacords de les fonts es representen sense resoldre'ls artificialment.

Fins que es compleixi aquest criteri, `output/` queda buit i les mostres continuen marcades com a editorials.
