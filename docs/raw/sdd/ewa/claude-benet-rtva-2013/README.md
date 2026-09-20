---
title: "Entrevista de Claude Benet a RTVA (12-12-2013)"
---

# Entrevista de Claude Benet a RTVA (12-12-2013)

## Procedència

- Emissió: *El Magazín de l'Aliança / Entrevista Claude Benet*.
- Productor: Ràdio i Televisió d'Andorra (RTVA), amb l'Aliança Andorrano-Francesa.
- Data d'emissió: 12 de desembre de 2013.
- Pàgina canònica: <https://www.rtva.ad/programes/entrevista-claude-benet>
- Identificador de contingut observat a la pàgina: `1463521`.
- Identificador de l'àudio: `740861`.
- URL pública de l'MP3:
  <https://mediaverse.rtva.hiway.media/audio/67d19cdd/0_1bczqnzk_0_wplgoxh4_1.mp3>
- Data de recuperació: 12 de setembre de 2026.

El fitxer `rtva-page.html` és una còpia de control de la pàgina pública. L'MP3
original es conserva com `entrevista-claude-benet-2013.mp3`: dura 28:01,85, és
estèreo a 44,1 kHz i té una taxa aproximada de 128 kb/s. L'entrevista pròpiament
dita ocupa aproximadament 06:02–25:44; abans hi ha l'agenda cultural del programa
i després una secció lingüística.

## Integritat

| Fitxer | SHA-256 |
|---|---|
| `entrevista-claude-benet-2013.mp3` | `48d8b662a9bbcce8deed6666cb4601c1ebd383603f68a5cbb90b0672597c9ff0` |
| `rtva-page.html` | `016f076866f2556d243c399cb4524ed8206bf7f4bbb5046164c87a94e78b83f3` |
| `entrevista-2013-tram-06m00-12m00.txt` | `51cdfbec176f4f389d37f3e573af5c24e3a94e58dc4f4bd07abfe1b06eef5168` |
| `entrevista-2013-tram-12m00-18m00.txt` | `4b2f534f50ebdfe42b59895f587582b3f3ef7346fde60cfedb5ce690f163354f` |
| `entrevista-2013-tram-18m00-24m00.txt` | `4430eba472e7f1ef7470e9c7e9621407358f56243ad9499761c97e07d52f5a0e` |
| `entrevista-2013-tram-24m00-28m02.txt` | `5402e32611bc834f5cbf203a854bfd1fed5c241fdd0e349fa22ef08e1fd869cb` |

Els SRT segmentats corresponents també es conserven al directori. Els seus
SHA-256 són, en el mateix ordre cronològic: `63cc030e3041252a7db200c83d5e24c9e159ce3ab0b61cc444f510e4a322d3af`,
`e7781a68928d2a773913614d4cc63d4cc1cbe6ee4bbec8b9f9c6a3ff143c77b5`,
`7948af635fa1c5791d50ef5f30f0f8e919321b897e7afca7ef3211dae967f1a1` i
`45d85b7d70d3916852f14264b835b01c41277841f27daf28452886b61b910672`.

## Transcripció i advertiment crític

La primera passada completa amb `whisper.cpp`, model multilingüe `small`, va
quedar atrapada en una repetició espúria a partir del minut 7. Es conserven
`entrevista-claude-benet-2013.txt`, `.srt` i `.whisper.log` per deixar rastre
del fracàs, però **no són una transcripció utilitzable** després d'aquell punt.

La segona passada reinicia el context cada sis minuts, amb `--max-context 0` i
`--no-fallback`. Els quatre parells `entrevista-2013-tram-*` recuperen l'àudio
sense la repetició. Continuen sent transcripcions automàtiques: deformen noms,
topònims i els canvis francès–català. Serveixen d'índex temporal, no de citació
literal. Abans de citar una frase cal escoltar l'MP3 i normalitzar-la contra
fonts independents.

Correccions clares que no s'han d'importar mecànicament de Whisper:

- `Pater Larry` és la xarxa **Pat O'Leary**;
- `Eva` és **Ewa**;
- `Terrascon`, `Vic de Sos` i `Osat` són **Tarascon-sur-Ariège**, **Vicdessos**
  i **Auzat**;
- `Cigarre` és probablement **Siguer** i `Fontargin` és **Fontargente**;
- `Valle d'Inglès` és la **vall d'Incles**;
- el títol del llibre és *Guies, fugitius i espies. Camins de pas per Andorra
  durant la Segona Guerra Mundial*, no les formes generades pel model.

