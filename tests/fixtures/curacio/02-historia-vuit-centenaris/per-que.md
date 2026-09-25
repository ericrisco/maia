# Exemple 2 — Article amb cites, conjectura i buits amb estats

**El cas difícil.** El text barreja fets, interpretació, el corpus parlant de si
mateix, una taula que el mateix text declara conjectura, i buits ratllats amb
estats diferents.

| Què hi ha a l'entrada | Què se'n fa | Regla |
| --- | --- | --- |
| `([font](../../../fonts/…))` al final d'una frase | S'elimina **amb el parèntesi** | Parèntesi que només conté un enllaç a `fonts/` o a un altre article = cita de navegació. La font ja és al frontmatter. |
| `([política](../../politica/…))` | S'elimina amb el parèntesi | Mateixa regla: parèntesi amb un sol enllaç. |
| `la [Nova Reforma](../segle-xix/nova-reforma.md)` dins la frase | `la Nova Reforma` | Enllaç dins la prosa → text de l'àncora. |
| Blockquote `> «entre el **2016**…»` en català | Paràgraf normal, **amb les cometes «»** | Cita en català: es manté dins del chunk, atribuïda pel text que la precedeix. Només les cites en una altra llengua es marquen `cita`. |
| «**El corpus no té la llista dels vuit.** …» | `nota-treball`, excloure | Paràgraf que té **«el corpus»** (o «aquest corpus») com a subjecte: parla del procés, no d'Andorra. |
| «**El que sí que pot fer és enumerar**… i marcar quins són conjectura seva:» | `nota-treball`, excloure | El subjecte implícit és el corpus. |
| La taula d'efemèrides | **`pendent`**, fora dels chunks | El text que l'envolta diu «conjectura», «no quadra» i les cel·les diuen «dubtós». Taula amb aquests senyals al paràgraf anterior o posterior → `pendent` per a revisió humana. No s'entrena una conjectura com a fet. |
| «El que sí que se sosté és la proporció, perquè la font la dona: sis dels vuit…» | **Cos, es manté** | Mateixa secció que la conjectura, però és un fet que la font dona. Per això la classificació és per paràgraf, no per secció. |
| «El corpus reté aquesta frase com el que és…» | `nota-treball`, excloure | «El corpus» com a subjecte. |
| Encapçalament «La lectura que el corpus n'extreu» | Es manté com a `seccio` | La regla de «el corpus» s'aplica als paràgrafs, no als encapçalaments. El contingut de la secció és cos. |
| «entre el 2016 i el 2020», «el que avui és Andorra», «el síndic general en exercici», «consellers generals en actiu» | `#b1` 0.3 · `#b2` 0.4 · `#b8` 0.4 → `#c1` 0.4, `#c2` 0.4 → tots dos continuen sent `coneixement` | Any ≥ 2020 suma 0.3; «avui» suma 0.4; «en exercici» i «en actiu» són **el mateix senyal** i compten una vegada. El chunk pren el màxim dels seus blocs. Tot queda per sota de 0.5. Fixa't que «avui» aquí és retòric: la regla és sorollosa però determinista, i per això el llindar és 0.5 i no 0.4. |
| 80 + 91 + 23 paraules, i després una secció de 132 | Dos chunks: `#c1` (194) i `#c2` (132) | Afegir la secció de 132 a `#c1` passaria de 300 → tall a la frontera de secció. L'últim chunk pot quedar sota 150. |

## Els buits ratllats: l'estat decideix

| Ítem | Estat | Què se'n fa |
| --- | --- | --- |
| 1. L'article de Pol que enumera els vuit | `parcial` | A `buits/`, **amb la troballa parcial** (sense la data d'auditoria ni els enllaços): la pregunta «quins són els vuit?» continua sense resposta. |
| 2. El programa oficial del 600 aniversari | `font_externa` | A `buits/`, només la pregunta. La frase fixa «cal consultar fonts, registres o observació que el corpus no conserva» s'elimina: és plantilla. |
| 3. Què es va publicar a cada efemèride | `font_externa` | Igual. |
| 4. Si hi ha hagut més commemoracions des del 2020 | `font_externa` | Igual. |

Estats que **no** van a `buits/` (vegeu l'exemple 3): `resolt` (la resposta ja és al
text) i `no-es-buit` (plantilla o limitació, no pregunta).
