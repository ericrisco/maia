---
type: font
id: consell-general-seu
title: "Seu electrònica del Consell General d'Andorra"
titular: Consell General del Principat d'Andorra
autor: Consell General (Secretaria General i Sindicatura)
publicacio: "Seu electrònica institucional: actes del Ple, butlletí del Consell General, iniciatives legislatives, tractats internacionals i convocatòries"
url: https://seu.consellgeneral.ad/
llicencia: "Tots els drets reservats. L'avís legal diu que el lloc web i tots els seus continguts són propietat del Consell General i que la reutilitzacio d'alguns documents pot estar limitada per la Llei del 10 de juny del 1999 sobre drets d'autor i drets veïns. No s'hi declara cap llicència oberta."
redistribucio: "no"
data_consulta: 2026-09-18
abast: >
  Actes del Ple del Consell General de la IX legislatura i dels anys 2023, 2024,
  2025 i 2026, en PDF i sense clau. Butlletí del Consell General des del 2023 a
  la seu i els anteriors al 2023 en un altre domini. Projectes i proposicions de
  llei, procediments especials, tractats internacionals, preguntes al Govern amb
  resposta oral i escrita, convocatòries del Ple i de comissions, concursos i
  contractacions directes.
notes: >
  DESCOBERTA DEL 18-09-2026, i el corpus la tenia apuntada com a via tancada.
  La seu respon a peticions anònimes: no hi ha token, ni cookie, ni registre.
  Els PDF de les actes es baixen de /documentPublic/download/<id>.
  ELS PDF NO PORTEN CAPA DE TEXT. El text que en treu pdftotext és només la
  franja de signatura electrònica —tipus, nom, unitat, codi segur de
  verificació— i el cos de l'acta és imatge. Cal OCR; tesseract amb -l cat
  llegeix bé la llista de consellers i el cos del debat.
  EL QUE FA VALUOSES LES ACTES PER AL CORPUS: cada acta obre amb la llista
  nominal de tots els consellers presents, amb el tractament Sr. o Sra. davant
  de cada nom. El sexe de cada conseller és, doncs, dada de la font i no
  inferència del corpus a partir del nom de fonts.
  DRETS: consulta sí, redistribució no. Ni els PDF ni els seus OCR no es
  versionen al corpus. El que hi entra són xifres i cites amb atribució, amb
  l'URL i el codi segur de verificació al costat perquè es puguin comprovar.
  EL QUE AIXÒ NO RESOL: les actes en línia comencen el 2023. Tot el que és
  anterior —el Consell Constituent, les legislatures del 1993 al 2019, la Llei
  Electoral del 1987 que el corpus busca— segueix essent arxiu parlamentari i
  segueix necessitant la petició escrita.
---

# La seu electrònica del Consell General

**Oberta el 18-09-2026**, i **el corpus la portava apuntada com a via tancada des
del 16-09-2026**: una de les onze peticions escrites demanava justament l'accés
a l'arxiu parlamentari.

## Què hi ha, i sense cap clau

| Secció | Què conté |
| --- | --- |
| **Actes del Ple** | **IX legislatura i els anys 2023, 2024, 2025 i 2026**, en PDF, a `/documentPublic/download/<id>` |
| **Butlletí del Consell General** | **des del 2023** a la seu; **els anteriors, en un altre domini** |
| **Procediment legislatiu** | projectes i proposicions de llei, d'iniciativa parlamentària, comunal i popular |
| **Procediments especials** | pressupost, llei qualificada, extrema urgència, lectura única, reforma constitucional |
| **Impuls i control** | elecció del cap de Govern, moció de censura, qüestió de confiança, preguntes amb resposta oral i escrita |
| Tractats internacionals, convocatòries, concursos i contractacions directes | |

## El detall tècnic que decideix com es llegeix

**Els PDF no porten capa de text.** `pdftotext` en treu **només la franja de
signatura electrònica** —tipus, nom del document, unitat, codi segur de
verificació, signants i hora—, **repetida una vegada per pàgina**, i **res del
cos**. **El cos és imatge i cal OCR**; `ocrmypdf -l cat --force-ocr` seguit de
`pdftotext -layout` en dona la llista de consellers i el debat.

**Cada acta obre amb la llista nominal de tots els presents**, i **davant de
cada nom hi ha el tractament**: **Sr.** o **Sra.** **El sexe de cada conseller
és dada de la font**, no una inferència del corpus a partir del nom de fonts.
**Això és el que fa que aquesta font pugui tancar buits que la Viquipèdia i els
decrets de proclamació no tancaven.**

## Drets

**Tots reservats.** L'avís legal declara que el lloc i **tots** els seus
continguts són propietat del Consell General, i que la reutilització d'alguns
documents **pot estar limitada** per la Llei del 10 de juny del 1999 sobre drets
d'autor i drets veïns. **No hi ha llicència oberta declarada.**

**Decisió del corpus**: **ni els PDF ni els seus OCR no es versionen.** El que
entra al corpus són **xifres i cites amb atribució**, amb **l'URL i el codi
segur de verificació** al costat, perquè qualsevol lector pugui comprovar-ho
contra l'original.

## El que això no resol

**Les actes en línia comencen el 2023.** **El Consell Constituent, les
legislatures del 1993 al 2019 i la Llei Electoral del 1987** —que el corpus
busca des que la Llei qualificada del 1993 la va citar en derogar-la— **segueixen
essent arxiu parlamentari**, i **la petició escrita segueix fent falta.**
