# Pla per crear converses de Maia

## Objectiu

Preparar converses que ensenyin a Maia a respondre preguntes reals sobre
Andorra. Cada conversa ha de començar amb un dubte que una persona podria
escriure en un xat. Els seguiments han de continuar el mateix fil.

El dataset no és un qüestionari del corpus. La cobertura dels fets es controla
en un inventari separat. Un fet només genera una conversa quan dona peu a una
resposta útil i natural.

## Estructura

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── review/
│   │   ├── CONVERSATION-GUIDE.md  # criteris editorials i exemples
│   │   ├── conversations.jsonl    # converses candidates, una per línia
│   │   └── provenance.jsonl       # fonts i estat dels drets
│   ├── work/                      # inventari i seguiment de cobertura
│   ├── output/                    # exportacions per entrenar
│   └── reports/                   # cobertura i validació
└── language/                      # flux separat, basat en parla autèntica
```

No esborrem `work/`, `provenance.jsonl` ni els informes quan refem les
converses. Aquests fitxers conserven la cobertura revisada i la traçabilitat de
les fonts. Les converses rebutjades es treuen de l'exportació; el motiu queda
anotat a la revisió.

## Procés editorial

1. Llegeix tota la peça i les fonts necessàries. Separa fets, incerteses,
   discrepàncies i drets d'ús.
2. Escriu en una frase el dubte humà que la peça pot resoldre. Si només pots
   formular-lo com «què diu la fitxa/secció/gràfic?», encara no hi ha una bona
   conversa.
3. Redacta una pregunta inicial que s'entengui sense haver vist el corpus.
   Afegeix context només si una persona el necessitaria per fer la pregunta.
4. Escriu una resposta directa i natural. No enumeris tots els fets de la peça.
   Situa les normes històriques en el temps i marca les llegendes com a relats.
5. Afegeix un seguiment només quan neixi de la resposta anterior. Pot aclarir
   un terme, preguntar per una conseqüència o comprovar una implicació.
6. Llegeix el diàleg sense mirar la font. Comprova que sona com un xat i que
   cada torn respon al torn anterior.
7. Contrasta després cada afirmació amb les fonts. Registra la procedència i
   els límits de reutilització.
8. Rebutja o reescriu qualsevol conversa que no passi tots els criteris.

## Criteris obligatoris

Una conversa només s'aprova si compleix tots aquests punts:

- **Dubte real:** la primera pregunta demana ajuda, explicació o aclariment
  sobre una situació o idea concreta.
- **Autònoma:** s'entén sense títols de fitxa, números de fila, seccions ni
  context ocult.
- **Natural:** no sembla un examen ni una petició de resum escolar.
- **Continuïtat:** cada seguiment reprèn una cosa que Maia acaba d'explicar.
- **Resposta útil:** Maia contesta primer i afegeix només el context necessari.
- **Fidelitat:** cada afirmació es pot justificar amb una font revisada.
- **Límits clars:** la resposta conserva incerteses, discrepàncies i el període
  històric quan són rellevants.
- **No duplicada:** no repeteix una conversa existent canviant-hi els noms.
- **Traçable:** té una entrada de procedència corresponent.

Si una pregunta falla el criteri de naturalitat, no es corregeix només canviant
«què explica» per «em pots explicar». Es torna a identificar el dubte de la
persona i es redacta de nou des d'allà.

## Converses multitorn

- Normalment, dos o tres intercanvis són suficients.
- Cada torn de l'usuari ha de tenir sentit com a rèplica a la resposta anterior.
- L'usuari no pot preguntar per un detall que Maia encara no ha esmentat.
- No s'encadenen preguntes independents per extreure una llista de dades.
- Si canvia el tema o la intenció, es crea una conversa nova.
- No s'inventa cap experiència personal per fer que la pregunta sembli humana.
- Una pregunta d'una sola resposta és preferible a una conversa allargada sense
  motiu.

## Cobertura

La cobertura és una auditoria del coneixement, no una quota de preguntes.
L'inventari registra quines parts de cada document s'han revisat, quines tenen
una conversa aprovada i quines no en necessiten cap. No s'inventa una pregunta
per cobrir una data, una fila o un nom aïllat.

Les converses sobre més d'una peça només s'escriuen quan una persona podria
necessitar aquella connexió per resoldre el seu dubte. Els fets relacionats es
guarden al mateix grup de split per evitar filtracions entre train, validation
i test.

## Flux de cada registre

1. Revisar una conversa candidata i la seva procedència.
2. Reescriure-la o rebutjar-la si falla un criteri.
3. Validar l'estructura i l'enllaç de procedència.
4. Actualitzar l'inventari de cobertura i l'informe.
5. Exportar només registres aprovats.
6. Revisar el diff i registrar el canvi segons el flux de Git del projecte.

## Maia Language

Maia Language continua separat. Només usa parla contemporània autèntica amb
transcripció prou fiable i drets anotats. No s'inventen preguntes per fer que
un fragment sembli una conversa. La resposta preserva les paraules de la
persona entrevistada.

## Quan es considera acabat

Knowledge només es dona per acabat quan s'ha revisat tot `docs/temes/`, les
converses aprovades són correctes i naturals, la cobertura està auditada, no hi
ha duplicats i els splits són vàlids.

Language només es dona per acabat quan s'han revisat totes les peces elegibles
de `docs/parla/`, s'han filtrat els fragments incerts i s'ha evitat barrejar
fragments relacionats entre splits.
