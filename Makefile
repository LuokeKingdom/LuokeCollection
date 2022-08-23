.PHONY: run build black
# ensure cpython is not generated
run:
	poetry install
	poetry run python -B index.py

black:
	poetry run black ./

# If the first argument is "version"
ifeq (version,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

version:
	poetry version $(RUN_ARGS)

build:
	pip install pyinstaller
	pyinstaller --noconsole --onefile index.py
	pyinstaller index.spec
	python build_utils.py
