# Revisió de Knowledge

Aquest directori separa les mostres editorials dels registres que es poden
exportar:

- `CONVERSATION-GUIDE.md` defineix la porta de qualitat.
- `EXEMPLES.md` calibra el to amb converses completes i fonts verificables; no
  compta com a dades d'entrenament.
- `conversations.jsonl` conté els candidats en format `messages`; els registres
  antics continuen pendents d'auditoria amb el criteri actual.
- `provenance.jsonl` guarda font, drets i revisió, fora del text que aprendrà el
  model.

No exportis ni donis per aprovats els registres antics fins a revisar-los amb el
criteri actual. No afegeixis una conversa només perquè sigui factualment correcta. Primer
comprova que la pregunta tingui un motiu humà, que cada seguiment reprengui el
fil i que la resposta es pugui verificar. Els registres antics s'han de
revisar amb el criteri actual abans de tractar-los com a aprovats.
