"""Genera una matriu machine-readable de l'estat de l'objectiu."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-objectiu.tsv"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    people = read(ROOT / "persones.tsv")
    canonical = read(PROV / "persones-canonics.tsv")
    sources = read(PROV / "fonts-resum.tsv")
    reports = list((ROOT / "persones").glob("pa-*.md"))
    report_audit = read(PROV / "auditoria-informes.tsv")
    audios = list((ROOT / "audios").glob("*/audio.wav"))
    transcripts = [path for path in (ROOT / "transcripcions").glob("*.txt") if not path.name.endswith("-marcada.txt")]
    master = read(PROV / "registre-audicio.tsv")
    scarce_master = read(PROV / "registre-audicio-formes-escasses.tsv") if (PROV / "registre-audicio-formes-escasses.tsv").exists() else []
    identity = read(PROV / "auditoria-identitat-linguistica.tsv")
    coverage_sessions = read(PROV / "auditoria-cobertura-sessions.tsv")
    transcript_audit = read(PROV / "auditoria-integritat-transcripcions.tsv")
    quarantine_queue = read(PROV / "cua-audicio-quarantena-20s.tsv") if (PROV / "cua-audicio-quarantena-20s.tsv").exists() else []
    candidate_audit = read(PROV / "auditoria-candidats.tsv") if (PROV / "auditoria-candidats.tsv").exists() else []
    forms_graph = read(ROOT / "grafo" / "nodes-formes-completa.tsv")
    acoustic_graph = read(ROOT / "grafo" / "nodes-acustic-canonic.tsv")
    candidate_form_nodes = read(ROOT / "grafo" / "nodes-formes-candidats.tsv")
    candidate_form_edges = read(ROOT / "grafo" / "arestes-formes-candidats.tsv")
    candidate_acoustic_nodes = read(ROOT / "grafo" / "nodes-acustic-candidats.tsv")
    candidate_acoustic_edges = read(ROOT / "grafo" / "arestes-acustic-candidats.tsv")
    scarce_graph_nodes = read(ROOT / "grafo" / "nodes-formes-escasses.tsv")
    scarce_graph_edges = read(ROOT / "grafo" / "arestes-parlants-formes-escasses.tsv")
    candidate_transcript_audit = read(PROV / "auditoria-integritat-transcripcions-candidats.tsv")
    candidate_priority_queue = read(PROV / "cua-audicio-candidats-prioritaria.tsv")
    scarce_priority_queue = read(PROV / "cua-audicio-formes-escasses-prioritaria.tsv")
    coverage_audit = read(PROV / "auditoria-cobertura-persones.tsv")
    channels = sorted({row["canal"] for row in sources})
    contextual = sum(row["estat"].startswith("context territorial documentat") for row in identity)
    metadata_only = sum(row["estat"].startswith("font andorrana") for row in identity)
    complete_reports = sum(row["estat"] == "complet-provisional" for row in report_audit)
    covered_sessions = sum(row["estat"] == "cobert" for row in coverage_sessions)
    quarantine_sessions = sum(row["estat"] == "quarantena" for row in coverage_sessions)
    complete_transcripts = sum(row["estat"] == "complet" for row in transcript_audit)
    rows = [
        {"requisit": "subcorpus independent", "evidencia": "README.md linked_to_existing_corpus=false", "estat": "assolit", "buit": ""},
        {"requisit": "entre 50 i 100 persones", "evidencia": f"persones-canonics.tsv: {len({row['id_parlant'] for row in canonical})} persones", "estat": "assolit", "buit": ""},
        {"requisit": "fonts audiovisuals institucionals", "evidencia": f"fonts-resum.tsv: {len(sources)} registres · canals: {', '.join(channels)}", "estat": "assolit", "buit": ""},
        {"requisit": "àudio local amb procedència", "evidencia": f"audios/*/audio.wav: {len(audios)} fitxers", "estat": "assolit", "buit": ""},
        {"requisit": "transcripció per font", "evidencia": f"transcripcions/*.txt: {len(transcripts)} fitxers; auditoria estructural: {complete_transcripts}/{len(transcript_audit)} completes; JSON/VTT al paquet", "estat": "assolit com a ASR", "buit": "QA de timestamps i revisió diplomàtica pendent en les incidències detectades"},
        {"requisit": "informe per font", "evidencia": f"persones/*.md: {len(reports)} fitxes amb inventari i repertori", "estat": "assolit com a anàlisi provisional", "buit": "confirmació auditiva pendent"},
        {"requisit": "completitud estructural de les fitxes", "evidencia": f"auditoria-informes.tsv: {complete_reports}/{len(report_audit)} fitxes provisionals completes", "estat": "assolit com a completitud documental", "buit": "anotació auditiva pendent"},
        {"requisit": "context i identitat documental", "evidencia": f"auditoria-identitat-linguistica.tsv: {contextual} parlants amb font contextual · {metadata_only} identificacions per títol/metadades", "estat": "assolit com a procedència contextual", "buit": "biografia lingüística, lloc de socialització i veu atribuïda pendents d'audició"},
        {"requisit": "cobertura operativa per persona", "evidencia": f"auditoria-cobertura-sessions.tsv: {covered_sessions} parlants coberts per les sessions · {quarantine_sessions} en quarantena", "estat": "assolit com a cobertura de selecció", "buit": "les decisions de veu i forma continuen pendents d'audició"},
        {"requisit": "graf textual independent", "evidencia": f"nodes-formes-completa.tsv: {len(forms_graph)} nodes canònics", "estat": "assolit com a semblança ASR", "buit": "no és resultat dialectològic fins a escoltar"},
        {"requisit": "graf acústic independent", "evidencia": f"nodes-acustic-canonic.tsv: {len(acoustic_graph)} nodes", "estat": "assolit com a exploració instrumental", "buit": "no és classificació dialectal"},
        {"requisit": "graf separat de candidats", "evidencia": f"nodes-formes-candidats.tsv: {len(candidate_form_nodes)} nodes · arestes-formes-candidats.tsv: {len(candidate_form_edges)} arestes · 11 expedients", "estat": "assolit com a semblança textual exploratòria", "buit": "veu, variant, termes i relació amb el cànon pendents d'audició"},
        {"requisit": "graf acústic separat de candidats", "evidencia": f"nodes-acustic-candidats.tsv: {len(candidate_acoustic_nodes)} nodes · arestes-acustic-candidats.tsv: {len(candidate_acoustic_edges)} arestes · 11 expedients", "estat": "assolit com a exploració instrumental", "buit": "no és classificació dialectal i continua pendent d'audició"},
        {"requisit": "graf canònic de formes escasses", "evidencia": f"nodes-formes-escasses.tsv: {len(scarce_graph_nodes)} nodes · arestes-parlants-formes-escasses.tsv: {len(scarce_graph_edges)} arestes · 10 formes", "estat": "assolit com a semblança ASR", "buit": "confirmació auditiva pendent"},
        {"requisit": "quadern de formes representatives", "evidencia": "quadern-formes-representatives.md: 35 formes amb contextos VTT i enllaç a fitxes", "estat": "preparat per audició", "buit": "els contextos ASR no són confirmacions"},
        {"requisit": "evidència gramatical i de contacte llegible", "evidencia": "quadern-evidencia-gramatica.md: 10.458 contextos en 9 categories", "estat": "assolit com a inventari textual", "buit": "morfosintaxi i contacte pendents d'escolta"},
        {"requisit": "integritat de transcripcions candidates", "evidencia": f"auditoria-integritat-transcripcions-candidats.tsv: {sum(row.get('estat') == 'complet' for row in candidate_transcript_audit)}/{len(candidate_transcript_audit)} clips amb WAV i doble ASR", "estat": "assolit tècnicament", "buit": "veu i forma pendents d'audició"},
        {"requisit": "primera cua humana de candidats", "evidencia": f"cua-audicio-candidats-prioritaria.tsv: {len(candidate_priority_queue)} clips de {len({row['candidate'] for row in candidate_priority_queue})} veus", "estat": "preparada", "buit": "decisions humanes pendents"},
        {"requisit": "primera cua humana de formes escasses", "evidencia": f"cua-audicio-formes-escasses-prioritaria.tsv: {len(scarce_priority_queue)} clips i {len({row['forma'] for row in scarce_priority_queue})} formes", "estat": "preparada", "buit": "decisions humanes pendents"},
        {"requisit": "cobertura documental per font", "evidencia": f"auditoria-cobertura-persones.tsv: {len(coverage_audit)} fitxes amb informe, àudio, transcripció i procedència", "estat": "assolit documentalment", "buit": "validació lingüística pendent"},
        {"requisit": "format d'àudio verificat", "evidencia": "auditoria-format-audio.md: 66/66 fonts vàlides i 656/656 clips PCM mono 16 kHz", "estat": "assolit tècnicament", "buit": "el format no confirma identitat ni variant"},
        {"requisit": "revisió auditiva de cada clip", "evidencia": f"registre-audicio.tsv: {sum(row.get('estat_audicio','') in ('', 'pendent', 'pendent-audicio') for row in master)} pendents de {len(master)} · registre formes escasses: {sum(row.get('estat_audicio','') in ('', 'pendent', 'pendent-audicio') for row in scarce_master)} pendents de {len(scarce_master)} · candidats: {sum(int(row.get('n_clips', '0')) for row in candidate_audit)} pendents", "estat": "pendent", "buit": "decisió, nota, variant, fonètica i prosòdia humanes"},
        {"requisit": "veus en quarantena", "evidencia": f"pa-044, pa-047 i pa-050 · cua curta: {len(quarantine_queue)} clips", "estat": "pendent", "buit": "revisió auditiva i confirmació de segments atribuïbles"},
    ]
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} requisits")


if __name__ == "__main__":
    main()
