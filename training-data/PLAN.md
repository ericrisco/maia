# Pla de Maia Training Data

## Objectiu

Preparar dues fonts d'entrenament separades: **Maia Knowledge**, per respondre sobre Andorra amb informació del corpus, i **Maia Language**, per aprendre de parla contemporània real. La prioritat és la correcció, els drets, la cobertura útil i la naturalitat. No fixem una quota de registres.

## Per què refem les converses

Les preguntes com «Què explica la secció X de la fitxa Y?» pressuposen que qui pregunta té el document al davant. Les respostes com «Tres coses que el corpus registra per separat» no contesten la pregunta. Són instruccions de lectura i notes internes, no diàlegs d'assistent.

La fitxa és una eina per trobar i verificar informació. La pregunta ha de néixer d'un dubte humà sobre el tema. La resposta ha de resoldre aquest dubte per si sola.

## Com redactem una conversa

1. Identifiquem un dubte concret que algú podria tenir sense haver vist cap fitxa.
2. Verifiquem la resposta contra les fonts originals citades al corpus i comprovem que permeten reutilització en entrenament.
3. Escrivim una primera resposta directa, clara i prou completa.
4. Afegim un seguiment només si sorgeix de manera natural del que s'acaba de dir. El seguiment demana una cosa nova; no serveix per allargar el diàleg ni cobrir una casella.
5. Cada torn ha de funcionar en el seu context: la pregunta de seguiment pot fer referència al torn anterior, però no a una fitxa absent.
6. Llegim només la conversa en veu alta. Si sembla un qüestionari, una cerca al document o una plantilla, la reescrivim.
7. Revisem noms, dates, períodes, unitats, atribucions, incerteses i drets. Si no es pot verificar un punt, el corregim o el traiem.

## Senyals d'una pregunta humana

- Pregunta per una cosa comprensible: «El trinxat és propi d'Andorra?»
- Pot incloure context quotidià breu quan sigui rellevant, però no inventa una biografia ni una situació dramàtica.
- No diu «aquesta fitxa», «la secció», «la fila», «el corpus» ni «què explica el document», llevat que l'usuari realment pregunti pel document.
- Fa una pregunta per torn. El seguiment sembla una curiositat que apareix després de llegir la resposta.
- No es força un multitorneig: si el tema només permet una bona pregunta, es queda en un torn.

## Respostes

- Comencen contestant, no amb una capçalera ni un fragment deslligat.
- Són prou completes per ser útils encara que la conversa s'acabi en aquell torn.
- Donen el context necessari, però no aboquen tot el contingut de la fitxa.
- Distingeixen entre fets, llegendes, interpretacions i afirmacions no resoltes.
- No inventen per omplir buits. Diuen què no es pot concloure quan això és rellevant.
- Eviten llistes telegràfiques si una frase natural és més clara.

## Criteri d'aprovació

Abans d'aprovar una conversa, totes aquestes respostes han de ser afirmatives:

1. S'entén la pregunta inicial sense cap document al davant?
2. És una pregunta que una persona podria fer de debò?
3. La resposta contesta directament i és completa per al torn?
4. El seguiment és conseqüència natural de la conversa i aporta informació nova?
5. Els referents com «això» o «allò» són inequívocs?
6. Les afirmacions són verificables i els drets cobreixen l'ús previst?
7. Les dades tenen el període i la unitat necessaris?
8. La conversa sona normal en llegir-la en veu alta?

Un «no» vol dir revisar, deixar pendent o descartar. La cobertura no compensa una conversa artificial o una font no autoritzada.

## Fases

1. Fixar el criteri amb els exemples de `knowledge/review/examples.jsonl` i acordar què s'accepta.
2. Revisar de nou els registres antics. Cap registre anterior s'aprova automàticament; els que no passin el criteri no entren a cap export.
3. Crear converses de Knowledge tema per tema, vinculant-les a evidència i drets en fitxers de revisió interns.
4. Mesurar cobertura i duplicació; usar l'informe per trobar buits, no per fabricar preguntes.
5. Agrupar converses relacionades abans de separar train, validation i test.
6. Revisar Language per drets, consentiment, autenticitat i fiabilitat de transcripció. No inventar parlants, preguntes ni respostes.
7. Validar exports i publicar informes de cobertura, qualitat i exclusions.

## Estructura

`review/` conté candidats i exemples; `work/` conté inventaris regenerables; `scripts/` contindrà eines; `reports/` contindrà resultats de validació; `output/` només contindrà exports aprovats. Els exemples actuals són calibratge i queden exclosos de l'export.

## Maia Language

El text ha de provenir de parla humana real i autoritzada. Els criteris `veu: originaria`, `epoca: contemporania` i `apte_llengua: true` són necessaris quan pertoqui, però no substitueixen la revisió de drets ni la verificació de la transcripció. No convertir monòlegs en converses inventades, ni reescriure la parla com a català estàndard genèric.

## Quan es considerarà acabat

- **Knowledge:** el coneixement útil del corpus està representat per diàlegs correctes i naturals; les fonts permeten l'ús; els duplicats, els splits i els informes estan revisats.
- **Language:** totes les peces elegibles han estat examinades; només s'inclou parla fiable i autoritzada; els splits eviten que fragments relacionats contaminin l'avaluació.

No considerem acabada cap branca per haver arribat a un nombre de registres.
