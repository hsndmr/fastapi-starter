SHELL := /bin/bash
VENV := .venv
ACTIVATE := source $(VENV)/bin/activate

.PHONY: help venv install install-dev dev run test lint format docker-build docker-run clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

venv: ## Create virtual environment
	python3 -m venv $(VENV)
	@echo "Activate: source $(VENV)/bin/activate"

install: ## Install dependencies
	$(ACTIVATE) && uv sync

install-dev: ## Install with dev dependencies
	$(ACTIVATE) && uv sync --group dev

dev: ## Start dev server with hot reload
	$(ACTIVATE) && fastapi dev app/main.py

run: ## Start production server
	$(ACTIVATE) && fastapi run --workers 4 app/main.py

test: ## Run tests with coverage
	$(ACTIVATE) && coverage run -m pytest && coverage report

lint: ## Run linting and type checks
	$(ACTIVATE) && ruff check app tests && mypy app

format: ## Format code with ruff
	$(ACTIVATE) && ruff check --fix app tests && ruff format app tests

docker-build: ## Build Docker image
	docker build -t fastapi-starter .

docker-run: ## Run Docker container
	docker run -p 8000:8000 --env-file .env fastapi-starter

clean: ## Remove cache and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov .coverage
