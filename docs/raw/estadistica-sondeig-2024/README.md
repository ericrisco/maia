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

**Tretze encerts, dotze de nous:**

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
- A117 → [De dos mil quatre-cents a quatre mil cent euros el metre](../../temes/societat/habitatge/de-dos-mil-quatre-cents-a-quatre-mil-cent-euros-el-metre.md).
  **Les dues notes llegides senceres**, totes les taules comprovades: **quatre
  columnes de nombre quadren exactament** i **tres de les quatre de valor fallen
  per un euro**. **El resum del `20241107` diu «tercer trimestre del 2023» on la
  taula diu 2024**; registrat i no corregit.
- A024, A052, A053 i A138 **encara no s'han llegit**.
