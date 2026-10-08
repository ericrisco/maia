# Pla de Maia Training Data

## Objectiu

Preparar dos conjunts independents a partir de `docs/`:

- **Maia Knowledge** ensenya coneixement documentat sobre Andorra a partir de `docs/temes/`.
- **Maia Language** conserva llengua produïda per persones a partir de `docs/parla/`; no s'hi inventen converses ni s'hi reescriu la veu humana.

Ara fem només l'estructura i un petit pilot de calibratge. Les converses antigues de `knowledge/review/` continuen sent candidates sense aprovar: no s'exporten i no compten com a exemples bons fins que es revisin.

## Com ha de sonar Maia Knowledge

Escriu primer el dubte que tindria una persona, no una pregunta sobre com està organitzat el material. La persona no ha de saber que existeix una fitxa, una secció, una taula o una base de dades.

Una conversa ha de tenir un fil recognoscible:

1. La primera pregunta planteja una curiositat real i amb prou context.
2. La primera resposta la resol directament, amb els matisos necessaris.
3. La repregunta surt d'alguna cosa que s'acaba de dir i demana aclariment, conseqüència o límit.
4. La segona resposta afegeix una comprensió útil. No repeteix la primera ni allarga el diàleg per quota.

Per defecte, el pilot té dos torns d'usuari. Afegim més torns només quan la conversa realment els necessita. Una conversa d'un sol torn pot ser útil per al dataset final; no la convertim artificialment en multitorn.

La persona pot parlar de manera espontània —«Però llavors…», «Això vol dir que…?»— però no amb anècdotes inventades ni col·loquialismes forçats. Les preguntes poden tenir context implícit si el diàleg ja l'ha establert; cada resposta ha de continuar sent clara en aquell diàleg.

## Què rebutgem

- «Què explica la secció…?», «Què indica aquesta fila?» o «Què diu la fitxa…?»
- Preguntes que només demanen extreure una llista o repetir un encapçalament.
- Seguiments genèrics com «I què més?» sense un dubte concret.
- Respostes telegràfiques, fragments, notes de recerca o llistes enganxades sense explicar-ne el sentit.
- Preguntes que amaguen la resposta inicial per reservar-la per al torn següent.
- Afirmacions més segures que la font; convertir una llegenda en fet, una coincidència en causa o una absència de prova en prova negativa.
- Repetir la mateixa plantilla de pregunta amb noms o dates canviats.

## Procediment per a cada conversa

1. Llegeix la fitxa sencera i les fonts enllaçades necessàries.
2. Escriu per a ús intern una frase d'intenció: quin dubte humà resol el diàleg?
3. Redacta només la informació necessària per respondre aquest dubte.
4. Comprova si la repregunta neix de la resposta i afegeix valor. Si no, no la forcis.
5. Llegeix el diàleg sense mirar la font. Si sona a qüestionari, reescriu-lo.
6. Torna a la font i verifica cada afirmació, nom, data, quantitat i matís.
7. Registra per separat procedència, drets i cobertura. La conversa de cara a l'usuari no porta IDs, camps ni llenguatge del pipeline.
8. Mantén qualsevol dubte legal o factual en revisió. Una conversa no s'exporta fins que contingut, procedència i ús estiguin aprovats.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── examples/       # pilot de calibratge; no s'exporta
│   ├── review/         # candidates pendents de revisió
│   ├── work/           # cobertura i material de treball
│   ├── output/         # només splits aprovats
│   └── reports/        # cobertura, qualitat, drets i exclusions
├── language/
│   ├── README.md
│   ├── review/          # fragments humans per verificar
│   ├── work/            # inventari, procedència i decisions
│   ├── output/          # només material autoritzat i verificat
│   └── reports/
└── scripts/             # validació i generació, quan el format estigui acordat
```

`output/` no és un abocador de proves: només conté material que ja ha passat revisió. Exemples, candidates, procedència i informes són fitxers separats. El format conversacional exportat és JSONL, una conversa per línia, amb només `messages` i missatges `user`/`assistant`.

## Ordre de treball

1. Aprovar el criteri amb els exemples de `knowledge/examples/`.
2. Decidir si les candidates antigues de `knowledge/review/` es reescriuen o es descarten; cap no s'accepta per inèrcia.
3. Recórrer exhaustivament `docs/temes/`, marcant cada fitxa coberta, exclosa amb motiu o pendent.
4. Crear converses Knowledge petites i revisables, vinculant cada conversa a les afirmacions, documents, fonts i llicències corresponents.
5. Auditar `docs/parla/` peça per peça: parlant, procedència, fidelitat de transcripció, incerteses i drets.
6. Només quan hi hagi prou material aprovat, deduplicar, separar per grups sense filtracions i generar splits.
7. Validar converses, cobertura, drets, splits i informes abans de publicar els exports.

Cada conversa nova és un pas petit amb registre, traçabilitat, validació i commit independent. No hi ha una quota de registres: prioritzem correcció, cobertura útil i naturalitat per damunt del volum.

## Criteri d'acceptació d'un diàleg

- Una persona podria fer la pregunta sense haver llegit el document.
- La resposta contesta el que s'ha preguntat i inclou prou context per entendre-la.
- La repregunta té un motiu recognoscible i continua el mateix fil.
- Cap resposta no és un fragment, una etiqueta o una nota interna.
- Cada afirmació es pot sostenir amb les fonts registrades.
- La conversa és clara en veu alta i no sembla una plantilla.
- Procedència i drets permeten l'ús previst abans d'exportar-la.

## Maia Language

Knowledge i Language no es barregen. Per Language només s'utilitza text humà verificat i amb drets compatibles. Es preserven lèxic, sintaxi i veu; no es demana a un model que imiti un parlant ni s'inventa la pregunta que faltaria en un monòleg. Les unitats i els splits s'agrupen per peça, conversa i parlant per evitar filtracions.

## Quan es pot dir que està acabat

Knowledge no està complet fins que cada fitxer de `docs/temes/` té una decisió traçable, el coneixement entrenable està cobert, els drets permeten l'ús, els splits no tenen filtracions i els informes passen validació.

Language no està complet fins que cada peça de `docs/parla/` té una decisió, el material inclòs és humà, verificat i reutilitzable, i els splits i informes passen validació.
