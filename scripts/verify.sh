#!/usr/bin/env bash
# La porta, en una sola ordre. Executeu-la ABANS de cada commit.
#
# Existeix perquè durant el desenvolupament d'aquest repositori van passar tres
# commits amb la porta en vermell: comprovar-ho de memòria no funciona.
set -uo pipefail
fail=0
pas() { printf '\n\033[1m▸ %s\033[0m\n' "$1"; }

pas "ruff format"; uv run ruff format --check . || fail=1
pas "ruff check";  uv run ruff check . || fail=1
pas "mypy --strict"; uv run mypy || fail=1
pas "pytest + cobertura curacio ≥ 80%"; uv run pytest --cov=src/curacio --cov-fail-under=80 || fail=1
pas "cervell render --check"; uv run cervell render docs --check || fail=1
pas "cervell cura --check"; uv run cervell cura --check || fail=1

echo
if [ "$fail" -eq 0 ]; then
  printf '\033[32m✓ tot en verd\033[0m\n'
else
  printf '\033[31m✗ la porta és vermella — no commitegeu\033[0m\n'
fi
exit "$fail"
