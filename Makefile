MAP = maps/easy/01_linear_path.txt
VENV = .venv
PYTHON = $(VENV)/bin/python3

help:
	@echo "make install  crea .venv e instala flake8, mypy y webcolors"
	@echo "make run      ejecuta el programa (MAP=archivo para otro mapa)"
	@echo "make debug    ejecuta el programa con pdb"
	@echo "make clean    borra __pycache__ y .mypy_cache"
	@echo "make lint     pasa flake8 y mypy"
	@echo "make lint-strict  pasa flake8 y mypy --strict"

install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install flake8 mypy webcolors

run:
	$(PYTHON) main.py $(MAP)

debug:
	$(PYTHON) -m pdb main.py $(MAP)

clean:
	rm -rf __pycache__ */__pycache__ .mypy_cache

lint:
	$(PYTHON) -m flake8 . --extend-exclude .venv
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 . --extend-exclude .venv
	$(PYTHON) -m mypy . --strict --follow-untyped-imports

.PHONY: help install run debug clean lint lint-strict
