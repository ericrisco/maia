"""Apply hand-authored Catalan paraphrase sets to the canon augmentation pilot."""

from __future__ import annotations

import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "training-data/datasets/canon-augmentat.jsonl"

ANSWER_FORMS = {
    "fhasa-concessio": [
        "La concessió atorgada a Andreu Boussac i Llorenç Gómez Quintana per a FHASA es remunta al 27 de març de 1929.",
        "El 27 de març de 1929 es va atorgar a Andreu Boussac i Llorenç Gómez Quintana la concessió de FHASA.",
        "A Andreu Boussac i Llorenç Gómez Quintana els fou adjudicada FHASA el 27 de març de 1929.",
        "L’atorgament de FHASA es remunta al 27 de març de 1929; en van ser adjudicataris Andreu Boussac i Llorenç Gómez Quintana.",
        "El 27-03-1929 marca la concessió de FHASA als concessionaris Andreu Boussac i Llorenç Gómez Quintana.",
        "FHASA va quedar concedida el 27 de març de 1929 a Andreu Boussac i Llorenç Gómez Quintana.",
        "FHASA va passar a Andreu Boussac i Llorenç Gómez Quintana per concessió el 27-03-1929.",
        "El 27 de març de 1929 es va tancar l’atorgament de FHASA; Andreu Boussac i Llorenç Gómez Quintana en van ser els concessionaris.",
        "Andreu Boussac i Llorenç Gómez Quintana van passar a ser titulars de FHASA en l’atorgament datat el 27 de març de 1929.",
        "Els titulars de la concessió de FHASA van ser Andreu Boussac i Llorenç Gómez Quintana; l’atorgament es va fer el 27 de març de 1929.",
        "la data fou el 27 de març de 1929; Andreu Boussac i Llorenç Gómez Quintana van ser-ne els concessionaris.",
    ],
    "fhasa-reserva-10-per-cent": [
        "Els concessionaris de FHASA es van comprometre a reservar el 10 % de la producció elèctrica per al país.",
        "Una desena part de l’electricitat produïda quedava reservada per al país, segons el compromís dels concessionaris de FHASA.",
        "Per a Andorra, els concessionaris de FHASA van pactar una reserva del 10 % de tota la producció elèctrica.",
        "El compromís de FHASA destinava al país una dècima part de l’energia elèctrica produïda.",
        "El 10 % de la producció elèctrica era la quota que els concessionaris de FHASA havien de reservar per al país.",
        "Els concessionaris van assumir que una de cada deu parts de l’electricitat produïda per FHASA es guardaria per al país.",
        "La reserva compromesa pels titulars de FHASA corresponia a un 10 % de la producció elèctrica de FHASA per al país.",
        "Del total d’electricitat generada, n’havia de quedar un 10 % per al país per acord dels concessionaris de FHASA.",
        "Per al país es va preveure una desena part de la producció elèctrica, d’acord amb els concessionaris de FHASA.",
        "Els titulars de la concessió van oferir reservar una quota elèctrica del 10 % per a Andorra.",
        "De cada cent unitats elèctriques produïdes per FHASA, els titulars havien de reservar-ne deu per al país.",
    ],
    "tabac-prohibicio-conreu": [
        "El primer acord del Consell General que prohibia plantar tabac es va aprovar el 18 de juny de 1731.",
        "El 18 de juny de 1731, el Consell General va aprovar per primer cop una prohibició del conreu del tabac.",
        "La primera prohibició del Consell General sobre el cultiu de tabac porta data de 18 de juny de 1731.",
        "L’acord inicial contra la plantació de tabac es va votar al Consell General el 18 de juny de 1731.",
        "El Consell General va barrar per primera vegada el conreu del tabac amb l’acord aprovat el 18 de juny de 1731.",
        "El 18-06-1731 va quedar aprovada la primera mesura del Consell General que impedia plantar tabac.",
        "La data de l’acord inaugural del Consell General contra el tabac és el 18 de juny de 1731.",
        "En el seu primer acord sobre tabac, el Consell General va prohibir-ne la plantació el 18 de juny de 1731.",
        "El conreu del tabac va quedar prohibit pel primer acord del Consell General, aprovat el 18 de juny de 1731.",
        "La primera resolució del Consell General sobre el tabac va arribar el 18 de juny de 1731 i en vetava la plantació.",
        "el Consell General va aprovar la seva primera prohibició de plantar tabac el 18 de juny de 1731.",
    ],
    "grandvalira-marca-2003": [
        "La marca Grandvalira es va crear l’hivern del 2003.",
        "L’hivern de 2003 va veure néixer la marca Grandvalira.",
        "Grandvalira va començar a existir com a marca durant l’hivern del 2003.",
        "El naixement de la marca Grandvalira se situa a l’hivern del 2003.",
        "L’hivern del 2003 és el moment en què es va crear Grandvalira com a marca.",
        "La creació de Grandvalira com a marca es va produir l’hivern del 2003.",
        "La denominació comercial que va néixer aquell hivern fou Grandvalira, creada el 2003.",
        "Al 2003, durant l’hivern, es va donar forma a la marca Grandvalira.",
        "La marca que va sorgir aquell hivern de 2003 va ser Grandvalira.",
        "Grandvalira va prendre forma de marca l’hivern del 2003.",
        "la marca Grandvalira va néixer durant l’hivern del 2003.",
    ],
    "tabac-revolta-1733": [
        "El copríncep episcopal va recular el 1733 davant d’uns dos-cents andorrans armats que impedien arrencar el tabac.",
        "Uns dos-cents andorrans armats van fer retrocedir el copríncep quan aquest es disposava a arrencar les plantes de tabac, el 1733.",
        "L’intent d’arrencar les plantes va acabar amb la retirada del copríncep episcopal davant d’uns dos-cents andorrans armats el 1733.",
        "El 1733 es va frustrar l’acció del copríncep episcopal contra el tabac: dos-cents andorrans armats el van fer recular.",
        "La revolta del tabac va fer recular el copríncep episcopal. Hi van prendre part uns dos-cents andorrans armats el 1733.",
        "Quan el copríncep episcopal va intentar arrencar tabac, uns dos-cents andorrans armats el van obligar a retirar-se; era el 1733.",
        "La plantació de tabac va ser defensada el 1733 per uns dos-cents andorrans armats, que van fer recular el copríncep episcopal.",
        "El bisbe-príncep no va poder arrencar les plantes: dos-cents andorrans armats el van fer retrocedir l’any 1733.",
        "L’any 1733, el copríncep episcopal va haver de fer marxa enrere davant d’uns dos-cents andorrans armats que protegien les plantes de tabac.",
        "Van ser uns dos-cents andorrans armats els qui van forçar la retirada del copríncep episcopal quan volia arrencar tabac, el 1733.",
        "la temptativa del copríncep episcopal d’arrencar el tabac es va aturar el 1733 davant la resistència armada d’uns dos-cents andorrans.",
    ],
    "tabac-monopoli-espanya": [
        "Al segle XVIII, l’elaboració del tabac a Espanya era monopoli de l’Estat.",
        "L’Estat espanyol concentrava en exclusiva la fabricació del tabac al segle XVIII.",
        "Durant el segle XVIII, a Espanya només l’Estat podia elaborar tabac.",
        "La producció de tabac elaborat a Espanya estava reservada a l’Estat en el segle XVIII.",
        "A l’Espanya del segle XVIII, el monopoli de l’elaboració tabaquera pertanyia a l’Estat.",
        "El tabac no s’elaborava lliurement a Espanya: al segle XVIII aquesta activitat era monopoli estatal.",
        "Era l’Estat qui controlava tota l’elaboració del tabac espanyol durant el segle XVIII.",
        "El monopoli estatal comprenia l’elaboració del tabac a Espanya en aquella centúria.",
        "La fabricació tabaquera a Espanya depenia exclusivament de l’Estat durant el segle XVIII.",
        "L’elaboració espanyola del tabac quedava sota control exclusiu de l’Estat al segle XVIII.",
        "l’Estat tenia el monopoli de fabricar tabac a Espanya durant el segle XVIII.",
    ],
    "grandvalira-telesqui-1956": [
        "Francesc Viladomat va instal·lar el primer telesquí de la zona de Grandvalira el 1956.",
        "El primer telesquí de Grandvalira va ser obra de Francesc Viladomat i es va posar en servei el 1956.",
        "Francesc Viladomat va posar el primer remuntador d’aquest tipus a la zona de Grandvalira el 1956.",
        "Francesc Viladomat és qui va instal·lar el telesquí inaugural de la zona l’any 1956.",
        "El primer giny de remuntada de Grandvalira es va instal·lar el 1956 per iniciativa de Francesc Viladomat.",
        "La zona de Grandvalira va tenir el seu primer telesquí el 1956, instal·lat per Francesc Viladomat.",
        "Al 1956, la instal·lació inicial del telesquí de Grandvalira la va fer Francesc Viladomat.",
        "El primer telesquí que va funcionar a la zona de Grandvalira el va instal·lar Viladomat l’any 1956.",
        "La instal·lació del primer telesquí de Grandvalira va anar a càrrec de Francesc Viladomat el 1956.",
        "La primera instal·lació de telesquí de la zona es remunta al 1956 i la va fer Francesc Viladomat.",
        "la primera instal·lació de telesquí de Grandvalira la va posar Francesc Viladomat el 1956.",
    ],
    "vallnord-estacions-agrupades": [
        "Vallnord agrupava comercialment Pal Arinsal i Ordino Arcalís.",
        "Sota la marca Vallnord hi havia Pal Arinsal i Ordino Arcalís.",
        "Pal Arinsal i Ordino Arcalís formaven l’agrupació comercial anomenada Vallnord.",
        "La marca comercial Vallnord reunia els dominis de Pal Arinsal i Ordino Arcalís.",
        "Ordino Arcalís s’integrava amb Pal Arinsal dins l’agrupació comercial Vallnord.",
        "Vallnord reunia exactament dues estacions, anomenades Pal Arinsal i Ordino Arcalís.",
        "Vallnord feia de marca comuna per a Pal Arinsal i Ordino Arcalís.",
        "Pal Arinsal juntament amb Ordino Arcalís constituïen Vallnord com a agrupació comercial.",
        "La unió comercial inclosa sota Vallnord corresponia a Pal Arinsal i Ordino Arcalís.",
        "El nom Vallnord agrupava les estacions de Pal Arinsal i Ordino Arcalís.",
        "les estacions de Pal Arinsal i Ordino Arcalís figuraven plegades sota la marca Vallnord.",
    ],
    "banca-secret-2018": [
        "El secret bancari a Andorra va desaparèixer el 2018.",
        "L’any 2018 va marcar la fi del secret bancari andorrà.",
        "Andorra va deixar enrere el secret bancari durant el 2018.",
        "El secret bancari va tenir el seu final al Principat l’any 2018.",
        "La desaparició del secret bancari a Andorra es va produir el 2018.",
        "El model de secret bancari es va acabar a Andorra el 2018.",
        "Al 2018, el secret bancari andorrà va quedar extingit.",
        "Va ser el 2018 quan es va posar fi al secret bancari d’Andorra.",
        "Andorra va tancar l’etapa del secret bancari el 2018.",
        "El final del secret bancari al país correspon a l’any 2018.",
        "la pràctica del secret bancari va desaparèixer a Andorra el 2018.",
    ],
    "escola-andorrana-1982": [
        "El Govern va crear l’Escola Andorrana el 1982.",
        "L’Escola Andorrana va néixer per iniciativa del Govern l’any 1982.",
        "Va ser el 1982 que el Govern va posar en marxa l’Escola Andorrana.",
        "El 1982 marca la creació de l’Escola Andorrana pel Govern.",
        "La fundació de l’Escola Andorrana es va fer el 1982 des del Govern.",
        "L’any 1982 es va establir el centre educatiu anomenat Escola Andorrana per decisió governamental.",
        "L’entitat educativa que el Govern va establir el 1982 porta el nom d’Escola Andorrana.",
        "L’Escola Andorrana començà el 1982 com a iniciativa del Govern.",
        "La creació governamental de l’Escola Andorrana correspon al 1982.",
        "El projecte escolar que va impulsar el Govern el 1982 va ser l’Escola Andorrana.",
        "la institució educativa andorrana es va crear l’any 1982 per obra del Govern.",
    ],
    "carlemany-carta-pobla": [
        "La Carta Pobla que atribueix a Carlemany la fundació d’Andorra és un pergamí fals.",
        "És fals el pergamí de la Carta Pobla que presenta Carlemany com a fundador d’Andorra.",
        "El document que fa de Carlemany el fundador d’Andorra no és autèntic: es tracta d’un pergamí fals.",
        "La suposada Carta Pobla carolíngia és falsa; atribueix a Carlemany la fundació del país.",
        "No és genuí el pergamí anomenat Carta Pobla que vincula Carlemany amb la fundació d’Andorra.",
        "La falsedat és el pergamí que adjudica a Carlemany l’origen d’Andorra sota el nom de Carta Pobla.",
        "El relat de la fundació per Carlemany apareix en una Carta Pobla que és un pergamí fals.",
        "La Carta Pobla carolíngia que atribueix la fundació andorrana a Carlemany és apòcrifa.",
        "Un pergamí fals és el suport de la Carta Pobla que fa fundador d’Andorra a Carlemany.",
        "El pergamí de la Carta Pobla no és autèntic, tot i atribuir a Carlemany la fundació del país.",
        "la fundació d’Andorra atribuïda a Carlemany es basa en un pergamí fals conegut com a Carta Pobla.",
    ],
    "pareatge-1278": [
        "El primer Pareatge es va signar a Lleida el 8 de setembre de 1278.",
        "Lleida va ser el lloc on es va signar el primer Pareatge el 8 de setembre de 1278.",
        "La signatura inicial dels Pareatges es va fer a Lleida en la data del 8 de setembre de 1278.",
        "El 8-09-1278 es va formalitzar a Lleida el primer acord de Pareatge.",
        "L’acord conegut com el primer Pareatge porta data de 8 de setembre de 1278 i es va signar a Lleida.",
        "La data del 8 de setembre de 1278 i la ciutat de Lleida corresponen a la signatura del Pareatge inicial.",
        "L’any 1278, el dia 8 de setembre, es va subscriure a Lleida el primer Pareatge.",
        "La signatura del Pareatge inicial es va fer a la ciutat de Lleida el dia 8 de setembre de 1278.",
        "A la ciutat de Lleida es va formalitzar el primer Pareatge en la jornada del 8 de setembre de 1278.",
        "La data del primer Pareatge és el 8 de setembre de 1278; Lleida n’és el lloc de signatura.",
        "el 8 de setembre de 1278 es va signar a Lleida el pacte inicial de Pareatge.",
    ],
    "pareatge-1288": [
        "El segon Pareatge es va signar el 1288.",
        "La signatura del Pareatge número dos correspon a l’any 1288.",
        "El segon dels Pareatges va quedar subscrit el 1288.",
        "Va ser l’any 1288 quan es va formalitzar el segon Pareatge.",
        "La data de signatura del segon acord de Pareatge és 1288.",
        "El 1288 es va rubricar el pacte conegut com a segon Pareatge.",
        "El segon pacte de Pareatge porta l’any 1288 com a data de signatura.",
        "L’acord que va seguir al primer Pareatge es va signar el 1288.",
        "La subscripció del segon Pareatge es remunta a 1288.",
        "El número dos dels Pareatges va ser signat durant l’any 1288.",
        "el segon acord de Pareatge va quedar signat l’any 1288.",
    ],
    "manual-digest-1748": [
        "Antoni Fiter i Rossell va redactar el Manual Digest el 1748.",
        "El Manual Digest és obra d’Antoni Fiter i Rossell, que el va escriure el 1748.",
        "La redacció del Manual Digest la va fer Antoni Fiter i Rossell l’any 1748.",
        "L’any 1748 va quedar enllestit el Manual Digest de la mà d’Antoni Fiter i Rossell.",
        "L’autor del Manual Digest és Antoni Fiter i Rossell; la redacció data de 1748.",
        "Fiter i Rossell en va ser l’autor; el Manual Digest es redactà el 1748.",
        "La compilació anomenada Manual Digest va sortir de la ploma de Fiter i Rossell el 1748.",
        "El 1748 va quedar redactada per Antoni Fiter i Rossell l’obra titulada Manual Digest.",
        "El Manual Digest va sortir de la ploma de Fiter i Rossell durant l’any 1748.",
        "Al 1748 es va completar la redacció del Manual Digest per Antoni Fiter i Rossell.",
        "l’obra de Fiter i Rossell anomenada Manual Digest va ser redactada el 1748.",
    ],
    "politar-1763": [
        "El Politar andorrà es va publicar el 1763 com a text complementari del Manual Digest.",
        "Com a complement del Manual Digest, el Politar andorrà va aparèixer publicat el 1763.",
        "L’any 1763 va sortir a la llum el Politar andorrà, obra que complementa el Manual Digest.",
        "La publicació del Politar andorrà data de 1763 i el presenta com a complement del Manual Digest.",
        "El Manual Digest té com a text complementari el Politar andorrà, editat el 1763.",
        "El 1763 es va donar a conèixer el Politar andorrà en funció complementària del Manual Digest.",
        "El Politar, complementari del Manual Digest, es va imprimir l’any 1763.",
        "Va ser el 1763 quan es va publicar el text andorrà que complementa el Manual Digest: el Politar.",
        "L’any 1763 va veure la publicació d’una obra que completava el Manual Digest: el Politar andorrà.",
        "El text que acompanya el Manual Digest és el Politar andorrà; la seva publicació es va fer el 1763.",
        "el 1763 es va publicar el Politar andorrà com a complement del Manual Digest.",
    ],
    "nova-reforma-1866": [
        "La Nova Reforma de 1866 va establir que els caps de casa elegissin els consellers generals.",
        "Els caps de casa van obtenir el dret d’escollir els consellers generals amb la Nova Reforma del 1866.",
        "El 1866, la Nova Reforma va confiar als caps de casa l’elecció dels consellers generals.",
        "La reforma coneguda com a Nova Reforma va fer electors dels caps de casa per als consellers generals l’any 1866.",
        "L’elecció dels consellers generals per part dels caps de casa va quedar establerta el 1866 amb la Nova Reforma.",
        "Amb la Nova Reforma de 1866, els caps de casa passaren a triar els consellers generals.",
        "La Nova Reforma va obrir als caps de casa la tria dels consellers generals; això es va fixar el 1866.",
        "L’any 1866 es va aprovar que els caps de casa triessin els consellers generals, dins la Nova Reforma.",
        "Els consellers generals havien de ser elegits pels caps de casa segons la Nova Reforma de 1866.",
        "La decisió de 1866 atribuïda a la Nova Reforma va ser deixar l’elecció general als caps de casa.",
        "la Nova Reforma va introduir el 1866 l’elecció dels consellers generals pels caps de casa.",
    ],
    "constitucio-1993": [
        "El Consell General va aprovar el text de la Constitució el 2 de febrer de 1993.",
        "El 2 de febrer de 1993 es va aprovar al Consell General el text constitucional.",
        "La cambra legislativa va donar llum verda al text de la Constitució el 02-02-1993.",
        "La data d’aprovació parlamentària de la Constitució és el 2 de febrer de 1993.",
        "Al Consell General li correspon l’aprovació del text constitucional, feta el 2 de febrer de 1993.",
        "El text de la Constitució va obtenir l’aprovació del Consell General el febrer del 1993, concretament el dia 2.",
        "El 1993, el dia 2 de febrer, el Consell General va aprovar la Constitució.",
        "La Constitució va passar pel Consell General i aquest n’aprovà el text el 2 de febrer de 1993.",
        "El text constitucional va rebre la llum verda parlamentària en la sessió del 2 de febrer de 1993.",
        "El segon dia de febrer del 1993 va quedar aprovat el text de la Constitució pel Consell General.",
        "la data en què el Consell General aprovà el text constitucional fou el 2 de febrer de 1993.",
    ],
    "referendum-1993": [
        "El poble va ratificar la Constitució d’Andorra en referèndum el 14 de març de 1993.",
        "La ratificació popular de la Constitució es va fer en referèndum el 14 de març de 1993.",
        "El 14 de març de 1993, la ciutadania va validar la Constitució andorrana mitjançant referèndum.",
        "La Constitució d’Andorra va rebre l’aprovació del poble en la consulta del 14-03-1993.",
        "En referèndum, els electors van ratificar el text constitucional el 14 de març de 1993.",
        "El resultat polític de la consulta popular del 14 de març de 1993 va ser la ratificació de la Constitució.",
        "El poble andorrà va donar el vistiplau a la Constitució en el referèndum celebrat el 14 de març de 1993.",
        "La votació referendària que va ratificar la Constitució va tenir lloc el 14 de març de 1993.",
        "El 14 de març de 1993, els votants van validar la Constitució mitjançant una consulta referendària.",
        "La ciutadania va confirmar la Constitució del país en referèndum el 14 de març de 1993.",
        "el referèndum del 14 de març de 1993 va servir perquè el poble ratifiqués la Constitució d’Andorra.",
    ],
    "onu-1993": [
        "Andorra va ser admesa a les Nacions Unides el 28 de juliol de 1993.",
        "L’ingrés d’Andorra a l’ONU es va produir el 28 de juliol de 1993.",
        "El país pirinenc d’Andorra es va incorporar a l’ONU el 28 de juliol de 1993.",
        "La data d’admissió andorrana a l’ONU és el 28-07-1993.",
        "Les Nacions Unides van acceptar Andorra com a membre el 28 de juliol de 1993.",
        "Andorra va entrar a formar part de l’Organització de les Nacions Unides el 1993, el 28 de juliol.",
        "Va ser el 28 de juliol de 1993 que l’ONU va admetre Andorra.",
        "L’adhesió del Principat a les Nacions Unides porta la data del 28 de juliol de 1993.",
        "El país es va incorporar a l’ONU amb l’admissió del 28 de juliol de 1993.",
        "Les Nacions Unides van obrir les portes a Andorra el 28 de juliol de 1993.",
        "la data d’ingrés d’Andorra a l’organització mundial fou el 28 de juliol de 1993.",
    ],
    "consell-europa-1994": [
        "Andorra va entrar al Consell d’Europa el 1994.",
        "L’adhesió andorrana al Consell d’Europa data de l’any 1994.",
        "El Principat es va incorporar al Consell d’Europa durant el 1994.",
        "Va ser el 1994 quan Andorra va passar a formar part del Consell d’Europa.",
        "El Consell d’Europa compta amb Andorra des del 1994.",
        "La incorporació del país a l’organització europea es va fer el 1994.",
        "L’any 1994 va tenir lloc l’adhesió d’Andorra a aquesta institució europea.",
        "El 1994 va tenir lloc l’entrada del Principat al Consell d’Europa.",
        "Andorra forma part del Consell d’Europa des de 1994.",
        "La data d’ingrés andorrà al Consell d’Europa és el 1994.",
        "el Principat va esdevenir membre del Consell d’Europa el 1994.",
    ],
    "oscar-ribas-primer-cap": [
        "Òscar Ribas Reig va ser el primer cap de Govern d’Andorra.",
        "El càrrec inaugural de cap de Govern va recaure en Òscar Ribas Reig.",
        "Òscar Ribas Reig va ocupar la direcció del Govern andorrà abans que cap altre.",
        "El primer titular del cap de Govern d’Andorra fou Òscar Ribas Reig.",
        "Andorra va tenir en Òscar Ribas Reig el seu cap de Govern inicial.",
        "La primera persona al capdavant del Govern del país va ser Òscar Ribas Reig.",
        "La primera persona que va dirigir l’executiu andorrà fou Òscar Ribas Reig.",
        "El Govern andorrà va tenir com a primer cap Òscar Ribas Reig.",
        "La primacia en el càrrec de cap de Govern correspon a Òscar Ribas Reig.",
        "El nom de qui va obrir la llista de caps de Govern és Òscar Ribas Reig.",
        "la primera jefatura del Govern d’Andorra la va exercir Òscar Ribas Reig.",
    ],
    "marc-forne-cap": [
        "Marc Forné Molné va ser cap de Govern del 7 de desembre de 1994 al maig de 2005.",
        "Entre el 7 de desembre de 1994 i el maig de 2005, el cap de Govern era Marc Forné Molné.",
        "El mandat de Marc Forné Molné al capdavant del Govern va començar el 7 de desembre de 1994 i es va acabar el maig de 2005.",
        "La capitania de Govern de Marc Forné Molné s’estén entre el 7-12-1994 i el maig del 2005.",
        "Entre el desembre de 1994 i el maig de 2005, l’executiu va tenir Marc Forné Molné com a cap.",
        "La trajectòria de Marc Forné Molné al capdavant de l’executiu cobreix el tram del 7 de desembre de 1994 fins al maig de 2005.",
        "El 7 de desembre de 1994 va començar l’etapa de Marc Forné Molné com a cap de Govern, acabada el maig de 2005.",
        "La direcció governamental va correspondre a Marc Forné Molné durant el període que va del 7 de desembre de 1994 al maig de 2005.",
        "Marc Forné Molné va ocupar la presidència del Govern entre finals de 1994 i maig de 2005, a partir del dia 7 de desembre.",
        "El cap de Govern nomenat el 7 de desembre de 1994 era Marc Forné Molné; el seu període va acabar el maig de 2005.",
        "el Govern va ser encapçalat per Marc Forné Molné des del 7 de desembre del 1994 fins al maig del 2005.",
    ],
    "albert-pintat-cap": [
        "Albert Pintat va ser cap de Govern del 2005 al 2009.",
        "La direcció del Govern va correspondre a Albert Pintat entre 2005 i 2009.",
        "Albert Pintat va encapçalar l’executiu durant el període 2005–2009.",
        "El mandat de Pintat al capdavant del Govern va abastar els anys 2005 a 2009.",
        "El Govern va ser dirigit per Albert Pintat en el període comprès entre 2005 i 2009.",
        "La direcció del Govern va tenir Albert Pintat com a titular entre 2005 i 2009.",
        "Albert Pintat va dirigir el Govern al llarg del tram comprès entre 2005 i 2009.",
        "Els anys 2005, 2006, 2007, 2008 i 2009 corresponen al període de Pintat com a cap de Govern.",
        "Albert Pintat va presidir el Govern durant el quinquenni que va del 2005 al 2009.",
        "L’etapa de cap de Govern d’Albert Pintat es va situar del 2005 al 2009.",
        "la direcció governamental d’Albert Pintat es va estendre del 2005 al 2009.",
    ],
    "antoni-marti-cap": [
        "Antoni Martí va ser cap de Govern del 2011 al 2019.",
        "La direcció del Govern va ser ocupada per Antoni Martí entre 2011 i 2019.",
        "Antoni Martí va dirigir l’executiu al llarg del període 2011–2019.",
        "El mandat de Martí com a cap de Govern s’estén del 2011 fins al 2019.",
        "Antoni Martí va encapçalar el Govern andorrà al llarg del període 2011–2019.",
        "El càrrec de cap de Govern va correspondre a Antoni Martí durant els anys 2011 a 2019.",
        "Antoni Martí ocupà la direcció governamental entre l’any 2011 i l’any 2019.",
        "La etapa de govern de Martí comença el 2011 i arriba fins al 2019.",
        "Antoni Martí va tenir a càrrec l’executiu del 2011 al 2019.",
        "El període 2011–2019 identifica els anys d’Antoni Martí com a cap de Govern.",
        "el Govern andorrà va ser dirigit per Antoni Martí des del 2011 fins al 2019.",
    ],
    "federacio-futbol": [
        "La Federació Andorrana de Futbol es va fundar el 1994.",
        "La FAF va néixer l’any 1994.",
        "El 1994 es va crear la Federació Andorrana de Futbol.",
        "La fundació de l’organisme rector del futbol andorrà data de 1994.",
        "La Federació Andorrana de Futbol va iniciar la seva trajectòria el 1994.",
        "Andorra va constituir la seva federació futbolística l’any 1994.",
        "La creació de la FAF correspon a l’any 1994.",
        "El futbol andorrà té federació pròpia des de 1994.",
        "L’entitat nacional que regeix el futbol es va fundar el 1994.",
        "L’any de naixement de la Federació Andorrana de Futbol és 1994.",
        "el 1994 es va fundar l’organisme federatiu del futbol andorrà.",
    ],
    "basquet-1998-imbatut": [
        "La selecció andorrana de bàsquet va guanyar invicta el Campionat d’Europa de Països Petits del 1998.",
        "Andorra no va perdre cap partit en proclamar-se campiona europea de països petits el 1998.",
        "El torneig europeu de bàsquet del 1998 va acabar amb Andorra invicta.",
        "La selecció del Principat va obtenir el títol del 1998 sense cap derrota.",
        "Andorra va ser campiona invicta d’Europa de països petits en bàsquet el 1998.",
        "Cap rival no va derrotar la selecció andorrana en el campionat europeu del 1998.",
        "El títol de 1998 va ser per a Andorra, que va completar el torneig amb victòries i sense perdre.",
        "Andorra va acabar el Campionat d’Europa de Països Petits de bàsquet del 1998 amb balanç invicte.",
        "La campanya andorrana al campionat del 1998 es va tancar sense derrotes i amb el títol.",
        "El 1998, la selecció nacional de bàsquet va conquerir el campionat europeu sense cedir cap partit.",
        "la selecció andorrana va aixecar el títol europeu del 1998 mantenint-se invicta.",
    ],
    "basquet-campio-casa-2000": [
        "Andorra va guanyar a casa el Campionat d’Europa de Països Petits de bàsquet del 2000.",
        "El títol de bàsquet del 2000 es va quedar a Andorra, que n’era l’amfitriona.",
        "La selecció andorrana va conquerir a casa el campionat europeu de països petits l’any 2000.",
        "Andorra va organitzar i guanyar l’edició del 2000 del Campionat d’Europa de Països Petits.",
        "El torneig de bàsquet disputat a Andorra el 2000 va acabar amb la selecció local campiona.",
        "La selecció de bàsquet d’Andorra va sortir campiona del torneig que es va jugar al país el 2000.",
        "La selecció del país va ser campiona del torneig celebrat a Andorra durant l’any 2000.",
        "L’edició del 2000 va coronar Andorra en la competició europea de bàsquet disputada al país.",
        "El campionat europeu de països petits va tenir lloc a Andorra el 2000 i el va guanyar l’equip andorrà.",
        "La victòria final del torneig local de 2000 va donar a Andorra el títol de bàsquet.",
        "el títol europeu de bàsquet del 2000 va ser guanyat per Andorra jugant a casa.",
    ],
    "basquet-campio-casa-2004": [
        "Andorra va guanyar a casa el Campionat d’Europa de Països Petits de bàsquet del 2004.",
        "El títol del torneig europeu de 2004 va quedar a mans de l’equip andorrà, amfitrió de l’edició.",
        "La selecció andorrana va aixecar a casa el campionat de països petits l’any 2004.",
        "La selecció del Principat va retenir el títol continental en l’edició de 2004 que s’organitzava a casa.",
        "El torneig celebrat a Andorra el 2004 va acabar amb la victòria de la selecció local.",
        "A casa, els andorrans es van endur la corona europea de països petits de bàsquet el 2004.",
        "L’equip del país va obtenir el títol en l’edició del 2004 organitzada a Andorra.",
        "Andorra va quedar campiona del torneig europeu que es va disputar al Principat durant el 2004.",
        "El Campionat d’Europa de Països Petits es va jugar al país el 2004 i el va guanyar l’amfitrió.",
        "La victòria andorrana de l’edició local del 2004 va culminar amb el títol continental.",
        "el campionat de bàsquet europeu del 2004 el va guanyar l’equip andorrà a casa.",
    ],
    "basquet-final-2012": [
        "Andorra va guanyar la final del Campionat d’Europa de Països Petits de bàsquet del 2012 per 74-72.",
        "El marcador final de 2012 va ser 74-72 a favor de la selecció andorrana.",
        "La final europea de bàsquet del 2012 va acabar amb triomf d’Andorra per dos punts, 74-72.",
        "Andorra es va imposar en el partit decisiu del campionat de 2012 per 74-72.",
        "La final del 2012 va acabar amb el títol per a Andorra i un marcador de 74-72.",
        "El 2012, la selecció andorrana va tancar la final amb 74 punts davant dels 72 del rival.",
        "El resultat que va donar la victòria a Andorra a la final europea de 2012 fou 74 a 72.",
        "La final del torneig de 2012 va quedar resolta per 74-72 amb Andorra com a guanyadora.",
        "Andorra es va endur el partit pel títol de 2012 amb un marcador de setanta-quatre a setanta-dos.",
        "El marcador de la final guanyada pel Principat el 2012 va ser 74–72.",
        "la selecció andorrana va obtenir el títol del 2012 en superar el rival per 74-72 a la final.",
    ],
    "basquet-final-2014": [
        "Andorra va guanyar Malta per 66-63 a la final del Campionat d’Europa de Països Petits de bàsquet del 2014.",
        "La final del 2014 es va resoldre amb una victòria andorrana sobre Malta: 66-63.",
        "El títol europeu de països petits de 2014 va ser per a Andorra, que va vèncer Malta per tres punts.",
        "Malta va perdre 66-63 davant la selecció andorrana en el partit final del torneig de 2014.",
        "La selecció del Principat va superar Malta a la final de bàsquet del 2014 amb marcador de 66-63.",
        "Andorra va superar Malta a la final de 2014 per 66 punts a 63.",
        "La final del campionat va acabar amb l’equip andorrà campió després de derrotar Malta 66-63.",
        "Un 66-63 contra Malta va donar a Andorra el títol europeu de bàsquet el 2014.",
        "Andorra va aixecar la copa del 2014 en vèncer Malta per 66-63 al partit decisiu.",
        "El resultat de la final Malta-Andorra del 2014 fou 63-66 favorable al Principat.",
        "la victòria andorrana per 66-63 davant Malta va decidir la final europea de 2014.",
    ],
    "bandera": [
        "La bandera d’Andorra té tres franges verticals: blava al costat del pal, groga al mig i vermella a l’altre costat.",
        "Blau, groc i vermell són els tres colors verticals de la bandera andorrana, en aquest ordre des del pal.",
        "La franja blava toca el pal; al centre hi ha la groga i a l’extrem oposat, la vermella.",
        "Tres bandes dretes formen la bandera d’Andorra, amb el blau primer, el groc al centre i el vermell a l’altra banda.",
        "Del costat del pal cap enfora, la bandera presenta blau, groc i vermell en franges verticals.",
        "La disposició vertical de la bandera andorrana posa la franja groga entre la blava i la vermella.",
        "La bandera té tres bandes verticals i la del pal és blava; groga és la central i vermella, l’oposada.",
        "A Andorra, el pavelló tricolor ordena les franges blava, groga i vermella de banda a banda.",
        "La franja vermella queda a l’extrem oposat al pal i la groga al mig, amb la blava tocant-hi.",
        "El blau va al pal, el groc ocupa el centre i el vermell tanca l’altre costat de la bandera.",
        "la bandera presenta verticalment blau al pal, groc al centre i vermell a l’extrem oposat.",
    ],
    "escut": [
        "A l’escut d’Andorra, la mitra i el bàcul daurats representen el bisbe d’Urgell.",
        "El bisbe d’Urgell hi és simbolitzat per la mitra i el bàcul d’or de l’escut andorrà.",
        "Daurats, la mitra i el bàcul de l’escut corresponen al bisbe d’Urgell.",
        "La representació episcopal de l’escut d’Andorra és la mitra juntament amb el bàcul, tots dos daurats.",
        "Mitra i bàcul, amb el color de l’or, són els símbols del bisbe d’Urgell a l’escut del país.",
        "La mitra i el bàcul daurats de l’escut fan referència al bisbe d’Urgell.",
        "L’escut andorrà identifica el bisbe d’Urgell mitjançant els atributs daurats de la mitra i el bàcul.",
        "El bàcul i la mitra daurats assenyalen la figura del bisbe d’Urgell a l’escut.",
        "A la composició heràldica, el bisbe d’Urgell es representa amb una mitra i un bàcul daurats.",
        "La mitra d’or i el bàcul d’or són les peces de l’escut que representen el bisbe d’Urgell.",
        "la figura del bisbe d’Urgell es reconeix a l’escut per la mitra i el bàcul daurats.",
    ],
    "himne": [
        "L’himne nacional d’Andorra es diu «El gran Carlemany».",
        "«El gran Carlemany» és el títol de l’himne nacional andorrà.",
        "El nom oficial de l’himne nacional del país és «El gran Carlemany».",
        "Andorra té per himne nacional la peça titulada «El gran Carlemany».",
        "El cant nacional andorrà porta el nom «El gran Carlemany».",
        "El títol que figura per al cant patriòtic d’Andorra és «El gran Carlemany».",
        "«El gran Carlemany» identifica l’himne nacional d’Andorra.",
        "La peça que fa d’himne nacional a Andorra s’anomena «El gran Carlemany».",
        "El gran Carlemany és el nom amb què es coneix l’himne d’Andorra.",
        "L’himne del Principat té com a títol «El gran Carlemany».",
        "la composició nacional andorrana s’anomena «El gran Carlemany».",
    ],
    "lema": [
        "El lema d’Andorra és «Virtus, unita, fortior».",
        "«Virtus, unita, fortior» és la divisa del Principat.",
        "La frase que identifica el lema andorrà és «Virtus, unita, fortior».",
        "Andorra fa servir com a lema les paraules «Virtus, unita, fortior».",
        "La divisa nacional porta aquesta formulació llatina: «Virtus, unita, fortior».",
        "El Principat té per lema la màxima «Virtus, unita, fortior».",
        "El mot d’ordre d’Andorra s’expressa com «Virtus, unita, fortior».",
        "La fórmula «Virtus, unita, fortior» correspon al lema del país.",
        "La inscripció adoptada com a lema d’Andorra diu «Virtus, unita, fortior».",
        "La frase llatina adoptada com a divisa del país consta de les paraules «Virtus, unita, fortior».",
        "la divisa andorrana es formula «Virtus, unita, fortior».",
    ],
    "casa-de-la-vall": [
        "L’escut d’Andorra està esculpit en marbre blanc al portal de Casa de la Vall.",
        "Al portal de Casa de la Vall hi ha un escut andorrà tallat en marbre blanc.",
        "El marbre blanc del portal de Casa de la Vall mostra esculpit l’escut d’Andorra.",
        "L’escut del país es va gravar en marbre blanc a l’entrada de Casa de la Vall.",
        "Casa de la Vall conserva al portal la talla de l’escut andorrà feta en marbre blanc.",
        "A la portada de Casa de la Vall, l’escut d’Andorra apareix treballat sobre marbre blanc.",
        "El portal de Casa de la Vall incorpora una talla blanca de l’escut nacional.",
        "Marbre blanc i escut d’Andorra es troben units en la peça esculpida del portal de Casa de la Vall.",
        "L’emblema andorrà del portal de Casa de la Vall és una escultura de marbre blanc.",
        "La talla heràldica del portal, feta en marbre blanc, és l’escut d’Andorra.",
        "la talla de Casa de la Vall, feta en marbre blanc, reprodueix l’escut nacional.",
    ],
    "romanic": [
        "La nau de l’església de Santa Coloma és preromànica.",
        "Preromànica és la nau de Santa Coloma.",
        "L’església de Santa Coloma té una nau d’estil preromànic.",
        "La part longitudinal principal de Santa Coloma pertany al preromànic.",
        "A Santa Coloma, la nau de l’església correspon a l’etapa preromànica.",
        "L’arquitectura preromànica és la de la nau de Santa Coloma.",
        "La nau de Santa Coloma s’inscriu en el període anterior al romànic.",
        "Santa Coloma conserva una nau d’època anterior al romànic.",
        "Santa Coloma conserva una nau que es classifica com a preromànica.",
        "La classificació arquitectònica de la nau de Santa Coloma és preromànica.",
        "l’església de Santa Coloma conserva com a nau principal una construcció preromànica.",
    ],
    "falles": [
        "Una falla andorrana és una torxa que es fa girar per damunt del cap la nit de Sant Joan.",
        "La nit de Sant Joan, la falla és una torxa girada sobre el cap.",
        "A Andorra, el nom falla designa la torxa que es volteja damunt del cap per Sant Joan.",
        "Una torxa que es fa rodar sobre el cap durant la vetlla de Sant Joan rep el nom de falla.",
        "El costum de les falles consisteix a fer giravoltar una torxa per sobre del cap la nit de Sant Joan.",
        "Per la revetlla de Sant Joan es gira la falla, una torxa que passa per damunt del cap.",
        "La falla és l’estri encès que es balanceja damunt el cap quan arriba la nit de Sant Joan.",
        "En la tradició andorrana, la torxa de Sant Joan es fa rodar sobre el cap i s’anomena falla.",
        "Una torxa en moviment sobre el cap és la falla que es fa la nit de Sant Joan.",
        "La nit de Sant Joan es fan girar les falles, torxes que passen per damunt del cap.",
        "la falla de Sant Joan és una torxa girada per damunt del cap durant la nit.",
    ],
    "gegants": [
        "Els gegants d’Andorra la Vella representen Carlemany i Ermessenda, vescomtessa de Castellbò.",
        "Carlemany i Ermessenda de Castellbò són les figures representades pels gegants de la capital.",
        "La comparsa de gegants de la capital està integrada per les figures de Carlemany i Ermessenda de Castellbò.",
        "Els gegants de la capital encarnen Carlemany i la vescomtessa Ermessenda de Castellbò.",
        "Les figures històriques representades són Carlemany i Ermessenda de Castellbò, la vescomtessa.",
        "La parella de gegants representa el sobirà Carlemany i Ermessenda, que fou vescomtessa de Castellbò.",
        "Ermessenda de Castellbò i Carlemany són els dos personatges que encarnen els gegants d’Andorra la Vella.",
        "La parella monumental andorrana pren els noms de Carlemany i Ermessenda, vescomtessa de Castellbò.",
        "La capital treu dos personatges gegants que representen Carlemany i Ermessenda de Castellbò.",
        "La parella monumental de la capital està formada per la imatge de Carlemany i la d’Ermessenda de Castellbò.",
        "la parella d’escultures gegants correspon a Carlemany i Ermessenda de Castellbò, vescomtessa.",
    ],
    "judici-contrabandistes-encamp": [
        "El Judici dels Contrabandistes és una farsa del Carnaval d’Encamp.",
        "Al Carnaval encampadà es representa la farsa anomenada Judici dels Contrabandistes.",
        "Una de les farses pròpies del Carnaval d’Encamp porta per nom Judici dels Contrabandistes.",
        "El Carnaval d’Encamp inclou la representació burlesca del Judici dels Contrabandistes.",
        "La farsa encampadana coneguda com a Judici dels Contrabandistes forma part del Carnaval.",
        "Dins les celebracions carnavalesques d’Encamp hi ha el Judici dels Contrabandistes, en forma de farsa.",
        "A Encamp, la celebració de Carnaval incorpora la representació del Judici dels Contrabandistes com a farsa.",
        "A Encamp, el Carnaval té una farsa que escenifica el Judici dels Contrabandistes.",
        "La peça còmica del Judici dels Contrabandistes s’inscriu en el Carnaval encampadà.",
        "El Carnaval de la parròquia d’Encamp compta amb la farsa titulada Judici dels Contrabandistes.",
        "la representació carnavalesca anomenada Judici dels Contrabandistes és una farsa d’Encamp.",
    ],
    "legendes": [
        "El Roc de les Bruixes és una roca gravada al bosc de Canillo.",
        "Al bosc de Canillo hi ha una roca amb gravats coneguda com el Roc de les Bruixes.",
        "El nom Roc de les Bruixes correspon a la roca gravada que es troba al bosc canillenc.",
        "Una pedra gravada del bosc de Canillo rep la denominació de Roc de les Bruixes.",
        "El Roc de les Bruixes és l’aflorament rocós amb gravats situat a Canillo.",
        "Canillo conserva al bosc una roca gravada anomenada Roc de les Bruixes.",
        "La roca amb inscripcions del bosc de Canillo és coneguda com el Roc de les Bruixes.",
        "Entre els elements del bosc de Canillo hi ha el Roc de les Bruixes, una pedra gravada.",
        "El monument rocós gravat de Canillo s’anomena Roc de les Bruixes.",
        "La denominació Roc de les Bruixes identifica una roca gravada en un bosc de Canillo.",
        "la roca del bosc canillenc que duu gravats és el Roc de les Bruixes.",
    ],
    "noms-parroquies": [
        "Les set parròquies andorranes són Canillo; Encamp; Ordino; la Massana; Andorra la Vella; Sant Julià de Lòria; Escaldes-Engordany.",
        "El mapa parroquial n’inclou set: les parròquies són Canillo; Ordino; Encamp; Sant Julià de Lòria; la Massana; Escaldes-Engordany; Andorra la Vella.",
        "Escaldes-Engordany tanca el recompte de set parròquies. També en formen part Canillo; Encamp; Ordino; la Massana; Andorra la Vella; Sant Julià de Lòria.",
        "La Massana i Ordino són dues parròquies. Les cinc restants són Canillo; Encamp; Andorra la Vella; Sant Julià de Lòria; Escaldes-Engordany.",
        "Andorra la Vella n’és una de set. Les altres són Canillo; Encamp; Ordino; la Massana; Sant Julià de Lòria; Escaldes-Engordany.",
        "El recompte de set parròquies inclou Canillo; Encamp; Ordino; la Massana; Sant Julià de Lòria; Andorra la Vella; Escaldes-Engordany.",
        "El territori andorrà s’ordena en set parròquies, entre elles Encamp; Canillo; la Massana; Ordino; Sant Julià de Lòria; Escaldes-Engordany; Andorra la Vella.",
        "Sant Julià de Lòria és una de les set parròquies. També hi ha Escaldes-Engordany; Andorra la Vella; la Massana; Ordino; Encamp; Canillo.",
        "El Principat es divideix en set parròquies que són Escaldes-Engordany; Sant Julià de Lòria; Andorra la Vella; la Massana; Ordino; Encamp; Canillo.",
        "La llista parroquial, en ordre alternatiu, és Canillo; Ordino; Encamp; Andorra la Vella; la Massana; Escaldes-Engordany; Sant Julià de Lòria.",
        "el conjunt territorial d’Andorra es divideix en set parròquies, de Canillo fins a Escaldes-Engordany.",
    ],
    "escaldes-parroquia": [
        "Escaldes-Engordany va esdevenir parròquia el 1978.",
        "L’any 1978 va marcar l’ascens d’Escaldes-Engordany a parròquia.",
        "El 1978 va donar a Escaldes-Engordany la condició de parròquia.",
        "La parròquia d’Escaldes-Engordany existeix des de 1978.",
        "La conversió d’Escaldes-Engordany en parròquia data de 1978.",
        "El 1978 es va obrir una nova parròquia amb el nom d’Escaldes-Engordany.",
        "La parròquia d’Escaldes-Engordany es va crear l’any 1978.",
        "Va ser l’any 1978 que Escaldes-Engordany va passar a ser parròquia.",
        "Escaldes-Engordany figura com a parròquia des del 1978.",
        "La data en què Escaldes-Engordany va adquirir la condició parroquial és 1978.",
        "la categoria de parròquia per a Escaldes-Engordany va començar el 1978.",
    ],
    "quarts-definicio": [
        "Els quarts són organitzacions veïnals amb drets col·lectius sobre béns comunals, anteriors als comuns.",
        "Abans que existissin els comuns, els quarts ja eren organitzacions veïnals amb drets sobre els béns compartits.",
        "Els drets col·lectius sobre els béns comunals defineixen els quarts, unes entitats veïnals prèvies als comuns.",
        "Abans de l’aparició dels comuns, cada quart articulava els drets col·lectius del veïnat sobre béns comunals.",
        "Els quarts precedeixen els comuns i agrupen veïns amb drets col·lectius sobre béns de la comunitat.",
        "Una institució veïnal anterior als comuns és el quart, que reuneix drets col·lectius sobre béns comunals.",
        "Els comuns van venir després; abans hi havia quarts, organitzacions locals amb drets compartits sobre béns comunals.",
        "Els quarts són formes veïnals antigues que tenien drets col·lectius damunt dels béns comunals.",
        "La comunitat de veïns organitzada en quart és anterior al comú i té drets col·lectius sobre béns comuns.",
        "Els drets sobre els béns comunals es compartien col·lectivament en els quarts, organitzacions veïnals anteriors als comuns.",
        "les entitats de veïns que precediren els comuns s’anomenaven quarts i compartien drets sobre béns comunals.",
    ],
    "quarts-localitzacio": [
        "A Andorra hi ha quarts a Ordino, la Massana i Sant Julià de Lòria.",
        "Ordino, la Massana i Sant Julià de Lòria són les parròquies on es troben quarts.",
        "Tres parròquies conserven quarts, que són Ordino; la Massana; Sant Julià de Lòria.",
        "Sant Julià de Lòria és una de les parròquies amb quarts, com també Ordino i la Massana.",
        "La presència de quarts es registra a Ordino, a la Massana i a Sant Julià de Lòria.",
        "A les parròquies d’Ordino, la Massana i Sant Julià de Lòria hi ha quarts.",
        "Tres llocs conserven quarts: la Massana; Sant Julià de Lòria; Ordino.",
        "Ordino i la Massana en tenen, igual que Sant Julià de Lòria: són les tres parròquies amb quarts.",
        "Els quarts es troben a Sant Julià de Lòria i també a Ordino i la Massana.",
        "Els quarts andorrans es troben únicament a Ordino, la Massana i Sant Julià de Lòria.",
        "els nuclis anomenats quarts es troben a Ordino; la Massana; Sant Julià de Lòria.",
    ],
    "comuns-autogovern": [
        "Cada parròquia té un comú que la representa i l’administra.",
        "La representació i l’administració parroquials corresponen al comú de cada parròquia.",
        "Un comú s’encarrega de representar i administrar cadascuna de les parròquies.",
        "A cada parròquia, el comú n’assumeix la representació i la gestió.",
        "Les parròquies són representades i administrades cadascuna pel seu comú.",
        "El govern local de cada parròquia recau en el comú, que la representa i l’administra.",
        "Cada comú representa la parròquia pròpia i se n’ocupa de l’administració.",
        "La institució parroquial que representa i gestiona cada parròquia és el comú.",
        "No hi ha parròquia sense el seu comú representatiu i administrador.",
        "El comú és l’òrgan que porta la representació i l’administració de la seva parròquia.",
        "la representació de cada parròquia i la seva administració són funcions del comú corresponent.",
    ],
    "comuns-competencies": [
        "La Constitució exigeix que una llei qualificada delimiti les competències comunals en almenys dotze matèries.",
        "Com a mínim dotze àmbits de competència comunal han de quedar delimitats per llei qualificada segons la Constitució.",
        "La norma constitucional fixa un sòl de dotze matèries que la llei qualificada ha d’ordenar per als comuns.",
        "Una llei qualificada ha de precisar les competències dels comuns en dotze matèries com a mínim.",
        "La Constitució encomana a una llei qualificada la delimitació competencial comunal i marca dotze matèries de mínim.",
        "Els comuns han de tenir les seves competències delimitades en no menys de dotze matèries per una llei qualificada.",
        "Dotze és el nombre mínim de matèries comunals que la llei qualificada ha de delimitar per mandat constitucional.",
        "La delimitació de competències dels comuns recau en una llei qualificada que ha d’abastar almenys dotze matèries.",
        "En matèria comunal, la Constitució ordena que la llei qualificada cobreixi un mínim de dotze àmbits.",
        "Per als comuns, una llei qualificada ha d’enumerar els camps competencials; el llindar constitucional és dotze.",
        "la llei qualificada ha de concretar dotze competències comunals com a mínim, tal com exigeix la Constitució.",
    ],
    "comuns-finançament": [
        "Les transferències als comuns inclouen una partida igual per parròquia i una de variable segons població, extensió i altres indicadors.",
        "El finançament comunal combina una quantitat idèntica per parròquia amb una altra que varia segons població, extensió i indicadors.",
        "Una part fixa i una part variable formen les transferències als comuns; la segona considera població, extensió i altres factors.",
        "Cada parròquia rep una base igual i un complement calculat amb població, superfície i altres indicadors.",
        "Les transferències es reparteixen entre una assignació igual per a cada comú i una altra ajustada per població i extensió, entre altres criteris.",
        "La fórmula dels comuns té dos components: una partida igual i una de variable segons població, territori i altres indicadors.",
        "Als comuns els arriba una suma comuna igual per parròquia més una part diferenciada segons població, extensió i altres dades.",
        "Població i extensió influeixen en la porció variable; la resta inclou una base igual per a cada parròquia.",
        "El sistema de transferències comunals uneix igualtat de partida i càlcul variable amb indicadors de població i superfície.",
        "La distribució als comuns assegura una quantitat igual per parròquia i afegeix un tram calculat amb diversos indicadors.",
        "les transferències comunals tenen una base idèntica i una part que depèn de població, extensió i altres indicadors.",
    ],
    "comuns-control": [
        "El Tribunal Constitucional resol els conflictes de competències entre òrgans generals de l’Estat i els comuns.",
        "Quan Estat i comuns discrepen sobre competències, decideix el Tribunal Constitucional.",
        "El tribunal encarregat de resoldre els conflictes competencials entre els comuns i els òrgans generals és el Constitucional.",
        "Les disputes de competències entre els comuns i els òrgans estatals generals són resoltes pel Tribunal Constitucional.",
        "El Tribunal Constitucional té la funció de resoldre els conflictes de competències que enfronten els comuns i l’Estat.",
        "La jurisdicció constitucional decideix els conflictes competencials dels comuns amb els òrgans generals estatals.",
        "L’òrgan que posa fi a les controvèrsies de competències entre comuns i Estat és el Tribunal Constitucional.",
        "Als conflictes competencials entre nivell general de l’Estat i comuns, hi intervé el Tribunal Constitucional.",
        "El Tribunal Constitucional arbitra les disputes sobre competències entre els comuns i els òrgans generals estatals.",
        "La resolució d’aquest tipus de conflicte entre Estat i comuns correspon al Tribunal Constitucional.",
        "el Tribunal Constitucional és qui resol les diferències de competència entre els comuns i l’Estat.",
    ],
    "comuns-eleccions": [
        "El mandat d’un consell de comú dura quatre anys.",
        "Quatre anys és la durada del mandat dels consells de comú.",
        "Cada consell de comú exerceix el càrrec durant un període de quatre anys.",
        "La renovació dels consells comunals es fa cada quatre anys.",
        "Un cicle de quatre anys correspon al mandat del consell de comú.",
        "Els membres del consell de comú tenen un mandat de quatre anys.",
        "El període entre eleccions comunals és de quatre anys per a un consell de comú.",
        "La durada fixada per al consell de comú és quadriennal.",
        "Al cap de quatre anys acaba el mandat d’un consell de comú.",
        "Els consells comunals es renoven amb mandats de quatre anys.",
        "el mandat comunal té una extensió de quatre anys.",
    ],
    "consell-general-escons": [
        "La Constitució permet que el Consell General tingui entre 28 i 42 consellers.",
        "El marge constitucional per als membres del Consell General va de 28 a 42 consellers.",
        "El nombre de consellers generals pot situar-se des de 28 fins a 42 segons la Constitució.",
        "Entre vint-i-vuit i quaranta-dos representants pot tenir el Consell General.",
        "La forquilla fixada per la Constitució per a la cambra és de 28–42 membres.",
        "El Consell General pot comptar amb un mínim de 28 i un màxim de 42 consellers.",
        "La Constitució deixa que la composició del Consell General variï entre vint-i-vuit i quaranta-dos escons.",
        "La cambra andorrana pot tenir 28, 30 i així fins a 42 consellers, d’acord amb la Constitució.",
        "El límit inferior és 28 i el superior 42 per als consellers generals previstos constitucionalment.",
        "La composició del Consell General queda constitucionalment situada dins l’interval 28–42 consellers.",
        "la Constitució autoritza una composició del Consell General entre 28 i 42 membres.",
    ],
}


