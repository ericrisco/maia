# Revisió de converses

La referència positiva és [`knowledge/examples/`](../examples/README.md). Els exemples d'allà calibren el to; no són registres aprovats ni s'exporten.

## D'on surt el defecte dels candidats antics

Una pregunta com «Què explica la secció “El relat” de la fitxa “La troballa de Meritxell”?» no és una petició humana: obliga l'usuari a conèixer l'estructura de la font. I una resposta que només retorna «Se la va endur a Canillo...» comença a mig fil, perquè no identifica qui se la va endur ni què era.

Es pot convertir en un dubte natural i autosuficient:

```text
Usuari: Segons la llegenda, què va passar quan van portar la imatge de Meritxell a Canillo?
Assistent: La imatge va desaparèixer de l'església i l'endemà va tornar a aparèixer al peu de la gavernera florida, al lloc on l'havien trobada.
```

Un segon torn només hi encaixa si continua aquell dubte:

```text
Usuari: Això es considera un fet històric?
Assistent: No es pot afirmar com a fet històric a partir d'aquest relat: la font el presenta com una llegenda.
```

El mateix criteri s'aplica a taules i gràfics. No preguntis «Què indica aquesta fila?». Pregunta quin resultat concret voldria entendre algú, i explica què comparen les dades abans de donar el valor. Si la font només presenta una llegenda de colors o no dona prou context, no inventis què vol dir la sèrie.

## Patrons que cal rebutjar

- «Què explica la secció X?» / «Què indica aquesta fila?» — depèn de navegar per la font.
- «I dos topònims que en surten:» — no és una resposta completa.
- Una resposta que comença amb «Se la va endur», sense identificar qui ni què.
- Dos torns sobre temes diferents només per fer la conversa multitorn.
- Preguntes de plantilla com «Què és X?» repetides per cada fitxa.
- Preguntes amb una premissa falsa i sense cap motiu recognoscible per creure-la.

## Porta d'aprovació

Reescriu o descarta si, llegida en veu alta sense obrir la font, la conversa no sembla una petició normal d'informació i una resposta útil. Rebutja també qualsevol detall que la font no sostingui, qualsevol seguiment que no surti del torn anterior i qualsevol registre amb drets pendents. No confonguis quantitat de preguntes amb cobertura ni amb qualitat.
