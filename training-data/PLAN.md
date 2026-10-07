# Pla de treball

## Objectiu

Crear converses d'entrenament útils, correctes i naturals. La unitat no és una dada de la fitxa: és una consulta humana que Maia sap resoldre gràcies a la fitxa.

## 1. Calibrar el to abans de produir registres

1. Llegir sencera la fitxa i comprovar-ne les fonts i els drets.
2. Escriure poques converses representatives a `knowledge/review/EXEMPLES.md`.
3. Fer que les preguntes inicials expliquin un dubte reconeixible sense esmentar la fitxa, cap secció ni cap fila.
4. Afegir seguiments només quan una resposta hagi obert una curiositat concreta. Preferir fils amb més d'un intercanvi quan siguin naturals; no allargar-los per quota.
5. Revisar els exemples llegint només els missatges de l'usuari. Si el fil no s'entén o el seguiment podria anar després de qualsevol resposta, reescriure'l.

Els exemples són guia editorial. No compten com a registres, cobertura ni exports. Cal revisar-ne el to abans d'obrir una tanda gran de registres.

## 2. Crear converses Knowledge, fitxa a fitxa

- Revisar la fitxa sencera, no només el títol o el fragment que inspira la pregunta.
- Buscar intencions reals: aclarir una confusió, entendre una tradició, comprovar una data, comparar dues mesures o saber què es pot concloure.
- Escriure una conversa per intenció. No acumular preguntes independents en un sol fil.
- Donar context a la primera pregunta. Els seguiments poden usar pronoms o el·lipsis perquè ja tenen context conversacional.
- Respondre directament. Distingir fets, llegendes, interpretacions, dades històriques i informació vigent.
- Dir què no se sap quan la font no permet tancar una qüestió. No inventar causes ni detalls per fer la resposta més rodona.
- Registrar fonts, drets, afirmacions recolzades i grup de deduplicació a `provenance.jsonl`.
- Una fitxa pot generar cap conversa si no hi ha cap pregunta humana útil. Cobertura vol dir haver-la revisat, no convertir cada frase en una pregunta.

## 3. Revisar, aprovar i exportar Knowledge

Mantenir separats els exemples editorials, els candidats actius i els registres aprovats. Revisar cada conversa en context, comprovar-ne les afirmacions i els drets, deduplicar-la i agrupar variants per tema i font. Crear `train`, `validation` i `test` només quan hi hagi prou registres aprovats; mantenir les variants d'una mateixa font o intenció al mateix split.

Abans d'exportar, validar el format, els torns, els duplicats, la procedència, els drets i la cobertura de les fitxes. No presentar exemples de calibratge ni candidats pendents com un dataset llest per entrenar.

## 4. Construir Maia Language per separat

- Revisar cada peça de `docs/parla/` i confirmar `veu: originaria`, `epoca: contemporania` i `apte_llengua: true`.
- Verificar drets, permís d'ús i fiabilitat de transcripció per peça.
- Conservar text produït per persones. No inventar preguntes o respostes per convertir monòlegs en diàleg.
- Preservar lèxic, sintaxi i ordre del parlant. Documentar qualsevol normalització.
- Separar les peces o entrevistes entre els splits per evitar que fragments relacionats caiguin a train i test.

## Criteri de sortida

Knowledge només es declara preparat després de revisar tot `docs/temes/`, tractar cobertura, drets i duplicats, i validar els exports. Language només es declara preparat després de revisar totes les peces elegibles, filtrar fragments dubtosos, comprovar drets i validar els splits. El nombre de registres no substitueix cap d'aquestes comprovacions.
