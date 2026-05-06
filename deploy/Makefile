# =============================================================================
# ReAgent · Makefile (Deployment utilities)
# =============================================================================

.PHONY: dev dev-build test prod prod-build lint clean logs

# ── Development ─────────────────────────────────────────────────────────────

dev:  ## Start development environment with hot-reload
	docker compose -f deploy/docker-compose.yml --profile dev up

dev-build:  ## Build and start development environment from scratch
	docker compose -f deploy/docker-compose.yml --profile dev up --build

dev-logs:  ## Tail development logs
	docker compose -f deploy/docker-compose.yml --profile dev logs -f

dev-down:  ## Stop development environment
	docker compose -f deploy/docker-compose.yml --profile dev down

# ── Test / Staging ──────────────────────────────────────────────────────────

test-build:  ## Build test environment
	docker compose -f deploy/docker-compose.yml --profile test build

test-up:  ## Start test environment
	docker compose -f deploy/docker-compose.yml --profile test up

# ── Production ──────────────────────────────────────────────────────────────

prod:  ## Start production environment
	docker compose -f deploy/docker-compose.yml --profile prod up -d

prod-build:  ## Build production images
	docker compose -f deploy/docker-compose.yml --profile prod build

prod-down:  ## Stop production environment
	docker compose -f deploy/docker-compose.yml --profile prod down

prod-logs:  ## Tail production logs
	docker compose -f deploy/docker-compose.yml --profile prod logs -f

# ── Utilities ───────────────────────────────────────────────────────────────

lint:  ## Run linting locally
	@echo "🔍 Running ruff check..."
	ruff check reagent/ tests/
	@echo "✅ Done"

format:  ## Auto-format code
	@echo "🎨 Formatting with ruff..."
	ruff format reagent/ tests/
	@echo "✅ Done"

test:  ## Run tests locally
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v --cov=reagent
	@echo "✅ Done"

clean:  ## Clean temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache

logs:  ## Tail all services logs
	docker compose -f deploy/docker-compose.yml logs -f

# ── Help ────────────────────────────────────────────────────────────────────

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
