# ensure cpython is not generated
run:
	poetry run python -B LuokeCollection/index.py

black:
	poetry run black ./LuokeCollection

# If the first argument is "version"
ifeq (version,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

version:
	poetry version $(RUN_ARGS)