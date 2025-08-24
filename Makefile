# EPL Defense API - Makefile
# Provides convenient commands for development, testing, and deployment

.PHONY: help install install-dev test test-unit test-integration test-coverage lint format clean run dev run-api build-docs install-deps update-deps clean-venv setup-dev database migrate

# Default target
help: ## Show this help message
	@echo "EPL Defense API - Available Commands:"
	@echo "======================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development Setup
setup-dev: ## Set up development environment
	@echo "🚀 Setting up development environment..."
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e .
	.venv/bin/pip install -e ".[dev]"
	@echo "✅ Development environment ready!"

install: ## Install production dependencies
	@echo "📦 Installing production dependencies..."
	pip install -e .

install-dev: ## Install development dependencies
	@echo "🔧 Installing development dependencies..."
	pip install -e ".[dev]"

install-deps: install-dev ## Alias for install-dev

update-deps: ## Update all dependencies to latest versions
	@echo "🔄 Updating dependencies..."
	pip install --upgrade -e ".[dev]"

clean-venv: ## Remove virtual environment
	@echo "🧹 Cleaning virtual environment..."
	rm -rf .venv
	@echo "✅ Virtual environment removed"

# Testing
test: ## Run all tests
	@echo "🧪 Running all tests..."
	python -m pytest tests/ -v

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	python -m pytest tests/ -v -m "not integration"

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	python -m pytest tests/ -v -m "integration"

test-coverage: ## Run tests with coverage report
	@echo "🧪 Running tests with coverage..."
	python -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html

test-fast: ## Run fast tests (skip slow ones)
	@echo "🧪 Running fast tests..."
	python -m pytest tests/ -v -m "not slow"

test-watch: ## Run tests in watch mode
	@echo "🧪 Running tests in watch mode..."
	python -m pytest tests/ -v --watch

# Code Quality
lint: ## Run linting checks
	@echo "🔍 Running linting checks..."
	flake8 app/ tests/
	pylint app/ tests/ || true

format: ## Format code with black
	@echo "🎨 Formatting code..."
	black app/ tests/
	isort app/ tests/

format-check: ## Check code formatting without making changes
	@echo "🔍 Checking code formatting..."
	black --check app/ tests/
	isort --check-only app/ tests/

# Database
database: ## Initialize database
	@echo "🗄️ Initializing database..."
	python init_database.py

migrate: ## Run database migrations
	@echo "🔄 Running database migrations..."
	alembic upgrade head

migrate-create: ## Create new migration
	@echo "📝 Creating new migration..."
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

# Running the Application
run: ## Run the FastAPI application
	@echo "🚀 Starting FastAPI application..."
	uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

run-api: run ## Alias for run

dev: run ## Alias for run

run-prod: ## Run in production mode
	@echo "🚀 Starting production server..."
	uvicorn app.main:app --host 0.0.0.0 --port 8001

# Documentation
build-docs: ## Build documentation
	@echo "📚 Building documentation..."
	# Add your documentation build commands here
	@echo "✅ Documentation built"

serve-docs: ## Serve documentation locally
	@echo "📚 Serving documentation..."
	# Add your documentation serve commands here

# Cleaning
clean: ## Clean build artifacts and cache
	@echo "🧹 Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	@echo "✅ Cleanup complete"

clean-all: clean clean-venv ## Clean everything including virtual environment

# Development Utilities
shell: ## Open Python shell with app context
	@echo "🐍 Opening Python shell..."
	python3 -c "from app.main import app; print('App loaded successfully')"

check: ## Run all checks (lint, format-check, test)
	@echo "🔍 Running all checks..."
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) test

pre-commit: check ## Run pre-commit checks

# Docker (if you use it)
docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -t epl-defense .

docker-run: ## Run Docker container
	@echo "🐳 Running Docker container..."
	docker run -p 8001:8001 epl-defense

# Database utilities
db-reset: ## Reset database (WARNING: destructive)
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? Type 'yes' to confirm: " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		rm -f epl_defense.db; \
		$(MAKE) database; \
		echo "✅ Database reset complete"; \
	else \
		echo "❌ Database reset cancelled"; \
	fi

# API utilities
openapi: ## Generate OpenAPI schema
	@echo "📋 Generating OpenAPI schema..."
	curl http://localhost:8001/openapi.json > openapi_generated.json
	@echo "✅ OpenAPI schema saved to openapi_generated.json"

# Quick development workflow
dev-setup: setup-dev install-deps database ## Complete development setup
	@echo "🎉 Development environment is ready!"
	@echo "Run 'make run' to start the application"

# Show project status
status: ## Show project status
	@echo "📊 EPL Defense API - Project Status"
	@echo "=================================="
	@echo "Python version: $(shell python3 --version)"
	@echo "Virtual env: $(shell if [ -d ".venv" ]; then echo "✅ Active"; else echo "❌ Not found"; fi)"
	@echo "Database: $(shell if [ -f "epl_defense.db" ]; then echo "✅ Found"; else echo "❌ Not found"; fi)"
	@echo "Dependencies: $(shell if [ -d ".venv" ]; then echo "✅ Installed"; else echo "❌ Not installed"; fi)"

# Player Data Sync
sync-league: ## Sync all players for a league (usage: make sync-league LEAGUE=39 SEASON=2025)
	@echo "🔄 Syncing players for league $(LEAGUE), season $(SEASON)..."
	@python3 scripts/sync_players.py --league $(LEAGUE) --season $(SEASON)

sync-team: ## Sync all players for a team (usage: make sync-team TEAM=40 SEASON=2025)
	@echo "🔄 Syncing players for team $(TEAM), season $(SEASON)..."
	@python3 scripts/sync_players.py --team $(TEAM) --season $(SEASON)

sync-premier-league: ## Sync Premier League players for current season
	@echo "🔄 Syncing Premier League players..."
	@python3 scripts/sync_players.py --league 39 --season 2025