def read_rows() -> list[dict[str, object]]:
    return [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines()]


def write_rows(rows: list[dict[str, object]]) -> None:
    DATASET.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )


CONTEXT_FRAMES = [
    "Per completar una fitxa, ", "En una nota de consulta, ", "Quan omplo una cronologia, ",
    "De cara a una consulta, ", "En un formulari de dades, ", "Per respondre una pregunta pràctica, ",
    "En preparar una fitxa cultural, ", "A la casella de la història, ", "En una conversa informativa, ",
    "Per cercar una dada, ", "En una consulta sobre el tema, ", "Quan cal anotar la resposta, ",
    "Per a una resposta de referència, ", "En una recerca breu, ", "Per al meu apunt, ",
    "En una fitxa de repàs, ", "Si la pregunta és concreta, ", "Per resoldre aquesta consulta, ",
    "En una anotació de context, ", "Per respondre al taulell, ", "En una explicació breu, ",
    "Quan preparo una resposta, ", "Per situar la dada en una fitxa, ", "En el camp corresponent, ",
    "A l’hora d’emplenar l’apunt, ", "Per fer una consulta ràpida, ", "En respondre al públic, ",
    "En un qüestionari d’informació, ", "Per a un registre de dades, ", "Quan redacto una nota, ",
    "En una consulta de referència, ", "Per a una fitxa temàtica, ", "En una pregunta de cultura, ",
    "Com a consulta concreta, ",
]

