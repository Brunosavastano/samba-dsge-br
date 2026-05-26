.PHONY: help check test

help:
	@echo "Targets:"
	@echo "  make check  - run lightweight repository checks"
	@echo "  make test   - run pytest"

check:
	python -m pytest --collect-only

test:
	python -m pytest

