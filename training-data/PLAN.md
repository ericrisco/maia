# Pla de Maia Training Data

## Objectiu

Preparar dos conjunts separats a partir de `docs/`:

- **Maia Knowledge** respon dubtes reals sobre Andorra amb informació del corpus.
- **Maia Language** conserva català andorrà contemporani de parlants humans.

La prioritat és que una persona reconegui el diàleg com una conversa que podria tenir. No convertim títols, apartats, cel·les o paràgrafs en preguntes automàtiques.

## Com escriure Maia Knowledge

1. Llegeix la fitxa sencera i les fonts que sostenen la resposta.
2. Comença pel dubte humà: què necessita aclarir la persona, i per què ho preguntaria?
3. Escriu la resposta directa. Afegeix només el context necessari perquè s'entengui.
4. Afegeix un seguiment si la resposta desperta una pregunta concreta i diferent.
5. Comprova cada afirmació contra la font. Marca clarament els límits, les dates i la incertesa.
6. Llegeix el diàleg sencer en veu alta. Si sembla una consulta d'examen o una visita guiada per la fitxa, reescriu-lo o descarta'l.
7. Desa només els missatges al JSONL. Desa fonts, evidència, drets i estat en el fitxer de procedència.

### Regles editorials

- La pregunta ha de funcionar per a algú que no ha vist el document.
- No esmentis fitxes, apartats, files, gràfics, corpus ni «la informació que has trobat».
- No inventis una biografia o situació personal per fer entrar una dada.
- No forcis una segona pregunta. Un intercanvi curt és complet si el dubte queda resolt.
- El seguiment ha de néixer del que s'acaba de dir i demanar alguna cosa nova.
- No afirmis causes quan la font només mostra una coincidència o una evolució.
- Quan les dades siguin mitjanes, estimacions o d'una data concreta, digues-ho.
- Una resposta pot dir que el corpus no ho permet saber. No omplir buits amb intuïcions.
- No cal cobrir cada xifra amb una pregunta pròpia. Agrupa dades només quan una persona les relacionaria.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── scripts/          # ordres comunes i validació final
├── knowledge/
│   ├── scripts/      # inventari, cobertura i validació Knowledge
│   ├── review/       # converses candidates, mostres i procedència
│   ├── work/         # inventari i evidència de cobertura
│   ├── reports/      # qualitat, cobertura, exclusions i drets
│   └── output/       # només registres revisats i aptes per a l'ús previst
└── language/
    ├── scripts/      # extracció i validació Language
    ├── review/       # fragments humans candidats i procedència
    ├── work/         # elegibilitat i selecció
    ├── reports/      # material inclòs i exclòs
    └── output/       # només registres revisats i aptes per a l'ús previst
```

Les mostres actuals de Knowledge són editorials i encara no estan aprovades. Els registres anteriors s'han mogut a `knowledge/review/quarantine/`; no entren als lots nous sense tornar-los a revisar. Els directoris `output/` romanen buits fins que hi hagi aprovació de contingut i drets.

## Maia Language

Només utilitza material de `docs/parla/` que compleixi `docs/CONTRACT.md`: veu originària, contemporània, apta per a llengua, transcripció prou fiable i drets compatibles. No inventis torns de conversa a partir de monòlegs. Conserva les paraules humanes tant com sigui possible.

## Cobertura i publicació

Per Knowledge, revisa el coneixement útil de totes les fitxes de `docs/temes/`: fets, context, noms, dates, xifres, relacions i límits. Comprova la cobertura per contingut, no per nombre de preguntes.

Abans d'exportar qualsevol conjunt: revisa naturalitat i fidelitat, resol drets, elimina duplicats, agrupa converses relacionades abans de separar `train`, `validation` i `test`, valida el JSONL i publica un report de cobertura i exclusions. No divideixis variants d'una mateixa conversa entre splits.

## Fase actual

Primer acordarem si les dues mostres de `knowledge/review/conversations.jsonl` sonen humanes i útils. Després corregirem la pauta amb el feedback rebut. Només llavors reprendrem l'elaboració de registres, tema a tema i conversa a conversa. No hi ha quota de volum.
