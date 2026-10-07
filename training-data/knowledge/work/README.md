# Treball intern de Knowledge

Aquí aniran els inventaris per tema i les notes que connecten cada conversa amb
els fets que la sostenen. No s'hi posen preguntes artificials per omplir buits.

`document-status.json` és la revisió humana per fitxa. Les fitxes comencen com a
`not_started`; una conversa les passa només a `in_progress`. Només es marca
`complete` després de llegir totes les seccions, taules, llistes, dates, xifres,
relacions i buits. Si no hi ha cap pregunta natural, es marca
`no_natural_question` i s'explica el motiu.

Regenera l'inventari i el report amb `../scripts/build_document_inventory.py`.