## Índex temporal de l'entrevista

| Temps | Contingut verificable a l'àudio |
|---|---|
| 06:02–08:27 | Presentació de Benet, del llibre de 2009 i de la seva trajectòria. |
| 08:27–09:48 | Origen de la recerca: una lectura que semblava novel·lesca, recerca de fets, entrevistes a antics passadors encara vius, visites a nombrosos arxius i acumulació documental abans de decidir publicar. |
| 09:48–10:30 | Declaració de mètode: vol reconstruir fets, no escriure una novel·la ni jutjar els actors. |
| 10:39–12:18 | Andorra com a frontissa entre Tolosa, node ferroviari de reunió, i Barcelona, seu del consolat britànic; possibilitat de descans i ocultació als hotels del Principat. |
| 12:18–13:21 | Evolució de les rutes: pas inicial per l'eix de l'Hospitalet i Soldeu; després de l'arribada alemanya a la frontera el novembre de 1942, desplaçament cap a vies més dures i menys vigilables des de Tarascon-sur-Ariège, Vicdessos i Auzat, pels cols del Rat, Siguer i Fontargente. |
| 13:28–14:07 | Benet rebutja com a exagerada la xifra de 200.000 passos i proposa prudentment uns 2.000–3.000 per Andorra, advertint que la clandestinitat impedeix un recompte exacte. |
| 14:07–16:24 | Perfils dels evadits i valor militar dels aviadors; els interrogatoris britànics de retorn com a font rica sobre missions, tripulacions, ajudes i itineraris. |
| 16:25–18:00 | Xarxes: dificultat de comptar-les; primacia inicial de l'organització polonesa i ús britànic de la seva informació; Pat O'Leary i Ewa com les dues xarxes importants que passaren per Andorra, davant Comète al País Basc. Benet explicita que Ewa significa evacuació. |
| 18:24–20:58 | Passadors sobretot espanyols, sovint antics contrabandistes; uns setanta noms recurrents en la seva recerca; retribució econòmica compatible amb risc, jornades llargues i manutenció dels grups. |
| 20:58–22:28 | «Llegenda negra»: admet enriquiments i alguns casos extrems, però els considera minoritaris; separa el lucre del pas de persones del negoci de contraban. |
| 22:28–23:40 | Autoritats andorranes: lectura globalment benvolent i neutral de Francesc Cairat, sotmès a pressió alemanya; referència imprecisa a militars desapareguts per evitar un pretext d'entrada alemanya. |
| 23:44–25:43 | Paper invisibilitzat de les dones. Éloïse com a símbol: vinculada al començament d'una organització d'evasió, desapareguda a Fontargente amb dos aviadors canadencs cap al maig de 1944; Benet encara en cercava la identitat i la família. |

## Què aporta al dossier Ewa

L'emissió fixa una capa pública de la recerca de Benet **set anys anterior** a
l'entrevista de 2020. El 2013 ja descrivia Ewa com una de les dues xarxes
principals que passaren per Andorra, destacava l'avantatge organitzatiu polonès,
les fonts dels interrogatoris britànics i el canvi topogràfic posterior al
novembre de 1942. En canvi, no presenta Józef Węgrzyn, Carlos, Antoni Forné ni
Francesc Viadiu en el fragment dedicat a Ewa. Aquesta absència no prova que
encara ignorés les identitats, però impedeix retroprojectar al 2013 la síntesi
nominal que explicà públicament el 2020.

L'episodi d'Éloïse obre una recerca independent: cal tornar a *Entre el torb i
la Gestapo*, identificar els dos canadencs i contrastar la data i el lloc amb
expedients d'evasió, registres de morts i documentació fronterera. Una notícia
de 2010 la descriu també com a guia desapareguda amb dos aviadors canadencs;
aquesta coincidència periodística és només una pista fins recuperar les fonts
que Benet utilitzà.

## Drets i ús

RTVA manté la pàgina i el fitxer d'àudio públics. La còpia local s'empra per a
verificació, citació temporal i preservació de la procedència dins una recerca
històrica. No es pressuposa una llicència oberta de redistribució; per això el
repositori només versiona aquest `README.md`, mentre l'HTML, l'MP3 i les
transcripcions queden exclosos localment.
