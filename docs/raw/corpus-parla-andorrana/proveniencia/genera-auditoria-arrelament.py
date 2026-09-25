"""Construeix una auditoria conservadora de l'arrelament andorrà dels candidats."""
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROS = ROOT / "proveniencia/prospeccio"
NOMS = {
    "isidre-bartumeu":"Isidre Bartumeu Martínez", "lurdes-riba":"Lurdes Riba", "josep-dalleres":"Josep Dallarès", "marc-forne":"Marc Forné", "pere-vilanova":"Pere Vilanova", "joan-burgues":"Joan Burgués Martisella", "isidre-baro":"Isidre Baró", "josep-areny":"Josep Areny", "simo-duro":"Simó Duró", "ricard-fiter":"Ricard Fiter", "lisa-cruz":"Lisa Cruz", "monica-bonell":"Mònica Bonell", "bonaventura-riberaygua":"Bonaventura Riberaygua", "josep-marsal":"Josep Marsal", "josep-maria-cases":"Josep Maria Cases", "denisa-font":"Denisa Font", "albert-gelabert":"Albert Gelabert", "rosa-maria-mandico":"Rosa Maria Mandicó", "jordi-guillamet":"Jordi Guillamet", "pere-besoli":"Pere Besolí", "angelina-mas":"Angelina Mas", "casimir-arajol":"Casimir Arajol", "ramon-rossell":"Mossèn Ramon Rossell", "anna-riberaygua":"Anna Riberaygua", "david-montane":"David Montané", "antoni-marti":"Antoni Martí Petit", "cerni-escale":"Cerni Escalé", "xavier-espot":"Xavier Espot", "oscar-ribas":"Òscar Ribas i Reig", "conxita-marsol":"Conxita Marsol Riart", "marta-roure":"Marta Roure", "guillem-forne":"Guillem Forné", "guillem-areny":"Guillem Areny", "andreu-gonzalez":"Andreu González", "oriol-agorreta":"Oriol Agorreta", "laura-casanovas":"Laura Casanovas", "arnau-rius":"Arnau Rius", "alberto-villagrasa":"Alberto Villagrasa", "katia-ustina":"Katia Ustina", "ander-mirambell":"Ander Mirambell", "joan-piquet":"Joan Piquet", "pau-chica":"Pau Chica", "albert-vilaro":"Albert Vilaró", "valenti-closa":"Valentí Closa", "sonia-andorrita":"Sonia (Andorrita)", "francesc-solana":"Francesc Solana", "enric-flix":"Enric Flix", "arnau-fortuny":"Arnau Fortuny", "gabriel-lezkano":"Gabriel Lezkano", "nuria-pablos":"Núria Pablos", "carles-ensenyat":"Carles Ensenyat", "xavier-espot-actual":"Xavier Espot", "antoni-morell":"Antoni Morell"
}
EXTERN = {
    "lead-yt-035-cerni-escale": ("institucional_andorrà", "Consell General: president del grup parlamentari de Concòrdia; nacionalitat individual a verificar separadament"),
    "lead-yt-038-conxita-marsol": ("arrelament_documentat_origen_extern", "Govern: nascuda a Artesa de Segre; trajectòria pública andorrana documentada"),
    "lead-yt-048-ander-mirambell": ("no_apte_com_a_andorrà_nadiu", "biografia pròpia: nascut a Barcelona; veu convidada en un programa produït a Andorra"),
    "lead-yt-047-katia-ustina": ("arrelament_no_verificat", "la font només identifica una secció de finances; no acredita nacionalitat ni residència"),
    "lead-yt-057-gabriel-lezkano": ("arrelament_no_verificat", "la font només identifica un músic; no acredita nacionalitat ni residència"),
    "lead-rtva-061-antoni-morell": ("referent_andorrà_origen_extern", "RTVA: nascut a Barcelona i descrit com un dels grans referents de la literatura andorrana"),
}
def main():
    out=[]
    for folder in sorted(PROS.glob("lead-*")):
        info=json.loads((folder/"source.info.json").read_text(encoding="utf-8")); slug=folder.name.split("-",3)[-1]
        nom=info.get("nom") or NOMS.get(slug) or slug.replace("-"," ").title(); url=info.get("source_url") or info.get("url") or ""
        if folder.name in EXTERN: categoria,evidencia=EXTERN[folder.name]
        elif folder.name == "lead-rtva-059-carles-ensenyat": categoria,evidencia=("institucional_andorrà", "font oficial RTVA/Consell: síndic general; nacionalitat individual a verificar separadament")
        elif folder.name == "lead-rtva-060-xavier-espot-actual": categoria,evidencia=("institucional_andorrà", "font oficial RTVA/Govern: cap de Govern; nacionalitat individual a verificar separadament")
        elif folder.name.startswith("lead-rtva-"): categoria,evidencia=("arrelament_documentat", "RTVA presenta una trajectòria institucional, cultural o comunitària al Principat; no és prova automàtica de lloc de naixement")
        else: categoria,evidencia=("arrelament_no_verificat", "vídeo produït o emès des d'Andorra; la font no basta per afirmar nacionalitat")
        out.append({"expedient":folder.name,"nom":nom,"categoria":categoria,"estat":"pendent_validacio_humana","evidencia":evidencia,"font":url})
    path=ROOT/"proveniencia/auditoria-arrelament-andorra.tsv"
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(out[0]),delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(out)
    from collections import Counter
    print(f"OK auditoria arrelament: {len(out)} expedients · {dict(Counter(r['categoria'] for r in out))} · {path}")
if __name__ == "__main__": main()
