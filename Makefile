.PHONY: help check test dynare-smoke

help:
	@echo "Targets:"
	@echo "  make check  - run lightweight repository checks"
	@echo "  make test   - run pytest"
	@echo "  make dynare-smoke - run Dynare smoke wrapper in a temp dir"

check:
	python -m pytest --collect-only

test:
	python -m pytest

dynare-smoke:
	python src/diagnostics/run_dynare.py --mode smoke
