# Sondeig del patró d'URL d'Estadística, finestra 2024-06-01 → 2025-09-30

**18-09-2026.** Notes de premsa del **Departament d'Estadística**, **CC BY 4.0**
segons l'avís legal conservat a
`docs/raw/estadistica-poblacio/avis-legal-2026-09-13.txt`. **Es versionen.**

## Per què hi ha aquest sondeig

El corpus tenia una escombrada **exhaustiva** del patró
`sig.govern.ad/SIGDDE.Public/Files/Documents/Notes_premsa_noticies/<CODI>_<AAAAMMDD>_A.pdf`
—**74.272 peticions `HEAD`**, els 211 codis del catàleg—, a
`02-DOCS/raw/operations/calendari-estadistica-2026-09-17.md`. **Va trobar 256
notes de 97 activitats**, i el corpus en va deduir que les **114 activitats
restants no publiquen**.

**La deducció era falsa, i el motiu és la finestra**: aquella escombrada anava
del **2025-10-01 al 2026-09-17**. **Un sondeig exhaustiu només ho és dins de la
seva finestra.**

## Aquest sondeig

**114 codis** —els que no tenien cap nota a la finestra anterior— per **348 dies
feiners** del **2024-06-01 al 2025-09-30**: **39.672 peticions `HEAD`**, 32 fils.

**Tretze encerts, i no dotze de nous: nou.** **A052 (`20250403`) i A117 ja eren
al corpus** —a `../estadistica-prestacions/` i a `../estadistica-habitatge/`—,
**i A109 s'havia trobat el mateix dia a mà.** **Comprovat després de baixar-les,
que és tard**: la comprovació correcta era mirar `docs/raw/` abans del sondeig.

| Codi | Activitat | Data | Porta dades? |
| --- | --- | --- | --- |
| **A024** | Pre-ensenyament superior | `20241118` | **sí**, 714 línies |
| **A052** | Prestacions per desocupació involuntària | `20240606` · `20241111` · `20250403` | **sí** |
| **A053** | Prestacions no contributives | `20240606` | **sí**, 746 línies |
| **A109** | Efectius i rendiments ramaders | `20250527` | **no**, nota-punter |
| **A110** | Pesca fluvial | `20250325` | **no**, nota-punter |
| **A111** | Caça | `20250808` | **no**, nota-punter |
| **A117** | Transaccions immobiliàries | `20240805` · `20241107` | **sí**, 606 línies |
| **A131** | Prevenció del blanqueig | `20250828` | **no**, nota-punter |
| **A138** | Balança de pagaments i posició inversora | `20250123` · `20250731` | **sí**, 971 línies |

## L'error d'aquest sondeig, escrit

**Nou dels tretze encerts eren nous; tres ja eren al corpus.** **A052 del
`20250403` és exactament el fitxer que ja hi ha a
`../estadistica-prestacions/a052-desocupacio-20250403.txt`**, i **A117 té dues
notes més recents i més completes a `../estadistica-habitatge/`**, **sota el nom
compost `A117_A145`** —que és per això que un sondeig per `A117_<data>` sol no
les torna, i **el README d'aquella carpeta ja ho advertia**.

**El sondeig es va llançar sense mirar què hi havia a `docs/raw/`.** És el mateix
error que aquesta sessió ha diagnosticat al *Politar*, a la *Instructa* i al
manuscrit Palmitjavila, **comès pel corpus mateix i el mateix dia**. Queda
escrit, i la regla que en surt és:

> **Abans de sondejar una font, mesura què en tens.** I **abans de creure que un
> codi no publica, mira si publica sota un nom compost.**

## El patró de les notes-punter, ara amb set casos

**A070, A071, A106, A109, A110, A111 i A131.** Un full, els articles 33 i 37.5.a
de la Llei 2/2013, i «les dades es poden consultar al següent enllaç».

**L'enllaç a vegades és visible al text i a vegades no.** Quan no ho és, és una
anotació del PDF i s'extreu així:

```python
for m in re.finditer(rb"/URI\s*\((.*?)\)", open(f, "rb").read(), re.S):
    print(m.group(1).decode("latin-1"))
```

**On porten:**

| Nota | Destí | Drets al destí |
| --- | --- | --- |
| A106, A109 | Departament d'Agricultura, `www.govern.ad` | **drets reservats** |
| A110, A111 | Departament de Medi Ambient, `www.govern.ad` | **drets reservats**, però amb clàusula de citació pròpia |
| A131 | **Memòria 2024 de la UIFAND**, `uifand.ad` | no comprovats |

**A110 i A111 afegeixen una segona via que val la pena retenir**: «**o bé, al
web d'estadística: `www.estadistica.ad` a l'apartat Estadístiques/Dades/Medi
ambient/Patrimoni natural**». **És a dir que `estadistica.ad` publica taules
fora del patró de notes de premsa**, que és l'únic que el corpus ha sondejat
fins ara. `Aquella secció no s'ha buidat: el lloc és una aplicació ArcGIS Hub i
la seva API de cerca no retorna les notes.`

## Destil·lació

- A110 i A111 → [Qui caça i qui pesca](../../temes/territori/fauna-i-flora/qui-caca-i-qui-pesca.md),
  per la via del destí.
- A117 → [Tres-centes tretze, els dos anys](../../temes/societat/habitatge/tres-centes-tretze-els-dos-anys.md),
  **però la fitxa no es basa en aquestes dues notes sinó en les millors que el
  corpus ja tenia** (vegeu l'avís de sota). **Llegides igualment senceres**:
  **quatre columnes de nombre quadren exactament**, **tres de les quatre de
  valor fallen per un euro**, i **el resum del `20241107` diu «tercer trimestre
  del 2023» on la taula diu 2024**; registrat i no corregit.
- A138 (`20250731`) → [Tot el superàvit és el turisme](../../temes/economia/transformacio-economica/tot-el-superavit-es-el-turisme.md).
  **Divuit pàgines; llegides la balança, les quatre taules comparatives i la
  posició inversora.** **Les cinc files d'actius de la PII quadren una per una**;
  **la línia «Béns» no quadra amb les seves dues subpartides** —trenta-dos
  milions— **i sí amb crèdit menys dèbit**. Registrat.
- A024, A052, A053 i la nota A138 del `20250123` **encara no s'han llegit**.
