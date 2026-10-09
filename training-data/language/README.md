# Maia Language

Dataset separat per aprendre trets del català andorrà contemporani a partir de parla humana de `docs/parla/`. Només s'hi inclou material elegible segons `docs/CONTRACT.md` i amb una transcripció prou fiable.

No s'inventen torns d'usuari, respostes o diàlegs per fer créixer el volum. Es conserva el text humà amb canvis mínims i traçables. La procedència, el parlant o la peça d'origen i les exclusions s'auditen abans de qualsevol export.

Les carpetes de revisió, treball, informes i output són independents de Maia Knowledge.

## Inventari actual

El primer inventari ha revisat 45 entrades de `docs/parla/`: 40 documents de tipus parla i 5 auxiliars. En resulten 38 peces elegibles, 7 entrades excloses i cap error de Markdown. El report d'elegibilitat reflecteix l'estat general de les fitxes de font, que és pendent; no discrimina llicències individuals de vídeo.

L'auditoria per peça confirma llicència Creative Commons Attribution a les càpsules AR+I #34, #49, #56, #57 i #66. Quatre són elegibles per llengua; la #49 queda exclosa perquè la veu no consta com a originària. Set altres peces AR+I elegibles continuen amb drets pendents. Les 27 entrevistes del Consell General també tenen redistribució pendent. El resum detallat és a `reports/piece-rights.json` i les decisions traçables a `work/piece-rights.jsonl`.

De les peces elegibles s'han extret 10.510 fragments literals (254.983 caràcters). S'han exclòs 5.159 línies de transcripció amb marques d'incertesa. El report registra zero fragments reescrits o generats. Vegeu `work/selection.jsonl`, `work/authentic-segments.jsonl` i els informes a `reports/`.

Encara falten la revisió humana de les transcripcions i la varietat dels parlants, obtenir o confirmar els permisos d'ús, agrupar per peça i parlant, i generar particions. Les llicències obertes de vídeo no validen per si soles la transcripció. Els fragments de treball no són exports finals.
