.PHONY: install api web test lint build compose-up compose-down

install:
	python3 -m venv .venv
	.venv/bin/pip install -e ".[dev]"
	cd apps/web && npx --yes pnpm@10.6.3 install

api:
	.venv/bin/uvicorn threatatlas.main:app --host 0.0.0.0 --port $${THREATATLAS_API_PORT:-4910}

web:
	cd apps/web && npx --yes pnpm@10.6.3 dev

lint:
	.venv/bin/ruff check .

test:
	.venv/bin/pytest -q
	cd apps/web && npx --yes pnpm@10.6.3 test

build:
	cd apps/web && npx --yes pnpm@10.6.3 build

compose-up:
	docker compose up --build

compose-down:
	docker compose down --remove-orphans
