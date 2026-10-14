# syntax=docker/dockerfile:1
# -------------------------------------------------------------------
# Stage 1: Build dependency environment using uv
# -------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install dependencies using frozen lockfile
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# -------------------------------------------------------------------
# Stage 2: Minimal runtime image
# -------------------------------------------------------------------
FROM python:3.14-slim-bookworm AS runner

WORKDIR /app

# Create non-root system user with dedicated home directory for cloud runtime compatibility
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m -d /home/appuser appuser && \
    mkdir -p /home/appuser /app/uploads && \
    chown -R appuser:appgroup /home/appuser /app

# Copy virtualenv and application source
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --chown=appuser:appgroup src ./src
COPY --chown=appuser:appgroup main.py ./main.py

# Ensure permissions on working and upload directories
RUN chown -R appuser:appgroup /app

ENV PATH="/app/.venv/bin:$PATH" \
    HOME="/home/appuser" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP="main.py" \
    HOST="0.0.0.0" \
    PORT="5000"

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import os, urllib.request; port = os.environ.get('PORT', '5000'); urllib.request.urlopen(f'http://localhost:{port}/api/v1/health', timeout=3)" || exit 1

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 4 --threads 2 --access-logfile - --error-logfile - main:app"]
