# Pla per a les converses de Maia

## Per a què serveix

Preparar dos conjunts diferents, tots dos en format de conversa:

- **Knowledge** respon preguntes sobre Andorra amb informació de `docs/temes/`.
- **Language** conserva usos autèntics del català andorrà contemporani de `docs/parla/`. No inventa diàlegs ni imita parlants.

Ara estem fixant l'estil i el procés amb mostres petites. Les mostres de `knowledge/examples/` són de calibratge. No són registres aprovats ni compten com a cobertura.

## Com trobar una pregunta humana

1. Identifica què vol resoldre algú: entendre una norma, preparar una visita, aclarir una paraula, comprovar una història o decidir què es pot concloure.
2. Formula la pregunta amb el context mínim perquè s'entengui sense haver vist Maia ni cap document.
3. Respon de seguida. Afegeix només el context necessari i marca els límits de la font.
4. Continua el diàleg només amb una pregunta que algú faria després d'escoltar la resposta.
5. Comprova cada afirmació contra la font i registra la procedència fora del diàleg.

Una conversa multitorn ha de tenir un fil recognoscible. El segon torn ha de néixer del primer. No hi ha una quota de preguntes de seguiment: si només es pot afegir un torn forçat, la conversa no és bona encara que sigui llarga.

### Transformar l'enunciat, no copiar-lo

| Evita | Busca el dubte real |
| --- | --- |
| «Què explica la secció sobre qui és demandat?» | «Si un comú em reclamava una cosa, m'havia de jutjar el mateix tribunal que si la reclamava jo?» |
| «Què diu aquesta fila?» | «Quines xifres no coincideixen, i què podem concloure?» |
| «Resumeix el relat de la fitxa.» | «Per què la llegenda situa el santuari de Meritxell en aquell indret?» |

No cal convertir cada taula, secció o detall en una conversa. El que no es pugui preguntar amb naturalitat queda a la cobertura, no es disfressa de pregunta.

## Criteris de resposta

- La primera frase resol la pregunta.
- Cada missatge s'entén en el context de la conversa. La primera pregunta no depèn del document.
- El seguiment demana informació nova i manté clar de què es parla.
- Els noms i termes locals s'expliquen quan cal.
- Els desacords entre fonts es presenten com a desacords. No s'inventa una solució.
- La incertesa o l'absència d'una dada es diuen clarament.
- Les notes internes, els IDs i la procedència queden fora de `messages`.
- Si no hi ha una llicència o una transcripció apta, el registre no s'exporta.

## Flux de treball

1. Tria una necessitat humana que el corpus pugui resoldre.
2. Llegeix totes les fonts pertinents, no només el títol o el fragment que sembla útil.
3. Escriu el diàleg sense esmentar la fitxa ni la seva estructura.
4. Llegeix només els missatges en veu alta. Si sembla un examen, una ordre editorial o una conversa inventada, torna'l a escriure.
5. Comprova cada fet, anota la font i la llicència a `provenance.jsonl`, i deixa l'estat com a pendent de revisió.
6. Afegeix registres nous només després de revisar aquestes mostres i acordar el criteri.

## Carpetes i estats

- `knowledge/examples/`: mostres de calibratge; mai no s'exporten automàticament.
- `knowledge/review/`: registres candidats pendents de revisió humana.
- `knowledge/work/`: inventari i mapa de cobertura auditable.
- `knowledge/reports/`: volum, cobertura, exclusions i qualitat.
- `knowledge/output/`: exportacions aprovades; queda buit mentre falti revisió, drets, deduplicació o validació.
- `language/`: flux separat; no es crea cap exemple sintètic de parla humana.

Cada línia d'un JSONL és una conversa. El format de missatges és només `user` i `assistant`. La procedència i l'estat d'aprovació van en un fitxer separat. Cap exemple de calibratge o candidat pendent no es pot confondre amb l'export final.

## Revisió abans d'afegir més registres

- [ ] La pregunta inicial sona com una cosa que preguntaria una persona?
- [ ] S'entén sense haver llegit la fitxa?
- [ ] La resposta contesta abans de donar context?
- [ ] El seguiment surt de la resposta anterior i obre una pregunta nova?
- [ ] Cada fet es pot verificar i la font es pot reutilitzar?
- [ ] Si llegeixo només el diàleg, sento una conversa i no un qüestionari?

Si una resposta és «no», es reescriu o s'exclou. No s'afegeixen variants cosmètiques per augmentar el recompte.
