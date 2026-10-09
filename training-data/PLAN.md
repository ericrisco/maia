# Pla de Maia Training Data

## Problema que corregim

Les preguntes anteriors sovint partien de la forma de la fitxa: demanaven què deia una secció, una fila o un gràfic. Algunes respostes eren fragments. Alguns diàlegs afegien torns només per cobrir més fets.

Això entrena el model a respondre consultes sobre documents interns. No l'entrena a ajudar una persona amb un dubte real.

## Criteri per a Knowledge

1. **Comença pel dubte, no pel document.** Formula què voldria saber una persona sense haver vist la fitxa.
2. **Dona context mínim.** La pregunta ha de deixar clar de quin tema o lloc parla, sense títols de secció, files ni identificadors.
3. **Resol el dubte a la primera frase.** Després afegeix només el context que evita una resposta confusa.
4. **Fes seguiment només quan el fil el provoqui.** Cada torn ha de preguntar una cosa nova que una persona podria voler saber després de la resposta anterior.
5. **Construeix un fil multitorn quan la font ho permeti.** Cada seguiment ha de sorgir de la resposta anterior i demanar informació nova. Si forçar-lo faria la conversa menys natural o menys exacta, no inventis un torn.
6. **No inventis vivències ni premisses.** No atribueixis records, visites o opinions a qui pregunta. Corregeix una premissa errònia amb tacte.
7. **Separa fet i interpretació.** Identifica llegendes, lectures d'autors, desacords entre fonts i informació que no consta.
8. **Llegeix només els missatges en veu alta.** Si semblen un examen o una instrucció de cerca, reescriu-los.
9. **Verifica cada afirmació.** Guarda les fonts i els drets a la procedència, mai dins dels missatges.

## Com escriure un registre

- Desa les mostres de calibratge a `knowledge/examples/` i els candidats nous a `knowledge/review/`.
- Escriu la procedència en un fitxer separat amb el mateix `example_id`.
- La conversa conté només `messages` amb rols `user` i `assistant`.
- La procedència registra fitxers font, necessitat humana, motiu dels seguiments, afirmacions comprovades i estat de drets.
- Marca totes les mostres `exportable: false`. No les copiïs a `output/`.

## Seqüència de treball

1. Revisar les mostres i aplicar la guia de `knowledge/review/EXEMPLES.md`.
2. Afegir registres de Knowledge tema a tema. Cada registre nou passa revisió de naturalitat, exactitud, duplicats i drets abans d'entrar als splits.
3. Revisar Language per peça i font. Només s'hi incorporen fragments autèntics amb permisos i transcripció prou fiables; no se'n generen diàlegs sintètics.
4. Quan hi hagi registres revisats suficients, crear generació, validació, deduplicació i splits. No generar fitxers d'entrenament buits ni mesurar progrés pel nombre de registres.

## Arbre

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── examples/       # exemples interns, no exportables
│   ├── review/         # converses candidates revisades
│   ├── work/           # evidència i cobertura
│   ├── reports/        # informes
│   ├── scripts/        # eines futures
│   └── output/         # només exports aprovats
└── language/
    ├── README.md
    ├── examples/
    ├── review/
    ├── work/
    ├── reports/
    ├── scripts/
    └── output/
```
