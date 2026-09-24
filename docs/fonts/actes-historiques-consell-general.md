---
type: font
id: actes-historiques-consell-general
title: "Actes històriques del Consell General (1289-1864)"
titular: Consell General del Principat d'Andorra
autor: institucional
publicacio: "consellgeneral.ad/actes-historiques. Projecte de transcripcio obert, quatre llibres d'actes i vuitanta documents precedents."
url: https://www.consellgeneral.ad/actes-historiques
llicencia: "Publicacio institucional en obert, sense llicencia declarada als llibres d'actes. La sintesi de Guillamet (2024) SI que porta prohibicio expressa de reproduccio."
redistribucio: pendent
data_consulta: 2026-09-17
abast: >
  Les actes del Consell de la Terra i del Consell General transcrites: vuitanta
  documents solts del 1289 al segle XVI i quatre llibres d'actes del 1529 al
  1864. Font primaria andorrana en catala de cada epoca.
notes: >
  COM S'HI ARRIBA. El lloc es Plone i tot son PDF servits sense clau a URL sense
  extensio: cada acta i cada llibre es un PDF encara que l'adreca sembli una
  pagina. CAL MIRAR EL BOM %PDF- abans de descodificar: decodificar bytes de PDF
  com a text no llenca cap error i dona un fitxer illegible que sembla baixat.
  Es el mateix defecte que provar UTF-16 sense mirar el BOM (vegeu bopa.md).
  El text s'extreu amb `pdftotext` i es el que el corpus cita; els PDF son
  gitignorats per R014 (26 MB de binaris).
  Client: `02-DOCS/raw/operations/gap-audit-scripts/baixa_precedents.py`.
  DOS REGIMS DE DRETS, que no es poden barrejar:
  - Els LLIBRES D'ACTES i els DOCUMENTS PRECEDENTS son transcripcions de
    documents d'arxiu public de fa segles, a cura d'Ignasi J. Baiges, Mariona
    Fages i Jordi Guillamet. No hi consta cap nota de drets. El corpus els cita
    i no els republica com a recull.
  - La SINTESI de Jordi Guillamet, "Del Consell de la Terra al Consell General.
    Sindics, subsindics, consellers i consols (1133-2023)" (2024, ISBN
    978-99920-52-52-5), porta copyright de l'autor i del Consell General i la
    frase "La reproduccio total o parcial d'aquesta obra per qualsevol
    procediment [...] resten rigorosament prohibides". NOMES CITACIO.
tema: fonts
veu: compilada
epoca: medieval
apte_llengua: true
timestamp: 2026-09-18T02:00:00Z
tags: [font, historia, consell-general, arxiu, llengua, font-primaria]
---

# Les actes històriques del Consell General

## Què és, i per què importa més que la mida

**Set milions de caràcters de text andorrà primari, del 1289 al 1864**, i **la
xifra no és el que importa.** **El que importa és que està transcrit i datat
document per document**, amb **la signatura arxivística de cadascun**.

| | |
| --- | --- |
| **Documents precedents** | **80 actes soltes**, de **1289 maig 20** al segle XVI, una per fitxer |
| **Llibre I** | **1529-1639** (ASC 32) |
| **Llibre II** | **1637-1682** |
| **Llibre III** | **1682-1744** ([transcripció i extracció local](../raw/consell-general/actes-historiques/llibre-iii-1682-1744.README.md)) |
| **Llibre IV** | **1743-1864** (ANA, ASC núm. 5.860) |

## El document més antic, i què hi ha a dins

**Ruta de col·lació afegida el 23-09-2026:** l’Arxiu Nacional descriu i ofereix
al portal **Arxius en Línia** el volum digital **ASC-16 / Ll-11**, *Llibre d’actes
i comptes del Consell de les Valls d’Andorra*, de **280 folis**, amb dates
**1586–1723** ([fitxa de la font](./asc-00016-llibre-actes-1586-1723.md)). El
corpus encara no n’ha descarregat ni llegit el PDF complet; el registra com a
font primària per col·lacionar les transcripcions dels llibres del segle XVII.

**L'acta del 20 de maig del 1289** —la més antiga del recull— **no és un
document sobre Andorra: és un document d'Andorra**, i **dona els noms dels
pròmens de cada parròquia**:

