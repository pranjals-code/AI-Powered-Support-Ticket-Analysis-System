# =========================
# Project configuration
# =========================
APP_MODULE=app.main:app
HOST=0.0.0.0
PORT=8000
ENV=dev

# =========================
# FastAPI
# =========================
run:
	uvicorn $(APP_MODULE) --reload --host $(HOST) --port $(PORT)

run-prod:
	uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT)

# =========================
# Alembic migrations
# =========================
migration:
	alembic revision --autogenerate -m "$(msg)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

# =========================
# Database
# =========================
db-current:
	alembic current

db-history:
	alembic history

# =========================
# Formatting & linting
# =========================
format:
	black app

lint:
	pylama app

# =========================
# Utilities
# =========================
shell:
	python

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

help:
	@echo "Available commands:"
	@echo "  make run                → Run FastAPI (dev)"
	@echo "  make run-prod           → Run FastAPI (prod)"
	@echo "  make migration msg='...'→ Create alembic migration"
	@echo "  make upgrade            → Apply migrations"
	@echo "  make downgrade          → Rollback last migration"
	@echo "  make db-current         → Show current DB revision"
	@echo "  make db-history         → Show migration history"
	@echo "  make format             → Run black"
	@echo "  make lint               → Run pylama"
	@echo "  make shell              → Python shell"
	@echo "  make clean              → Remove cache files"
