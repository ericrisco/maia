# Mostres de conversa

`examples.jsonl` fixa el to i el tipus de seguiment que busquem. No són dades aprovades per entrenar ni es compten com a cobertura.

Les mostres provenen de [`el-trinxat.md`](../../../docs/temes/gastronomia/plats/el-trinxat.md) i [`madriu-perafita-claror.md`](../../../docs/temes/territori/patrimoni-natural/madriu-perafita-claror.md). Totes dues fitxes declaren la Viquipèdia en català com a font; la fitxa de la font indica CC BY-SA 4.0 i permet redistribució amb atribució i compartir igual. Si aquests exemples s'incorporessin a un export, caldria conservar aquestes condicions.

## Què mostren

- La pregunta sona com un dubte sobre el tema, no com una petició de resum d'una fitxa.
- La resposta inicial resol el dubte i no presumeix més del que diu la font.
- El seguiment surt del que s'acaba d'explicar i demana un detall nou.
- La resposta al seguiment continua la conversa sense repetir-la sencera.
- Si una persona dona context, és breu i serveix per entendre la pregunta; no fem veure que coneixem la seva vida.

## Exemple que descartem

```text
Usuari: Què explica la secció «El nom» de la fitxa del trinxat?
Assistent: El nom.
Usuari: I què més diu?
Assistent: Col i patata.
```

Depèn d'un document absent, no contesta de manera útil i el seguiment només demana més fragments.