> «Ací comense lo **Libre de les Ordenacions dels habitans de les vals
> d'Endora**, feytas e ordenades per los pròmens he consellés del **Consel de
> les dites vals d'Endorra** ab lisènsia e voluntat del senyor en Perre, per la
> divinall providènsia **bisbe de Urgell**, e del senyor en **Royger Bernat**,
> per gràcia de Déu **comte de Foys**, a XX del mes de may, en l'an de la
> nativitat de nostre Senyor **Mo CCo LXXXo IXo**»

**Hi consten sis parròquies** —Canillo, Encamp, Ordino, la Massana, Andorra i
Lòria— **amb els seus consellers pel nom**, i **la matèria és la muntanya**:
cabanes, *apreus*, senyalar, i **la quèstia deguda als coprínceps**.

**Un any després del segon Pareatge, el Consell de la Terra ja legisla sobre
pastures amb llicència dels dos senyors.**

## Per a la llengua

**`apte_llengua: true`, i és el primer fons del corpus que ho és de debò per a
l'andorrà antic.** **No és català de Barcelona transcrit a Andorra: és la
grafia andorrana de cada segle** —*Endorra*, *pròmens*, *feytas*, *seynalar*,
*aprés*— **amb cinc-cents setanta-cinc anys de continuïtat documentada.**

## Un defecte d'extracció que cal saber abans de citar

**Els llibres d'actes estan impresos a dues columnes, i `pdftotext` les
intercala.** **Una frase pot continuar dotze línies més avall i, entremig,
n'hi ha una d'una altra columna que parla d'una altra cosa.**

**No fa el text inservible i sí que fa perillosa la citació curta.** **La regla
que el corpus segueix des del 17-09-2026 és aquesta**:

- **Llegir sempre el voltant**, no la línia que ha sortit al `grep`;
- **si una frase no lliga, comprovar si el que s'hi ha colat és d'una altra
  columna** —sol notar-se perquè canvia de matèria de cop;
- **i quan un mot o una xifra no es poden confirmar, dir-ho al costat de la
  citació** en comptes d'arrodonir.

**Les actes soltes i els documents precedents no tenen aquest problema**: són a
una columna.

## Què ha resultat tenir, comprovat article per article

**El 17-09-2026 aquest fons va tancar o avançar més de quaranta buits del corpus
en un sol dia.** **La llista serveix d'índex del que s'hi ha trobat, per si cal
tornar-hi:**

