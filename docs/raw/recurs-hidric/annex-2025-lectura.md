# Annex del balanç 2025 — FORA_DEL_CORPUS

Font: [PDF del Govern](balanc-hidric-2025.pdf), §9, p. 44–53.
Document datat 20-04-2026; lectura 13-09-2026. Drets pendents; no dataset.
Les pàgines 46–47 i 49–52 s'han contrastat visualment. Les p. 44–45,
48 i 53 s'han llegit en l'extracció textual; el mapa de p. 48 no s'ha
interpretat quantitativament.

## Fórmules que l'extracció no recupera

Transcripció de les expressions numerades de **p. 46** de l'informe:

- (2) `Epa = 16 × (10T/I)^a`.
- (3) `i = (T/5)^1,514`; el text defineix `I` com la suma dels dotze
  índexs mensuals `i`.
- (4) `a = 0,000000675 × I³ − 0,0000771 × I² + 0,01792 × I + 0,49239`.
- (5) `ETP (mm/mes) = Epa × (N/12) × (NDM/30)`.

El document ajusta `N`, hores d'insolació tabulades, a latitud de 42°;
`NDM` és el nombre de dies. Imposa `Epa = 0` si la temperatura mitjana
mensual és igual o inferior a zero. La descripció verbal d'Epa diu que
és calculada per un dia amb dotze hores de sol; no es reformula aquesta
frase ni es valida la implementació real del programari.

## Regles i abast de la lectura

§9.1.2, p. 45–47: càlcul des del gener, inicialitzat amb la reserva del
desembre precedent; neu i pluja incorporades al mateix mes. ETR igual
a ETP quan hi ha aigua suficient; quan s'esgota la reserva, ETR inferior
a ETP i dèficit. Reserva màxima variable amb sòl i pendent, mitjana
citada 8,6 mm. Càlcul anunciat per cel·les de 27,5 × 27,5 m, mentre que
la nota de la figura 52 diu 27 × 27; no s'unifiquen els dos valors.

§9.2, p. 48–49: excedents entesos com a precipitació que escapa de
l'evapotranspiració i de la reserva del sòl; interpretació anual com a
drenatge cap als rius. El mapa s'ha inspeccionat, però no s'han extret
valors de punts concrets ni interpolat entre colors.

§9.3, p. 50: dèficit definit a partir d'ETP i ETR sense reserva disponible.
No s'ha interpretat com a demanda urbana insatisfeta ni com a registre
de restriccions de subministrament.

§9.4, p. 51–52: evolució mensual modelitzada. La taula inferior dona
variacions anuals, no el nivell total de reserva. La figura mostra el
cicle 2016–2025, però les etiquetes automàtiques dels eixos inclouen
dates fora del període amb dades dibuixades. No s'han generat valors
mensuals exactes a partir del gràfic.

## Què queda

Ràsters i sèries originals, valors mensuals numèrics, implementació i
reproducció del balanç; metodologia de reserva citada com Govern 2015.
La discrepància de variació de reserva de 2025 es conserva al
[registre general](recurs-hidric-fora-del-corpus.md). La lectura no resol els drets de reutilització.
