# Pilot de calibratge: converses que podria iniciar una persona

Aquests cinc exemples serveixen per comprovar el nou criteri. Parteixen d'un dubte, una confusió o una petició de recordar; cap pregunta no depèn del nom d'una fitxa o d'una secció. Els seguiments continuen el tema que Maia acaba d'explicar.

**No són registres aprovats ni entren dades.** Es conserven aquí perquè els puguem revisar i canviar abans d'obrir una nova tanda de candidats. La procedència i l'estat de drets consten a [`examples-provenance.md`](examples-provenance.md).

## 1. Denunciar i demandar no eren el mateix

```json
{"messages":[{"role":"user","content":"Com pot ser que es pogués denunciar un cònsol però no reclamar-li un deute? No era el mateix?"},{"role":"assistant","content":"No. La fitxa descriu dues vies diferents. Abans de la Reforma de 1866, calia autorització prèvia per iniciar una acció civil contra una autoritat, fins i tot per un deute personal. Per perseguir-la criminalment, no calia aquell permís."},{"role":"user","content":"I després de la Reforma ja se li podia reclamar qualsevol deute?"},{"role":"assistant","content":"No qualsevol. Després de 1866, l'autorització només es mantenia per als deutes contrets en exercici del càrrec. Per un deute personal, es podia citar l'autoritat sense demanar-la abans."}]}
```

**Per què funciona:** la pregunta neix d'una contradicció aparent; el seguiment pregunta per la conseqüència del canvi històric.

## 2. El text i el gràfic es contradiuen

```json
{"messages":[{"role":"user","content":"La publicació diu que el 2018 el català era al 56,8 i el castellà al 57,6, però el gràfic sembla posar el català per sobre. Quina dada és correcta?"},{"role":"assistant","content":"Per al 2018, la sèrie del Departament d'Estadística dona 56,8 per al català i 57,6 per al castellà, igual que el text. El gràfic està invertit: dibuixa el català a 57,6 i el castellà a 56,8."},{"role":"user","content":"I el 2014 el català sí que havia passat al davant?"},{"role":"assistant","content":"Sí. El 2014 la mateixa sèrie dona 57,7 per al català i 56,4 per al castellà: una diferència d'1,3 punts a favor del català."}]}
```

**Per què funciona:** l'usuari demana resoldre una contradicció concreta; la resposta separa text, gràfic i sèrie estadística.

## 3. D'on ve el nom de la Marratxa?

```json
{"messages":[{"role":"user","content":"Per què es diu Marratxa? Encara ballen amb aquell recipient?"},{"role":"assistant","content":"El nom ve d'una marratxa, un recipient d'aigua perfumada que els dansaires duien a les mans. La fitxa diu que l'objecte va desaparèixer del ball, tot i que el nom es va conservar."},{"role":"user","content":"I quan es balla ara a Sant Julià?"},{"role":"assistant","content":"La Marratxa es balla el dilluns de la festa major de Sant Julià de Lòria, juntament amb el ball del Cerdà i la Passa."}]}
```

**Per què funciona:** el seguiment sorgeix d'una resposta sobre la dansa i afegeix una dada pràctica relacionada.

## 4. Un tipus del 3,33% i un altre del 5%

```json
{"messages":[{"role":"user","content":"M'he trobat un 3,33% i un 5% en textos sobre interessos a Andorra. Quin dels dos s'aplicava?"},{"role":"assistant","content":"Depenia del contracte. Un decret de 1895 diu que els censals continuaven al tres i terç per cent —aproximadament un 3,33%—, mentre que per a la resta el Consell i les Corts acceptaven el 5%."},{"role":"user","content":"Aleshores la regla del tres i terç encara valia el 1895?"},{"role":"assistant","content":"Sí. El decret del 25 de novembre de 1895 reconeix que el tipus del censal continuava vigent «segons la llei de la Vall». També diferencia aquest contracte de la resta, per als quals s'acceptava el 5%."}]}
```

**Per què funciona:** la primera pregunta expressa una confusió real; el seguiment comprova si una norma anterior continuava vigent.

## 5. Recordar la llegenda de Meritxell

```json
{"messages":[{"role":"user","content":"Em recordes la llegenda de la imatge de Meritxell? Per què es va quedar en aquell lloc?"},{"role":"assistant","content":"Segons la llegenda, un pastor va trobar la imatge sota una gavernera florida el dia de Reis. La van portar a Canillo i després la van tancar a Encamp, però cada vegada tornava al lloc de la troballa. La gent va entendre que volia quedar-s'hi i hi va construir el santuari."},{"role":"user","content":"Això es pot donar per fet històric?"},{"role":"assistant","content":"No amb les fonts que recull la fitxa. És el relat de la llegenda; no hi consta una font primària ni la data en què es va documentar per primera vegada."}]}
```

**Per què funciona:** la primera pregunta demana una història concreta; el seguiment comprova què és llegenda i què està verificat.

## Les preguntes que no passaven el filtre

| Formulació descartada | Què falla | Direcció millor |
|---|---|---|
| «Què explica la secció “El relat” de la fitxa “La troballa de Meritxell”?» | L'usuari ha de tenir la fitxa oberta. | «Em recordes la llegenda de la imatge de Meritxell?» |
| «Què indica aquesta fila?» | No identifica què vol entendre. | Explicar què es contradiu i preguntar quina dada és fiable. |
| «I dos topònims que en surten:» | És un fragment sense una petició completa. | Descartar-lo, llevat que hi hagi una pregunta real sobre aquells llocs. |
| «Tres coses que el corpus registra per separat:» | És una nota editorial, no una intervenció d'usuari. | Preguntar quin dubte resol el document —per exemple, per què hi ha dos tipus d'interès. |

No cal convertir cada pregunta descartada en una pregunta nova. Si no hi ha una motivació natural, no hi ha registre.