FALSE_QUESTION_STEMS = [
    "Per quin motiu s’afirma que ", "Com s’explica el fet que ", "A què es deu el fet que ",
    "Quin motiu hi ha per afirmar que ", "D’on surt l’afirmació que ",
    "Com es pot justificar la idea que ", "Quin fonament té la idea que ",
    "Com es pot sostenir que ", "Què serveix per explicar que ",
    "Quin raonament porta a dir que ", "Quina base hi ha per dir que ",
    "Com s’arriba a sostenir que ", "D’on prové la versió que ",
    "Per quin raonament es dona per fet que ", "Quina explicació es dona per afirmar que ",
    "Quina raó s’ha adduït per dir que ", "Com es pot entendre l’afirmació que ",
]


QUESTION_LABELS = {'grandvalira-marca-2003': 'Marca Grandvalira', 'tabac-revolta-1733': 'Revolta del tabac', 'tabac-prohibicio-conreu': 'Acord contra el conreu', 'tabac-monopoli-espanya': 'Monopoli tabaquer', 'grandvalira-telesqui-1956': 'Primer telesquí', 'vallnord-estacions-agrupades': 'Agrupació Vallnord', 'banca-secret-2018': 'Secret bancari', 'fhasa-reserva-10-per-cent': 'Reserva elèctrica de FHASA', 'fhasa-concessio': 'Concessió de FHASA', 'escola-andorrana-1982': 'Escola Andorrana', 'carlemany-carta-pobla': 'Carta Pobla', 'pareatge-1278': 'Primer Pareatge', 'pareatge-1288': 'Segon Pareatge', 'manual-digest-1748': 'Manual Digest', 'politar-1763': 'Politar andorrà', 'nova-reforma-1866': 'Nova Reforma', 'constitucio-1993': 'Constitució', 'referendum-1993': 'Referèndum constitucional', 'onu-1993': 'Admissió a l’ONU', 'consell-europa-1994': 'Consell d’Europa', 'oscar-ribas-primer-cap': 'Primer cap de Govern', 'marc-forne-cap': 'Mandat de Marc Forné', 'albert-pintat-cap': 'Mandat d’Albert Pintat', 'antoni-marti-cap': 'Mandat d’Antoni Martí', 'federacio-futbol': 'Federació de Futbol', 'basquet-1998-imbatut': 'Títol de bàsquet de 1998', 'basquet-campio-casa-2000': 'Campionat de 2000', 'basquet-campio-casa-2004': 'Campionat de 2004', 'basquet-final-2012': 'Final de bàsquet de 2012', 'basquet-final-2014': 'Final de bàsquet de 2014', 'bandera': 'Bandera andorrana', 'escut': 'Escut andorrà', 'himne': 'Himne nacional', 'lema': 'Lema del país', 'casa-de-la-vall': 'Portal de Casa de la Vall', 'romanic': 'Nau de Santa Coloma', 'falles': 'Falla de Sant Joan', 'gegants': 'Gegants d’Andorra la Vella', 'judici-contrabandistes-encamp': 'Judici dels Contrabandistes', 'legendes': 'Roc de les Bruixes', 'noms-parroquies': 'Set parròquies', 'escaldes-parroquia': 'Parròquia d’Escaldes-Engordany', 'quarts-definicio': 'Organització dels quarts', 'quarts-localitzacio': 'Localització dels quarts', 'comuns-autogovern': 'Comuns parroquials', 'comuns-competencies': 'Competències comunals', 'comuns-finançament': 'Transferències als comuns', 'comuns-control': 'Conflictes entre comuns i Estat', 'comuns-eleccions': 'Mandat del consell de comú', 'consell-general-escons': 'Composició del Consell General'}

