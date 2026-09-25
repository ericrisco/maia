"""Genera una cua auditiva equilibrada de 100 tokens small.

La cua cobreix cada parlant que té almenys una ocurrència tokenitzada,
reparteix les 20 formes i conserva les mesures instrumentals disponibles.
Les columnes humanes es deixen buides expressament: només l'escolta pot
convertir una coincidència ASR en una decisió lingüística.
"""

from collections import Counter, defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OCC = PROV / "qa-cua-small-token-occurrences.tsv"
FORMANTS = PROV / "analisi-formants-cua-small.tsv"
OUT = PROV / "cua-audicio-small-equilibrada.tsv"
MD = PROV / "quadern-audicio-small-equilibrada.md"
PRIOR = PROV / "prioritat-formes-small-token.tsv"


def read(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def prob(row):
    try:
        return float(row["prob_min"])
    except (ValueError, TypeError):
        return -1.0


def choose(rows):
    # Stable ordering keeps the queue reproducible when probabilities tie.
    rows = sorted(rows, key=lambda r: (-prob(r), float(r["absolute_start_s"]), int(r["occurrence"])))
    selected = []
    selected_keys = set()
    by_person = Counter()
    by_form = Counter()

    def add(row):
        key = (row["id_persona"], row["forma"], row["clip"], row["occurrence"])
        if key in selected_keys:
            return False
        selected_keys.add(key)
        selected.append(row)
        by_person[row["id_persona"]] += 1
        by_form[row["forma"]] += 1
        return True

    # First pass: one highest-confidence occurrence for every active speaker.
    people = defaultdict(list)
    for row in rows:
        people[row["id_persona"]].append(row)
    for person in sorted(people):
        add(max(people[person], key=lambda r: (prob(r), -float(r["absolute_start_s"]), -int(r["occurrence"]))))

    # Rebalance the mandatory one-per-speaker set. If a frequent form dominates,
    # replace one occurrence by another form from the same speaker, accepting the
    # smallest confidence loss. This keeps speaker coverage while avoiding a queue
    # made almost entirely of the most common lexical items.
    for _ in range(300):
        over = max(by_form, key=by_form.get)
        if by_form[over] <= 7:
            break
        best = None
        for index, current in enumerate(selected):
            if current["forma"] != over:
                continue
            old_key = (current["id_persona"], current["forma"], current["clip"], current["occurrence"])
            for alternate in people[current["id_persona"]]:
                alternate_key = (alternate["id_persona"], alternate["forma"], alternate["clip"], alternate["occurrence"])
                if alternate["forma"] == over or alternate_key in selected_keys:
                    continue
                score = (by_form[alternate["forma"]], prob(current) - prob(alternate))
                if best is None or score < best[0]:
                    best = (score, index, old_key, alternate_key, alternate)
        if best is None:
            break
        _, index, old_key, alternate_key, alternate = best
        selected_keys.remove(old_key)
        selected_keys.add(alternate_key)
        by_form[selected[index]["forma"]] -= 1
        by_form[alternate["forma"]] += 1
        selected[index] = alternate

    # Ensure every form appears before filling the remaining places. Prefer a
    # second token from a speaker with only one selected row.
    while len(selected) < min(100, len(rows)) and any(by_form[r["forma"]] == 0 for r in rows):
        candidates = [r for r in rows if by_form[r["forma"]] == 0 and (r["id_persona"], r["forma"], r["clip"], r["occurrence"]) not in selected_keys]
        if not candidates:
            break
        under_cap = [r for r in candidates if by_person[r["id_persona"]] < 2]
        pool = under_cap or candidates
        add(max(pool, key=lambda r: (prob(r), -by_person[r["id_persona"]], -float(r["absolute_start_s"]))))

    # Fill the queue by form coverage first, then confidence. A soft cap of two
    # per speaker prevents the queue from being dominated by prolific voices.
    while len(selected) < min(100, len(rows)):
        candidates = [r for r in rows if (r["id_persona"], r["forma"], r["clip"], r["occurrence"]) not in selected_keys]
        if not candidates:
            break
        under_cap = [r for r in candidates if by_person[r["id_persona"]] < 2]
        pool = under_cap or candidates
        pool = sorted(pool, key=lambda r: (by_form[r["forma"]], by_person[r["id_persona"]], -prob(r), float(r["absolute_start_s"])))
        add(pool[0])
    return selected, by_person, by_form


def main():
    rows = read(OCC)
    acoustic = {(r["id_persona"], r["forma"], r["clip"], r["occurrence"]): r for r in read(FORMANTS)}
    priorities = {r["forma"]: r["prioritat"] for r in read(PRIOR)}
    selected, by_person, by_form = choose(rows)
    if len(selected) != 100:
        raise SystemExit(f"la cua equilibrada té {len(selected)} files, no 100")
    if len(by_person) != 63 or len(by_form) != 20:
        raise SystemExit(f"cobertura inesperada: {len(by_person)} persones, {len(by_form)} formes")

    fields = ["ordre", "id_persona", "forma", "clip", "prob_min", "absolute_start_s", "absolute_end_s", "text", "f0_hz", "f1_hz", "f2_hz", "f3_hz", "prioritat", "decisio_auditiva", "variant_transcrita", "trets_fonetica", "observacions_prosodia", "nota_audicio"]
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for order, row in enumerate(sorted(selected, key=lambda r: (r["id_persona"], float(r["absolute_start_s"]), r["forma"])), 1):
            a = acoustic.get((row["id_persona"], row["forma"], row["clip"], row["occurrence"]), {})
            writer.writerow({
                "ordre": order,
                "id_persona": row["id_persona"], "forma": row["forma"], "clip": row["clip"],
                "prob_min": row["prob_min"], "absolute_start_s": row["absolute_start_s"], "absolute_end_s": row["absolute_end_s"], "text": row["text"],
                "f0_hz": a.get("f0_hz", ""), "f1_hz": a.get("f1_hz", ""), "f2_hz": a.get("f2_hz", ""), "f3_hz": a.get("f3_hz", ""),
                "prioritat": priorities.get(row["forma"], ""),
                "decisio_auditiva": "", "variant_transcrita": "", "trets_fonetica": "", "observacions_prosodia": "", "nota_audicio": "",
            })

    by_person_rows = defaultdict(list)
    for row in sorted(selected, key=lambda r: (r["id_persona"], float(r["absolute_start_s"]), r["forma"])):
        by_person_rows[row["id_persona"]].append(row)
    lines = [
        "# Quadern d'audició: mostra equilibrada small (100 clips)",
        "",
        "Aquesta mostra cobreix els 63 parlants amb ocurrències small i les 20 formes candidates. La selecció és automàtica i serveix per començar l'escolta; no confirma cap variant.",
        "",
        "**Camps a completar al TSV:** decisió auditiva (`sí`, `no` o `incerta`), variant transcrita, trets fonètics, observacions prosòdiques i nota justificativa.",
        "",
        f"Cobertura: {len(selected)} clips · {len(by_person_rows)} parlants · {len(by_form)} formes.",
        "",
    ]
    for person in sorted(by_person_rows):
        lines += [f"## {person}", ""]
        for row in by_person_rows[person]:
            key = (row["id_persona"], row["forma"], row["clip"], row["occurrence"])
            a = acoustic.get(key, {})
            acoustic_text = ", ".join(f"{name}={a.get(name) or '—'}" for name in ("f0_hz", "f1_hz", "f2_hz", "f3_hz"))
            lines += [
                f"- **{row['forma']}** · [{Path(row['clip']).name}](clips/{Path(row['clip']).name}) · {row['absolute_start_s']}–{row['absolute_end_s']} s · p={row['prob_min']} · prioritat {priorities.get(row['forma'], '—')}",
                f"  - ASR: `{row['text']}` · {acoustic_text}",
                "  - Decisió auditiva: ____ · variant: ____ · trets fonètics: ____ · prosòdia: ____ · nota: ____",
            ]
        lines.append("")
    MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK: {OUT.name} {len(selected)} files · {len(by_person)} parlants · {len(by_form)} formes")


if __name__ == "__main__":
    main()
