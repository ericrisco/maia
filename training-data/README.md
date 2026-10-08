# Maia Training Data

Espai per preparar dos recursos diferents per a l'ajust fi de Maia:

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb informació de `docs/temes/`.
- **Language** conserva trets del català andorrà contemporani a partir de parla humana de `docs/parla/`.

No es barregen. Els exemples de Knowledge són material de calibratge i no formen part d'un dataset d'entrenament. Language no conté exemples inventats: només s'hi afegirà material humà elegible, verificat i amb drets documentats.

Comença per [el pla](PLAN.md). Encara no hi ha exports per entrenar.

## Estructura

- [`knowledge/examples/`](knowledge/examples/) conté tres exemples curts de calibratge, amb procedència separada. No s'exporten.
- [`knowledge/review/`](knowledge/review/) conté candidates antigues pendents de tornar a revisar. Ser-hi no vol dir que siguin aprovades.
- [`knowledge/work/`](knowledge/work/) guarda la matriu de cobertura i material de treball.
- `knowledge/output/` es reserva per als splits que hagin passat revisió de contingut i drets.
- `language/review/` i `language/work/` es reserven per a parla humana i les seves decisions de verificació.
- `language/output/` es reserva per a material humà verificat i autoritzat.
- `scripts/` es farà servir per a validació i generació quan els formats estiguin estabilitzats.

El JSONL de conversa només porta `messages`, amb missatges `user` i `assistant`. La traçabilitat i les decisions de drets van en fitxers separats. La carpeta de revisió actual no és un export.
