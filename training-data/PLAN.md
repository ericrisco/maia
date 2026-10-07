# Pla de treball de Maia Training Data

## Objectiu

Preparar dos datasets separats: **Maia Knowledge**, amb respostes correctes
sobre Andorra, i **Maia Language**, basat només en llengua humana autèntica.
La prioritat ara és acordar què sona com una conversa útil. Encara no toca
produir registres en volum.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── review/
│   │   ├── EXEMPLES.md          # mostres editorials, no són dades d'entrenament
│   │   ├── CONVERSATION-GUIDE.md
│   │   ├── conversations.jsonl  # només converses aprovades
│   │   └── provenance.jsonl     # font i revisió, fora de l'export
│   ├── work/                    # inventari i cobertura
│   ├── scripts/
│   ├── output/                  # exports quan n'hi hagi prou
│   └── reports/
└── language/
    ├── README.md
    ├── review/
    ├── work/
    ├── output/
    └── reports/
```

## Com decidim si una conversa val la pena

1. Tria una necessitat recognoscible: planificar una visita, entendre una
   tradició, aclarir una diferència, comprovar una afirmació o saber què se sap.
2. Escriu la pregunta com la diria algú que no té la fitxa al davant. No preguntis
   per seccions, files, gràfics ni pel corpus.
3. Respon primer el dubte. Afegeix només el context necessari per no induir a
   error.
4. Afegeix un seguiment només si neix del que acaba de dir Maia. Una conversa
   d'un sol intercanvi és vàlida.
5. Contrasta cada afirmació amb les fonts i conserva els matisos: data, lloc,
   incertesa, llegenda o desacord.
6. Rebutja la conversa si la pregunta només serveix per buidar una fitxa, si
   repeteix una altra amb sinònims o si la resposta sona a camps d'una taula.

No hi ha una quota de preguntes per document. Una fitxa pot donar una conversa,
unes quantes o cap. La cobertura es mesura pel coneixement útil que queda
representat, no pel nombre de preguntes.

## Revisió abans d'afegir un registre

- La pregunta té sentit sense veure cap document.
- Es podria imaginar una persona fent-la en aquella situació.
- La resposta contesta de seguida i no afegeix una explicació de farciment.
- Cada torn posterior reprèn clarament el fil.
- No es presenta una llegenda, interpretació o hipòtesi com un fet verificat.
- La procedència i els drets consten a `provenance.jsonl`.
- El registre no duplica una conversa existent.

Les mostres de `knowledge/review/EXEMPLES.md` fixen el to. No s'han de copiar
com a plantilles.

## Registre i separació dels datasets

Una conversa aprovada ocupa una línia de `knowledge/review/conversations.jsonl`
i només conté `messages` amb rols `user` i `assistant`. La font, la llicència,
la revisió i els avisos de drets queden a `provenance.jsonl`, mai al text que
aprèn el model. Els valors `no` i `pendent` s'han de mostrar com a avisos segons
`docs/CONTRACT.md`; no es canvien ni s'amaguen.

Maia Language segueix un procés separat. Només pot conservar parla humana
elegible de `docs/parla/`; no es creen preguntes fictícies per convertir
monòlegs en diàlegs.

## Etapes

1. Validar aquestes mostres amb l'usuari.
2. Afegir converses Knowledge una a una i revisar-les abans d'aprovar-les.
3. Reprendre l'inventari exhaustiu i informar què queda cobert i què no genera
   una pregunta natural.
4. Auditar Maia Language sense fabricar material lingüístic.
5. Deduplicar, separar train/validation/test per font o conversa i validar els
   exports quan hi hagi volum suficient.

No començar l'etapa següent si l'anterior encara no té criteri i evidència clars.
