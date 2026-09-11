<!-- GENERAT des de schema/corpus.toml. No l'editeu a mà: els canvis es perden i la comprovació falla amb R012. -->

# Contracte d'entrada del cervell andorrà

> Esquema v1.0.0 · arrel de la bóveda: `docs/`

Qualsevol document que entri al corpus compleix això. El que no ho compleix no
entra: la comprovació falla i us diu quin document i quin camp.

## La distinció que ho ordena tot

Un text **sobre** Andorra no és un text **en** andorrà. Per això cada document
declara dos fets independents, i l'aptitud com a model de llengua se'n **deriva**:

```
apte_llengua = veu == 'originaria' and epoca == 'contemporania'
```

Un document serveix com a model de llengua andorrana si i només si el text el va
produir algú parlant andorrà (veu originaria) i la llengua és d'avui (epoca
contemporania). Qualsevol altra combinació, no.

És una regla i no un criteri perquè no s'hagi de discutir document a document.
Conseqüència contraintuïtiva que val la pena recordar: **la revisió humana no
canvia la veu**. Un article compilat que algú revisa i corregeix és més fiable
com a coneixement i segueix sent compilat — el va escriure un agent.

## Valors tancats

- `veu` — `originaria` · `compilada`
- `epoca` — `contemporania` · `historica`
- `redistribucio` — `si` · `no` · `pendent`
- `type` — `article` · `parla` · `font`

## Camps d'un document de corpus

| Camp | Obligatori | Valors | Què hi va |
| --- | --- | --- | --- |
| `type` | **sí** | enum `type` | Tipus OKF. Obligatori i no buit. |
| `title` | **sí** | text lliure | Títol llegible. L'H1 del cos hi coincideix. |
| `description` | no | text lliure | Una frase de resum, per a previsualitzacions i cerca. |
| `tema` | **sí** | per forma | La branca on viu el document, en kebab-case i separada per barres. Es valida per FORMA, no contra una llista tancada: afegir una branca és crear un directori, no esmenar el contracte. La ruta del fitxer ha de correspondre a aquest valor. |
| `veu` | **sí** | enum `veu` | Qui va produir el text: originaria (verbatim andorrà) o compilada (redactat per un agent). |
| `epoca` | **sí** | enum `epoca` | De quan és la llengua: contemporania o historica. |
| `apte_llengua` | **sí** | `bool` | Derivat. Veure [derivation]. Es materialitza perquè les vistes .base d'Obsidian només filtren per frontmatter escrit. |
| `font` | **sí** | text lliure | Id d'una fitxa a docs/fonts/. Una fitxa per FONT, no per document. |
| `timestamp` | **sí** | text lliure | ISO 8601 de l'última edició amb significat. |
| `tags` | no | text lliure | Qualitats transversals. Mai la categoria principal: això és tema. |

## Camps d'una fitxa de font

Una fitxa per **font**, no per document. Cinquanta articles del mateix fons
referencien la mateixa fitxa: duplicar la llicència a cada document garanteix
que d'aquí a sis mesos n'hi hagi cinquanta versions divergents.

| Camp | Obligatori | Valors | Què hi va |
| --- | --- | --- | --- |
| `type` | **sí** | text lliure | Sempre 'font'. |
| `id` | **sí** | per forma | Identificador estable. És el que referencien els documents. |
| `title` | **sí** | text lliure | Nom llegible de la font. |
| `titular` | **sí** | text lliure | Qui té els drets. |
| `url` | **sí** | text lliure | On viu l'original. |
| `llicencia` | **sí** | text lliure | La llicència tal com la declara el titular. |
| `redistribucio` | **sí** | enum `redistribucio` | Si el titular permet redistribuir. Es REGISTRA sempre amb el seu valor real. Un 'no' o un 'pendent' generen un avís i no tanquen la porta (constitució §24): el propietari del projecte sosté els permisos. El registre existeix perquè la decisió segueixi sent reversible i es pugui separar el corpus per porcions. |
| `data_consulta` | **sí** | text lliure | Quan es va consultar i verificar. |
| `abast` | no | text lliure | Quina part del fons cobreix aquesta fitxa. |
| `notes` | no | text lliure | Context sobre el permís, la verificació o les limitacions. |

## Com s'afegeix un document

1. Si la font encara no té fitxa, escriviu-la a `docs/fonts/<id>.md`.
2. Escriviu el document a la branca que li toca. La **ruta ha de correspondre**
   al camp `tema`.
3. Calculeu `apte_llengua` amb la regla de dalt. No l'inventeu: si no quadra, la
   comprovació ho detecta.
4. Executeu `uv run cervell check docs/`.
5. Regenereu l'índex. No l'editeu a mà.

Afegir una branca nova és **crear un directori**. `tema` es valida per forma i no
contra una llista tancada, precisament perquè el contracte no faci nosa.

## Les regles

| Id | Severitat | Què comprova |
| --- | --- | --- |
| `R001` | error | Camp obligatori absent o buit. |
| `R002` | error | Valor fora de l'enum declarat. |
| `R003` | error | apte_llengua declarada no coincideix amb la derivada de veu i epoca. |
| `R004` | error | El camp font apunta a una fitxa que no existeix a docs/fonts/. |
| `R005` | **avís** | La font no permet la redistribució o la té pendent. S'avisa; no bloqueja. |
| `R006` | error | Cita verbatim sense marcar o sense atribuir. |
| `R007` | error | La ruta del document no correspon al seu camp tema. |
| `R008` | error | Enllaç intern trencat. |
| `R009` | error | Wikilink [[...]] present. Trenca la conformitat OKF; feu servir enllaços markdown relatius. |
| `R010` | error | Camp obligatori absent a la fitxa de font. |
| `R011` | error | Document no parsejable: el frontmatter no és YAML vàlid. |
| `R012` | error | Els fitxers generats no coincideixen amb l'esquema i el corpus. Regenereu-los. |
| `R013` | error | Maquinària prohibida present. El cervell hereta la forma del harness, no el seu motor. |
| `R014` | error | Binari commitejat sota docs/. El corpus és text. |

Els **avisos** s'imprimeixen i no canvien el codi de sortida. Avui només `R005`:
la procedència es registra sempre amb el seu valor real, però no veta l'entrada
(constitució §24). El registre existeix perquè la decisió segueixi sent
reversible i es pugui separar el corpus per porcions de llicència.
