# Exemple 4 — Parla: la veu andorrana, sense verificar

**El material més valuós i el més fràgil.** És l'únic tipus de text que és llengua
andorrana de veritat, i encara ningú no l'ha escoltat per corregir-lo.

| Què hi ha a l'entrada | Què se'n fa | Regla |
| --- | --- | --- |
| Preàmbul «Tanda 28 de parla…», «Avís», «Consentiment», taula «Qui parla» | Fora del text. Les dades útils passen al **frontmatter**: `parlant` (nom, parròquia, rol, el que no consta), `durada`, `marques_incertes` | En `parla`, tot el que no és la transcripció són metadades de la mostra, no text. |
| Bloc ```` ``` ```` amb `[00:00:04.990 --> 00:00:08.550] …` | Un segment per línia: `<!-- seg: …#s001 · inici–fi · incerts: N (paraules) -->` + el text | La marca de temps surt del text i va al comentari. **42 segments, en el mateix ordre.** |
| `[?Això] recordo…` | `Això recordo…`, i `incerts: 1 (Això)` | Es treuen els claudàtors, **la paraula es queda**, i es registra quines eren incertes. No es corregeix res: «Caldes», «Caldea de davall», «Béal» o «carribes» probablement són errors de l'ASR, però **només una persona escoltant l'àudio ho pot decidir**. |
| 65 marques en total | `marques_incertes: 65` | Ha de coincidir amb el recompte de l'«Avís» de l'entrada. Si no quadra, és un error del parser. |
| `bueno`, `tindre`, `lo que`, `dins d'un altre marc`… | **Es manté tal qual** | És exactament el que volem ensenyar: la parla real. No es normalitza cap a l'estàndard (§12). |
| Els 4 buits | **Cap va a `buits/`** | En `parla`, els buits parlen de la mostra (qualitat, perfil, drets), no d'Andorra. El perfil que no consta passa al frontmatter. |
| Buit 4: «Cap afirmació d'aquesta peça no s'ha de citar com a fet» | `citable_com_a_fet: false` al frontmatter | És memòria personal de fa trenta anys transcrita per una màquina. Serveix per aprendre **com parla** un andorrà, no **què va passar**. Per això `usos: [llengua]` i mai `coneixement` ni `raft-context`. |
| — | `estat: pendent-escolta`, `decisio: pendent` | Fins que algú escolti l'àudio i validi els segments, no entra a cap dataset d'entrenament. Sí que pot servir ja per avaluar. |
