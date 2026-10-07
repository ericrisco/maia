# Revisió de Maia Knowledge

`conversations.jsonl` desa una conversa per línia i només conté missatges visibles. `provenance.jsonl` conserva, en el mateix ordre, les fonts, llicències, afirmacions sostingudes, límits i estat de revisió.

Hi ha converses aprovades i mostres de calibratge. Només els registres amb `review_status: approved` compten com a dades entrenables i cobertura; `approved_sample` no compta. El validador comprova l'estructura, els drets i la cobertura; la checklist humana de [`EXEMPLES.md`](EXEMPLES.md) revisa si el diàleg sona espontani.

Els registres anteriors s'han retirat del fitxer actiu perquè les preguntes depenien de la forma de les fitxes i els seguiments sovint semblaven afegits per rutina. Es poden recuperar de l'historial de Git si cal revisar-los.
