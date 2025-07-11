all: help

.PHONY: help up down test lint

help:
	@echo "Usage: make <command>"
	@echo ""
	@echo "Commands:"
	@echo "  up    - Build and start all Docker containers"
	@echo "  down  - Stop and remove all Docker containers"
	@echo "  test  - Run all unit tests"
	@echo "  lint  - Run linting checks"

up:
	docker-compose -f infrastructure/docker-compose.yml up --build -d

down:
	docker-compose -f infrastructure/docker-compose.yml down

test:
	pytest backend/tests/unit/
	pytest worker/tests/unit/

lint:
	# Add linting commands here (e.g., ruff check .)