| Matèria | On és |
| --- | --- |
| **Els dos pergamins fundacionals del Consell, 1419**, amb la clàusula que prohibeix actuar contra el bisbe | precedents |
| **L'apel·lació del 1364** i les vuit greuges | precedents |
| **Els dos saigs del 1390**, un per copríncep, i el que es nega | precedents |
| **La citació comtal de 1381, l'execució de privilegis de 1383 i la franquícia de generalitats de 1391** | precedents |
| **La continuïtat de la quèstia, 1394**, la remissió de penes i costos judicials, i la còpia d'un privilegi comercial perdut, **1398** | precedents |
| **La franquesa de la lleuda de Querol i del Maestrat de Ports, 1401–1403**: sentència reial, restitució de penyores i jurament contra el frau | precedents |
| **La ratificació de l'infant Pere del 1335** | precedents |
| **Les ordinacions del 1289 i del 1390** —quèstia, cabanes, i primes per llop, ós i «llop cerver» | precedents |
| **El dret de pas per l'Urgellet, 1341**: un parell de formatges l'any | precedents |
| **El jurament dels veguers**, amb dues negatives i una represa episcopal (1442, 1447, 1456) | precedents |
| **L’avís de gent armada francesa i el bestiar, 1445**: alerta preventiva, responsabilitat del lloctinent i resposta dels jurats | precedents |
| **La quèstia, el crèdit i les fiances, 1446–1456**: 3.000 florins exigits, 500 escuts autoritzats, 35 lliures de «mengeria» i 1.800 florins manllevats | precedents |
| **La consolidació del Consell General, 1448–1498**: procuradors, deutes, patrimoni, defensa i Casa del Consell | precedents |
| **El clam de pau i treva i la marca de la Cerdanya, 1460**: dos procuradors davant el rei i capacitat de composició | precedents |
| **El manament d’homes armats i l’apel·lació del Consell, 1463**: frontera, manca de muralles i defensa pròpia | precedents |
| **La venda d’una casa de Bixessarri, 1464**: sis jurats, domini de les universitats i garantia amb els béns de la Terra | precedents |
| **Els cortals comunals i la tria del jutge, 1480–1482**: llicència de la universitat i jutge escollit per a unes Corts concretes | precedents |
| **La litigació i administració, 1510–1556**: emprius, blat, lleuda, *treta forana*, execució de sentències, pactes i procuradors | precedents |
| **Montsó, 1537**: dos procuradors, privilegis, reparació de greuges i defensa del comerç amb Foix | precedents |
| **El batlle comtal i el jurament dels usos, 1538**: acceptació de Miquel Deulofeu, privilegis escrits i no escrits i justícia per a pobres i rics | precedents |
| **La pau amb Vernet, 1552**: pastors, ferides, procuracions, arbitratge i Reial Audiència | precedents |
| **L’arbitratge entre Siguer, Vicdessos i el Pallars, 1592**: sis compromisaris de la Terra, preses de bestiar i una sentència interrompuda | precedents |
| **El govern quotidià, 1616–1617**: preus, camins, pesca, emprius, càrrecs i memòria dels Pareatges | Llibre I |
| **Les Corts del veguer francès, 1618**: jutge adjunt de Foix i dos arraonadors de la Terra | Llibre I |
| **Els juraments dels batlles i la visura dels camins, 1619**: privilegi prestat al veguer francès, jurament comtal, jurament episcopal per tres anys i inspecció d'un camí | Llibre I |
| **Preus, pesca i certificats, 1619–1622**: aforaments del pa, vi i blat, vedes de truites i certificat parroquial per entrar i sortir | Llibre I |
| **El comissari del rei de França, 1620**: escorta, provisions, privilegis i visita preparada a la Vall | Llibre I |
| **La guarda dels presos i el privilegi de no fer-la gratis, 1621**: requesta al veguer i termini de tres dies | Llibre I |
| **La trencada de la presó i la petició d’un edifici, 1635**: fuga, manca de presó, jurisdicció vacant i ajuda de la quèstia | Llibre I |
| **La frontera, 1631–1633**: sortida del blat, control de la sal, certificats i plet de la lleuda | Llibre I |
| **La plaça de la Vall al col·legi de Foix, 1632**: sentència, privilegi i projecte d’estudis a Toulouse | Llibre I |
| **La plaça del col·legi de Foix i el reemborsament de Rossell, 1636**: disputa sobre l’ocupant, 25 lliures i reserva de la plaça | Llibre I |
| **La forana i els privilegis enviats a París, 1635–1636**: missions a França, actes a Ax i Tarascó i sis privilegis | Llibre I |
| **El privilegi d’entrar a Catalunya en temps de guerra, 1637**: emissaris, papers de Carles V i memorial de Fontanella | Llibre I |
| **Els albarans i la frontera, 1637–1638**: sal, ús propi, vi, guàrdies de ports i sancions | Llibre II |
| **La frontera sanitària, 1640**: avís de contagi a França, prohibició de mercaderies i certificats de pas | Llibre II |
| **El metge cònsol i l’ordre de captura, 1640**: necessitat mèdica, jurisdicció episcopal i defensa del cònsol en cap | Llibre II |
| **La sisena del batlle episcopal, 1640**: sis candidats mentre el Bisbe és absent i el batlle vigent cessa | Llibre II |
| **La nominació del batlle episcopal, 1644**: sis candidats, transmissió de la llista a la Seu i decisió episcopal pendent | Llibre II |
| **Les rendes episcopals i l’arrendament de Beuregart, 1642–1643**: col·lectors parroquials, delmes, presa a França i protestos | Llibre II |
| **El blat de les rendes per als pobres, 1643**: diners de la renda episcopal, compra de gra i termini fins a Tots Sants | Llibre II |
| **El blat reservat i les provisions de l’ermada, 1644**: prohibició de revenda, propi ús, ordi, civada i vi | Llibre II |
| **Els forasters i l’abastament local, 1641**: tres dies d’estada, sal i publicació porta per porta | Llibre II |
| **La sisena del batlle del veguer francès, 1641**: sis candidats, un per parròquia, i càrrec pendent de tria | Llibre II |
| **La reserva de quatre soldats per parròquia, 1644**: emissaris a França, capitans i mobilització eventual a la muntanya | Llibre II |
| **El pres de la Val de Videsós, 1644**: quatre homes enviats a França i topònim conservat amb cautela per una lectura OCR | Llibre II |
| **La guarda del morbo i la llana forastera, 1650–1651**: certificats i portals controlats, sis torns de guàrdia, prohibició porta per porta i reserva de blat | Llibre II |
| **La logística davant els soldats, 1652**: emissaris per desviar-los i farina parroquial per fer pa de munició | Llibre II |
| **La Seu vacant i les rendes episcopals, 1656**: sis informadors a la Seu, col·lectors parroquials i delmes en espècie | Llibre II |
| **La contribució, 1657–1658**: imposició amb diners, bestiar, mercaderies, recaptadors i negociacions d'exempció | Llibre II |
| **Els habitants que fan de capa als forasters, 1661**: franquícia del General, càrregues estrangeres i prohibició porta per porta | Llibre II |
| **L’allotjament de vint-i-tres soldats a Sant Julià, 1659**: Junta interparroquial, despeses i reclamació de la contribució | Llibre II |
| **El Dret de Guerra, 1663–1666**: albarans, testimonis, certificats, Reial Audiència i plet obert | Llibre II |
| **El robatori de Fontargent, 1680**: carta al vicari, recerca armada i informacions sobre els malfactors | Llibre II |
| **Les Corts dels dos veguers i els arraonadors, 1681**: avisos a Foix i la Seu i torns de representació | Llibre II |
| **El jurament del veguer episcopal, 1681**: possessió de Miquel de Senmanat i Requesens a la Casa del Consell | Llibre II |
| **El Dret de Guerra, 1688**: carta de Barcelona, resposta pendent de la Seu i proposta d'un sol dret per bestiar | Llibre III |
| **Quan la llana queda retinguda a Sant Julià, 1690**: llana de Cerdanya, retenció, despatxos i composició amb el governador | Llibre III |
| **La Vall defensa el comerç amb Catalunya amb xifres, 1692**: 628 cases, consums anuals i necessitat del comerç transfronterer | Llibre III |
| **La Vall obliga a acceptar moneda francesa i espanyola, 1693**: preu corrent, publicació porta per porta i responsabilitat dels cònsols | Llibre III |
| **El pleit d’Organyà pel passatge dels Tres Pons, 1683**: procuradors, documents, intimacions i defensa del privilegi | Llibre III |
| **Quan el veguer obre Corts per quatre presos, 1684**: arraonadors, juraments, cartes i avituallament | Llibre III |
| **La Vall posa espies i sometent als ports, 1686**: vigilància, homes armats, Montlluís i dret de la sal | Llibre III |
| **La Vall arma els ports i demana salvaguarda, 1689**: guàrdies per torns, forasters, miquelets i protecció dels governadors | Llibre III |
| **La neutralitat sota pressió militar, 1691**: blat, farratge, miquelets i peticions a París durant el setge de la Seu | Llibre III |
| **El sometent vigila els ports, 1692**: dos homes per parròquia durant una setmana a Perefita, les Portelles i els ports de la frontera | Llibre III |
| **La franquícia de lleudes, 1693**: el privilegi atribuït a Roger Bernat i les lletres de *nihil innovando* contra el cobrament de mules | Llibre III |
| **El blat i la privació de comerç, 1694–1695**: certificats d'ús propi, guàrdies, comissió episcopal i testimonis | Llibre III |
| **La jurisdicció del mas de Tolse, 1695**: lletres d'excomunió rebutjades, privilegis pontificis i rahonadors a la Seu | Llibre III |
| **La concòrdia de Canillo, 1699**: sis representants, ple poder, jurament i còpia autèntica a la caixa del Consell | Llibre III |
| **Un pres de la baronia d'Allés, 1698–1699**: costos limitats, còpia del procés i un lliurament que el baró retarda | Llibre III |
| **La guarda d'Anserall, 1699–1700**: vexacions, carta al governador de la Seu i possible recurs a Barcelona | Llibre III |
| **Una dona presa a Encamp, 1701**: el veguer demana justícia i la Vall invoca els seus privilegis davant dels costos | Llibre III |
| **El ferro i el Dret de Guerra, 1702**: fargues, plet a Barcelona, declaració de càrregues i quatre dobles de sanció | Llibre III |
| **Les herbes migeres, 1702**: Encamp i Canillo alternen cada any el pas del bestiar | Llibre III |
| **La sentència de Sant Julià, 1703**: pas, dues nits i estranys perdonats per mal temps | Llibre III |
| **El prat de Forest i la sentència dels veadors, 1703**: aigua, barreres, visura i costos | Llibre III |
| **La casa d'hostal de Canillo, 1704**: obra aturada, veadors i termini per reprendre-la | Llibre III |
| **La sisena per triar el batlle episcopal, 1704**: sis noms, tria del Bisbe i jurament parroquial | Llibre III |
| **Els Solans d'Ordino, 1708**: límits de bestiar, ban del Quart i tala | Llibre III |
| **El robatori de les mitges de seda i el sometent de Querol, 1712**: lladres, guàrdies, emissaris i indemnització | Llibre III |
| **L'apotecari conduït i els talls, 1713**: botiga, negociació i exempcions fiscals | Llibre III |
| **El pas de Rull per la coma de Sant Joan, 1719–1725**: testimonis, veadors i pas per Querol | Llibre III |
| **La jurisdicció episcopal en el litigi de Canillo, 1724–1725**: ordre del vicari, representacions i indult | Llibre III |
| **Mèrens i els pasturatges d'Encamp i Canillo, 1726**: arrest de Tolosa i defensa de la Vall | Llibre III |
| **Afiliació i masoveria a Sant Julià, 1727**: herbes, talles, penyores i composició | Llibre III |
| **L'albarà i l'ús propi, 1728**: deu per cent, bestiar i dossier de privilegis | Llibre III |
| **El prat de l'Aiguera, 1729**: desviament d'aigua, veadors, restitució i cot | Llibre III |
| **La sentència de la Gunarda, 1729**: empriu, creus de terme, aclariment dels veadors i proves de possessió | Llibre III |
| **La pesca fora del terme, 1733**: llicència parroquial i pèrdua dels instruments | Llibre III |
| **La confirmació reial dels privilegis, 1735**: cinc representants reprenen la petició a Felip V després de les guerres | Llibre III |
| **La guia duanera i el frau de mocadors de seda, 1736**: tres dies de presó per a tres habitants pobres | Llibre III |
| **La mort del Bisbe i la reorganització dels càrrecs, 1737–1738**: sisenes, veguer, batlle i possessió episcopal | Llibre III |
| **La sentència criminal de Guillem Castellà, 1739**: mort violenta, dos veguers, jutge i tres anys de galera | Llibre III |
| **La delegació judicial per la neu, 1742**: jurisdicció civil i criminal, jurament i privilegis conservats | Llibre III |
| **El desterrament perpetu contra el contraban, 1742**: guies, tabac i avís del visitador de la Seu | Llibre III |
| **El conlloc simulat i el cot de les herbes d’Ordino, 1743**: bestiar, cots i ús de les herbes comunals | Llibre IV |
| **La preferència dels naturals en les herbes comunals, 1746**: arrendament, bestiar local i reserva de vuit dies | Llibre IV |
| **El comú de Sant Julià i els arbres del prat, 1750**: sentència arbitral, tanques, aigua i fites | Llibre IV |
| **El bestiar foraster i les herbes d’Encamp, 1761**: Gargantillà, empriu, penyores i 16 lliures de gastos | Llibre IV |
| **La fadiga de les herbes: revocació i retorn, 1764–1765**: disturbis, llibertat d’arrendament i reafirmació de l’ordinació de 1746 | Llibre IV |
| **Quan les avingudes canvien els termes, 1773**: riuades, sis comissions parroquials, possessions i demolició del molí de Coma | Llibre IV |
| **El dret comú per damunt de les lleis veïnes, 1753**: atestat sobre jutges, dret romà i recurs als coprínceps | Llibre IV |
| **L'encabesament de sal, 1743–1748**: 1.400 fanegues anuals i investigació dels contrafactors | Llibre III |
| **La guia de la sal i les hores de la duana, 1744**: Cardona, Sant Julià, tauler, horaris i cots | Llibre IV |
| **El preu de la sal de revena i les fargues, 1764**: hora de plaça, preus màxims, vigilància parroquial i usos de les fargues | Llibre IV |
| **El desterrament dels Nyerros per contraban de tabac, 1748**: bonbosina, trenta-vuit lliures de tabac, cot i defensa | Llibre IV |
| **Quan les Corts s’obren fora de temps, 1754**: presos, veguer, arraonadors i entrega a l’intendent | Llibre IV |
| **L’exili de cinc anys per contravenir les ordenances del tabac, 1757**: Esteve Sansa, Nicolau Senturé, procés i servei militar | Llibre IV |
| **L’edicte del tabac es llegeix porta per porta, 1767**: termini de 24 hores, pregó anual i còpies als llibres parroquials | Llibre IV |
| **Homes armats i forasters sota vigilància, 1768**: cinc homes per parròquia, armes, hostals i presentació davant la justícia | Llibre IV |
| **El blat fiat i el crèdit per abastir la Vall, 1757–1761**: preus del pa, Cerdanya, 465 i 600 càrregues i censals | Llibre IV |
| **La possessió del veguer i les regalies de la Vall, 1758–1759**: Guillem Moles, condicions, submissió i auto episcopal | Llibre IV |
| **La festa de Sant Ermengol i el calendari del Consell, 1762**: 3 de novembre, processó, còpia autèntica i reunió general | Llibre IV |
| **Quan el Bisbe reforça les ordres contra el tabac, 1765**: edictes, pregó, veguer, batlles i inquisicions | Llibre IV |
| **El Consell suspèn el substitut del veguer i endureix el control del tabac, 1771**: privilegi, inspeccions, exili i auxili als contrabandistes | Llibre IV |
| **Quan el veguer retira un ordre sobre els danys del bestiar, 1770**: política de bans, comissió, recurs al príncep i prats comunals | Llibre IV |
| **Quan el Consell defensa els usos davant un procés, 1776**: procés original, provisions, batlle, notari i anul·lació demanada al sobirà | Llibre IV |
| **Quan violenten la caixa de la Casa de la Vall, 1778**: panys trencats, investigació, batlles, cònsols i edictes | Llibre IV |
| **Vint-i-quatre hores i trenta dies de presó per plantar tabac, 1783**: visita general, arrencada, crema pública i justícia alta | Llibre IV |
| **La Vall defensa l’entrada de moneda davant un edicte reial, 1784**: comissió a Barcelona, títols i possessió monetària | Llibre IV |
| **Quan el Bisbe canvia el batlle i la Vall nomena un interí, 1786**: renúncia de Riba, nomenament de Jaume Areny Calbó i jurament a Canillo | Llibre IV |
| **El Consell prohibeix joc i tabola als hostals, 1785**: cartes, soroll, detenció, contraban i dobla d’or | Llibre IV |
| **Quatre presos cap a Barcelona, amb sis homes armats, 1788**: procés, lliurament al capità general i protesta contra la pena capital | Llibre IV |
| **El nou veguer francès i les dues sisenes de batlle, 1788**: possessió, sis noms per copríncep i renovació judicial | Llibre IV |
| **El blat s’ha de netejar i vendre amb control públic, 1789**: neteja, magatzem públic, permís de comerç i preu corrent | Llibre IV |
| **Tres-cents o quatre-cents homes armats amenacen la Vall des de l’Hospitalet, 1790**: alarma d’Encamp i Canillo i defensa dels comuns | Llibre IV |
| **Qui exerceix la jurisdicció d’Andorra? La resposta del Consell, 1775**: jurisdicció compartida, jutges, veguers, batlles i edicte contra fraus | Llibre IV |
| **El nomenament del veguer Franès Morou, 1703**: privilegi de Versalles, presa de possessió i jurament davant del Consell | Llibre III |
| **La doble obertura de Corts, 1704**: Morou obre i tanca, Cruïlles intenta reobrir i el Consell ho contradiu | Llibre III |
| **Presos trets de la Vall, 1686–1687**: reclama a la Seu, al Bisbe i a Perpinyà, amb cinc dobles de despesa | Llibre III |
| **Els presos i els dos veguers, 1703**: missió a Acs, missió a la Seu i escala fins al Bisbe | Llibre III |
| **La sèrie de la quèstia comtal del segle XV**, sempre a crèdit | precedents |
| **La cluseda per contagi del 1628-1630**: soldats, guardes, certificats, campanes | Llibre I |
| **[La cacera de bruixes entra al govern del Consell (1621)](../temes/institucions/justicia/la-cacera-de-bruixes-entra-al-govern-del-consell-1621.md)**: finançament, rahonadors, vigilància, execució i cobraments | Llibre I |
| **El règim de la farga** i els treballadors francesos, 1629 | Llibre I |
| **L'*afor*, 1744-1795**, i el preu del vi, el pa, les truites i les perdius | Llibres I-IV |
| **La *conducta* de metges, barber, advocats i llosador**, des del 1624 | Llibres I-IV |
| **La prohibició del tabac, 1731-1733**, i el permís de conreu del 1791 | Llibres III i IV |
| **L'acta del 23 de març de 1775** i l'edicte contra la gent vaga | Llibre IV |
| **El canvi de la moneda francesa, 1723** | Llibre III |
| **Els *manadors*** i el torn de casa | Llibres II-IV |
| **Els darrers pagaments de la quèstia i els passos tancats, 1863–1864**: pagaments als dos coprínceps, comissió a Madrid i certificats de bestiar | Llibre IV |

## Related

- [El BOPA](./bopa.md) — la sèrie que comença on aquesta s'acaba, el 1989.
