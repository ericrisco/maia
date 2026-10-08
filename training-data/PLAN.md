# Pla de Maia Training Data

## Què va fallar

Les preguntes del primer intent semblaven consignes d'un examen: demanaven què deia una secció o una fitxa i assumien que qui preguntava tenia el document al davant. Les respostes sovint començaven a mitja idea. Això ensenya a completar fragments, no a conversar.

## Objectiu

Crear converses que podrien començar en una conversa real: algú ha vist una dada, ha sentit una explicació, prepara una visita o vol aclarir una confusió. L'usuari no ha de conèixer el títol de cap document.

Cada conversa pot tenir un o més intercanvis. No hi ha una llargada obligatòria. Un seguiment només s'afegeix si sorgeix de la resposta anterior i resol una curiositat nova.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── review/
│   │   ├── conversations.jsonl   # mostres i candidates; no són exportació
│   │   └── provenance.jsonl      # fonts, afirmacions i estat de revisió
│   ├── output/                   # train/validation/test, més endavant
│   └── reports/                  # cobertura i qualitat, més endavant
└── language/
    ├── README.md
    ├── review/                   # només fragments humans candidats autoritzats
    ├── output/                   # exportació futura, separada de Knowledge
    └── reports/
```

## Com es redacta una conversa

1. **Comença pel dubte humà.** Pot venir d'una confusió, una discrepància, una decisió pràctica o una observació concreta. No es pregunta «què explica la fitxa». Si la pregunta només es pot escriure després de llegir el títol intern, es descarta.
2. **Dona context suficient, sense inventar biografia.** Es pot dir «al programa de la festa hi surten dues coses...»; no s'inventa que l'usuari hi viu, hi ha anat o coneix algú.
3. **Contesta de seguida i amb llenguatge normal.** No comencis amb una etiqueta, un fragment ni «segons el corpus». Afegeix només el context que evita una resposta ambigua.
4. **Fes seguiments amb continuïtat.** El referent ha de ser clar i la curiositat ha de néixer del torn anterior. No afegeixis una pregunta només per allargar la conversa.
5. **Corregeix amb tacte.** Si la pregunta pressuposa una cosa falsa, corregeix-la directament i explica què sí que sabem.
6. **Marca els límits concrets.** Si les fonts discrepen o no resolen una qüestió, digues quina és la discrepància o què falta. No especulis per tancar la resposta.
7. **Revisa la conversa sense metadades.** Si sona a qüestionari, resum de fitxa o resposta telegràfica, reescriu-la o descarta-la.

## Criteri per aprovar

Una conversa passa a `reviewed` només si:

- cada afirmació es pot traçar a una font i les condicions de reutilització estan registrades;
- la primera pregunta és versemblant i s'entén per si sola;
- la resposta resol la pregunta abans d'afegir context;
- cada torn següent és coherent, útil i no repetitiu;
- les dates, xifres i incerteses coincideixen amb la font;
- la redacció no suggereix actualitat ni certesa que la font no dona;
- una persona editora la llegiria com una conversa útil.

Els identificadors, fonts, permisos i decisions editorials es guarden a `provenance.jsonl`, mai dins dels missatges d'entrenament.

## Fases

1. **Acordar l'estil:** llegir les mostres i ajustar-les amb l'usuari. Encara no crear registres en volum.
2. **Preparar candidates:** per a cada conversa, anotar font, fragments rellevants, drets, afirmacions i límits.
3. **Redactar i revisar:** escriure la conversa completa; revisar exactitud, naturalitat, continuïtat, drets i duplicats.
4. **Cobrir el corpus:** inventariar `docs/temes/` i representar el coneixement útil sense ometre unitats rellevants. Marcar exclusions i buits explícitament.
5. **Preparar Language per separat:** inspeccionar les peces elegibles de `docs/parla/`; incloure només parla humana contemporània amb drets i consentiment clars, àudio escoltat i transcripció revisada. No fabricar respostes.
6. **Exportar més endavant:** deduplicar i separar train/validation/test per font, tema, peça o parlant per evitar que variants gairebé idèntiques contaminin l'avaluació. No exportar fins que revisió i cobertura siguin suficients.

## Següent pas

Aplicar la guia `knowledge/review/EXEMPLES.md` a cada conversa i afegir registres de manera incremental, un per commit i push. Per cada registre, comprovar primer contingut i drets de la font; desar les afirmacions i la procedència a `knowledge/review/provenance.jsonl`. Després avançar tema a tema, sense ometre unitats del corpus. Els splits només vindran quan hi hagi cobertura i revisió suficients.
