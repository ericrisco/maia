"""Compara marcadors i formes entre parlants del subcorpus independent.

No decideix que una forma sigui andorrana. Només compta en quantes mostres
apareix, separant candidats compartits d'errors o idiolectes.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict
from itertools import combinations
import csv
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
FORMS = [
    "bé",
    "de fet",
    "és a dir",
    "aleshores",
    "evidentment",
    "diguem",
    "crec",
    "bueno",
    "clar",
    "vull dir",
    "o sigui",
    "llavors",
    "a veure",
    "aviam",
    "doncs",
    "perquè",
    "a nivell",
    "tirar endavant",
    "ensenyança",
    "reformeta",
]


def occurrences(text: str, form: str) -> int:
    return len(re.findall(r"(?i)(?<!\w)" + re.escape(form) + r"(?!\w)", text))


def main() -> None:
    excluded = set()
    exclusions = ROOT / "proveniencia" / "qa-exclusions.tsv"
    if exclusions.exists():
        with exclusions.open(encoding="utf-8", newline="") as handle:
            excluded = {row["id_persona"] for row in csv.DictReader(handle, delimiter="\t") if row.get("estat") == "quarantena-asr"}
    pieces = {}
    for path in sorted((ROOT / "transcripcions").glob("pa-*.txt")):
        if path.name.endswith("-marcada.txt") or path.stem in excluded:
            continue
        pieces[path.stem] = path.read_text(encoding="utf-8")
    out = ROOT / "grafo" / "trets.tsv"
    edges = ROOT / "grafo" / "arestes-auto.tsv"
    audit = ROOT / "grafo" / "auditoria-formes.tsv"
    with out.open("w", encoding="utf-8") as handle:
        handle.write("forma\tpeces\tparlants\tcomptatge_total\tveredicte\n")
        edge_rows = []
        for form in FORMS:
            counts = {pid: occurrences(text, form) for pid, text in pieces.items()}
            active = {pid: n for pid, n in counts.items() if n}
            verdict = "candidat compartit" if len(active) >= 3 else "pendent"
            handle.write(
                f"{form}\t{len(active)}\t{','.join(sorted(active))}\t{sum(active.values())}\t{verdict}\n"
            )
            if len(active) >= 3:
                ascii_form = "".join(
                    char
                    for char in unicodedata.normalize("NFD", form.lower())
                    if not unicodedata.combining(char)
                )
                trait = "trait-" + re.sub(r"[^a-z0-9]+", "-", ascii_form).strip("-")
                edge_rows.extend((pid, trait, "usa", str(n), "recompte ASR; revisió auditiva pendent") for pid, n in active.items())
    with edges.open("w", encoding="utf-8") as handle:
        handle.write("origen\tdesti\trelacio\tpes\tevidencia\n")
        for row in edge_rows:
            handle.write("\t".join(row) + "\n")

    # A second, stricter view keeps only forms present in both ASR passes.
    # It remains provisional until a human checks the corresponding WAV.
    cross_path = ROOT / "proveniencia" / "auditoria-creuada-asr.tsv"
    consensus = {form: [] for form in FORMS}
    consensus_counts = {form: 0 for form in FORMS}
    if cross_path.exists():
        with cross_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                if row.get("id_persona") in excluded:
                    continue
                if row.get("consens_dos_asr") == "sí":
                    consensus.setdefault(row["forma"], []).append(row["id_persona"])
                    consensus_counts[row["forma"]] += min(
                        int(row.get("recompte_small", 0)), int(row.get("recompte_base", 0))
                    )
    consensus_traits = ROOT / "grafo" / "trets-consens.tsv"
    consensus_edges = ROOT / "grafo" / "arestes-consens-asr.tsv"
    with consensus_traits.open("w", encoding="utf-8") as handle_traits, consensus_edges.open(
        "w", encoding="utf-8"
    ) as handle_edges:
        handle_traits.write("forma\tparlants\tcomptatge_total\tveredicte\n")
        handle_edges.write("origen\tdesti\trelacio\tpes\tevidencia\n")
        for form in FORMS:
            active = sorted(set(consensus.get(form, [])))
            handle_traits.write(
                f"{form}\t{','.join(active)}\t{consensus_counts.get(form, 0)}\t"
                f"{'consens textual; revisió auditiva pendent' if len(active) >= 3 else 'pendent'}\n"
            )
            if len(active) >= 3:
                ascii_form = "".join(
                    char
                    for char in unicodedata.normalize("NFD", form.lower())
                    if not unicodedata.combining(char)
                )
                trait = "trait-" + re.sub(r"[^a-z0-9]+", "-", ascii_form).strip("-")
                for pid in active:
                    handle_edges.write(
                        f"{pid}\t{trait}\tusa\t1\tconsens textual entre dos ASR; revisió auditiva pendent\n"
                    )

    speaker_forms = defaultdict(set)
    for form, people in consensus.items():
        if len(set(people)) < 3:
            continue
        for pid in set(people):
            speaker_forms[pid].add(form)
    speaker_edges = ROOT / "grafo" / "arestes-parlants-consens.tsv"
    with speaker_edges.open("w", encoding="utf-8") as handle:
        handle.write("origen\tdesti\trelacio\tpes\tformes_compartides\tevidencia\n")
        for left, right in combinations(sorted(speaker_forms), 2):
            shared = sorted(speaker_forms[left] & speaker_forms[right])
            if len(shared) < 3:
                continue
            handle.write(
                f"{left}\t{right}\tsemblança textual provisional\t{len(shared)}\t"
                f"{','.join(shared)}\tconsens entre dos ASR; revisió auditiva pendent\n"
            )
    mermaid = ROOT / "grafo" / "graf-parlants-consens.mmd"
    with mermaid.open("w", encoding="utf-8") as handle:
        handle.write("flowchart LR\n")
        for pid in sorted(speaker_forms):
            handle.write(f"  {pid.replace('-', '')}[\"{pid}\"]\n")
        for left, right in combinations(sorted(speaker_forms), 2):
            shared = sorted(speaker_forms[left] & speaker_forms[right])
            if len(shared) >= 5:
                handle.write(
                    f"  {left.replace('-', '')} -->|{len(shared)} formes| {right.replace('-', '')}\n"
                )

    # Add time-localized evidence so a human can audit the candidate directly
    # against the audio.  We keep only the first few segment hits per speaker;
    # the full counts remain in trets.tsv.
    with audit.open("w", encoding="utf-8") as handle:
        handle.write("forma\tparlant\tocurrencies\tsegments_temporals\tconf_min_segment\tprioritat\n")
        for form in FORMS:
            pattern = re.compile(r"(?i)(?<!\w)" + re.escape(form) + r"(?!\w)")
            for pid in sorted(pieces):
                data = json.loads((ROOT / "transcripcions" / f"{pid}.json").read_text())
                hits = []
                confs = []
                for segment in data["transcription"]:
                    if pattern.search(segment.get("text", "")):
                        start = segment["offsets"]["from"] / 1000
                        end = segment["offsets"]["to"] / 1000
                        hits.append(f"{start:.2f}-{end:.2f}")
                        ps = [float(token["p"]) for token in segment["tokens"] if re.search(r"\w", token["text"])]
                        if ps:
                            confs.append(min(ps))
                if hits:
                    minimum = min(confs) if confs else 1.0
                    priority = "alta" if minimum < 0.55 else "normal"
                    handle.write(
                        f"{form}\t{pid}\t{len(hits)}\t{','.join(hits[:8])}\t{minimum:.3f}\t{priority}\n"
                    )

    # Keep the node table closed under the generated edges.  The hand-curated
    # rows stay intact; regenerated traits are appended with their observed
    # speaker IDs and an explicit provisional status.
    nodes = ROOT / "grafo" / "nodes.tsv"
    existing = []
    existing_ids = set()
    if nodes.exists():
        with nodes.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                existing.append(row)
                existing_ids.add(row["id"])
    labels = {form: " ".join(form.split()) for form in FORMS}
    generated_traits = {}
    for form in FORMS:
        ascii_form = "".join(
            char
            for char in unicodedata.normalize("NFD", form.lower())
            if not unicodedata.combining(char)
        )
        trait = "trait-" + re.sub(r"[^a-z0-9]+", "-", ascii_form).strip("-")
        active = [pid for pid, text in pieces.items() if occurrences(text, form)]
        generated_traits[trait] = active
        if len(active) >= 3 and trait not in existing_ids:
            existing.append({
                "id": trait,
                "tipus": "tret",
                "etiqueta": labels[form],
                "font_ref": ",".join(sorted(active)),
                "notes": "candidat compartit; recompte ASR pendent de revisió auditiva",
            })
            existing_ids.add(trait)
    for row in existing:
        active = generated_traits.get(row.get("id"))
        if active is not None and row.get("tipus") == "tret":
            row["font_ref"] = ",".join(sorted(active))
    with nodes.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "tipus", "etiqueta", "font_ref", "notes"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(existing)
    print(f"{len(pieces)} parlants · {len(FORMS)} formes · {out}")


if __name__ == "__main__":
    main()
