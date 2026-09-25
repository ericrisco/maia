"""Verifica la cobertura y coherencia mínima del corpus independent."""

from pathlib import Path
import csv
import hashlib
import sys

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def read(rel):
    with (ROOT / rel).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def fail(message):
    print(f"ERROR: {message}")
    return 1


def main() -> int:
    errors = []
    people = read("persones.tsv")
    ids = {row["id_persona"] for row in people}
    reports = list((ROOT / "persones").glob("pa-*.md"))
    canonical = read("proveniencia/persones-canonics.tsv") if (ROOT / "proveniencia/persones-canonics.tsv").exists() else []
    identity = read("proveniencia/auditoria-identitat-linguistica.tsv") if (PROV / "auditoria-identitat-linguistica.tsv").exists() else []
    provenance = list(PROV.glob("pa-*/README.md"))
    if len(people) != 66:
        errors.append(f"persones.tsv té {len(people)} files")
    if len(reports) != len(people):
        errors.append(f"informes {len(reports)} != persones {len(people)}")
    people_index = (ROOT / "persones/INDEX.md").read_text(encoding="utf-8") if (ROOT / "persones/INDEX.md").exists() else ""
    if "# Índex de persones del corpus de parla andorrana" not in people_index or people_index.count("| `pa-") != 66:
        errors.append("persones/INDEX.md no confirma les 66 fitxes individuals")
    if len(provenance) != len(people):
        errors.append(f"proveniencia {len(provenance)} != persones {len(people)}")
    if len(canonical) != 66 or len({row["id_parlant"] for row in canonical}) != 60:
        errors.append(f"mapa canònic inconsistent: registres={len(canonical)} persones={len({row["id_parlant"] for row in canonical}) if canonical else 0}")
    contextual = sum(row.get("estat", "").startswith("context territorial documentat") for row in identity)
    metadata_only = sum(row.get("estat", "").startswith("font andorrana") for row in identity)
    if len(identity) != 60 or contextual != 60 or metadata_only != 0:
        errors.append(f"auditoria d'identitat inconsistent: files={len(identity)} context={contextual} metadades={metadata_only}")
    for person in ids:
        for rel in [f"audios/{person}/audio.wav", f"transcripcions/{person}.txt", f"transcripcions/{person}.vtt", f"transcripcions/{person}.json"]:
            if not (ROOT / rel).exists():
                errors.append(f"falta {rel}")
    clips = read("proveniencia/clips-audicio.tsv")
    clip_keys = {(row["id_persona"], row["forma"]) for row in clips}
    queue = read("proveniencia/cua-audicio.tsv")
    queue_keys = {(row["id_persona"], row["forma"]) for row in queue}
    if len(queue) != 656 or len(clips) != 656 or clip_keys != queue_keys:
        errors.append(f"cua/clips incoherents: cua={len(queue)} clips={len(clips)}")
    bad_hashes = [row["clip"] for row in clips if not (PROV / row["clip"]).exists() or hashlib.sha256((PROV / row["clip"]).read_bytes()).hexdigest() != row["sha256"]]
    audio_audit = read("proveniencia/auditoria-integritat-audio.tsv")
    if (
        len(audio_audit) != 722
        or sum(row.get("tipus") == "font" and row.get("estat") == "ok" for row in audio_audit) != 66
        or sum(row.get("tipus") == "clip" and row.get("estat") == "ok" for row in audio_audit) != 656
    ):
        errors.append("auditoria-integritat-audio.tsv no confirma 66 fonts i 656 clips WAV vàlids")
    readme_audit = read("../auditoria-readme-titols.tsv") if (ROOT / "../auditoria-readme-titols.tsv").exists() else []
    if len(readme_audit) != 266 or any(row.get("estat") != "identificable" for row in readme_audit):
        errors.append("auditoria-readme-titols.tsv no confirma 266 títols README identificables")
    provenance_audit = read("proveniencia/auditoria-proveniencia.tsv")
    if len(provenance_audit) != 66 or any(row.get("estat") != "complet" for row in provenance_audit):
        errors.append("auditoria-proveniencia.tsv no confirma 66 procedències completes")
    transcript_audit = read("proveniencia/auditoria-integritat-transcripcions.tsv")
    transcript_pending = {row.get("id_persona") for row in transcript_audit if row.get("estat") != "complet"}
    if len(transcript_audit) != 66 or sum(row.get("estat") == "complet" for row in transcript_audit) != 64 or transcript_pending != {"pa-028", "pa-047"}:
        errors.append("auditoria-integritat-transcripcions.tsv no confirma 64 completes i pa-028/pa-047 en QA")
    remediation = read("proveniencia/auditoria-remediacio-transcripcions.tsv")
    if len(remediation) != 2 or {row.get("id_persona") for row in remediation} != {"pa-028", "pa-047"} or any(row.get("estat") != "derivat-qa-pendent-audicio" for row in remediation):
        errors.append("auditoria-remediacio-transcripcions.tsv no confirma els dos derivats QA")
    independence_audit = read("proveniencia/auditoria-independencia.tsv")
    if len(independence_audit) != 253 or any(row.get("estat") != "independent" for row in independence_audit):
        errors.append("auditoria-independencia.tsv detecta dependències fora del subcorpus")
    brain_isolation = read("proveniencia/auditoria-aillament-brain.tsv")
    brain_isolation_report = (PROV / "auditoria-aillament-brain.md").read_text(encoding="utf-8") if (PROV / "auditoria-aillament-brain.md").exists() else ""
    if brain_isolation or "Referències fora del subcorpus: **0**" not in brain_isolation_report:
        errors.append("auditoria-aillament-brain.tsv detecta referències semàntiques fora del subcorpus")
    prospect_lead = ROOT / "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu"
    prospect_report = (prospect_lead / "informe.md").read_text(encoding="utf-8") if (prospect_lead / "informe.md").exists() else ""
    prospect_forms = read("proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/formes.tsv") if (prospect_lead / "formes.tsv").exists() else []
    prospect_queue = read("proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/cua-audicio.tsv") if (prospect_lead / "cua-audicio.tsv").exists() else []
    prospect_acoustic = read("proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/analisi-acustica.tsv") if (prospect_lead / "analisi-acustica.tsv").exists() else []
    prospect_small = prospect_lead / "asr/isidre-bartumeu-nocontext.json"
    prospect_base = prospect_lead / "asr/isidre-bartumeu-base-nocontext.json"
    if (
        not (prospect_lead / "audio.wav").exists()
        or not prospect_small.exists()
        or not prospect_base.exists()
        or len(prospect_forms) != 35
        or len(prospect_queue) != 16
        or len(prospect_acoustic) != 16
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in prospect_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in prospect_queue)
        or "fora del recompte canònic" not in prospect_report
        or "repetició" not in prospect_report
    ):
        errors.append("l'expedient nou de prospecció RTVA no conserva àudio, doble ASR i cua separada")
    else:
        try:
            import json
            small_last = json.loads(prospect_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            base_last = json.loads(prospect_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if small_last < 2_800_000 or base_last < 2_800_000:
                errors.append("l'expedient nou de prospecció RTVA no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient nou de prospecció RTVA invàlid")
    prospect_lurdes = ROOT / "proveniencia/prospeccio/lead-rtva-010-lurdes-riba"
    lurdes_report = (prospect_lurdes / "informe.md").read_text(encoding="utf-8") if (prospect_lurdes / "informe.md").exists() else ""
    lurdes_forms = read("proveniencia/prospeccio/lead-rtva-010-lurdes-riba/formes.tsv") if (prospect_lurdes / "formes.tsv").exists() else []
    lurdes_queue = read("proveniencia/prospeccio/lead-rtva-010-lurdes-riba/cua-audicio.tsv") if (prospect_lurdes / "cua-audicio.tsv").exists() else []
    lurdes_acoustic = read("proveniencia/prospeccio/lead-rtva-010-lurdes-riba/analisi-acustica.tsv") if (prospect_lurdes / "analisi-acustica.tsv").exists() else []
    lurdes_small = prospect_lurdes / "asr/lurdes-riba-small-nocontext.json"
    lurdes_base = prospect_lurdes / "asr/lurdes-riba-base-nocontext.json"
    if (
        not (prospect_lurdes / "audio.wav").exists()
        or not lurdes_small.exists()
        or not lurdes_base.exists()
        or len(lurdes_forms) != 55
        or len(lurdes_queue) != 38
        or len(lurdes_acoustic) != 38
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in lurdes_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in lurdes_queue)
        or "fora del recompte" not in lurdes_report
        or "macarulla" not in lurdes_report
    ):
        errors.append("l'expedient Lurdes Riba no conserva àudio, doble ASR, formes locals i cua separada")
    else:
        try:
            import json
            lurdes_small_last = json.loads(lurdes_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            lurdes_base_last = json.loads(lurdes_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if lurdes_small_last < 3_400_000 or lurdes_base_last < 3_400_000:
                errors.append("l'expedient Lurdes Riba no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Lurdes Riba invàlid")
    prospect_dalleres = ROOT / "proveniencia/prospeccio/lead-rtva-011-josep-dalleres"
    dalleres_report = (prospect_dalleres / "informe.md").read_text(encoding="utf-8") if (prospect_dalleres / "informe.md").exists() else ""
    dalleres_forms = read("proveniencia/prospeccio/lead-rtva-011-josep-dalleres/formes.tsv") if (prospect_dalleres / "formes.tsv").exists() else []
    dalleres_queue = read("proveniencia/prospeccio/lead-rtva-011-josep-dalleres/cua-audicio.tsv") if (prospect_dalleres / "cua-audicio.tsv").exists() else []
    dalleres_acoustic = read("proveniencia/prospeccio/lead-rtva-011-josep-dalleres/analisi-acustica.tsv") if (prospect_dalleres / "analisi-acustica.tsv").exists() else []
    dalleres_small = prospect_dalleres / "asr/josep-dalleres-small-nocontext.json"
    dalleres_base = prospect_dalleres / "asr/josep-dalleres-base-nocontext.json"
    if (
        not (prospect_dalleres / "audio.wav").exists()
        or not dalleres_small.exists()
        or not dalleres_base.exists()
        or len(dalleres_forms) != 57
        or len(dalleres_queue) != 34
        or len(dalleres_acoustic) != 34
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in dalleres_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in dalleres_queue)
        or "fora del recompte" not in dalleres_report
        or "síndic general" not in dalleres_report
    ):
        errors.append("l'expedient Josep Dallarès no conserva àudio, doble ASR, formes contextuals i cua separada")
    else:
        try:
            import json
            dalleres_small_last = json.loads(dalleres_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            dalleres_base_last = json.loads(dalleres_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if dalleres_small_last < 3_700_000 or dalleres_base_last < 3_700_000:
                errors.append("l'expedient Josep Dallarès no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Josep Dallarès invàlid")
    prospect_forne = ROOT / "proveniencia/prospeccio/lead-rtva-012-marc-forne"
    forne_report = (prospect_forne / "informe.md").read_text(encoding="utf-8") if (prospect_forne / "informe.md").exists() else ""
    forne_forms = read("proveniencia/prospeccio/lead-rtva-012-marc-forne/formes.tsv") if (prospect_forne / "formes.tsv").exists() else []
    forne_queue = read("proveniencia/prospeccio/lead-rtva-012-marc-forne/cua-audicio.tsv") if (prospect_forne / "cua-audicio.tsv").exists() else []
    forne_acoustic = read("proveniencia/prospeccio/lead-rtva-012-marc-forne/analisi-acustica.tsv") if (prospect_forne / "analisi-acustica.tsv").exists() else []
    forne_small = prospect_forne / "asr/marc-forne-small-nocontext.json"
    forne_base = prospect_forne / "asr/marc-forne-base-nocontext.json"
    if (
        not (prospect_forne / "audio.wav").exists()
        or not forne_small.exists()
        or not forne_base.exists()
        or len(forne_forms) != 57
        or len(forne_queue) != 32
        or len(forne_acoustic) != 32
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in forne_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in forne_queue)
        or "fora del recompte" not in forne_report
        or "cap de Govern" not in forne_report
    ):
        errors.append("l'expedient Marc Forné no conserva àudio, doble ASR, formes contextuals i cua separada")
    else:
        try:
            import json
            forne_small_last = json.loads(forne_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            forne_base_last = json.loads(forne_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if forne_small_last < 3_100_000 or forne_base_last < 3_100_000:
                errors.append("l'expedient Marc Forné no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Marc Forné invàlid")
    prospect_vilanova = ROOT / "proveniencia/prospeccio/lead-rtva-013-pere-vilanova"
    vilanova_report = (prospect_vilanova / "informe.md").read_text(encoding="utf-8") if (prospect_vilanova / "informe.md").exists() else ""
    vilanova_forms = read("proveniencia/prospeccio/lead-rtva-013-pere-vilanova/formes.tsv") if (prospect_vilanova / "formes.tsv").exists() else []
    vilanova_queue = read("proveniencia/prospeccio/lead-rtva-013-pere-vilanova/cua-audicio.tsv") if (prospect_vilanova / "cua-audicio.tsv").exists() else []
    vilanova_acoustic = read("proveniencia/prospeccio/lead-rtva-013-pere-vilanova/analisi-acustica.tsv") if (prospect_vilanova / "analisi-acustica.tsv").exists() else []
    vilanova_small = prospect_vilanova / "asr/pere-vilanova-small-nocontext.json"
    vilanova_base = prospect_vilanova / "asr/pere-vilanova-base-nocontext.json"
    if (
        not (prospect_vilanova / "audio.wav").exists()
        or not vilanova_small.exists()
        or not vilanova_base.exists()
        or len(vilanova_forms) != 56
        or len(vilanova_queue) != 30
        or len(vilanova_acoustic) != 30
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in vilanova_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in vilanova_queue)
        or "fora del recompte" not in vilanova_report
        or "Constitució" not in vilanova_report
    ):
        errors.append("l'expedient Pere Vilanova no conserva àudio, doble ASR, formes contextuals i cua separada")
    else:
        try:
            import json
            vilanova_small_last = json.loads(vilanova_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            vilanova_base_last = json.loads(vilanova_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if vilanova_small_last < 3_500_000 or vilanova_base_last < 3_500_000:
                errors.append("l'expedient Pere Vilanova no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Pere Vilanova invàlid")
    prospect_burgues = ROOT / "proveniencia/prospeccio/lead-rtva-014-joan-burgues"
    burgues_report = (prospect_burgues / "informe.md").read_text(encoding="utf-8") if (prospect_burgues / "informe.md").exists() else ""
    burgues_forms = read("proveniencia/prospeccio/lead-rtva-014-joan-burgues/formes.tsv") if (prospect_burgues / "formes.tsv").exists() else []
    burgues_queue = read("proveniencia/prospeccio/lead-rtva-014-joan-burgues/cua-audicio.tsv") if (prospect_burgues / "cua-audicio.tsv").exists() else []
    burgues_acoustic = read("proveniencia/prospeccio/lead-rtva-014-joan-burgues/analisi-acustica.tsv") if (prospect_burgues / "analisi-acustica.tsv").exists() else []
    burgues_small = prospect_burgues / "asr/joan-burgues-small-nocontext.json"
    burgues_base = prospect_burgues / "asr/joan-burgues-base-nocontext.json"
    if (
        not (prospect_burgues / "audio.wav").exists()
        or not burgues_small.exists()
        or not burgues_base.exists()
        or len(burgues_forms) != 55
        or len(burgues_queue) != 27
        or len(burgues_acoustic) != 27
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in burgues_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in burgues_queue)
        or "fora del recompte" not in burgues_report
        or "fotografia" not in burgues_report
    ):
        errors.append("l'expedient Joan Burgués no conserva àudio, doble ASR, formes culturals i cua separada")
    else:
        try:
            import json
            burgues_small_last = json.loads(burgues_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            burgues_base_last = json.loads(burgues_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if burgues_small_last < 3_100_000 or burgues_base_last < 3_100_000:
                errors.append("l'expedient Joan Burgués no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Joan Burgués invàlid")
    prospect_baro = ROOT / "proveniencia/prospeccio/lead-rtva-015-isidre-baro"
    baro_report = (prospect_baro / "informe.md").read_text(encoding="utf-8") if (prospect_baro / "informe.md").exists() else ""
    baro_forms = read("proveniencia/prospeccio/lead-rtva-015-isidre-baro/formes.tsv") if (prospect_baro / "formes.tsv").exists() else []
    baro_queue = read("proveniencia/prospeccio/lead-rtva-015-isidre-baro/cua-audicio.tsv") if (prospect_baro / "cua-audicio.tsv").exists() else []
    baro_acoustic = read("proveniencia/prospeccio/lead-rtva-015-isidre-baro/analisi-acustica.tsv") if (prospect_baro / "analisi-acustica.tsv").exists() else []
    baro_small = prospect_baro / "asr/isidre-baro-small-nocontext.json"
    baro_base = prospect_baro / "asr/isidre-baro-base-nocontext.json"
    if (
        not (prospect_baro / "audio.wav").exists()
        or not baro_small.exists()
        or not baro_base.exists()
        or len(baro_forms) != 55
        or len(baro_queue) != 33
        or len(baro_acoustic) != 33
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in baro_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in baro_queue)
        or "fora del recompte" not in baro_report
        or "olimpisme" not in baro_report
    ):
        errors.append("l'expedient Isidre Baró no conserva àudio, doble ASR, formes esportives i cua separada")
    else:
        try:
            import json
            baro_small_last = json.loads(baro_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            baro_base_last = json.loads(baro_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if baro_small_last < 3_200_000 or baro_base_last < 3_200_000:
                errors.append("l'expedient Isidre Baró no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Isidre Baró invàlid")
    prospect_areny = ROOT / "proveniencia/prospeccio/lead-rtva-016-josep-areny"
    areny_report = (prospect_areny / "informe.md").read_text(encoding="utf-8") if (prospect_areny / "informe.md").exists() else ""
    areny_forms = read("proveniencia/prospeccio/lead-rtva-016-josep-areny/formes.tsv") if (prospect_areny / "formes.tsv").exists() else []
    areny_queue = read("proveniencia/prospeccio/lead-rtva-016-josep-areny/cua-audicio.tsv") if (prospect_areny / "cua-audicio.tsv").exists() else []
    areny_acoustic = read("proveniencia/prospeccio/lead-rtva-016-josep-areny/analisi-acustica.tsv") if (prospect_areny / "analisi-acustica.tsv").exists() else []
    areny_small = prospect_areny / "asr/josep-areny-small-nocontext.json"
    areny_base = prospect_areny / "asr/josep-areny-base-nocontext.json"
    if (
        not (prospect_areny / "audio.wav").exists()
        or not areny_small.exists()
        or not areny_base.exists()
        or len(areny_forms) != 62
        or len(areny_queue) != 42
        or len(areny_acoustic) != 42
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in areny_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in areny_queue)
        or "fora del recompte" not in areny_report
        or "Soldeu" not in areny_report
    ):
        errors.append("l'expedient Josep Areny no conserva àudio, doble ASR, formes hoteleres i cua separada")
    else:
        try:
            import json
            areny_small_last = json.loads(areny_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            areny_base_last = json.loads(areny_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if areny_small_last < 3_700_000 or areny_base_last < 3_700_000:
                errors.append("l'expedient Josep Areny no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Josep Areny invàlid")
    prospect_simo = ROOT / "proveniencia/prospeccio/lead-rtva-017-simo-duro"
    simo_report = (prospect_simo / "informe.md").read_text(encoding="utf-8") if (prospect_simo / "informe.md").exists() else ""
    simo_forms = read("proveniencia/prospeccio/lead-rtva-017-simo-duro/formes.tsv") if (prospect_simo / "formes.tsv").exists() else []
    simo_queue = read("proveniencia/prospeccio/lead-rtva-017-simo-duro/cua-audicio.tsv") if (prospect_simo / "cua-audicio.tsv").exists() else []
    simo_acoustic = read("proveniencia/prospeccio/lead-rtva-017-simo-duro/analisi-acustica.tsv") if (prospect_simo / "analisi-acustica.tsv").exists() else []
    simo_small = prospect_simo / "asr/simo-duro-small-nocontext.json"
    simo_base = prospect_simo / "asr/simo-duro-base-nocontext.json"
    if (
        not (prospect_simo / "audio.wav").exists()
        or not simo_small.exists()
        or not simo_base.exists()
        or len(simo_forms) != 69
        or len(simo_queue) != 46
        or len(simo_acoustic) != 46
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in simo_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in simo_queue)
        or "fora del recompte" not in simo_report
        or "ramader" not in simo_report
        or "memoria-dun-pais-pgm14_simo-duro-20582" not in simo_report
    ):
        errors.append("l'expedient Simó Duró no conserva àudio, doble ASR, formes educatives i cua separada")
    else:
        try:
            import json
            simo_small_last = json.loads(simo_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            simo_base_last = json.loads(simo_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if simo_small_last < 3_500_000 or simo_base_last < 3_500_000:
                errors.append("l'expedient Simó Duró no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Simó Duró invàlid")
    prospect_fiter = ROOT / "proveniencia/prospeccio/lead-rtva-018-ricard-fiter"
    fiter_report = (prospect_fiter / "informe.md").read_text(encoding="utf-8") if (prospect_fiter / "informe.md").exists() else ""
    fiter_forms = read("proveniencia/prospeccio/lead-rtva-018-ricard-fiter/formes.tsv") if (prospect_fiter / "formes.tsv").exists() else []
    fiter_queue = read("proveniencia/prospeccio/lead-rtva-018-ricard-fiter/cua-audicio.tsv") if (prospect_fiter / "cua-audicio.tsv").exists() else []
    fiter_acoustic = read("proveniencia/prospeccio/lead-rtva-018-ricard-fiter/analisi-acustica.tsv") if (prospect_fiter / "analisi-acustica.tsv").exists() else []
    fiter_small = prospect_fiter / "asr/ricard-fiter-small-nocontext.json"
    fiter_base = prospect_fiter / "asr/ricard-fiter-base-nocontext.json"
    if (
        not (prospect_fiter / "audio.wav").exists()
        or not fiter_small.exists()
        or not fiter_base.exists()
        or len(fiter_forms) != 74
        or len(fiter_queue) != 45
        or len(fiter_acoustic) != 45
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in fiter_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in fiter_queue)
        or "fora del recompte" not in fiter_report
        or "drets humans" not in fiter_report
        or "ricard-fiter-170220252" not in fiter_report
    ):
        errors.append("l'expedient Ricard Fiter no conserva àudio, doble ASR, formes jurídiques i cua separada")
    else:
        try:
            import json
            fiter_small_last = json.loads(fiter_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            fiter_base_last = json.loads(fiter_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if fiter_small_last < 3_100_000 or fiter_base_last < 3_100_000:
                errors.append("l'expedient Ricard Fiter no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Ricard Fiter invàlid")
    prospect_lisa = ROOT / "proveniencia/prospeccio/lead-rtva-019-lisa-cruz"
    lisa_report = (prospect_lisa / "informe.md").read_text(encoding="utf-8") if (prospect_lisa / "informe.md").exists() else ""
    lisa_forms = read("proveniencia/prospeccio/lead-rtva-019-lisa-cruz/formes.tsv") if (prospect_lisa / "formes.tsv").exists() else []
    lisa_queue = read("proveniencia/prospeccio/lead-rtva-019-lisa-cruz/cua-audicio.tsv") if (prospect_lisa / "cua-audicio.tsv").exists() else []
    lisa_acoustic = read("proveniencia/prospeccio/lead-rtva-019-lisa-cruz/analisi-acustica.tsv") if (prospect_lisa / "analisi-acustica.tsv").exists() else []
    lisa_small = prospect_lisa / "asr/lisa-cruz-small-nocontext.json"
    lisa_base = prospect_lisa / "asr/lisa-cruz-base-nocontext.json"
    if (
        not (prospect_lisa / "audio.wav").exists()
        or not lisa_small.exists()
        or not lisa_base.exists()
        or len(lisa_forms) != 74
        or len(lisa_queue) != 38
        or len(lisa_acoustic) != 38
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in lisa_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in lisa_queue)
        or "fora del recompte" not in lisa_report
        or "joventut" not in lisa_report
        or "clau-19-desembre-2024-20559" not in lisa_report
    ):
        errors.append("l'expedient Lisa Cruz no conserva àudio, doble ASR, formes de joventut i cua separada")
    else:
        try:
            import json
            lisa_small_last = json.loads(lisa_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            lisa_base_last = json.loads(lisa_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if lisa_small_last < 1_700_000 or lisa_base_last < 1_700_000:
                errors.append("l'expedient Lisa Cruz no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Lisa Cruz invàlid")
    prospect_monica = ROOT / "proveniencia/prospeccio/lead-rtva-020-monica-bonell"
    monica_report = (prospect_monica / "informe.md").read_text(encoding="utf-8") if (prospect_monica / "informe.md").exists() else ""
    monica_forms = read("proveniencia/prospeccio/lead-rtva-020-monica-bonell/formes.tsv") if (prospect_monica / "formes.tsv").exists() else []
    monica_queue = read("proveniencia/prospeccio/lead-rtva-020-monica-bonell/cua-audicio.tsv") if (prospect_monica / "cua-audicio.tsv").exists() else []
    monica_acoustic = read("proveniencia/prospeccio/lead-rtva-020-monica-bonell/analisi-acustica.tsv") if (prospect_monica / "analisi-acustica.tsv").exists() else []
    monica_small = prospect_monica / "asr/monica-bonell-small-nocontext.json"
    monica_base = prospect_monica / "asr/monica-bonell-base-nocontext.json"
    if (
        not (prospect_monica / "audio.wav").exists()
        or not monica_small.exists()
        or not monica_base.exists()
        or len(monica_forms) != 73
        or len(monica_queue) != 46
        or len(monica_acoustic) != 46
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in monica_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in monica_queue)
        or "fora del recompte" not in monica_report
        or "ministeri" not in monica_report
        or "video-entrevista-monica-bonell-ministra-cultura-joventut" not in monica_report
    ):
        errors.append("l'expedient Mònica Bonell no conserva àudio, doble ASR, formes culturals i cua separada")
    else:
        try:
            import json
            monica_small_last = json.loads(monica_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            monica_base_last = json.loads(monica_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if monica_small_last < 2_000_000 or monica_base_last < 2_000_000:
                errors.append("l'expedient Mònica Bonell no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Mònica Bonell invàlid")
    prospect_bonaventura = ROOT / "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua"
    bonaventura_report = (prospect_bonaventura / "informe.md").read_text(encoding="utf-8") if (prospect_bonaventura / "informe.md").exists() else ""
    bonaventura_forms = read("proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/formes.tsv") if (prospect_bonaventura / "formes.tsv").exists() else []
    bonaventura_queue = read("proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/cua-audicio.tsv") if (prospect_bonaventura / "cua-audicio.tsv").exists() else []
    bonaventura_acoustic = read("proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/analisi-acustica.tsv") if (prospect_bonaventura / "analisi-acustica.tsv").exists() else []
    bonaventura_small = prospect_bonaventura / "asr/bonaventura-riberaygua-small-nocontext.json"
    bonaventura_base = prospect_bonaventura / "asr/bonaventura-riberaygua-base-nocontext.json"
    if (
        not (prospect_bonaventura / "audio.wav").exists()
        or not bonaventura_small.exists()
        or not bonaventura_base.exists()
        or len(bonaventura_forms) != 86
        or len(bonaventura_queue) != 36
        or len(bonaventura_acoustic) != 36
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in bonaventura_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in bonaventura_queue)
        or "fora del recompte" not in bonaventura_report
        or "empresari" not in bonaventura_report
        or "bonaventura-riberaygua-080120249" not in bonaventura_report
    ):
        errors.append("l'expedient Bonaventura Riberaygua no conserva àudio, doble ASR, formes econòmiques i cua separada")
    else:
        try:
            import json
            bonaventura_small_last = json.loads(bonaventura_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            bonaventura_base_last = json.loads(bonaventura_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if bonaventura_small_last < 3_100_000 or bonaventura_base_last < 3_100_000:
                errors.append("l'expedient Bonaventura Riberaygua no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Bonaventura Riberaygua invàlid")
    prospect_marsal = ROOT / "proveniencia/prospeccio/lead-rtva-022-josep-marsal"
    marsal_report = (prospect_marsal / "informe.md").read_text(encoding="utf-8") if (prospect_marsal / "informe.md").exists() else ""
    marsal_forms = read("proveniencia/prospeccio/lead-rtva-022-josep-marsal/formes.tsv") if (prospect_marsal / "formes.tsv").exists() else []
    marsal_queue = read("proveniencia/prospeccio/lead-rtva-022-josep-marsal/cua-audicio.tsv") if (prospect_marsal / "cua-audicio.tsv").exists() else []
    marsal_acoustic = read("proveniencia/prospeccio/lead-rtva-022-josep-marsal/analisi-acustica.tsv") if (prospect_marsal / "analisi-acustica.tsv").exists() else []
    marsal_small = prospect_marsal / "asr/josep-marsal-small-nocontext.json"
    marsal_base = prospect_marsal / "asr/josep-marsal-base-nocontext.json"
    if (
        not (prospect_marsal / "audio.wav").exists()
        or not marsal_small.exists()
        or not marsal_base.exists()
        or len(marsal_forms) != 86
        or len(marsal_queue) != 37
        or len(marsal_acoustic) != 37
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in marsal_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in marsal_queue)
        or "fora del recompte" not in marsal_report
        or "política" not in marsal_report
        or "josep-marcal-180220251" not in marsal_report
    ):
        errors.append("l'expedient Josep Marsal no conserva àudio, doble ASR, formes institucionals i cua separada")
    else:
        try:
            import json
            marsal_small_last = json.loads(marsal_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            marsal_base_last = json.loads(marsal_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if marsal_small_last < 3_250_000 or marsal_base_last < 3_250_000:
                errors.append("l'expedient Josep Marsal no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Josep Marsal invàlid")
    prospect_cases = ROOT / "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases"
    cases_report = (prospect_cases / "informe.md").read_text(encoding="utf-8") if (prospect_cases / "informe.md").exists() else ""
    cases_forms = read("proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/formes.tsv") if (prospect_cases / "formes.tsv").exists() else []
    cases_queue = read("proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/cua-audicio.tsv") if (prospect_cases / "cua-audicio.tsv").exists() else []
    cases_acoustic = read("proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/analisi-acustica.tsv") if (prospect_cases / "analisi-acustica.tsv").exists() else []
    cases_small = prospect_cases / "asr/josep-maria-cases-small-nocontext.json"
    cases_base = prospect_cases / "asr/josep-maria-cases-base-nocontext.json"
    if (
        not (prospect_cases / "audio.wav").exists()
        or not cases_small.exists()
        or not cases_base.exists()
        or len(cases_forms) != 84
        or len(cases_queue) != 34
        or len(cases_acoustic) != 34
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in cases_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in cases_queue)
        or "fora del recompte" not in cases_report
        or "empresari" not in cases_report
        or "josep-maria-cases-pgm23-210220250" not in cases_report
    ):
        errors.append("l'expedient Josep Maria Cases no conserva àudio, doble ASR, formes econòmiques i cua separada")
    else:
        try:
            import json
            cases_small_last = json.loads(cases_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            cases_base_last = json.loads(cases_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if cases_small_last < 3_300_000 or cases_base_last < 3_300_000:
                errors.append("l'expedient Josep Maria Cases no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Josep Maria Cases invàlid")
    prospect_denisa = ROOT / "proveniencia/prospeccio/lead-rtva-024-denisa-font"
    denisa_report = (prospect_denisa / "informe.md").read_text(encoding="utf-8") if (prospect_denisa / "informe.md").exists() else ""
    denisa_forms = read("proveniencia/prospeccio/lead-rtva-024-denisa-font/formes.tsv") if (prospect_denisa / "formes.tsv").exists() else []
    denisa_queue = read("proveniencia/prospeccio/lead-rtva-024-denisa-font/cua-audicio.tsv") if (prospect_denisa / "cua-audicio.tsv").exists() else []
    denisa_acoustic = read("proveniencia/prospeccio/lead-rtva-024-denisa-font/analisi-acustica.tsv") if (prospect_denisa / "analisi-acustica.tsv").exists() else []
    denisa_small = prospect_denisa / "asr/denisa-font-small-nocontext.json"
    denisa_base = prospect_denisa / "asr/denisa-font-base-nocontext.json"
    if (
        not (prospect_denisa / "audio.wav").exists()
        or not denisa_small.exists()
        or not denisa_base.exists()
        or len(denisa_forms) != 85
        or len(denisa_queue) != 35
        or len(denisa_acoustic) != 35
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in denisa_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in denisa_queue)
        or "fora del recompte" not in denisa_report
        or "tradició" not in denisa_report
        or "denisa-font-pgm23-210220250" not in denisa_report
    ):
        errors.append("l'expedient Denisa Font no conserva àudio, doble ASR, formes culturals i cua separada")
    else:
        try:
            import json
            denisa_small_last = json.loads(denisa_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            denisa_base_last = json.loads(denisa_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if denisa_small_last < 3_150_000 or denisa_base_last < 3_150_000:
                errors.append("l'expedient Denisa Font no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Denisa Font invàlid")
    prospect_gelabert = ROOT / "proveniencia/prospeccio/lead-rtva-025-albert-gelabert"
    gelabert_report = (prospect_gelabert / "informe.md").read_text(encoding="utf-8") if (prospect_gelabert / "informe.md").exists() else ""
    gelabert_forms = read("proveniencia/prospeccio/lead-rtva-025-albert-gelabert/formes.tsv") if (prospect_gelabert / "formes.tsv").exists() else []
    gelabert_queue = read("proveniencia/prospeccio/lead-rtva-025-albert-gelabert/cua-audicio.tsv") if (prospect_gelabert / "cua-audicio.tsv").exists() else []
    gelabert_acoustic = read("proveniencia/prospeccio/lead-rtva-025-albert-gelabert/analisi-acustica.tsv") if (prospect_gelabert / "analisi-acustica.tsv").exists() else []
    gelabert_small = prospect_gelabert / "asr/albert-gelabert-small-nocontext.json"
    gelabert_base = prospect_gelabert / "asr/albert-gelabert-base-nocontext.json"
    if (
        not (prospect_gelabert / "audio.wav").exists()
        or not gelabert_small.exists()
        or not gelabert_base.exists()
        or len(gelabert_forms) != 82
        or len(gelabert_queue) != 43
        or len(gelabert_acoustic) != 43
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in gelabert_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in gelabert_queue)
        or "fora del recompte" not in gelabert_report
        or "educació" not in gelabert_report
        or "albert-gelabert-pgm23-210220250" not in gelabert_report
    ):
        errors.append("l'expedient Albert Gelabert no conserva àudio, doble ASR, formes socials i cua separada")
    else:
        try:
            import json
            gelabert_small_last = json.loads(gelabert_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            gelabert_base_last = json.loads(gelabert_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if gelabert_small_last < 3_250_000 or gelabert_base_last < 3_250_000:
                errors.append("l'expedient Albert Gelabert no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Albert Gelabert invàlid")
    prospect_rosa = ROOT / "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico"
    rosa_report = (prospect_rosa / "informe.md").read_text(encoding="utf-8") if (prospect_rosa / "informe.md").exists() else ""
    rosa_forms = read("proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/formes.tsv") if (prospect_rosa / "formes.tsv").exists() else []
    rosa_queue = read("proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/cua-audicio.tsv") if (prospect_rosa / "cua-audicio.tsv").exists() else []
    rosa_acoustic = read("proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/analisi-acustica.tsv") if (prospect_rosa / "analisi-acustica.tsv").exists() else []
    rosa_small = prospect_rosa / "asr/rosa-maria-mandico-small-nocontext.json"
    rosa_base = prospect_rosa / "asr/rosa-maria-mandico-base-nocontext.json"
    if (
        not (prospect_rosa / "audio.wav").exists()
        or not rosa_small.exists()
        or not rosa_base.exists()
        or len(rosa_forms) != 82
        or len(rosa_queue) != 36
        or len(rosa_acoustic) != 36
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in rosa_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in rosa_queue)
        or "fora del recompte" not in rosa_report
        or "història" not in rosa_report
        or "rosa-maria-mandico-pgm23-210220260" not in rosa_report
    ):
        errors.append("l'expedient Rosa Maria Mandicó no conserva àudio, doble ASR, formes culturals i cua separada")
    else:
        try:
            import json
            rosa_small_last = json.loads(rosa_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            rosa_base_last = json.loads(rosa_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if rosa_small_last < 3_100_000 or rosa_base_last < 3_100_000:
                errors.append("l'expedient Rosa Maria Mandicó no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Rosa Maria Mandicó invàlid")
    prospect_jordi = ROOT / "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet"
    jordi_report = (prospect_jordi / "informe.md").read_text(encoding="utf-8") if (prospect_jordi / "informe.md").exists() else ""
    jordi_forms = read("proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/formes.tsv") if (prospect_jordi / "formes.tsv").exists() else []
    jordi_queue = read("proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/cua-audicio.tsv") if (prospect_jordi / "cua-audicio.tsv").exists() else []
    jordi_acoustic = read("proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/analisi-acustica.tsv") if (prospect_jordi / "analisi-acustica.tsv").exists() else []
    jordi_small = prospect_jordi / "asr/jordi-guillamet-small-nocontext.json"
    jordi_base = prospect_jordi / "asr/jordi-guillamet-base-nocontext.json"
    if (
        not (prospect_jordi / "audio.wav").exists()
        or not jordi_small.exists()
        or not jordi_base.exists()
        or len(jordi_forms) != 84
        or len(jordi_queue) != 40
        or len(jordi_acoustic) != 40
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in jordi_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in jordi_queue)
        or "fora del recompte" not in jordi_report
        or "cultura" not in jordi_report
        or "jordi-guillamet-pgm23-210220270" not in jordi_report
    ):
        errors.append("l'expedient Jordi Guillamet no conserva àudio, doble ASR, formes socials i cua separada")
    else:
        try:
            import json
            jordi_small_last = json.loads(jordi_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            jordi_base_last = json.loads(jordi_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if jordi_small_last < 3_200_000 or jordi_base_last < 3_200_000:
                errors.append("l'expedient Jordi Guillamet no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Jordi Guillamet invàlid")
    prospect_pere = ROOT / "proveniencia/prospeccio/lead-rtva-028-pere-besoli"
    pere_report = (prospect_pere / "informe.md").read_text(encoding="utf-8") if (prospect_pere / "informe.md").exists() else ""
    pere_forms = read("proveniencia/prospeccio/lead-rtva-028-pere-besoli/formes.tsv") if (prospect_pere / "formes.tsv").exists() else []
    pere_queue = read("proveniencia/prospeccio/lead-rtva-028-pere-besoli/cua-audicio.tsv") if (prospect_pere / "cua-audicio.tsv").exists() else []
    pere_acoustic = read("proveniencia/prospeccio/lead-rtva-028-pere-besoli/analisi-acustica.tsv") if (prospect_pere / "analisi-acustica.tsv").exists() else []
    pere_small = prospect_pere / "asr/pere-besoli-small-nocontext.json"
    pere_base = prospect_pere / "asr/pere-besoli-base-nocontext.json"
    if (
        not (prospect_pere / "audio.wav").exists()
        or not pere_small.exists()
        or not pere_base.exists()
        or len(pere_forms) != 84
        or len(pere_queue) != 38
        or len(pere_acoustic) != 38
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in pere_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in pere_queue)
        or "fora del recompte" not in pere_report
        or "empresa" not in pere_report
        or "pere-besoli-pgm23-210220280" not in pere_report
    ):
        errors.append("l'expedient Pere Besolí no conserva àudio, doble ASR, formes econòmiques i cua separada")
    else:
        try:
            import json
            pere_small_last = json.loads(pere_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            pere_base_last = json.loads(pere_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if pere_small_last < 3_700_000 or pere_base_last < 3_700_000:
                errors.append("l'expedient Pere Besolí no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Pere Besolí invàlid")
    prospect_angelina = ROOT / "proveniencia/prospeccio/lead-rtva-029-angelina-mas"
    angelina_report = (prospect_angelina / "informe.md").read_text(encoding="utf-8") if (prospect_angelina / "informe.md").exists() else ""
    angelina_forms = read("proveniencia/prospeccio/lead-rtva-029-angelina-mas/formes.tsv") if (prospect_angelina / "formes.tsv").exists() else []
    angelina_queue = read("proveniencia/prospeccio/lead-rtva-029-angelina-mas/cua-audicio.tsv") if (prospect_angelina / "cua-audicio.tsv").exists() else []
    angelina_acoustic = read("proveniencia/prospeccio/lead-rtva-029-angelina-mas/analisi-acustica.tsv") if (prospect_angelina / "analisi-acustica.tsv").exists() else []
    angelina_small = prospect_angelina / "asr/angelina-mas-small-nocontext.json"
    angelina_base = prospect_angelina / "asr/angelina-mas-base-nocontext.json"
    if (
        not (prospect_angelina / "audio.wav").exists()
        or not angelina_small.exists()
        or not angelina_base.exists()
        or len(angelina_forms) != 83
        or len(angelina_queue) != 37
        or len(angelina_acoustic) != 37
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in angelina_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in angelina_queue)
        or "fora del recompte" not in angelina_report
        or "història" not in angelina_report
        or "angelina-mas-pgm23-210220290" not in angelina_report
    ):
        errors.append("l'expedient Angelina Mas no conserva àudio, doble ASR, formes socials i cua separada")
    else:
        try:
            import json
            angelina_small_last = json.loads(angelina_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            angelina_base_last = json.loads(angelina_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if angelina_small_last < 3_000_000 or angelina_base_last < 3_000_000:
                errors.append("l'expedient Angelina Mas no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Angelina Mas invàlid")
    prospect_casimir = ROOT / "proveniencia/prospeccio/lead-rtva-030-casimir-arajol"
    casimir_report = (prospect_casimir / "informe.md").read_text(encoding="utf-8") if (prospect_casimir / "informe.md").exists() else ""
    casimir_forms = read("proveniencia/prospeccio/lead-rtva-030-casimir-arajol/formes.tsv") if (prospect_casimir / "formes.tsv").exists() else []
    casimir_queue = read("proveniencia/prospeccio/lead-rtva-030-casimir-arajol/cua-audicio.tsv") if (prospect_casimir / "cua-audicio.tsv").exists() else []
    casimir_acoustic = read("proveniencia/prospeccio/lead-rtva-030-casimir-arajol/analisi-acustica.tsv") if (prospect_casimir / "analisi-acustica.tsv").exists() else []
    casimir_small = prospect_casimir / "asr/casimir-arajol-small-nocontext.json"
    casimir_base = prospect_casimir / "asr/casimir-arajol-base-nocontext.json"
    if (
        not (prospect_casimir / "audio.wav").exists()
        or not casimir_small.exists()
        or not casimir_base.exists()
        or len(casimir_forms) != 85
        or len(casimir_queue) != 39
        or len(casimir_acoustic) != 39
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in casimir_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in casimir_queue)
        or "fora del recompte" not in casimir_report
        or "cultura" not in casimir_report
        or "casimir-arajol-pgm23-210220300" not in casimir_report
    ):
        errors.append("l'expedient Casimir Arajol no conserva àudio, doble ASR, formes econòmiques i cua separada")
    else:
        try:
            import json
            casimir_small_last = json.loads(casimir_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            casimir_base_last = json.loads(casimir_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if casimir_small_last < 3_100_000 or casimir_base_last < 3_100_000:
                errors.append("l'expedient Casimir Arajol no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Casimir Arajol invàlid")
    prospect_anna = ROOT / "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua"
    anna_report = (prospect_anna / "informe.md").read_text(encoding="utf-8") if (prospect_anna / "informe.md").exists() else ""
    anna_forms = read("proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/formes.tsv") if (prospect_anna / "formes.tsv").exists() else []
    anna_queue = read("proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/cua-audicio.tsv") if (prospect_anna / "cua-audicio.tsv").exists() else []
    anna_acoustic = read("proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/analisi-acustica.tsv") if (prospect_anna / "analisi-acustica.tsv").exists() else []
    anna_small = prospect_anna / "asr/anna-riberaygua-small-nocontext.json"
    anna_base = prospect_anna / "asr/anna-riberaygua-base-nocontext.json"
    if (
        not (prospect_anna / "audio.wav").exists()
        or not anna_small.exists()
        or not anna_base.exists()
        or len(anna_forms) != 87
        or len(anna_queue) != 46
        or len(anna_acoustic) != 46
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in anna_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in anna_queue)
        or "fora del recompte" not in anna_report
        or "empresa" not in anna_report
        or "anna-riberaygua-080120245" not in anna_report
    ):
        errors.append("l'expedient Anna Riberaygua no conserva àudio, doble ASR, formes socials i cua separada")
    else:
        try:
            import json
            anna_small_last = json.loads(anna_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            anna_base_last = json.loads(anna_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if anna_small_last < 3_700_000 or anna_base_last < 3_700_000:
                errors.append("l'expedient Anna Riberaygua no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Anna Riberaygua invàlid")
    prospect_david = ROOT / "proveniencia/prospeccio/lead-yt-033-david-montane"
    david_report = (prospect_david / "informe.md").read_text(encoding="utf-8") if (prospect_david / "informe.md").exists() else ""
    david_forms = read("proveniencia/prospeccio/lead-yt-033-david-montane/formes.tsv") if (prospect_david / "formes.tsv").exists() else []
    david_queue = read("proveniencia/prospeccio/lead-yt-033-david-montane/cua-audicio.tsv") if (prospect_david / "cua-audicio.tsv").exists() else []
    david_acoustic = read("proveniencia/prospeccio/lead-yt-033-david-montane/analisi-acustica.tsv") if (prospect_david / "analisi-acustica.tsv").exists() else []
    david_small = prospect_david / "asr/david-montane-small-nocontext.json"
    david_base = prospect_david / "asr/david-montane-base-nocontext.json"
    if (
        not (prospect_david / "audio.wav").exists()
        or not david_small.exists()
        or not david_base.exists()
        or len(david_forms) != 64
        or len(david_queue) != 28
        or len(david_acoustic) != 28
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in david_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in david_queue)
        or "fora del recompte" not in david_report
        or "pressupost" not in david_report
        or "youtube.com/watch?v=-Nn6jatvEAY" not in david_report
    ):
        errors.append("l'expedient David Montané no conserva àudio, doble ASR, formes institucionals i cua separada")
    else:
        try:
            import json
            david_small_last = json.loads(david_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            david_base_last = json.loads(david_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if david_small_last < 360_000 or david_base_last < 360_000:
                errors.append("l'expedient David Montané no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient David Montané invàlid")
    prospect_antoni = ROOT / "proveniencia/prospeccio/lead-yt-034-antoni-marti"
    antoni_report = (prospect_antoni / "informe.md").read_text(encoding="utf-8") if (prospect_antoni / "informe.md").exists() else ""
    antoni_forms = read("proveniencia/prospeccio/lead-yt-034-antoni-marti/formes.tsv") if (prospect_antoni / "formes.tsv").exists() else []
    antoni_queue = read("proveniencia/prospeccio/lead-yt-034-antoni-marti/cua-audicio.tsv") if (prospect_antoni / "cua-audicio.tsv").exists() else []
    antoni_acoustic = read("proveniencia/prospeccio/lead-yt-034-antoni-marti/analisi-acustica.tsv") if (prospect_antoni / "analisi-acustica.tsv").exists() else []
    antoni_small = prospect_antoni / "asr/antoni-marti-small-nocontext.json"
    antoni_base = prospect_antoni / "asr/antoni-marti-base-nocontext.json"
    if (
        not (prospect_antoni / "audio.wav").exists()
        or not antoni_small.exists()
        or not antoni_base.exists()
        or len(antoni_forms) != 68
        or len(antoni_queue) != 33
        or len(antoni_acoustic) != 33
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in antoni_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in antoni_queue)
        or "fora del recompte" not in antoni_report
        or "transparència" not in antoni_report
        or "youtube.com/watch?v=WAN5vuqAOhQ" not in antoni_report
    ):
        errors.append("l'expedient Antoni Martí Petit no conserva àudio, doble ASR, formes institucionals i cua separada")
    else:
        try:
            import json
            antoni_small_last = json.loads(antoni_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            antoni_base_last = json.loads(antoni_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if antoni_small_last < 1_600_000 or antoni_base_last < 1_600_000:
                errors.append("l'expedient Antoni Martí Petit no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Antoni Martí Petit invàlid")
    prospect_cerni = ROOT / "proveniencia/prospeccio/lead-yt-035-cerni-escale"
    cerni_report = (prospect_cerni / "informe.md").read_text(encoding="utf-8") if (prospect_cerni / "informe.md").exists() else ""
    cerni_forms = read("proveniencia/prospeccio/lead-yt-035-cerni-escale/formes.tsv") if (prospect_cerni / "formes.tsv").exists() else []
    cerni_queue = read("proveniencia/prospeccio/lead-yt-035-cerni-escale/cua-audicio.tsv") if (prospect_cerni / "cua-audicio.tsv").exists() else []
    cerni_acoustic = read("proveniencia/prospeccio/lead-yt-035-cerni-escale/analisi-acustica.tsv") if (prospect_cerni / "analisi-acustica.tsv").exists() else []
    cerni_small = prospect_cerni / "asr/cerni-escale-small-nocontext.json"
    cerni_base = prospect_cerni / "asr/cerni-escale-base-nocontext.json"
    if (
        not (prospect_cerni / "audio.wav").exists()
        or not cerni_small.exists()
        or not cerni_base.exists()
        or len(cerni_forms) != 70
        or len(cerni_queue) != 49
        or len(cerni_acoustic) != 49
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in cerni_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in cerni_queue)
        or "fora del recompte" not in cerni_report
        or "Concòrdia" not in cerni_report
        or "youtube.com/watch?v=eRcBWJzHdyo" not in cerni_report
    ):
        errors.append("l'expedient Cerni Escalé no conserva àudio, doble ASR, formes polítiques i cua separada")
    else:
        try:
            import json
            cerni_small_last = json.loads(cerni_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            cerni_base_last = json.loads(cerni_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if cerni_small_last < 3_400_000 or cerni_base_last < 3_400_000:
                errors.append("l'expedient Cerni Escalé no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Cerni Escalé invàlid")
    prospect_xavier = ROOT / "proveniencia/prospeccio/lead-yt-036-xavier-espot"
    xavier_report = (prospect_xavier / "informe.md").read_text(encoding="utf-8") if (prospect_xavier / "informe.md").exists() else ""
    xavier_forms = read("proveniencia/prospeccio/lead-yt-036-xavier-espot/formes.tsv") if (prospect_xavier / "formes.tsv").exists() else []
    xavier_queue = read("proveniencia/prospeccio/lead-yt-036-xavier-espot/cua-audicio.tsv") if (prospect_xavier / "cua-audicio.tsv").exists() else []
    xavier_acoustic = read("proveniencia/prospeccio/lead-yt-036-xavier-espot/analisi-acustica.tsv") if (prospect_xavier / "analisi-acustica.tsv").exists() else []
    xavier_small = prospect_xavier / "asr/xavier-espot-small-nocontext.json"
    xavier_base = prospect_xavier / "asr/xavier-espot-base-nocontext.json"
    if (
        not (prospect_xavier / "audio.wav").exists()
        or not xavier_small.exists()
        or not xavier_base.exists()
        or len(xavier_forms) != 70
        or len(xavier_queue) != 39
        or len(xavier_acoustic) != 39
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in xavier_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in xavier_queue)
        or "fora del recompte" not in xavier_report
        or "habitatge" not in xavier_report
        or "youtube.com/watch?v=MhGYlCSdtQ4" not in xavier_report
    ):
        errors.append("l'expedient Xavier Espot no conserva àudio, doble ASR, formes polítiques i cua separada")
    else:
        try:
            import json
            xavier_small_last = json.loads(xavier_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            xavier_base_last = json.loads(xavier_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if xavier_small_last < 2_400_000 or xavier_base_last < 2_400_000:
                errors.append("l'expedient Xavier Espot no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Xavier Espot invàlid")
    prospect_oscar = ROOT / "proveniencia/prospeccio/lead-yt-037-oscar-ribas"
    oscar_report = (prospect_oscar / "informe.md").read_text(encoding="utf-8") if (prospect_oscar / "informe.md").exists() else ""
    oscar_forms = read("proveniencia/prospeccio/lead-yt-037-oscar-ribas/formes.tsv") if (prospect_oscar / "formes.tsv").exists() else []
    oscar_queue = read("proveniencia/prospeccio/lead-yt-037-oscar-ribas/cua-audicio.tsv") if (prospect_oscar / "cua-audicio.tsv").exists() else []
    oscar_acoustic = read("proveniencia/prospeccio/lead-yt-037-oscar-ribas/analisi-acustica.tsv") if (prospect_oscar / "analisi-acustica.tsv").exists() else []
    oscar_small = prospect_oscar / "asr/oscar-ribas-small-nocontext.json"
    oscar_base = prospect_oscar / "asr/oscar-ribas-base-nocontext.json"
    if (
        not (prospect_oscar / "audio.wav").exists()
        or not oscar_small.exists()
        or not oscar_base.exists()
        or len(oscar_forms) != 71
        or len(oscar_queue) != 29
        or len(oscar_acoustic) != 29
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in oscar_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in oscar_queue)
        or "fora del recompte" not in oscar_report
        or "aiguat" not in oscar_report
        or "youtube.com/watch?v=9mXzxEA4Jlg" not in oscar_report
    ):
        errors.append("l'expedient Òscar Ribas no conserva àudio, doble ASR, formes històriques i cua separada")
    else:
        try:
            import json
            oscar_small_last = json.loads(oscar_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            oscar_base_last = json.loads(oscar_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if oscar_small_last < 1_000_000 or oscar_base_last < 1_000_000:
                errors.append("l'expedient Òscar Ribas no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Òscar Ribas invàlid")
    prospect_conxita = ROOT / "proveniencia/prospeccio/lead-yt-038-conxita-marsol"
    conxita_report = (prospect_conxita / "informe.md").read_text(encoding="utf-8") if (prospect_conxita / "informe.md").exists() else ""
    conxita_forms = read("proveniencia/prospeccio/lead-yt-038-conxita-marsol/formes.tsv") if (prospect_conxita / "formes.tsv").exists() else []
    conxita_queue = read("proveniencia/prospeccio/lead-yt-038-conxita-marsol/cua-audicio.tsv") if (prospect_conxita / "cua-audicio.tsv").exists() else []
    conxita_acoustic = read("proveniencia/prospeccio/lead-yt-038-conxita-marsol/analisi-acustica.tsv") if (prospect_conxita / "analisi-acustica.tsv").exists() else []
    conxita_small = prospect_conxita / "asr/conxita-marsol-small-nocontext.json"
    conxita_base = prospect_conxita / "asr/conxita-marsol-base-nocontext.json"
    if (
        not (prospect_conxita / "audio.wav").exists()
        or not conxita_small.exists()
        or not conxita_base.exists()
        or len(conxita_forms) != 68
        or len(conxita_queue) != 12
        or len(conxita_acoustic) != 12
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in conxita_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in conxita_queue)
        or "fora del recompte" not in conxita_report
        or "cònsol" not in conxita_report
        or "youtube.com/watch?v=Nd1cHcMh-ks" not in conxita_report
    ):
        errors.append("l'expedient Conxita Marsol no conserva àudio, doble ASR, formes institucionals i cua separada")
    else:
        try:
            import json
            conxita_small_last = json.loads(conxita_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            conxita_base_last = json.loads(conxita_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if conxita_small_last < 600_000 or conxita_base_last < 600_000:
                errors.append("l'expedient Conxita Marsol no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Conxita Marsol invàlid")
    prospect_marta = ROOT / "proveniencia/prospeccio/lead-yt-039-marta-roure"
    marta_report = (prospect_marta / "informe.md").read_text(encoding="utf-8") if (prospect_marta / "informe.md").exists() else ""
    marta_forms = read("proveniencia/prospeccio/lead-yt-039-marta-roure/formes.tsv") if (prospect_marta / "formes.tsv").exists() else []
    marta_queue = read("proveniencia/prospeccio/lead-yt-039-marta-roure/cua-audicio.tsv") if (prospect_marta / "cua-audicio.tsv").exists() else []
    marta_acoustic = read("proveniencia/prospeccio/lead-yt-039-marta-roure/analisi-acustica.tsv") if (prospect_marta / "analisi-acustica.tsv").exists() else []
    marta_small = prospect_marta / "asr/marta-roure-small-nocontext.json"
    marta_base = prospect_marta / "asr/marta-roure-base-nocontext.json"
    if (
        not (prospect_marta / "audio.wav").exists()
        or not marta_small.exists()
        or not marta_base.exists()
        or len(marta_forms) != 71
        or len(marta_queue) != 49
        or len(marta_acoustic) != 49
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in marta_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in marta_queue)
        or "fora del recompte" not in marta_report
        or "Eurovisió" not in marta_report
        or "youtube.com/watch?v=_mez8hd4Oxs" not in marta_report
    ):
        errors.append("l'expedient Marta Roure no conserva àudio, doble ASR, formes culturals i cua separada")
    else:
        try:
            import json
            marta_small_last = json.loads(marta_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            marta_base_last = json.loads(marta_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if marta_small_last < 1_500_000 or marta_base_last < 1_500_000:
                errors.append("l'expedient Marta Roure no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Marta Roure invàlid")
    prospect_guillem = ROOT / "proveniencia/prospeccio/lead-yt-040-guillem-forne"
    guillem_report = (prospect_guillem / "informe.md").read_text(encoding="utf-8") if (prospect_guillem / "informe.md").exists() else ""
    guillem_forms = read("proveniencia/prospeccio/lead-yt-040-guillem-forne/formes.tsv") if (prospect_guillem / "formes.tsv").exists() else []
    guillem_queue = read("proveniencia/prospeccio/lead-yt-040-guillem-forne/cua-audicio.tsv") if (prospect_guillem / "cua-audicio.tsv").exists() else []
    guillem_acoustic = read("proveniencia/prospeccio/lead-yt-040-guillem-forne/analisi-acustica.tsv") if (prospect_guillem / "analisi-acustica.tsv").exists() else []
    guillem_small = prospect_guillem / "asr/guillem-forne-small-nocontext.json"
    guillem_base = prospect_guillem / "asr/guillem-forne-base-nocontext.json"
    if (
        not (prospect_guillem / "audio.wav").exists()
        or not guillem_small.exists()
        or not guillem_base.exists()
        or len(guillem_forms) != 70
        or len(guillem_queue) != 49
        or len(guillem_acoustic) != 49
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in guillem_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in guillem_queue)
        or "fora del recompte" not in guillem_report
        or "Massana" not in guillem_report
        or "youtube.com/watch?v=I1QZRB8A5Y4" not in guillem_report
    ):
        errors.append("l'expedient Guillem Forné no conserva àudio, doble ASR, formes culturals i cua separada")
    else:
        try:
            import json
            guillem_small_last = json.loads(guillem_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            guillem_base_last = json.loads(guillem_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if guillem_small_last < 1_800_000 or guillem_base_last < 1_800_000:
                errors.append("l'expedient Guillem Forné no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Guillem Forné invàlid")
    prospect_areny = ROOT / "proveniencia/prospeccio/lead-yt-041-guillem-areny"
    areny_report = (prospect_areny / "informe.md").read_text(encoding="utf-8") if (prospect_areny / "informe.md").exists() else ""
    areny_forms = read("proveniencia/prospeccio/lead-yt-041-guillem-areny/formes.tsv") if (prospect_areny / "formes.tsv").exists() else []
    areny_queue = read("proveniencia/prospeccio/lead-yt-041-guillem-areny/cua-audicio.tsv") if (prospect_areny / "cua-audicio.tsv").exists() else []
    areny_acoustic = read("proveniencia/prospeccio/lead-yt-041-guillem-areny/analisi-acustica.tsv") if (prospect_areny / "analisi-acustica.tsv").exists() else []
    areny_small = prospect_areny / "asr/guillem-areny-small-nocontext.json"
    areny_base = prospect_areny / "asr/guillem-areny-base-nocontext.json"
    if (
        not (prospect_areny / "audio.wav").exists()
        or not areny_small.exists()
        or not areny_base.exists()
        or len(areny_forms) != 63
        or len(areny_queue) != 13
        or len(areny_acoustic) != 13
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in areny_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in areny_queue)
        or "fora del recompte" not in areny_report
        or "aiguat" not in areny_report
        or "youtube.com/watch?v=8gerOARXiYM" not in areny_report
    ):
        errors.append("l'expedient Guillem Areny no conserva àudio, doble ASR, formes històriques i cua separada")
    else:
        try:
            import json
            areny_small_last = json.loads(areny_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            areny_base_last = json.loads(areny_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if areny_small_last < 350_000 or areny_base_last < 350_000:
                errors.append("l'expedient Guillem Areny no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Guillem Areny invàlid")
    prospect_andreu_gonzalez = ROOT / "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez"
    andreu_gonzalez_report = (prospect_andreu_gonzalez / "informe.md").read_text(encoding="utf-8") if (prospect_andreu_gonzalez / "informe.md").exists() else ""
    andreu_gonzalez_forms = read("proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/formes.tsv") if (prospect_andreu_gonzalez / "formes.tsv").exists() else []
    andreu_gonzalez_queue = read("proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/cua-audicio.tsv") if (prospect_andreu_gonzalez / "cua-audicio.tsv").exists() else []
    andreu_gonzalez_acoustic = read("proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/analisi-acustica.tsv") if (prospect_andreu_gonzalez / "analisi-acustica.tsv").exists() else []
    andreu_gonzalez_small = prospect_andreu_gonzalez / "asr/andreu-gonzalez-small-nocontext.json"
    andreu_gonzalez_base = prospect_andreu_gonzalez / "asr/andreu-gonzalez-base-nocontext.json"
    if (
        not (prospect_andreu_gonzalez / "audio.wav").exists()
        or not andreu_gonzalez_small.exists()
        or not andreu_gonzalez_base.exists()
        or len(andreu_gonzalez_forms) != 56
        or len(andreu_gonzalez_queue) != 25
        or len(andreu_gonzalez_acoustic) != 25
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in andreu_gonzalez_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in andreu_gonzalez_queue)
        or "fora del recompte" not in andreu_gonzalez_report
        or "naturalesa" not in andreu_gonzalez_report
        or "youtube.com/watch?v=4dWGHdqBL8A" not in andreu_gonzalez_report
    ):
        errors.append("l'expedient Andreu González no conserva àudio, doble ASR, formes ambientals i cua separada")
    else:
        try:
            import json
            andreu_gonzalez_small_last = json.loads(andreu_gonzalez_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            andreu_gonzalez_base_last = json.loads(andreu_gonzalez_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if andreu_gonzalez_small_last < 1100000 or andreu_gonzalez_base_last < 1100000:
                errors.append("l'expedient Andreu González no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Andreu González invàlid")

    prospect_oriol_agorreta = ROOT / "proveniencia/prospeccio/lead-yt-043-oriol-agorreta"
    oriol_agorreta_report = (prospect_oriol_agorreta / "informe.md").read_text(encoding="utf-8") if (prospect_oriol_agorreta / "informe.md").exists() else ""
    oriol_agorreta_forms = read("proveniencia/prospeccio/lead-yt-043-oriol-agorreta/formes.tsv") if (prospect_oriol_agorreta / "formes.tsv").exists() else []
    oriol_agorreta_queue = read("proveniencia/prospeccio/lead-yt-043-oriol-agorreta/cua-audicio.tsv") if (prospect_oriol_agorreta / "cua-audicio.tsv").exists() else []
    oriol_agorreta_acoustic = read("proveniencia/prospeccio/lead-yt-043-oriol-agorreta/analisi-acustica.tsv") if (prospect_oriol_agorreta / "analisi-acustica.tsv").exists() else []
    oriol_agorreta_small = prospect_oriol_agorreta / "asr/oriol-agorreta-small-nocontext.json"
    oriol_agorreta_base = prospect_oriol_agorreta / "asr/oriol-agorreta-base-nocontext.json"
    if (
        not (prospect_oriol_agorreta / "audio.wav").exists()
        or not oriol_agorreta_small.exists()
        or not oriol_agorreta_base.exists()
        or len(oriol_agorreta_forms) != 55
        or len(oriol_agorreta_queue) != 23
        or len(oriol_agorreta_acoustic) != 23
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in oriol_agorreta_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in oriol_agorreta_queue)
        or "fora del recompte" not in oriol_agorreta_report
        or "joier" not in oriol_agorreta_report
        or "youtube.com/watch?v=G001CWkBezs" not in oriol_agorreta_report
    ):
        errors.append("l'expedient Oriol Agorreta no conserva àudio, doble ASR, formes culturals i cua separada")
    else:
        try:
            import json
            oriol_agorreta_small_last = json.loads(oriol_agorreta_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            oriol_agorreta_base_last = json.loads(oriol_agorreta_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if oriol_agorreta_small_last < 1200000 or oriol_agorreta_base_last < 1200000:
                errors.append("l'expedient Oriol Agorreta no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Oriol Agorreta invàlid")

    prospect_laura_casanovas = ROOT / "proveniencia/prospeccio/lead-yt-044-laura-casanovas"
    laura_casanovas_report = (prospect_laura_casanovas / "informe.md").read_text(encoding="utf-8") if (prospect_laura_casanovas / "informe.md").exists() else ""
    laura_casanovas_forms = read("proveniencia/prospeccio/lead-yt-044-laura-casanovas/formes.tsv") if (prospect_laura_casanovas / "formes.tsv").exists() else []
    laura_casanovas_queue = read("proveniencia/prospeccio/lead-yt-044-laura-casanovas/cua-audicio.tsv") if (prospect_laura_casanovas / "cua-audicio.tsv").exists() else []
    laura_casanovas_acoustic = read("proveniencia/prospeccio/lead-yt-044-laura-casanovas/analisi-acustica.tsv") if (prospect_laura_casanovas / "analisi-acustica.tsv").exists() else []
    laura_casanovas_small = prospect_laura_casanovas / "asr/laura-casanovas-small-nocontext.json"
    laura_casanovas_base = prospect_laura_casanovas / "asr/laura-casanovas-base-nocontext.json"
    if (
        not (prospect_laura_casanovas / "audio.wav").exists()
        or not laura_casanovas_small.exists()
        or not laura_casanovas_base.exists()
        or len(laura_casanovas_forms) != 55
        or len(laura_casanovas_queue) != 28
        or len(laura_casanovas_acoustic) != 28
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in laura_casanovas_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in laura_casanovas_queue)
        or "fora del recompte" not in laura_casanovas_report
        or "escriptora" not in laura_casanovas_report
        or "youtube.com/watch?v=YVOqMgemCbY" not in laura_casanovas_report
    ):
        errors.append("l'expedient Laura Casanovas no conserva àudio, doble ASR, formes culturals i cua separada")
    else:
        try:
            import json
            laura_casanovas_small_last = json.loads(laura_casanovas_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            laura_casanovas_base_last = json.loads(laura_casanovas_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if laura_casanovas_small_last < 1400000 or laura_casanovas_base_last < 1400000:
                errors.append("l'expedient Laura Casanovas no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Laura Casanovas invàlid")

    prospect_arnau_rius = ROOT / "proveniencia/prospeccio/lead-yt-045-arnau-rius"
    arnau_rius_report = (prospect_arnau_rius / "informe.md").read_text(encoding="utf-8") if (prospect_arnau_rius / "informe.md").exists() else ""
    arnau_rius_forms = read("proveniencia/prospeccio/lead-yt-045-arnau-rius/formes.tsv") if (prospect_arnau_rius / "formes.tsv").exists() else []
    arnau_rius_queue = read("proveniencia/prospeccio/lead-yt-045-arnau-rius/cua-audicio.tsv") if (prospect_arnau_rius / "cua-audicio.tsv").exists() else []
    arnau_rius_acoustic = read("proveniencia/prospeccio/lead-yt-045-arnau-rius/analisi-acustica.tsv") if (prospect_arnau_rius / "analisi-acustica.tsv").exists() else []
    arnau_rius_small = prospect_arnau_rius / "asr/arnau-rius-small-nocontext.json"
    arnau_rius_base = prospect_arnau_rius / "asr/arnau-rius-base-nocontext.json"
    if (
        not (prospect_arnau_rius / "audio.wav").exists()
        or not arnau_rius_small.exists()
        or not arnau_rius_base.exists()
        or len(arnau_rius_forms) != 53
        or len(arnau_rius_queue) != 23
        or len(arnau_rius_acoustic) != 23
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in arnau_rius_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in arnau_rius_queue)
        or "fora del recompte" not in arnau_rius_report
        or "arquitectura" not in arnau_rius_report
        or "youtube.com/watch?v=b5aQmIfpqR8" not in arnau_rius_report
    ):
        errors.append("l'expedient Arnau Rius no conserva àudio, doble ASR, formes arquitectòniques i cua separada")
    else:
        try:
            import json
            arnau_rius_small_last = json.loads(arnau_rius_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            arnau_rius_base_last = json.loads(arnau_rius_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if arnau_rius_small_last < 1100000 or arnau_rius_base_last < 1100000:
                errors.append("l'expedient Arnau Rius no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Arnau Rius invàlid")

    prospect_alberto_villagrasa = ROOT / "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa"
    alberto_villagrasa_report = (prospect_alberto_villagrasa / "informe.md").read_text(encoding="utf-8") if (prospect_alberto_villagrasa / "informe.md").exists() else ""
    alberto_villagrasa_forms = read("proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/formes.tsv") if (prospect_alberto_villagrasa / "formes.tsv").exists() else []
    alberto_villagrasa_queue = read("proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/cua-audicio.tsv") if (prospect_alberto_villagrasa / "cua-audicio.tsv").exists() else []
    alberto_villagrasa_acoustic = read("proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/analisi-acustica.tsv") if (prospect_alberto_villagrasa / "analisi-acustica.tsv").exists() else []
    alberto_villagrasa_small = prospect_alberto_villagrasa / "asr/alberto-villagrasa-small-nocontext.json"
    alberto_villagrasa_base = prospect_alberto_villagrasa / "asr/alberto-villagrasa-base-nocontext.json"
    if (
        not (prospect_alberto_villagrasa / "audio.wav").exists()
        or not alberto_villagrasa_small.exists()
        or not alberto_villagrasa_base.exists()
        or len(alberto_villagrasa_forms) != 52
        or len(alberto_villagrasa_queue) != 21
        or len(alberto_villagrasa_acoustic) != 21
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in alberto_villagrasa_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in alberto_villagrasa_queue)
        or "fora del recompte" not in alberto_villagrasa_report
        or "ciberseguretat" not in alberto_villagrasa_report
        or "youtube.com/watch?v=82SaEquzEy4" not in alberto_villagrasa_report
    ):
        errors.append("l'expedient Alberto Villagrasa no conserva àudio, doble ASR, formes tecnològiques i cua separada")
    else:
        try:
            import json
            alberto_villagrasa_small_last = json.loads(alberto_villagrasa_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            alberto_villagrasa_base_last = json.loads(alberto_villagrasa_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if alberto_villagrasa_small_last < 1100000 or alberto_villagrasa_base_last < 1100000:
                errors.append("l'expedient Alberto Villagrasa no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Alberto Villagrasa invàlid")

    prospect_katia_ustina = ROOT / "proveniencia/prospeccio/lead-yt-047-katia-ustina"
    katia_ustina_report = (prospect_katia_ustina / "informe.md").read_text(encoding="utf-8") if (prospect_katia_ustina / "informe.md").exists() else ""
    katia_ustina_forms = read("proveniencia/prospeccio/lead-yt-047-katia-ustina/formes.tsv") if (prospect_katia_ustina / "formes.tsv").exists() else []
    katia_ustina_queue = read("proveniencia/prospeccio/lead-yt-047-katia-ustina/cua-audicio.tsv") if (prospect_katia_ustina / "cua-audicio.tsv").exists() else []
    katia_ustina_acoustic = read("proveniencia/prospeccio/lead-yt-047-katia-ustina/analisi-acustica.tsv") if (prospect_katia_ustina / "analisi-acustica.tsv").exists() else []
    katia_ustina_small = prospect_katia_ustina / "asr/katia-ustina-small-nocontext.json"
    katia_ustina_base = prospect_katia_ustina / "asr/katia-ustina-base-nocontext.json"
    if (
        not (prospect_katia_ustina / "audio.wav").exists()
        or not katia_ustina_small.exists()
        or not katia_ustina_base.exists()
        or len(katia_ustina_forms) != 51
        or len(katia_ustina_queue) != 12
        or len(katia_ustina_acoustic) != 12
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in katia_ustina_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in katia_ustina_queue)
        or "fora del recompte" not in katia_ustina_report
        or "diners" not in katia_ustina_report
        or "youtube.com/watch?v=KexXOfGSjVo" not in katia_ustina_report
    ):
        errors.append("l'expedient Katia Ustina no conserva àudio, doble ASR, formes econòmiques i cua separada")
    else:
        try:
            import json
            katia_ustina_small_last = json.loads(katia_ustina_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            katia_ustina_base_last = json.loads(katia_ustina_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if katia_ustina_small_last < 800000 or katia_ustina_base_last < 800000:
                errors.append("l'expedient Katia Ustina no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Katia Ustina invàlid")

    prospect_ander_mirambell = ROOT / "proveniencia/prospeccio/lead-yt-048-ander-mirambell"
    ander_mirambell_report = (prospect_ander_mirambell / "informe.md").read_text(encoding="utf-8") if (prospect_ander_mirambell / "informe.md").exists() else ""
    ander_mirambell_forms = read("proveniencia/prospeccio/lead-yt-048-ander-mirambell/formes.tsv") if (prospect_ander_mirambell / "formes.tsv").exists() else []
    ander_mirambell_queue = read("proveniencia/prospeccio/lead-yt-048-ander-mirambell/cua-audicio.tsv") if (prospect_ander_mirambell / "cua-audicio.tsv").exists() else []
    ander_mirambell_acoustic = read("proveniencia/prospeccio/lead-yt-048-ander-mirambell/analisi-acustica.tsv") if (prospect_ander_mirambell / "analisi-acustica.tsv").exists() else []
    ander_mirambell_small = prospect_ander_mirambell / "asr/ander-mirambell-small-nocontext.json"
    ander_mirambell_base = prospect_ander_mirambell / "asr/ander-mirambell-base-nocontext.json"
    if (
        not (prospect_ander_mirambell / "audio.wav").exists()
        or not ander_mirambell_small.exists()
        or not ander_mirambell_base.exists()
        or len(ander_mirambell_forms) != 53
        or len(ander_mirambell_queue) != 27
        or len(ander_mirambell_acoustic) != 27
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in ander_mirambell_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in ander_mirambell_queue)
        or "fora del recompte" not in ander_mirambell_report
        or "medalla" not in ander_mirambell_report
        or "youtube.com/watch?v=I7Nv4edlBOI" not in ander_mirambell_report
    ):
        errors.append("l'expedient Ander Mirambell no conserva àudio, doble ASR, formes esportives i cua separada")
    else:
        try:
            import json
            ander_mirambell_small_last = json.loads(ander_mirambell_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            ander_mirambell_base_last = json.loads(ander_mirambell_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if ander_mirambell_small_last < 1700000 or ander_mirambell_base_last < 1700000:
                errors.append("l'expedient Ander Mirambell no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Ander Mirambell invàlid")

    prospect_joan_piquet = ROOT / "proveniencia/prospeccio/lead-yt-049-joan-piquet"
    joan_piquet_report = (prospect_joan_piquet / "informe.md").read_text(encoding="utf-8") if (prospect_joan_piquet / "informe.md").exists() else ""
    joan_piquet_forms = read("proveniencia/prospeccio/lead-yt-049-joan-piquet/formes.tsv") if (prospect_joan_piquet / "formes.tsv").exists() else []
    joan_piquet_queue = read("proveniencia/prospeccio/lead-yt-049-joan-piquet/cua-audicio.tsv") if (prospect_joan_piquet / "cua-audicio.tsv").exists() else []
    joan_piquet_acoustic = read("proveniencia/prospeccio/lead-yt-049-joan-piquet/analisi-acustica.tsv") if (prospect_joan_piquet / "analisi-acustica.tsv").exists() else []
    joan_piquet_small = prospect_joan_piquet / "asr/joan-piquet-small-nocontext.json"
    joan_piquet_base = prospect_joan_piquet / "asr/joan-piquet-base-nocontext.json"
    if (
        not (prospect_joan_piquet / "audio.wav").exists()
        or not joan_piquet_small.exists()
        or not joan_piquet_base.exists()
        or len(joan_piquet_forms) != 52
        or len(joan_piquet_queue) != 27
        or len(joan_piquet_acoustic) != 27
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in joan_piquet_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in joan_piquet_queue)
        or "fora del recompte" not in joan_piquet_report
        or "reiki" not in joan_piquet_report
        or "youtube.com/watch?v=A8IQKfxQxtg" not in joan_piquet_report
    ):
        errors.append("l'expedient Joan Piquet no conserva àudio, doble ASR, formes salut i cua separada")
    else:
        try:
            import json
            joan_piquet_small_last = json.loads(joan_piquet_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            joan_piquet_base_last = json.loads(joan_piquet_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if joan_piquet_small_last < 1400000 or joan_piquet_base_last < 1400000:
                errors.append("l'expedient Joan Piquet no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Joan Piquet invàlid")

    prospect_pau_chica = ROOT / "proveniencia/prospeccio/lead-yt-050-pau-chica"
    pau_chica_report = (prospect_pau_chica / "informe.md").read_text(encoding="utf-8") if (prospect_pau_chica / "informe.md").exists() else ""
    pau_chica_forms = read("proveniencia/prospeccio/lead-yt-050-pau-chica/formes.tsv") if (prospect_pau_chica / "formes.tsv").exists() else []
    pau_chica_queue = read("proveniencia/prospeccio/lead-yt-050-pau-chica/cua-audicio.tsv") if (prospect_pau_chica / "cua-audicio.tsv").exists() else []
    pau_chica_acoustic = read("proveniencia/prospeccio/lead-yt-050-pau-chica/analisi-acustica.tsv") if (prospect_pau_chica / "analisi-acustica.tsv").exists() else []
    pau_chica_small = prospect_pau_chica / "asr/pau-chica-small-nocontext.json"
    pau_chica_base = prospect_pau_chica / "asr/pau-chica-base-nocontext.json"
    if (
        not (prospect_pau_chica / "audio.wav").exists()
        or not pau_chica_small.exists()
        or not pau_chica_base.exists()
        or len(pau_chica_forms) != 53
        or len(pau_chica_queue) != 36
        or len(pau_chica_acoustic) != 36
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in pau_chica_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in pau_chica_queue)
        or "fora del recompte" not in pau_chica_report
        or "historiador" not in pau_chica_report
        or "youtube.com/watch?v=SBenbl0lHpE" not in pau_chica_report
    ):
        errors.append("l'expedient Pau Chica no conserva àudio, doble ASR, formes històriques i cua separada")
    else:
        try:
            import json
            pau_chica_small_last = json.loads(pau_chica_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            pau_chica_base_last = json.loads(pau_chica_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if pau_chica_small_last < 1800000 or pau_chica_base_last < 1800000:
                errors.append("l'expedient Pau Chica no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Pau Chica invàlid")

    prospect_albert_vilaro = ROOT / "proveniencia/prospeccio/lead-yt-051-albert-vilaro"
    albert_vilaro_report = (prospect_albert_vilaro / "informe.md").read_text(encoding="utf-8") if (prospect_albert_vilaro / "informe.md").exists() else ""
    albert_vilaro_forms = read("proveniencia/prospeccio/lead-yt-051-albert-vilaro/formes.tsv") if (prospect_albert_vilaro / "formes.tsv").exists() else []
    albert_vilaro_queue = read("proveniencia/prospeccio/lead-yt-051-albert-vilaro/cua-audicio.tsv") if (prospect_albert_vilaro / "cua-audicio.tsv").exists() else []
    albert_vilaro_acoustic = read("proveniencia/prospeccio/lead-yt-051-albert-vilaro/analisi-acustica.tsv") if (prospect_albert_vilaro / "analisi-acustica.tsv").exists() else []
    albert_vilaro_small = prospect_albert_vilaro / "asr/albert-vilaro-small-nocontext.json"
    albert_vilaro_base = prospect_albert_vilaro / "asr/albert-vilaro-base-nocontext.json"
    if (
        not (prospect_albert_vilaro / "audio.wav").exists()
        or not albert_vilaro_small.exists()
        or not albert_vilaro_base.exists()
        or len(albert_vilaro_forms) != 56
        or len(albert_vilaro_queue) != 17
        or len(albert_vilaro_acoustic) != 17
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in albert_vilaro_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in albert_vilaro_queue)
        or "fora del recompte" not in albert_vilaro_report
        or "economia" not in albert_vilaro_report
        or "youtube.com/watch?v=2d_HBO8K29g" not in albert_vilaro_report
    ):
        errors.append("l'expedient Albert Vilaró no conserva àudio, doble ASR, formes econòmiques i cua separada")
    else:
        try:
            import json
            albert_vilaro_small_last = json.loads(albert_vilaro_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            albert_vilaro_base_last = json.loads(albert_vilaro_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if albert_vilaro_small_last < 850000 or albert_vilaro_base_last < 850000:
                errors.append("l'expedient Albert Vilaró no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Albert Vilaró invàlid")

    prospect_valenti_closa = ROOT / "proveniencia/prospeccio/lead-yt-052-valenti-closa"
    valenti_closa_report = (prospect_valenti_closa / "informe.md").read_text(encoding="utf-8") if (prospect_valenti_closa / "informe.md").exists() else ""
    valenti_closa_forms = read("proveniencia/prospeccio/lead-yt-052-valenti-closa/formes.tsv") if (prospect_valenti_closa / "formes.tsv").exists() else []
    valenti_closa_queue = read("proveniencia/prospeccio/lead-yt-052-valenti-closa/cua-audicio.tsv") if (prospect_valenti_closa / "cua-audicio.tsv").exists() else []
    valenti_closa_acoustic = read("proveniencia/prospeccio/lead-yt-052-valenti-closa/analisi-acustica.tsv") if (prospect_valenti_closa / "analisi-acustica.tsv").exists() else []
    valenti_closa_small = prospect_valenti_closa / "asr/valenti-closa-small-nocontext.json"
    valenti_closa_base = prospect_valenti_closa / "asr/valenti-closa-base-nocontext.json"
    if (
        not (prospect_valenti_closa / "audio.wav").exists()
        or not valenti_closa_small.exists()
        or not valenti_closa_base.exists()
        or len(valenti_closa_forms) != 49
        or len(valenti_closa_queue) != 26
        or len(valenti_closa_acoustic) != 26
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in valenti_closa_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in valenti_closa_queue)
        or "fora del recompte" not in valenti_closa_report
        or "Conseller" not in valenti_closa_report
        or "youtube.com/watch?v=VndqXBVK2tw" not in valenti_closa_report
    ):
        errors.append("l'expedient Valentí Closa no conserva àudio, doble ASR, formes institucionals i cua separada")
    else:
        try:
            import json
            valenti_closa_small_last = json.loads(valenti_closa_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            valenti_closa_base_last = json.loads(valenti_closa_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if valenti_closa_small_last < 2200000 or valenti_closa_base_last < 2200000:
                errors.append("l'expedient Valentí Closa no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Valentí Closa invàlid")

    prospect_sonia_andorrita = ROOT / "proveniencia/prospeccio/lead-yt-053-sonia-andorrita"
    sonia_andorrita_report = (prospect_sonia_andorrita / "informe.md").read_text(encoding="utf-8") if (prospect_sonia_andorrita / "informe.md").exists() else ""
    sonia_andorrita_forms = read("proveniencia/prospeccio/lead-yt-053-sonia-andorrita/formes.tsv") if (prospect_sonia_andorrita / "formes.tsv").exists() else []
    sonia_andorrita_queue = read("proveniencia/prospeccio/lead-yt-053-sonia-andorrita/cua-audicio.tsv") if (prospect_sonia_andorrita / "cua-audicio.tsv").exists() else []
    sonia_andorrita_acoustic = read("proveniencia/prospeccio/lead-yt-053-sonia-andorrita/analisi-acustica.tsv") if (prospect_sonia_andorrita / "analisi-acustica.tsv").exists() else []
    sonia_andorrita_small = prospect_sonia_andorrita / "asr/sonia-andorrita-small-nocontext.json"
    sonia_andorrita_base = prospect_sonia_andorrita / "asr/sonia-andorrita-base-nocontext.json"
    if (
        not (prospect_sonia_andorrita / "audio.wav").exists()
        or not sonia_andorrita_small.exists()
        or not sonia_andorrita_base.exists()
        or len(sonia_andorrita_forms) != 52
        or len(sonia_andorrita_queue) != 24
        or len(sonia_andorrita_acoustic) != 24
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in sonia_andorrita_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in sonia_andorrita_queue)
        or "fora del recompte" not in sonia_andorrita_report
        or "Andorrita" not in sonia_andorrita_report
        or "youtube.com/watch?v=hW33qita_Vk" not in sonia_andorrita_report
    ):
        errors.append("l'expedient Sonia no conserva àudio, doble ASR, formes socials i cua separada")
    else:
        try:
            import json
            sonia_andorrita_small_last = json.loads(sonia_andorrita_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            sonia_andorrita_base_last = json.loads(sonia_andorrita_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if sonia_andorrita_small_last < 900000 or sonia_andorrita_base_last < 900000:
                errors.append("l'expedient Sonia no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Sonia invàlid")

    prospect_francesc_solana = ROOT / "proveniencia/prospeccio/lead-yt-054-francesc-solana"
    francesc_solana_report = (prospect_francesc_solana / "informe.md").read_text(encoding="utf-8") if (prospect_francesc_solana / "informe.md").exists() else ""
    francesc_solana_forms = read("proveniencia/prospeccio/lead-yt-054-francesc-solana/formes.tsv") if (prospect_francesc_solana / "formes.tsv").exists() else []
    francesc_solana_queue = read("proveniencia/prospeccio/lead-yt-054-francesc-solana/cua-audicio.tsv") if (prospect_francesc_solana / "cua-audicio.tsv").exists() else []
    francesc_solana_acoustic = read("proveniencia/prospeccio/lead-yt-054-francesc-solana/analisi-acustica.tsv") if (prospect_francesc_solana / "analisi-acustica.tsv").exists() else []
    francesc_solana_small = prospect_francesc_solana / "asr/francesc-solana-small-nocontext.json"
    francesc_solana_base = prospect_francesc_solana / "asr/francesc-solana-base-nocontext.json"
    if (
        not (prospect_francesc_solana / "audio.wav").exists()
        or not francesc_solana_small.exists()
        or not francesc_solana_base.exists()
        or len(francesc_solana_forms) != 52
        or len(francesc_solana_queue) != 24
        or len(francesc_solana_acoustic) != 24
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in francesc_solana_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in francesc_solana_queue)
        or "fora del recompte" not in francesc_solana_report
        or "Esportiu" not in francesc_solana_report
        or "youtube.com/watch?v=a9FcTn5yjZ0" not in francesc_solana_report
    ):
        errors.append("l'expedient Francesc Solana no conserva àudio, doble ASR, formes esportives i cua separada")
    else:
        try:
            import json
            francesc_solana_small_last = json.loads(francesc_solana_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            francesc_solana_base_last = json.loads(francesc_solana_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if francesc_solana_small_last < 1700000 or francesc_solana_base_last < 1700000:
                errors.append("l'expedient Francesc Solana no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Francesc Solana invàlid")

    prospect_enric_flix = ROOT / "proveniencia/prospeccio/lead-yt-055-enric-flix"
    enric_flix_report = (prospect_enric_flix / "informe.md").read_text(encoding="utf-8") if (prospect_enric_flix / "informe.md").exists() else ""
    enric_flix_forms = read("proveniencia/prospeccio/lead-yt-055-enric-flix/formes.tsv") if (prospect_enric_flix / "formes.tsv").exists() else []
    enric_flix_queue = read("proveniencia/prospeccio/lead-yt-055-enric-flix/cua-audicio.tsv") if (prospect_enric_flix / "cua-audicio.tsv").exists() else []
    enric_flix_acoustic = read("proveniencia/prospeccio/lead-yt-055-enric-flix/analisi-acustica.tsv") if (prospect_enric_flix / "analisi-acustica.tsv").exists() else []
    enric_flix_small = prospect_enric_flix / "asr/enric-flix-small-nocontext.json"
    enric_flix_base = prospect_enric_flix / "asr/enric-flix-base-nocontext.json"
    if (
        not (prospect_enric_flix / "audio.wav").exists()
        or not enric_flix_small.exists()
        or not enric_flix_base.exists()
        or len(enric_flix_forms) != 52
        or len(enric_flix_queue) != 28
        or len(enric_flix_acoustic) != 28
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in enric_flix_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in enric_flix_queue)
        or "fora del recompte" not in enric_flix_report
        or "empresa" not in enric_flix_report
        or "youtube.com/watch?v=ddITYkCxaxo" not in enric_flix_report
    ):
        errors.append("l'expedient Enric Flix no conserva àudio, doble ASR, formes empresarials i cua separada")
    else:
        try:
            import json
            enric_flix_small_last = json.loads(enric_flix_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            enric_flix_base_last = json.loads(enric_flix_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if enric_flix_small_last < 2350000 or enric_flix_base_last < 2350000:
                errors.append("l'expedient Enric Flix no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Enric Flix invàlid")

    prospect_arnau_fortuny = ROOT / "proveniencia/prospeccio/lead-yt-056-arnau-fortuny"
    arnau_fortuny_report = (prospect_arnau_fortuny / "informe.md").read_text(encoding="utf-8") if (prospect_arnau_fortuny / "informe.md").exists() else ""
    arnau_fortuny_forms = read("proveniencia/prospeccio/lead-yt-056-arnau-fortuny/formes.tsv") if (prospect_arnau_fortuny / "formes.tsv").exists() else []
    arnau_fortuny_queue = read("proveniencia/prospeccio/lead-yt-056-arnau-fortuny/cua-audicio.tsv") if (prospect_arnau_fortuny / "cua-audicio.tsv").exists() else []
    arnau_fortuny_acoustic = read("proveniencia/prospeccio/lead-yt-056-arnau-fortuny/analisi-acustica.tsv") if (prospect_arnau_fortuny / "analisi-acustica.tsv").exists() else []
    arnau_fortuny_small = prospect_arnau_fortuny / "asr/arnau-fortuny-small-nocontext.json"
    arnau_fortuny_base = prospect_arnau_fortuny / "asr/arnau-fortuny-base-nocontext.json"
    if (
        not (prospect_arnau_fortuny / "audio.wav").exists()
        or not arnau_fortuny_small.exists()
        or not arnau_fortuny_base.exists()
        or len(arnau_fortuny_forms) != 52
        or len(arnau_fortuny_queue) != 28
        or len(arnau_fortuny_acoustic) != 28
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in arnau_fortuny_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in arnau_fortuny_queue)
        or "fora del recompte" not in arnau_fortuny_report
        or "Arnau Fortuny" not in arnau_fortuny_report
        or "youtube.com/watch?v=1yJPzRkvyXw" not in arnau_fortuny_report
    ):
        errors.append("l'expedient Arnau Fortuny no conserva àudio, doble ASR, formes emprenedoria i cua separada")
    else:
        try:
            import json
            arnau_fortuny_small_last = json.loads(arnau_fortuny_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            arnau_fortuny_base_last = json.loads(arnau_fortuny_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if arnau_fortuny_small_last < 1550000 or arnau_fortuny_base_last < 1550000:
                errors.append("l'expedient Arnau Fortuny no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Arnau Fortuny invàlid")

    prospect_gabriel_lezkano = ROOT / "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano"
    gabriel_lezkano_report = (prospect_gabriel_lezkano / "informe.md").read_text(encoding="utf-8") if (prospect_gabriel_lezkano / "informe.md").exists() else ""
    gabriel_lezkano_forms = read("proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/formes.tsv") if (prospect_gabriel_lezkano / "formes.tsv").exists() else []
    gabriel_lezkano_queue = read("proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/cua-audicio.tsv") if (prospect_gabriel_lezkano / "cua-audicio.tsv").exists() else []
    gabriel_lezkano_acoustic = read("proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/analisi-acustica.tsv") if (prospect_gabriel_lezkano / "analisi-acustica.tsv").exists() else []
    gabriel_lezkano_small = prospect_gabriel_lezkano / "asr/gabriel-lezkano-small-nocontext.json"
    gabriel_lezkano_base = prospect_gabriel_lezkano / "asr/gabriel-lezkano-base-nocontext.json"
    if (
        not (prospect_gabriel_lezkano / "audio.wav").exists()
        or not gabriel_lezkano_small.exists()
        or not gabriel_lezkano_base.exists()
        or len(gabriel_lezkano_forms) != 52
        or len(gabriel_lezkano_queue) != 25
        or len(gabriel_lezkano_acoustic) != 25
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in gabriel_lezkano_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in gabriel_lezkano_queue)
        or "fora del recompte" not in gabriel_lezkano_report
        or "músic" not in gabriel_lezkano_report
        or "youtube.com/watch?v=gqr2NK_dWCk8" not in gabriel_lezkano_report
    ):
        errors.append("l'expedient Gabriel Lezkano no conserva àudio, doble ASR, formes culturals i cua separada")
    else:
        try:
            import json
            gabriel_lezkano_small_last = json.loads(gabriel_lezkano_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            gabriel_lezkano_base_last = json.loads(gabriel_lezkano_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if gabriel_lezkano_small_last < 1130000 or gabriel_lezkano_base_last < 1130000:
                errors.append("l'expedient Gabriel Lezkano no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Gabriel Lezkano invàlid")

    prospect_nuria_pablos = ROOT / "proveniencia/prospeccio/lead-yt-058-nuria-pablos"
    nuria_pablos_report = (prospect_nuria_pablos / "informe.md").read_text(encoding="utf-8") if (prospect_nuria_pablos / "informe.md").exists() else ""
    nuria_pablos_forms = read("proveniencia/prospeccio/lead-yt-058-nuria-pablos/formes.tsv") if (prospect_nuria_pablos / "formes.tsv").exists() else []
    nuria_pablos_queue = read("proveniencia/prospeccio/lead-yt-058-nuria-pablos/cua-audicio.tsv") if (prospect_nuria_pablos / "cua-audicio.tsv").exists() else []
    nuria_pablos_acoustic = read("proveniencia/prospeccio/lead-yt-058-nuria-pablos/analisi-acustica.tsv") if (prospect_nuria_pablos / "analisi-acustica.tsv").exists() else []
    nuria_pablos_small = prospect_nuria_pablos / "asr/nuria-pablos-small-nocontext.json"
    nuria_pablos_base = prospect_nuria_pablos / "asr/nuria-pablos-base-nocontext.json"
    if (
        not (prospect_nuria_pablos / "audio.wav").exists()
        or not nuria_pablos_small.exists()
        or not nuria_pablos_base.exists()
        or len(nuria_pablos_forms) != 52
        or len(nuria_pablos_queue) != 31
        or len(nuria_pablos_acoustic) != 31
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in nuria_pablos_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in nuria_pablos_queue)
        or "fora del recompte" not in nuria_pablos_report
        or "Celiaquía" not in nuria_pablos_report
        or "youtube.com/watch?v=tcTwUEJjKz8" not in nuria_pablos_report
    ):
        errors.append("l'expedient Núria Pablos no conserva àudio, doble ASR, formes salut i cua separada")
    else:
        try:
            import json
            nuria_pablos_small_last = json.loads(nuria_pablos_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            nuria_pablos_base_last = json.loads(nuria_pablos_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if nuria_pablos_small_last < 1380000 or nuria_pablos_base_last < 1380000:
                errors.append("l'expedient Núria Pablos no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Núria Pablos invàlid")

    prospect_ramon = ROOT / "proveniencia/prospeccio/lead-rtva-031-ramon-rossell"
    ramon_report = (prospect_ramon / "informe.md").read_text(encoding="utf-8") if (prospect_ramon / "informe.md").exists() else ""
    ramon_forms = read("proveniencia/prospeccio/lead-rtva-031-ramon-rossell/formes.tsv") if (prospect_ramon / "formes.tsv").exists() else []
    ramon_queue = read("proveniencia/prospeccio/lead-rtva-031-ramon-rossell/cua-audicio.tsv") if (prospect_ramon / "cua-audicio.tsv").exists() else []
    ramon_acoustic = read("proveniencia/prospeccio/lead-rtva-031-ramon-rossell/analisi-acustica.tsv") if (prospect_ramon / "analisi-acustica.tsv").exists() else []
    ramon_small = prospect_ramon / "asr/ramon-rossell-small-nocontext.json"
    ramon_base = prospect_ramon / "asr/ramon-rossell-base-nocontext.json"
    if (
        not (prospect_ramon / "audio.wav").exists()
        or not ramon_small.exists()
        or not ramon_base.exists()
        or len(ramon_forms) != 86
        or len(ramon_queue) != 47
        or len(ramon_acoustic) != 47
        or any(not row.get("estat", "").startswith("descriptor instrumental") for row in ramon_acoustic)
        or any(row.get("estat_audicio") != "pendent" for row in ramon_queue)
        or "fora del recompte" not in ramon_report
        or "església" not in ramon_report
        or "mossen-ramon-rossell-080120249" not in ramon_report
    ):
        errors.append("l'expedient Mossèn Ramon Rossell no conserva àudio, doble ASR, formes religioses i cua separada")
    else:
        try:
            import json
            ramon_small_last = json.loads(ramon_small.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            ramon_base_last = json.loads(ramon_base.read_text(encoding="utf-8"))["transcription"][-1]["offsets"]["to"]
            if ramon_small_last < 3_300_000 or ramon_base_last < 3_300_000:
                errors.append("l'expedient Mossèn Ramon Rossell no cobreix tota la durada de l'àudio")
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            errors.append("JSON de l'expedient Mossèn Ramon Rossell invàlid")
    prospect_graph_nodes = read("grafo/nodes-formes-prospeccio.tsv") if (ROOT / "grafo/nodes-formes-prospeccio.tsv").exists() else []
    prospect_graph_edges = read("grafo/arestes-formes-prospeccio.tsv") if (ROOT / "grafo/arestes-formes-prospeccio.tsv").exists() else []
    prospect_graph_matrix = read("grafo/matriu-formes-prospeccio.tsv") if (ROOT / "grafo/matriu-formes-prospeccio.tsv").exists() else []
    prospect_graph_readme = (ROOT / "grafo/README-formes-prospeccio.md").read_text(encoding="utf-8") if (ROOT / "grafo/README-formes-prospeccio.md").exists() else ""
    if (
        len(prospect_graph_nodes) != 1352
        or len(prospect_graph_edges) != 1369
        or len(prospect_graph_matrix) != 19133
        or len({row.get("candidat") for row in prospect_graph_nodes}) != 53
        or any(not row.get("candidat", "").startswith("lead-") for row in prospect_graph_nodes)
        or "nodes-formes-completa.tsv" not in prospect_graph_readme
        or "no enllacen" not in prospect_graph_readme
    ):
        errors.append("graf de prospecció nova inconsistent o connectat amb el cànon")
    for new_lead, nick in (("lead-rtva-059-carles-ensenyat", "carles-ensenyat"), ("lead-rtva-060-xavier-espot-actual", "xavier-espot-actual"), ("lead-rtva-061-antoni-morell", "antoni-morell")):
        folder = PROV / "prospeccio" / new_lead
        required = [folder / x for x in ("source-page.html", "legal-page.html", "terms.md", "source-original.mp4", "audio.wav", "source.info.json", "formes.tsv", "cua-audicio.tsv", "informe.md", f"asr/{nick}-small-nocontext.json", f"asr/{nick}-base-nocontext.json")]
        if any(not path.exists() for path in required):
            errors.append(f"expedient nou {new_lead} incomplet")
    prospect_player = (PROV / "auditoria-prospeccio-nova.html").read_text(encoding="utf-8") if (PROV / "auditoria-prospeccio-nova.html").exists() else ""
    if (
        '<title>Audició — prospecció nova del corpus de parla andorrana</title>' not in prospect_player
        or '<meta name="prospect-items" content="1650">' not in prospect_player
        or prospect_player.count('"id":') != 1650
        or any(lead not in prospect_player for lead in (
            "lead-rtva-009-isidre-bartumeu",
            "lead-rtva-010-lurdes-riba",
            "lead-rtva-011-josep-dalleres",
            "lead-rtva-012-marc-forne",
            "lead-rtva-013-pere-vilanova",
            "lead-rtva-014-joan-burgues",
            "lead-rtva-015-isidre-baro",
            "lead-rtva-016-josep-areny",
            "lead-rtva-017-simo-duro",
            "lead-rtva-018-ricard-fiter",
            "lead-rtva-019-lisa-cruz",
            "lead-rtva-020-monica-bonell",
            "lead-rtva-021-bonaventura-riberaygua",
            "lead-rtva-022-josep-marsal",
            "lead-rtva-023-josep-maria-cases",
            "lead-rtva-024-denisa-font",
            "lead-rtva-025-albert-gelabert",
            "lead-rtva-026-rosa-maria-mandico",
            "lead-rtva-027-jordi-guillamet",
            "lead-rtva-028-pere-besoli",
            "lead-rtva-029-angelina-mas",
            "lead-rtva-030-casimir-arajol",
            "lead-rtva-031-ramon-rossell",
            "lead-rtva-032-anna-riberaygua",
            "lead-yt-033-david-montane",
            "lead-yt-034-antoni-marti",
            "lead-yt-035-cerni-escale",
            "lead-yt-036-xavier-espot",
            "lead-yt-037-oscar-ribas",
            "lead-yt-038-conxita-marsol",
            "lead-yt-039-marta-roure",
            "lead-yt-040-guillem-forne",
            "lead-yt-041-guillem-areny",
            "lead-yt-042-andreu-gonzalez",
            "lead-yt-043-oriol-agorreta",
            "lead-yt-044-laura-casanovas",
            "lead-yt-045-arnau-rius",
            "lead-yt-046-alberto-villagrasa",
            "lead-yt-047-katia-ustina",
            "lead-yt-048-ander-mirambell",
            "lead-yt-049-joan-piquet",
            "lead-yt-050-pau-chica",
        "lead-yt-051-albert-vilaro",
        "lead-yt-052-valenti-closa",
        "lead-yt-053-sonia-andorrita",
        "lead-yt-054-francesc-solana",
        "lead-yt-055-enric-flix",
        "lead-yt-056-arnau-fortuny",
        "lead-yt-057-gabriel-lezkano",
        "lead-yt-058-nuria-pablos",
        "lead-rtva-059-carles-ensenyat",
        "lead-rtva-060-xavier-espot-actual",
        "lead-rtva-061-antoni-morell",
        ))
        or "nodes-formes-completa.tsv" in prospect_player
    ):
        errors.append("auditoria-prospeccio-nova.html no confirma els 1650 clips separats")
    prospect_linguistic_summary = read("proveniencia/prospeccio/resum-analisi-linguistica.tsv") if (PROV / "prospeccio/resum-analisi-linguistica.tsv").exists() else []
    prospect_linguistic_rows = []
    for lead in (
        "lead-rtva-009-isidre-bartumeu",
        "lead-rtva-010-lurdes-riba",
        "lead-rtva-011-josep-dalleres",
        "lead-rtva-012-marc-forne",
        "lead-rtva-013-pere-vilanova",
        "lead-rtva-014-joan-burgues",
        "lead-rtva-015-isidre-baro",
        "lead-rtva-016-josep-areny",
        "lead-rtva-017-simo-duro",
        "lead-rtva-018-ricard-fiter",
        "lead-rtva-019-lisa-cruz",
        "lead-rtva-020-monica-bonell",
        "lead-rtva-021-bonaventura-riberaygua",
        "lead-rtva-022-josep-marsal",
        "lead-rtva-023-josep-maria-cases",
        "lead-rtva-024-denisa-font",
        "lead-rtva-025-albert-gelabert",
        "lead-rtva-026-rosa-maria-mandico",
        "lead-rtva-027-jordi-guillamet",
        "lead-rtva-028-pere-besoli",
        "lead-rtva-029-angelina-mas",
        "lead-rtva-030-casimir-arajol",
        "lead-rtva-031-ramon-rossell",
        "lead-rtva-032-anna-riberaygua",
        "lead-yt-033-david-montane",
        "lead-yt-034-antoni-marti",
        "lead-yt-035-cerni-escale",
        "lead-yt-036-xavier-espot",
        "lead-yt-037-oscar-ribas",
        "lead-yt-038-conxita-marsol",
        "lead-yt-039-marta-roure",
        "lead-yt-040-guillem-forne",
        "lead-yt-041-guillem-areny",
        "lead-yt-042-andreu-gonzalez",
        "lead-yt-043-oriol-agorreta",
        "lead-yt-044-laura-casanovas",
        "lead-yt-045-arnau-rius",
        "lead-yt-046-alberto-villagrasa",
        "lead-yt-047-katia-ustina",
        "lead-yt-048-ander-mirambell",
        "lead-yt-049-joan-piquet",
        "lead-yt-050-pau-chica",
        "lead-yt-051-albert-vilaro",
        "lead-yt-052-valenti-closa",
        "lead-yt-053-sonia-andorrita",
        "lead-yt-054-francesc-solana",
        "lead-yt-055-enric-flix",
        "lead-yt-056-arnau-fortuny",
        "lead-yt-057-gabriel-lezkano",
        "lead-yt-058-nuria-pablos",
        "lead-rtva-059-carles-ensenyat",
        "lead-rtva-060-xavier-espot-actual",
        "lead-rtva-061-antoni-morell",
    ):
        path = PROV / "prospeccio" / lead / "analisi-linguistica.tsv"
        if path.exists():
            prospect_linguistic_rows.extend(read(f"proveniencia/prospeccio/{lead}/analisi-linguistica.tsv"))
    report_linguistic = sum(
        "## Inventari lingüístic comparable" in (PROV / "prospeccio" / lead / "informe.md").read_text(encoding="utf-8")
        for lead in (
            "lead-rtva-009-isidre-bartumeu",
            "lead-rtva-010-lurdes-riba",
            "lead-rtva-011-josep-dalleres",
            "lead-rtva-012-marc-forne",
            "lead-rtva-013-pere-vilanova",
            "lead-rtva-014-joan-burgues",
            "lead-rtva-015-isidre-baro",
            "lead-rtva-016-josep-areny",
            "lead-rtva-017-simo-duro",
            "lead-rtva-018-ricard-fiter",
            "lead-rtva-019-lisa-cruz",
            "lead-rtva-020-monica-bonell",
            "lead-rtva-021-bonaventura-riberaygua",
            "lead-rtva-022-josep-marsal",
            "lead-rtva-023-josep-maria-cases",
            "lead-rtva-024-denisa-font",
            "lead-rtva-025-albert-gelabert",
            "lead-rtva-026-rosa-maria-mandico",
            "lead-rtva-027-jordi-guillamet",
            "lead-rtva-028-pere-besoli",
            "lead-rtva-029-angelina-mas",
            "lead-rtva-030-casimir-arajol",
            "lead-rtva-031-ramon-rossell",
            "lead-rtva-032-anna-riberaygua",
            "lead-yt-033-david-montane",
            "lead-yt-034-antoni-marti",
            "lead-yt-035-cerni-escale",
            "lead-yt-036-xavier-espot",
            "lead-yt-037-oscar-ribas",
            "lead-yt-038-conxita-marsol",
            "lead-yt-039-marta-roure",
            "lead-yt-040-guillem-forne",
            "lead-yt-041-guillem-areny",
            "lead-yt-042-andreu-gonzalez",
            "lead-yt-043-oriol-agorreta",
            "lead-yt-044-laura-casanovas",
            "lead-yt-045-arnau-rius",
            "lead-yt-046-alberto-villagrasa",
            "lead-yt-047-katia-ustina",
            "lead-yt-048-ander-mirambell",
            "lead-yt-049-joan-piquet",
            "lead-yt-050-pau-chica",
        "lead-yt-051-albert-vilaro",
        "lead-yt-052-valenti-closa",
        "lead-yt-053-sonia-andorrita",
        "lead-yt-054-francesc-solana",
        "lead-yt-055-enric-flix",
        "lead-yt-056-arnau-fortuny",
        "lead-yt-057-gabriel-lezkano",
        "lead-yt-058-nuria-pablos",
        "lead-rtva-059-carles-ensenyat",
        "lead-rtva-060-xavier-espot-actual",
        "lead-rtva-061-antoni-morell",
        )
        if (PROV / "prospeccio" / lead / "informe.md").exists()
    )
    if len(prospect_linguistic_summary) != 106 or len(prospect_linguistic_rows) != 106 or any(row.get("estat") != "inventari ASR; pendent d'audició" for row in prospect_linguistic_rows) or report_linguistic != 53:
        errors.append("anàlisi lingüística de la prospecció nova incompleta o sense avís ASR")
    arrelament = read("proveniencia/auditoria-arrelament-andorra.tsv") if (PROV / "auditoria-arrelament-andorra.tsv").exists() else []
    if len(arrelament) != 53 or any(row.get("estat") != "pendent_validacio_humana" for row in arrelament):
        errors.append("auditoria-arrelament-andorra.tsv incompleta o amb afirmacions no marcades com a pendents")
    graph_audit = read("proveniencia/auditoria-grafo-independent.tsv")
    if len(graph_audit) != 9 or any(row.get("estat") != "independent" for row in graph_audit):
        errors.append("auditoria-grafo-independent.tsv detecta IDs fora del conjunt canònic")
    scarce_graph_nodes = read("grafo/nodes-formes-escasses.tsv")
    scarce_graph_edges = read("grafo/arestes-parlants-formes-escasses.tsv")
    scarce_graph_matrix = read("grafo/matriu-formes-escasses.tsv")
    scarce_graph_readme = (ROOT / "grafo/README-formes-escasses.md").read_text(encoding="utf-8") if (ROOT / "grafo/README-formes-escasses.md").exists() else ""
    if (
        len(scarce_graph_nodes) != 60
        or len(scarce_graph_edges) != 13
        or len(scarce_graph_matrix) != 600
        or "10 formes" not in scarce_graph_readme
        or any(not row.get("id_parlant", "").startswith("spk-") for row in scarce_graph_nodes)
        or any(not row.get("id_a", "").startswith("spk-") or not row.get("id_b", "").startswith("spk-") for row in scarce_graph_edges)
    ):
        errors.append("graf de formes escasses inconsistent o amb IDs fora del cànon")
    candidate_audit = read("proveniencia/auditoria-candidats.tsv")
    if (
        len(candidate_audit) != 11
        or sum(int(row.get("n_clips", "0")) for row in candidate_audit) != 124
        or sum(int(row.get("n_formes_consens", "0")) for row in candidate_audit) != 371
        or any(not row.get("source_page") for row in candidate_audit)
        or any(row.get("estat") != "separat-del-canon; pendent-d-audicio" or row.get("veu_confirmada") != "pendent" or row.get("termes_confirmats") != "pendent" for row in candidate_audit)
    ):
        errors.append("auditoria-candidats.tsv no confirma els 11 expedients separats i pendents")
    candidate_transcript_audit = read("proveniencia/auditoria-integritat-transcripcions-candidats.tsv")
    if (
        len(candidate_transcript_audit) != 124
        or sum(row.get("estat") == "complet" for row in candidate_transcript_audit) != 124
        or any(row.get("audio_exists") != "sí" or row.get("small_exists") != "sí" or row.get("base_exists") != "sí" or not row.get("audio_sha256") for row in candidate_transcript_audit)
    ):
        errors.append("auditoria-integritat-transcripcions-candidats.tsv no confirma 124 clips amb WAV i doble ASR local")
    candidate_form_nodes = read("grafo/nodes-formes-candidats.tsv")
    candidate_form_edges = read("grafo/arestes-formes-candidats.tsv")
    candidate_graph_readme = (ROOT / "grafo/README-formes-candidats.md").read_text(encoding="utf-8") if (ROOT / "grafo/README-formes-candidats.md").exists() else ""
    if (
        len(candidate_form_nodes) != 100
        or len(candidate_form_edges) != 36
        or len({row.get("candidat") for row in candidate_form_nodes}) != 9
        or any(not row.get("candidat", "").startswith("lead-") for row in candidate_form_nodes)
        or any(not row.get("candidat_a", "").startswith("lead-") or not row.get("candidat_b", "").startswith("lead-") for row in candidate_form_edges)
        or "11 candidats" not in candidate_graph_readme
        or "no enllacen amb `nodes-formes-completa.tsv`" not in candidate_graph_readme
    ):
        errors.append("graf de formes dels candidats inconsistent o connectat al cànon")
    candidate_player = (PROV / "auditoria-candidats-completa.html").read_text(encoding="utf-8") if (PROV / "auditoria-candidats-completa.html").exists() else ""
    if "<title>Audició completa dels candidats — corpus de parla andorrana</title>" not in candidate_player or '<meta name="candidate-items" content="124">' not in candidate_player or candidate_player.count('"id":') != 124:
        errors.append("auditoria-candidats-completa.html no confirma els 124 clips dels 11 candidats")
    candidate_queue = read("proveniencia/cua-audicio-candidats-prioritaria.tsv")
    candidate_queue_audio = [
        row for row in candidate_queue
        if not (PROV / row.get("clip", "")).exists()
        or hashlib.sha256((PROV / row["clip"]).read_bytes()).hexdigest() != row.get("sha256")
        or not (PROV / row.get("transcripcio_small", "")).exists()
        or not (PROV / row.get("transcripcio_base", "")).exists()
    ]
    if (
        len(candidate_queue) != 20
        or len({row.get("candidate") for row in candidate_queue}) != 11
        or candidate_queue_audio
        or any(row.get("estat_audicio") != "pendent" or row.get("veu_confirmada") != "pendent" or row.get("forma_confirmada") != "pendent" for row in candidate_queue)
    ):
        errors.append("cua-audicio-candidats-prioritaria.tsv no confirma 20 clips locals, 11 candidats i camps humans pendents")
    priority_player = (PROV / "auditoria-cua-candidats-prioritaria.html").read_text(encoding="utf-8") if (PROV / "auditoria-cua-candidats-prioritaria.html").exists() else ""
    if "<title>Audició prioritària de candidats — corpus de parla andorrana</title>" not in priority_player or priority_player.count('"id":') != 20 or "anotacions-cua-candidats-prioritaria.tsv" not in priority_player:
        errors.append("auditoria-cua-candidats-prioritaria.html no confirma els 20 clips de la cua humana")
    objective_audit = read("proveniencia/auditoria-objectiu.tsv")
    candidate_objective = next((row for row in objective_audit if row.get("requisit") == "graf separat de candidats"), None)
    if (
        len(objective_audit) != 23
        or candidate_objective is None
        or "100 nodes" not in candidate_objective.get("evidencia", "")
        or "36 arestes" not in candidate_objective.get("evidencia", "")
        or candidate_objective.get("estat") != "assolit com a semblança textual exploratòria"
    ):
        errors.append("auditoria-objectiu.tsv no registra el graf separat dels candidats")
    candidate_acoustic_objective = next((row for row in objective_audit if row.get("requisit") == "graf acústic separat de candidats"), None)
    if (
        candidate_acoustic_objective is None
        or "124 nodes" not in candidate_acoustic_objective.get("evidencia", "")
        or "859 arestes" not in candidate_acoustic_objective.get("evidencia", "")
    ):
        errors.append("auditoria-objectiu.tsv no registra el graf acústic dels candidats")
    quarantine_alt = read("proveniencia/qa-quarantena-20s-alt-resum.tsv")
    if len(quarantine_alt) != 237 or sum(row.get("estat") == "text-localitzable" for row in quarantine_alt) != 193 or sum(row.get("estat") == "bucle-asr" for row in quarantine_alt) != 42 or sum(row.get("estat") == "silenci" for row in quarantine_alt) != 2:
        errors.append("qa-quarantena-20s-alt-resum.tsv no confirma la passada alternativa de 237 finestres")
    quarantine_queue = read("proveniencia/auditoria-cua-quarantena-20s.tsv")
    if len(quarantine_queue) != 15 or any(row.get("estat") != "preparat" or row.get("estat_asr_alternatiu") != "text-localitzable" for row in quarantine_queue):
        errors.append("auditoria-cua-quarantena-20s.tsv no confirma 15 clips preparats i localitzables")
    forms_audit = read("proveniencia/auditoria-cobertura-formes.tsv")
    if len(forms_audit) != 35 or sum(row.get("nivell_cobertura") == "escassa" for row in forms_audit) != 10 or any(row.get("prioritat_audicio") not in {"alta", "mitjana", "normal"} for row in forms_audit):
        errors.append("auditoria-cobertura-formes.tsv no confirma les 35 formes i la priorització")
    forms_quadern = (PROV / "quadern-formes-representatives.md").read_text(encoding="utf-8") if (PROV / "quadern-formes-representatives.md").exists() else ""
    if "# Quadern de formes representatives del corpus de parla andorrana" not in forms_quadern or forms_quadern.count("## ") != 35 or "pendent d'audició humana" not in forms_quadern:
        errors.append("quadern-formes-representatives.md no confirma les 35 formes i els contextos pendents")
    people_coverage_md = (PROV / "auditoria-cobertura-persones.md").read_text(encoding="utf-8") if (PROV / "auditoria-cobertura-persones.md").exists() else ""
    if "# Auditoria de cobertura per persona" not in people_coverage_md or "66/66" not in people_coverage_md or people_coverage_md.count("| `pa-") != 66:
        errors.append("auditoria-cobertura-persones.md no confirma les 66 fitxes documentals")
    grammar_quadern = (PROV / "quadern-evidencia-gramatica.md").read_text(encoding="utf-8") if (PROV / "quadern-evidencia-gramatica.md").exists() else ""
    if "# Quadern d'evidència gramatical i de contacte" not in grammar_quadern or "10,458 contextos" not in grammar_quadern or grammar_quadern.count("## ") != 9 or "requereix escolta" not in grammar_quadern:
        errors.append("quadern-evidencia-gramatica.md no confirma les nou categories ASR pendents")
    audio_format_md = (PROV / "auditoria-format-audio.md").read_text(encoding="utf-8") if (PROV / "auditoria-format-audio.md").exists() else ""
    if "# Auditoria de format d'àudio" not in audio_format_md or "66/66" not in audio_format_md or "656/656" not in audio_format_md:
        errors.append("auditoria-format-audio.md no confirma fonts i clips amb format vàlid")
    prospect_map = (PROV / "mapa-prospeccio.md").read_text(encoding="utf-8") if (PROV / "mapa-prospeccio.md").exists() else ""
    if "# Mapa de prospecció del corpus de parla andorrana" not in prospect_map or "66 fonts canòniques" not in prospect_map or "11 candidats preanalitzats" not in prospect_map or "4 referències" not in prospect_map:
        errors.append("mapa-prospeccio.md no confirma fonts, candidats i permisos pendents")
    scarce_queue = read("proveniencia/cua-audicio-formes-escasses.tsv")
    scarce_forms = {row.get("forma") for row in scarce_queue}
    scarce_bad = [row for row in scarce_queue if not (PROV / row["clip"]).exists() or hashlib.sha256((PROV / row["clip"]).read_bytes()).hexdigest() != row["sha256"] or row.get("decisio_humana") != "pendent"]
    if len(scarce_queue) != 30 or len(scarce_forms) != 10 or scarce_bad:
        errors.append("cua-audicio-formes-escasses.tsv no confirma 30 clips locals amb hash i decisions pendents")
    scarce_priority = read("proveniencia/cua-audicio-formes-escasses-prioritaria.tsv")
    scarce_priority_bad = [row for row in scarce_priority if not (PROV / row["clip"]).exists() or hashlib.sha256((PROV / row["clip"]).read_bytes()).hexdigest() != row["sha256"] or row.get("decisio_humana") != "pendent"]
    if len(scarce_priority) != 10 or len({row.get("forma") for row in scarce_priority}) != 10 or scarce_priority_bad:
        errors.append("cua-audicio-formes-escasses-prioritaria.tsv no confirma un clip local per forma i decisions pendents")
    scarce_register = read("proveniencia/registre-audicio-formes-escasses.tsv")
    scarce_register_keys = {(row.get("id_persona"), row.get("forma"), row.get("clip")) for row in scarce_register}
    if len(scarce_register) != 30 or scarce_register_keys != {(row.get("id_persona"), row.get("forma"), row.get("clip")) for row in scarce_queue} or any(row.get("estat_audicio") not in {"pendent", "confirmada", "descartada", "incerta"} for row in scarce_register):
        errors.append("registre-audicio-formes-escasses.tsv no confirma 30 claus i estats vàlids")
    scarce_guide = read("proveniencia/guia-audicio-formes-escasses.tsv")
    if len(scarce_guide) != 10 or sum(int(row.get("n_clips", "0")) for row in scarce_guide) != 30 or any(row.get("estat") != "pendent d'audició" for row in scarce_guide):
        errors.append("guia-audicio-formes-escasses.tsv no confirma 10 formes i 30 clips pendents")
    scarce_acoustic = read("proveniencia/analisi-acustica-formes-escasses.tsv")
    if len(scarce_acoustic) != 30 or len({(row.get("id_persona"), row.get("forma"), row.get("clip")) for row in scarce_acoustic}) != 30 or any(not row.get("nota", "").startswith("descriptor orientatiu") for row in scarce_acoustic):
        errors.append("analisi-acustica-formes-escasses.tsv no confirma 30 descriptors instrumentals")
    hearing_summary = read("proveniencia/resum-estat-audicio.tsv")
    if len(hearing_summary) != 60 or sum(int(row.get("n_intervals", "0")) for row in hearing_summary) != 686 or sum(int(row.get("n_intervals_escasses", "0")) for row in hearing_summary) != 30 or sum(int(row.get("pendent", "0")) for row in hearing_summary) != 686:
        errors.append("resum-estat-audicio.tsv no confirma 60 persones i 686 clips pendents")
    scarce_player = (PROV / "auditoria-formes-escasses.html").read_text(encoding="utf-8") if (PROV / "auditoria-formes-escasses.html").exists() else ""
    if "<title>Audició — formes escasses del corpus de parla andorrana</title>" not in scarce_player or scarce_player.count('"id":') != 30:
        errors.append("auditoria-formes-escasses.html no confirma el reproductor local dels 30 clips")
    candidate_stereo = ROOT / "proveniencia/candidats/lead-rtva-001/audio-stereo.wav"
    if not candidate_stereo.exists() or hashlib.sha256(candidate_stereo.read_bytes()).hexdigest() != "93888c71234150052b8bb50a9aebe4790007f19e2c61e50e0761d11d137568c8":
        errors.append("hash de l'àudio estèreo candidat lead-rtva-001 invàlid")
    candidate_audio = ROOT / "proveniencia/candidats/lead-rtva-001/audio.wav"
    if not candidate_audio.exists() or hashlib.sha256(candidate_audio.read_bytes()).hexdigest() != "5317200bbe5ca24c2262499ccdf03491936bb317accb7311bafe8fd248df099b":
        errors.append("hash de l'àudio candidat lead-rtva-001 invàlid")
    candidate_ian_audio = ROOT / "proveniencia/candidats/lead-rtva-002-ian-moya/audio.wav"
    if not candidate_ian_audio.exists() or hashlib.sha256(candidate_ian_audio.read_bytes()).hexdigest() != "6aab86bcd8fdcb40d247e85f27cec1ed3ef07807bdc238bf286438ccdac005be":
        errors.append("hash de l'àudio candidat lead-rtva-002-ian-moya invàlid")
    candidate_ian_mp3 = ROOT / "proveniencia/candidats/lead-rtva-002-ian-moya/audio-original.mp3"
    if not candidate_ian_mp3.exists() or hashlib.sha256(candidate_ian_mp3.read_bytes()).hexdigest() != "33a1f035f56e9a86dec3e1d08d984ee81c3a840f99368479273d2b4a535366c1":
        errors.append("hash del MP3 original candidat lead-rtva-002-ian-moya invàlid")
    candidate_dj_audio = ROOT / "proveniencia/candidats/lead-rtva-003-dj-neura/audio.wav"
    if not candidate_dj_audio.exists() or hashlib.sha256(candidate_dj_audio.read_bytes()).hexdigest() != "215137090848657e1aae31f5cf3ca144ffdd83e2358ac14905f11754403f91aa":
        errors.append("hash de l'àudio candidat lead-rtva-003-dj-neura invàlid")
    candidate_dj_mp3 = ROOT / "proveniencia/candidats/lead-rtva-003-dj-neura/audio-original.mp3"
    if not candidate_dj_mp3.exists() or hashlib.sha256(candidate_dj_mp3.read_bytes()).hexdigest() != "02d0856611082534b956121557ce01db00e7b8391db07b0423c7fd9472df0502":
        errors.append("hash del MP3 original candidat lead-rtva-003-dj-neura invàlid")
    candidate_joan_mico_audio = ROOT / "proveniencia/candidats/lead-rtva-004-joan-mico/audio.wav"
    if not candidate_joan_mico_audio.exists() or hashlib.sha256(candidate_joan_mico_audio.read_bytes()).hexdigest() != "7e7372265a56c2a33f955856288d76b2fe4552b3f710d61280436d3b38b4cfbe":
        errors.append("hash de l'àudio candidat lead-rtva-004-joan-mico invàlid")
    candidate_joan_mico_mp3 = ROOT / "proveniencia/candidats/lead-rtva-004-joan-mico/audio-original.mp3"
    if not candidate_joan_mico_mp3.exists() or hashlib.sha256(candidate_joan_mico_mp3.read_bytes()).hexdigest() != "31de7b084b689d9dfd3f31982e11507b1d9a49ef2ad16fcee55162c0478167bc":
        errors.append("hash del MP3 original candidat lead-rtva-004-joan-mico invàlid")
    candidate_xavier_audio = ROOT / "proveniencia/candidats/lead-cg-001-xavier-espot/audio.wav"
    if not candidate_xavier_audio.exists() or hashlib.sha256(candidate_xavier_audio.read_bytes()).hexdigest() != "748c588fe7403ee9bd33115814357e212f8963f9aef77dad1295956d348be405":
        errors.append("hash de l'extracte candidat lead-cg-001-xavier-espot invàlid")
    candidate_roser_audio = ROOT / "proveniencia/candidats/lead-cg-003-roser-sune/audio.wav"
    if not candidate_roser_audio.exists() or hashlib.sha256(candidate_roser_audio.read_bytes()).hexdigest() != "fa19d408c228361841b944d50a1b2be0b3f993f20f39cdea493abd2367ea0719":
        errors.append("hash de l'àudio candidat lead-cg-003-roser-sune invàlid")
    candidate_carine_audio = ROOT / "proveniencia/candidats/lead-rtva-005-carine-montaner/audio.wav"
    if not candidate_carine_audio.exists() or hashlib.sha256(candidate_carine_audio.read_bytes()).hexdigest() != "d48772ec308ba4fc686b2811b0f6ec4988ee9f95dcf4993c542785886b913840":
        errors.append("hash de l'àudio candidat lead-rtva-005-carine-montaner invàlid")
    candidate_jaume_audio = ROOT / "proveniencia/candidats/lead-rtva-006-jaume-tomas/audio.wav"
    if not candidate_jaume_audio.exists() or hashlib.sha256(candidate_jaume_audio.read_bytes()).hexdigest() != "936cd8a49ad7ce1bcf89c17cfe705c37d8b019fdbe5b2e187b1594d11176ef5c":
        errors.append("hash de l'àudio candidat lead-rtva-006-jaume-tomas invàlid")
    candidate_robert_audio = ROOT / "proveniencia/candidats/lead-rtva-007-robert-guirao/audio.wav"
    if not candidate_robert_audio.exists() or hashlib.sha256(candidate_robert_audio.read_bytes()).hexdigest() != "70e8c005d798cd5f14bcb53e6ae5602c349e6db05aeea46e0faef4eb55a096b3":
        errors.append("hash de l'àudio candidat lead-rtva-007-robert-guirao invàlid")
    candidate_mireia_audio = ROOT / "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/audio.wav"
    if not candidate_mireia_audio.exists() or hashlib.sha256(candidate_mireia_audio.read_bytes()).hexdigest() != "99092a10edeccecfcab0f7596a18600545f5a9c11243d083e5e92e287e96a39c":
        errors.append("hash de l'àudio candidat lead-rtva-008-mireia-pedescoll invàlid")
    if bad_hashes:
        errors.append(f"hashes de clips invàlids: {len(bad_hashes)}")
    for rel, expected in [("proveniencia/prioritat-audicio-triple.tsv", 656), ("proveniencia/inventari-incerteses-asr.tsv", 13390), ("proveniencia/cua-audicio-incerteses.tsv", 100), ("proveniencia/qa-beam.tsv", 63), ("proveniencia/qa-quarantena-20s.tsv", 237), ("proveniencia/cua-audicio-quarantena-20s.tsv", 15), ("proveniencia/qa-quarantena-20s-formes.tsv", 105), ("proveniencia/qa-quarantena-20s-consens.tsv", 15), ("proveniencia/analisi-acustica-quarantena-20s.tsv", 15), ("grafo/trets-triple-full.tsv", 19), ("grafo/arestes-parlants-triple-full.tsv", 106), ("grafo/nodes-triple-full.tsv", 60), ("grafo/matriu-formes-triple-full.tsv", 1140), ("proveniencia/qa-clips-greedy-full.tsv", 656), ("proveniencia/qa-clips-triple-full.tsv", 656), ("proveniencia/qa-equilibrada-triple.tsv", 100), ("proveniencia/resum-estat-audicio.tsv", 60), ("proveniencia/resum-trajectories-base-equilibrada.tsv", 19), ("proveniencia/analisi-trajectories-base-equilibrada.tsv", 350), ("proveniencia/prioritat-audicio-equilibrada.tsv", 100), ("proveniencia/persones-canonics.tsv", 66), ("proveniencia/auditoria-cobertura-persones.tsv", 66), ("proveniencia/auditoria-identitat-linguistica.tsv", 60), ("grafo/trets-small-token-canonics.tsv", 20), ("grafo/arestes-parlants-small-token-canonics.tsv", 996), ("grafo/nodes-small-token-canonics.tsv", 60), ("grafo/matriu-formes-small-token-canonics.tsv", 1200), ("proveniencia/qa-equilibrada-base-tokens.tsv", 100), ("proveniencia/qa-equilibrada-base-token-occurrences.tsv", 70), ("proveniencia/analisi-formants-base-equilibrada.tsv", 70), ("proveniencia/resum-formants-base-equilibrada.tsv", 19), ("proveniencia/qa-equilibrada-base.tsv", 100), ("proveniencia/qa-equilibrada-consens.tsv", 100), ("proveniencia/qa-clips.tsv", 656), ("proveniencia/qa-clips-base.tsv", 656), ("proveniencia/qa-clips-consens.tsv", 656), ("proveniencia/qa-clips-boundary.tsv", 656), ("proveniencia/resum-consens-per-persona.tsv", 66), ("proveniencia/resum-boundary-per-persona.tsv", 66), ("proveniencia/analisi-acustica-clips.tsv", 656), ("proveniencia/analisi-acustica-consens.tsv", 263), ("proveniencia/resum-acustica-formes-consens.tsv", 20), ("proveniencia/analisi-acustica-normalitzada-consens.tsv", 263), ("proveniencia/resum-acustica-normalitzada-formes.tsv", 20), ("proveniencia/analisi-formants-consens.tsv", 250), ("proveniencia/resum-formants-consens.tsv", 20), ("proveniencia/analisi-formants-qa.tsv", 309), ("proveniencia/resum-formants-qa.tsv", 20), ("proveniencia/qa-cua-small-json.tsv", 656), ("proveniencia/qa-cua-small-tokens.tsv", 656), ("proveniencia/qa-cua-small-token-occurrences.tsv", 451), ("proveniencia/analisi-formants-cua-small.tsv", 451), ("proveniencia/resum-formants-cua-small.tsv", 20), ("proveniencia/analisi-trajectories-formants.tsv", 1250), ("proveniencia/resum-trajectories-formants.tsv", 20), ("proveniencia/evidencia-gramatica.tsv", 10458), ("proveniencia/resum-evidencia-gramatica.tsv", 66), ("proveniencia/prioritat-formes-small-token.tsv", 20), ("proveniencia/qa-clips-forts-greedy.tsv", 109), ("proveniencia/qa-clips-forts-consens.tsv", 109), ("proveniencia/registre-audicio-forts-divergencies.tsv", 28), ("proveniencia/analisi-acustica-divergencies.tsv", 28), ("proveniencia/repertori-evidencia.tsv", 1188), ("proveniencia/resum-cobertura-repertori.tsv", 18), ("proveniencia/qa-consens-tokens-base.tsv", 263), ("proveniencia/prioritat-consens-token.tsv", 263), ("proveniencia/qa-token-missing-small.tsv", 14), ("proveniencia/qa-token-missing-comparativa.tsv", 14), ("proveniencia/qa-quarantena-base.tsv", 9), ("proveniencia/qa-quarantena-comparativa.tsv", 9), ("proveniencia/registre-audicio.tsv", 656), ("proveniencia/prioritat-audicio.tsv", 656), ("grafo/trets-linguistics.tsv", 284), ("grafo/arestes-linguistics.tsv", 1951), ("grafo/trets-small-token.tsv", 20), ("grafo/arestes-parlants-small-token.tsv", 1140), ("grafo/nodes-small-token.tsv", 66), ("grafo/matriu-formes.tsv", 2310), ("grafo/matriu-formes-linguistics.tsv", 18744), ("grafo/matriu-formes-small-token.tsv", 1320), ("grafo/trets-formes-completa.tsv", 35), ("grafo/arestes-parlants-formes-completa.tsv", 1690), ("grafo/nodes-formes-completa.tsv", 60), ("grafo/matriu-formes-completa.tsv", 2100), ("grafo/nodes-acustic-candidats.tsv", 124), ("grafo/arestes-acustic-candidats.tsv", 859), ("grafo/nodes-acustic-canonic.tsv", 60), ("grafo/arestes-acustic-canonic.tsv", 1036), ("proveniencia/evidencia-formes.tsv", 2014), ("proveniencia/candidats/lead-rtva-002-ian-moya/formes.tsv", 299), ("proveniencia/candidats/lead-rtva-002-ian-moya/formes-consens.tsv", 35), ("proveniencia/candidats/lead-rtva-002-ian-moya/formes-clips.tsv", 15), ("proveniencia/candidats/lead-rtva-002-ian-moya/graf/arestes.tsv", 60), ("proveniencia/candidats/lead-rtva-002-ian-moya/graf/nodes.tsv", 61), ("proveniencia/candidats/lead-rtva-002-ian-moya/graf/trets.tsv", 14), ("proveniencia/candidats/lead-rtva-002-ian-moya/segments-speaker-provisional.tsv", 470), ("proveniencia/candidats/lead-rtva-002-ian-moya/formes-ian-provisional.tsv", 40), ("proveniencia/candidats/lead-rtva-003-dj-neura/formes.tsv", 79), ("proveniencia/candidats/lead-rtva-003-dj-neura/formes-consens.tsv", 35), ("proveniencia/candidats/lead-rtva-003-dj-neura/formes-clips.tsv", 10), ("proveniencia/candidats/lead-rtva-003-dj-neura/graf/arestes.tsv", 60), ("proveniencia/candidats/lead-rtva-003-dj-neura/graf/nodes.tsv", 61), ("proveniencia/candidats/lead-rtva-003-dj-neura/graf/trets.tsv", 8), ("proveniencia/candidats/lead-rtva-003-dj-neura/segments-speaker-provisional.tsv", 142), ("proveniencia/candidats/lead-rtva-003-dj-neura/formes-dj-neura-provisional.tsv", 17), ("proveniencia/candidats/lead-rtva-001/analisi-acustica.tsv", 10), ("proveniencia/candidats/lead-rtva-002-ian-moya/qa-greedy.tsv", 15), ("proveniencia/candidats/lead-rtva-002-ian-moya/formants.tsv", 15), ("proveniencia/candidats/lead-rtva-002-ian-moya/analisi-acustica.tsv", 15), ("proveniencia/candidats/lead-rtva-003-dj-neura/qa-greedy.tsv", 10), ("proveniencia/candidats/lead-rtva-003-dj-neura/formants.tsv", 10), ("proveniencia/candidats/lead-rtva-003-dj-neura/analisi-acustica.tsv", 10), ("proveniencia/candidats/lead-rtva-004-joan-mico/formes.tsv", 327), ("proveniencia/candidats/lead-rtva-004-joan-mico/formes-consens.tsv", 35), ("proveniencia/candidats/lead-rtva-004-joan-mico/formes-clips.tsv", 12), ("proveniencia/candidats/lead-rtva-004-joan-mico/graf/arestes.tsv", 60), ("proveniencia/candidats/lead-rtva-004-joan-mico/graf/nodes.tsv", 61), ("proveniencia/candidats/lead-rtva-004-joan-mico/graf/trets.tsv", 12), ("proveniencia/candidats/lead-rtva-004-joan-mico/segments-speaker-provisional.tsv", 337), ("proveniencia/candidats/lead-rtva-004-joan-mico/formes-joan-mico-provisional.tsv", 22), ("proveniencia/candidats/lead-rtva-004-joan-mico/qa-greedy.tsv", 12), ("proveniencia/candidats/lead-rtva-004-joan-mico/analisi-acustica.tsv", 12), ("proveniencia/candidats/lead-rtva-004-joan-mico/formants.tsv", 12), ("proveniencia/candidats/lead-cg-001-xavier-espot/formes.tsv", 7), ("proveniencia/candidats/lead-cg-001-xavier-espot/formes-consens.tsv", 35), ("proveniencia/candidats/lead-cg-001-xavier-espot/formes-clips.tsv", 4), ("proveniencia/candidats/lead-cg-001-xavier-espot/graf/arestes.tsv", 37), ("proveniencia/candidats/lead-cg-001-xavier-espot/graf/nodes.tsv", 61), ("proveniencia/candidats/lead-cg-001-xavier-espot/graf/trets.tsv", 3), ("proveniencia/candidats/lead-cg-001-xavier-espot/segments-speaker-provisional.tsv", 32), ("proveniencia/candidats/lead-cg-001-xavier-espot/formes-xavier-espot-provisional.tsv", 0), ("proveniencia/candidats/lead-cg-001-xavier-espot/qa-greedy.tsv", 4), ("proveniencia/candidats/lead-cg-001-xavier-espot/analisi-acustica.tsv", 4), ("proveniencia/candidats/lead-cg-001-xavier-espot/formants.tsv", 4), ("proveniencia/cua-audicio-small-equilibrada.tsv", 100), ("proveniencia/sessions/sessio-01.tsv", 65), ("proveniencia/sessions/sessio-02.tsv", 20), ("proveniencia/guia-audicio-sessions-canoniques.tsv", 89), ("proveniencia/resum-cobertura-fonts.tsv", 4), ("proveniencia/sessions/sessio-03.tsv", 12), ("proveniencia/sessions/sessio-04.tsv", 4)]:
        if len(read(rel)) != expected:
            errors.append(f"{rel} no té {expected} files")
    if len(read("proveniencia/sessions/sessio-05.tsv")) != 20:
        errors.append("proveniencia/sessions/sessio-05.tsv no té 20 files")
    if len(read("proveniencia/sessions/sessio-06.tsv")) != 19:
        errors.append("proveniencia/sessions/sessio-06.tsv no té 19 files")
    coverage_sessions = read("proveniencia/auditoria-cobertura-sessions.tsv")
    if len(coverage_sessions) != 60 or sum(row.get("estat") == "cobert" for row in coverage_sessions) != 57 or sum(row.get("estat") == "quarantena" for row in coverage_sessions) != 3:
        errors.append("auditoria-cobertura-sessions.tsv no confirma 57 parlants coberts i 3 en quarantena")
    uncertain = read("proveniencia/inventari-incerteses-asr.tsv")
    missing_uncertain_clips = [clip for row in uncertain for clip in row["clips_coberts"].split(";") if clip and not (PROV / clip).exists()]
    if missing_uncertain_clips:
        errors.append(f"clips de l'inventari d'incerteses inexistents: {len(missing_uncertain_clips)}")
    if sum("### Evidència textual localitzable" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen evidència textual")
    if sum("## Buits registrats" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen Buits registrats")
    if sum("Mesura directa del WAV: **pendent**" in path.read_text(encoding="utf-8") for path in reports):
        errors.append("hi ha informes amb mètriques directes del WAV encara pendents")
    report_audit = read("proveniencia/auditoria-informes.tsv")
    if len(report_audit) != 66 or any(row.get("estat") != "complet-provisional" or row.get("cobertura_audicio") != "sí" for row in report_audit):
        errors.append("auditoria-informes.tsv no confirma 66 fitxes completes")
    if sum("### Inventari complet de formes candidates" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen l'inventari complet de formes")
    if sum("### Sessions operatives 01–02 i 05" in path.read_text(encoding="utf-8") for path in reports) != 61:
        errors.append("no totes les fitxes esperades tenen les sessions operatives 01–02, 05 i 06")
    if sum("### Repertori lingüístic complet" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen el repertori lingüístic complet")
    if (PROV / "quadern-sessions-canoniques.md").read_text(encoding="utf-8").count("## ") != 90:
        errors.append("el quadern de les sessions canòniques no té 89 entrades")
    if sum("### Consens textual de dues passades ASR" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen resum de doble ASR")
    if sum("### Perfil acústic dels consensos" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen perfil acústic de consensos")
    if sum("### Coincidències amb límit de paraula" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen recompte amb límit de paraula")
    if sum("### Referència institucional del cas persistent" in path.read_text(encoding="utf-8") for path in reports) != 7:
        errors.append("no hi ha set referències institucionals dels casos persistents")
    if sum("### Comparació ASR de quarantena" in path.read_text(encoding="utf-8") for path in reports) != 3:
        errors.append("no hi ha comparació ASR en les tres veus en quarantena")
    if sum("### Comparació ASR de la cua curta" in path.read_text(encoding="utf-8") for path in reports) != 3:
        errors.append("no hi ha comparació ASR de la cua curta en les tres veus en quarantena")
    if sum("### Perfil acústic de la cua curta" in path.read_text(encoding="utf-8") for path in reports) != 3:
        errors.append("no hi ha perfil acústic de la cua curta en les tres veus en quarantena")
    if sum("### Perfil acústic normalitzat dels consensos" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen perfil acústic normalitzat")
    if sum("### Mesures instrumentals de formants" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen mesures instrumentals de formants")
    if sum("### Trajectòries instrumentals de formants" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen trajectòries instrumentals de formants")
    if sum("### Evidència gramatical i de contacte textual" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen evidència gramatical i de contacte")
    if sum("### Tercera descodificació dels clips forts" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen la tercera descodificació dels clips forts")
    if sum("### Perfil formàntic de la cua QA" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen perfil formàntic de la cua QA")
    if sum("### Perfil formàntic de la cua completa small" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen perfil formàntic de la cua completa small")
    if sum("### Formes QA small compartides" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen formes QA small compartides")
    if sum("### Perfil small comparatiu" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen perfil small comparatiu")
    if sum("### Mostra equilibrada small per a l'audició" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen la mostra equilibrada d'audició")
    if sum("### Contrast small/base de la mostra equilibrada" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen el contrast small/base de la mostra equilibrada")
    if sum("### Formants base de coincidències small/base" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen formants base de la mostra equilibrada")
    if sum("### Prioritat d’audició de la mostra equilibrada" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen prioritat d’audició equilibrada")
    if sum("### Trajectòries base de la mostra equilibrada" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen trajectòries base de la mostra equilibrada")
    if sum("### Tercera descodificació de la mostra equilibrada" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen tercera descodificació equilibrada")
    if sum("### Tercera descodificació greedy de la cua completa" in path.read_text(encoding="utf-8") for path in reports) != 66:
        errors.append("no tots els informes tenen greedy de la cua completa")
    json_consens = list((PROV / "qa-consens-base-json").glob("*.json"))
    if len(json_consens) != 263:
        errors.append(f"JSON base de consensos {len(json_consens)} != 263")
    greedy_txt = list((PROV / "qa-equilibrada-greedy").glob("*.txt"))
    greedy_full_txt = list((PROV / "qa-clips-greedy-full").glob("*.txt"))
    candidate_clips = list((PROV / "candidats/lead-rtva-001/clips").glob("*.wav"))
    if len(candidate_clips) != 10:
        errors.append(f"clips de Joan Verdú {len(candidate_clips)} != 10")
    candidate_ian_clips = list((PROV / "candidats/lead-rtva-002-ian-moya/clips").glob("*.wav"))
    if len(candidate_ian_clips) != 15:
        errors.append(f"clips d'Ian Moya {len(candidate_ian_clips)} != 15")
    candidate_dj_clips = list((PROV / "candidats/lead-rtva-003-dj-neura/clips").glob("*.wav"))
    if len(candidate_dj_clips) != 10:
        errors.append(f"clips de DJ Neura {len(candidate_dj_clips)} != 10")
    candidate_joan_mico_clips = list((PROV / "candidats/lead-rtva-004-joan-mico/clips").glob("*.wav"))
    if len(candidate_joan_mico_clips) != 12:
        errors.append(f"clips de Joan Micó {len(candidate_joan_mico_clips)} != 12")
    candidate_xavier_clips = list((PROV / "candidats/lead-cg-001-xavier-espot/clips").glob("*.wav"))
    if len(candidate_xavier_clips) != 4:
        errors.append(f"clips de Xavier Espot {len(candidate_xavier_clips)} != 4")
    candidate_roser_clips = list((PROV / "candidats/lead-cg-003-roser-sune/clips").glob("*.wav"))
    if len(candidate_roser_clips) != 3:
        errors.append(f"clips de Roser Suñé {len(candidate_roser_clips)} != 3")
    candidate_carine_clips = list((PROV / "candidats/lead-rtva-005-carine-montaner/clips").glob("*.wav"))
    if len(candidate_carine_clips) != 22:
        errors.append(f"clips de Carine Montaner {len(candidate_carine_clips)} != 22")
    candidate_jaume_clips = list((PROV / "candidats/lead-rtva-006-jaume-tomas/clips").glob("*.wav"))
    if len(candidate_jaume_clips) != 14:
        errors.append(f"clips de Jaume Tomàs {len(candidate_jaume_clips)} != 14")
    candidate_robert_clips = list((PROV / "candidats/lead-rtva-007-robert-guirao/clips").glob("*.wav"))
    if len(candidate_robert_clips) != 13:
        errors.append(f"clips de Robert Guirao {len(candidate_robert_clips)} != 13")
    candidate_mireia_clips = list((PROV / "candidats/lead-rtva-008-mireia-pedescoll/clips").glob("*.wav"))
    if len(candidate_mireia_clips) != 19:
        errors.append(f"clips de Mireia Pedescoll {len(candidate_mireia_clips)} != 19")
    candidate_graph_counts = [("proveniencia/candidats/lead-rtva-001/graf/nodes.tsv", 61), ("proveniencia/candidats/lead-rtva-001/graf/arestes.tsv", 54), ("proveniencia/candidats/lead-rtva-001/graf/trets.tsv", 11)]
    for rel, expected in candidate_graph_counts:
        if len(read(rel)) != expected:
            errors.append(f"{rel} no té {expected} files")
    beam_txt = list((PROV / "qa-beam").glob("*.txt"))
    if len(beam_txt) != 63:
        errors.append(f"fitxers beam {len(beam_txt)} != 63")
    if len(greedy_full_txt) != 656:
        errors.append(f"fitxers greedy de la cua completa {len(greedy_full_txt)} != 656")
    if len(greedy_txt) != 100:
        errors.append(f"fitxers greedy de la mostra {len(greedy_txt)} != 100")
    json_equilibrada = list((PROV / "qa-equilibrada-base").glob("*.json"))
    txt_equilibrada = list((PROV / "qa-equilibrada-base").glob("*.txt"))
    if len(json_equilibrada) != 100 or len(txt_equilibrada) != 100:
        errors.append(f"fitxers base de la mostra equilibrada json={len(json_equilibrada)} txt={len(txt_equilibrada)} != 100")
    json_missing_small = list((PROV / "qa-token-missing-small-json").glob("*.json"))
    if len(json_missing_small) != 14:
        errors.append(f"JSON small de casos sense token {len(json_missing_small)} != 14")
    for rel in [
        "grafo/trets-qa.tsv",
        "grafo/arestes-parlants-qa.tsv",
        "grafo/trets-forts.tsv",
        "grafo/arestes-parlants-forts.tsv",
        "grafo/trets-base-consens.tsv",
        "grafo/arestes-parlants-base-consens.tsv",
        "grafo/graf-parlants-base-consens.mmd",
        "ESTAT-OBJECTIU.md",
        "persones/INDEX.md",
        "proveniencia/auditoria-cua.html",
        "proveniencia/genera-auditoria-cua.py",
        "proveniencia/genera-auditoria-global.py",
        "proveniencia/genera-auditoria-sessions-candidats.py",
        "proveniencia/auditoria-sessions-candidats.html",
        "proveniencia/genera-auditoria-sessions-canoniques.py",
        "proveniencia/auditoria-sessions-canoniques.html",
        "proveniencia/quadern-sessions-canoniques.md",
        "proveniencia/auditoria-objectiu.tsv",
        "proveniencia/auditoria-informes.tsv",
        "proveniencia/importa-auditoria-global.py",
        "proveniencia/genera-sessio-audicio-01.py",
        "proveniencia/genera-sessio-audicio-02.py",
        "proveniencia/genera-sessio-audicio-03.py",
        "proveniencia/genera-sessio-audicio-04.py",
        "proveniencia/auditoria-global.html",
        "proveniencia/sessions/sessio-01.md",
        "proveniencia/sessions/sessio-02.md",
        "proveniencia/sessions/sessio-03.md",
        "proveniencia/sessions/sessio-04.md",
        "proveniencia/genera-sessio-audicio-05.py",
        "proveniencia/genera-sessio-audicio-06.py",
        "proveniencia/verifica-sessions-audicio.py",
        "proveniencia/genera-auditoria-cobertura-sessions.py",
        "proveniencia/auditoria-cobertura-sessions.tsv",
        "proveniencia/genera-auditoria-integritat-audio.py",
        "proveniencia/auditoria-integritat-audio.tsv",
        "proveniencia/genera-auditoria-proveniencia.py",
        "proveniencia/auditoria-proveniencia.tsv",
        "proveniencia/genera-auditoria-integritat-transcripcions.py",
        "proveniencia/auditoria-integritat-transcripcions.tsv",
        "proveniencia/genera-remediacio-transcripcions.py",
        "proveniencia/auditoria-remediacio-transcripcions.tsv",
        "proveniencia/genera-index-audicio.py",
        "proveniencia/genera-index-persones.py",
        "proveniencia/INDEX-AUDICIO.md",
        "proveniencia/genera-auditoria-independencia.py",
        "proveniencia/auditoria-independencia.tsv",
        "proveniencia/genera-auditoria-aillament-brain.py",
        "proveniencia/auditoria-aillament-brain.tsv",
        "proveniencia/auditoria-aillament-brain.md",
        "proveniencia/prospeccio/INDEX.md",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/informe.md",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/source.info.json",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/source-page.html",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/audio.wav",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/asr/isidre-bartumeu-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/asr/isidre-bartumeu-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/informe.md",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/source.info.json",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/source-page.html",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/terms.md",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/audio.wav",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/asr/lurdes-riba-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/asr/lurdes-riba-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/informe.md",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/source.info.json",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/source-page.html",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/terms.md",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/audio.wav",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/asr/josep-dalleres-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/asr/josep-dalleres-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/informe.md",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/source.info.json",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/source-page.html",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/terms.md",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/audio.wav",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/asr/marc-forne-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/asr/marc-forne-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/informe.md",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/source.info.json",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/source-page.html",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/terms.md",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/audio.wav",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/asr/pere-vilanova-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/asr/pere-vilanova-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/informe.md",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/source.info.json",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/source-page.html",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/terms.md",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/audio.wav",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/asr/joan-burgues-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/asr/joan-burgues-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/informe.md",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/source.info.json",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/terms.md",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/source-page.html",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/audio.wav",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/asr/isidre-baro-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/asr/isidre-baro-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/informe.md",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/source.info.json",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/terms.md",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/source-page.html",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/audio.wav",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/asr/josep-areny-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/asr/josep-areny-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/informe.md",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/source.info.json",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/terms.md",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/source-page.html",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/audio.wav",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/asr/simo-duro-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/asr/simo-duro-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/informe.md",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/source.info.json",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/terms.md",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/source-page.html",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/audio.wav",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/asr/ricard-fiter-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/asr/ricard-fiter-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/informe.md",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/source.info.json",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/terms.md",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/source-page.html",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/audio.wav",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/asr/lisa-cruz-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/asr/lisa-cruz-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/informe.md",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/source.info.json",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/terms.md",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/source-page.html",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/audio.wav",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/asr/monica-bonell-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/asr/monica-bonell-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/informe.md",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/source.info.json",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/terms.md",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/source-page.html",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/audio.wav",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/asr/bonaventura-riberaygua-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/asr/bonaventura-riberaygua-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/informe.md",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/source.info.json",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/terms.md",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/source-page.html",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/audio.wav",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/asr/josep-marsal-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/asr/josep-marsal-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/informe.md",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/source.info.json",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/terms.md",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/source-page.html",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/audio.wav",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/asr/josep-maria-cases-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/asr/josep-maria-cases-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/informe.md",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/source.info.json",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/terms.md",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/source-page.html",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/audio.wav",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/asr/denisa-font-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/asr/denisa-font-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/informe.md",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/source.info.json",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/terms.md",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/source-page.html",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/audio.wav",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/asr/albert-gelabert-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/asr/albert-gelabert-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/informe.md",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/source.info.json",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/terms.md",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/source-page.html",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/audio.wav",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/asr/rosa-maria-mandico-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/asr/rosa-maria-mandico-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/informe.md",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/source.info.json",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/terms.md",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/source-page.html",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/audio.wav",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/asr/jordi-guillamet-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/asr/jordi-guillamet-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/informe.md",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/source.info.json",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/terms.md",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/source-page.html",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/audio.wav",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/asr/pere-besoli-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/asr/pere-besoli-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/informe.md",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/source.info.json",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/terms.md",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/source-page.html",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/audio.wav",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/asr/angelina-mas-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/asr/angelina-mas-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/informe.md",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/source.info.json",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/terms.md",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/source-page.html",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/audio.wav",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/asr/casimir-arajol-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/asr/casimir-arajol-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/informe.md",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/source.info.json",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/terms.md",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/source-page.html",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/audio.wav",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/asr/ramon-rossell-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/asr/ramon-rossell-base-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/genera-dossier.py",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/informe.md",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/source.info.json",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/formes.tsv",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/analitza-acustica.py",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/terms.md",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/source-page.html",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/legal-page.html",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/stream-url.txt",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/audio.wav",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/source-original.mp4",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/asr/anna-riberaygua-small-nocontext.json",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/asr/anna-riberaygua-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-033-david-montane/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-033-david-montane/informe.md",
        "proveniencia/prospeccio/lead-yt-033-david-montane/source.info.json",
        "proveniencia/prospeccio/lead-yt-033-david-montane/formes.tsv",
        "proveniencia/prospeccio/lead-yt-033-david-montane/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-033-david-montane/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-033-david-montane/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-033-david-montane/terms.md",
        "proveniencia/prospeccio/lead-yt-033-david-montane/source-page.html",
        "proveniencia/prospeccio/lead-yt-033-david-montane/legal-page.html",
        "proveniencia/prospeccio/lead-yt-033-david-montane/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-033-david-montane/audio.wav",
        "proveniencia/prospeccio/lead-yt-033-david-montane/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-033-david-montane/asr/david-montane-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-033-david-montane/asr/david-montane-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/informe.md",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/source.info.json",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/formes.tsv",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/terms.md",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/source-page.html",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/legal-page.html",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/audio.wav",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/asr/antoni-marti-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/asr/antoni-marti-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/informe.md",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/source.info.json",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/formes.tsv",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/terms.md",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/source-page.html",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/legal-page.html",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/audio.wav",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/asr/cerni-escale-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/asr/cerni-escale-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/informe.md",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/source.info.json",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/formes.tsv",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/terms.md",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/source-page.html",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/legal-page.html",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/audio.wav",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/asr/xavier-espot-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/asr/xavier-espot-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/informe.md",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/source.info.json",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/formes.tsv",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/terms.md",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/source-page.html",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/legal-page.html",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/audio.wav",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/asr/oscar-ribas-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/asr/oscar-ribas-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/informe.md",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/source.info.json",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/formes.tsv",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/terms.md",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/source-page.html",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/legal-page.html",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/audio.wav",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/asr/conxita-marsol-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/asr/conxita-marsol-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/informe.md",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/source.info.json",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/formes.tsv",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/terms.md",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/source-page.html",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/legal-page.html",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/audio.wav",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/asr/marta-roure-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/asr/marta-roure-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/informe.md",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/source.info.json",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/formes.tsv",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/terms.md",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/source-page.html",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/legal-page.html",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/audio.wav",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/asr/guillem-forne-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/asr/guillem-forne-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/informe.md",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/source.info.json",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/formes.tsv",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/terms.md",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/source-page.html",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/legal-page.html",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/audio.wav",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/asr/guillem-areny-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/asr/guillem-areny-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/informe.md",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/source.info.json",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/formes.tsv",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/terms.md",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/source-page.html",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/legal-page.html",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/audio.wav",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/asr/andreu-gonzalez-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/asr/andreu-gonzalez-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/informe.md",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/source.info.json",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/formes.tsv",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/terms.md",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/source-page.html",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/legal-page.html",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/audio.wav",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/asr/oriol-agorreta-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/asr/oriol-agorreta-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/informe.md",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/source.info.json",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/formes.tsv",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/terms.md",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/source-page.html",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/legal-page.html",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/audio.wav",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/asr/laura-casanovas-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/asr/laura-casanovas-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/informe.md",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/source.info.json",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/formes.tsv",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/terms.md",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/source-page.html",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/legal-page.html",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/audio.wav",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/asr/arnau-rius-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/asr/arnau-rius-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/informe.md",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/source.info.json",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/formes.tsv",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/terms.md",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/source-page.html",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/legal-page.html",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/audio.wav",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/asr/alberto-villagrasa-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/asr/alberto-villagrasa-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/informe.md",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/source.info.json",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/formes.tsv",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/terms.md",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/source-page.html",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/legal-page.html",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/audio.wav",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/asr/katia-ustina-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/asr/katia-ustina-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/informe.md",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/source.info.json",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/formes.tsv",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/terms.md",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/source-page.html",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/legal-page.html",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/audio.wav",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/asr/ander-mirambell-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/asr/ander-mirambell-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/informe.md",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/source.info.json",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/formes.tsv",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/terms.md",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/source-page.html",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/legal-page.html",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/audio.wav",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/asr/joan-piquet-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/asr/joan-piquet-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/informe.md",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/source.info.json",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/formes.tsv",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/terms.md",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/source-page.html",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/legal-page.html",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/audio.wav",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/asr/pau-chica-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/asr/pau-chica-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/informe.md",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/source.info.json",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/formes.tsv",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/terms.md",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/source-page.html",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/legal-page.html",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/audio.wav",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/asr/albert-vilaro-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/asr/albert-vilaro-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/informe.md",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/source.info.json",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/formes.tsv",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/terms.md",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/source-page.html",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/legal-page.html",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/audio.wav",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/asr/valenti-closa-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/asr/valenti-closa-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/informe.md",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/source.info.json",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/formes.tsv",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/terms.md",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/source-page.html",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/legal-page.html",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/audio.wav",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/asr/sonia-andorrita-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/asr/sonia-andorrita-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/informe.md",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/source.info.json",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/formes.tsv",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/terms.md",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/source-page.html",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/legal-page.html",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/audio.wav",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/asr/francesc-solana-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/asr/francesc-solana-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/informe.md",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/source.info.json",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/formes.tsv",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/terms.md",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/source-page.html",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/legal-page.html",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/audio.wav",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/asr/enric-flix-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/asr/enric-flix-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/informe.md",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/source.info.json",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/formes.tsv",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/terms.md",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/source-page.html",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/legal-page.html",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/audio.wav",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/asr/arnau-fortuny-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/asr/arnau-fortuny-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/informe.md",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/source.info.json",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/formes.tsv",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/terms.md",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/source-page.html",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/legal-page.html",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/audio.wav",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/asr/gabriel-lezkano-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/asr/gabriel-lezkano-base-nocontext.json",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/genera-dossier.py",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/informe.md",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/source.info.json",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/formes.tsv",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/cua-audicio.tsv",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/analitza-acustica.py",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/analisi-acustica.tsv",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/terms.md",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/source-page.html",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/legal-page.html",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/stream-url.txt",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/audio.wav",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/source-original.mp4",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/asr/nuria-pablos-small-nocontext.json",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/asr/nuria-pablos-base-nocontext.json",
        "proveniencia/genera-graf-prospeccio-nova.py",
        "grafo/nodes-formes-prospeccio.tsv",
        "grafo/arestes-formes-prospeccio.tsv",
        "grafo/matriu-formes-prospeccio.tsv",
        "grafo/graf-formes-prospeccio.mmd",
        "grafo/README-formes-prospeccio.md",
        "proveniencia/genera-auditoria-prospeccio-nova.py",
        "proveniencia/auditoria-prospeccio-nova.html",
        "proveniencia/genera-analisi-linguistica-prospeccio.py",
        "proveniencia/prospeccio/resum-analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-009-isidre-bartumeu/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-010-lurdes-riba/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-011-josep-dalleres/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-012-marc-forne/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-013-pere-vilanova/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-014-joan-burgues/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-015-isidre-baro/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-016-josep-areny/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-017-simo-duro/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-018-ricard-fiter/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-019-lisa-cruz/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-020-monica-bonell/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-021-bonaventura-riberaygua/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-022-josep-marsal/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-023-josep-maria-cases/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-024-denisa-font/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-025-albert-gelabert/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-026-rosa-maria-mandico/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-027-jordi-guillamet/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-028-pere-besoli/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-029-angelina-mas/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-030-casimir-arajol/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-031-ramon-rossell/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-rtva-032-anna-riberaygua/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-033-david-montane/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-034-antoni-marti/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-035-cerni-escale/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-036-xavier-espot/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-037-oscar-ribas/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-038-conxita-marsol/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-039-marta-roure/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-040-guillem-forne/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-041-guillem-areny/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-042-andreu-gonzalez/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-043-oriol-agorreta/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-044-laura-casanovas/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-047-katia-ustina/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-050-pau-chica/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-051-albert-vilaro/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-052-valenti-closa/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-053-sonia-andorrita/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-054-francesc-solana/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-055-enric-flix/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-056-arnau-fortuny/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-057-gabriel-lezkano/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-058-nuria-pablos/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-049-joan-piquet/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-048-ander-mirambell/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-046-alberto-villagrasa/analisi-linguistica.tsv",
        "proveniencia/prospeccio/lead-yt-045-arnau-rius/analisi-linguistica.tsv",
        "proveniencia/genera-auditoria-grafo-independent.py",
        "proveniencia/auditoria-grafo-independent.tsv",
        "proveniencia/genera-resum-qa-quarantena-20s-alt.py",
        "proveniencia/qa-quarantena-20s-alt-resum.tsv",
        "proveniencia/genera-auditoria-cua-quarantena.py",
        "proveniencia/auditoria-cua-quarantena-20s.tsv",
        "proveniencia/genera-auditoria-cobertura-formes.py",
        "proveniencia/auditoria-cobertura-formes.tsv",
        "proveniencia/genera-quadern-formes-representatives.py",
        "proveniencia/quadern-formes-representatives.md",
        "proveniencia/genera-cua-formes-escasses.py",
        "proveniencia/cua-audicio-formes-escasses.tsv",
        "proveniencia/genera-cua-formes-escasses-prioritaria.py",
        "proveniencia/cua-audicio-formes-escasses-prioritaria.tsv",
        "proveniencia/cua-audicio-formes-escasses-prioritaria.md",
        "proveniencia/genera-registre-audicio-formes-escasses.py",
        "proveniencia/registre-audicio-formes-escasses.tsv",
        "proveniencia/genera-guia-formes-escasses.py",
        "proveniencia/guia-audicio-formes-escasses.tsv",
        "proveniencia/analitza-acustica-formes-escasses.py",
        "proveniencia/analisi-acustica-formes-escasses.tsv",
        "proveniencia/genera-auditoria-formes-escasses.py",
        "proveniencia/auditoria-formes-escasses.html",
        "proveniencia/importa-auditoria-formes-escasses.py",
        "../auditoria-readme-titols.tsv",
        "proveniencia/sessions/sessio-05.md",
        "proveniencia/sessions/sessio-05.tsv",
        "proveniencia/sessions/sessio-06.md",
        "proveniencia/sessions/sessio-06.tsv",
        "proveniencia/quadern-audicio-global.md",
        "proveniencia/importa-auditoria.py",
        "proveniencia/actualitza-informes-consens.py",
        "proveniencia/analitza-acustica-consens.py",
        "proveniencia/genera-quadern-consens.py",
        "proveniencia/genera-json-consens-base.py",
        "proveniencia/prioritza-consens-token.py",
        "proveniencia/genera-informe-token-missing.py",
        "proveniencia/genera-json-missing-small.py",
        "proveniencia/compara-token-missing.py",
        "proveniencia/analitza-limits-paraula.py",
        "proveniencia/genera-informe-falsos-positius.py",
        "proveniencia/actualitza-informes-boundary.py",
        "proveniencia/actualitza-referencies-persistents.py",
        "proveniencia/informe-falsos-positius-boundary.md",
        "proveniencia/referencies-institucionals-casos-persistents.md",
        "proveniencia/audita-quarantena-base.py",
        "proveniencia/informe-quarantena-comparativa.py",
        "proveniencia/informe-quarantena-comparativa.md",
        "proveniencia/resegmenta-quarantena-20s.py",
        "proveniencia/genera-auditoria-quarantena-20s.py",
        "proveniencia/analitza-quarantena-20s.py",
        "proveniencia/compara-quarantena-20s.py",
        "proveniencia/analitza-acustica-quarantena-20s.py",
        "proveniencia/qa-quarantena-20s-small/pa-044__0020.txt",
        "proveniencia/qa-quarantena-20s-consens.tsv",
        "proveniencia/informe-quarantena-20s.md",
        "proveniencia/auditoria-quarantena-20s.html",
        "proveniencia/qa-quarantena-20s/pa-044-combinada.txt",
        "proveniencia/qa-quarantena-20s/pa-047-combinada.txt",
        "proveniencia/qa-quarantena-20s/pa-050-combinada.txt",
        "proveniencia/analitza-acustica-normalitzada.py",
        "proveniencia/analitza-formants-consens.py",
        "proveniencia/analitza-trajectories-formants.py",
        "proveniencia/genera-evidencia-gramatica.py",
        "proveniencia/genera-informe-cobertura-repertori.py",
        "proveniencia/actualitza-informes-inventari-formes.py",
        "proveniencia/verifica-clips-forts-greedy.py",
        "proveniencia/compara-forts-greedy.py",
        "proveniencia/informe-forts-greedy.md",
        "proveniencia/genera-auditoria-forts-triple.py",
        "proveniencia/auditoria-forts-triple.html",
        "proveniencia/genera-registre-divergencies.py",
        "proveniencia/quadern-audicio-forts-divergencies.md",
        "proveniencia/analitza-acustica-divergencies.py",
        "proveniencia/analitza-formants-qa.py",
        "proveniencia/genera-json-cua-small.py",
        "proveniencia/extrae-tokens-cua-small.py",
        "proveniencia/analitza-formants-cua-small.py",
        "grafo/genera-graf-small-token.py",
        "grafo/genera-graf-formes-completa.py",
        "grafo/trets-formes-completa.tsv",
        "grafo/arestes-parlants-formes-completa.tsv",
        "grafo/nodes-formes-completa.tsv",
        "grafo/matriu-formes-completa.tsv",
        "grafo/graf-parlants-formes-completa.mmd",
        "grafo/README-formes-completa.md",
        "grafo/genera-graf-formes-escasses.py",
        "grafo/trets-formes-escasses.tsv",
        "grafo/nodes-formes-escasses.tsv",
        "grafo/arestes-parlants-formes-escasses.tsv",
        "grafo/matriu-formes-escasses.tsv",
        "grafo/graf-parlants-formes-escasses.mmd",
        "grafo/README-formes-escasses.md",
        "grafo/informe-cobertura-repertori.md",
        "grafo/trets-small-token.tsv",
        "grafo/arestes-parlants-small-token.tsv",
        "grafo/graf-parlants-small-token.mmd",
        "grafo/matriu-formes-small-token.tsv",
        "grafo/genera-perfils-small-token.py",
        "grafo/nodes-small-token.tsv",
        "proveniencia/prioritza-formes-small-token.py",
        "proveniencia/quadern-formes-small-token.md",
        "grafo/genera-matriu-formes.py",
        "grafo/matriu-formes-linguistics.tsv",
        "proveniencia/genera-repertori-evidencia.py",
        "grafo/trets-boundary-consens.tsv",
        "grafo/arestes-parlants-boundary-consens.tsv",
        "grafo/graf-parlants-boundary-consens.mmd",
        "proveniencia/informe-token-missing.md",
        "proveniencia/quadern-audicio-consens.md",
        "proveniencia/genera-cua-equilibrada-small.py",
        "proveniencia/quadern-audicio-small-equilibrada.md",
        "proveniencia/actualitza-informes-cua-equilibrada.py",
        "proveniencia/genera-auditoria-small-equilibrada.py",
        "proveniencia/importa-auditoria-small-equilibrada.py",
        "proveniencia/genera-qa-base-equilibrada.py",
        "proveniencia/genera-mapa-persones-canonics.py",
        "proveniencia/prioritza-audicio-equilibrada.py",
        "proveniencia/quadern-audicio-equilibrada-prioritzat.md",
        "grafo/genera-graf-canonics-small.py",
        "grafo/trets-small-token-canonics.tsv",
        "grafo/arestes-parlants-small-token-canonics.tsv",
        "grafo/graf-parlants-small-token-canonics.mmd",
        "grafo/nodes-small-token-canonics.tsv",
        "grafo/matriu-formes-small-token-canonics.tsv",
        "proveniencia/compara-qa-base-equilibrada.py",
        "proveniencia/actualitza-informes-qa-equilibrada.py",
        "proveniencia/extrae-tokens-base-equilibrada.py",
        "proveniencia/analitza-formants-base-equilibrada.py",
        "proveniencia/actualitza-informes-formants-base-equilibrada.py",
        "proveniencia/actualitza-informes-prioritat-equilibrada.py",
        "proveniencia/importa-auditoria-equilibrada-master.py",
        "proveniencia/protocol-audicio-anotacio.md",
        "proveniencia/resumeix-estat-audicio.py",
        "proveniencia/resum-estat-audicio.md",
        "proveniencia/genera-qa-greedy-equilibrada.py",
        "proveniencia/genera-qa-greedy-completa.py",
        "proveniencia/compara-qa-greedy-completa.py",
        "proveniencia/qa-clips-greedy-full",
        "proveniencia/informe-qa-triple-complet.md",
        "proveniencia/prioritza-audicio-triple-completa.py",
        "proveniencia/quadern-audicio-triple-complet.md",
        "proveniencia/genera-inventari-incerteses-asr.py",
        "proveniencia/inventari-incerteses-asr.tsv",
        "proveniencia/inventari-incerteses-asr.md",
        "proveniencia/genera-cua-incerteses.py",
        "proveniencia/quadern-audicio-incerteses.md",
        "proveniencia/genera-auditoria-incerteses.py",
        "proveniencia/auditoria-incerteses.html",
        "proveniencia/genera-qa-beam.py",
        "proveniencia/qa-beam.tsv",
        "proveniencia/qa-beam",
        "proveniencia/genera-informe-candidat-rtva.py",
        "proveniencia/genera-informe-candidat-rtva-002.py",
        "proveniencia/genera-informe-candidat-rtva-003.py",
        "proveniencia/genera-graf-candidat-rtva-002.py",
        "proveniencia/genera-graf-candidat-rtva-003.py",
        "proveniencia/genera-qa-greedy-candidats-rtva.py",
        "proveniencia/segmenta-veus-candidat-rtva-002.py",
        "proveniencia/segmenta-veus-candidat-rtva-003.py",
        "proveniencia/genera-informe-candidat-rtva-004.py",
        "proveniencia/genera-informe-candidat-cg-001.py",
        "proveniencia/genera-informe-candidat-cg-002.py",
        "proveniencia/analitza-acustica-candidat-cg-002.py",
        "proveniencia/verifica-candidat-cg-002.py",
        "proveniencia/genera-informe-candidat-cg-003.py",
        "proveniencia/analitza-acustica-candidat-cg-003.py",
        "proveniencia/verifica-candidat-cg-003.py",
        "proveniencia/genera-informe-candidat-rtva-005.py",
        "proveniencia/analitza-acustica-candidat-rtva-005.py",
        "proveniencia/verifica-candidat-rtva-005.py",
        "proveniencia/genera-informe-candidat-rtva-006.py",
        "proveniencia/analitza-acustica-candidat-rtva-006.py",
        "proveniencia/verifica-candidat-rtva-006.py",
        "proveniencia/genera-informe-candidat-rtva-007.py",
        "proveniencia/analitza-acustica-candidat-rtva-007.py",
        "proveniencia/verifica-candidat-rtva-007.py",
        "proveniencia/genera-informe-candidat-rtva-008.py",
        "proveniencia/analitza-acustica-candidat-rtva-008.py",
        "proveniencia/verifica-candidat-rtva-008.py",
        "proveniencia/genera-auditoria-candidats.py",
        "proveniencia/auditoria-candidats.tsv",
        "proveniencia/auditoria-candidats.md",
        "proveniencia/genera-auditoria-candidats-completa.py",
        "proveniencia/auditoria-candidats-completa.html",
        "proveniencia/genera-cua-audicio-candidats-prioritaria.py",
        "proveniencia/cua-audicio-candidats-prioritaria.tsv",
        "proveniencia/cua-audicio-candidats-prioritaria.md",
        "proveniencia/genera-auditoria-integritat-transcripcions-candidats.py",
        "proveniencia/auditoria-integritat-transcripcions-candidats.tsv",
        "proveniencia/genera-auditoria-cua-candidats-prioritaria.py",
        "proveniencia/auditoria-cua-candidats-prioritaria.html",
        "proveniencia/importa-cua-audicio-candidats-prioritaria.py",
        "grafo/genera-graf-formes-candidats.py",
        "grafo/nodes-formes-candidats.tsv",
        "grafo/arestes-formes-candidats.tsv",
        "grafo/graf-formes-candidats.mmd",
        "grafo/README-formes-candidats.md",
        "proveniencia/genera-graf-candidat-cg-001.py",
        "proveniencia/segmenta-veus-candidat-cg-001.py",
        "proveniencia/analitza-acustica-candidat-cg-001.py",
        "proveniencia/analitza-acustica-candidats.py",
        "proveniencia/enriqueix-sessions-audicio.py",
        "proveniencia/enriqueix-sessio-01-candidats.py",
        "proveniencia/enriqueix-sessions-canoniques.py",
        "proveniencia/auditoria-cobertura-persones.py",
        "proveniencia/genera-informe-cobertura-persones.py",
        "proveniencia/auditoria-cobertura-persones.md",
        "proveniencia/genera-informe-format-audio.py",
        "proveniencia/auditoria-format-audio.md",
        "proveniencia/genera-mapa-prospeccio.py",
        "proveniencia/mapa-prospeccio.md",
        "proveniencia/genera-quadern-evidencia-gramatica.py",
        "proveniencia/quadern-evidencia-gramatica.md",
        "proveniencia/importa-auditoria-sessions-canoniques.py",
        "proveniencia/genera-guia-audicio-sessions-canoniques.py",
        "proveniencia/genera-quadern-sessions-canoniques.py",
        "proveniencia/genera-auditoria-objectiu.py",
        "proveniencia/genera-auditoria-informes.py",
        "proveniencia/actualitza-informes-sessions-canoniques.py",
        "proveniencia/actualitza-informes-repertori.py",
        "proveniencia/genera-resum-cobertura-fonts.py",
        "proveniencia/genera-auditoria-identitat-linguistica.py",
        "proveniencia/analitza-acustica-candidat-rtva-004.py",
        "proveniencia/analitza-formants-candidats.py",
        "grafo/genera-graf-acustic-candidats.py",
        "grafo/genera-graf-acustic-canonic.py",
        "grafo/genera-repertori-aplicat-canonic.py",
        "grafo/repertori-aplicat-canonic.tsv",
        "proveniencia/genera-graf-candidat-rtva-004.py",
        "proveniencia/segmenta-veus-candidat-rtva-004.py",
        "proveniencia/candidats/README.md",
        "proveniencia/candidats/lead-rtva-001/README.md",
        "proveniencia/candidats/lead-rtva-001/source-url.txt",
        "proveniencia/candidats/lead-rtva-002-ian-moya/README.md",
        "proveniencia/candidats/lead-rtva-002-ian-moya/source-url.txt",
        "proveniencia/candidats/lead-rtva-002-ian-moya/audio-original.mp3",
        "proveniencia/candidats/lead-rtva-002-ian-moya/audio.wav",
        "proveniencia/candidats/lead-rtva-002-ian-moya/informe.md",
        "proveniencia/candidats/lead-rtva-002-ian-moya/comparacio-asr.md",
        "proveniencia/candidats/lead-rtva-002-ian-moya/formes.tsv",
        "proveniencia/candidats/lead-rtva-002-ian-moya/formes-consens.tsv",
        "proveniencia/candidats/lead-rtva-002-ian-moya/formes-clips.tsv",
        "proveniencia/candidats/lead-rtva-002-ian-moya/quadern-clips-formes.md",
        "proveniencia/candidats/lead-rtva-002-ian-moya/auditoria.html",
        "proveniencia/candidats/lead-rtva-002-ian-moya/graf/README.md",
        "proveniencia/candidats/lead-rtva-002-ian-moya/graf/nodes.tsv",
        "proveniencia/candidats/lead-rtva-002-ian-moya/graf/arestes.tsv",
        "proveniencia/candidats/lead-rtva-002-ian-moya/graf/trets.tsv",
        "proveniencia/candidats/lead-rtva-002-ian-moya/graf/graf.mmd",
        "proveniencia/candidats/lead-rtva-002-ian-moya/segmentacio-veus.md",
        "proveniencia/candidats/lead-rtva-002-ian-moya/segments-speaker-provisional.tsv",
        "proveniencia/candidats/lead-rtva-002-ian-moya/formes-ian-provisional.tsv",
        "proveniencia/candidats/lead-rtva-002-ian-moya/asr/ian-moya.txt",
        "proveniencia/candidats/lead-rtva-002-ian-moya/asr/ian-moya.vtt",
        "proveniencia/candidats/lead-rtva-002-ian-moya/asr/ian-moya.json",
        "proveniencia/candidats/lead-rtva-002-ian-moya/asr/ian-moya-base.txt",
        "proveniencia/candidats/lead-rtva-002-ian-moya/asr/ian-moya-base.vtt",
        "proveniencia/candidats/lead-rtva-002-ian-moya/asr/ian-moya-base.json",
        "proveniencia/candidats/lead-rtva-002-ian-moya/clips",
        "proveniencia/candidats/lead-rtva-002-ian-moya/informe-qa-greedy.md",
        "proveniencia/candidats/lead-rtva-002-ian-moya/qa-greedy.tsv",
        "proveniencia/candidats/lead-rtva-002-ian-moya/qa-greedy",
        "proveniencia/candidats/lead-rtva-003-dj-neura/README.md",
        "proveniencia/candidats/lead-rtva-003-dj-neura/source-url.txt",
        "proveniencia/candidats/lead-rtva-003-dj-neura/audio-original.mp3",
        "proveniencia/candidats/lead-rtva-003-dj-neura/audio.wav",
        "proveniencia/candidats/lead-rtva-003-dj-neura/informe.md",
        "proveniencia/candidats/lead-rtva-003-dj-neura/comparacio-asr.md",
        "proveniencia/candidats/lead-rtva-003-dj-neura/formes.tsv",
        "proveniencia/candidats/lead-rtva-003-dj-neura/formes-consens.tsv",
        "proveniencia/candidats/lead-rtva-003-dj-neura/formes-clips.tsv",
        "proveniencia/candidats/lead-rtva-003-dj-neura/quadern-clips-formes.md",
        "proveniencia/candidats/lead-rtva-003-dj-neura/auditoria.html",
        "proveniencia/candidats/lead-rtva-003-dj-neura/graf/README.md",
        "proveniencia/candidats/lead-rtva-003-dj-neura/graf/nodes.tsv",
        "proveniencia/candidats/lead-rtva-003-dj-neura/graf/arestes.tsv",
        "proveniencia/candidats/lead-rtva-003-dj-neura/graf/trets.tsv",
        "proveniencia/candidats/lead-rtva-003-dj-neura/graf/graf.mmd",
        "proveniencia/candidats/lead-rtva-003-dj-neura/asr/dj-neura.txt",
        "proveniencia/candidats/lead-rtva-003-dj-neura/asr/dj-neura.vtt",
        "proveniencia/candidats/lead-rtva-003-dj-neura/asr/dj-neura.json",
        "proveniencia/candidats/lead-rtva-003-dj-neura/asr/dj-neura-base.txt",
        "proveniencia/candidats/lead-rtva-003-dj-neura/asr/dj-neura-base.vtt",
        "proveniencia/candidats/lead-rtva-003-dj-neura/asr/dj-neura-base.json",
        "proveniencia/candidats/lead-rtva-003-dj-neura/clips",
        "proveniencia/candidats/lead-rtva-003-dj-neura/informe-qa-greedy.md",
        "proveniencia/candidats/lead-rtva-003-dj-neura/qa-greedy.tsv",
        "proveniencia/candidats/lead-rtva-003-dj-neura/qa-greedy",
        "proveniencia/candidats/lead-rtva-003-dj-neura/segmentacio-veus.md",
        "proveniencia/candidats/lead-rtva-003-dj-neura/segments-speaker-provisional.tsv",
        "proveniencia/candidats/lead-rtva-003-dj-neura/formes-dj-neura-provisional.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/README.md",
        "proveniencia/candidats/lead-rtva-004-joan-mico/source-url.txt",
        "proveniencia/candidats/lead-rtva-004-joan-mico/audio-original.mp3",
        "proveniencia/candidats/lead-rtva-004-joan-mico/audio.wav",
        "proveniencia/candidats/lead-rtva-004-joan-mico/informe.md",
        "proveniencia/candidats/lead-rtva-004-joan-mico/analisi-acustica.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/analisi-acustica.md",
        "proveniencia/candidats/lead-rtva-004-joan-mico/formants.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/formants.md",
        "proveniencia/candidats/lead-rtva-004-joan-mico/comparacio-asr.md",
        "proveniencia/candidats/lead-rtva-004-joan-mico/formes.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/formes-consens.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/formes-clips.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/quadern-clips-formes.md",
        "proveniencia/candidats/lead-rtva-004-joan-mico/auditoria.html",
        "proveniencia/candidats/lead-rtva-004-joan-mico/graf/README.md",
        "proveniencia/candidats/lead-rtva-004-joan-mico/graf/nodes.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/graf/arestes.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/graf/trets.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/graf/graf.mmd",
        "proveniencia/candidats/lead-rtva-004-joan-mico/asr/joan-mico.txt",
        "proveniencia/candidats/lead-rtva-004-joan-mico/asr/joan-mico.vtt",
        "proveniencia/candidats/lead-rtva-004-joan-mico/asr/joan-mico.json",
        "proveniencia/candidats/lead-rtva-004-joan-mico/asr/joan-mico-base.txt",
        "proveniencia/candidats/lead-rtva-004-joan-mico/asr/joan-mico-base.vtt",
        "proveniencia/candidats/lead-rtva-004-joan-mico/asr/joan-mico-base.json",
        "proveniencia/candidats/lead-rtva-004-joan-mico/clips",
        "proveniencia/candidats/lead-rtva-004-joan-mico/informe-qa-greedy.md",
        "proveniencia/candidats/lead-rtva-004-joan-mico/qa-greedy.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/qa-greedy",
        "proveniencia/candidats/lead-rtva-004-joan-mico/segmentacio-veus.md",
        "proveniencia/candidats/lead-rtva-004-joan-mico/segments-speaker-provisional.tsv",
        "proveniencia/candidats/lead-rtva-004-joan-mico/formes-joan-mico-provisional.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/README.md",
        "proveniencia/candidats/lead-cg-001-xavier-espot/source-url.txt",
        "proveniencia/candidats/lead-cg-001-xavier-espot/audio.wav",
        "proveniencia/candidats/lead-cg-001-xavier-espot/informe.md",
        "proveniencia/candidats/lead-cg-001-xavier-espot/analisi-acustica.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/analisi-acustica.md",
        "proveniencia/candidats/lead-cg-001-xavier-espot/formants.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/formants.md",
        "grafo/nodes-acustic-candidats.tsv",
        "grafo/arestes-acustic-candidats.tsv",
        "grafo/graf-acustic-candidats.mmd",
        "grafo/README-acustic-candidats.md",
        "grafo/nodes-acustic-canonic.tsv",
        "grafo/arestes-acustic-canonic.tsv",
        "grafo/graf-acustic-canonic.mmd",
        "grafo/README-acustic-canonic.md",
        "proveniencia/candidats/lead-cg-001-xavier-espot/comparacio-asr.md",
        "proveniencia/candidats/lead-cg-001-xavier-espot/formes.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/formes-consens.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/formes-clips.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/quadern-clips-formes.md",
        "proveniencia/candidats/lead-cg-001-xavier-espot/auditoria.html",
        "proveniencia/candidats/lead-cg-001-xavier-espot/graf/README.md",
        "proveniencia/candidats/lead-cg-001-xavier-espot/graf/nodes.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/graf/arestes.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/graf/trets.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/graf/graf.mmd",
        "proveniencia/candidats/lead-cg-001-xavier-espot/asr/xavier-espot.txt",
        "proveniencia/candidats/lead-cg-001-xavier-espot/asr/xavier-espot.vtt",
        "proveniencia/candidats/lead-cg-001-xavier-espot/asr/xavier-espot.json",
        "proveniencia/candidats/lead-cg-001-xavier-espot/asr/xavier-espot-base.txt",
        "proveniencia/candidats/lead-cg-001-xavier-espot/asr/xavier-espot-base.vtt",
        "proveniencia/candidats/lead-cg-001-xavier-espot/asr/xavier-espot-base.json",
        "proveniencia/candidats/lead-cg-001-xavier-espot/clips",
        "proveniencia/candidats/lead-cg-001-xavier-espot/informe-qa-greedy.md",
        "proveniencia/candidats/lead-cg-001-xavier-espot/qa-greedy.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/qa-greedy",
        "proveniencia/candidats/lead-cg-001-xavier-espot/segmentacio-veus.md",
        "proveniencia/candidats/lead-cg-001-xavier-espot/segments-speaker-provisional.tsv",
        "proveniencia/candidats/lead-cg-001-xavier-espot/formes-xavier-espot-provisional.tsv",
        "proveniencia/candidats/lead-cg-002-pere-lopez/README.md",
        "proveniencia/candidats/lead-cg-002-pere-lopez/source-url.txt",
        "proveniencia/candidats/lead-cg-002-pere-lopez/audio.wav",
        "proveniencia/candidats/lead-cg-002-pere-lopez/informe.md",
        "proveniencia/candidats/lead-cg-002-pere-lopez/analisi-acustica.tsv",
        "proveniencia/candidats/lead-cg-002-pere-lopez/analisi-acustica.md",
        "proveniencia/candidats/lead-cg-002-pere-lopez/comparacio-asr.md",
        "proveniencia/candidats/lead-cg-002-pere-lopez/formes.tsv",
        "proveniencia/candidats/lead-cg-002-pere-lopez/formes-consens.tsv",
        "proveniencia/candidats/lead-cg-002-pere-lopez/formes-clips.tsv",
        "proveniencia/candidats/lead-cg-002-pere-lopez/quadern-clips-formes.md",
        "proveniencia/candidats/lead-cg-002-pere-lopez/auditoria.html",
        "proveniencia/candidats/lead-cg-002-pere-lopez/asr/pere-lopez.txt",
        "proveniencia/candidats/lead-cg-002-pere-lopez/asr/pere-lopez.vtt",
        "proveniencia/candidats/lead-cg-002-pere-lopez/asr/pere-lopez.json",
        "proveniencia/candidats/lead-cg-002-pere-lopez/asr/pere-lopez-base.txt",
        "proveniencia/candidats/lead-cg-002-pere-lopez/asr/pere-lopez-base.vtt",
        "proveniencia/candidats/lead-cg-002-pere-lopez/asr/pere-lopez-base.json",
        "proveniencia/candidats/lead-cg-002-pere-lopez/clips",
        "proveniencia/candidats/lead-cg-003-roser-sune/README.md",
        "proveniencia/candidats/lead-cg-003-roser-sune/source-url.txt",
        "proveniencia/candidats/lead-cg-003-roser-sune/audio.wav",
        "proveniencia/candidats/lead-cg-003-roser-sune/audio-extracte-120.wav",
        "proveniencia/candidats/lead-cg-003-roser-sune/informe.md",
        "proveniencia/candidats/lead-cg-003-roser-sune/analisi-acustica.tsv",
        "proveniencia/candidats/lead-cg-003-roser-sune/analisi-acustica.md",
        "proveniencia/candidats/lead-cg-003-roser-sune/comparacio-asr.md",
        "proveniencia/candidats/lead-cg-003-roser-sune/formes.tsv",
        "proveniencia/candidats/lead-cg-003-roser-sune/formes-consens.tsv",
        "proveniencia/candidats/lead-cg-003-roser-sune/formes-clips.tsv",
        "proveniencia/candidats/lead-cg-003-roser-sune/quadern-clips-formes.md",
        "proveniencia/candidats/lead-cg-003-roser-sune/auditoria.html",
        "proveniencia/candidats/lead-cg-003-roser-sune/asr/roser-sune-full.txt",
        "proveniencia/candidats/lead-cg-003-roser-sune/asr/roser-sune-full.vtt",
        "proveniencia/candidats/lead-cg-003-roser-sune/asr/roser-sune-full.json",
        "proveniencia/candidats/lead-cg-003-roser-sune/asr/roser-sune-full-base.txt",
        "proveniencia/candidats/lead-cg-003-roser-sune/asr/roser-sune-full-base.vtt",
        "proveniencia/candidats/lead-cg-003-roser-sune/asr/roser-sune-full-base.json",
        "proveniencia/candidats/lead-cg-003-roser-sune/clips",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/README.md",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/source-url.txt",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/audio-original.mp3",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/audio.wav",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/informe.md",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/analisi-acustica.tsv",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/analisi-acustica.md",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/comparacio-asr.md",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/formes.tsv",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/formes-consens.tsv",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/formes-clips.tsv",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/quadern-clips-formes.md",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/auditoria.html",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/asr/carine-montaner.txt",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/asr/carine-montaner.vtt",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/asr/carine-montaner.json",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/asr/carine-montaner-base.txt",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/asr/carine-montaner-base.vtt",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/asr/carine-montaner-base.json",
        "proveniencia/candidats/lead-rtva-005-carine-montaner/clips",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/README.md",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/source-url.txt",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/audio-original.mp3",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/audio.wav",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/informe.md",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/analisi-acustica.tsv",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/analisi-acustica.md",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/comparacio-asr.md",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/formes.tsv",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/formes-consens.tsv",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/formes-clips.tsv",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/quadern-clips-formes.md",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/auditoria.html",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/asr/jaume-tomas.txt",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/asr/jaume-tomas.vtt",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/asr/jaume-tomas.json",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/asr/jaume-tomas-base.txt",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/asr/jaume-tomas-base.vtt",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/asr/jaume-tomas-base.json",
        "proveniencia/candidats/lead-rtva-006-jaume-tomas/clips",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/README.md",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/source-url.txt",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/audio-original.mp3",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/audio.wav",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/informe.md",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/analisi-acustica.tsv",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/analisi-acustica.md",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/comparacio-asr.md",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/formes.tsv",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/formes-consens.tsv",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/formes-clips.tsv",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/quadern-clips-formes.md",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/auditoria.html",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/asr/robert-guirao.txt",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/asr/robert-guirao.vtt",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/asr/robert-guirao.json",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/asr/robert-guirao-base.txt",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/asr/robert-guirao-base.vtt",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/asr/robert-guirao-base.json",
        "proveniencia/candidats/lead-rtva-007-robert-guirao/clips",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/README.md",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/source-url.txt",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/audio-original.mp3",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/audio.wav",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/informe.md",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/analisi-acustica.tsv",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/analisi-acustica.md",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/comparacio-asr.md",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/formes.tsv",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/formes-consens.tsv",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/formes-clips.tsv",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/quadern-clips-formes.md",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/auditoria.html",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/asr/mireia-pedescoll.txt",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/asr/mireia-pedescoll.vtt",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/asr/mireia-pedescoll.json",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/asr/mireia-pedescoll-base.txt",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/asr/mireia-pedescoll-base.vtt",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/asr/mireia-pedescoll-base.json",
        "proveniencia/candidats/lead-rtva-008-mireia-pedescoll/clips",
        "proveniencia/candidats/lead-rtva-002-ian-moya/clips",
        "proveniencia/candidats/lead-rtva-001/audio.wav",
        "proveniencia/analitza-stereo-candidat.py",
        "proveniencia/candidats/lead-rtva-001/audio-stereo.wav",
        "proveniencia/candidats/lead-rtva-001/stereo-canals.md",
        "proveniencia/candidats/lead-rtva-001/asr/joan-verdu.txt",
        "proveniencia/candidats/lead-rtva-001/asr/joan-verdu.vtt",
        "proveniencia/candidats/lead-rtva-001/asr/joan-verdu.json",
        "proveniencia/candidats/lead-rtva-001/asr/joan-verdu-base.txt",
        "proveniencia/candidats/lead-rtva-001/asr/joan-verdu-base.vtt",
        "proveniencia/candidats/lead-rtva-001/asr/joan-verdu-base.json",
        "proveniencia/compara-candidat-rtva.py",
        "proveniencia/candidats/lead-rtva-001/formes-consens.tsv",
        "proveniencia/candidats/lead-rtva-001/comparacio-asr.md",
        "proveniencia/candidats/lead-rtva-001/formes.tsv",
        "proveniencia/candidats/lead-rtva-001/informe.md",
        "proveniencia/analitza-clusters-veus-candidat.py",
        "proveniencia/candidats/lead-rtva-001/segments-clusters.tsv",
        "proveniencia/candidats/lead-rtva-001/clusters-veus.md",
        "proveniencia/segmenta-veus-candidat.py",
        "proveniencia/candidats/lead-rtva-001/segments-speaker-provisional.tsv",
        "proveniencia/candidats/lead-rtva-001/formes-joan-provisional.tsv",
        "proveniencia/candidats/lead-rtva-001/segmentacio-veus.md",
        "proveniencia/genera-clips-candidat-rtva.py",
        "proveniencia/candidats/lead-rtva-001/formes-joan-clips.tsv",
        "proveniencia/candidats/lead-rtva-001/quadern-clips-formes.md",
        "proveniencia/genera-auditoria-candidat-rtva.py",
        "proveniencia/candidats/lead-rtva-001/auditoria.html",
        "proveniencia/analitza-formants-candidat-rtva.py",
        "proveniencia/genera-graf-candidat-rtva.py",
        "proveniencia/candidats/lead-rtva-001/formants.tsv",
        "proveniencia/candidats/lead-rtva-001/formants.md",
        "proveniencia/candidats/lead-rtva-001/graf/README.md",
        "proveniencia/candidats/lead-rtva-001/graf/nodes.tsv",
        "proveniencia/candidats/lead-rtva-001/graf/arestes.tsv",
        "proveniencia/candidats/lead-rtva-001/graf/trets.tsv",
        "proveniencia/candidats/lead-rtva-001/graf/graf.mmd",
        "proveniencia/candidats/lead-rtva-001/clips",
        "proveniencia/compara-qa-greedy-equilibrada.py",
        "proveniencia/actualitza-informes-qa-triple-equilibrada.py",
        "proveniencia/qa-equilibrada-greedy.tsv",
        "proveniencia/qa-equilibrada-greedy",
        "proveniencia/informe-qa-equilibrada-triple.md",
        "grafo/genera-graf-triple-full.py",
        "grafo/trets-triple-full.tsv",
        "grafo/arestes-parlants-triple-full.tsv",
        "grafo/graf-parlants-triple-full.mmd",
        "grafo/nodes-triple-full.tsv",
        "grafo/matriu-formes-triple-full.tsv",
        "proveniencia/analitza-trajectories-base-equilibrada.py",
        "proveniencia/actualitza-informes-trajectories-base-equilibrada.py",
        "proveniencia/analisi-trajectories-base-equilibrada.tsv",
        "proveniencia/resum-trajectories-base-equilibrada.tsv",
        "proveniencia/qa-equilibrada-base-tokens.tsv",
        "proveniencia/qa-equilibrada-base-token-occurrences.tsv",
        "proveniencia/analisi-formants-base-equilibrada.tsv",
        "proveniencia/resum-formants-base-equilibrada.tsv",
        "proveniencia/qa-equilibrada-base.tsv",
        "proveniencia/qa-equilibrada-consens.tsv",
        "proveniencia/informe-qa-equilibrada.md",
        "proveniencia/qa-equilibrada-base",
        "proveniencia/auditoria-small-equilibrada.html",
    ]:
        if not (ROOT / rel).exists():
            errors.append(f"falta artefacte {rel}")
    full_audit = (PROV / "auditoria-cua.html").read_text(encoding="utf-8") if (PROV / "auditoria-cua.html").exists() else ""
    if "const items=" not in full_audit or "anotacions-audicio-cua.tsv" not in full_audit:
        errors.append("auditoria-cua.html no sembla contenir la cua completa")
    global_audit = (PROV / "auditoria-global.html").read_text(encoding="utf-8") if (PROV / "auditoria-global.html").exists() else ""
    if "const allItems=" not in global_audit or "anotacions-auditoria-global.tsv" not in global_audit or global_audit.count('"id":') != 780:
        errors.append("auditoria-global.html no confirma els 780 clips canònics i candidats")
    global_quadern = (PROV / "quadern-audicio-global.md").read_text(encoding="utf-8") if (PROV / "quadern-audicio-global.md").exists() else ""
    if "780 clips" not in global_quadern or "11 candidats" not in global_quadern:
        errors.append("quadern-audicio-global.md no declara els 780 clips i els 11 candidats")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK corpus independent: 66 registres · 60 persones canòniques · 656 intervals/clips · 2.310 cel·les · hashes vàlids")
    return 0


if __name__ == "__main__":
    sys.exit(main())
