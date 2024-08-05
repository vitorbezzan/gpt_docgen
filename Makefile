.DEFAULT_GOAL:= default

.PHONY: install
install:
	python -m pip install pip-tools
	python -m piptools compile --extra dev -o requirements.txt pyproject.toml
	python -m pip install -r requirements.txt

.PHONY: format
format:
	isort src/
	pre-commit run --all-files

.PHONY: mypy
mypy:
	mypy src/ --ignore-missing-imports

.PHONY: flint
flint: format mypy

.PHONY: build
build:
	python -m build .

.PHONY: test
test:
	pytest -rP tests/

.PHONY: docs
docs:
	cp -r docs_build/. docs_temp/
	export PYTHONPATH=$$PYTHONPATH:"./src" && sphinx-apidoc -o ./docs_temp ./src
	export PYTHONPATH=$$PYTHONPATH:"./src" && sphinx-build -b html docs_temp/ docs/
	cp -r docs_temp/.nojekyll docs/.nojekyll
	rm -rf docs_temp/