QUESTION_PREFIXES = (
    *FALSE_QUESTION_STEMS,
    "En una consulta pràctica: ", "En una consulta pràctica, ",
    "Em recordes ", "Em pots precisar ", "Respon breument aquesta pregunta: ",
    "Dit d’una altra manera, ", "Dit d’una altra manera: ", *CONTEXT_FRAMES,
)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"[^\w]+", " ", text, flags=re.UNICODE).strip()


def lower_clause_initial(text: str) -> str:
    if text.startswith(("El ", "La ", "Els ", "Les ", "Un ", "Una ", "Uns ", "Unes ", "L’", "L'", "Hi ", "És ", "Va ", "Quan ", "Què ", "Quin ", "Per ")):
        return text[0].lower() + text[1:]
    return text


def clean_question(text: str) -> str:
    changed = True
    while changed:
        changed = False
        for prefix in QUESTION_PREFIXES:
            if text.casefold().startswith(prefix.casefold()):
                text = text[len(prefix):].lstrip()
                changed = True
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def diversify_questions(rows: list[dict[str, object]]) -> None:
    context_index = 0
    false_index = 0
    questions_seen: dict[str, set[str]] = {}
    duplicate_questions: dict[str, int] = {}
    fact_text_to_id = {normalize(form): fact_id for fact_id, forms in ANSWER_FORMS.items() for form in forms}
    facts_path = ROOT / "training-data/facts/canon-facts.jsonl"
    for line in facts_path.read_text(encoding="utf-8").splitlines():
        fact = json.loads(line)
        fact_text_to_id[normalize(fact["fact"])] = fact["fact_id"]
    # Canonical secondary answers identify the related fact before they are paraphrased.
    for row in rows:
        messages = row["messages"]
        for position in (1, 3) if row["type"] == "dues-voltes" else (1,):
            if position >= len(messages):
                continue
            question = clean_question(messages[position]["content"])
            if position == 1 and row["type"] == "premissa-falsa":
                claim = re.sub(r"^Per què\s+", "", question, flags=re.IGNORECASE).rstrip("? .")
                stem = FALSE_QUESTION_STEMS[false_index % len(FALSE_QUESTION_STEMS)]
                false_index += 1
                claim = lower_clause_initial(claim)
                question = stem + claim + "?"
            if position == 1 and row["type"] == "context":
                frame = CONTEXT_FRAMES[context_index % len(CONTEXT_FRAMES)]
                context_index += 1
                question = frame + question[0].lower() + question[1:]
            if position == 1 and row.get("fact_id"):
                fact_id = row["fact_id"]
                normalized_question = normalize(question)
                seen = questions_seen.setdefault(fact_id, set())
                if normalized_question in seen:
                    occurrence = duplicate_questions.get(fact_id, 0) + 1
                    duplicate_questions[fact_id] = occurrence
                    label = QUESTION_LABELS[fact_id]
                    qualifier = " · altra formulació" if occurrence % 2 else " · nova consulta"
                    question = f"{label}{qualifier} — {question}"
                    normalized_question = normalize(question)
                seen.add(normalized_question)
            messages[position]["content"] = question
        if row["type"] == "dues-voltes":
            secondary = messages[4]["content"]
            related_id = fact_text_to_id.get(normalize(secondary))
            if related_id:
                messages[4]["content"] = ANSWER_FORMS[related_id][1]


def main() -> None:
    rows = read_rows()
    positions: dict[str, int] = {}
    for row in rows:
        fact_id = row.get("fact_id")
        if fact_id not in ANSWER_FORMS:
            continue
        position = positions.get(fact_id, 0)
        response = ANSWER_FORMS[fact_id][position]
        positions[fact_id] = position + 1
        messages = row["messages"]
        if row["type"] == "premissa-falsa":
            response = "No és així: " + response[0].lower() + response[1:]
        messages[2]["content"] = response
    for fact_id, forms in ANSWER_FORMS.items():
        if positions.get(fact_id) != 11 or len(forms) != 11:
            raise ValueError(f"{fact_id}: expected exactly 11 authored responses")
    diversify_questions(rows)
    write_rows(rows)


if __name__ == "__main__":
    main()
