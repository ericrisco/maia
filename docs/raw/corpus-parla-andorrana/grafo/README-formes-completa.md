# Graf canònic de les 35 formes candidates

Aquesta capa agrupa els **66 registres de font en 60 persones canòniques** i calcula presència i freqüència per a les **35 formes** de `matriu-formes.tsv`. Les formes provenen de l'ASR i no són trets dialectals confirmats.

- `nodes-formes-completa.tsv`: 60 perfils canònics.
- `trets-formes-completa.tsv`: 35 formes amb cobertura i freqüència.
- `arestes-parlants-formes-completa.tsv`: 1690 parelles amb almenys 3 formes compartides.
- `matriu-formes-completa.tsv`: 2100 cel·les persona-forma.
- `graf-parlants-formes-completa.mmd`: vista Mermaid que mostra només les parelles amb almenys 5 formes.

Les arestes expressen semblança textual entre transcripcions, no identitat de veu ni proximitat dialectal. La confirmació es farà al registre d'audició, que conserva variant, fonètica i prosòdia com a camps separats.

El [quadern de formes representatives](../proveniencia/quadern-formes-representatives.md) ofereix tres contextos ASR temporals per cadascuna de les 35 formes, amb enllaç a la fitxa de la persona. Són mostres de revisió, no confirmacions dialectals.

La vista específica de les formes amb cobertura baixa és [README-formes-escasses.md](README-formes-escasses.md); manté els seus nodes i arestes separats de la lectura completa.
