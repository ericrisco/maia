# Demografia vital per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../README.md).

| | |
| --- | --- |
| **Fitxer** | `demografia-vital-api-2026-09-18.tsv` — **55.358 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **200 divisions** dels prefixos `010102` naixements, `010103` matrimonis, `010104` taxa de natalitat, `010105` immigració i `010106` autoritzacions d'immigració |
| **Sèries més llargues** | naixements i defuncions **des del 1953**, matrimonis **des del 1977**, taxa de natalitat **des del 2010** |

## Vuit taules retallades a consciència

**El bolcat sencer feia 19 MB i 119.706 valors.** **Vuit encreuaments hi posaven
64.348 valors, la majoria zeros**: són creuaments de cada edat per cada tipus,
de cada nacionalitat per cada tipus i de cada parròquia per cada tram d'edat i
sexe. **S'han retirat i el fitxer queda en 8,1 MB.**

Les taules retirades, per si s'han de tornar a demanar —**es tornen a baixar amb
el mateix guió, sense filtre**—:

- `AUTORITZACIONS D'IMMIGRACIÓ EN VIGOR PER TIPUS I TEMPS DE RESIDÈNCIA`
- `AUTORITZACIONS D'IMMIGRACIÓ EN VIGOR PER EDAT I TIPUS`
- `AUTORITZACIONS D'IMMIGRACIÓ EN VIGOR PER NACIONALITAT I TIPUS`
- `AUTORITZACIONS D'IMMIGRACIÓ INICIALS PER NACIONALITAT I TIPUS`
- `BAIXES PAÍS PER EDAT I TIPUS (DETALL)`
- `BAIXES PAÍS PER NACIONALITAT I TIPUS`
- `DEFUNCIONS PER PARRÒQUIA, EDAT (TRAMS 10 ANYS) I SEXE`
- `NAIXEMENTS PER EDAT I NACIONALITAT DE LA MARE (TRAMS 1 ANY)`

## Una divisió que no respon

**La 558, `AUTORITZACIONS D'IMMIGRACIÓ D'HIVERN ACORDADES PER QUOTA`**, no
retorna dades. **Les altres 199 sí.** **No s'ha tornat a provar amb altres
paràmetres**: queda dit.

## El que aquest bolcat ha tancat

- **Si la sèrie de naixements i defuncions canvia de mètode el 1997**: **la
  sèrie publicada no ho recull.**
- **Quants matrimonis canònics i quants civils se celebren**: **del 1998 ençà,
  desglossat** — i **el bescanvi és del 2001-2002**.

**On s'ha escrit**: a
[`setanta-nou-anys-de-padro`](../../../temes/societat/demografia/setanta-nou-anys-de-padro.md)
i a [`casar-se-a-andorra`](../../../temes/societat/familia/casar-se-a-andorra.md).
**No s'ha fet fitxa nova**: **la sèrie de naixements i defuncions ja hi era, i
duplicar-la hauria posat les mateixes xifres a dos llocs.**
