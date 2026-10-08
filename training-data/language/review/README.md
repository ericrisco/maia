# Revisió de Maia Language

`segments.jsonl` conté un objecte `{"text": "…"}` per cada mostra. La mostra
uneix línies de transcripció adjacents i elegibles amb espais; no canvia les
paraules. `provenance.jsonl` té una fila corresponent, en el mateix ordre, amb
els offsets i els hashes de cada fragment font, la fitxa de font, la llicència
i l'estat de redistribució. Les línies amb una marca explícita `[?…]`
s'exclouen, i una marca dubtosa entre dues línies trenca la mostra.

El registre conserva mostres curtes per revisar-les, però el generador les
exclou dels splits si tenen menys de 80 caràcters. Això evita entrenar amb
fragments com «i» o «no» sense context.

Les transcripcions encara no s'han verificat línia per línia contra l'àudio.
Per això cada fila porta `transcript_review_status: audio_verification_pending`.
L'estat no afirma que una paraula incerta sigui correcta. Reviseu aquest camp i
les condicions de cada font abans de tractar la sortida com a final. No barregeu
els fragments amb les converses de Maia Knowledge ni inventeu preguntes o
respostes per completar-los.

El 2026-10-08 s'ha verificat a les metadades individuals de YouTube la llicència
CC BY de les càpsules AR+I **#34, #56 i #57**. La procedència de les **177
mostres** d'aquestes tres peces apunta a les captures guardades a
`docs/raw/parla/ari-capsula-*/`. Això resol només els drets d'aquestes peces;
la transcripció continua pendent de comprovació contra l'àudio i no acredita,
per si sola, que els ponents siguin parlants andorrans.
