.DEFAULT_GOAL:= default

.PHONY: install
install:
	python -m pip install pip-tools
	python -m piptools compile --extra dev -o requirements.txt pyproject.toml
	python -m pip install -r requirements.txt

.PHONY: format
format:
	pre-commit run --all-files

.PHONY: mypy
mypy:
	mypy src/ --ignore-missing-imports

.PHONY: flint
flint: format mypy

.PHONY: build
build:
	python -m build .

.PHONY: docs
docs:
	cp ./README.md ./docs/README.md
	mkdocs build
	touch ./site/.nojekyll
	rm ./docs/README.md

.PHONY: serve-docs
serve-docs:
	cp ./README.md ./docs/README.md
	mkdocs build
	touch ./site/.nojekyll
	mkdocs serve
