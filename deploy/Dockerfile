# =============================================================================
# ReAgent · Docker Image
# Stage 1: Build / dependency install
# Stage 2: Runtime (slim)
# =============================================================================

# ── Build stage ──────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# System deps for building native extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir --user --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# ── Runtime stage ────────────────────────────────────────────────────────────
FROM python:3.12-slim

LABEL maintainer="edict" \
      org.opencontainers.image.title="ReAgent" \
      org.opencontainers.image.description="Intelligent Marketing AI Platform" \
      org.opencontainers.image.version="2.0.0"

# Runtime system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Application code
WORKDIR /app
COPY reagent/ reagent/
COPY pyproject.toml .

# Runtime directories
RUN mkdir -p /app/outputs

# Non-root user
RUN groupadd -r reagent && useradd -r -g reagent -d /app -s /sbin/nologin reagent
RUN chown -R reagent:reagent /app
USER reagent

# Environment variables (override via .env or docker-compose)
ENV REAGENT_DEBUG=false \
    REAGENT_LOG_LEVEL=INFO \
    REAGENT_DATABASE_URL=sqlite:///./reagent.db \
    REAGENT_CONTENT_OUTPUT_DIR=/app/outputs

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "reagent.main:app", "--host", "0.0.0.0", "--port", "8000"]
