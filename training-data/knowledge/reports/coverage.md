# Estat de cobertura de Maia Knowledge

Inventari revisat el 2026-10-09. Les xifres descriuen la cua de treball, no cobertura d'entrenament aprovada.

| Estat | Documents | Significat |
|---|---:|---|
| `pending_review` | 1.421 | Encara no hi ha cap conversa candidata associada. |
| `candidate_pending_review` | 52 | Hi ha converses candidates recuperades que encara necessiten revisió de contingut o fonts. |
| `content_reviewed_rights_pending` | 1 | La pregunta, resposta i cobertura factual s'han revisat; els drets de la font encara impedeixen exportar-la. |
| `retrieval_only` | 3 | Índexs de navegació; els articles enllaçats s'inventarien separadament. |

Hi ha 409 unitats candidates de coneixement a `../work/coverage-items.jsonl`. S'han de revalidar abans de comptar-les com a cobertes. El fitxer de revisió conté 216 converses candidates; cap no passa automàticament a `output/`.

**Exportació actual: cap.** No hi ha fitxers train/validation/test preparats. La revisió de drets continua pendent per als candidats existents.
