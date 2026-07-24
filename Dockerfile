# MAIA development / reproducibility image.
# Multi-stage (uv best practice): deps resolved from the lockfile in a builder,
# then copied into a slim non-root runtime with no uv and no build tooling.
# The heavier training/serving images (torch, vLLM, Unsloth) arrive at M3/M5.

# ─────────────────────────────── builder ───────────────────────────────
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Layer 1: dependencies only (cached until the lockfile changes).
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Layer 2: the project itself.
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# ─────────────────────────────── runtime ───────────────────────────────
FROM python:3.11-slim-bookworm

# Non-root user.
RUN groupadd --system --gid 999 maia \
 && useradd --system --gid 999 --uid 999 --create-home maia

COPY --from=builder --chown=maia:maia /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER maia
WORKDIR /app

# Sanity default: prove the package imports. Overridden in dev / by later services.
CMD ["python", "-c", "import maia; print('maia', maia.__version__)"]
