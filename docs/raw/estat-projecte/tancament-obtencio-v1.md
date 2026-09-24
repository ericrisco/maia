---
type: index
title: "Maia — tancament de l'obtenció inicial i preparació de datasets"
---

# Maia — tancament de l'obtenció inicial i preparació de datasets

## Decisió de tancament

**La fase d'obtenció inicial del corpus queda tancada el 24 de setembre de
2026, per instrucció del responsable del projecte.** Hi ha prou material per
preparar una primera selecció d'entrenament i mesurar-ne la utilitat.

«v1» identifica aquesta fita de recopilació. No és una release publicada, una
instantània immutable ni una declaració que tot el material sigui apte per
entrenar. La recopilació general deixa de ser la prioritat; les ampliacions
posteriors respondran a mancances concretes de curació o a errors d'avaluació.

## Inventari observat al tancament

Recompte dels Markdown segons el camp `type` a `docs/temes/`, `docs/parla/` i
`docs/fonts/`, excloent els índexs:

| Unitat | Recompte |
| --- | ---: |
| Articles temàtics | 1.347 |
| Fitxes de font | 618 |
| Documents de parla | 40 |

Els índexs de navegació, les fonts primàries, les notes i els derivats sota
`raw/` no incrementen aquests recomptes. El material audiovisual de prospecció
conserva els seus estats pendents; no es promou automàticament al corpus
validat pel fet de tancar la recopilació.

## Pendents traspassats

- Verificació factual: resoldre contradiccions internes, comprovar xifres i
  vincular les afirmacions seleccionades a la peça exacta de la font.
- Metadades: corregir les dues etiquetes `apte_llengua` incompatibles amb
  `veu: compilada` detectades a la revisió i la referència de font absent de
  l'article d'Esteve Albert. Revisar també identificadors i camps obligatoris.
- Condicions d'ús: normalitzar els estats i determinar l'elegibilitat per a
  cada ús previst. La presència d'una fitxa no implica permís per entrenar o
  distribuir un dataset.
- Parla: els 39 documents que declaren veu originària estan etiquetats com a
  transcripció no verificada. Cal atribuir torns, revisar l'àudio i documentar
  el perfil lingüístic. El lloc de naixement, tot sol, no determina la varietat
  de parla d'una persona.
- Cobertura: equilibrar dominis i famílies de fonts abans de mostrejar. El
  nombre d'articles no mesura la diversitat d'evidència independent.
- Eines: el README anuncia `cervell check`, però la CLI inspeccionada només
  ofereix `render`. Comprovar índexs i enllaços no valida la veritat del text.

## Fase següent: curació i preparació de datasets

Objectiu: obtenir una primera selecció traçable i un conjunt de proves
independent que permeti comparar models.

1. **Inventari d'elegibilitat.** Per document o fragment: font, evidència,
   dates de referència, ús previst, estat de revisió i decisió
   `incloure`, `pendent` o `excloure`, amb motiu.
2. **Curació.** Resoldre els errors detectats, separar fets d'hipòtesis,
   retirar anotacions de treball dels textos d'entrenament i agrupar duplicats
   i derivats de la mateixa font.
3. **Avaluació reservada.** Definir tasques i respostes verificades abans de
   generar Q&A. Separar famílies de fonts entre entrenament i prova; mantenir
   juntes les paràfrasis i els derivats per evitar filtracions.
4. **Datasets pilot.** Preparar coneixement verificat, Q&A amb evidència i
   llengua revisada com a conjunts amb finalitats diferents. Conservar també
   exemples d'ambigüitat i d'evidència insuficient sense convertir absències
   documentals en negacions sobre Andorra.
5. **Validació de la versió.** Comprovar estructura, traçabilitat, elegibilitat,
   cobertura, separació de conjunts i una revisió humana definida abans de
   exportar-la.

Com a proposta inicial, no com a producció ja feta ni rendiment garantit:
300–500 preguntes d'avaluació revisades i 3.000–5.000 Q&A d'entrenament si la
selecció verificada ho permet. La qualitat i la cobertura prevalen sobre
assolir un nombre d'exemples.

La fase es podrà tancar quan els exemples acceptats tinguin evidència i estat
d'ús explícits, els errors coneguts no passin a l'exportació, i existeixi una
avaluació reservada i documentada. L'entrenament pilot i la comparació amb el
model base constituiran la fase posterior.

## Buits registrats

No s'ha verificat exhaustivament cada afirmació del corpus. Encara no hi ha
una mesura de millora del model atribuïble a aquest material ni un dataset
pilot certificat per aquest tancament. El volum final elegible, els permisos
pendents i la qualitat de les transcripcions continuen per determinar.
