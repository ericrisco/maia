"""Afegeix referències institucionals als set informes més incerts."""

from pathlib import Path

ROOT = Path(__file__).parents[1]
MARKER = "### Referència institucional del cas persistent"
URLS = {
    "pa-019": ("Pere Altimir Pintat", "l'índex antroponímic el situa com a conseller de Sant Julià", "https://www.consellgeneral.ad/actes-historiques/llibres-actes/estudi-sobre-les-actes-transcrites/index-de-carrecs-institucionals-1133-2023"),
    "pa-021": ("Josep Areny Fité", "una acta del Consell General el registra entre els consellers de Canillo", "https://www.consellgeneral.ad/ca/arxiu/diari-oficial-del-consell-general-1/any-1992/dcg-11-1992/at_download/pdf"),
    "pa-022": ("Miquel Armengol Pons", "la fitxa institucional confirma la identitat i el càrrec de conseller general", "https://www.consellgeneral.ad/ca/arxiu/arxiu-de-lleis-i-textos-aprovats-en-legislatures-anteriors/legislatura-constituent-1993/consellers-generals-del-1993/miquel-armengol-pons"),
    "pa-037": ("Miquel Naudi Casal", "l'índex antroponímic el situa com a de Soldeu de Canillo i conseller de 1992–1993", "https://www.consellgeneral.ad/actes-historiques/llibres-actes/estudi-sobre-les-actes-transcrites/index-de-carrecs-institucionals-1133-2023"),
    "pa-051": ("Josep Casal", "la fitxa de l'Arxiu d'Etnografia identifica la peça de ramaderia d'alçada", "https://www.arxiuenlinia.ad/fotoweb/archives/5005-Audiovisual/Audiovisual/AE/AE_0033.mp4.info"),
    "pa-056": ("Enric Dolsa Font", "la fitxa institucional confirma la trajectòria de conseller general 1990–1997", "https://www.consellgeneral.ad/ca/arxiu/arxiu-de-lleis-i-textos-aprovats-en-legislatures-anteriors/i-legislatura-1994-1997/consellers-generals-del-1994-1997/enric-dolsa-font"),
    "pa-057": ("Gabriel Dallerès Codina", "l'índex de càrrecs institucionals confirma el context de conseller andorrà", "https://www.consellgeneral.ad/actes-historiques/llibres-actes/estudi-sobre-les-actes-transcrites/index-de-carrecs-institucionals-1133-2023"),
}


def main() -> None:
    for pid, (name, claim, url) in URLS.items():
        report = ROOT / "persones" / f"{pid}.md"
        text = report.read_text(encoding="utf-8")
        if MARKER in text:
            text = text[: text.index(MARKER)].rstrip() + "\n"
        section = (
            f"\n{MARKER}\n\n"
            f"La font institucional identifica **{name}**: {claim} ([referència]({url})). "
            "Aquesta dada reforça la identificació territorial o institucional del clip; "
            "no prova la llengua inicial ni la socialització lingüística.\n"
        )
        report.write_text(text.rstrip() + "\n" + section, encoding="utf-8")
    print(f"{len(URLS)} informes actualitzats")


if __name__ == "__main__":
    main()
