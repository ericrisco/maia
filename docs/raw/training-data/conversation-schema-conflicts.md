# Conflictes d'estructura de les converses

Durant la revisió del JSONL s'han conservat totes les entrades i els seus identificadors. Algunes entrades no seguien cap de les dues formes admeses per l'objectiu (3 missatges o 5 missatges):

- Sis entrades de `training-data/datasets/esports-futbol.jsonl` repetien dues vegades la mateixa pregunta de continuació i el seu assistant buit. S'ha conservat la primera parella.
- Una entrada de `training-data/datasets/institucions-justicia.jsonl` tenia dues preguntes de continuació diferents. S'ha conservat la primera, que pregunta per la identitat del pres i el delicte, i s'ha retirat la segona parella per mantenir una sola continuació.
- 152 entrades de `training-data/datasets/historia-segle-xix.jsonl` i una de `training-data/datasets/historia-origens.jsonl` acabaven amb la pregunta de continuació però sense el missatge assistant buit. S'ha afegit aquest missatge.

Cap línia d'entrada no s'ha eliminat. Aquest canvi normalitza l'estructura dels missatges i manté la continuació sense resposta, tal com demana l'objectiu.
