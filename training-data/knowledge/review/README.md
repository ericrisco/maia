# Revisió de Knowledge

`conversations.jsonl` desa una conversa per línia i només conté els missatges
que veuria l'usuari. `provenance.jsonl` conserva, en el mateix ordre, les fonts,
llicències, afirmacions sostingudes, límits i referències de revisió.

El conjunt anterior s'ha retirat perquè les preguntes sonaven com un qüestionari
sobre les fitxes i alguns seguiments repetien informació. `conversations.jsonl`
ara conté tres mostres per calibrar la naturalitat. La validació comprova
l'estructura i els drets, però no pot decidir si una conversa sona humana.
Consulta [`EXEMPLES.md`](EXEMPLES.md) i revisa les mostres abans de reprendre la
generació de registres.
